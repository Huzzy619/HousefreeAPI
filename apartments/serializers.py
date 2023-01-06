from rest_framework import serializers

from .models import Apartment, Bookmark, Media, Picture, Review


class CreateBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["id", "apartment_id"]  #'__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "text", "date_created"]

    def save(self, **kwargs):
        user = self.context["user"]
        return super().save(user=user, **self.validated_data)


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["id", "video"]

    def save(self, **kwargs):
        _id = self.context["apartment_pk"]
        return super().save(apartment_id=_id, **self.validated_data)

    def get_video(self, obj):
        return self.context["request"].build_absolute_uri(obj.video.url)


class PictureSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Picture
        fields = ["id", "image"]

    def get_image(self, obj):
        return self.context["request"].build_absolute_uri(obj.image.url)

    def save(self, **kwargs):
        _id = self.context["apartment_pk"]
        return super().save(apartment_id=_id, **self.validated_data)


class CreateApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = [
            "id",
            "title",
            "category",
            "price",
            "location",
            "specifications",
            "descriptions",
            "is_available",
        ]

    def save(self, **kwargs):
        user = self.context["user"]
        return super().save(agent=user, **self.validated_data)


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = [
            "id",
            "title",
            "category",
            "type",
            "price",
            "location",
            "specifications",
            "descriptions",
            "is_available",
            "agent",
            "pictures",
            "videos",
        ]

    agent = serializers.SerializerMethodField()
    pictures = PictureSerializer(many=True)
    videos = MediaSerializer(many=True)

    def get_agent(self, object):
        user = object.agent.get_full_name()
        if not user:
            return ""
        return user
