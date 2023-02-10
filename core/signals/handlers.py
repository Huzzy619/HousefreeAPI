from decouple import config
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from mailjet_rest import Client

from ..models import Profile, UserSettings
from ..otp import OTPGenerator
from . import new_user_signal


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

        # localhost email
        # EmailMessage(
        #     subject="", body="okay", from_email="me@go.com", to=[email]
        # ).send()

        try:
            api_key = settings.MJ_API_KEY
            api_secret = settings.MJ_API_SECRET
            mailjet = Client(auth=(api_key, api_secret), version="v3.1")

            data = {
                "Messages": [
                    {
                        "From": {
                            "Email": config("OFFICIAL_EMAIL", "blazingkrane@gmail.com"),
                            "Name": "Mailjet Pilot",
                        },
                        "To": [
                            {
                                "Email": user.email,
                                "Name": user.get_full_name(),
                            }
                        ],
                        "Subject": "Email Verification!",
                        "TextPart": f"Use this code to verify email address {code} ",
                        "HTMLPart": '<h3>Dear passenger 1, welcome to <a href="https://www.mailjet.com/">Mailjet</a>!</h3><br />May the delivery force be with you!',
                        "CustomCampaign": "SendAPI_campaign",
                        # "DeduplicateCampaign": True
                    }
                ]
            }

            result = mailjet.send.create(data=data)
            print({'status':result.status_code})
            print(result.json())
        except:

            print("Something went wrong with email messaging")
