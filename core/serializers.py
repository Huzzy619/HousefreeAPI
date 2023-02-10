from urllib.parse import unquote

from dj_rest_auth.registration.serializers import (
    RegisterSerializer,
    SocialLoginSerializer,
)
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import *
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

class AgentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentDetails

        fields = [
            "nin",
            "id_front",
            "id_back",
            "photo",
            "id_type",
            "phone",
            "certificate",
        ]

    def save(self, **kwargs):

        return super().save(agent=self.context["user"], is_verified=True, **kwargs)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "image", "background_image", "location"]


# For Google Login


class CustomSocialLoginSerializer(SocialLoginSerializer):
    access_token = None
    id_token = None
    
    def validate(self, attrs):
        # update the received code to a proper format. so it doesn't throw error.

        attrs["code"] = unquote(attrs.get("code"))

        return super().validate(attrs)


class CustomLoginSerializer(LoginSerializer):
    username = None  # Remove username from the login


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(max_length=250)
    last_name = serializers.CharField(max_length=250)
    is_agent = serializers.BooleanField(required=False)

    def custom_signup(self, request, user):
        user_obj = get_user_model().objects.get(email=user)

        user_obj.first_name = request.data.get("first_name", "")
        user_obj.last_name = request.data.get("last_name", "")
        user_obj.is_agent = bool(request.data.get("is_agent", False))
        user_obj.save()

        pass


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ["id", "name", "email", "is_agent", "date_joined", "status", "phone"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj):
        return obj.get_full_name()

    @extend_schema_field(OpenApiTypes.STR)
    def get_status (self, obj):
        try:
            if obj.is_agent:
                status = obj.agent_details.is_verified
                return "Verified" if status else "Unverified"
        except:
            return None

    @extend_schema_field(OpenApiTypes.STR)
    def get_phone (self, obj):
        try:
            if obj.is_agent:
                return str(obj.agent_details.phone)
        except:
            return None

class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)



class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ['id','language', 'theme', 'notification']