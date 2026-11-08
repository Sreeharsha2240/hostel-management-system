"""Execute Devansh's nine reviewed expanded cases in disposable MySQL test_hms.

Run serially with every other database suite. Existing/custom/mirrored test
databases are refused before Django setup can create or replace a database.
Per-step records and JUnit remain separate from the original 13 HMS-18 cases.
"""

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
CASE_IDS = tuple(f"TC-REG-S2-{number:02d}" for number in range(8, 17))
MODULES = (
    "scripts.part3.test_owned_transactions",
    "scripts.part3.test_owned_reports_inputs",
)
CASE_METHODS = dict(
    zip(
        CASE_IDS,
        (
            MODULES[0]
            + ".OwnedAllocationTransactions.test_tc_reg_s2_08_rollback_and_retry",
            MODULES[0]
            + ".OwnedPaymentTransactions.test_tc_reg_s2_09_payment_permanence",
            MODULES[0]
            + ".OwnedPaymentTransactions.test_tc_reg_s2_10_rejected_failed_and_exhausted_receipts",
            MODULES[0]
            + ".OwnedPaymentCorrectionConcurrency.test_tc_reg_s2_11_competing_corrections",
            MODULES[1]
            + ".OwnedReportInputCases.test_tc_reg_s2_12_report_history_balances_and_locations",
            MODULES[1]
            + ".OwnedReportInputCases.test_tc_reg_s2_13_csv_literals_unicode_and_html",
            MODULES[1] + ".OwnedReportInputCases.test_tc_reg_s2_14_report_boundaries",
            MODULES[1]
            + ".OwnedReportInputCases.test_tc_reg_s2_15_malformed_json_and_controls",
            MODULES[1]
            + ".OwnedReportInputCases.test_tc_reg_s2_16_typed_dates_references_and_contracts",
        ),
        strict=True,
    )
)


