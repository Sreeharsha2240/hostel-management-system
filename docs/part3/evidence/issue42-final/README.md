# HMS-20 current-candidate coverage evidence

Measured **2026-11-06**, clean candidate `9a0f814e403a6f83535e80a68db4150197eba74b` / tree `c916feba77b7a2aad4d75626ddab4326948d6851`. This evidence supports the two owned coverage reports. **Classification is PROPOSED, pending #41 independent scope review; accepted submission build and report review are pending.** It does not write or complete the QA Unit Test Report, the System Validation Report or final readiness.

- `coverage-metrics.json`: mixed, complete-context and two proposed component-context scopes; complete per-file lines/arcs, module/configured/application totals, unique nonempty XML row counts, source manifests and raw-artifact SHA-256 references.
- `checks-run.json`: normal environment, versions, all 12 verification gates and exact executed argument lists.
- `context-run.json`: matching clean source, copied configuration and full context-collection/export argument lists.
- `validation.json`: per-file/line/arc/XML/context/JUnit reconciliation and classification freeze chronology.
- `junit-summary.json`: every mixed/context method outcome and separate uninstrumented timing result.
- `method-classification.json`: exhaustive method inventory with behavior-based rationale. Current corrected SHA-256: `67a5dc896137bf370f8060ff02b86effbb9218e1177eb85b428346e87242d2f7`. Selection chronology and index-only repair are recorded below.
- `attribution.json`: proposed selections, observed contexts, methods without measured application contexts, fixed classification reference and interpretation limits.
- `startup-context-diagnostic.json`: later read-only analysis of all nonempty method contexts versus empty startup/shared setup, with per-file counts/overlap and the current proxy's statement ceiling; no selectors or collection data changed.

Earlier `evidence/issue42` and `evidence/owned-defects` metrics remain historical and unchanged. Raw `.coverage`, JSON/XML/JUnit and logs remain in ignored test outputs; publish only sanitized source paths, synthetic method names, relevant metadata and hashes. No credentials, real student data, connection secrets or database dumps belong here.

## Recorded normal verification

| Normal verification gate | Executed arguments | Exit code | Seconds |
|---|---|---|---|
| lint | `python -m ruff check .` | 0 | 0.175 |
| format | `python -m ruff format --check .` | 0 | 0.115 |
| dependencies | `python -m pip check` | 0 | 0.703 |
| django-checks | `python manage.py check --database default` | 0 | 1.042 |
| applied-migrations | `python manage.py migrate --check` | 0 | 1.006 |
| migration-consistency | `python manage.py makemigrations --check --dry-run` | 0 | 0.958 |
| staticfiles | `python manage.py collectstatic --dry-run --noinput --verbosity 0` | 0 | 0.724 |
| test-results | `python -m coverage run manage.py test --noinput --testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner` | 0 | 41.096 |
| coverage | `python -m coverage report` | 0 | 0.397 |
| coverage-xml | `python scripts/run_checks.py --coverage-xml <repository>\test-results\hms20-finish\20261106T032022197510Z\checks\coverage.xml` | 0 | 0.467 |
| coverage-json | `python -m coverage json -o <repository>\test-results\hms20-finish\20261106T032022197510Z\checks\coverage.json` | 0 | 0.447 |
| timing-smoke | `python manage.py test accounts.tests.AuthenticationTests.test_login_and_role_dashboard_respond_within_two_seconds --noinput` | 0 | 6.297 |

| Context step | Executed arguments | Exit code |
|---|---|---|
| context-preflight | `python -c "import os;os.environ.setdefault('DJANGO_SETTINGS_MODULE','hms.settings');import django;django.setup();from django.db import connection;assert connection.vendor=='mysql' and connection.settings_dict['NAME']=='hms';c=connection.cursor();c.execute(\"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='test_hms'\");assert c.fetchone() is None,'test_hms exists; identify its owner';connection.close();print('MySQL hms configuration verified; disposable test_hms absent')"` | 0 |
| context-tests | `python -m coverage run manage.py test --noinput --testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner` | 0 |
| context-json | `python -m coverage json --show-contexts -o <repository>\test-results\hms20-finish\20261106T032022197510Z\contexts\coverage.json` | 0 |
| context-xml | `python scripts/run_checks.py --coverage-xml <repository>\test-results\hms20-finish\20261106T032022197510Z\contexts\coverage.xml` | 0 |

