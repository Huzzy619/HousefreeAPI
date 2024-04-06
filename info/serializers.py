from rest_framework import serializers
from .models import Contact, Newsletter, HelpDesk, Report


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "message", "created_at"]


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ["id", "email"]


class HelpDeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpDesk
        fields = ["category", "problem", "message", "created_at"]

    def save(self, **kwargs):
        return super().save(user=self.context["user"], **self.validated_data)


class ReportListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["problem", "description", "apartment"]

    def save(self, **kwargs):
        user = self.context["user"]
        return super().save(user=user, **self.validated_data)
