from decouple import config
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.db.utils import IntegrityError
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from core.models import Profile

from .models import AgentDetails, UserSettings
from .utils import Google, login_with_google, register_with_google


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


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ["name"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj):
        return obj.get_full_name()


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
        fields = ["id", "language", "theme", "notification"]


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if get_user_model().objects.filter(email=email):
            return email
        raise serializers.ValidationError()


class CPasswordChangeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    set_password_form = None

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings,
            "OLD_PASSWORD_FIELD_ENABLED",
            False,
        )
        self.logout_on_password_change = getattr(
            settings,
            "LOGOUT_ON_PASSWORD_CHANGE",
            False,
        )
        super().__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop("old_password")

        self.request = self.context.get("request")
        self.user = self.context.get("user")

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value),
        )

        if all(invalid_password_conditions):
            err_msg = _(
                "Your old password was entered incorrectly. Please enter it again."
            )
            raise serializers.ValidationError(err_msg)
        return value

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user,
            data=attrs,
        )

        self.custom_validation(attrs)
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash

            update_session_auth_hash(self.request, self.user)


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


class InfoSerializer(serializers.Serializer):
    message = serializers.CharField()
    status = serializers.BooleanField()


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
            login_details = register_with_google(
                email=email,
                first_name=first_name,
                last_name=last_name,
                picture=picture,
                google_id=google_id,
            )
        else:
            login_details = login_with_google(email=email, google_id=google_id)

        login_details["user"] = UserSerializer(login_details["user"]).data

        return login_details
