from django.urls import path
from rest_framework import routers

from .views import ContactViewSet, NewsletterViewSet, form_subscribe

router = routers.DefaultRouter()

router.register("subscribe", NewsletterViewSet)
router.register("contact", ContactViewSet)

urlpatterns = [
    path(
        "form_subscribe", form_subscribe , name='form_subscribe'
    )
] + router.urls
