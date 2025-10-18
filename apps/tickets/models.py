"""
Modèles de billet pour l'application JO Tickets.

Projet étudiant - BTS SIO
Date : Septembre 2024
"""

import secrets
import qrcode
from io import BytesIO
from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from apps.orders.models import Order

User = get_user_model()


def qr_code_upload_path(instance, filename):
    """
    Génère le chemin d'upload pour les images de codes QR.

    Format: media/qr/tickets/{ticket_id}_{final_key[:8]}.png
    """
    return f"qr/tickets/{instance.id}_{instance.final_key[:8]}.png"


class Ticket(models.Model):
    """
    Modèle représentant un billet individuel.

    Chaque billet est associé à une commande et contient :
    - key2: Clé secrète générée au moment de l'achat
    - final_key: Concatenation de user.key1 + key2
    - qr_image: Fichier image du code QR
    - status: Statut valide ou utilisé
    """

    STATUS_CHOICES = [
        ("valid", "Valide"),
        ("used", "Utilisé"),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="ticket",
        help_text="Commande associée à ce billet",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tickets",
        help_text="Propriétaire du billet",
    )
    key2 = models.CharField(max_length=64, help_text="Clé secrète générée à l'achat")
    final_key = models.CharField(
        max_length=128, unique=True, help_text="Clé finale = key1 + key2"
    )
    qr_image = models.ImageField(
        upload_to=qr_code_upload_path,
        blank=True,
        null=True,
        help_text="Image QR code du billet",
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="valid",
        help_text="Statut du billet",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tickets_ticket"
        verbose_name = "Billet"
        verbose_name_plural = "Billets"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Billet #{self.id} - {self.user.email} - {self.status}"

    def save(self, *args, **kwargs):
        """
        Surcharge save pour générer key2 et final_key s'ils ne sont pas définis.
        """
        if not self.key2:
            self.key2 = secrets.token_urlsafe(32)

        if not self.final_key and self.user.key1:
            self.final_key = self.user.key1 + self.key2

        super().save(*args, **kwargs)

        # Générer le code QR s'il n'existe pas
        if not self.qr_image and self.final_key:
            self.generate_qr_code()

    def generate_qr_code(self):
        """
        Génère l'image du code QR pour ce billet.

        Le code QR contient uniquement la final_key pour des raisons de sécurité.
        Aucune information personnelle n'est encodée dans le code QR.
        """
        if not self.final_key:
            return

        # Créer le code QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.final_key)
        qr.make(fit=True)

        # Créer l'image
        img = qr.make_image(fill_color="black", back_color="white")

        # Sauvegarder dans BytesIO
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Générer le nom de fichier
        # Utiliser un nom qui correspond exactement à l'URL attendue
        # /media/qr/tickets/{id}_{final_key_prefix}.png
        filename = f"{self.id}_{self.final_key[:8]}.png"

        # Sauvegarder dans ImageField
        self.qr_image.save(filename, ContentFile(buffer.getvalue()), save=True)

    def get_status_display_class(self):
        """Retourne la classe CSS pour l'affichage du statut."""
        status_classes = {
            "valid": "badge-success",
            "used": "badge-error",
        }
        return status_classes.get(self.status, "badge-neutral")

    def is_valid(self):
        """Vérifie si le billet est valide pour utilisation."""
        return self.status == "valid"

    def is_used(self):
        """Vérifie si le billet a été utilisé."""
        return self.status == "used"

    def mark_as_used(self):
        """Marque le billet comme utilisé."""
        if self.is_valid():
            self.status = "used"
            self.save(update_fields=["status", "updated_at"])
            return True
        return False

    @classmethod
    def validate_ticket(cls, final_key):
        """
        Valide un billet par sa final_key.

        Cette méthode effectue une validation atomique et marque comme utilisé.
        Retourne un tuple (is_valid, ticket, message).
        """
        try:
            with transaction.atomic():
                # Utiliser select_for_update pour éviter les conditions de course
                ticket = cls.objects.select_for_update().get(final_key=final_key)

                if not ticket.is_valid():
                    return False, ticket, "Ce billet a déjà été utilisé"

                # Vérifier si la commande associée est payée
                if ticket.order.status != "paid":
                    return False, ticket, "Cette commande n'est pas payée"

                # Marquer comme utilisé
                ticket.mark_as_used()

                return True, ticket, "Billet validé avec succès"

        except cls.DoesNotExist:
            return False, None, "Billet non trouvé"
        except Exception as e:
            return False, None, f"Erreur lors de la validation: {str(e)}"

    @classmethod
    def get_ticket_info(cls, final_key):
        """
        Récupère les informations d'un billet par sa final_key.

        Retourne les informations même si le billet est déjà utilisé.
        Retourne un tuple (found, ticket, message).
        """
        try:
            ticket = cls.objects.get(final_key=final_key)

            # Vérifier si la commande associée est payée
            if ticket.order.status != "paid":
                return False, ticket, "Cette commande n'est pas payée"

            return True, ticket, "Informations du billet récupérées"

        except cls.DoesNotExist:
            return False, None, "Billet introuvable"
        except Exception as e:
            return False, None, f"Erreur lors de la récupération: {str(e)}"
