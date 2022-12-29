from django.core.exceptions import ValidationError

from .models import Newsletter


def validate_newsletter_instance(email):
    if Newsletter.objects.filter(email=email).exists():
        raise ValidationError("You've already subscribed")

    return email
