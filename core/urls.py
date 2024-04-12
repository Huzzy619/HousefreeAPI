from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
# router.register("profile", ProfileViewSet, basename="profile")
router.register("settings", views.UserSettingsViewSet, basename="settings")

urlpatterns = [
    path("register", views.RegisterView.as_view()),
    path("login", views.LoginView.as_view()),
    path("login/google", views.GoogleSocialAuthView.as_view()),
    path("signup/google", views.GoogleSocialAuthView.as_view()),
    path("refresh/token", views.RefreshView.as_view()),
    path(
        "agent/verification",
        views.AgentDetailsView.as_view(),
        name="agent-verification",
    ),
    path("otp/resend/<str:email>/<str:event>", views.GetOTPView.as_view()),
    path("otp/verify", views.VerifyOTPView.as_view()),
] + router.urls


# urlpatterns = [
# path("otp/send/order/<str:email>", views.GetOTPView.as_view()),
# path("otp/send/forgot-password/<str:email>", views.GetOTPView.as_view()),
# path("otp/resend/email-verify-code/<str:email>", views.GetOTPView.as_view()),
# path("otp/verify", views.VerifyOTPView.as_view()),
# path("user/profile", views.ProfileView.as_view()),
# path("change/password", views.ChangePasswordView.as_view()),
# path("otp/change/password", views.OTPChangePasswordView.as_view()),
# path("user/settings", views.UserSettingsView.as_view())
# ]
