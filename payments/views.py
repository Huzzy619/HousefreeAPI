import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from decouple import config
from django.http import HttpRequest

from .models import Payment, Wallet
from .serializers import CreateCardDepositFlutterwaveSerializer, CreatePaystackPaymentSerializer

User = get_user_model()


class CreateCardDepositFlutterwaveAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateCardDepositFlutterwaveSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return super().get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = Payment.objects.create(
            user=request.user,
            amount=serializer.validated_data["amount"],
            email=serializer.validated_data["email"],
            verified=False,
            payment_options="flutterwave",
            payment_plan=serializer.validated_data["payment_plan"],
            metadata=serializer.validated_data["metadata"],
        )
        endpoint = "https://api.flutterwave.com/v3/payments"
        
        # full_url = (
        #     scheme
        #     + "://"
        #     + str(request.get_host())
        #     + "/payments/flw-deposit/verify/"
        # )
        headers = {"Authorization": f"Bearer {settings.FLW_SECRET_KEY}"}
        json_data = {
            "tx_ref": payment.txn_ref,
            "amount": payment.amount,
            "currency": "NGN",
            "redirect_url": request.scheme + "://" + config("FRONTEND_URL", ""),
            "payment_plan": serializer.validated_data["payment_plan"],
            "meta": {
                "customer_id": request.user.profile.id or "xxxxxxxxxxxxxxxx",
            },
            "customer": {
                "email": serializer.validated_data["email"],
                "phonenumber": request.user.profile.phone or "090000000000",
                "name": request.user.username or "customer name",
            },
            "customizations": {
                "title": "RentRite NGN Card Deposit Payments",
                "logo": "https://images.unsplash.com/photo-1554995207-c18c203602cb?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80",
            },
        }
        try:
            response = requests.post(endpoint, json=json_data, headers=headers)
            try:
                if response.json()["status"] == "success":
                    payment_link = response.json()["data"]["link"]
                    return Response(
                        {"success": payment_link}, status=status.HTTP_200_OK
                    )
                else:
                    error = response.json()
                    return Response(
                        {"error": {"some error occurred": str(error)}},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Exception as error:
                return Response(
                    {"error": {"something went wrong": str(error)}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as error:
            return Response(
                {"error": {"something went wrong": str(error)}},
                status=status.HTTP_400_BAD_REQUEST,
            )


flutterwave_card_deposit = CreateCardDepositFlutterwaveAPIView.as_view()


class ConfirmCardDepositFlutterwave(generics.GenericAPIView):
    """
    webhook to confirm card deposit and increase associated user balance
    """

    def get(self, request):
        tx_status = self.request.query_params.get("status")
        tx_ref = self.request.query_params.get("tx_ref")
        transaction_id = request.query_params.get("transaction_id")

        if tx_status == "successful":
            url = f"https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref={tx_ref}"
            headers = {"Authorization": f"Bearer {settings.FLW_SECRET_KEY}"}
            response = requests.get(url, headers=headers)
            response = response.json()
            transactionDetails = Payment.objects.filter(txn_ref=tx_ref).first()
            if (
                response["data"]["amount"] == transactionDetails.amount
                and response["data"]["currency"] == "NGN"
            ):
                transactionDetails.verified = True
                transactionDetails.save()
                recipient = transactionDetails.user
                user_wallet = Wallet.objects.filter(user=recipient).first()
                user_wallet.balance += transactionDetails.amount
                user_wallet.save()
                return Response(
                    {"success": "successful deposit"}, status=status.HTTP_200_OK
                )
            else:
                # Inform the customer their payment was unsuccessful
                return Response(
                    {"error": {"something went wrong": "unsuccessful payment"}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {
                "error": {
                    "something went wrong": "payment could not be verified, contact the admin"
                }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


flutterwave_confirm_card_deposit = ConfirmCardDepositFlutterwave.as_view()


class PaystackPaymentView(APIView):
    serializer_class = CreatePaystackPaymentSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request: HttpRequest, *args, **kwargs):
        serializer = CreatePaystackPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        metadata = serializer.validated_data["metadata"]

        payment = Payment.objects.create(
            user=user,
            amount=serializer.validated_data["amount"],
            email=user.email,
            verified=False,
            payment_options="paystack",
            metadata=metadata,
        )

        # callback_url = (
        #     request.scheme
        #     + "://"
        #     + request.get_host()
        #     + "/payments/paystack-deposit/verify/"
        # )

        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": user.email,
            "plan": serializer.validated_data['plan_id'],
            "amount": serializer.validated_data['amount'],
            "callback_url":  request.scheme + "://" + config("FRONTEND_URL", ""),
            "reference": payment.txn_ref,
            "metadata": metadata,
        }

        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        payment_link = response_data["data"]["authorization_url"]
        if response.status_code != 200:
            raise Exception(response_data["message"])
        return Response({"success": payment_link}, status=status.HTTP_200_OK)


paystack_card_deposit = PaystackPaymentView.as_view()


class VerifyPaystackPayment(APIView):
    def get(self, request):
        tx_ref = self.request.query_params.get("trxref")
        paystack_reference = self.request.query_params.get("reference")
        payment = Payment.objects.get(txn_ref=tx_ref)
        verified = payment.verify_paystack_payment()
        if verified:
            # do some things
            recipient = payment.user
            user_wallet = Wallet.objects.filter(user=recipient).first()
            user_wallet.balance += payment.amount
            user_wallet.save()
            return Response(
                {"message": "Verified payment successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Payment Verification Failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )


verify_paystack_payment = VerifyPaystackPayment.as_view()
