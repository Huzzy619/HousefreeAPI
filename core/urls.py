from django.urls import path
from .views import (
    GoogleLogin, CustomRegisterView, 
    ProfileViewSet, AgentDetailsView,
    SendVerification_token, TokenVerification, OTPView
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path("register/", CustomRegisterView.as_view()),
    path('login/google/', GoogleLogin.as_view(), name='google-rest'), 
    path("agent/verification", AgentDetailsView.as_view(), name="agent-verification"), 
    path('otp', OTPView.as_view()),

    path("get-token/<str:email>/", SendVerification_token.as_view(), name="send-token"),
    path("token-verification/<str:token>/", TokenVerification.as_view(), name="token-verification") 
] + router.urls
