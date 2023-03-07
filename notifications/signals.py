from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification


@receiver(post_save, sender=get_user_model())
def create_user_profile(instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            description="Welcome to Rentrite, update your profile to get started",
        )
