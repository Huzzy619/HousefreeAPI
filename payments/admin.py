from django.contrib import admin

from .models import Payment, Wallet, TransactionIntent, PaymentPlan, BankDetail


admin.site.register([Payment, Wallet, TransactionIntent, PaymentPlan, BankDetail])
