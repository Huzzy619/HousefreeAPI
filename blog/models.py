from django.contrib.auth import get_user_model
from django.db import models

from utils.paths.path_helpers import get_blogs_image_path
from RentRite.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Blog(BaseModel):
    class Category(models.TextChoices):
        SPOTLIGHT = "spotlight", _("Spotlight")
        BUYING_AND_SELLING = "buying_and_selling", _("Buying & Selling")
        RENTING = "renting", _("Renting")
        TIPS_AND_ADVICE = "tips_and_advice", _("Tips & Advice")

    title = models.CharField(max_length=500)
    content = models.TextField()
    category = models.CharField(max_length=200, choices=Category)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_blogs_image_path, null=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Post"

    def __str__(self):
        return self.title

    @property
    def author_name(self):
        return self.author.get_full_name()
