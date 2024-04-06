from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.services import PaymentService

from .models import BankDetail, Payment, PaymentPlan, Wallet
from .serializers import (
    BankDetailSerializer,
    PaymentHistorySerializer,
    PaymentInputSerializer,
    PaymentPlanSerializer,
    SubscriptionInfoSerializer,
)


class PaymentView(APIView):
    serializer_class = PaymentInputSerializer

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, **kwargs):
        serializer = PaymentInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment_service = PaymentService(user=request.user, **serializer.validated_data)

        response = payment_service.initialize_payment()

        return Response(response, status=status.HTTP_200_OK)


class BankDetailView(APIView):
    serializer_class = BankDetailSerializer

    def get(self, request: Request, **kwargs):
        detail = BankDetail.objects.first()
        if detail:
            serializer = BankDetailSerializer(detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"details": "Bank details unavailable"}, status=status.HTTP_200_OK
        )


class PlanView(APIView):
    serializer_class = PaymentPlanSerializer

    def get(self, request: Request, **kwargs):
        plans = PaymentPlan.objects.all()
        serializer = PaymentPlanSerializer(plans, many=True)
        if plans:
            Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"details": "no registered plans"}, status=status.HTTP_200_OK)


class AgentSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionInfoSerializer

    def get(self, request: Request, **kwargs):
        wallet = Wallet.objects.get(user=request.user)
        payments = Payment.objects.filter(user=request.user)
        plan = None
        if payments:
            recent_payment = payments.latest("created_at")

            plan = PaymentPlan.objects.get(plan_id=recent_payment.payment_plan)

        data = {
            "email": request.user.email,
            "account_id": wallet.account_id,
            "current_subscription": plan.name if plan else None,
        }

        return Response(data, status.HTTP_200_OK)


class PaymentHistoryView(APIView):
    serializer_class = PaymentHistorySerializer

    def get(self, request: Request, *args, **kwargs):
        payment = Payment.objects.filter(user=request.user)
        serializer = self.serializer_class(payment, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
