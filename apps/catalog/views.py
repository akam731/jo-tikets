"""
Views for the catalog app.
"""

from django.views.generic import ListView
from .models import Offer


class OfferListView(ListView):
    """
    View to display all available offers.
    """

    model = Offer
    template_name = "catalog/offers.html"
    context_object_name = "offers"

    def get_queryset(self):
        """Return only active offers."""
        return Offer.objects.filter(is_active=True).order_by("price")

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Nos Offres"
        return context
