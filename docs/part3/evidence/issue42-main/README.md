# HMS-20 current-main and standalone76 coverage evidence

Measured **2026-11-06**, clean candidate `b936e4d8ef7efd37dd66fde022efcb44e5b386ee`, tree `1191cfa0aed5201d3529e2f63120c5b99a29e781`. Formal SRS unit70 remains **UNPROVEN**; independent review of this refresh and accepted submission-build decisions remain pending.

- `coverage-metrics.json`: current per-file line/arc inventories, all nine observations, full fixed denominators, manifests, immutable raw/export hashes, complete prior-evidence hashes and added-command gaps.
- `checks-run.json`: exact clean normal run, environment and all 12 gates.
- `collection-run.json`: all serialized commands, timings, source identity and frozen76 confirmation.
- `junit-summary.json`: every normal190/context190/standalone76 outcome plus separate timing PASS.
- `attribution.json`: exact selections, observed/missing contexts, historical classification hash, unchanged source hashes and limitations.
- `startup-context-diagnostic.json`: application per-file method/empty exclusive and overlapping execution for mixed and standalone runs.
- `validation.json`: artifact reconciliation outcomes; these do not confer human acceptance.

The exhaustive method classification stays in [the original immutable evidence](../issue42-final/method-classification.json); current test-source hashes match it. The historical selection was confirmed unchanged before current execution, not reclassified after earlier rates. All prior **36** tracked evidence JSON files retain their original bytes. The manifest preserves the measured `docs/PART3.md` hash as the pre-publication documentation snapshot; its later owner index update does not alter the tested source identity. `Test_Case_Document.md` is unchanged in this refresh.

## Recorded normal verification

| Gate | Executed command | Exit code |
|---|---|---|
| lint | python -m ruff check . | 0 |
| format | python -m ruff format --check . | 0 |
| dependencies | python -m pip check | 0 |
| django-checks | python manage.py check --database default | 0 |
| applied-migrations | python manage.py migrate --check | 0 |
| migration-consistency | python manage.py makemigrations --check --dry-run | 0 |
| staticfiles | python manage.py collectstatic --dry-run --noinput --verbosity 0 | 0 |
| test-results | python -m coverage run manage.py test --noinput --testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner | 0 |
| coverage | python -m coverage report | 0 |
| coverage-xml | python scripts/run_checks.py --coverage-xml <repository>\test-results\sprint-remaining\20261106T162946225635Z\checks\coverage.xml | 0 |
| coverage-json | python -m coverage json -o <repository>\test-results\sprint-remaining\20261106T162946225635Z\checks\coverage.json | 0 |
| timing-smoke | python manage.py test accounts.tests.AuthenticationTests.test_login_and_role_dashboard_respond_within_two_seconds --noinput | 0 |

## Reproduction

Use the recorded dependencies/MySQL environment and synthetic test fixtures. Coordinate serial ownership of disposable `test_hms`; preserve existing outputs and use fresh coverage/JUnit directories. Clear inherited `COVERAGE_FILE`, `COVERAGE_RCFILE`, `COVERAGE_RUN`, `COVERAGE_PROCESS_START` and `HMS_TEST_OUTPUT_DIR` before normal checks:

```powershell
python scripts/run_checks.py --output-dir test-results/<new-run>/checks
```

Copy unchanged `.coveragerc` into each new collection folder and add only `dynamic_context = test_function` beneath `[run]`. Set `COVERAGE_FILE`, `COVERAGE_RCFILE` and `HMS_TEST_OUTPUT_DIR` to that folder's new artifacts. The full mixed collection runs:

```powershell
python -m coverage run manage.py test --noinput --testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner
```

The standalone collection uses the **76 exact labels** in `attribution.json` under `scopes.standalone76_methods.selected_methods` as positional arguments after `manage.py test`, with the same flags. Do not substitute module/class labels or discover the complete suite. The exact executed argument vector is retained in `collection-run.json`. Assert JUnit identities equal the selected76 exactly before interpreting coverage.

