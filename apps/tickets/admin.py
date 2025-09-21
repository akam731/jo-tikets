"""
Admin configuration for the tickets app.
"""

from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Ticket model.
    """

    list_display = ("id", "user", "order", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__email", "final_key", "order__id")
    readonly_fields = ("key2", "final_key", "created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        ("Informations générales", {"fields": ("order", "user", "status")}),
        (
            "Clés de sécurité",
            {"fields": ("key2", "final_key"), "classes": ("collapse",)},
        ),
        ("QR Code", {"fields": ("qr_image",)}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related("user", "order")
