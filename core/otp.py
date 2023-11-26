import base64

from django.conf import settings
from pyotp import HOTP

from core.models import OTP
from datetime import timedelta
from django.utils import timezone


class OTPGenerator:
    """
    secret_key(Base32): is needed to generate and verify the otp securely
    processed_id: is the first 4 digit of a UUID object type casted to Integer
    counter: keeps track of otp request made by a user.
    value: makes each request unique by adding processed_id and counter
    """

    def __init__(self, user_id, **kwargs) -> None:
        self.secret_key = self.get_secret()
        self.user_id = user_id
        self.processed_id = int(str(int(user_id))[:4])
        self.hotp = HOTP(self.secret_key)
        self.obj, created = OTP.objects.get_or_create(user_id=self.user_id)

    def get_otp(self):
        value = self.processed_id + self.obj.counter
        otp = self.hotp.at(value)

        self.obj.counter += 1
        self.obj.save()

        return otp

    def check_otp(self, otp):
        otp_time = self.obj.date_created
        current_time = timezone.now()

        time_check = current_time - otp_time <= timedelta(minutes=10)

        # get the previous counter associated with a user and evaluate to get value
        value = self.processed_id + (self.obj.counter - 1)
        verify_status = self.hotp.verify(otp, value)

        if verify_status and time_check:
            return "passed", True
        elif verify_status and not time_check:
            return "expired", False
        else:
            return "invalid", False

    def get_secret(self):
        """
        # Note: the otpauth scheme DOES NOT use base32 padding for secret lengths not divisible by 8.
        # Some third-party tools have bugs when dealing with such secrets.
        # We might consider warning the user when generating a secret of length not divisible by 8.

        """
        string = getattr(settings, "SECRET_KEY")

        base32_encoded = base64.b32encode(string.encode("utf-8"))

        secret = base32_encoded.decode("utf-8")

        return secret[:32]
