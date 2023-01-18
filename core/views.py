import asyncio
import os
from datetime import datetime, timedelta, timezone

from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from asgiref.sync import async_to_sync
from decouple import config
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from jose import JWTError, jwt
from pyotp import HOTP, random_base32
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from utils.auth.agent_verification import agent_identity_verification
from utils.permissions import IsAgent

from .models import AgentDetails, Profile, User
from .permissions import IsOwner
from .serializers import (
    AgentDetailsSerializer,
    CustomRegisterSerializer,
    CustomSocialLoginSerializer,
    OTPSerializer,
    ProfileSerializer,
)


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
    queryset = AgentDetails.objects.none()

    @async_to_sync
    async def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        front_image = serializer.validated_data["id_front"]
        back_image = serializer.validated_data["id_back"]
        selfie_image = serializer.validated_data["photo"]

        agent_verification = await agent_identity_verification(
            front_image, back_image, selfie_image
        )
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
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED, headers=headers
                )

            return Response(
                data="user details does not match", status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data="agent verification failed",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    def get_serializer_context(self):
        return {"user": self.request.user}

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


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

    def get_response_data(self, user):

        response = super().get_response_data(user)

        # Update response to include user's name
        user_pk = response["user"]["pk"]
        user = get_user_model().objects.get(id=user_pk)
        response["user"]["first_name"] = user.first_name
        response["user"]["last_name"] = user.last_name

        return response


# if you want to use Authorization Code Grant, use this
class GoogleLogin(CustomSocialLoginView):
    """
    # Visit this [`link`](https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://127.0.0.1:8000/accounts/google/login/callback/&prompt=consent&response_type=code&client_id=878674025478-e8s4rf34md8h4n7qobb6mog43nfhfb7r.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline) for users to see the google account select modal.


    After Users select account for login, they will be redirected to a new url.

    extract the `code` query parameter passed in the redirected url and send to this endpoint to get access and refresh tokens

    Example data:

        code : "4%2F0AWgavdfDkbD_aCXtaruulCuVFpZSEpImEuZouGFZACGO1hxoDwqCV1znzazpn7ev5FmH2w"
    """

    # CALLBACK_URL_YOU_SET_ON_GOOGLE
    if settings.DEBUG:
        _call_back_url = "http://127.0.0.1:8000/accounts/google/login/callback/"
    else:
        _call_back_url = settings.ALLOWED_HOSTS[0] + "/accounts/google/login/callback/"

    adapter_class = GoogleOAuth2Adapter
    callback_url = os.environ.get(
        "CALLBACK_URL", config("CALLBACK_URL", default=_call_back_url)
    )
    client_class = OAuth2Client


class SendVerificationTokenView(APIView):
    """
    An endpoint that encodes user data and generate JWT token

    Args:

        Email- a path parameter

    Response:

        HTTP_201_CREATED- if token for user is generated successfully

    Raise:

        HTTP_404_NOT_FOUND- if a user with supplied email does not exist
    """

    permission_classes = [AllowAny]

    def post(self, request, email):

        user = get_object_or_404(User, email=email)
        expiration_time = datetime.now(timezone.utc) + timedelta(seconds=600)
        encode_user_data = {"user_id": str(user.id), "expire": str(expiration_time)}
        encoded_jwt = jwt.encode(
            encode_user_data, settings.SECRET_KEY, algorithm="HS256"
        )
        return Response(status=status.HTTP_201_CREATED, data=encoded_jwt)


class TokenVerificationView(APIView):
    """
    An email verification endpoint

    Args:

        token- a path parameter

    Response:

        HTTP_200_OK- if email verification is successful

    Raise:

        HTTP_404_NOT_FOUND- if a user with supplied ID does not exist

        HTTP_400_BAD_REQUEST- if credential validation is unsuccessful or token has expired
    """

    permission_classes = [AllowAny]

    def post(self, request, token):

        if not token:
            return Response("token cannot be empty", status=status.HTTP_404_NOT_FOUND)

        credentials_exception = Response(
            status=status.HTTP_400_BAD_REQUEST,
            data="Could not validate credentials",
        )

        try:
            # Decodes token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user_id: str = payload.get("user_id")
            expire = payload.get("expire")
            if user_id is None or expire is None:
                raise credentials_exception
        except JWTError as e:
            msg = {"error": e, "time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}

            return credentials_exception

        # Check token expiration
        if str(datetime.now(timezone.utc)) > expire:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data="Token expired or invalid!",
            )

        user = get_object_or_404(User, id=user_id)
        get_allauth = get_object_or_404(EmailAddress, user=user)

        if get_allauth.verified == True:
            return Response("email already verified", status=status.HTTP_403_FORBIDDEN)

        get_allauth.verified = True
        get_allauth.save()
        return Response("verification successful", status=status.HTTP_200_OK)


# I will be back
class OTPView(APIView):

    # permission_classes = [IsAuthenticated]
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # self.hotp = HOTP('Hussein')

    def get(self, request):
        # global hotp

        hotp = HOTP(random_base32())

        otp = hotp.at(1)

        request.session["value"] = otp

        return Response({"detail": int(otp)})

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data["otp"]
        hotp = request.session.get("value", "")
        if hotp:
            if hotp.verify(otp, 1):

                # user = request.user
                # user.is_verified = True
                # user.save()
                return Response(
                    {"success": "2FA successful"}, status=status.HTTP_202_ACCEPTED
                )

            return Response({"error": "invalid otp"})

        return Response({"no value"})
