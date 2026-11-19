"""Production settings for https://se.d3va.dev.

Select with DJANGO_SETTINGS_MODULE=deployment.settings. Only explicit process
environment values supply credentials; the development .env is never loaded.
The Windows launcher supplies these values from its private configuration file.
"""

import os

from django.core.exceptions import ImproperlyConfigured

# This must happen before importing the development settings. python-dotenv
# otherwise searches the project .env, which may contain development secrets.
os.environ["PYTHON_DOTENV_DISABLED"] = "1"

for _name in (
    "DJANGO_SECRET_KEY",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_PORT",
):
    if not os.environ.get(_name, "").strip():
        raise ImproperlyConfigured(f"Production requires an explicit {_name}.")

_secret = os.environ["DJANGO_SECRET_KEY"]
if len(_secret) < 50 or len(set(_secret)) < 5 or _secret.startswith("django-insecure-"):
    raise ImproperlyConfigured("Production requires a strong DJANGO_SECRET_KEY.")
del _secret, _name

from hms.settings import *  # noqa: E402,F403

# These are enforced values: stale DJANGO_DEBUG / DJANGO_*_SECURE values from
# a development shell must never weaken this production settings module.
DEBUG = False
ALLOWED_HOSTS = ["se.d3va.dev"]
CSRF_TRUSTED_ORIGINS = []
USE_X_FORWARDED_HOST = False
USE_X_FORWARDED_PORT = False

# Never trust client-supplied forwarding headers in Django. The Windows
# launcher binds Waitress to 127.0.0.1 and explicitly trusts only that peer's
# X-Forwarded-Proto after cloudflared has normalized it. Waitress then sets
# wsgi.url_scheme; its untrusted forwarded headers are removed. If another
# server is used, configure that same isolated proxy boundary at the server,
# never enable Django's SECURE_PROXY_SSL_HEADER on a publicly reachable origin.
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = True
SECURE_REDIRECT_EXEMPT = []
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_DOMAIN = None

# SecurityMiddleware must wrap WhiteNoise so static responses also receive
# HTTPS redirects, HSTS and nosniff. Serve only collectstatic output in public.
MIDDLEWARE = list(MIDDLEWARE)  # noqa: F405
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATIC_URL = "/static/"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}
WHITENOISE_AUTOREFRESH = False
WHITENOISE_USE_FINDERS = False
WHITENOISE_MANIFEST_STRICT = True
WHITENOISE_ALLOW_ALL_ORIGINS = False
