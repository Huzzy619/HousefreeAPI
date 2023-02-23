from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from payments.models import Wallet


@receiver(post_save, sender=get_user_model())
def create_user_wallet(instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
