from payments.models import (
    PaymentPlan,
    TransactionIntent,
    PaymentGateway,
    Payment,
    Subscription,
)
from payments.payment_gateways.paystack import paystack
from core.models import User
from loguru import logger
from payments.payment_gateways.paystack.paystack_models import (
    PaystackWebhookData,
)

import json


class PaymentService:
    def __init__(
        self,
        payment_gateway: PaymentGateway,
        payment_plan_id: int,
        callback_url: str,
        user: User,
    ) -> None:
        self.payment_gateway = payment_gateway
        self.payment_plan_id = payment_plan_id
        self.callback_url = callback_url
        self.user = user

    def initialize_payment(self) -> dict:
        """
        Initiates payment
        """
        plan = PaymentPlan.objects.get(id=self.payment_plan_id)

        # total_charge_amount = payment_utils.get_gateway_charges_for_transaction(
        #     payment_gateway=self.payment_gateway, amount=float(plan.price)
        # )

        # ? Since the plan will invalidate the amount, the charges need to have been included in the plan.
        total_charge_amount = plan.price

        transaction_intent = TransactionIntent.objects.create(
            user=self.user,
            payment_plan=plan,
            payment_gateway=self.payment_gateway,
            amount=total_charge_amount,
            description="Payment for subscription",
        )

        match self.payment_gateway:
            case PaymentGateway.PAYSTACK:
                response = paystack.charge_amount(
                    email=self.user.email,
                    amount=total_charge_amount * 100,
                    transaction_uid=transaction_intent.transaction_uid,
                    callback_url=self.callback_url,
                    plan_code=plan.plan_code,
                )

            case _:
                raise NotImplementedError

        return response.model_dump()

    @staticmethod
    def process_paystack_payment(payment_data: PaystackWebhookData, **kwargs):
        transaction_intent = TransactionIntent.objects.filter(
            transaction_uid=payment_data.data.reference
        ).first()

        metadata = json.loads(payment_data.model_dump_json(exclude_none=True))

        if not transaction_intent:
            # That means it was not initiated by the app.
            # It could be a recurring payment.
            user = User.objects.filter(email=payment_data.data.customer.email).first()

            plan = None

            if payment_data.data.plan:
                plan = PaymentPlan.objects.filter(
                    plan_code=payment_data.data.plan.plan_code
                ).first()

            Payment.objects.create(
                user=user,
                email=payment_data.data.customer.email,
                amount=payment_data.data.amount,
                txn_ref=payment_data.data.reference,
                verified=False,  #! verification might be done manually
                metadata=metadata,
                payment_plan=plan,
            )

            logger.info(f"Payment recorded for user: {transaction_intent.user.email}")

            return

        transaction_intent.status = TransactionIntent.TransactionStatus.PROCESSING

        transaction_intent.save()

        response = paystack.verify_transaction(transaction_intent.transaction_uid)

        if response.data.status != "success":
            transaction_intent.status = TransactionIntent.TransactionStatus.FAILED

            logger.error(
                "Paystack transaction with transaction_uid:"
                f" {transaction_intent.transaction_uid} is reported failed"
            )

        elif response.data.status == "success":
            logger.info(
                f"Transaction {transaction_intent.transaction_uid} was successful"
            )

            transaction_intent.status = TransactionIntent.TransactionStatus.COMPLETED

            Payment.objects.create(
                user=transaction_intent.user,
                email=transaction_intent.user.email,
                amount=transaction_intent.amount,
                txn_ref=transaction_intent.transaction_uid,
                verified=True,
                metadata=metadata,
                payment_plan=transaction_intent.payment_plan,
            )

            logger.info(f"Payment recorded for user: {transaction_intent.user.email}")

        transaction_intent.save()


class SubscriptionService:

    @staticmethod
    def create_subscription(payment_data: PaystackWebhookData, **kwargs):

        user = User.objects.filter(email=payment_data.data.customer.email).first()
        metadata = json.loads(payment_data.model_dump_json(exclude_none=True))

        plan = PaymentPlan.objects.filter(
            plan_code=payment_data.data.plan.plan_code
        ).first()
        Subscription.objects.create(
            payment_plan=plan,
            metadata=metadata,
            user=user,
            subscription_code=payment_data.data.subscription_code,
            email_token=payment_data.data.email_token,
        )

    def cancel_subscription(self, user: User):

        subscription: Subscription = self.get_current_subscription(user=user)

        if not subscription:
            return None

        try:

            response = paystack.cancel_subscription(
                code=subscription.subscription_code, token=subscription.email_token
            )

            logger.warning("Request to cancel subscription has been initiated")

        except Exception as exc:
            logger.error(exc)

            return

        return response

    @staticmethod
    def send_invoice_reminder():
        pass

    def get_current_subscription(self, user: User):
        pass
