from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework.viewsets import ModelViewSet

from .models import Profile
from .permissions import IsOwner
from .serializers import (
    CustomRegisterSerializer,
    CustomSocialLoginSerializer,
    ProfileSerializer,
)
from decouple import config
import os


class ProfileViewSet(ModelViewSet):
    http_method_names = ["get", "options", "head", "put"]
    permission_classes = [IsOwner]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class CustomSocialLoginView(SocialLoginView):
    """_summary_

    Args:
        SocialLoginView (_type_): _description_
    """

    serializer_class = CustomSocialLoginSerializer


class CustomRegisterView(RegisterView):
    """_summary_

    Args:
        RegisterView (_type_): _description_

    Returns:
        _type_: _description_
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
    """_summary_

    Args:
        CustomSocialLoginView (_type_): _description_
    """

    adapter_class = GoogleOAuth2Adapter
    # CALLBACK_URL_YOU_SET_ON_GOOGLE
    default = "http://127.0.0.1:8000/accounts/google/login/callback/"
    callback_url = os.environ.get("CALLBACK_URL", config("CALLBACK_URL", default))
    client_class = OAuth2Client


def google_view(request):

    """
    # Alternatively, you can send a post request from directly.

    response = requests.post('http://127.0.0.1:8000/dj/google', data={'code': code})
    print("status: " + response.status_code)
    print(response.json()['access_token'])
    """
    # This View just gets the code and prints on the terminal.

    code = request.GET.get("code")
    print(f"The code is : {code}")
    print("go to the browser to make a post request")

    return redirect("google-rest")


# https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://127.0.0.1:8000/accounts/google/login/callback/&prompt=consent&response_type=code&client_id=878674025478-e8s4rf34md8h4n7qobb6mog43nfhfb7r.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline
