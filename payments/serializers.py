from rest_framework import serializers
from .models import Payment
from django.contrib.auth.models import User
from django.conf import settings
import requests
import json
from django.core.serializers.json import DjangoJSONEncoder

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
	metadata = serializers.JSONField()
	
	def validate(self, data):
		request = self.context.get('request')
		user = request.user
		amount = data.get("amount")
		email = data.get("email")
		metadata = data.get("metadata")
		# json.dumps(user, cls=DjangoJSONEncoder)

		if amount is None:
			raise serializers.ValidationError("amount is required")
		
		if email is None:
			raise serializers.ValidationError("email is required")
		
		if metadata is None:
			raise serializers.ValidationError("metadata is required")
		
		return data