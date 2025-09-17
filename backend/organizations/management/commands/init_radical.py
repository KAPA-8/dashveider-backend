"""
Management command to initialize Radical organization with superuser
This command should be run after deployment to set up the initial super-admin organization
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from organizations.models import Organization, UserProfile
import getpass


User = get_user_model()


class Command(BaseCommand):
    help = "Initialize Radical organization with superuser account"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            type=str,
            help="Email for the superuser account",
        )
        parser.add_argument(
            "--password",
            type=str,
            help="Password for the superuser account",
        )
        parser.add_argument(
            "--interactive",
            action="store_true",
            help="Prompt for email and password interactively",
        )

    def handle(self, *args, **options):
        # Check if Radical organization already exists
        if Organization.objects.filter(name="Radical").exists():
            radical_org = Organization.objects.get(name="Radical")
            self.stdout.write(self.style.WARNING("Radical organization already exists"))

            # Check if there's already a superuser linked to Radical
            radical_profiles = UserProfile.objects.filter(organization=radical_org)
            if radical_profiles.exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"Radical organization already has {radical_profiles.count()} user(s)"
                    )
                )
                return
        else:
            # Create Radical organization
            radical_org = Organization.get_radical_org()
            self.stdout.write(self.style.SUCCESS("Created Radical organization"))

        # Get email and password
        if options["interactive"] or not (options["email"] and options["password"]):
            email = input("Email: ") if not options["email"] else options["email"]
            password = (
                getpass.getpass("Password: ")
                if not options["password"]
                else options["password"]
            )
        else:
            email = options["email"]
            password = options["password"]

        if not email or not password:
            raise CommandError("Email and password are required")

        # Create or get superuser
        try:
            user = User.objects.get(email=email)
            self.stdout.write(self.style.WARNING(f"User {email} already exists"))
        except User.DoesNotExist:
            user = User.objects.create_superuser(
                email=email, password=password, first_name="Radical", last_name="Admin"
            )
            self.stdout.write(self.style.SUCCESS(f"Created superuser: {email}"))

        # Link user to Radical organization
        profile, created = UserProfile.objects.get_or_create(
            user=user, organization=radical_org
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Linked {email} to Radical organization")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"{email} already linked to Radical organization")
            )

        self.stdout.write(
            self.style.SUCCESS("Radical organization initialization complete!")
        )
