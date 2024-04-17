from django.urls import path

from src.wallet.views import WalletView

urlpatterns = [
    path('wallet/', WalletView.as_view(), name='wallet'),
]
