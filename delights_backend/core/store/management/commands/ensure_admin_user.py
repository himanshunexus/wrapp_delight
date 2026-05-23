import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


ADMIN_USERNAME = os.getenv("ADMIN_BOOTSTRAP_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_BOOTSTRAP_PASSWORD", "")
ADMIN_EMAIL = os.getenv("ADMIN_BOOTSTRAP_EMAIL", "admin@example.com")


class Command(BaseCommand):
    help = "Bootstrap admin superuser from environment credentials."

    def handle(self, *args, **options):
        if not ADMIN_PASSWORD:
            raise RuntimeError(
                "ADMIN_BOOTSTRAP_PASSWORD must be set before bootstrapping the admin user."
            )

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=ADMIN_USERNAME,
            defaults={
                "email": ADMIN_EMAIL,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        # Enforce credentials on every run.
        user.email = ADMIN_EMAIL
        user.is_staff = True
        user.is_superuser = True
        user.set_password(ADMIN_PASSWORD)
        user.save()

        action = "created" if created else "updated"
        self.stdout.write(
            self.style.SUCCESS(f"Admin superuser '{ADMIN_USERNAME}' {action}.")
        )
