import random
import string
import uuid

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import FileExtensionValidator
from django.db import models
from hitcount.models import (  # This will add a reverse lookup from HitCount Model
    HitCount,
    HitCountMixin,
)

TYPE_CHOICES = [
    ("Rent", "Rent"),
    ("Buy", "Buy"),
    ("Event Center", "Event Center"),
]

CATEGORY_TYPE = [
    ("Bungalow", "Bungalow"),
    ("Duplex", "Duplex"),
    ("Flats", "Flats"),
    ("Self Contain", "Self Contain"),
    ("Hostels", "Hostels"),
]


class Apartment(models.Model, HitCountMixin):

    guid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

    title = models.CharField(
        max_length=100, null=False, blank=True, verbose_name="Apartment Title"
    )
    property_ref = models.CharField(max_length=10, editable=False)
    category = models.CharField(choices=CATEGORY_TYPE, max_length=20)
    _type = models.CharField(
        max_length=255, choices=TYPE_CHOICES, default="Rent", verbose_name="type"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    locality = models.CharField(max_length=550)
    state = models.CharField(max_length=500)
    area = models.CharField(max_length=500)
    street = models.CharField(max_length=500)
    descriptions = models.TextField(blank=True, null=True)
    specifications = models.JSONField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    clicks = GenericRelation(
        HitCount, object_id_field="object_pk", related_query_name="clicks_relation"
    )

    agent = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    verified = models.BooleanField(default=False)
    
    def property_ref_generator(self, length=10, chars=string.digits):
        value = "".join(random.choice(chars) for _ in range(length))
        while self.__class__.objects.filter(property_ref=value).exists():
            value = "".join(random.choice(chars) for _ in range(length))

        return value

    def save(self, **kwargs) -> None:
        self.property_ref = self.property_ref_generator()
        return super().save(**kwargs)
    
    def cover_pic(self):
        return self.pictures.order_by('date_created').first()


    def __str__(self) -> str:
        return f"{self.title}-- {self.id}" 


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

    class Meta:
        verbose_name_plural = "Media"


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
