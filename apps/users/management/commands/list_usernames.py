"""
Management command to list all users and their usernames.
"""

from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    help = "List all users and their generated usernames"

    def handle(self, *args, **options):
        users = User.objects.all().order_by("email")

        self.stdout.write(self.style.SUCCESS(f"Found {users.count()} users:"))
        self.stdout.write("")

        for user in users:
            self.stdout.write(
                f"  {user.email:<30} | {user.first_name} {user.last_name:<20} | {user.username}"
            )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Done!"))
