# Create your models here.
import random
import uuid

from django.conf import settings
from django.db import models


def generate_short_id(size=9, chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
    return "".join(random.choice(chars) for _ in range(size))


class Room(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room_id = models.CharField(max_length=255, default=generate_short_id, unique=True)


class Message(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, serialize=False, unique=True
    )
    room = models.ForeignKey(
        Room, related_name="messages", on_delete=models.CASCADE, null=True
    )
    author = models.CharField(max_length=255)
    content = models.TextField(unique=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    short_id = models.CharField(max_length=255, default=generate_short_id, unique=True)


class MessageManager(models.Manager):
    def by_room(self, room):
        qs = Message.objects.filter(room=room).order_by("-timestamp")
        return qs

    def __str__(self):
        return self.content


class PrivateRoom(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    messages = models.ForeignKey(Message, on_delete=models.CASCADE)
    send_file = models.FileField()

    def __str__(self):
        return self.user
