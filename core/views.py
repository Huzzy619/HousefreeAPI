import asyncio

from asgiref.sync import async_to_sync
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError

# Create your views here.
from django.core.validators import validate_email
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.exception_handlers import ErrorEnum, ErrorResponse, response_schemas
from core.schemas import EmailEvents
from core.serializers import (
    AgentDetailsSerializer,
    OTPSerializer,
    PasswordResetSerializer,
    ProfileSerializer,
    UserSettingsSerializer,
)
from core.signals import new_user_signal, reset_password_signal
from utils.auth.agent_verification import agent_identity_verification
from utils.permissions import IsAgent, IsOwner

from .models import AgentDetails, Profile, UserSettings
from .otp import OTPGenerator
from .serializers import (
    GoogleSocialAuthSerializer,
    InfoSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)
from .signals import verification_signal


class GetOTPView(APIView):
    """
    REGISTER = "register"
    EMAIL_VERIFICATION = "email-verification"
    PASSWORD_RESET = "password-reset"
    PASSWORD_RESET_CONFIRM = "password-reset-confirm"
    PASSWORD_CHANGE = "password-change"
    PASSWORD_RESET_REQUEST = "password-reset-request"

    Args:
        APIView (_type_): _description_
    """

    def get(self, request, email, event, **kwargs):
        try:
            email_event = EmailEvents(event)
        except ValueError as e:
            return ErrorResponse(
                code=ErrorEnum.ERR_001,
                status=status.HTTP_400_BAD_REQUEST,
                extra_detail=str(e),
            )

        user = get_object_or_404(get_user_model(), email=email)

        if email_event == EmailEvents.REGISTER:
            new_user_signal.send_robust(__class__, user=user, send_email=True)

        return Response(
            {"detail": "Email resent successfully"}, status=status.HTTP_200_OK
        )


class VerifyOTPView(APIView):
    serializer_class = OTPSerializer

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            get_user_model(), email=serializer.validated_data["email"]
        )
        otp_gen = OTPGenerator(user_id=user.id)

        message, otp_status = otp_gen.check_otp(serializer.validated_data["otp"])

        if otp_status:
            # Mark user as verified

            user.is_verified = True
            user.save()

            return Response(
                {"detail": "2FA successfully completed"},
                status=status.HTTP_202_ACCEPTED,
            )

        return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)


class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]

            reset_password_signal.send(__class__, email=email)

        return Response(
            {"detail": "otp to reset password has been sent to the provided email"},
            status=status.HTTP_200_OK,
        )


class UserSettingsViewSet(
    ListModelMixin, UpdateModelMixin, GenericViewSet
):  # GenericViewSet
    """
    Users can see and update their settings

    The PATCH endpoint requires that the settings_id is sent as a path parameter


    """

    http_method_names = ["get", "patch"]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSettingsSerializer

    def get_queryset(self):
        return UserSettings.objects.filter(user=self.request.user)


class AgentDetailsView(CreateAPIView):
    """
    Send Agent's Data in for Validation and verification

    Only users that are agent can access this endpoint


    id_type - (Options)

    NIN,
    GOVERNMENT_ID

    """

    permission_classes = [IsAgent]
    serializer_class = AgentDetailsSerializer
    queryset = AgentDetails.objects.none().select_related("user")

    @async_to_sync
    async def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        front_image = serializer.validated_data["id_front"]
        back_image = serializer.validated_data["id_back"]
        selfie_image = serializer.validated_data["photo"]

        agent_verification = await agent_identity_verification(
            front_image, back_image, selfie_image
        )

        verification_signal.send(__class__, status="pending", user=request.user)
        if agent_verification:
            # checks if the agent details from identity verification service provider API
            # matches the agent details we've in our DB
            agent_first_name = agent_verification["result"]["firstName"]
            agent_last_name = agent_verification["result"]["lastName"]
            if (
                request.user.first_name.lower() == agent_first_name.lower()
                and request.user.last_name.lower() == agent_last_name.lower()
            ):
                await asyncio.get_event_loop().run_in_executor(None, serializer.save)
                headers = self.get_success_headers(serializer.data)
                verification_signal.send(__class__, status="success", user=request.user)

                return Response(
                    serializer.data, status=status.HTTP_201_CREATED, headers=headers
                )
            verification_signal.send(__class__, status="failed", user=request.user)

            return Response(
                data="user details does not match", status=status.HTTP_400_BAD_REQUEST
            )
        verification_signal.send(__class__, status="failed", user=request.user)

        return Response(
            data="agent verification failed",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    def get_serializer_context(self):
        return {"user": self.request.user}


class ProfileViewSet(ModelViewSet):
    http_method_names = ["get", "options", "head", "put"]
    permission_classes = [IsOwner]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


# Create your views here.


@response_schemas(response_model=InfoSerializer)
class RegisterView(GenericAPIView):
    """
    Create an account

    Returns:

        new_user: A newly registered user
    """

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serializer = InfoSerializer(
            data={"message": "Registered successfully", "status": True}
        )
        new_user_signal.send_robust(__class__, send_email=True, user=user)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    """
    Login with either Email & Password to get Authentication tokens

    Args:

        Login credentials (_type_): email/password

    Returns:

        message: success

        tokens: access and refresh

        user: user profile details
    """

    serializer_class = TokenObtainPairSerializer

    def post(self, request: HttpRequest, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # This could be a username or email
        email, password = serializer.validated_data.values()

        try:
            validate_email(email)
            email = get_user_model().objects.get(email=email).get_username()

        except (get_user_model().DoesNotExist, ValidationError):
            pass

        user = authenticate(request, username=email, password=password)

        if not user:
            return ErrorResponse(code=ErrorEnum.ERR_007)

        if not user.is_verified:
            # We could prevent login here and return error message to user to verify email
            # Or we could just return their verification status to the UI and show them a message to go complete their email verification
            pass

        request.data["username"] = email
        tokens = super().post(request)
        return Response(
            {
                "status": True,
                "message": "Logged in successfully",
                "tokens": tokens.data,
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class RefreshView(TokenRefreshView):
    """
    To get new access token after the initial one expires or becomes invalid

    Args:
        refresh_token

    Returns:
        access_token
    """

    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data["access"]
        return Response(
            {"access": access_token, "status": True}, status=status.HTTP_200_OK
        )


class GoogleSocialAuthView(APIView):
    """
    Login with Google by providing Auth_token

    Args:
        Auth_token
    """

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request: HttpRequest):
        """

        POST with "auth_token"
        Send an id token from google to get user information
        """

        path = "signup" if "signup" in request.path else "login"
        serializer = self.serializer_class(data=request.data, context={"path": path})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["status"]: True
        return Response(data, status=status.HTTP_200_OK)
