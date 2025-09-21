"""
Management command to create tickets for paid orders that don't have tickets yet.
"""

from django.core.management.base import BaseCommand
from apps.orders.models import Order
from apps.tickets.models import Ticket


class Command(BaseCommand):
    help = "Create tickets for all paid orders that don't have tickets yet"

    def handle(self, *args, **options):
        # Find all paid orders without tickets
        orders_without_tickets = Order.objects.filter(status="paid").exclude(
            ticket__isnull=False
        )

        created_count = 0

        for order in orders_without_tickets:
            # Create ticket
            ticket = Ticket.objects.create(
                order=order,
                user=order.user,
                final_key=f"{order.user.key1}_{order.id}_{order.created_at.timestamp()}",
            )
            # Generate QR code
            ticket.generate_qr_code()
            created_count += 1

            self.stdout.write(
                self.style.SUCCESS(f"Created ticket {ticket.id} for order {order.id}")
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created_count} tickets")
        )
