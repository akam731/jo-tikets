"""
URL configuration for the adminpanel app.
"""

from django.urls import path
from . import views

app_name = "adminpanel"

urlpatterns = [
    path("administration/", views.dashboard_view, name="dashboard"),
    path("administration/offres/", views.offers_crud_view, name="offers_crud"),
    path("api/administration/offres/", views.offers_api, name="offers_api"),
    path(
        "api/administration/offres/creer/",
        views.create_offer_api,
        name="create_offer_api",
    ),
    path(
        "api/administration/offres/<int:offer_id>/",
        views.update_offer_api,
        name="update_offer_api",
    ),
    path(
        "api/administration/offres/<int:offer_id>/supprimer/",
        views.delete_offer_api,
        name="delete_offer_api",
    ),
]
