from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField
import uuid

# Create your models here.


class Payment(models.Model):
    name = models.CharField(blank=False, max_length=30, verbose_name="name")
    email = models.EmailField(unique=True, verbose_name="email", blank=False)
    phone = PhoneNumberField(null=True, verbose_name="phone number")
    date_created = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=40, blank=False)
    agent_email = models.CharField(max_length=150, blank=False)
    apartment_id = models.CharField(max_length=500, blank=False)


class PaymentHistory(models.Model):

    history_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, unique=True
    )
    sender = models.CharField(blank=False, max_length=30, null=True)
    recipient = models.CharField(max_length=60, blank=True, null=True)
    phone = models.CharField(blank=False, max_length=30, null=True)
    date_sent = models.CharField(max_length=60, blank=True, null=True)
    amount = models.CharField(max_length=40, blank=False)
    agent_account_number = models.CharField(max_length=150, blank=False)
    account_number = models.CharField(max_length=20, null=True)
    history_time = models.DateTimeField(auto_now_add=True)
    account_bank = models.CharField(max_length=4, null=True)
    narration = models.CharField(max_length=200, null=True)
    reference = models.CharField(max_length=150, blank=True, null=True)
    debit_currency = models.CharField(null=True, max_length=3)
    account_id = models.CharField(max_length=60, blank=True, null=True)
    transaction_status = models.CharField(max_length=12, null=True)
    withdrawal_date = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        ordering = ["-history_time"]


class Withdrawal(models.Model):
    currency_choice = [("USD", "USD"), ("NGN", "NGN")]
    
    account_number = models.CharField(max_length=20)
    account_bank = models.CharField(max_length=4)
    amount = models.CharField(max_length=20)
    narration = models.CharField(max_length=200)
    currency = models.CharField(choices=currency_choice, max_length=3)
    reference = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    email = models.EmailField()
    debit_currency = models.CharField(choices=currency_choice, max_length=3)
    account_id = models.CharField(max_length=60)
    withdrawal_date = models.DateTimeField(auto_now_add=True)
