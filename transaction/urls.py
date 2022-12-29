from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path(
        "make-payment/",
        views.MakePayment.as_view(),
        name="make_payment",
    ),
    path(
        "verify_transaction/<int:transaction_id>",
        views.VerifyTransaction.as_view(),
        name="verify_payment",
    ),
    path(
        "agent/withdraw/",
        views.AgentWithdrawal.as_view(),
        name="verify_payment",
    ),
    path("agent/balance/", views.AgentBalance.as_view(), name="balance"),
    path("history/all/", views.AllTransactionHistory.as_view()),
    path(
        "user/<str:user_id>/payment-history",
        views.UserTransactionHistory.as_view(),
    ),
]
