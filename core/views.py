import os

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from decouple import config
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from utils.permissions import IsAgent

from .models import AgentDetails, Profile
from .permissions import IsOwner
from .serializers import (
    AgentDetailsSerializer,
    CustomRegisterSerializer,
    CustomSocialLoginSerializer,
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
        "CALLBACK_URL", config("CALLBACK_URL", _call_back_url)
    )
    client_class = OAuth2Client
