from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.email_backend import send_email

from ..models import Profile, UserSettings
from ..otp import OTPGenerator
from . import new_user_signal, reset_password_signal, verification_signal
from notifications.models import Notification
from core.schemas import VerificationStatus

@receiver(post_save, sender=get_user_model())
def create_user_profile_and_settings(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserSettings.objects.create(user=instance)


@receiver(new_user_signal)
def send_verification_email(*args, **kwargs):
    if kwargs["send_email"]:
        user = kwargs["user"]
        code = OTPGenerator(user_id=user.id).get_otp()
        send_email(
            subject="Email Verification!",
            recipients=[user.email],
            message=f"Use this code to verify email address {code} ",
            context={"code": code, "name": user.get_full_name()},
            template=(
                "email/email_seller_verification.html"
                if user.is_agent
                else "email/email_verification.html"
            ),
        )


@receiver(reset_password_signal)
def reset_password(**kwargs):
    email = kwargs["email"]

    user = get_user_model().objects.get(email=email)

    code = OTPGenerator(user_id=user.id).get_otp()

    send_email(
        subject="Password Reset",
        message=f"Use this code for resetting your password {code}",
        recipients=[email],
        template="email/password_reset.html",
        context={"code": code},
    )


@receiver(verification_signal)
def send_verification_status_email(*args, **kwargs):

    status, user = kwargs.values()
    context = {"name": user.get_full_name()}

    match status:
        case VerificationStatus.PENDING:
            subject = "Verification Pending"
            message = "Your verification is currently pending"
            template = "email/verification_pending.html"

        case VerificationStatus.SUCCESS:
            subject = "Verification Successful"
            message = "Your verification has been successful"
            template = "email/verification_success.html"

        case VerificationStatus.FAILED:
            subject = "Verification Failed"
            message = "Your verification has been rejected"
            template = "email/verification_failed.html"

    send_email(
        subject=subject,
        message=message,
        recipients=[user.email],
        template=template,
        context=context,
    )

    Notification.objects.create(
        user = user,
        description = message
    )

