from rest_framework import serializers
from core.serializers import UserSerializer
from .models import Apartment, Bookmark, Media, Picture, Review


class CreateBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["id", "apartment_id"]  


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

    def get_video(self, obj: Media):
        return self.context["request"].build_absolute_uri(obj.video.url)


class PictureSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()

    class Meta:
        model = Picture
        fields = ["id", "image"]

    def get_image(self, obj: Picture):
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
    apartment_type = serializers.CharField(source = '_type')
    agent = UserSerializer(read_only = True)
    pictures = PictureSerializer(many=True)
    videos = MediaSerializer(many=True)
    clicks = serializers.SerializerMethodField()

    class Meta:
        model = Apartment
        fields = [
            "id",
            "property_ref",
            "title",
            "category",
            "apartment_type",
            "price",
            "location",
            "specifications",
            "descriptions",
            "is_available",
            "clicks",
            "agent",
            "pictures",
            "videos",
        ]

    
    
    def get_clicks(self, apartment):
        return apartment.hit_count.hits 

