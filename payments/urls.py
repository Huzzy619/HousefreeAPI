from django.urls import path
from . import views

urlpatterns = [
	path('pay/card-deposit-flutterwave/', views.flutterwave_card_deposit),
    path('flw-deposit/verify/', views.flutterwave_confirm_card_deposit),
	
	path('pay/card-deposit-paytack/', views.paystack_card_deposit),
    path('deposit/verify/<str:reference>/', views.verify_paystack_payment),
]
