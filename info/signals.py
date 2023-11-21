from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Contact


# @receiver(post_save, sender=get_user_model())
# def subscribe_user_to_newsletters(instance, created, **kwargs):
#     if created:
#         Newsletter.objects.create(email=instance.email)


@receiver(post_save, sender=Contact)
def send_contact_email(instance, created, **kwargs):
    if created:
        # api_key = settings.MJ_APIKEY_PUBLIC
        # api_secret = settings.MJ_APIKEY_PRIVATE
        # mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        # data = {
        # 'Messages': [
        #     {
        #     "From": {
        #         "Email": "$SENDER_EMAIL",
        #         "Name": "Me"
        #     },
        #     "To": [
        #         {
        #         "Email": "$RECIPIENT_EMAIL",
        #         "Name": "You"
        #         }
        #     ],
        #     "Subject": "RentRite Contact",
        #     "TextPart": instance.message,
        #     "HTMLPart": "<h3>Dear passenger 1, welcome to <a href=\"https://www.mailjet.com/\">Mailjet</a>!</h3><br />May the delivery force be with you!"
        #     }
        # ]
        # }
        # mailjet.send.create(data=data)

        pass
