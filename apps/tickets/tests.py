"""
Tests for the tickets app.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from apps.tickets.models import Ticket
from apps.orders.models import Order
from apps.catalog.models import Offer

User = get_user_model()


class TicketModelTest(TestCase):
    """Test cases for the Ticket model."""

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

        self.order = Order.objects.create(
            user=self.user, offer=self.offer, amount=Decimal("50.00"), status="paid"
        )

    def test_ticket_creation(self):
        """Test ticket creation with required fields."""
        ticket = Ticket.objects.create(order=self.order, user=self.user)

        self.assertEqual(ticket.order, self.order)
        self.assertEqual(ticket.user, self.user)
        self.assertEqual(ticket.status, "valid")
        self.assertTrue(ticket.key2)
        self.assertTrue(ticket.final_key)
        self.assertEqual(len(ticket.key2), 43)  # token_urlsafe(32) produces 43 chars

    def test_ticket_str_representation(self):
        """Test ticket string representation."""
        ticket = Ticket.objects.create(order=self.order, user=self.user)
        expected = f"Billet #{ticket.id} - {self.user.email} - valid"
        self.assertEqual(str(ticket), expected)

    def test_final_key_generation(self):
        """Test final_key generation (key1 + key2)."""
        ticket = Ticket.objects.create(order=self.order, user=self.user)

        expected_final_key = self.user.key1 + ticket.key2
        self.assertEqual(ticket.final_key, expected_final_key)

    def test_get_status_display_class(self):
        """Test get_status_display_class method."""
        ticket = Ticket.objects.create(order=self.order, user=self.user)

        self.assertEqual(ticket.get_status_display_class(), "badge-success")

        ticket.status = "used"
        self.assertEqual(ticket.get_status_display_class(), "badge-error")

    def test_is_valid(self):
        """Test is_valid method."""
        ticket = Ticket.objects.create(order=self.order, user=self.user)

        self.assertTrue(ticket.is_valid())

        ticket.status = "used"
        ticket.save()
        self.assertFalse(ticket.is_valid())

    def test_mark_as_used(self):
        """Test mark_as_used method."""
        ticket = Ticket.objects.create(order=self.order, user=self.user)

        self.assertTrue(ticket.mark_as_used())
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "used")

    def test_validate_ticket_success(self):
        """Test validate_ticket method with valid ticket."""
        ticket = Ticket.objects.create(order=self.order, user=self.user)

        is_valid, returned_ticket, message = Ticket.validate_ticket(ticket.final_key)

        self.assertTrue(is_valid)
        self.assertEqual(returned_ticket, ticket)
        self.assertIn("succès", message)

        # Check that ticket is now marked as used
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "used")

    def test_validate_ticket_not_found(self):
        """Test validate_ticket method with non-existent ticket."""
        is_valid, ticket, message = Ticket.validate_ticket("invalid_key")

        self.assertFalse(is_valid)
        self.assertIsNone(ticket)
        self.assertIn("non trouvé", message)

    def test_validate_ticket_already_used(self):
        """Test validate_ticket method with already used ticket."""
        ticket = Ticket.objects.create(order=self.order, user=self.user, status="used")

        is_valid, returned_ticket, message = Ticket.validate_ticket(ticket.final_key)

        self.assertFalse(is_valid)
        self.assertEqual(returned_ticket, ticket)
        self.assertIn("déjà été utilisé", message)

    def test_validate_ticket_unpaid_order(self):
        """Test validate_ticket method with unpaid order."""
        unpaid_order = Order.objects.create(
            user=self.user, offer=self.offer, amount=Decimal("50.00"), status="pending"
        )

        ticket = Ticket.objects.create(order=unpaid_order, user=self.user)

        is_valid, returned_ticket, message = Ticket.validate_ticket(ticket.final_key)

        self.assertFalse(is_valid)
        self.assertEqual(returned_ticket, ticket)
        self.assertIn("pas payée", message)

    def test_ticket_ordering(self):
        """Test ticket ordering by creation date (newest first)."""
        ticket1 = Ticket.objects.create(order=self.order, user=self.user)

        ticket2 = Ticket.objects.create(order=self.order, user=self.user)

        tickets = Ticket.objects.all()
        self.assertEqual(tickets[0], ticket2)  # Newest first
        self.assertEqual(tickets[1], ticket1)

    def test_ticket_status_choices(self):
        """Test ticket status choices."""
        valid_statuses = [choice[0] for choice in Ticket.STATUS_CHOICES]
        self.assertIn("valid", valid_statuses)
        self.assertIn("used", valid_statuses)

    def test_ticket_uniqueness(self):
        """Test that final_key must be unique."""
        ticket1 = Ticket.objects.create(order=self.order, user=self.user)

        # Create another order for the same user
        order2 = Order.objects.create(
            user=self.user, offer=self.offer, amount=Decimal("50.00"), status="paid"
        )

        # This should work as it will have a different key2
        ticket2 = Ticket.objects.create(order=order2, user=self.user)

        self.assertNotEqual(ticket1.final_key, ticket2.final_key)