Mixed: **190 methods: 189 PASS, 0 failures, 0 errors, 1 skipped**. Full context run: **190 methods: 189 PASS, 0 failures, 0 errors, 1 skipped**. The timing check skips under tracing and separately records an uninstrumented **PASS**, without coverage credit. Both current normal-environment runs pass the XML helper regression. This does not reproduce, explain or fix the earlier #38 restricted AppContainer environment failure.

All environment versions are in `checks-run.json`; the context collection uses the same software/database setup, with deliberate coverage/output environment overrides described in `context-run.json`. Source manifest inputs: **158**; original raw artifact SHA-256 entries: **80**; read-only JSON/XML reexport hashes: **8**. The measured normal and context datasets are preserved unchanged by read-only reexports.

The manifest retains the measured versions of `docs/PART3.md` and `docs/part3/Test_Case_Document.md`; both have subsequent documentation edits. Runtime, test and configuration inputs remain unchanged from the measured candidate. The original frozen artifact remains in private raw evidence under its recorded hash for teammate inspection; the repository artifact is the corrected version, and its serialized bytes are not claimed to predate the rates.

The method decisions and exact 76/100 selections were frozen at **2026-11-06T03:27:27.875258+00:00**, before subset exports or unit-rate extraction. Original pre-export artifact SHA-256: `4bb5ccd486ea2da7c64029f484de923ea40846c8a9bf8d337dfe75688549ffe3`. A redundant borderline summary index was repaired afterward at **2026-11-06T03:30:23.647384+00:00** (21 cached IDs versus 24 unchanged flagged method rows). All categories, reasons, flags and selections remained unchanged; the corrected serialized artifact postdates the rates. Unchanged selection-core SHA-256: `654020d1bb897ed83e4d2dfc4a265e25d41932af0e6f3778d69e0ddcbbaf5679`. Of 85 primary component methods, 9 borderline cases are excluded from conservative76; sensitivity100 adds all24 borderline cases to conservative76. This correction does not claim a new coverage-blind selection after seeing results.

The [startup/shared-setup diagnostic](startup-context-diagnostic.json) quantifies a limit of this proxy: **all 181 recorded nonempty test-method contexts together** cover only **792/1579 application statements (50.16%)**, and **328/378 branch outcomes (86.77%)**. These contexts include integration, system and tooling checks as well as proposed units. Their union is an upper bound for any selection of the existing observed methods, not a unit result.

The empty context executes **735 statements**: **713 exclusively** there and **22 also within methods**. It mixes imports, declarations and shared setup. Thus reclassification alone cannot demonstrate 70% with this recorded method-only/full-file proxy. The 25.65%/39.84% figures do not establish inadequate unit tests or a formal SRS failure. QA must agree on application logic and appropriate attribution/instrumentation; this diagnostic does not credit shared setup to units or remove it from the denominator. Different execution, future tests or a reviewed denominator may differ. This later read-only analysis preserves the original data, frozen decisions and 76/100 selections; it is not a new unit run.

## Reproduction

Use the recorded Python/Django/MySQL dependencies and synthetic fixtures in a disposable environment. Run **one MySQL suite at a time**, coordinating with #41. Preserve prior outputs and choose a new ignored output directory. Start a fresh PowerShell session so diagnostic coverage variables cannot affect the normal verification:

```powershell
Remove-Item Env:COVERAGE_FILE,Env:COVERAGE_RCFILE,Env:COVERAGE_RUN,Env:COVERAGE_PROCESS_START,Env:HMS_TEST_OUTPUT_DIR -ErrorAction SilentlyContinue
python scripts/run_checks.py --output-dir test-results/<new-run>/checks
```

