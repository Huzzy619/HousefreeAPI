import uuid

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

TYPE_CHOICES = [
    ('RENT','RENT'),
    ('BUY', "BUY"),
    ("CONSULTANT','CONSULTANT"),
]

CATEGORY_TYPE = [
    ("Bungalow", "Bungalow"),
    ("Duplex", "Duplex"),
    ("Flats", "Flats"),
    ("Self Contain", "Self Contain"),
    ("Hostels", "Hostels"),
]
class Apartment(models.Model):


    id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, unique=True
    )

    title = models.CharField(
        max_length=100, null=False, blank=True, verbose_name="Apartment Title"
    )
    category = models.CharField(choices=CATEGORY_TYPE, max_length=20)
    type_ = models.CharField(max_length=255, choices=TYPE_CHOICES, default="RENT")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    location = models.CharField(max_length=550)
    descriptions = models.TextField(blank=True, null=True)
    specifications = models.JSONField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    agent = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ["category"]


class Picture(models.Model):

    image = models.ImageField(upload_to="apartments")
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name="pictures"
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Media(models.Model):

    video = models.FileField(
        upload_to="apartment/videos",
        validators=[FileExtensionValidator(allowed_extensions=["mp4", "mkv", "3gp"])],
    )
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name="videos"
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Review(models.Model):

    text = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name="reviews"
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_updated"]


class Bookmark(models.Model):

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    