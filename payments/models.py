import random
import string
from django.contrib.auth import get_user_model
from django.db import models
from uuid import uuid4

from RentRite.models import BaseModel


class PaymentGateway(models.TextChoices):
    PAYSTACK = "paystack"
    FLUTTERWAVE = "flutterwave"


class PaymentPlan(BaseModel):
    class Term(models.TextChoices):
        MONTHLY = "month"
        BI_WEEKLY = "bi-weekly"
        SIX_MONTHS = "6-months"
        ANNUALLY = "year"

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    term = models.CharField(max_length=50, choices=Term, default=Term.MONTHLY)
    property_listings = models.IntegerField()
    premium_listings = models.IntegerField()
    post_boost = models.IntegerField()
    plan_code = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.term}"


class TransactionIntent(BaseModel):
    class TransactionStatus(models.TextChoices):
        CREATED = "CREATED"
        PROCESSING = "PROCESSING"
        COMPLETED = "COMPLETED"
        FAILED = "FAILED"


    user = user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True
    )
    payment_plan = models.ForeignKey(
        PaymentPlan, on_delete=models.SET_NULL, blank=True, null=True
    )
    payment_gateway = models.CharField(max_length=255, choices=PaymentGateway)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    transaction_uid = models.UUIDField(default=uuid4)
    status = models.CharField(
        max_length=255,
        choices=TransactionStatus.choices,
        default=TransactionStatus.CREATED,
    )

    def __str__(self) -> str:
        return f"{self.transaction_uid} - {self.status}"


class Subscription(BaseModel):
    start_date = models.DateTimeField(auto_now=True)
    payment_plan = models.ForeignKey(
        PaymentPlan, on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(null=True, blank=True)
    subscription_code = models.CharField(null=True, blank=True)
    email_token = models.CharField(null=True, blank=True)


class Payment(BaseModel):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True
    )
    email = models.EmailField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    txn_ref = models.CharField(max_length=200, unique=True)
    verified = models.BooleanField(default=False)
    payment_plan = models.ForeignKey(
        PaymentPlan, on_delete=models.SET_NULL, blank=True, null=True
    )
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment of {self.amount} by {self.user} on {self.created_at}"


class Wallet(BaseModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=0)
    currency = models.CharField(default="NGN", max_length=100)
    account_id = models.IntegerField(default=1, null=True)

    def account_id_generator(self, length=10, chars=string.digits):
        value = "".join(random.choice(chars) for _ in range(length))
        while self.__class__.objects.filter(account_id=value).exists():
            value = "".join(random.choice(chars) for _ in range(length))

        return int(value)

    def __str__(self):
        return f"{self.user}: {self.balance} {self.currency}"

    def save(self, **kwargs) -> None:
        if not self.account_id:
            self.account_id = self.account_id_generator()
        return super().save(**kwargs)


class BankDetail(BaseModel):
    account_number = models.IntegerField()
    account_name = models.CharField(max_length=500)
    bank_name = models.CharField(max_length=500)
