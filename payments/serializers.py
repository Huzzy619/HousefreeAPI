from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import BankDetail, Payment, PaymentGateway, PaymentPlan

User = get_user_model()


class PaystackPaymentSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()
    email = serializers.EmailField()

    class Meta:
        model = Payment
        fields = ["amount", "email", "metadata"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            return value
        raise serializers.ValidationError({"detail": "Email not found"})


class PaymentInputSerializer(serializers.Serializer):
    payment_gateway = serializers.ChoiceField(PaymentGateway.choices)
    payment_plan_id = serializers.IntegerField()
    callback_url = serializers.URLField()

    def validate(self, attrs):
        if not PaymentPlan.objects.filter(id=attrs["payment_plan_id"]).exists():
            raise serializers.ValidationError({"detail": "Payment plan not found"})
        return attrs


class PaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        exclude = ["plan_code"]


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "amount", "payment_plan"]


class SubscriptionInfoSerializer(serializers.Serializer):
    email = serializers.EmailField()
    account_id = serializers.IntegerField()
    current_subscription = serializers.CharField()


class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = ["account_name", "account_number", "bank_name"]
