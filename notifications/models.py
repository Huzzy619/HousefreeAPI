from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(_("Notification Description"))
    read = models.BooleanField(_("Read Notification"), default=False)

    def __str__(self):
        return f"{self.user.email}: {self.description[:50]}..."

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ("-id",)
