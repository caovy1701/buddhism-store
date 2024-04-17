from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import View, TemplateView, ListView, DetailView

# Create your views here.
from src.wallet.models import Wallet


User = get_user_model()


class WalletView(TemplateView):
    template_name = "wallet.html"

    def get_context_data(self, **kwargs):
        context = super(WalletView, self).get_context_data(**kwargs)
        context['wallet'] = Wallet.objects.get(user=self.request.user)
        return context