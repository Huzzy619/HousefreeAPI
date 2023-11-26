from decouple import config
from django.contrib.auth import get_user_model
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework_simplejwt.tokens import RefreshToken

from core.exception_handlers import ErrorEnum, ErrorResponse


def register_with_google(email, **kwargs):
    user_check = (
        get_user_model()
        .objects.filter(email=email, google_id=kwargs.get("google_id"))
        .first()
    )

    kwargs.pop("picture", None)  # For now, we would update the profile picture later
    if user_check:
        return ErrorResponse(
            code=ErrorEnum.ERR_007,
            extra_detail="Google account with this email already exists",
        )

    user = get_user_model().objects.create_user(
        email=email, password=config("SOCIAL_PASSWORD"), **kwargs
    )

    refresh = RefreshToken.for_user(user)

    access = refresh.access_token

    return {"tokens": {"access": str(access), "refresh": str(refresh)}, "user": user}


def login_with_google(email, google_id):
    user = get_user_model().objects.filter(email=email, google_id=google_id).first()

    if not user:
        return ErrorResponse(
            code=ErrorEnum.ERR_007,
            extra_detail="No Google account found with this email",
        )

    refresh = RefreshToken.for_user(user)

    access = refresh.access_token

    return {"tokens": {"access": str(access), "refresh": str(refresh)}, "user": user}


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            response_data = id_token.verify_oauth2_token(
                auth_token, google_requests.Request()
            )

            if "accounts.google.com" in response_data["iss"]:
                return response_data
        except Exception:
            return ErrorResponse(
                code=ErrorEnum.ERR_007,
                extra_detail="The token is either invalid or has expired",
            )
