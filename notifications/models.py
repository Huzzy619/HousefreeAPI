from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from RentRite.models import BaseModel

User = get_user_model()

# Create your models here.


class Notification(BaseModel):
    class Category(models.TextChoices):
        PAYMENT = "Payment", _("Payment")
        CHAT = "Chat", _("Chat")
        ADVERT = "Advert", _("Advert")
        OTHER = "Other", _("Other")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(_("Notification Description"))
    read = models.BooleanField(_("Read Notification"), default=False)
    category = models.CharField(
        verbose_name=_("Category"),
        max_length=100,
        choices=Category,
        default=Category.OTHER,
    )

    def __str__(self):
        return f"{self.user.email}: {self.description[:50]}..."

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ("-id",)