For a new standalone reproduction, run the following Python from the repository root with the recorded environment. Choose a fresh `run_name`; the directory creation deliberately refuses to reuse previous outputs. Coordinate `test_hms` ownership before executing it. Its preflight reads configuration/schema ownership; Django tests create and remove their own test database.

```python
import json
import os
import subprocess
import sys
from pathlib import Path

root = Path.cwd()
run_name = "standalone76-reproduction-unique"
out = root / "test-results" / run_name
out.mkdir(parents=True, exist_ok=False)
attribution = json.loads(
    (root / "docs/part3/evidence/issue42-main/attribution.json").read_text(
        encoding="utf-8"
    )
)
ids = attribution["scopes"]["standalone76_methods"]["selected_methods"]
assert len(ids) == len(set(ids)) == 76
config = (root / ".coveragerc").read_text(encoding="utf-8")
config = config.replace("[run]", "[run]\ndynamic_context = test_function", 1)
(out / ".coveragerc").write_text(config, encoding="utf-8")
environment = os.environ.copy()
for key in (
    "COVERAGE_FILE",
    "COVERAGE_RCFILE",
    "COVERAGE_RUN",
    "COVERAGE_PROCESS_START",
    "HMS_TEST_OUTPUT_DIR",
):
    environment.pop(key, None)
environment.update(
    COVERAGE_FILE=str(out / ".coverage"),
    COVERAGE_RCFILE=str(out / ".coveragerc"),
    HMS_TEST_OUTPUT_DIR=str(out / "junit"),
    PYTHONIOENCODING="utf-8",
)
preflight = (
    "import os;os.environ.setdefault('DJANGO_SETTINGS_MODULE','hms.settings');"
    "import django;django.setup();from django.db import connection;"
    "assert connection.vendor=='mysql' and connection.settings_dict['NAME']=='hms';"
    'c=connection.cursor();c.execute("SELECT SCHEMA_NAME FROM '
    "INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='test_hms'\");"
    "assert c.fetchone() is None,'test_hms exists; identify its owner';"
    "connection.close()"
)
subprocess.run([sys.executable, "-c", preflight], cwd=root, env=environment, check=True)
subprocess.run(
    [
        sys.executable,
        "-m",
        "coverage",
        "run",
        "manage.py",
        "test",
        *ids,
        "--noinput",
        "--testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner",
    ],
    cwd=root,
    env=environment,
    check=True,
)
subprocess.run([sys.executable, "-c", preflight], cwd=root, env=environment, check=True)
```

Export complete data and retain `.coverage` unchanged. For method-only exports, use anchored alternatives built with `re.escape` from the exact selected IDs. Empty context uses `^$`; all nonempty method contexts use `^.+$`. Use the existing `scripts/run_checks.py --coverage-xml <path>` helper with query contexts explicitly set through the Coverage API for filtered XML, and independently reconcile every line and branch destination to JSON. Diagnostic `--fail-under=0` is an observation-export option only; retain the normal combined gate unchanged.

The following standalone Python exports the new `.coverage` read-only through the public Coverage API, without the private generation helper. Reuse the same `run_name` as above. Separate fresh Coverage objects keep JSON/XML reporter state independent. Setting query contexts **before both reporters** avoids granting startup line hits to selected-method XML. Restrict XML to the complete measured file set and use repository-relative paths so same-named package files remain distinct. Report-level `fail_under = 0` here only exports diagnostic observations; the tracked gate remains70.

