from django.urls import path
from .views import GoogleLogin, CustomRegisterView, ProfileViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path("register/", CustomRegisterView.as_view()),
    path('google/', GoogleLogin.as_view(), name='google-rest'), 
    
] + router.urls
