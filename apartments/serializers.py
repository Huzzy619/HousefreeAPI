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

class MediaSerializer(serializers.Serializer):
    video0 = serializers.FileField(required=False)
    video1 = serializers.FileField(required=False)
    video2 = serializers.FileField(required=False)

    def create(self, validated_data):
        
        media = self.context["request"].FILES

        pics = [
            Media(
                video=media[f"video{i}"], apartment_id=self.context["apartment_pk"]
            )
            for i in range(len(media))
        ]

        return Media.objects.bulk_create(pics)


class PictureSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()

    class Meta:
        model = Picture
        fields = ["id", "image"]  # "cover_pic"

    def get_image(self, obj: Picture):
        # obj.apartment.
        return self.context["request"].build_absolute_uri(obj.image.url)

    


class CreatePictureSerializer(serializers.Serializer):
    image0 = serializers.ImageField(required=False)
    image1 = serializers.ImageField(required=False)
    image2 = serializers.ImageField(required=False)
    image3 = serializers.ImageField(required=False)
    image4 = serializers.ImageField(required=False)
    image5 = serializers.ImageField(required=False)
    image6 = serializers.ImageField(required=False)
    image7 = serializers.ImageField(required=False)
    image8 = serializers.ImageField(required=False)
    image9 = serializers.ImageField(required=False)


    def create(self, validated_data):
        
        pictures = self.context["request"].FILES

        pics = [
            Picture(
                image=pictures[f"image{i}"], apartment_id=self.context["apartment_pk"]
            )
            for i in range(len(pictures))
        ]

        return Picture.objects.bulk_create(pics)

class CreateApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = [
            "id",
            "title",
            "category",
            "price",
            "locality",
            "state",
            "area",
            "street",
            "specifications",
            "descriptions",
            "is_available",
        ]

    def save(self, **kwargs):
        user = self.context["user"]
        return super().save(agent=user, **self.validated_data)


class ApartmentSerializer(serializers.ModelSerializer):
    # apartment_type = serializers.CharField(source = '_type')
    agent = UserSerializer(read_only=True)
    pictures = PictureSerializer(many=True)
    videos = MediaSerializer(many=True)
    clicks = serializers.SerializerMethodField()
    verified = serializers.BooleanField(read_only=True)
    # cover_pic = serializers.SerializerMethodField()

    class Meta:
        model = Apartment
        fields = [
            "id",
            "property_ref",
            "title",
            "category",
            "_type",
            "price",
            "locality",
            "state",
            "area",
            "street",
            "specifications",
            "descriptions",
            "is_available",
            "verified",
            "clicks",
            "agent",
            "pictures",
            # "cover_pic",
            "videos",
        ]

    # def get_cover_pic(self, apartment:Apartment):

    #     obj = apartment.cover_pic()

    #     try:
    #         return  obj.id # self.context['request'].build_absolute_uri(obj.image.url)
    #     except:
    #         return None

    def get_clicks(self, apartment):
        return apartment.hit_count.hits

