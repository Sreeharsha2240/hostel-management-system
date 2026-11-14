from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """User account for Admin, Warden and Student logins (C2).

    Declared at project start because Django cannot switch AUTH_USER_MODEL
    after the first migration.
    """

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        WARDEN = "warden", "Warden"
        STUDENT = "student", "Student"

    role = models.CharField(max_length=16, choices=Role.choices, default=Role.STUDENT)
    failed_attempts = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(blank=True, null=True)
    objects = UserManager()

    def is_locked(self):
        return bool(self.locked_until and self.locked_until > timezone.now())

    def save(self, *args, **kwargs):
        if self.is_superuser and self.role != self.Role.ADMIN:
            self.role = self.Role.ADMIN
            if kwargs.get("update_fields") is not None:
                kwargs["update_fields"] = set(kwargs["update_fields"]) | {"role"}
        if self.role == self.Role.STUDENT and self.is_staff:
            # Django's admin site uses is_staff as its entry gate. Keep it in
            # sync with HMS roles so demoting an account immediately removes
            # its Django admin access, including when save(update_fields=...)
            # is used by account-management code.
            self.is_staff = False
            if kwargs.get("update_fields") is not None:
                kwargs["update_fields"] = set(kwargs["update_fields"]) | {"is_staff"}
        super().save(*args, **kwargs)
