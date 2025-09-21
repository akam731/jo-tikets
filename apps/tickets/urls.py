"""
URL configuration for the tickets app.
"""

from django.urls import path
from . import views

app_name = "tickets"

urlpatterns = [
    path("mes-billets/", views.my_tickets_view, name="my_tickets"),
    path("billet/<int:ticket_id>/", views.ticket_detail_view, name="ticket_detail"),
    path("api/billets/valider/", views.validate_ticket_api, name="validate_ticket_api"),
]
