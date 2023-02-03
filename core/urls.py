from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AgentDetailsView,
    CustomRegisterView,
    GoogleLogin,
    OTPView,
    ProfileViewSet,
    SendVerificationTokenView,
    TokenVerificationView,
    UserSettingsViewSet,
)

# from dj_rest_auth.views import PasswordResetConfirmView

router = DefaultRouter()
router.register("profile", ProfileViewSet, basename="profile")
router.register("settings", UserSettingsViewSet, basename='settings') 

urlpatterns = [
    path("register/", CustomRegisterView.as_view()),
    path("login/google/", GoogleLogin.as_view(), name="google-rest"),
    path("agent/verification/", AgentDetailsView.as_view(), name="agent-verification"),
    path("otp/", OTPView.as_view()),
    path(
        "get-token/<str:email>/", SendVerificationTokenView.as_view(), name="send-token"
    ),
    path(
        "token-verification/<str:token>/",
        TokenVerificationView.as_view(),
        name="token-verification",
    ),
    # path("settings/", UserSettingsViewSet.as_view(), name='settings')
    # path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
] + router.urls
