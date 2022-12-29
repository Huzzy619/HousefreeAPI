from .models import Payment, PaymentHistory, Withdrawal
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    House_location = serializers.CharField(max_length=150)

    class Meta:
        model = Payment
        fields = [
            "amount",
            "email",
            "name",
            "phone",
            "agent_email",
            "apartment_id",
            "House_location",
        ]


class PaymentHistorySerializer(serializers.Serializer):
    class Meta:
        model = PaymentHistory
        depth = 1
        fields = [
            "sender",
            "recipient",
            "phone",
            "date_sent",
            "agent_account_number",
            "narration",
            "reference",
            "transaction_status",
            "amount",
            "history_time",
            "short_id",
        ]


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = [
            "account_number",
            "account_bank",
            "amount",
            "narration",
            "currency",
            "reference",
            "email",
            "debit_currency",
            "account_id",
        ]

        def __str__(self):
            return self.amount
