"""
Tests for the catalog app.
"""

from django.test import TestCase
from decimal import Decimal
from apps.catalog.models import Offer


class OfferModelTest(TestCase):
    """Test cases for the Offer model."""

    def setUp(self):
        """Set up test data."""
        self.offer_data = {
            "name": "solo",
            "capacity": 1,
            "price": Decimal("50.00"),
            "description": "Test offer",
            "is_active": True,
        }

    def test_offer_creation(self):
        """Test offer creation with required fields."""
        offer = Offer.objects.create(**self.offer_data)

        self.assertEqual(offer.name, "solo")
        self.assertEqual(offer.capacity, 1)
        self.assertEqual(offer.price, Decimal("50.00"))
        self.assertEqual(offer.description, "Test offer")
        self.assertTrue(offer.is_active)

    def test_offer_str_representation(self):
        """Test offer string representation."""
        offer = Offer.objects.create(**self.offer_data)
        expected = "Solo - 50.00€ (1 personne)"
        self.assertEqual(str(offer), expected)

    def test_get_capacity_display(self):
        """Test get_capacity_display method."""
        offer = Offer.objects.create(**self.offer_data)
        self.assertEqual(offer.get_capacity_display(), "1 personne")

        # Test with multiple capacity
        offer.capacity = 4
        self.assertEqual(offer.get_capacity_display(), "4 personnes")

    def test_is_available(self):
        """Test is_available method."""
        offer = Offer.objects.create(**self.offer_data)
        self.assertTrue(offer.is_available())

        offer.is_active = False
        offer.save()
        self.assertFalse(offer.is_available())

    def test_offer_choices(self):
        """Test offer type choices."""
        valid_choices = [choice[0] for choice in Offer.OFFER_TYPES]
        self.assertIn("solo", valid_choices)
        self.assertIn("duo", valid_choices)
        self.assertIn("familiale", valid_choices)

    def test_price_validation(self):
        """Test price validation."""
        # Test minimum price validation
        with self.assertRaises(Exception):  # ValidationError
            Offer.objects.create(
                name="test",
                capacity=1,
                price=Decimal("0.00"),  # Should fail minimum validation
                is_active=True,
            )

    def test_offer_ordering(self):
        """Test offer ordering by price."""
        Offer.objects.create(
            name="duo", capacity=2, price=Decimal("90.00"), is_active=True
        )
        Offer.objects.create(
            name="familiale", capacity=4, price=Decimal("160.00"), is_active=True
        )
        Offer.objects.create(**self.offer_data)  # solo - 50.00

        offers = Offer.objects.all()
        self.assertEqual(offers[0].name, "solo")  # Lowest price first
        self.assertEqual(offers[1].name, "duo")
        self.assertEqual(offers[2].name, "familiale")

    def test_offer_uniqueness(self):
        """Test that offer name must be unique."""
        Offer.objects.create(**self.offer_data)

        with self.assertRaises(Exception):  # IntegrityError
            Offer.objects.create(
                name="solo",  # Same name
                capacity=2,
                price=Decimal("100.00"),
                is_active=True,
            )
