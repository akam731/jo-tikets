"""
URL configuration for the control app.
"""

from django.urls import path
from . import views

app_name = "control"

urlpatterns = [
    path("controle/scanner/", views.scan_view, name="scan"),
]
