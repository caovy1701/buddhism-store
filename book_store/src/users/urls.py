from src.users.views import (
    UserCreateView,
    LoginViewCustom,
    logout_view,
    ProfileView,
    PasswordResetConfirmViewCustom,
    PasswordResetViewCustom,
    ContactView,
)
from django.urls import path

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", LoginViewCustom.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("password_reset/", PasswordResetViewCustom.as_view(), name="password_reset"),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        PasswordResetConfirmViewCustom.as_view(),
        name="password_reset_confirm",
    ),
    path("contact/", ContactView.as_view(), name="contact"),
    path("logout/", logout_view, name="logout"),
]
