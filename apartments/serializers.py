from django.contrib.humanize.templatetags.humanize import intcomma
from rest_framework import serializers

from core.serializers import UserSerializer, SimpleUserSerializer

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
        apartment_pk = self.context.get("apartment_pk", "")

        if not Apartment.objects.filter(pk = apartment_pk ).exists():
            raise serializers.ValidationError("No Apartment with the given ID")
        
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


class CreateMediaSerializer(serializers.Serializer):
    video = serializers.ListField(child=serializers.FileField(), allow_empty=False)

    def create(self, validated_data):
        videos = validated_data.pop("video")

        apartment_pk = self.context["apartment_pk"]

        if not Apartment.objects.filter(pk = apartment_pk ).exists():
            raise serializers.ValidationError("No Apartment with the given ID")

        vids = [
            Media(video=vid, apartment_id=apartment_pk)
            for vid in videos
        ]

        instance = Media.objects.bulk_create(vids)

        # Since the `instance` is a list, a key has to be assigned to the instance so it can be accessed in the View Response

        return {"video": instance}


class PictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = ["id", "image"]  # "cover_pic"

    def get_image(self, obj: Picture):
        return self.context["request"].build_absolute_uri(obj.image.url)


class CreatePictureSerializer(serializers.Serializer):
    """
    ListField -- A field class that validates a list of objects.

    Signature: ListField(child=<A_FIELD_INSTANCE>, allow_empty=True, min_length=None, max_length=None)

        child - A field instance that should be used for validating the objects in the list. If this argument is not provided then objects in the list will not be validated.
        allow_empty - Designates if empty lists are allowed.
        min_length - Validates that the list contains no fewer than this number of elements.
        max_length - Validates that the list contains no more than this number of elements.

    """

    image = serializers.ListField(child=serializers.ImageField(), allow_empty=False)

    def create(self, validated_data):
        images = validated_data.pop("image")
        apartment_pk = self.context.get("apartment_pk", "")

        if not Apartment.objects.filter(pk = apartment_pk ).exists():
            raise serializers.ValidationError("No Apartment with the given ID")

        pics = [
            Picture(image=img, apartment_id= apartment_pk)
            for img in images
        ]
        #
        

        instance = Picture.objects.bulk_create(pics)

        # Since the `instance` is a list, a key has to be assigned to the instance so it can be accessed in the View Response

        return {"image": instance}


class CreateApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = [
            "id",
            "title",
            "category",
            "_type",
            "price",
            "address",
            "state",
            "map_link",
            "specifications",
            "descriptions",
            "is_available",
        ]

    def save(self, **kwargs):
        user = self.context["user"]
        return super().save(agent=user, **self.validated_data)


class ApartmentSerializer(serializers.ModelSerializer):
    # apartment_type = serializers.CharField(source = '_type')
    pictures = PictureSerializer(many=True)
    videos = MediaSerializer(many=True)
    verified = serializers.BooleanField(read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Apartment
        fields = [
            "id",
            "property_ref",
            "title",
            "category",
            "_type",
            "price",
            "state",
            "address",
            "map_link",
            "specifications",
            "descriptions",
            "is_available",
            "verified",
            "clicks",
            "agent",
            "pictures",
            "videos",
        ]


    def get_price(self, apartment):
        price = intcomma(apartment.price)
        if price.endswith("00"):
            price = price.replace(".00", "")
        return price


class SimpleApartmentSerializer(serializers.ModelSerializer):

    agent = SimpleUserSerializer(read_only=True)
    price = serializers.SerializerMethodField()
    short_address = serializers.SerializerMethodField()
    pictures = serializers.SerializerMethodField()

    class Meta:
        model = Apartment
        fields = [
            "id",
            "title",
            "price",
            "short_address",
            "pictures", 
            "agent"
        ]
    
    def get_pictures(self, apartment:Apartment):
        if apartment.pictures.count() >= 1 :
            first_picture = apartment.pictures.first()

            request = self.context.get('request')
            return [request.build_absolute_uri(first_picture.image.url)]
        return []
    
    def get_price(self, apartment):
        price = intcomma(apartment.price)
        if price.endswith("00"):
            price = price.replace(".00", "")
        return price

    def get_short_address(self, apartment: Apartment):

        # ? Shortening the Address so it would look better on the frontend

        address_parts = apartment.address.rsplit(",", 2)
        if len(address_parts) > 1:
            short = address_parts[-1].strip()
            if short.lower() == apartment.state.lower():
                short = address_parts[-2].strip()
        else:
            address_parts = apartment.address.split()
            if len(address_parts) >= 2:
                short = " ".join(address_parts[-2:]).strip()
                if apartment.state.lower() in short.lower():
                    short = short.replace(apartment.state, "").strip()
            else:
                short = apartment.address

        if short is not None and short.lower() != apartment.state.lower():
            return f"{short}, {apartment.state}"
        else:
            return apartment.state