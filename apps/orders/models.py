"""
Modèles de commande pour l'application JO Tickets.

Projet étudiant - BTS SIO
Date : Septembre 2024

J'ai créé ce modèle pour gérer les commandes des utilisateurs.
C'est un peu compliqué mais j'ai réussi à faire marcher !
"""

from django.db import models
from django.contrib.auth import get_user_model
from apps.catalog.models import Offer

User = get_user_model()


class Order(models.Model):
    """
    Modèle représentant une commande de billets.

    Chaque commande est associée à un utilisateur et une offre, et suit
    le statut de paiement et le montant.
    """

    STATUS_CHOICES = [
        ("pending", "En attente de paiement"),
        ("paid", "Payé"),
        ("cancelled", "Annulé"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        help_text="Utilisateur qui a passé la commande",
    )
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="orders",
        help_text="Offre commandée",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Statut de la commande",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Montant total de la commande"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders_order"
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Commande #{self.id} - {self.user.email} - {self.offer.name} - {self.status}"

    def get_status_display_class(self):
        """Retourne la classe CSS pour l'affichage du statut."""
        status_classes = {
            "pending": "badge-warning",
            "paid": "badge-success",
            "cancelled": "badge-error",
        }
        return status_classes.get(self.status, "badge-neutral")

    def can_be_cancelled(self):
        """Vérifie si la commande peut être annulée."""
        return self.status == "pending"

    def can_be_paid(self):
        """Vérifie si la commande peut être payée."""
        return self.status == "pending"

    def mark_as_paid(self):
        """Marque la commande comme payée."""
        if self.can_be_paid():
            self.status = "paid"
            self.save(update_fields=["status", "updated_at"])
            return True
        return False

    def mark_as_cancelled(self):
        """Marque la commande comme annulée."""
        if self.can_be_cancelled():
            self.status = "cancelled"
            self.save(update_fields=["status", "updated_at"])
            return True
        return False
