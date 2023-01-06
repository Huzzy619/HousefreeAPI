import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager

# Create your models here.


class User(AbstractUser):
    username = None
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    is_agent = models.BooleanField(default= False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Profile(models.Model):
    GENDER = [
            ("M", "Male"),
            ("F", "Female"),

        ]
    
    image = models.ImageField(default="default.jpg", upload_to="profile_pictures")
    background_image = models.ImageField(default="default_id.png", upload_to="background_images") 
    phone = PhoneNumberField(blank = True, null = True)
    location = models.CharField(max_length=550, blank = True, null = True)
    country = models.CharField(max_length=250, blank = True, null = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)