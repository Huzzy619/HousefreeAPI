from django.urls import path
from .views import GoogleLogin, CustomRegisterView, ProfileViewSet, AgentDetailsView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path("register/", CustomRegisterView.as_view()),
    path('login/google/', GoogleLogin.as_view(), name='google-rest'), 
    path("agent/verification", AgentDetailsView.as_view(), name="agent-verification") 
] + router.urls
