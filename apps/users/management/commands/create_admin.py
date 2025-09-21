"""
Management command to create admin users for the JO Tickets application.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = "Create admin users for the JO Tickets application"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            type=str,
            default="admin@jo-tickets.com",
            help="Email for the admin user",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="admin123",
            help="Password for the admin user",
        )
        parser.add_argument(
            "--employee", action="store_true", help="Create an employee user as well"
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create admin panel user
            admin_email = options["email"]
            admin_password = options["password"]

            admin_user, created = User.objects.get_or_create(
                email=admin_email,
                defaults={
                    "username": "admin",
                    "first_name": "Admin",
                    "last_name": "JO Tickets",
                    "is_staff": True,
                    "is_superuser": True,
                    "is_adminpanel": True,
                    "is_employee": True,
                },
            )

            if created:
                admin_user.set_password(admin_password)
                admin_user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Admin user created successfully: {admin_email}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Admin user already exists: {admin_email}")
                )

            # Create employee user if requested
            if options["employee"]:
                employee_email = "employee@jo-tickets.com"
                employee_password = "employee123"

                employee_user, created = User.objects.get_or_create(
                    email=employee_email,
                    defaults={
                        "username": "employee",
                        "first_name": "Employee",
                        "last_name": "JO Tickets",
                        "is_employee": True,
                    },
                )

                if created:
                    employee_user.set_password(employee_password)
                    employee_user.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Employee user created successfully: {employee_email}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Employee user already exists: {employee_email}"
                        )
                    )

            # Create demo customer
            demo_email = "demo@jo-tickets.com"
            demo_password = "demo123"

            demo_user, created = User.objects.get_or_create(
                email=demo_email,
                defaults={
                    "username": "demo",
                    "first_name": "Demo",
                    "last_name": "Customer",
                },
            )

            if created:
                demo_user.set_password(demo_password)
                demo_user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Demo customer created successfully: {demo_email}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Demo customer already exists: {demo_email}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                "\n=== Account Information ===\n"
                f"Admin Panel: {admin_email} / {admin_password}\n"
                f"Employee: employee@jo-tickets.com / employee123\n"
                f"Demo Customer: {demo_email} / {demo_password}\n"
                "========================"
            )
        )
