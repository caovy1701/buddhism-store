from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, View

# Create your views here.
from src.wallet.models import Wallet

User = get_user_model()


class WalletView(TemplateView, LoginRequiredMixin):
    template_name = "users/user_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(WalletView, self).get_context_data(**kwargs)
        context["wallet"] = Wallet.objects.get(user=self.request.user)
        return context
