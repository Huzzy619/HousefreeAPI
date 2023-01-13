from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
# Create your models here.

def validate_newsletter_instance(email):
    if Newsletter.objects.filter(email=email).exists():
        raise ValidationError("You've already subscribed")

    return email

class Contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name}'s Message"


class Newsletter(models.Model):

    email = models.EmailField(validators=[validate_newsletter_instance])

    def __str__(self):
        return self.email

class HelpDesk(models.Model):

    category = models.CharField(max_length=500)
    problem = models.CharField(max_length=500)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
