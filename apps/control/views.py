"""
Views for the control app.

This app handles QR code scanning and ticket validation for employees.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


def is_employee(user):
    """
    Check if user is an employee (can access QR scanning).
    """
    return user.is_authenticated and user.is_employee


@login_required
@user_passes_test(is_employee)
def scan_view(request):
    """
    QR code scanning page for employees.

    Only accessible to users with is_employee=True.
    """
    return render(request, "control/scan.html", {"title": "Scan des Billets"})
