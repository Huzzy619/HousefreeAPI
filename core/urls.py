from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AgentDetailsView,
    CustomRegisterView,
    GoogleLogin,
    ProfileViewSet,
    SendVerificationTokenView,
    TokenVerificationView,
    UserSettingsViewSet,
)

# from dj_rest_auth.views import PasswordResetConfirmView

router = DefaultRouter()
# router.register("profile", ProfileViewSet, basename="profile")
router.register("settings", UserSettingsViewSet, basename="settings")

urlpatterns = [
    path("register/", CustomRegisterView.as_view()),
    path("login/google/", GoogleLogin.as_view(), name="google-rest"),
    path("agent/verification/", AgentDetailsView.as_view(), name="agent-verification"),
    # path("otp/", OTPView.as_view()),
    path(
        "get-token/<str:email>/", SendVerificationTokenView.as_view(), name="send-token"
    ),
    path(
        "token-verification/<str:token>/",
        TokenVerificationView.as_view(),
        name="token-verification",
    ),
    # path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
] + router.urls


# dj_rest_auth_urls

from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    # PasswordChangeView,
    # PasswordResetConfirmView,
    # PasswordResetView,
    # UserDetailsView,
)
from django.conf import settings

urlpatterns += [
    # URLs that do not require a session or valid token
    # path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    # path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path("login/", LoginView.as_view(), name="rest_login"),
    # URLs that require a user to be logged in with a valid session / token.
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    # path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    # path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
]

if getattr(settings, "REST_USE_JWT", False):
    from dj_rest_auth.jwt_auth import get_refresh_view
    from rest_framework_simplejwt.views import TokenVerifyView

    urlpatterns += [
        path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
        path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    ]
