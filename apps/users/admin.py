"""
Admin configuration for the users app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin configuration.

    Extends Django's default UserAdmin to include custom fields
    and maintain the existing functionality.
    """

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_employee",
        "is_adminpanel",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_employee",
        "is_adminpanel",
        "is_staff",
        "is_active",
        "date_joined",
    )
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("JO Tickets Specific", {"fields": ("key1", "is_employee", "is_adminpanel")}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("JO Tickets Specific", {"fields": ("key1", "is_employee", "is_adminpanel")}),
    )

    readonly_fields = ("key1",)
