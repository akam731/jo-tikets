"""
URL configuration for the orders app.
"""

from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("finalisation/", views.checkout_view, name="checkout"),
    path("confirmation/<int:order_id>/", views.confirmation_view, name="confirmation"),
    path("api/commandes/", views.create_order_api, name="create_order_api"),
    path("api/paiements/mock/", views.mock_payment_api, name="mock_payment_api"),
]
