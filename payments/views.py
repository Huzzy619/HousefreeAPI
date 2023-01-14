from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer, PaystackPaymentSerializer
from rave_python.rave_exceptions import RaveError, IncompletePaymentDetailsError
from rave_python.rave_payment import Payment
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

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