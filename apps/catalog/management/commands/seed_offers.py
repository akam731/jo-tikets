"""
Management command to seed the database with sample offers.
"""

from django.core.management.base import BaseCommand
from decimal import Decimal
from apps.catalog.models import Offer


class Command(BaseCommand):
    help = "Seed the database with sample offers for the Olympic Games"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear", action="store_true", help="Clear existing offers before seeding"
        )

    def handle(self, *args, **options):
        if options["clear"]:
            Offer.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing offers cleared"))

        # Define sample offers
        offers_data = [
            {
                "name": "solo",
                "capacity": 1,
                "price": Decimal("50.00"),
                "description": "Billet individuel pour une personne. Accès à tous les événements des Jeux Olympiques.",
                "is_active": True,
            },
            {
                "name": "duo",
                "capacity": 2,
                "price": Decimal("90.00"),
                "description": "Pack duo pour deux personnes. Idéal pour un couple ou des amis.",
                "is_active": True,
            },
            {
                "name": "familiale",
                "capacity": 4,
                "price": Decimal("160.00"),
                "description": "Pack familial pour quatre personnes. Parfait pour toute la famille.",
                "is_active": True,
            },
        ]

        created_count = 0
        updated_count = 0

        for offer_data in offers_data:
            offer, created = Offer.objects.get_or_create(
                name=offer_data["name"], defaults=offer_data
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created offer: {offer.get_name_display()} - {offer.price}€"
                    )
                )
            else:
                # Update existing offer
                for key, value in offer_data.items():
                    setattr(offer, key, value)
                offer.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Updated offer: {offer.get_name_display()} - {offer.price}€"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n=== Seeding Complete ===\n"
                f"Created: {created_count} offers\n"
                f"Updated: {updated_count} offers\n"
                f"Total: {Offer.objects.count()} offers in database"
            )
        )
