from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class PaystackTransactionData(BaseModel):
    authorization_url: Optional[str] = None
    access_code: Optional[str] = None
    reference: Optional[str] = None

class PaystackMessage(BaseModel):
    message: Optional[str] = None
    status: bool

class PaystackTransaction(PaystackMessage):
    data: PaystackTransactionData


class PaystackVerifyData(BaseModel):
    status: Optional[str] = None
    amount: int


class PaystackTransactionVerify(PaystackMessage):
    data: PaystackVerifyData



class HistoryItem(BaseModel):
    type: Optional[str] = None
    message: Optional[str] = None
    time: int


class Log(BaseModel):
    time_spent: int
    attempts: int
    authentication: Optional[str] = None
    errors: int
    success: bool
    mobile: bool
    input: List
    channel: Optional[str] = None
    history: List[HistoryItem]


class Customer(BaseModel):
    id: int = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    customer_code: Optional[str] = None
    phone: Optional[str] = None
    metadata: Optional[dict] = None
    risk_action: Optional[str] = None


class Authorization(BaseModel):
    authorization_code: Optional[str] = None
    bin: Optional[str] = None
    last4: Optional[str] = None
    exp_month: Optional[str] = None
    exp_year: Optional[str] = None
    card_type: Optional[str] = None
    bank: Optional[str] = None
    country_code: Optional[str] = None
    brand: Optional[str] = None
    account_name: Optional[str] = None


class Plan(BaseModel):
    name: Optional[str] = None
    plan_code: Optional[str] = None
    description: Optional[str] = None
    amount: int = None
    interval: Optional[str] = None
    send_invoices: bool = False
    send_sms: bool = False
    currency: Optional[str] = None


class Transaction(BaseModel):
    reference: Optional[str] = None
    status: Optional[str] = None
    amount: int = None
    currency: Optional[str] = None


class Subscription(BaseModel):
    status: Optional[str] = None
    subscription_code: Optional[str] = None
    email_token: Optional[str] = None
    amount: int = None
    cron_expression: Optional[str] = None
    next_payment_date: Optional[str] = None
    open_invoice: Optional[str] = None


class Data(BaseModel):
    id: int = None
    domain: Optional[str] = None
    status: Optional[str] = None
    reference: Optional[str] = None
    amount: int = None
    message: Optional[str] = None
    gateway_response: Optional[str] = None
    paid_at: Optional[str] = None
    created_at: Optional[str] = None
    channel: Optional[str] = None
    currency: Optional[str] = None
    ip_address: Optional[str] = None
    metadata: Optional[str] = None
    subscription_code: Optional[str] = None
    cron_expression: Optional[str] = None
    next_payment_date: Optional[str] = None
    open_invoice: dict = None
    createdAt: Optional[str] = None
    log: Optional[Log] = None
    fees: Optional[int] = None
    customer: Customer = None
    authorization: Authorization = None
    plan: Optional[Plan] = None
    transaction: Optional[Transaction] = None
    subscription: Optional[Subscription] = None
    email_token: Optional[str] = None


class PaystackEvents(str, Enum):
    INVOICE_CREATE = "invoice.create"
    INVOICE_PAYMENT_FAILED = "invoice.payment_failed"
    INVOICE_UPDATE = "invoice.update"
    SUBSCRIPTION_CREATE = "subscription.create"
    SUBSCRIPTION_NOT_RENEW = "subscription.not_renew"
    SUBSCRIPTION_DISABLE = "subscription.disable"
    TRANSACTION_CHARGE_SUCCESS = "charge.success"


class PaystackWebhookData(BaseModel):
    event: PaystackEvents
    data: Optional[Data] = None


# https://paystack.com/docs/payments/subscriptions/#create-a-subscription
