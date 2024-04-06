from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from apartments.models import Apartment
from RentRite.models import BaseModel

# Create your models here.


def validate_newsletter_instance(email):
    if Newsletter.objects.filter(email=email).exists():
        raise ValidationError("You've already subscribed")

    return email


class Contact(BaseModel):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.first_name}'s Message"


class Newsletter(BaseModel):
    email = models.EmailField(validators=[validate_newsletter_instance])

    def __str__(self):
        return self.email


class HelpDesk(BaseModel):
    category = models.CharField(max_length=500)
    problem = models.CharField(max_length=500)
    message = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)


class Report(BaseModel):
    problem = models.CharField(max_length=500)
    description = models.TextField()
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name="reports"
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
