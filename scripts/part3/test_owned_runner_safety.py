"""Offline guards and truthful JUnit reconciliation; no database is contacted."""

import importlib.util
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

spec = importlib.util.spec_from_file_location(
    "owned_runner", Path(__file__).with_name("run_owned_regressions.py")
)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class OwnedRunnerSafetyTests(unittest.TestCase):
    def test_custom_live_or_mirrored_database_is_refused_without_a_query(self):
        for database in (
            {"ENGINE": "django.db.backends.sqlite3", "NAME": "hms"},
            {"ENGINE": "django.db.backends.mysql", "NAME": "live"},
            {
                "ENGINE": "django.db.backends.mysql",
                "NAME": "hms",
                "TEST": {"NAME": "hms"},
            },
            {
                "ENGINE": "django.db.backends.mysql",
                "NAME": "hms",
                "TEST": {"MIRROR": "default"},
            },
        ):
            with self.subTest(database=database):
                connection = MagicMock()
                with self.assertRaises(ValueError):
                    runner.check_database(database, connection)
                connection.cursor.assert_not_called()

    def test_existing_test_database_is_refused_and_connection_closed(self):
        connection = MagicMock()
        cursor = connection.cursor.return_value.__enter__.return_value
        cursor.fetchone.side_effect = [("8.4.13",), ("test_hms",)]
        with self.assertRaisesRegex(ValueError, "refusing to replace"):
            runner.check_database(
                {"ENGINE": "django.db.backends.mysql", "NAME": "hms"}, connection
            )
        self.assertEqual(cursor.execute.call_count, 2)
        self.assertTrue(
            all(
                call.args[0].startswith("SELECT ")
                for call in cursor.execute.call_args_list
            )
        )
        connection.close.assert_called_once()

    def test_absent_test_database_preflight_only_reads_metadata(self):
        connection = MagicMock()
        cursor = connection.cursor.return_value.__enter__.return_value
        cursor.fetchone.side_effect = [("8.4.13",), None]
        self.assertEqual(
            runner.check_database(
                {"ENGINE": "django.db.backends.mysql", "NAME": "hms"}, connection
            ),
            "8.4.13",
        )
        connection.close.assert_called_once()

    def test_failed_subtest_is_fail_even_without_a_case_record(self):
        with TemporaryDirectory() as temporary:
            folder = Path(temporary)
            (folder / "junit").mkdir()
            method = runner.CASE_METHODS["TC-REG-S2-09"]
            classname, name = method.rsplit(".", 1)
            (folder / "junit/TEST-case.xml").write_text(
                f'<testsuite><testcase classname="{classname}" name="{name} (mutation=delete)"><failure/></testcase></testsuite>',
                encoding="utf-8",
            )
            methods, cases, raw = runner.collect_results(folder)
            self.assertEqual(methods, {method: "FAIL"})
            self.assertEqual(cases["TC-REG-S2-09"]["status"], "FAIL")
            self.assertEqual(len(raw), 1)

    def test_setup_error_and_skip_are_not_relabelled_not_run(self):
        for tag, expected in (("error", "ERROR"), ("skipped", "SKIP")):
            with self.subTest(tag=tag), TemporaryDirectory() as temporary:
                folder = Path(temporary)
                (folder / "junit").mkdir()
                method = runner.CASE_METHODS["TC-REG-S2-08"]
                classname, name = method.rsplit(".", 1)
                (folder / "junit/TEST-case.xml").write_text(
                    f'<testsuite><testcase classname="{classname}" name="{name}"><{tag}/></testcase></testsuite>',
                    encoding="utf-8",
                )
                _, cases, _ = runner.collect_results(folder)
                self.assertEqual(cases["TC-REG-S2-08"]["status"], expected)
                self.assertTrue(cases["TC-REG-S2-08"]["record_missing"])

    def test_passing_method_without_completed_steps_is_not_a_case_pass(self):
        with TemporaryDirectory() as temporary:
            folder = Path(temporary)
            (folder / "junit").mkdir()
            method = runner.CASE_METHODS["TC-REG-S2-08"]
            classname, name = method.rsplit(".", 1)
            (folder / "junit/TEST-case.xml").write_text(
                f'<testsuite><testcase classname="{classname}" name="{name}"/></testsuite>',
                encoding="utf-8",
            )
            self.assertEqual(
                runner.collect_results(folder)[1]["TC-REG-S2-08"]["status"], "ERROR"
            )
            (folder / "TC-REG-S2-08.json").write_text(
                json.dumps(
                    {
                        "case_id": "TC-REG-S2-08",
                        "test_id": method,
                        "execution_status": "IN_PROGRESS",
                        "steps": [],
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(
                runner.collect_results(folder)[1]["TC-REG-S2-08"]["status"], "ERROR"
            )

    def test_refused_database_keeps_failure_evidence_and_never_starts_child(self):
        class FakeDjango:
            @staticmethod
            def setup():
                return None

        settings = MagicMock()
        settings.DATABASES = {
            "default": {"ENGINE": "django.db.backends.mysql", "NAME": "hms"}
        }
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            modules = {
                "django": FakeDjango(),
                "django.conf": MagicMock(settings=settings),
                "django.db": MagicMock(),
            }
            with (
                patch.object(runner, "ROOT", root),
                patch.object(
                    runner,
                    "git_output",
                    side_effect=lambda *args: (
                        "" if args[0] in {"status", "ls-files"} else "revision"
                    ),
                ),
                patch.object(runner, "version", return_value="test-version"),
                patch.object(
                    runner, "check_database", side_effect=ValueError("refuse")
                ),
                patch.object(
                    runner.subprocess, "run", return_value=MagicMock(returncode=0)
                ) as child,
                patch.dict("sys.modules", modules),
            ):
                output = root / "evidence"
                self.assertEqual(runner.main(["--output-dir", str(output)]), 1)
                result = json.loads((output / "run.json").read_text())
                self.assertFalse(result["success"])
                self.assertEqual(result["failure_stage"], "database-preflight")
                self.assertEqual(result["failure_type"], "ValueError")
                self.assertEqual(result["case_counts"], {"NOT RUN": 9})
                self.assertEqual(child.call_count, 1)  # Git ignore check only.


if __name__ == "__main__":
    unittest.main()
