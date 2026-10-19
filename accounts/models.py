from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models


class User(AbstractUser):
    """User account for Admin, Warden and Student logins (C2).

    Declared at project start because Django cannot switch AUTH_USER_MODEL
    after the first migration.
    """

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        WARDEN = 'warden', 'Warden'
        STUDENT = 'student', 'Student'

    role = models.CharField(max_length=16, choices=Role.choices, default=Role.STUDENT)
    failed_attempts = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(blank=True, null=True)
    objects = UserManager()

    def is_locked(self):
        from django.utils import timezone

        return bool(self.locked_until and self.locked_until > timezone.now())

    def save(self, *args, **kwargs):
        if self.is_superuser and self.role != self.Role.ADMIN:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)
