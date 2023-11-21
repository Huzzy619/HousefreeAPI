from django.contrib import messages
from django.core.validators import EmailValidator
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Contact, HelpDesk, Newsletter, Report
from .serializers import (
    ContactSerializer,
    HelpDeskSerializer,
    NewsletterSerializer,
    ReportListingSerializer,
)


class ReportListingView(CreateAPIView):
    """
    The apartment field represents the `id` of the current apartment being reported.

    Example data:

        {
            "problem":"Other problems",
            "description":"Love and War",
            "apartment": 1
        }

    Returns:

        An instance of the newly created report for a listing

    """

    queryset = Report.objects.none()
    permission_classes = [IsAuthenticated]
    serializer_class = ReportListingSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}


class ContactView(CreateAPIView):
    queryset = Contact.objects.none()
    serializer_class = ContactSerializer


class NewsletterView(CreateAPIView):
    """
    request body for both subscribe endpoints

    Post : `Subscribe`

    Delete : `Unsubscribe`

        {

            "email":"user@example.com"
        }
    """

    serializer_class = NewsletterSerializer

    def delete(self, request, **kwargs):
        validate = EmailValidator()
        try:
            validate(request.data["email"])
        except Exception as e:
            return Response({"detail": e}, status.HTTP_400_BAD_REQUEST)

        if obj := Newsletter.objects.filter(email=request.data["email"]):
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"detail": "email not subscribed previously"}, status.HTTP_404_NOT_FOUND
        )


class HelpDeskView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = HelpDesk.objects.none()
    serializer_class = HelpDeskSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}


def form_subscribe(request):
    """
    Form subscription from the index page

    Args:
        request
        email

    Returns:
        Redirect to home page
    """
    email = request.POST.get("email", "")

    if Newsletter.objects.filter(email=email):
        messages.error(request, "Email is subscribed already")
    else:
        Newsletter.objects.create(email=email)
        messages.success(request, "Email subscribed successfully")

    return redirect("index")
