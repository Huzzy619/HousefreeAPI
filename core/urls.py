from django.urls import path
from .views import (
    GoogleLogin, CustomRegisterView, 
    ProfileViewSet, AgentDetailsView,
    Send_verification_token, Token_verification
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path("register/", CustomRegisterView.as_view()),
    path('login/google/', GoogleLogin.as_view(), name='google-rest'), 
    path("agent/verification", AgentDetailsView.as_view(), name="agent-verification"),
     path("get-token/<str:email>", Send_verification_token.as_view(), name="send-token"),
    path("token-verification/<str:token>", Token_verification.as_view(), name="token-verification") 
] + router.urls
