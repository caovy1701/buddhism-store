# Generated by Django 3.2 on 2024-04-17 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bankname',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('transaction_type', models.CharField(choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw'), ('refund', 'Refund'), ('charge', 'Charge')], max_length=20)),
                ('transaction_status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_history', to='wallet.transaction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-transaction__created_at'],
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='wallet.wallet'),
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=50)),
                ('account_name', models.CharField(max_length=100)),
                ('bank_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_account', to='wallet.bankname')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bank_account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]