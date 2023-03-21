from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Payment, PaymentPlan

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


class CreateCardDepositFlutterwaveSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    email = serializers.EmailField()
    metadata = serializers.JSONField()
    payment_plan = serializers.CharField()
    
class CreatePaystackPaymentSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    email = serializers.EmailField()
    plan_id = serializers.CharField()
    metadata = serializers.JSONField()


class PlanSerializer(serializers.ModelSerializer):

    class Meta: 
        model = PaymentPlan
        exclude = ('id',)
        # fields = "__all__"



class PaymentHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['id','amount', 'payment_plan']