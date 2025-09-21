"""
Tests for the orders app.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from apps.orders.models import Order
from apps.catalog.models import Offer

User = get_user_model()


class OrderModelTest(TestCase):
    """Test cases for the Order model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            password="testpass123",
        )

        self.offer = Offer.objects.create(
            name="solo", capacity=1, price=Decimal("50.00"), is_active=True
        )

    def test_order_creation(self):
        """Test order creation with required fields."""
        order = Order.objects.create(
            user=self.user, offer=self.offer, amount=Decimal("50.00")
        )

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.offer, self.offer)
        self.assertEqual(order.amount, Decimal("50.00"))
        self.assertEqual(order.status, "pending")

    def test_order_str_representation(self):
        """Test order string representation."""
        order = Order.objects.create(
            user=self.user, offer=self.offer, amount=Decimal("50.00")
        )
        expected = f"Commande #{order.id} - {self.user.email} - solo - pending"
        self.assertEqual(str(order), expected)

    def test_get_status_display_class(self):
        """Test get_status_display_class method."""
        order = Order.objects.create(
            user=self.user, offer=self.offer, amount=Decimal("50.00")
        )

        self.assertEqual(order.get_status_display_class(), "badge-warning")

        order.status = "paid"
        self.assertEqual(order.get_status_display_class(), "badge-success")

        order.status = "cancelled"
        self.assertEqual(order.get_status_display_class(), "badge-error")

    def test_can_be_cancelled(self):
        """Test can_be_cancelled method."""
        order = Order.objects.create(
            user=self.user, offer=self.offer, amount=Decimal("50.00")
        )

        self.assertTrue(order.can_be_cancelled())

        order.status = "paid"
        order.save()
        self.assertFalse(order.can_be_cancelled())

    def test_can_be_paid(self):
        """Test can_be_paid method."""
        order = Order.objects.create(
            user=self.user, offer=self.offer, amount=Decimal("50.00")
        )

        self.assertTrue(order.can_be_paid())

        order.status = "paid"
        order.save()
        self.assertFalse(order.can_be_paid())

    def test_mark_as_paid(self):
        """Test mark_as_paid method."""
        order = Order.objects.create(
            user=self.user, offer=self.offer, amount=Decimal("50.00")
        )

        self.assertTrue(order.mark_as_paid())
        order.refresh_from_db()
        self.assertEqual(order.status, "paid")

    def test_mark_as_cancelled(self):
        """Test mark_as_cancelled method."""
        order = Order.objects.create(
            user=self.user, offer=self.offer, amount=Decimal("50.00")
        )

        self.assertTrue(order.mark_as_cancelled())
        order.refresh_from_db()
        self.assertEqual(order.status, "cancelled")

    def test_order_ordering(self):
        """Test order ordering by creation date (newest first)."""
        order1 = Order.objects.create(
            user=self.user, offer=self.offer, amount=Decimal("50.00")
        )

        order2 = Order.objects.create(
            user=self.user, offer=self.offer, amount=Decimal("50.00")
        )

        orders = Order.objects.all()
        self.assertEqual(orders[0], order2)  # Newest first
        self.assertEqual(orders[1], order1)

    def test_order_status_choices(self):
        """Test order status choices."""
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        self.assertIn("pending", valid_statuses)
        self.assertIn("paid", valid_statuses)
        self.assertIn("cancelled", valid_statuses)
