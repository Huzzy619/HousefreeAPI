from django.urls import path

from . import views

urlpatterns = [
    path("api/v1/user/<str:email>/messages", views.GetUserMessages.as_view()),
]
