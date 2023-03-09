from decouple import config
from django.conf import settings
from hitcount.views import HitCountDetailView
from mailjet_rest import Client
import threading

from apartments.models import Apartment


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        super().__init__(group=None)

    def run(self):
        self.email.send()

# To make the hitcount work.
class ApartmentClicks(HitCountDetailView):
    model = Apartment
    count_hit = True
    template_name = "apartment_detail.html"


def mailjet_email_backend(
    to: str,
    subject: str,
    text: str,
    name: str = None,
    html_part: str = None,
    template_id: int = None,
    variables: dict = {},
    **kwargs
):
    try:
        api_key = settings.MJ_API_KEY
        api_secret = settings.MJ_API_SECRET
        mailjet = Client(auth=(api_key, api_secret), version="v3.1")

        data = {
            "Messages": [
                {
                    "From": {
                        "Email": config("OFFICIAL_EMAIL", "blazingkrane@gmail.com"),
                        "Name": "RentRite",
                    },
                    "To": [
                        {
                            "Email": to,
                            "Name": name,
                        }
                    ],
                    "TemplateID": template_id,
                    "TemplateLanguage": True,
                    "Subject": "Comfy Home Receipt",
                    "Variables": variables,
                }
            ]
        }

        result = mailjet.send.create(data=data)
        print({"status": result.status_code})
        print(result.json())
    except:

        print("Something went wrong with email messaging")
