from django.db import models
# from .validators import validate_newsletter_instance
from django.core.exceptions import ValidationError

# Create your models here.

def validate_newsletter_instance(email):
    if Newsletter.objects.filter(email=email).exists():
        raise ValidationError("You've already subscribed")

    return email

class Contact(models.Model):

    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Newsletter(models.Model):

    email = models.EmailField(validators=[validate_newsletter_instance])

    def __str__(self):
        return self.email
