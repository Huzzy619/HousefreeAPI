from django.urls import path
from . import views

urlpatterns = [
	path('pay/card-deposit-flutterwave/', views.flutterwave_card_deposit),
    path('deposit/verify/<str:reference>/', views.verify_paystack_payment),
]
