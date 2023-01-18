from urllib.parse import unquote

from dj_rest_auth.registration.serializers import (
    RegisterSerializer,
    SocialLoginSerializer,
)
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import *


class AgentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentDetails

        fields = ['nin', 'id_front', "id_back", "photo", "id_type", "phone", "certificate"]
    
    def save(self, **kwargs):
        
        return super().save(agent=self.context['user'], is_verified=True, **kwargs)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ["id", "image", "background_image", "location"]

# For Google Login


class CustomSocialLoginSerializer(SocialLoginSerializer):
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

    class Meta:
        model = get_user_model()
        fields = ["id", "name", "email", "is_agent", "date_joined"]

    def get_name(self, obj):
        return obj.get_full_name()

class OTPSerializer (serializers.Serializer):
    otp = serializers.CharField(max_length=6)
