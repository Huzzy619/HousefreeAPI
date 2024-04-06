from django.urls import path

from . import views, webhooks

urlpatterns = [
    path("plans/", views.PlanView.as_view(), name="plans"),
    path("bank-details/", views.BankDetailView.as_view(), name="bank_details"),
    path(
        "agent/subscription/", views.AgentSubscriptionView.as_view(), name="agent_sub"
    ),
    path("history/", views.PaymentHistoryView.as_view()),
    path("make-payment/", views.PaymentView.as_view()),
    path("webhooks/paystack/", webhooks.paystack_webhook),
]
