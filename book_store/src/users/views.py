from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import urlsafe_base64_decode
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    RedirectView,
    TemplateView,
    UpdateView,
)
from src.users.forms.accounts import (
    AddressForm,
    ChangePasswordForm,
    CustomUserCreationForm,
    PasswordResetConfirmForm,
    ResetPasswordCustomForm,
    UserProfileUpdateForm,
)
from src.users.forms.contact_form import ContactForm
from src.users.models import Address, User

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
        return super().form_invalid(form)


# Login View
class LoginViewCustom(TemplateView):
    template_name = "users/login.html"

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect("/")
        message = "Invalid credentials"
        return render(request, self.template_name, {"message": message})

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name, {})


# Profile View
class ProfileView(LoginRequiredMixin, RedirectView):
    template_name = "users/user_dashboard.html"
    form_class = UserProfileUpdateForm

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.update()
            return redirect("profile")
        messages = form.errors
        return render(request, self.template_name, {"messages": messages})


class PasswordChangeView(LoginRequiredMixin, RedirectView):
    template_name = "users/user_dashboard.html"
    form_class = ChangePasswordForm

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("account")
        messages = form.errors
        return render(request, self.template_name, {"messages": messages})


class CreateAddressView(LoginRequiredMixin, CreateView):
    template_name = "users/user_dashboard.html"
    form_class = AddressForm
    model = Address

    def get(self, request, *args, **kwargs):
        user = request.user
        addresses = Address.objects.filter(user=user)
        if kwargs.get("pk"):
            address = Address.objects.get(pk=kwargs.get("pk"))
            return render(
                request,
                self.template_name,
                {"addresses": addresses, "address": address},
            )
        return render(request, self.template_name, {"addresses": addresses})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save(user)
            return redirect("address")
        messages = form.errors
        return render(request, self.template_name, {"messages": messages})


class UpdateAddressView(LoginRequiredMixin, UpdateView):
    template_name = "users/user_dashboard.html"
    form_class = AddressForm
    model = Address

    def get(self, request, *args, **kwargs):
        user = request.user
        addresses = Address.objects.filter(user=user)
        address = Address.objects.get(pk=kwargs.get("pk"))
        return render(
            request, self.template_name, {"addresses": addresses, "address": address}
        )

    def post(self, request, *args, **kwargs):
        user = request.user
        address = Address.objects.get(pk=kwargs.get("pk"))
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save(user)
            return redirect("address")
        messages = form.errors
        return render(request, self.template_name, {"messages": messages})


class DeleteAddressView(LoginRequiredMixin, DeleteView):
    template_name = "users/user_dashboard.html"
    model = Address

    def post(self, request, *args, **kwargs):
        address = Address.objects.get(pk=kwargs.get("pk"))
        address.delete()
        return redirect("address")


class PasswordResetViewCustom(FormView):
    template_name = "users/password_reset_form.html"
    form_class = ResetPasswordCustomForm
    success_url = "/users/login/"

    def form_valid(self, form):
        form.save(request=self.request)
        return super().form_valid(form)

    def form_invalid(self, form):
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
