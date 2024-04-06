
# from celery import shared_task
from loguru import logger

from payments.payment_gateways.paystack.paystack_models import (
    PaystackEvents, PaystackWebhookData
)
from payments.services import PaymentGateway, PaymentService, SubscriptionService


# @shared_task
def process_paystack_payment_in_background(payment_gateway: PaymentGateway, payment_data : dict, **kwargs):

    payment_data = PaystackWebhookData(**payment_data)

    match payment_data.event:
        case PaystackEvents.TRANSACTION_CHARGE_SUCCESS:
            """
            If you created the subscription by adding a plan code to a transaction, a charge.success event is also sent to indicate that the transaction was successful.
            """
            PaymentService.process_paystack_payment(
                payment_data = payment_data
            )
            logger.info(f"Payment from {payment_gateway} processed successfully")
                
        case PaystackEvents.SUBSCRIPTION_CREATE:
            """
            A subscription.create event is sent to indicate that a subscription was created for the customer who was charged.
            
            """

            SubscriptionService.create_subscription(payment_data=payment_data)

            logger.info("Subscription created")


        case PaystackEvents.INVOICE_CREATE:
            """
            An invoice.create event will be sent to indicate a charge attempt will be made on the subscription. This will be sent 3 days before the next payment date.
            """

            logger.info("Invoice created")

        case PaystackEvents.INVOICE_PAYMENT_FAILED:
            """
                On the next payment date, a charge.success event will be sent, if the charge attempt was successful. If not, an invoice.payment_failed event will be sent instead.
            """
            logger.info("Payment failed")

        case PaystackEvents.SUBSCRIPTION_NOT_RENEW:
            """
            
            A subscription.not_renew event will be sent to indicate that the subscription will not renew on the next payment date.
            """
            logger.info("Subscription not renewed")

        case PaystackEvents.SUBSCRIPTION_DISABLE:
            """
            On the next payment date, a subscription.disable event will be sent to indicate that the subscription has been cancelled.
            """
            logger.info("Subscription disabled")

