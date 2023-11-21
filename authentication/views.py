from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError

# Create your views here.
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.exception_handlers import ErrorEnum, ErrorResponse, response_schemas

from .serializers import (
    GoogleSocialAuthSerializer,
    InfoSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)
from django.http import HttpRequest

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
        serializer.save()
        serializer = InfoSerializer(
            data={"message": "Registered successfully", "status": True}
        )
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
