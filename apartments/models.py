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
from autoslug import AutoSlugField
from RentRite.models import BaseModel


class Apartment(BaseModel, HitCountMixin):
    class Type(models.TextChoices):
        RENT = "Rent"
        SALE = "Sale"

    class Category(models.TextChoices):
        APARTMENTS = "Apartments"
        HOSTELS = "Hostels"
        FLATS = "Flats"
        COMMERCIAL_PROPERTIES = "Commercial Properties"
        EVENT_CENTERS = "Event Centers"
        SELF_CONTAIN = "Self Contain"
        HOUSES = "Houses"

    guid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(
        max_length=500, null=False, blank=True, verbose_name="Apartment Title"
    )
    slug = AutoSlugField(populate_from="title", default="")
    property_ref = models.CharField(max_length=10, editable=False)
    category = models.CharField(choices=Category, max_length=50)
    _type = models.CharField(
        max_length=255, choices=Type, default=Type.RENT, verbose_name="type"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=500)
    address = models.CharField(max_length=1000)
    map_link = models.URLField(null=True, blank=True)
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
        if not self.property_ref:
            self.property_ref = self.property_ref_generator()

        return super().save(**kwargs)

    def cover_pic(self):
        return self.pictures.order_by("date_created").first()

    def __str__(self) -> str:
        return f"{self.title}-- {self.id}"

    @property
    def clicks(self):
        return self.hit_count.hits

    class Meta:
        ordering = ["category"]


class Picture(BaseModel):
    image = models.ImageField(upload_to="apartments")
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name="pictures"
    )


class Media(BaseModel):
    video = models.FileField(
        upload_to="apartment/videos",
        validators=[FileExtensionValidator(allowed_extensions=["mp4", "mkv", "3gp"])],
    )
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name="videos"
    )

    class Meta:
        verbose_name = "Video"


class Review(BaseModel):
    text = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name="reviews"
    )

    class Meta:
        ordering = ["-updated_at"]


class Bookmark(BaseModel):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
