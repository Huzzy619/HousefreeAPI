from django.urls import path

from .views import (
    MarkNotificationAsReadAPIView,
    NotificationDeleteView,
    NotificationListAPIView,
)

urlpatterns = [
    path("notifications/", NotificationListAPIView.as_view(), name="notification-list"),
    path(
        "notifications/<int:pk>/read/",
        MarkNotificationAsReadAPIView.as_view(),
        name="notification-read",
    ),
    path(
        "notifications/<int:pk>/delete/",
        NotificationDeleteView.as_view(),
        name="notification-read",
    ),
]
