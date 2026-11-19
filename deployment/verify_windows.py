"""Safety checks for the private-config production launcher; no sockets or DBs."""

import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from deployment import windows


class WindowsRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.config_path = Path(self.directory.name) / "private.json"
        self.config = {
            "DJANGO_SECRET_KEY": "test-only-secret-for-launcher-validation-0123456789abcdef",
            "DB_NAME": "test_hms",
            "DB_USER": "test_hms",
            "DB_PASSWORD": "test-only-password",
            "DB_HOST": "127.0.0.1",
            "DB_PORT": "3306",
        }
        self.write_config()

    def write_config(self):
        self.config_path.write_text(json.dumps(self.config), encoding="utf-8-sig")

    def test_explicit_config_cannot_inherit_credentials_or_inject_environment(self):
        del self.config["DB_PASSWORD"]
        self.write_config()
        with patch.dict(os.environ, {"DB_PASSWORD": "inherited-credential"}):
            with self.assertRaisesRegex(windows.ConfigurationError, "DB_PASSWORD"):
                windows.load_config(self.config_path)
        self.config["DB_PASSWORD"] = "test-only-password"
        self.config["DJANGO_SETTINGS_MODULE"] = "hms.settings"
        self.write_config()
        with self.assertRaisesRegex(windows.ConfigurationError, "unsupported keys"):
            windows.load_config(self.config_path)

    def test_duplicate_keys_and_bad_json_are_rejected_without_values(self):
        for content in (
            '{"DB_PASSWORD":"private-value","DB_PASSWORD":"again"}',
            '{"private-value":',
        ):
            with self.subTest(content=content):
                self.config_path.write_text(content, encoding="utf-8")
                with self.assertRaises(windows.ConfigurationError) as raised:
                    windows.load_config(self.config_path)
                self.assertNotIn("private-value", str(raised.exception))

    def test_port_validation_rejects_privileged_invalid_and_boolean_ports(self):
        for port in (True, False, 0, 80, 1023, 65536, "8110.0", " 8110", [], None):
            with self.subTest(port=port):
                self.config["HMS_PORT"] = port
                self.write_config()
                with self.assertRaises(windows.ConfigurationError):
                    windows.load_config(self.config_path)
        self.config["HMS_PORT"] = "8111"
        self.write_config()
        _, port = windows.load_config(self.config_path)
        self.assertEqual(port, 8111)

    def test_weak_secret_is_rejected(self):
        for secret in ("short", "x" * 64, "django-insecure-" + "abcdefghij" * 8):
            with self.subTest(secret=secret):
                self.config["DJANGO_SECRET_KEY"] = secret
                self.write_config()
                with self.assertRaisesRegex(
                    windows.ConfigurationError, "newly generated"
                ):
                    windows.load_config(self.config_path)

    def test_waitress_serves_loopback_and_only_trusts_local_scheme(self):
        application, serve, adjustments = Mock(), Mock(), Mock()
        with (
            patch.dict(
                os.environ,
                {
                    "DJANGO_SETTINGS_MODULE": "hms.settings",
                    "PYTHON_DOTENV_DISABLED": "0",
                },
            ),
            patch.object(windows, "load_waitress", return_value=(serve, adjustments)),
            patch.object(windows, "load_application", return_value=application),
            patch.object(windows, "check_django"),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(windows.main(["--config", str(self.config_path)]), 0)
            self.assertEqual(
                os.environ["DJANGO_SETTINGS_MODULE"], "deployment.settings"
            )
            self.assertEqual(os.environ["PYTHON_DOTENV_DISABLED"], "1")
            self.assertEqual(os.environ["DB_PASSWORD"], self.config["DB_PASSWORD"])
        options = serve.call_args.kwargs
        serve.assert_called_once_with(application, **options)
        self.assertEqual(options["host"], "127.0.0.1")
        self.assertEqual(options["port"], 8110)
        self.assertEqual(options["trusted_proxy"], "127.0.0.1")
        self.assertEqual(options["trusted_proxy_count"], 1)
        self.assertEqual(options["trusted_proxy_headers"], {"x-forwarded-proto"})
        self.assertTrue(options["clear_untrusted_proxy_headers"])
        self.assertFalse(options["log_untrusted_proxy_headers"])
        self.assertFalse(options["expose_tracebacks"])
        self.assertEqual(options["max_request_body_size"], 10 * 1024 * 1024)
        self.assertEqual(options["ident"], "")
        adjustments.assert_called_once_with(**options)

    def test_check_initializes_application_but_never_serves(self):
        serve, adjustments = Mock(), Mock()
        with (
            patch.dict(os.environ, {}, clear=False),
            patch.object(windows, "load_waitress", return_value=(serve, adjustments)),
            patch.object(windows, "load_application") as load_application,
            patch.object(windows, "check_django") as check_django,
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            self.assertEqual(
                windows.main(["--config", str(self.config_path), "--check"]), 0
            )
        serve.assert_not_called()
        load_application.assert_called_once_with()
        check_django.assert_called_once_with()
        self.assertIn("no listener was opened", output.getvalue())

    def test_bad_config_never_initializes_application_or_server(self):
        self.config["HMS_PORT"] = 80
        self.write_config()
        with (
            patch.object(windows, "load_waitress") as load_waitress,
            patch.object(windows, "load_application") as load_application,
            contextlib.redirect_stderr(io.StringIO()) as errors,
        ):
            self.assertEqual(windows.main(["--config", str(self.config_path)]), 1)
        load_waitress.assert_not_called()
        load_application.assert_not_called()
        self.assertIn("HMS_PORT must be between", errors.getvalue())

    def test_startup_exception_does_not_disclose_secret_or_traceback(self):
        with (
            patch.dict(os.environ, {}, clear=False),
            patch.object(windows, "load_waitress", return_value=(Mock(), Mock())),
            patch.object(
                windows,
                "load_application",
                side_effect=RuntimeError(self.config["DB_PASSWORD"]),
            ),
            contextlib.redirect_stderr(io.StringIO()) as errors,
        ):
            self.assertEqual(windows.main(["--config", str(self.config_path)]), 1)
        self.assertIn("RuntimeError", errors.getvalue())
        self.assertNotIn(self.config["DB_PASSWORD"], errors.getvalue())
        self.assertNotIn("Traceback", errors.getvalue())

    def test_django_checks_use_no_database_aliases_and_fail_on_warning_ids(self):
        from django.core import checks

        warning = checks.Warning("private-value", id="security.W999")
        with (
            patch.object(checks, "run_checks", return_value=[warning]) as run_checks,
            patch.object(warning, "is_silenced", return_value=False),
            self.assertRaises(windows.ConfigurationError) as raised,
        ):
            windows.check_django()
        run_checks.assert_called_once_with(include_deployment_checks=True)
        self.assertIn("security.W999", str(raised.exception))
        self.assertNotIn("private-value", str(raised.exception))

    def test_real_waitress_accepts_hardened_options_without_opening_socket(self):
        _, adjustments = windows.load_waitress()
        configured = adjustments(**windows.server_options(8110))
        self.assertEqual(configured.host, "127.0.0.1")
        self.assertEqual(configured.trusted_proxy_headers, {"x-forwarded-proto"})


if __name__ == "__main__":
    unittest.main()
