"""
URL configuration for the catalog app.
"""

from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("offres/", views.OfferListView.as_view(), name="offers"),
]
