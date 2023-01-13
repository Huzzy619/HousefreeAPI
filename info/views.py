from rest_framework.viewsets import ModelViewSet
from django.shortcuts import redirect
from .models import Contact, Newsletter, HelpDesk
from .serializers import ContactSerializer, NewsletterSerializer, HelpDeskSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
# Create your views here.


class ContactViewSet(ModelViewSet):
    http_method_names = ["post", "head", "options"]

    queryset = Contact.objects.none()
    serializer_class = ContactSerializer


class NewsletterViewSet(ModelViewSet):
    http_method_names = ["post", "head", "options"]

    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

class HelpDeskViewSet(ModelViewSet):
    http_method_names = ["post", "head", "options"]
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


    if Newsletter.objects.filter(email = email):
        messages.error(request, "Email is subscribed already")
    else:
        Newsletter.objects.create(email= email)
        messages.success(request, "Email subscribed successfully")


    return redirect('index')
