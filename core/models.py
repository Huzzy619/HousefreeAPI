import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from utils.paths.path_helpers import get_passport_path
from utils.validators.models import validate_NIN_digits

from .managers import CustomUserManager

# Create your models here.


class User(AbstractUser):
    username = None
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    is_agent = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Profile(models.Model):
    GENDER = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    image = models.ImageField(default="default.jpg", upload_to="profile_pictures")
    background_image = models.ImageField(
        default="default_id.png", upload_to="background_images"
    )
    phone = PhoneNumberField(blank=True, null=True)
    location = models.CharField(max_length=550, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)


class AgentDetails(models.Model):
    ID_TYPE = [("NIN", "NIN"), ("GOVERNMENT_ID", "GOVERNMENT_ID")]

    nin = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(11), validate_NIN_digits],
        null=True,
        blank=True,
    )
    id_front = models.ImageField(
        upload_to=get_passport_path,
        null=True,
        blank=True,
        verbose_name="Goverment ID Front",
    )
    id_back = models.ImageField(
        upload_to=get_passport_path,
        null=True,
        blank=True,
        verbose_name="Goverment ID Back",
    )
    photo = models.ImageField(upload_to=get_passport_path)
    id_type = models.CharField(choices=ID_TYPE, max_length=50)
    phone = PhoneNumberField()
    is_verified = models.BooleanField(default=False)

    agent = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="agent_details"
    )
