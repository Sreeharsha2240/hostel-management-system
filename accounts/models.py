from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User account for Admin, Warden and Student logins (C2).

    Declared at project start because Django cannot switch AUTH_USER_MODEL
    after the first migration. The role and lockout fields from SAD 4.1 are
    added under HMS-04.
    """
