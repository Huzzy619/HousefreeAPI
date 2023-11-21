from decouple import config
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from core.models import Profile

from .utils import Google, login_with_google, register_with_google


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    is_agent = serializers.BooleanField(default=False)

    def save(self, **kwargs):
        try:
            user = get_user_model().objects._create_user(**self.validated_data)
        except IntegrityError:
            raise serializers.ValidationError("User with provided email already exists")

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "image", "background_image", "location"]


class InfoSerializer(serializers.Serializer):
    message = serializers.CharField()
    status = serializers.BooleanField()


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    is_verified = serializers.SerializerMethodField(method_name="get_status")
    phone = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "name",
            "email",
            "is_agent",
            "date_joined",
            "is_verified",
            "phone",
            "address",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj):
        return obj.get_full_name()

    @extend_schema_field(OpenApiTypes.STR)
    def get_status(self, obj: get_user_model()):
        try:
            if obj.is_agent:
                status = obj.agent_details.is_verified
                return status
        except Exception:
            return False

    @extend_schema_field(OpenApiTypes.STR)
    def get_phone(self, obj):
        try:
            if obj.is_agent:
                return str(obj.agent_details.phone)
        except Exception:
            return None

    @extend_schema_field(OpenApiTypes.STR)
    def get_address(self, obj):
        try:
            if obj.is_agent:
                return str(obj.profile.location)
        except Exception:
            return ""
        return ""


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate(self, data):
        auth_token = data.get("auth_token")
        user_data = Google.validate(auth_token)
        try:
            user_data["sub"]
        except Exception as identifier:
            raise serializers.ValidationError(
                {"message": str(identifier), "status": False}
            )

        if user_data["aud"] != config("GOOGLE_CLIENT_ID"):
            raise serializers.ValidationError(
                {"message": "Invalid credentials", "status": False}
            )

        email = user_data["email"]
        first_name = user_data["given_name"]
        last_name = user_data["family_name"]
        picture = user_data.get("picture")
        google_id = user_data.get("sub")

        if self.context.get("path") == "signup":
            return register_with_google(
                email=email,
                first_name=first_name,
                last_name=last_name,
                picture=picture,
                google_id=google_id,
            )
        return login_with_google(email=email, google_id=google_id)
