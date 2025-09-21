"""
Modèles de panier pour l'application JO Tickets.

Projet étudiant - BTS SIO
Date : Septembre 2024

J'ai créé ces modèles pour gérer le panier d'achat.
C'est comme un panier de supermarché mais pour les billets !
"""

from django.db import models
from django.conf import settings
from apps.catalog.models import Offer


class Cart(models.Model):
    """
    Modèle de panier d'achat.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cart_cart"
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"

    def __str__(self):
        return f"Panier pour {self.user.email}"

    @property
    def total_price(self):
        """Calcule le prix total de tous les articles dans le panier."""
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        """Calcule le nombre total d'articles dans le panier."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Article individuel dans le panier d'achat.
    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cart_cartitem"
        verbose_name = "Article du panier"
        verbose_name_plural = "Articles du panier"

    def __str__(self):
        return f"{self.quantity}x {self.offer.name} dans le panier de {self.cart.user.email}"

    @property
    def total_price(self):
        """Calcule le prix total pour cet article."""
        return self.offer.price * self.quantity
