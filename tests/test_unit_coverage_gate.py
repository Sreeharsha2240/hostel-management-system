"""A successful process or high startup coverage cannot replace isolated evidence."""

import hashlib
import tempfile
from copy import deepcopy
from pathlib import Path
from unittest import TestCase

from scripts.part3.check_unit_coverage import assess


class UnitCoverageGateTests(TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        (self.root / "logic.py").write_text(
            "# frozen fixture\n", encoding="utf-8", newline="\n"
        )
        entry = {
            "function_body": {
                "included_lines": list(range(1, 11)),
                "method_executed_lines": list(range(1, 8)),
            },
            "full_file": {
                "included_lines": list(range(1, 21)),
                "method_executed_lines": list(range(1, 8)),
            },
        }
        self.report = {
            "status": "RECORDED; all isolated tests passed",
            "git": {"dirty": False},
            "source_unchanged_during_run": True,
            "selected_methods": ["example.test_one"],
            "junit_methods": ["example.test_one"],
            "execution": {
                "started_methods": ["example.test_one"],
                "method_outcomes": {"example.test_one": "PASS"},
                "database_attempts": [],
                "runner_failures": 0,
            },
            "source_sha256_canonical_lf": {
                "logic.py": hashlib.sha256(
                    (self.root / "logic.py").read_bytes()
                ).hexdigest()
            },
            "expected_source_hashes_verified": 1,
            "measurement": {
                "files": {
                    "accounts/logic.py": entry,
                    "scripts/helper.py": deepcopy(entry),
                }
            },
        }

    def test_exact_seventy_passes_and_companion_is_separate(self):
        result = assess(self.report, source_root=self.root)
        self.assertTrue(result["meets_target"])
        self.assertEqual((result["covered"], result["statements"]), (7, 10))
        self.assertEqual(
            result["all_statements_companion"], {"covered": 7, "statements": 20}
        )

    def test_below_seventy_fails_even_with_complete_startup_coverage(self):
        entry = self.report["measurement"]["files"]["accounts/logic.py"]
        entry["function_body"]["method_executed_lines"] = list(range(1, 7))
        entry["function_body"]["total_executed_lines"] = list(range(1, 11))
        self.assertFalse(assess(self.report, source_root=self.root)["meets_target"])

    def test_db_skips_dirty_incomplete_or_changed_source_evidence_is_rejected(self):
        for mutate in (
            lambda r: r.update(status="INCOMPLETE"),
            lambda r: r["git"].update(dirty=True),
            lambda r: r.update(source_unchanged_during_run=False),
            lambda r: r["execution"].update(database_attempts=["blocked"]),
            lambda r: r["execution"]["method_outcomes"].update(
                {"example.test_one": "SKIP"}
            ),
            lambda r: r.update(junit_methods=[]),
            lambda r: r.update(expected_source_hashes_verified=0),
        ):
            with self.subTest(mutation=mutate):
                report = deepcopy(self.report)
                mutate(report)
                with self.assertRaises(ValueError):
                    assess(report, source_root=self.root)

    def test_stale_or_escaping_source_pin_is_rejected(self):
        self.report["source_sha256_canonical_lf"]["logic.py"] = "0" * 64
        with self.assertRaises(ValueError):
            assess(self.report, source_root=self.root)
        self.report["source_sha256_canonical_lf"] = {"../outside.py": "0" * 64}
        with self.assertRaises(ValueError):
            assess(self.report, source_root=self.root)

    def test_invalid_thresholds_and_overcredited_or_empty_denominators_are_rejected(
        self,
    ):
        for value in (-1, 101, float("nan"), float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                assess(self.report, value, source_root=self.root)
        entry = self.report["measurement"]["files"]["accounts/logic.py"]
        entry["function_body"]["method_executed_lines"] = [999]
        with self.assertRaises(ValueError):
            assess(self.report, source_root=self.root)
        entry["function_body"] = {"included_lines": [], "method_executed_lines": []}
        with self.assertRaises(ValueError):
            assess(self.report, source_root=self.root)
