from django.urls import path

from .views import (
    form_subscribe,
    NewsletterView,
    HelpDeskView,
    ContactView,
    ReportListingView,
)


urlpatterns = [
    path(
        "form_subscribe/",
        form_subscribe,
        name="form_subscribe",
    ),
    path("subscribe", NewsletterView.as_view()),
    path("help/desk", HelpDeskView.as_view()),
    path("contact", ContactView.as_view()),
    path("report/listing", ReportListingView.as_view(), name="report-listing"),
]
