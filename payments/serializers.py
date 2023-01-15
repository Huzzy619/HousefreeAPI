from rest_framework import serializers
from .models import Payment
from django.contrib.auth.models import User
from django.conf import settings
import requests

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

class PaystackPaymentSerializer(serializers.ModelSerializer):
	amount = serializers.IntegerField()
	email = serializers.EmailField()

	def validate_email(self, value):
		if User.objects.filter(email=value).exists():
			return value
		raise serializers.ValidationError({"detail": "Email not found"})

	def save(self):
		user = self.context['request'].user
		data = self.validated_data
		url = 'https://api.paystack.co/transaction/initialize'
		headers = {
			"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
			"Content-Type": "application/json"
		}
		response = requests.post(url, headers=headers, json=data)
		response_data = response.json()
		if response.status_code != 200:
			raise Exception(response_data['message'])
		Payment.objects.create(
			user=user,
			amount=data['amount'],
			email=user.email,
			verified=False
		)
		return response_data

class CreateCardDepositFlutterwaveSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    email = serializers.EmailField()

    def validate(self, data):
        user = data.get("user")
        amount = data.get("amount")
        email = data.get("email")

        if amount is None:
            raise serializers.ValidationError("amount is required")
        
        if email is None:
            raise serializers.ValidationError("email is required")
        return data