For the second collection, copy the unchanged repository `.coveragerc` to `test-results/<new-run>/contexts/.coveragerc` and add **only** `dynamic_context = test_function` under `[run]`. Leave all collection sources, omissions and the 70% combined gate unchanged. In a separate shell:

```powershell
$env:COVERAGE_FILE = "test-results/<new-run>/contexts/.coverage"
$env:COVERAGE_RCFILE = "test-results/<new-run>/contexts/.coveragerc"
$env:HMS_TEST_OUTPUT_DIR = "test-results/<new-run>/contexts/junit"
python -m coverage run manage.py test --noinput --testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner
python -m coverage json --show-contexts -o test-results/<new-run>/contexts/coverage.json
python scripts/run_checks.py --coverage-xml test-results/<new-run>/contexts/coverage.xml
```

This executes the **entire mixed suite**, not a standalone unit suite. Freeze the exhaustive behavior-based classification before extracting/interpreting unit rates. Select exact method IDs from `attribution.json`; construct each anchored context expression with `re.escape` rather than treating method names as regular expressions:

```python
import json, re
from pathlib import Path

root = Path("test-results/<new-run>/contexts")
base = (root / ".coveragerc").read_text(encoding="utf-8")
attribution = json.loads(
    Path("docs/part3/evidence/issue42-final/attribution.json").read_text(
        encoding="utf-8"
    )
)
for scope in ("component_proposal", "component_sensitivity"):
    ids = attribution["scopes"][scope]["selected_methods"]
    expression = "^(?:" + "|".join(re.escape(value) for value in ids) + ")$"
    selected = base.replace("[report]", "[report]\ncontexts = " + expression, 1)
    (root / (scope + ".coveragerc")).write_text(selected, encoding="utf-8")
```

For each scope, point `COVERAGE_RCFILE` at its selected configuration while retaining the same `COVERAGE_FILE`. Export without rerunning the tests:

```powershell
$env:COVERAGE_RCFILE = "test-results/<new-run>/contexts/component_proposal.coveragerc"
python -m coverage json --show-contexts --fail-under=0 -o test-results/<new-run>/contexts/component_proposal.json
python scripts/run_checks.py --coverage-xml test-results/<new-run>/contexts/component_proposal.xml
```

Repeat exports with `component_sensitivity.coveragerc` and matching filenames. Use `scripts/run_checks.py --coverage-xml` for selected XML: its helper explicitly sets data query contexts before reporting, avoiding startup-inclusive statement hits from ordinary XML export. `--fail-under=0` is an extraction option only; the normal 70% combined gate remains unchanged.

## Reconciliation and interpretation

Check all 12 normal gates, normal/context JUnit sums and exact method IDs, classification SHA, selected/observed contexts, missing-context methods, every source manifest entry, every file's executed/missing lines/arcs, module/application/configured sums and unique XML paths/rows against the same raw datasets. The two full collections must retain identical measured file/statement/outcome denominators. All selected IDs must occur in JUnit; observed contexts must be a subset of the selection. No missing method context receives inferred coverage. Verify timing separately and preserve every failed attempt or tooling diagnostic.

The application subtotal excludes only runner tooling and retains full measured application-file denominators, including declarations. Empty startup/import/shared setup context is excluded from the proposed unit numerators. This conservative asymmetry and the application-logic definition require #41 review; do not silently credit setup or reduce the denominator to reach 70%. Test Plan §5 permits model/form/view units, so classify behavior rather than the mere presence of ORM fixtures. Sensitivity documents uncertainty and does not replace the primary proposal.

SRS §6.4's at-least-70% unit application-logic criterion remains **UNPROVEN pending accepted scope and independent review**, regardless of proposed numerical rates. The existing combined gate is a different metric. There is no separately specified Part 3 branch threshold. Test Case Document merge, issue closure, CI or these owner reports do not establish QA/Dev/PO approvals, RTM/system acceptance or readiness.