```python
import hashlib
import json
import re
from pathlib import Path
from coverage import Coverage

root = Path.cwd()
run_name = "standalone76-reproduction-unique"
out = root / "test-results" / run_name
data_file, config_file = out / ".coverage", out / ".coveragerc"
attribution = json.loads(
    (root / "docs/part3/evidence/issue42-main/attribution.json").read_text(
        encoding="utf-8"
    )
)
ids = attribution["scopes"]["standalone76_methods"]["selected_methods"]
selected = ["^(?:" + "|".join(re.escape(value) for value in ids) + ")$"]
before = hashlib.sha256(data_file.read_bytes()).hexdigest()
for name, filters in (("all", None), ("methods", selected), ("empty", ["^$"])):
    folder = out / "exports" / name
    folder.mkdir(parents=True, exist_ok=True)
    json_cov = Coverage(data_file=str(data_file), config_file=str(config_file))
    json_cov.load()
    json_cov.set_option("report:fail_under", 0)
    json_cov.set_option("report:contexts", filters)
    json_cov.get_data().set_query_contexts(filters)
    json_cov.json_report(
        outfile=str(folder / "coverage.json"), contexts=filters, show_contexts=True
    )
    xml_cov = Coverage(data_file=str(data_file), config_file=str(config_file))
    xml_cov.load()
    xml_cov.set_option("report:fail_under", 0)
    xml_cov.set_option("report:contexts", filters)
    xml_cov.get_data().set_query_contexts(filters)
    xml_cov.set_option("run:source", [str(root)])
    xml_cov.xml_report(
        morfs=sorted(xml_cov.get_data().measured_files()),
        outfile=str(folder / "coverage.xml"),
    )
    assert hashlib.sha256(data_file.read_bytes()).hexdigest() == before
```

All scopes must preserve the same current measured files, executable statement lines and branch arcs. Reconcile raw and independent aggregate exports, JSON/XML hits and per-line branch destinations, JUnit identities/statuses, source hashes, prior JSON hashes, and method/empty unions/overlaps. No absent method context receives inferred credit. Raw artifacts remain private under ignored test outputs; only sanitized relevant metrics/hashes are committed.

## Observations and limitations

| Application scope | Executed/measured statements | Statements | Covered/measured outcomes | Branches |
|---|---|---|---|---|
| Normal full mixed suite | 1505/1677 | 89.74% | 330/410 | 80.49% |
| Context full mixed suite | 1505/1677 | 89.74% | 330/410 | 80.49% |
| Mixed-run conservative76 method contexts | 405/1677 | 24.15% | 173/410 | 42.20% |
| Mixed-run sensitivity100 method contexts | 629/1677 | 37.51% | 261/410 | 63.66% |
| Standalone76 including startup/shared setup | 1127/1677 | 67.20% | 175/410 | 42.68% |
| Standalone76 method contexts only | 414/1677 | 24.69% | 173/410 | 42.20% |
| Standalone76 empty startup/shared-setup context | 735/1677 | 43.83% | 13/410 | 3.17% |

| Execution | Observed method contexts | Method statements | Empty-context statements | Empty-only statements | Overlap statements |
|---|---|---|---|---|---|
| mixed | 181 | 792 | 735 | 713 | 22 |
| standalone76 | 73 | 414 | 735 | 713 | 22 |

Standalone aggregate means execution of the selected proposed component suite **including imports/startup/shared fixtures**, not coverage solely attributable to assertions. Empty context mixes imports/declarations, framework/database setup, shared fixtures and teardown. This collection cannot separate those causes. Method and empty execution overlap; summing them overcounts. Retaining the full-file denominator is deliberate, and it is not an approved application-logic definition.

The same76 selected methods observe 414 application statements in standalone execution versus 405 in the full mixed run. The additional nine lines are only import/class/function declarations in `accounts/backends.py` (3, 5, 6, 7, 8, 11, 12, 13, 15), attributed differently because of import timing and test order. No extra tested behavior is inferred.

All measured files—including new zero-executed seed/demo commands—remain in the denominator. The commands were not invoked to populate application data. No tests, omissions, threshold or frozen method choice changed for a percentage. No fresh unit scope, QA acceptance, full RTM acceptance or readiness is inferred. PR #54's real previous independent approval is acknowledged; this current refresh still needs fresh review.
