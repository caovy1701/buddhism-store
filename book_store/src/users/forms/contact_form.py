from django import forms
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from src.users.models import Contact
from django.conf import settings
from src.users.models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField()
    phone = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Contact
        fields = ["name", "phone", "email", "message"]

    def send_email(self, request):
        name = self.cleaned_data["name"]
        phone = self.cleaned_data["phone"]
        email = self.cleaned_data["email"]
        message = self.cleaned_data["message"]

        # send thank you email
        subject = "Thank you for contacting us"
        html_message = render_to_string(
            "users/contact_email.html",
            {
                "name": name,
                "phone": phone,
                "email": email,
                "message": message,
            },
        )
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = email
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        # send notification email
        subject = "New contact"
        html_message = render_to_string(
            "users/contact_notification.html",
            {
                "name": name,
                "phone": phone,
                "email": email,
                "message": message,
            },
        )
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = settings.EMAIL_HOST_USER
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        Contact.objects.create(name=name, phone=phone, email=email, message=message)
        return True

    def save(self, commit=True):
        return super().save(commit=commit)
