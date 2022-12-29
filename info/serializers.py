from rest_framework import serializers
from .models import Contact, Newsletter

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['email', 'message', 'date']


class NewsletterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Newsletter
        fields = ['id', 'email']