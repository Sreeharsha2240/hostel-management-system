"""Measure a frozen, database-forbidden unit selection without an SRS disposition.

Scope JSON: {"schema_version": 1, "selected_methods": ["app.module.Class.test_x"]}.
Additional descriptive fields are allowed. Output must be a new test-results subdir.
Hashes normalize CRLF to LF; JSON hashes use sorted keys, compact separators,
UTF-8, and a final newline. Application boundaries and exclusions come unchanged
from .coveragerc; scripts/ is reported separately from the application subtotal.
"""

import argparse
import ast
import configparser
import contextlib
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import subprocess
import sys
import time
import traceback
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[4]
CONFIG = ROOT / ".coveragerc"


def canonical_json(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")


def source_hash(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def write_json(path, value):
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def git(*arguments):
    return subprocess.check_output(["git", *arguments], cwd=ROOT, text=True).strip()


def selection(scope):
    labels = scope.get("selected_methods")
    if scope.get("schema_version") != 1 or not isinstance(labels, list) or not labels:
        raise ValueError(
            "Scope requires schema_version=1 and nonempty selected_methods"
        )
    if any(
        not isinstance(label, str)
        or not re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+\.test_\w+", label)
        for label in labels
    ):
        raise ValueError(
            "Every selected method must be an explicit canonical dotted test ID"
        )
    if len(set(labels)) != len(labels):
        raise ValueError("Duplicate selected test methods are forbidden")
    return sorted(labels)


def flatten(suite):
    for item in suite:
        if hasattr(item, "_tests"):
            yield from flatten(item)
        else:
            yield item


def validate_suite(suite, labels):
    from django.test import SimpleTestCase, TransactionTestCase

    tests = list(flatten(suite))
    identities = sorted(test.id() for test in tests)
    if identities != labels:
        raise ValueError(
            f"Discovered identities differ: missing={sorted(set(labels) - set(identities))}, unexpected={sorted(set(identities) - set(labels))}"
        )
    for test in tests:
        if not isinstance(test, SimpleTestCase) or isinstance(
            test, TransactionTestCase
        ):
            raise ValueError(f"Not an isolated SimpleTestCase: {test.id()}")
        if test.databases:
            raise ValueError(f"Database-enabled test rejected: {test.id()}")
    return identities


def junit_identities(directory):
    identities = []
    for path in sorted(directory.glob("*.xml")):
        suite = ElementTree.parse(path).getroot()
        identities.extend(
            f"{case.attrib['classname']}.{case.attrib['name']}"
            for case in suite.iter("testcase")
        )
    return sorted(identities)


def validate_junit(identities, labels):
    if identities != labels:
        raise ValueError("JUnit identities do not match the frozen selection")


def behavior_statements(source, statements):
    """All callable bodies, including decorators of definitions created in them.

    Import-time module/class declarations are excluded by syntax, independent of
    execution counts. Declarative validators/constraints/routes remain outside
    this behavioral diagnostic even when unit tests validate their contracts.
    """
    tree = ast.parse(source)
    function_types = (ast.FunctionDef, ast.AsyncFunctionDef)
    parents = {
        child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)
    }
    body_lines = {
        line
        for node in ast.walk(tree)
        if isinstance(node, function_types)
        for statement in node.body
        for line in range(statement.lineno, statement.end_lineno + 1)
    }
    for node in ast.walk(tree):
        if not isinstance(node, (*function_types, ast.ClassDef)):
            continue
        parent = parents.get(node)
        while parent is not None and not isinstance(parent, function_types):
            parent = parents.get(parent)
        if parent is not None:
            for decorator in node.decorator_list:
                body_lines.update(range(decorator.lineno, decorator.end_lineno + 1))
    return set(statements) & body_lines


def source_snapshot(config, scope_path):
    paths = {
        CONFIG,
        ROOT / "requirements.txt",
        ROOT / "requirements-dev.txt",
        ROOT / ".github/workflows/django.yml",
        scope_path,
    }
    paths.update(Path(__file__).parent.glob("*.py"))
    for name in config.get("run", "source").replace("\n", "").split(","):
        directory = ROOT / name.strip()
        if not directory.is_dir():
            raise ValueError(f"Configured source directory missing: {directory}")
        paths.update(directory.rglob("*.py"))
    return {
        str(path.relative_to(ROOT)).replace("\\", "/"): source_hash(path)
        for path in sorted(paths)
    }


def coverage_lines(data):
    return {
        os.path.normcase(str(Path(name).resolve())): sorted(data.lines(name) or [])
        for name in data.measured_files()
    }


def aggregate(files, category):
    included = [
        entry for name, entry in files.items() if not name.startswith("scripts/")
    ]
    statements = sum(len(entry[category]["included_lines"]) for entry in included)
    covered = sum(len(entry[category]["method_executed_lines"]) for entry in included)
    return {
        "covered_statements": covered,
        "statements": statements,
        "percent": 100 * covered / statements if statements else None,
    }


def measure(cov, output, labels, startup):
    from coverage.parser import PythonParser

    patterns = ["^" + re.escape(label) + "$" for label in labels]
    cov.json_report(
        outfile=str(output / "total-coverage.json"),
        pretty_print=True,
        show_contexts=True,
    )
    cov.json_report(
        outfile=str(output / "method-coverage.json"),
        contexts=patterns,
        pretty_print=True,
        show_contexts=True,
    )
    total = json.loads((output / "total-coverage.json").read_text(encoding="utf-8"))
    methods = json.loads((output / "method-coverage.json").read_text(encoding="utf-8"))
    method_files = {
        name.replace("\\", "/"): entry for name, entry in methods["files"].items()
    }
    data = cov.get_data()
    contexts = sorted(data.measured_contexts())
    unexpected = sorted(set(contexts) - {"", *labels})
    if unexpected:
        raise ValueError(f"Unexpected dynamic coverage contexts: {unexpected}")
    files = {}
    for name, report in total["files"].items():
        name = name.replace("\\", "/")
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError(f"Coverage source outside repository: {name}")
        source = path.read_text(encoding="utf-8")
        parser = PythonParser(text=source, filename=str(path))
        parser.parse_source()
        statements = set(parser.statements) - set(report["excluded_lines"])
        if len(statements) != report["summary"]["num_statements"]:
            raise ValueError(f"Coverage/parser denominator mismatch: {name}")
        body = behavior_statements(source, statements)
        executed = set(report["executed_lines"])
        method_executed = set(method_files[name]["executed_lines"])
        startup_executed = set(startup.get(os.path.normcase(str(path)), []))
        files[name] = {"sha256_canonical_lf": source_hash(path)}
        for category, included in (("full_file", statements), ("function_body", body)):
            files[name][category] = {
                "included_lines": sorted(included),
                "excluded_lines": sorted(statements - included),
                "total_executed_lines": sorted(executed & included),
                "startup_before_runner_lines": sorted(startup_executed & included),
                "method_executed_lines": sorted(method_executed & included),
                "other_only_executed_lines": sorted(
                    (executed - method_executed - startup_executed) & included
                ),
            }
        files[name]["method_branches"] = {
            key: method_files[name]["summary"][key]
            for key in ("covered_branches", "num_branches")
        }
    return {
        "full_file_method_diagnostic": aggregate(files, "full_file"),
        "function_body_method_diagnostic": aggregate(files, "function_body"),
        "contexts": contexts,
        "methods_without_application_context": sorted(set(labels) - set(contexts)),
        "files": files,
        "interpretation": "Diagnostics only; no threshold PASS or stakeholder scope acceptance. Startup and method sets may overlap. Other-only means executed after the startup snapshot outside selected method contexts. Declarative rules are excluded from the function-body denominator.",
    }


def execute(labels, output, cov, metadata):
    import django
    from django.db.backends.base.base import BaseDatabaseWrapper
    from xmlrunner.extra.djangotestrunner import XMLTestRunner
    from xmlrunner.result import _XMLTestResult

    started, outcomes, database_attempts = [], {}, []
    metadata["execution"] = {
        "started_methods": started,
        "method_outcomes": outcomes,
        "database_attempts": database_attempts,
    }

    def forbid_database(*args, **kwargs):
        database_attempts.append("Connection attempt blocked")
        raise AssertionError("This isolated measurement forbids database connections")

    class RecordingResult(_XMLTestResult):
        def startTest(self, test):
            started.append(test.id())
            super().startTest(test)

        def addSuccess(self, test):
            outcomes[test.id()] = "PASS"
            super().addSuccess(test)

        def addFailure(self, test, error):
            outcomes[test.id()] = "FAIL"
            super().addFailure(test, error)

        def addError(self, test, error):
            outcomes[test.id()] = "ERROR"
            super().addError(test, error)

        def addSkip(self, test, reason):
            outcomes[test.id()] = "SKIP"
            super().addSkip(test, reason)

        def addExpectedFailure(self, test, error):
            outcomes[test.id()] = "EXPECTED_FAILURE"
            super().addExpectedFailure(test, error)

        def addUnexpectedSuccess(self, test):
            outcomes[test.id()] = "UNEXPECTED_SUCCESS"
            super().addUnexpectedSuccess(test)

        def addSubTest(self, test, subtest, error):
            if error:
                outcomes[test.id()] = "FAIL"
            super().addSubTest(test, subtest, error)

    class FrozenRunner(XMLTestRunner):
        def build_suite(self, test_labels=None, **kwargs):
            if not hasattr(self, "frozen_suite"):
                suite = super().build_suite(test_labels, **kwargs)
                metadata["discovered_methods"] = validate_suite(suite, labels)
                self.frozen_suite = suite
            return self.frozen_suite

        def setup_databases(self, **kwargs):
            if kwargs.get("aliases"):
                raise ValueError("Runner requested a database for isolated tests")
            return []

        def teardown_databases(self, old_config, **kwargs):
            if old_config:
                raise ValueError("Unexpected database teardown configuration")

        def get_test_runner_kwargs(self):
            return {
                **super().get_test_runner_kwargs(),
                "output": str(output / "junit"),
                "resultclass": RecordingResult,
            }

    with (
        patch.object(BaseDatabaseWrapper, "ensure_connection", forbid_database),
        patch.object(BaseDatabaseWrapper, "connect", forbid_database),
    ):
        django.setup()
        from django.conf import settings

        metadata["effective_settings"] = {
            name: getattr(settings, name)
            for name in (
                "DEBUG",
                "SECURE_SSL_REDIRECT",
                "SESSION_COOKIE_SECURE",
                "CSRF_COOKIE_SECURE",
            )
        }
        runner = FrozenRunner(verbosity=1, interactive=False)
        runner.build_suite(labels)
        startup = coverage_lines(cov.get_data())
        failures = runner.run_tests(labels)
    metadata["execution"]["counts"] = {
        status: sum(value == status for value in outcomes.values())
        for status in sorted(set(outcomes.values()))
    }
    metadata["execution"]["runner_failures"] = failures
    if (
        failures
        or database_attempts
        or sorted(started) != labels
        or set(outcomes) != set(labels)
        or any(status != "PASS" for status in outcomes.values())
    ):
        raise ValueError(
            "Frozen isolated test execution was incomplete or unsuccessful"
        )
    metadata["junit_methods"] = junit_identities(output / "junit")
    validate_junit(metadata["junit_methods"], labels)
    return startup


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args(argv)
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))
    scope_path = Path(args.scope).resolve()
    if not scope_path.is_relative_to(ROOT):
        parser.error("--scope must be inside this repository")
    output = Path(args.output_dir).resolve()
    results_root = (ROOT / "test-results").resolve()
    if output == results_root or not output.is_relative_to(results_root):
        parser.error(
            "--output-dir must be a new subdirectory of this repository's test-results/"
        )
    if subprocess.run(
        ["git", "check-ignore", "-q", str(output.relative_to(ROOT)) + "/"], cwd=ROOT
    ).returncode:
        parser.error("Output directory must be ignored by Git")
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    metadata = {
        "schema_version": 1,
        "status": "INCOMPLETE",
        "srs_disposition": "UNPROVEN; stakeholder scope acceptance pending",
        "hash_format": "SHA-256; source CRLF normalized to LF; JSON UTF-8 sorted keys, compact separators, final LF",
        "started_at_utc": datetime.now(UTC).isoformat(),
        "invocation": [
            "python",
            str(Path(__file__).relative_to(ROOT)).replace("\\", "/"),
            "--scope",
            str(Path(args.scope).resolve().relative_to(ROOT)).replace("\\", "/"),
            "--output-dir",
            str(output.relative_to(ROOT)).replace("\\", "/"),
        ],
    }
    cov = None
    before = None
    try:
        from coverage import Coverage

        for name in list(os.environ):
            if name.startswith("COVERAGE_"):
                os.environ.pop(name)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hms.settings")
        scope = json.loads(scope_path.read_text(encoding="utf-8"))
        labels = selection(scope)
        metadata["selected_methods"] = labels
        metadata["selection_sha256_canonical_json"] = hashlib.sha256(
            canonical_json({"selected_methods": labels})
        ).hexdigest()
        metadata["scope_sha256_canonical_json"] = hashlib.sha256(
            canonical_json(scope)
        ).hexdigest()
        metadata["git"] = {
            "commit": git("rev-parse", "HEAD"),
            "tree": git("rev-parse", "HEAD^{tree}"),
            "dirty": bool(git("status", "--porcelain", "--untracked-files=all")),
        }
        metadata["environment"] = {
            "python": sys.version,
            "platform": platform.platform(),
            "settings_module": os.environ["DJANGO_SETTINGS_MODULE"],
        }
        metadata["dependencies"] = {
            name: importlib.metadata.version(name)
            for name in (
                "coverage",
                "Django",
                "unittest-xml-reporting",
                "mysqlclient",
                "python-dotenv",
                "reportlab",
                "pypdf",
            )
        }
        if metadata["dependencies"]["coverage"] != "7.16.2":
            raise ValueError("This measurement requires coverage==7.16.2")
        config = configparser.ConfigParser(interpolation=None)
        config.read(CONFIG, encoding="utf-8")
        before = source_snapshot(config, scope_path)
        metadata["source_sha256_canonical_lf"] = before
        expected = scope.get("expected_source_sha256_canonical_lf", {})
        if not isinstance(expected, dict) or any(
            before.get(name) != digest for name, digest in expected.items()
        ):
            raise ValueError("Frozen expected source hashes do not match this checkout")
        metadata["expected_source_hashes_verified"] = len(expected)
        config.set("run", "dynamic_context", "test_function")
        config_path = output / "coverage.ini"
        with config_path.open("w", encoding="utf-8", newline="\n") as stream:
            config.write(stream)
        metadata["temporary_config_sha256_canonical_lf"] = source_hash(config_path)
        cov = Coverage(
            config_file=str(config_path), data_file=str(output / "coverage.data")
        )
        with (
            (output / "tests.log").open("w", encoding="utf-8", newline="\n") as log,
            contextlib.redirect_stdout(log),
            contextlib.redirect_stderr(log),
        ):
            cov.start()
            try:
                startup = execute(labels, output, cov, metadata)
            finally:
                cov.stop()
                cov.save()
        after = source_snapshot(config, scope_path)
        metadata["source_unchanged_during_run"] = before == after
        if before != after:
            raise ValueError("Source/configuration changed during this run")
        metadata["measurement"] = measure(cov, output, labels, startup)
        if before != source_snapshot(config, scope_path):
            raise ValueError("Source/configuration changed while exporting coverage")
        metadata["status"] = (
            "RECORDED; all frozen isolated tests passed; no SRS disposition"
        )
    except Exception as error:
        metadata["error"] = f"{type(error).__name__}: {error}"
        (output / "error.log").write_text(
            traceback.format_exc(), encoding="utf-8", newline="\n"
        )
        if before is not None:
            try:
                metadata["source_unchanged_during_run"] = before == source_snapshot(
                    config, scope_path
                )
            except Exception as snapshot_error:
                metadata["source_unchanged_during_run"] = False
                metadata["source_snapshot_error"] = str(snapshot_error)
    finally:
        metadata["completed_at_utc"] = datetime.now(UTC).isoformat()
        metadata["elapsed_seconds"] = time.monotonic() - started
        metadata["artifacts_sha256"] = {
            str(path.relative_to(output)).replace("\\", "/"): hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
            for path in sorted(output.rglob("*"))
            if path.is_file()
        }
        write_json(output / "summary.json", metadata)
    print(
        json.dumps(
            {key: metadata[key] for key in ("status", "error") if key in metadata},
            indent=2,
        )
    )
    return 0 if metadata["status"].startswith("RECORDED;") else 1


if __name__ == "__main__":
    raise SystemExit(main())
