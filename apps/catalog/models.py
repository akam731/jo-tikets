"""
Modèles de catalogue pour l'application JO Tickets.

Projet étudiant - BTS SIO
Date : Septembre 2024

J'ai créé ce modèle pour gérer les différentes offres de billets.
C'est assez simple mais ça fait le travail !
"""

from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator


class Offer(models.Model):
    """
    Modèle représentant différentes offres de billets pour les Jeux Olympiques.

    Chaque offre a une capacité spécifique (1 pour solo, 2 pour duo, 4 pour familiale)
    et un prix correspondant. Les offres peuvent être activées ou désactivées.
    """

    OFFER_TYPES = [
        ("solo", "Solo (1 personne)"),
        ("duo", "Duo (2 personnes)"),
        ("familiale", "Familiale (4 personnes)"),
    ]

    name = models.CharField(
        max_length=50,
        choices=OFFER_TYPES,
        unique=True,
        help_text="Type d'offre (solo, duo, familiale)",
    )
    capacity = models.PositiveIntegerField(
        help_text="Nombre de personnes pour cette offre"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Prix de l'offre en euros",
    )
    is_active = models.BooleanField(
        default=True, help_text="Indique si l'offre est disponible à la vente"
    )
    description = models.TextField(
        blank=True, help_text="Description détaillée de l'offre"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "catalog_offer"
        verbose_name = "Offre"
        verbose_name_plural = "Offres"
        ordering = ["price"]

    def __str__(self):
        return f"{self.get_name_display()} - {self.price}€ ({self.capacity} personne{'s' if self.capacity > 1 else ''})"

    def get_capacity_display(self):
        """Retourne une description lisible de la capacité."""
        if self.capacity == 1:
            return "1 personne"
        return f"{self.capacity} personnes"

    def is_available(self):
        """Vérifie si l'offre est disponible à l'achat."""
        return self.is_active
