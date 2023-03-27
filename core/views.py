import asyncio

from allauth.account import app_settings as allauth_settings
from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from asgiref.sync import async_to_sync
from decouple import config
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.views import PasswordChangeView, PasswordResetView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.signals import reset_password_signal
from utils.auth.agent_verification import agent_identity_verification
from utils.permissions import IsAgent, IsOwner

from .models import AgentDetails, Profile, UserSettings
from .otp import OTPGenerator
from .serializers import *
from .signals import new_user_signal, verification_signal


class GetOTPView(APIView):
    def get(self, request, email):
        user = get_object_or_404(get_user_model(), email=email)
        otp_gen = OTPGenerator(user_id=user.id)

        otp = otp_gen.get_otp()

        return Response({"detail": f"success otp- {otp}"}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    serializer_class = OTPSerializer

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            get_user_model(), email=serializer.validated_data["email"]
        )
        otp_gen = OTPGenerator(user_id=user.id)

        check = otp_gen.check_otp(serializer.validated_data["otp"])

        if check:
            # Mark user as verified
            user_obj = get_object_or_404(EmailAddress, user=user)

            user_obj.verified = True
            user_obj.save()

            return Response(
                {"detail": "2FA successfully completed"},
                status=status.HTTP_202_ACCEPTED,
            )

        return Response({"detail": "Invalid otp"}, status=status.HTTP_403_FORBIDDEN)


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


class CustomPasswordResetConfirmView(PasswordChangeView):
    serializer_class = CPasswordChangeSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):

        data = super().get_serializer_context()
        if self.request.method == "POST":

            email = self.request.data["email"]
            user = get_object_or_404(get_user_model(), email=email)
            data["user"] = user
            return data
        return super().get_serializer_context()

    def get_queryset(self):
        return super().get_queryset()


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


class CustomSocialLoginView(SocialLoginView):
    """
    Google Login- Changing the Serializer class to a Custom made one
    """

    serializer_class = CustomSocialLoginSerializer


class CustomRegisterView(RegisterView):
    """
    Register New users
    """

    serializer_class = CustomRegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save(self.request)

        # Whether to send email after registration
        send_email_check = getattr(settings, "SEND_EMAIL", False)
        new_user_signal.send_robust(__class__, send_email=send_email_check, user=user)

        if (
            allauth_settings.EMAIL_VERIFICATION
            != allauth_settings.EmailVerificationMethod.MANDATORY
        ):
            if getattr(settings, "REST_USE_JWT", False):
                self.access_token, self.refresh_token = jwt_encode(user)
            elif not getattr(settings, "REST_SESSION_LOGIN", False):
                # Session authentication isn't active either, so this has to be
                #  token authentication
                # create_token(self.token_model, user, serializer)
                pass

        return user


# if you want to use Authorization Code Grant, use this
class GoogleLogin(CustomSocialLoginView):

    site = config("CALLBACK_URL", "")
    domain = site.split("/")[2] if site else ""

    @extend_schema(
        description=f"# Visit this [`link`](https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=https://{domain}/accounts/google/login/callback/&prompt=consent&response_type=code&client_id=878674025478-e8s4rf34md8h4n7qobb6mog43nfhfb7r.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline) for users to see the google account select modal."
        + """
        After Users select account for login, they will be redirected to a new url.

        extract the `code` query parameter passed in the redirected url and send to this endpoint to get access and refresh tokens

        Example data:

        {

            code : "4%2F0AWgavdfDkbD_aCXtaruulCuVFpZSEpImEuZouGFZACGO1hxoDwqCV1znzazpn7ev5FmH2w"

        }
        """
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    # * Local Development link
    # ? https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://127.0.0.1:8000/accounts/google/login/callback/&prompt=consent&response_type=code&client_id=878674025478-e8s4rf34md8h4n7qobb6mog43nfhfb7r.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline

    # CALLBACK_URL_YOU_SET_ON_GOOGLE
    default_call_back_url = "http://127.0.0.1:8000/accounts/google/login/callback/"

    adapter_class = GoogleOAuth2Adapter
    callback_url = config("CALLBACK_URL", default_call_back_url)

    client_class = OAuth2Client
