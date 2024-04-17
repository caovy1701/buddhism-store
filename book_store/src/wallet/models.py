from django.db import models
from django.contrib.auth import get_user_model
from django.db import transaction
# Create your models here.

User = get_user_model()


class Bankname(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Wallet'


class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bank_account')
    bank_name = models.ForeignKey(Bankname, on_delete=models.CASCADE, related_name='bank_account')
    account_number = models.CharField(max_length=50)
    account_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username} Bank Account'

class Transaction(TimeStampedModel):
    class TransactionType(models.TextChoices):
        DEPOSIT = 'deposit'
        WITHDRAW = 'withdraw'
        REFUND = 'refund'
        CHARGE = 'charge'

    class TransactionStatus(models.TextChoices):
        PENDING = 'pending'
        SUCCESS = 'success'
        FAILED = 'failed'
        CANCELLED = 'cancelled'

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.PositiveIntegerField()
    description = models.TextField()
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    transaction_status = models.CharField(max_length=20, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)

    def __str__(self):
        return f'{self.wallet.user.username} Transaction'
    
    class Meta:
        ordering = ['-created_at']
        

class TransactionHistory(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='transaction_history')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_history')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"< {self.user.username} - {self.transaction.description} - {self.amount} - {self.transaction.transaction_type} >"

    class Meta:
        ordering = ['-transaction__created_at']
