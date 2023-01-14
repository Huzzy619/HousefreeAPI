from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Payment, Wallet
from .serializers import CreateCardDepositFlutterwaveSerializer, PaymentSerializer, PaystackPaymentSerializer
from rave_python.rave_exceptions import RaveError, IncompletePaymentDetailsError
from rave_python.rave_payment import Payment
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework import permissions
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
import requests

User = get_user_model()

class PaymentView(generics.GenericAPIView):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		# Get Rave API keys from settings
		rave = Payment(settings.RAVE_PUBLIC_KEY, settings.RAVE_SECRET_KEY)

		try:
			# Make payment
			response = rave.card.charge(request.data['amount'], request.data['email'], request.data['txn_ref'], request.data['metadata']['product_name'])
			if response['status'] == 'success':
				serializer.save(verified=True)
				return Response(response, status=status.HTTP_201_CREATED)
			else:
				return Response(response, status=status.HTTP_400_BAD_REQUEST)
		except (RaveError, IncompletePaymentDetailsError) as e:
			return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateCardDepositFlutterwaveAPIView(generics.GenericAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = CreateCardDepositFlutterwaveSerializer
	
	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		payment = Payment.objects.create(
			user=request.user,
			amount=serializer.validated_data['amount'],
			email=serializer.validated_data['email'],
			verified=False,
			payment_option='flutterwave'
		)
		payment.save()
		endpoint = "https://api.flutterwave.com/v3/payments"
		scheme = request.is_secure() and "https" or "http"
		full_url = scheme +"://"+ str(get_current_site(request).domain) + "/api/billpayments/pay/card-deposit/confirm-card-deposit/"
		headers = {
			"Authorization": f"Bearer {settings.FLW_SECRET_KEY}"
		}
		json = {
			"tx_ref": payment.txn_ref,
			"amount": payment.amount,
			"currency": "NGN",
			"redirect_url": full_url,
			"meta": {
				"customer_id": request.user.id,
			},
			"customer": {
				"email": serializer.validated_data['email'],
				"phonenumber": request.user.profile.phone,
				"name": request.user.username,
			},
			"customizations": {
				"title": "Ome NGN Card Deposit Payments",
				"logo": "logo image here"
			}
		}
		try:
			response = requests.post(endpoint, json=json, headers=headers)
			try:
				if response.json()['status'] == "success":
					payment_link = response.json()['data']['link']
					return Response({"success": payment_link}, status=status.HTTP_200_OK)
				else:
					error = response.json()
					return Response({"error": {"some error occurred": str(error)}}, status=status.HTTP_400_BAD_REQUEST)
			except Exception as error:
				return Response({"error": {"something went wrong": str(error)}}, status=status.HTTP_400_BAD_REQUEST)    

		except Exception as error:
			return Response({"error": {"something went wrong":str(error)}}, status=status.HTTP_400_BAD_REQUEST)

flutterwave_card_deposit = CreateCardDepositFlutterwaveAPIView.as_view()


class ConfirmCardDepositFlutterwave(generics.GenericAPIView):
	"""
	webhook to confirm card deposit and increase associated user balance
	"""
	def get(self, request):
		tx_status = self.request.query_params.get('status')
		tx_ref = self.request.query_params.get('tx_ref')
		transaction_id = request.query_params.get('transaction_id')
		print(f"tx ref is {tx_ref} and tx status is {tx_status} and transaction id is {transaction_id}")
		
		if tx_status == 'successful':
			url = f"https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref={tx_ref}"
			headers = {
				"Authorization": f"Bearer {settings.FLW_SECRET_KEY}"
			}
			response = requests.get(url, headers=headers)
			print(response.status_code, response.text)
			response = response.json()
			transactionDetails = Payment.objects.filter(txn_ref=tx_ref).first()		
			if response['data']['amount'] == transactionDetails.amount and response['data']['currency'] == "NGN":
				transactionDetails.verified = True
				print("txn verified now increase user wallet balance")
				recipient = transactionDetails.user
				user_wallet = Wallet.objects.filter(user=recipient, currency="NGN").first()
				if user_wallet.currency == "NGN":
					user_wallet.balance += transactionDetails.amount
					user_wallet.save()
					return Response({"success": "successful deposit"}, status=status.HTTP_200_OK)
				return Response({"error": {"something went wrong": "error"}}, status=status.HTTP_400_BAD_REQUEST)	
			else:
				# Inform the customer their payment was unsuccessful
				print("unsuccessful payment")
				return Response({"error": {"something went wrong": "unsuccessful payment"}}, status=status.HTTP_400_BAD_REQUEST)	

		return Response({"error": {"something went wrong": "unsuccessful payment"}}, status=status.HTTP_400_BAD_REQUEST)	
	
flutterwave_confirm_card_deposit = ConfirmCardDepositFlutterwave.as_view()


class PaystackPaymentView(CreateAPIView):
	serializer_class = PaystackPaymentSerializer
	permission_classes = (IsAuthenticated,)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class VerifyPaystackPayment(APIView):
	def get(self, request, reference):
		payment = Payment.objects.get(txn_ref=reference)
		verified = payment.verify_payment()
		if verified:
			# do some things
			return Response({"message": "Verified payment successfully"}, status=status.HTTP_200_OK)
		return Response({"message": "Payment Verification Failed"}, status=status.HTTP_400_BAD_REQUEST)

verify_paystack_payment = VerifyPaystackPayment.as_view()