from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    metadata = serializers.JSONField(required=False)

    def validate_metadata(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("metadata must be a dictionary.")
        if 'product_name' not in value:
            raise serializers.ValidationError("metadata must contain a product_name key.")
        if len(value['product_name']) > 100:
            raise serializers.ValidationError("product_name must be less than 100 characters.")
        return value

    class Meta:
        model = Payment
        fields = ('id', 'user', 'email', 'amount', 'txn_ref', 'verified', 'payment_options', 'created_at', 'updated_at', 'metadata')
        read_only_fields = ('txn_ref', 'created_at', 'updated_at')
