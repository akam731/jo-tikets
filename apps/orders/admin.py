"""
Admin configuration for the orders app.
"""

from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Order model.
    """

    list_display = ("id", "user", "offer", "amount", "status", "created_at")
    list_filter = ("status", "created_at", "offer")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        ("Informations générales", {"fields": ("user", "offer", "amount")}),
        ("Statut", {"fields": ("status",)}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related("user", "offer")
