import math
from enum import Enum
from payments.models import PaymentGateway

class Currency(str, Enum):
    NGN = "NGN"

ALL_PAYMENT_GATEWAYS = [
    
    {
        "payment_gateway": PaymentGateway.PAYSTACK,
        "currencies": [
            {"name": Currency.NGN, "max_amount": 200_000_000}
        ],  # converts to 2_000_000 NGN
        "charges": {
            "percentage": 1.6,
            "max_charge": 200_000,  # converts to 2_000 NGN
        },
    }
    
]


def get_gateway_charges_for_transaction(payment_gateway: PaymentGateway, amount: int):
    gateway_fee_percentage = None
    gateway_fee_amount = None
    total_charge_amount = None
    for gateway in ALL_PAYMENT_GATEWAYS:
        if payment_gateway == gateway["payment_gateway"]:
            gateway_fee_percentage = gateway["charges"]["percentage"]
            # converting to int gets rid of the extra decimal places
            # calculated_gateway_fee is still in the smallest denomination of the currency
            calculated_gateway_fee = math.ceil(amount * (gateway_fee_percentage / 100))
            if gateway["charges"]["max_charge"]:
                max_charge = gateway["charges"]["max_charge"]
                if calculated_gateway_fee > max_charge:
                    gateway_fee_amount = max_charge
                else:
                    gateway_fee_amount = calculated_gateway_fee
            else:
                gateway_fee_amount = calculated_gateway_fee
            total_charge_amount = amount + gateway_fee_amount
            break

    return total_charge_amount
