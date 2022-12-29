from rest_framework.viewsets import ModelViewSet
from django.shortcuts import redirect
from .models import Contact, Newsletter
from .serializers import ContactSerializer, NewsletterSerializer

# Create your views here.


class ContactViewSet(ModelViewSet):
    http_method_names = ["post", "head", "options"]

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class NewsletterViewSet(ModelViewSet):
    http_method_names = ["post", "head", "options"]

    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


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
    Newsletter.objects.get_or_create(email=email)

    return redirect('index')
