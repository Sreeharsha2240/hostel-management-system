"""Run HMS behind the laptop's Cloudflare Tunnel, never on a public socket.

Usage: python -m deployment.windows --config C:\\private\\hms.json [--check]
The JSON file contains the six required Django/database environment variables
listed below and, optionally, HMS_PORT. Keep it outside the source checkout.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from pathlib import Path
from typing import Any

REQUIRED_ENVIRONMENT = frozenset(
    {"DJANGO_SECRET_KEY", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"}
)
ALLOWED_CONFIG_KEYS = REQUIRED_ENVIRONMENT | {"HMS_PORT"}
DEFAULT_PORT = 8110
MAX_CONFIG_BYTES = 64 * 1024


class ConfigurationError(ValueError):
    """An actionable error whose message never includes configuration values."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ConfigurationError("The JSON config contains duplicate keys.")
        result[key] = value
    return result


def _port(value: object, name: str, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ConfigurationError(f"{name} must be a whole-number port.")
    if isinstance(value, str) and (
        len(value) > 5 or not value.isascii() or not value.isdecimal()
    ):
        raise ConfigurationError(f"{name} must be a whole-number port.")
    number = int(value)
    if not minimum <= number <= 65535:
        raise ConfigurationError(f"{name} must be between {minimum} and 65535.")
    return number


def load_config(path: Path) -> tuple[dict[str, str], int]:
    """Read an explicit allowlist of settings without inheriting missing values."""
    try:
        if not path.is_file() or path.stat().st_size > MAX_CONFIG_BYTES:
            raise ConfigurationError("The config must be a JSON file under 64 KiB.")
        with path.open(encoding="utf-8-sig") as stream:
            config = json.load(stream, object_pairs_hook=_unique_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ConfigurationError("Cannot read the config as UTF-8 JSON.") from error

    if not isinstance(config, dict):
        raise ConfigurationError("The config must be a JSON object.")
    if config.keys() - ALLOWED_CONFIG_KEYS:
        raise ConfigurationError(
            "The config has unsupported keys; use only DJANGO_SECRET_KEY, "
            "DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, and optional HMS_PORT."
        )
    missing = REQUIRED_ENVIRONMENT - config.keys()
    if missing:
        raise ConfigurationError(
            "Missing required config keys: " + ", ".join(sorted(missing))
        )

    environment = {}
    for name in sorted(REQUIRED_ENVIRONMENT):
        value = config[name]
        if not isinstance(value, str) or not value.strip() or "\0" in value:
            raise ConfigurationError(
                f"{name} must be a non-empty string without NUL characters."
            )
        environment[name] = value
    secret = environment["DJANGO_SECRET_KEY"]
    if (
        len(secret) < 50
        or len(set(secret)) < 5
        or secret.startswith("django-insecure-")
    ):
        raise ConfigurationError(
            "DJANGO_SECRET_KEY must be a newly generated production secret."
        )
    _port(environment["DB_PORT"], "DB_PORT", 1)
    return environment, _port(config.get("HMS_PORT", DEFAULT_PORT), "HMS_PORT", 1024)


def configure_environment(environment: dict[str, str]) -> None:
    """Apply only validated values before Django or python-dotenv is imported."""
    if environment.keys() != REQUIRED_ENVIRONMENT:
        raise ConfigurationError(
            "The production environment must contain exactly the required keys."
        )
    os.environ.update(environment)
    os.environ["PYTHON_DOTENV_DISABLED"] = "1"
    os.environ["DJANGO_SETTINGS_MODULE"] = "deployment.settings"


def server_options(port: int) -> dict[str, Any]:
    """Trust only the local tunnel's scheme; keep Host and client headers untrusted."""
    return {
        "host": "127.0.0.1",
        "port": _port(port, "HMS_PORT", 1024),
        "threads": 8,
        "connection_limit": 100,
        "max_request_body_size": 10 * 1024 * 1024,
        "trusted_proxy": "127.0.0.1",
        "trusted_proxy_count": 1,
        "trusted_proxy_headers": {"x-forwarded-proto"},
        "clear_untrusted_proxy_headers": True,
        "log_untrusted_proxy_headers": False,
        "expose_tracebacks": False,
        "ident": "",
    }


def load_application() -> Any:
    return importlib.import_module("hms.wsgi").application


def load_waitress() -> tuple[Any, Any]:
    from waitress import serve
    from waitress.adjustments import Adjustments

    return serve, Adjustments


def check_django() -> None:
    from django.core import checks

    # Leaving databases unset avoids database connection checks. No management
    # command, migration, user creation, or database write belongs in this process.
    problems = [
        issue
        for issue in checks.run_checks(include_deployment_checks=True)
        if issue.level >= checks.WARNING and not issue.is_silenced()
    ]
    if problems:
        identifiers = ", ".join(
            sorted({issue.id or "unidentified check" for issue in problems})
        )
        raise ConfigurationError(
            "Django production checks require attention: " + identifiers
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", required=True, type=Path, help="Private production JSON file"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate startup without opening a listener",
    )
    args = parser.parse_args(argv)
    try:
        environment, port = load_config(args.config)
        configure_environment(environment)
        serve, adjustments = load_waitress()
        options = server_options(port)
        adjustments(**options)  # Validate Waitress arguments without creating a socket.
        application = load_application()
        check_django()
        if args.check:
            print(
                "Production configuration and Django checks passed; no listener was opened."
            )
            return 0
        print(f"Starting HMS on http://127.0.0.1:{port}.", flush=True)
        serve(application, **options)
    except ConfigurationError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 0
    except Exception as error:
        # Database/driver exceptions can include credentials or connection strings.
        # Do not print their messages, exception chains, config, or request headers.
        print(
            f"Production startup failed ({type(error).__name__}). "
            "Verify deployment dependencies, the private config, and collected static files.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
