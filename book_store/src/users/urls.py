from src.users.views import UserCreateView, LoginViewCustom, logout_view, ProfileView
from django.urls import path

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginViewCustom.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', logout_view, name='logout'),
]