"""Exercise database-creation races without opening a database connection."""

import io
import os
import subprocess
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.db.backends.base.creation import BaseDatabaseCreation
from django.test import SimpleTestCase

from scripts import run_checks
from scripts.part3 import (
    run_issue38_focused,
    run_issue40_browser,
    run_issue40_load,
)


class VerificationDatabaseOwnershipTests(SimpleTestCase):
    def assert_creation_race_cannot_drop(self, command, kwargs):
        """Use Django's actual collision branch after an absent-DB preflight."""
        self.assertEqual(kwargs.get("stdin"), subprocess.DEVNULL)
        self.assertNotIn("--noinput", command)
        self.assertNotIn("--keepdb", command)
        creation = BaseDatabaseCreation(MagicMock())
        cursor = MagicMock()
        creation._get_test_db_name = lambda: "test_hms"
        creation.sql_table_creation_suffix = lambda: ""
        creation._nodb_cursor = MagicMock()
        creation._nodb_cursor.return_value.__enter__.return_value = cursor
        creation._execute_create_test_db = MagicMock(
            side_effect=RuntimeError("Synthetic database appeared after preflight")
        )
        with (
            patch("builtins.input", side_effect=EOFError),
            redirect_stderr(io.StringIO()),
            self.assertRaises(EOFError),
        ):
            creation._create_test_db(verbosity=0, autoclobber="--noinput" in command)
        creation._execute_create_test_db.assert_called_once()
        cursor.execute.assert_not_called()

    def test_full_checks_and_timing_smoke_never_request_automatic_replacement(self):
        steps = dict(run_checks.verification_steps(Path("evidence")))
        for name in ("test-results", "timing-smoke"):
            with self.subTest(step=name):
                self.assertNotIn("--noinput", steps[name])

    def test_full_check_child_has_closed_stdin_when_database_appears(self):
        with TemporaryDirectory() as temporary:
            output = Path(temporary)

            def start(command, **kwargs):
                self.assert_creation_race_cannot_drop(command, kwargs)
                process = MagicMock()
                process.__enter__.return_value = process
                process.stdout = []
                process.wait.return_value = 1
                return process

            with (
                patch.object(run_checks.subprocess, "Popen", side_effect=start),
                redirect_stdout(io.StringIO()),
            ):
                result = run_checks.run_step(
                    "test-results", ["manage.py", "test"], output, {}
                )
            self.assertEqual(result["exit_code"], 1)

    def test_browser_and_load_children_refuse_a_database_created_after_preflight(self):
        for runner in (run_issue40_browser, run_issue40_load):
            with (
                self.subTest(runner=runner.__name__),
                TemporaryDirectory() as temporary,
            ):
                root = Path(temporary)
                output = root / "evidence"
                jar = root / "ApacheJMeter.jar"
                java = root / "java.exe"
                jar.touch()
                java.touch()
                arguments = ["runner", "--output-dir", str(output)]
                if runner is run_issue40_load:
                    arguments += ["--jmeter", str(jar), "--java", str(java)]
                cursor = MagicMock()
                cursor.fetchone.return_value = None
                connection = MagicMock()
                connection.cursor.return_value.__enter__.return_value = cursor
                fake_modules = {
                    "django": SimpleNamespace(setup=lambda: None),
                    "django.conf": SimpleNamespace(
                        settings=SimpleNamespace(
                            DATABASES={
                                "default": {
                                    "ENGINE": "django.db.backends.mysql",
                                    "NAME": "hms",
                                }
                            }
                        )
                    ),
                    "django.db": SimpleNamespace(connection=connection),
                }
                children = []

                def execute(command, *, launched=children, **kwargs):
                    if command[0] in ("git", "node"):
                        return SimpleNamespace(returncode=0)
                    launched.append(command)
                    self.assert_creation_race_cannot_drop(command, kwargs)
                    return SimpleNamespace(returncode=1)

                with (
                    patch.object(runner, "ROOT", root),
                    patch.object(runner.subprocess, "run", side_effect=execute),
                    patch.object(sys, "argv", arguments),
                    patch.object(sys, "path", list(sys.path)),
                    patch.dict(os.environ),
                    patch(
                        "django.core.management.call_command",
                        side_effect=AssertionError("Use a child with closed stdin"),
                    ),
                    patch.dict(sys.modules, fake_modules),
                ):
                    self.assertEqual(runner.main(), 1)
                self.assertEqual(len(children), 1)
                self.assertIn("test", children[0])
                self.assertTrue(
                    any("scripts.part3.test_issue40_" in arg for arg in children[0])
                )
                connection.close.assert_called_once()

    def test_issue38_offers_only_implemented_batches(self):
        self.assertNotIn("browser", run_issue38_focused.LABELS)
        self.assertEqual(set(run_issue38_focused.LABELS), {"owner", "gaps", "audit"})
