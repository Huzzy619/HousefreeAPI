from rest_framework import serializers
from .models import Contact, Newsletter, HelpDesk, Report
from django.contrib.auth import get_user_model


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "message", "date"]


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ["id", "email"]


class HelpDeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpDesk
        fields = ["category", "problem", "message", "date_created"]

    def save(self, **kwargs):
        return super().save(user=self.context["user"], **self.validated_data)


class ReportListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["problem", "description", "apartment"]

    def save(self, **kwargs):
        user = get_user_model().objects.first()
        return super().save(user=user, **self.validated_data)
        self.context["user"]
