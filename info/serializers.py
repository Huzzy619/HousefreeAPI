from rest_framework import serializers
from .models import Contact, Newsletter, HelpDesk

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message', 'date']


class NewsletterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Newsletter
        fields = ['id', 'email']


class HelpDeskSerializer(serializers.ModelSerializer):

    class Meta:
        model = HelpDesk
        fields = ['category', 'problem', 'message', 'date_created']

    def save(self, **kwargs):
        return super().save(author = self.context['user'], **self.validated_data)