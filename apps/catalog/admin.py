"""
Admin configuration for the catalog app.
"""

from django.contrib import admin
from .models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Offer model.
    """

    list_display = ("name", "get_capacity_display", "price", "is_active", "created_at")
    list_filter = ("is_active", "name", "created_at")
    search_fields = ("name", "description")
    list_editable = ("is_active",)
    ordering = ("price",)

    fieldsets = (
        (
            "Informations générales",
            {"fields": ("name", "capacity", "price", "description")},
        ),
        ("Statut", {"fields": ("is_active",)}),
    )

    readonly_fields = ("created_at", "updated_at")
