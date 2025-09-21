"""
Admin configuration for the cart app.
"""

from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin configuration for Cart model."""

    list_display = ["user", "total_items", "total_price", "created_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["user__email", "user__first_name", "user__last_name"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin configuration for CartItem model."""

    list_display = ["cart", "offer", "quantity", "total_price", "created_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["cart__user__email", "offer__name"]
    readonly_fields = ["created_at", "updated_at"]
