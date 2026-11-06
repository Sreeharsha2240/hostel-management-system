"""Create or reset local Admin, Warden, and Student demo logins."""

from getpass import getpass

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounts.models import User


class Command(BaseCommand):
    help = "Create or reset the three local demo accounts, prompting for passwords."

    accounts = (
        ("hms_demo_admin", "admin@example.test", User.Role.ADMIN, True, True),
        ("hms_demo_warden", "warden@example.test", User.Role.WARDEN, False, False),
        ("hms_demo_student", "student@example.test", User.Role.STUDENT, False, False),
    )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError(
                "Demo accounts may only be created when DJANGO_DEBUG=True."
            )

        prepared = []
        for username, email, role, is_staff, is_superuser in self.accounts:
            user = User(username=username, email=email, role=role)
            while True:
                password = getpass(f"Password for {username}: ")
                confirmation = getpass("Confirm password: ")
                if not password or password != confirmation:
                    self.stderr.write(
                        "Passwords must be non-empty and match. Try again."
                    )
                    continue
                try:
                    validate_password(password, user=user)
                except ValidationError as exc:
                    for message in exc.messages:
                        self.stderr.write(message)
                    continue
                prepared.append(
                    (username, email, role, is_staff, is_superuser, password)
                )
                break

        with transaction.atomic():
            for username, email, role, is_staff, is_superuser, password in prepared:
                user, created = User.objects.get_or_create(username=username)
                user.email = email
                user.role = role
                user.is_active = True
                user.is_staff = is_staff
                user.is_superuser = is_superuser
                user.set_password(password)
                user.save()
                action = "Created" if created else "Reset"
                self.stdout.write(f"{action} {role} login: {username}")

        self.stdout.write(
            self.style.SUCCESS("Demo logins are ready for this local database.")
        )
