import hashlib
import hmac

from django.conf import settings
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payments.models import PaymentGateway

from .tasks import process_paystack_payment_in_background
from drf_spectacular.utils import extend_schema


@extend_schema(exclude=True)
@api_view(http_method_names=["POST"])
def paystack_webhook(request: HttpRequest, *args, **kwargs):
    signature = hmac.new(
        bytes(settings.PAYSTACK_SECRET_KEY, "latin-1"),
        msg=request.body,
        digestmod=hashlib.sha512,
    ).hexdigest()

    if not signature == request.headers.get("x-paystack-signature", ""):
        return Response("You are not paystack", status=status.HTTP_403_FORBIDDEN)

    process_paystack_payment_in_background(
        payment_gateway=PaymentGateway.PAYSTACK, payment_data=request.data
    )
    # We would not use background task for now cos of cost of an extra process running.
    # process_paystack_payment_in_background.delay(
    #     payment_gateway=PaymentGateway.PAYSTACK, payment_data=request.data
    # )

    return Response("OK")
