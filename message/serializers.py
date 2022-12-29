from rest_framework import serializers

from .models import Message


def message_serializer(a) -> dict:
    return {
        "room_id": a.room.room_id,
        "author": a.author,
        "message": a.content,
        "timestamp": (a.timestamp).strftime("%a. %I:%M %p"),
        "short_id": a.short_id,
    }


class ContactUsSerializer(serializers.Serializer):
    sender = serializers.EmailField()
    message = serializers.CharField()

    def __str__(self):
        return self.sender


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["author", "content", "timestamp", "short_id"]
