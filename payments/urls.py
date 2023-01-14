from django.urls import path
from . import views

urlpatterns = [
    path('deposit/verify/<str:reference>/', views.verify_paystack_payment),
]
