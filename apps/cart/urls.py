"""
URL configuration for the cart app.
"""

from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("panier/", views.cart_view, name="cart"),
    path("panier/ajouter/", views.add_to_cart, name="add_to_cart"),
    path(
        "panier/modifier/<int:item_id>/",
        views.update_cart_item,
        name="update_cart_item",
    ),
    path(
        "panier/supprimer/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path(
        "panier/modifier-quantite/",
        views.update_quantity_ajax,
        name="update_quantity_ajax",
    ),
    path("panier/supprimer/", views.remove_item_ajax, name="remove_item_ajax"),
    path("panier/finaliser/", views.checkout_view, name="checkout"),
    path("panier/paiement/", views.process_payment, name="process_payment"),
]
