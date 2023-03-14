import threading

from decouple import config
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from mailjet_rest import Client



class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        super().__init__(group=None)

    def run(self):
        self.email.send()


def send_email(
    subject: str,
    recipients: list,
    message: str = None,
    context: dict = {},
    template: str = None,
):
    html_content = render_to_string(template, context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[email for email in recipients],
    )

    email.attach_alternative(html_content, "text/html")

    # start a thread for each email
    try:
        EmailThread(email).start()
    except:
        print("Something went wrong \nCouldn't send Email")


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
