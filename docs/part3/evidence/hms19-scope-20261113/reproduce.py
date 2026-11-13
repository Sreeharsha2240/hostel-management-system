"""Reproduce the documented unit/component attribution in a new output folder.

Set the documented MySQL and Django environment before running. Django's test
runner may prompt if a test database already exists; it is never auto-deleted by
this script. Run database suites serially.
"""

import argparse
import configparser
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCOPE = Path(__file__).with_name("scope-v11.json")


def run(command, *, env, log=None):
    result = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
    output = result.stdout + result.stderr
    if log:
        log.write_text(output, encoding="utf-8")
    print(output, end="")
    if result.returncode:
        raise SystemExit(result.returncode)


def summarize(path):
    report = json.loads(path.read_text(encoding="utf-8"))
    application = [
        entry["summary"]
        for name, entry in report["files"].items()
        if not name.replace("\\", "/").startswith("scripts/")
    ]
    keys = ("covered_lines", "num_statements", "covered_branches", "num_branches")
    return {key: sum(item[key] for item in application) for key in keys}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, help="A new output directory")
    args = parser.parse_args()
    output = Path(args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=False)

    scope = json.loads(SCOPE.read_text(encoding="utf-8"))
    config = configparser.ConfigParser(interpolation=None)
    config.read(ROOT / ".coveragerc", encoding="utf-8")
    config.set("run", "dynamic_context", "test_function")
    config_path = output / "coverage.ini"
    with config_path.open("w", encoding="utf-8") as stream:
        config.write(stream)

    environment = os.environ.copy()
    for name in (
        "COVERAGE_FILE",
        "COVERAGE_RCFILE",
        "COVERAGE_RUN",
        "COVERAGE_PROCESS_START",
    ):
        environment.pop(name, None)
    data_path = output / "coverage.data"
    base = [sys.executable, "-m", "coverage"]
    labels = scope["historical_component_methods"] + scope["additional_modules"]
    command = [
        *base,
        "run",
        f"--rcfile={config_path}",
        f"--data-file={data_path}",
        "manage.py",
        "test",
        *labels,
        "-v",
        "1",
    ]
    run(command, env=environment, log=output / "tests.log")

    component_parts = [
        re.escape(name) + r"(?:\|.*)?$"
        for name in scope["historical_component_methods"]
    ]
    component_parts += [re.escape(name) + r"\." for name in scope["additional_modules"]]
    isolated_parts = [
        re.escape(name) + r"\."
        for name in scope["historical_isolated_modules"] + scope["additional_modules"]
    ]
    results = {}
    for name, parts in (("component", component_parts), ("isolated", isolated_parts)):
        report_path = output / f"{name}.json"
        pattern = "^(?:" + "|".join(parts) + ")"
        run(
            [
                *base,
                "json",
                f"--rcfile={config_path}",
                f"--data-file={data_path}",
                f"--contexts={pattern}",
                "--fail-under=0",
                "-o",
                str(report_path),
            ],
            env=environment,
        )
        results[name] = summarize(report_path)

    (output / "summary.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
