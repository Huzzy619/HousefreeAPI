from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from mailjet_rest import Client

from ..models import Profile, UserSettings
from . import new_user_signal


@receiver(post_save, sender=get_user_model())
def create_user_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserSettings.objects.create(user=instance)


@receiver(new_user_signal)
def send_verification_email(*args, **kwargs):
    if kwargs["send_email"]:
        user = kwargs["user"]
        code = "get_otp_code()"

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
                            "Email": "blazingkrane@gmail.com",
                            "Name": "Mailjet Pilot",
                        },
                        "To": [
                            {
                                # "Email": "hussein.ibrahim6196@gmail.com",
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
            print(result.status_code)
            print(result.json())
        except:

            print("Something went wrong with email messaging")
    #     data = {
    #   'Messages': [
    # 				{
    # 						"From": {
    # 								"Email": "blazingkrane@gmail.com",

    # 								"Name": "Mailjet Pilot"
    # 						},
    # 						"To": [
    # 								{
    # 										"Email": "hussein.ibrahim6196@gmail.com",
    # 										"Name": "passenger 1"
    # 								}
    # 						],
    # 						"TemplateID": 4568001,
    # 						"TemplateLanguage": True,
    # 						"Subject": "Your email flight plan22!"
    # 				}
    # 		]
    # }
