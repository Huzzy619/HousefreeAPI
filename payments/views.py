from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
from rave_python.rave_exceptions import RaveError, IncompletePaymentDetailsError
from rave_python.rave_payment import Payment

class PaymentView(generics.GenericAPIView):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		# Get Rave API keys from settings
		rave = Payment(RAVE_PUBLIC_KEY, RAVE_SECRET_KEY)

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