def git_output(*arguments):
    return subprocess.check_output(
        ["git", *arguments], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_database(database, connection):
    if (
        database["ENGINE"] != "django.db.backends.mysql"
        or database["NAME"] != "hms"
        or database.get("TEST", {}).get("NAME") not in (None, "test_hms")
        or database.get("TEST", {}).get("MIRROR")
    ):
        raise ValueError("Require MySQL hms with separate, non-mirrored test_hms.")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            mysql_version = cursor.fetchone()[0]
            cursor.execute(
                "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",
                ["test_hms"],
            )
            if cursor.fetchone() is not None:
                raise ValueError("test_hms exists; refusing to replace existing data.")
    finally:
        connection.close()
    return mysql_version


def collect_results(output):
    raw_methods = {}
    for path in sorted((output / "junit").glob("TEST-*.xml")):
        for case in ElementTree.parse(path).getroot().iter("testcase"):
            identity = case.attrib["classname"] + "." + case.attrib["name"]
            if identity in raw_methods:
                raise ValueError("Duplicate JUnit method identity.")
            raw_methods[identity] = (
                "FAIL"
                if case.find("failure") is not None
                else "ERROR"
                if case.find("error") is not None
                else "SKIP"
                if case.find("skipped") is not None
                else "PASS"
            )
    methods = {}
    rank = {"PASS": 0, "SKIP": 1, "FAIL": 2, "ERROR": 3}
    for identity, status in raw_methods.items():
        # xmlrunner records failing subtests with their parameter suffix.
        parent = identity.split(" (", 1)[0].split(" [", 1)[0]
        if parent not in CASE_METHODS.values():
            raise ValueError("Unexpected JUnit method identity.")
        previous = methods.get(parent, "PASS")
        methods[parent] = max(previous, status, key=rank.__getitem__)
    cases = {}
    for case_id, expected_method in CASE_METHODS.items():
        path = output / f"{case_id}.json"
        if not path.exists():
            status = methods.get(expected_method, "NOT RUN")
            if status == "PASS":
                status = "ERROR"
            cases[case_id] = {
                "status": status,
                "test_id": expected_method,
                "steps": [],
                "record_missing": True,
            }
            continue
        record = json.loads(path.read_text(encoding="utf-8"))
        if record["case_id"] != case_id or record["test_id"] != expected_method:
            raise ValueError("Case record identity mismatch.")
        status = methods.get(expected_method, "ERROR")
        if status == "PASS" and (
            record["execution_status"] != "ASSERTIONS_COMPLETED" or not record["steps"]
        ):
            status = "ERROR"
        cases[case_id] = {**record, "status": status, "record": path.name}
    return methods, cases, raw_methods


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args(argv)
    output = (
        args.output_dir
        or ROOT
        / "test-results"
        / "owned-regressions"
        / datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    ).resolve()
    if not output.is_relative_to(ROOT):
        parser.error("Choose an ignored output directory inside this repository.")
    if output.exists():
        parser.error("Choose a new empty output directory; preserve earlier evidence.")
    ignored = subprocess.run(
        ["git", "check-ignore", "--quiet", str(output / "private-evidence-check")],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if ignored.returncode:
        parser.error("The evidence output must be Git-ignored, e.g. test-results/NEW.")
    # Atomic reservation prevents concurrent writers from sharing a result set.
    try:
        output.mkdir(parents=True)
    except FileExistsError:
        parser.error("The evidence directory was created by another process.")
    result = {
        "issue": 63,
        "owner": "Devansh Gupta (DevaOnL)",
        "started_at": datetime.now(UTC).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "expected_case_methods": CASE_METHODS,
        "success": False,
        "scope": "Nine reviewed synthetic integration cases; not unit-only or whole-plan acceptance",
    }
    # Save even failed setup/launch/result collection; never copy exception text.
    (output / "run.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    stage = "source-and-dependencies"
    try:
        result.update(
            {
                "commit": git_output("rev-parse", "HEAD"),
                "tree": git_output("rev-parse", "HEAD^{tree}"),
                "git_dirty": bool(git_output("status", "--porcelain")),
                "dependencies": {
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
        names = set(git_output("ls-files").splitlines())
        names.update(
            git_output("ls-files", "--others", "--exclude-standard").splitlines()
        )
        design_names = {
            ".coveragerc",
            ".github/workflows/django.yml",
            "requirements.txt",
            "requirements-dev.txt",
            "docs/part3/Test_Case_Document.md",
            "docs/part3/evidence/issue63/pre-execution-review.md",
            "Test_Plan_Hostel_Management_System.docx",
            "SRS_Hostel_Management_System.docx",
            "SAD_Hostel_Management_System.docx",
            "docs/part3/SE_Mini_Project_Delivereables_Part-3.pdf",
        }
        result["source_sha256"] = {
            name: file_hash(ROOT / name)
            for name in sorted(names)
            if name.endswith((".py", ".html")) or name in design_names
        }
        sys.path.insert(0, str(ROOT))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hms.settings")
        import django
        from django.conf import settings
        from django.db import connection

        django.setup()
        stage = "database-preflight"
        result["mysql"] = check_database(settings.DATABASES["default"], connection)
        environment = os.environ.copy()
        environment.pop("COVERAGE_RUN", None)
        environment.update(
            {
                "PYTHONIOENCODING": "utf-8",
                "HMS_OWNED_CASE_OUTPUT_DIR": str(output),
                "HMS_TEST_OUTPUT_DIR": str(output / "junit"),
                "DJANGO_SECURE_SSL_REDIRECT": "False",
                "DJANGO_SESSION_COOKIE_SECURE": "False",
                "DJANGO_CSRF_COOKIE_SECURE": "False",
            }
        )
        result["test_settings"] = {
            "TIME_ZONE": settings.TIME_ZONE,
            "SECURE_SSL_REDIRECT": False,
            "SESSION_COOKIE_SECURE": False,
            "CSRF_COOKIE_SECURE": False,
            "transport_scope": "Django test-client HTTP in disposable test_hms; no TLS claim",
        }
        # Interactive creation plus closed stdin refuses a newly appeared DB;
        # --noinput would let Django automatically drop that database on a race.
        command = [
            sys.executable,
            "manage.py",
            "test",
            *MODULES,
            "--verbosity=2",
            "--testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner",
        ]
        result["command"] = ["python", *command[1:]]
        stage = "case-execution"
        log_path = output / "execution.txt"
        with log_path.open("w", encoding="utf-8") as log:
            completed = subprocess.run(
                command,
                cwd=ROOT,
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                check=False,
            )
        result["exit_code"] = completed.returncode
        print(log_path.read_text(encoding="utf-8"))
    except Exception as error:
        result["failure_stage"] = stage
        result["failure_type"] = type(error).__name__
        print(
            f"Owned case execution could not complete during {stage} ({type(error).__name__})."
        )
    finally:
        try:
            methods, cases, raw_methods = collect_results(output)
            result.update(
                {
                    "methods": methods,
                    "raw_junit_outcomes": raw_methods,
                    "method_counts": dict(Counter(methods.values())),
                    "cases": cases,
                    "case_counts": dict(
                        Counter(case["status"] for case in cases.values())
                    ),
                }
            )
            changed_inputs = [
                name
                for name, digest in result.get("source_sha256", {}).items()
                if not (ROOT / name).is_file() or file_hash(ROOT / name) != digest
            ]
            result["changed_inputs_during_execution"] = changed_inputs
            result["success"] = (
                "failure_type" not in result
                and result.get("exit_code") == 0
                and set(methods) == set(CASE_METHODS.values())
                and all(case["status"] == "PASS" for case in cases.values())
                and not changed_inputs
            )
        except Exception as error:
            result["success"] = False
            result["collection_failure_type"] = type(error).__name__
        result["completed_at"] = datetime.now(UTC).isoformat()
        result["raw_artifact_sha256"] = {
            str(path.relative_to(output)).replace("\\", "/"): file_hash(path)
            for path in sorted(output.rglob("*"))
            if path.is_file() and path.name != "run.json"
        }
        (output / "run.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
    print(f"Case counts: {result.get('case_counts', {})}; evidence: {output}")
    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
