"""Run one HMS-16 evidence batch serially against disposable MySQL test_hms."""

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[2]
LABELS = {
    "owner": [
        "accounts.tests",
        "accounts.test_security",
        "audit.tests",
        "students.test_self_service",
        "students.tests.StudentManagementViewTests.test_student_list_escapes_script_payload_and_search_treats_sql_as_literal",
    ],
    "gaps": ["accounts.test_issue38_gaps"],
    "audit": [
        "audit.tests.AuditTests.test_events_cannot_be_changed_or_deleted_through_supported_orm_operations",
        "audit.tests.AuditTests.test_retention_command_preserves_a_full_year_and_supports_dry_run",
        "audit.tests.AuditTests.test_audit_failure_rolls_back_account_creation",
        "audit.tests.AuditTests.test_authentication_events_include_actor_record_and_time_without_secrets",
        "audit.tests.AuditTests.test_create_update_and_deactivate_accounts_record_the_admin_actor",
        "audit.tests.AuditTests.test_only_admin_can_read_audit_log_including_direct_json_requests",
        "accounts.test_issue38_gaps.Issue38GapTests.test_sec07_original_six_actions_have_records_times_and_expected_actors",
    ],
    "browser": ["scripts.part3.test_issue38_browser"],
}


def git(*args):
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def database_preflight(database, connection):
    if (
        database["ENGINE"] != "django.db.backends.mysql"
        or database["NAME"] != "hms"
        or database.get("TEST", {}).get("NAME") not in (None, "test_hms")
        or database.get("TEST", {}).get("MIRROR")
    ):
        raise ValueError("Require separate nonmirrored MySQL hms/test_hms")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            server = cursor.fetchone()[0]
            cursor.execute(
                "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",
                ["test_hms"],
            )
            if cursor.fetchone() is not None:
                raise ValueError("Existing test_hms: refusing replacement")
    finally:
        connection.close()
    return server


def junit_rows(output):
    rows = {}
    for path in sorted((output / "junit").glob("TEST-*.xml")):
        for case in ElementTree.parse(path).getroot().iter("testcase"):
            identity = case.attrib["classname"] + "." + case.attrib["name"]
            if identity in rows:
                raise ValueError("Duplicate JUnit identity")
            rows[identity] = (
                "FAIL"
                if case.find("failure") is not None
                else "ERROR"
                if case.find("error") is not None
                else "SKIP"
                if case.find("skipped") is not None
                else "PASS"
            )
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", required=True, choices=LABELS)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT) or output.exists():
        parser.error("Choose a new Git-ignored directory inside this checkout")
    ignored = subprocess.run(
        ["git", "check-ignore", "--quiet", str(output / "private-evidence-check")],
        cwd=ROOT,
        capture_output=True,
    )
    if ignored.returncode:
        parser.error("Output must be Git-ignored, e.g. test-results/issue38-NEW")
    output.mkdir(parents=True, exist_ok=False)
    manifest = {
        "issue": 38,
        "started_at": datetime.now(UTC).isoformat(),
        "mode": args.mode,
        "scope": "Synthetic MySQL component/integration/browser evidence; not unit-only or whole-plan approval",
        "success": False,
        "python": platform.python_version(),
        "platform": platform.platform(),
    }
    stage = "source-and-dependencies"
    try:
        manifest.update(
            {
                "commit": git("rev-parse", "HEAD"),
                "tree": git("rev-parse", "HEAD^{tree}"),
                "git_dirty": bool(git("status", "--porcelain")),
                "versions": {
                    name: version(name)
                    for name in (
                        "Django",
                        "mysqlclient",
                        "unittest-xml-reporting",
                        "python-dotenv",
                    )
                },
            }
        )
        inputs = set(git("ls-files").splitlines()) | set(
            git("ls-files", "--others", "--exclude-standard").splitlines()
        )
        manifest["source_sha256"] = {
            name: digest(ROOT / name)
            for name in sorted(inputs)
            if name.endswith((".py", ".cjs", ".html", ".docx"))
            or name
            in (
                "requirements.txt",
                "requirements-dev.txt",
                "docs/part3/Test_Case_Document.md",
                "docs/part3/System_Validation_Report.md",
            )
        }
        sys.path.insert(0, str(ROOT))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hms.settings")
        import django

        django.setup()
        from django.conf import settings
        from django.db import connection

        stage = "database-preflight"
        manifest["mysql"] = database_preflight(
            settings.DATABASES["default"], connection
        )
        environment = os.environ.copy()
        environment.pop("COVERAGE_RUN", None)
        environment.update(
            {
                "PYTHONIOENCODING": "utf-8",
                "HMS_TEST_OUTPUT_DIR": str(output / "junit"),
                "HMS_ISSUE38_OUTPUT_DIR": str(output),
                "DJANGO_DEBUG": "True",
                "DJANGO_SECURE_SSL_REDIRECT": "False",
                "DJANGO_SESSION_COOKIE_SECURE": "False",
                "DJANGO_CSRF_COOKIE_SECURE": "False",
                "DJANGO_SECURE_HSTS_SECONDS": "0",
            }
        )
        manifest["test_profile"] = {
            "settings_module": environment["DJANGO_SETTINGS_MODULE"],
            "SECURE_SSL_REDIRECT": False,
            "SESSION_COOKIE_SECURE": False,
            "CSRF_COOKIE_SECURE": False,
            "transport": "HTTP on disposable MySQL test_hms; separate TLS evidence required",
        }
        command = [
            sys.executable,
            "manage.py",
            "test",
            *LABELS[args.mode],
            "--verbosity=2",
            "--testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner",
        ]
        manifest["command"] = ["python", *command[1:]]
        stage = "test-execution"
        # No --noinput and no --keepdb: if an existing schema appears after
        # preflight, interactive creation with closed stdin cannot approve DROP.
        with (output / "private-run.log").open("w", encoding="utf-8") as log:
            completed = subprocess.run(
                command,
                cwd=ROOT,
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=False,
            )
        manifest["exit_code"] = completed.returncode
        stage = "result-reconciliation"
        manifest["junit"] = junit_rows(output)
        manifest["method_counts"] = dict(Counter(manifest["junit"].values()))
        manifest["changed_inputs_during_execution"] = [
            name
            for name, value in manifest["source_sha256"].items()
            if not (ROOT / name).is_file() or digest(ROOT / name) != value
        ]
        manifest["success"] = (
            completed.returncode == 0
            and bool(manifest["junit"])
            and all(value == "PASS" for value in manifest["junit"].values())
            and not manifest["changed_inputs_during_execution"]
        )
    except Exception as error:
        # Avoid exception messages containing credentials/configuration data.
        manifest.update({"failure_stage": stage, "failure_type": type(error).__name__})
    finally:
        manifest["completed_at"] = datetime.now(UTC).isoformat()
        manifest["artifact_sha256"] = {
            str(p.relative_to(output)): digest(p)
            for p in sorted(output.rglob("*"))
            if p.is_file() and p.name != "run.json"
        }
        (output / "run.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
    print(
        "HMS-16 batch finished; inspect private run.json, log and JUnit; success="
        + str(manifest["success"])
    )
    return 0 if manifest["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
