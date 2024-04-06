from payments.payment_gateways.paystack.paystack_models import (
    PaystackTransaction,
    PaystackTransactionVerify, PaystackMessage
)
from django.conf import settings
import httpx
from uuid import UUID
from pydantic import HttpUrl
from loguru import logger


def charge_amount(
    email: str, amount: int, transaction_uid: UUID, callback_url: HttpUrl, plan_code: str, currency ="NGN", 
) -> PaystackTransaction:
    url = "https://api.paystack.co/transaction/initialize"

    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}

    payment_data = {
        "email": email,
        "amount": str(amount),
        "reference": str(transaction_uid),
        "currency": currency,
        "channels": ["card", "bank", "ussd", "qr", "mobile_money", "bank_transfer"],
        "callback_url": callback_url,
        "plan": plan_code # This would invalidate the value provided in amount
    }

    with httpx.Client() as client:
        response = client.post(url=url, json=payment_data, headers=headers)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as ex:
            logger.error(response.text)
            logger.exception(ex)
            raise ex
        return PaystackTransaction(**response.json())


def verify_transaction(transaction_uid: UUID) -> PaystackTransactionVerify:
    url = f"https://api.paystack.co/transaction/verify/{str(transaction_uid)}"

    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}

    with httpx.Client() as client:
        response = client.get(url=url, headers=headers)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as ex:
            logger.error(response.text)
            logger.exception(ex)
            raise ex
        return PaystackTransactionVerify(**response.json())



def cancel_subscription(code: str, token: str) -> PaystackMessage:
    url = "https://api.paystack.co/subscription/disable"

    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    payload = { 
        "code": code, 
        "token":  token 
        }
    with httpx.Client() as client:
        response = client.post(url=url, headers=headers, json=payload)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as ex:
            logger.error(response.text)
            logger.exception(ex)
            raise ex
        return PaystackMessage(**response.json())