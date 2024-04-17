from django.contrib import admin

# Register your models here.
from src.wallet.models import BankAccount, Bankname, TransactionHistory, Wallet, Transaction


class BanknameAdmin(admin.ModelAdmin):
    list_display = ['name']


class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'bank_name', 'account_number', 'account_name']


class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'amount', 'description', 'transaction_type', 'transaction_status']


class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ['transaction']


admin.site.register(Bankname, BanknameAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionHistory, TransactionHistoryAdmin)

