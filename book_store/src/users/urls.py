from django.urls import path
from src.users.views import (
    ContactView,
    CreateAddressView,
    DeleteAddressView,
    LoginViewCustom,
    PasswordChangeView,
    PasswordResetConfirmViewCustom,
    PasswordResetViewCustom,
    ProfileView,
    UpdateAddressView,
    UserCreateView,
    logout_view,
)

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", LoginViewCustom.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("account/", PasswordChangeView.as_view(), name="account"),
    path("address/", CreateAddressView.as_view(), name="address"),
    path("address/<int:pk>/", UpdateAddressView.as_view(), name="address"),
    path(
        "address/<int:pk>/delete/", DeleteAddressView.as_view(), name="delete_address"
    ),
    path("password_reset/", PasswordResetViewCustom.as_view(), name="password_reset"),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        PasswordResetConfirmViewCustom.as_view(),
        name="password_reset_confirm",
    ),
    path("contact/", ContactView.as_view(), name="contact"),
    path("logout/", logout_view, name="logout"),
]
