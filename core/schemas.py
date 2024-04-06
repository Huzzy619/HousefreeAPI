from enum import Enum


class EmailEvents(str, Enum):
    REGISTER = "register"
    EMAIL_VERIFICATION = "email-verification"
    PASSWORD_RESET = "password-reset"
    PASSWORD_RESET_CONFIRM = "password-reset-confirm"
    PASSWORD_CHANGE = "password-change"
    PASSWORD_RESET_REQUEST = "password-reset-request"


class VerificationStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
