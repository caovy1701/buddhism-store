from django.shortcuts import render, redirect
from src.users.models import User, Address
from src.users.forms.accounts import (
    CustomUserCreationForm,
    UserProfileUpdateForm,
    AddressForm,
    ChangePasswordForm,
    ResetPasswordCustomForm,
    PasswordResetConfirmForm,
)
from src.users.forms.contact_form import ContactForm
from django.views.generic import (
    CreateView,
    TemplateView,
    FormView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

# Create your views here.

User = get_user_model()


class UserCreateView(CreateView):
    model = User
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = "/users/login/"

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


# Login View
class LoginViewCustom(TemplateView):
    template_name = "users/login.html"

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        print(user)
        if user:
            login(request, user)
            return HttpResponseRedirect("/")
        message = "Invalid credentials"
        print(message)
        return render(request, self.template_name, {"message": message})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


# Profile View
class ProfileView(LoginRequiredMixin, FormView):
    template_name = "users/profile.html"
    success_url = "/users/profile/"

    def post(self, request, *args, **kwargs):
        type_form = request.POST.get("type")
        user = request.user
        address = Address.objects.filter(user=user).first()
        # check user has address
        if not address:
            address = Address(user=user)
            address.save()

        if type_form == "profile":
            profile_form = UserProfileUpdateForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect("profile")
            else:
                form = profile_form.errors
        elif type_form == "address":
            address_form = AddressForm(request.POST, instance=address)
            if address_form.is_valid():
                address_form.save()
                return redirect("profile")
            else:
                form = address_form.errors
        elif type_form == "password_change":
            password_form = ChangePasswordForm(request.POST, instance=user)
            if password_form.is_valid():
                password_form.save()
                # logout user
                logout(request)
                return redirect("profile")
            else:
                form = password_form.errors
        return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        user = request.user
        address = Address.objects.filter(user=user).first()
        return render(request, self.template_name, {"user": user, "address": address})


class PasswordResetViewCustom(FormView):
    template_name = "users/password_reset_form.html"
    form_class = ResetPasswordCustomForm
    success_url = "/users/login/"

    def form_valid(self, form):
        form.save(request=self.request)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            form = ResetPasswordCustomForm(request.POST)
            if form.is_valid():
                form.save(request=self.request)
                return HttpResponseRedirect("/users/login/")
            else:
                return render(request, self.template_name, {"form": form})
        return render(request, self.template_name, {"form": form})


class PasswordResetConfirmViewCustom(FormView):
    template_name = "users/password_reset_confirm.html"
    form_class = PasswordResetConfirmForm
    success_url = "/users/login/"

    def post(self, request, *arg, **kwargs):
        uidb64 = self.kwargs.get("uidb64")
        token = self.kwargs.get("token")
        user_id = urlsafe_base64_decode(uidb64)
        user = User.objects.filter(id=user_id).first()
        if user and default_token_generator.check_token(user, token):
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                form.save(uid=uidb64, token=token)
                return HttpResponseRedirect("/users/login/")
            else:
                return render(request, self.template_name, {"form": form})
        return HttpResponseRedirect("/users/login/")


# Logout View
def logout_view(request):
    logout(request)
    return redirect("login")


class ContactView(FormView):
    template_name = "users/contact.html"
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = ContactForm(data)
        if form.is_valid():
            form.send_email(request)
            return HttpResponseRedirect("/")
        return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": ContactForm()})
