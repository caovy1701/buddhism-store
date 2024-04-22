from django import forms
from django.conf import settings

# Message
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

# Email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from src.users.models import Address, User

User = get_user_model()


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password", "confirm_password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "phone_number"]

    def update(self, *args, **kwargs):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.save(
            update_fields=[
                "email",
                "username",
                "first_name",
                "last_name",
                "phone_number",
            ]
        )
        return user

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["address", "city", "district", "ward", "street", "note", "is_default"]

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, user, *args, **kwargs):
        # check maximum address is 3
        address_pk = self.instance.pk
        print(address_pk)
        if not address_pk:
            if Address.objects.filter(user=user).count() >= 3:
                messages.error("You can only have 3 addresses")
                return None
        address = super().save(commit=False)
        address.user = user
        address.save()
        return address


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        old_password = cleaned_data.get("old_password")
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        if not self.instance.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect")
        return cleaned_data

    def save(self):
        self.instance.set_password(self.cleaned_data["new_password"])
        self.instance.save(update_fields=["password"])
        return self.instance


class ResetPasswordCustomForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            raise forms.ValidationError("Email does not exist")
        return cleaned_data

    def save(self, request, *args, **kwargs):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).first()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        current_site = get_current_site(request)
        mail_subject = "Reset your password"
        message = render_to_string(
            "users/reset_password_email.html",
            {
                "user": user,
                "domain": current_site,
                "uid": uid,
                "token": token,
                "reset_password_url": f"{current_site}{reverse('password_reset_confirm', args=[uid, token])}",
                "site_name": "Book Store",
                "url": "http://localhost:8000",
            },
        )
        plain_message = strip_tags(message)
        send_mail(
            mail_subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message=message,
        )
        return self.cleaned_data


class PasswordResetConfirmForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, uid, token):
        uid = urlsafe_base64_decode(uid)
        user = User.objects.filter(pk=uid).first()
        password = self.cleaned_data["new_password"]
        if user and default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save(update_fields=["password"])
            return user
        return None
