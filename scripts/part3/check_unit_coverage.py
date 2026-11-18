"""Enforce the recorded owner-approved unit boundary without changing measurement."""

import argparse
import hashlib
import json
import subprocess
from math import isfinite
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def assess(report, minimum=70, *, source_root=ROOT):
    if not isfinite(minimum) or not 0 <= minimum <= 100:
        raise ValueError("The coverage threshold must be between 0 and 100.")
    if not report.get("status", "").startswith("RECORDED;"):
        raise ValueError("The isolated measurement did not complete.")
    if report.get("git", {}).get("dirty") is not False:
        raise ValueError("Accepted evidence requires a clean measured revision.")
    if report.get("source_unchanged_during_run") is not True:
        raise ValueError("The measured source changed during execution.")
    selected = report.get("selected_methods", [])
    execution = report.get("execution", {})
    outcomes = execution.get("method_outcomes", {})
    if (
        not selected
        or len(set(selected)) != len(selected)
        or sorted(execution.get("started_methods", [])) != sorted(selected)
        or sorted(report.get("junit_methods", [])) != sorted(selected)
        or set(outcomes) != set(selected)
        or any(value != "PASS" for value in outcomes.values())
        or execution.get("database_attempts") != []
        or execution.get("runner_failures") != 0
    ):
        raise ValueError(
            "Require every exact isolated method PASS and zero DB attempts."
        )
    pins = report.get("source_sha256_canonical_lf", {})
    if not pins or report.get("expected_source_hashes_verified", 0) <= 0:
        raise ValueError("Frozen source verification is missing.")
    root = Path(source_root).resolve()
    for name, expected in pins.items():
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError("A pinned source file is missing or outside the checkout.")
        if (
            hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
            != expected
        ):
            raise ValueError("The current source differs from the measured source.")
    totals = {"function_body": [0, 0], "full_file": [0, 0]}
    for name, entry in report["measurement"]["files"].items():
        if name.startswith("scripts/"):
            continue
        for boundary, total in totals.items():
            included = set(entry[boundary]["included_lines"])
            credited = set(entry[boundary]["method_executed_lines"])
            if not credited.issubset(included):
                raise ValueError(
                    "Credited lines exceed the declared measurement boundary."
                )
            total[0] += len(credited)
            total[1] += len(included)
    covered, statements = totals["function_body"]
    if statements <= 0:
        raise ValueError("The application function-body denominator must be nonzero.")
    percent = 100 * covered / statements
    return {
        "boundary": "Owner-approved application function-body statements; method attribution only",
        "methods": len(selected),
        "covered": covered,
        "statements": statements,
        "percent": percent,
        "minimum": minimum,
        "meets_target": percent >= minimum,
        "all_statements_companion": {
            "covered": totals["full_file"][0],
            "statements": totals["full_file"][1],
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("measurement", type=Path)
    parser.add_argument("--minimum", type=float, default=70)
    args = parser.parse_args()
    report = json.loads(args.measurement.read_text(encoding="utf-8"))
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    if report.get("git", {}).get("commit") != head:
        raise ValueError("The measurement belongs to a different revision.")
    result = assess(report, args.minimum)
    print(json.dumps(result, indent=2))
    return 0 if result["meets_target"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
