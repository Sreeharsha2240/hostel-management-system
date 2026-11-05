# Issue #42 coverage evidence

This directory preserves the 3 November measurements of `bf70f53`. Current
reports use the [4 November follow-up evidence](../owned-defects/README.md).
The strict 16-method database-free subset here is a narrow diagnostic: the
submitted Test Plan also permits model/form/view component units. Its 1.96%
result does not classify or measure all Test Plan units. The broader
classification and SRS target remain subject to #41/#42 review.

These sanitized metrics support the separate [Code Coverage Report](../../Code_Coverage_Report.md) and [Branch Coverage Report](../../Branch_Coverage_Report.md). Both refer to clean candidate `bf70f53e10fecdfdc34e2e63bb33590b0990eb40` / tree `6fa3a7a6614d3f79d6e56e70eb92c807c805f3c5` on 3 November 2026. They are not teammate approval or an accepted submission build.

- `coverage-metrics.json`: complete measured file summaries, executed/missing statements and branch arcs for both scopes; module/total/application subtotals; exact configuration; all tracked Python/configuration input hashes; unmeasured Python inventory and matching private artifact hashes.
- `mixed-run.json`: sanitized original 12-gate runner metadata, versions, command arguments and results. `<repository>` replaces only the local absolute path; original raw file hash is retained in the metrics.
- `unit-run.json`: separate 16-method run, context selection, extraction commands and the XML-context correction.
- `junit-summary.json`: all 187 mixed and 16 isolated test-method outcomes, including the intended timing skip and separate uninstrumented PASS.
- `unit-scope.json`: proposed per-level classification and all 16 selected contexts for #41 review. The 1.96% application statement observation is below 70%; neither mixed coverage nor export exit 0 proves the SRS unit target.

Source-manifest `sha256` values describe exact executed Windows working-file bytes; `git_blob` values identify committed Git-normalized content. 23 inputs differ only by CRLF/LF line endings. Every input is checked against the tested commit after newline normalization; no other content differences are present. These are two distinct hash semantics, not a claim that a working-file SHA equals a Git object ID.

## Reproduce serially

Use the documented MySQL environment, Python requirements and synthetic Django fixtures. Run one Django/database suite at a time. Choose a **new ignored directory** for every run; do not overwrite prior evidence. The original run output was `test-results/issue42/20261103T121538608463Z/`.

```powershell
python scripts/run_checks.py --output-dir test-results/issue42/<new-run>/checks
```

This produces matching `.coverage`, JSON/XML, JUnit, 12 step logs and `run.json`. Verify all gates, failures/skips and the separate timing pass. Re-export the same `.coverage` with coverage.py and compare per-file lines/arcs/totals; JSON context-list ordering is immaterial. Check XML `lines-valid`, `lines-covered`, `branches-valid`, `branches-covered` and JUnit sums against those same metrics. Source/hash comparisons are required before reusing a run for #41. Only one suite used the shared MySQL test database at a time.

Run the isolated commands in a separate shell and close it afterward so diagnostic environment variables cannot affect a later mixed run. Copy `.coveragerc` into the new ignored unit output, adding **only** `dynamic_context = test_function` under `[run]` and the following under `[report]`:

```ini
contexts = ^hms\.test_(forms|http|responses)\..*\.test_
```

Set `COVERAGE_FILE` to that output's `.coverage` and `HMS_TEST_OUTPUT_DIR` to its `junit/`. Run:

```powershell
python -m coverage run --rcfile <unit-config> manage.py test hms.test_forms hms.test_http hms.test_responses --noinput --testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner
python -m coverage json --rcfile <unit-config> --show-contexts --fail-under=0 -o <unit-output>/coverage.json
python -m coverage report --rcfile <unit-config> --fail-under=0
```

Verify all 16 expected test contexts match `unit-scope.json`; the empty startup/import/setup context must not contribute. Preserve the same 51 measured files and 1,674-statement/392-outcome denominator. Application-only subtotal removes only `scripts/run_checks.py`, retaining 1,579 statements/378 outcomes. Do not reduce it to the three exercised helper files. `--fail-under=0` retains a diagnostic low result; it does not alter `.coveragerc` or satisfy a coverage gate.

## XML extraction correction and preserved diagnostics

coverage.py 7.16.2's XML CLI accepts no `--contexts` argument; the first attempted export failed with exit 1 after passing tests. A rerun using report contexts produced correctly filtered JSON/text, but CLI XML still credited **742 startup-inclusive statements**, inconsistent with **31** in filtered JSON. Its branch total was already filtered. Both diagnostic attempts remain private, and neither supplies the final unit XML metric.

From the repository root, export the final XML from the same raw unit data with the fixed helper. Keep `COVERAGE_FILE` set to the unit data and set `COVERAGE_RCFILE` to the context configuration:

```powershell
$env:COVERAGE_RCFILE = "<unit-config>"
python scripts/run_checks.py --coverage-xml <unit-output>/coverage.xml
```

The XML export sets repository-root source paths **only after loading the originally scoped data**, and reconciles all 49 nonempty file rows to the filtered JSON. The runner's equivalent XML-only helper fixes the earlier 17-row filename collision; `.coveragerc` and its collection scope/omissions/gate remain unchanged. Both final exports reconcile every file's executed/missing line set, not only root totals. Original diagnostics remain private and their correction is recorded in the metrics. The initial export error is a tooling/extraction failure, not an application-test failure.

## Limits and review handoff

The complete mixed suite passed 186 methods, skipped one timing method under tracing, then passed that one without tracing. All 16 isolated methods passed. No application failures were observed; the XML tooling defect was fixed and uncovered lines/arcs are retained, not excused. Scope omits generated migrations, test files and bootstrap/configuration; `scripts/part3`, JavaScript/JMX, templates and other non-Python content are unmeasured. These reports do not rerun or accept the complete Test Plan.

All raw `.coverage`, JSON/XML/JUnit files and diagnostic logs are kept under ignored test results. Only selected source paths, aggregate/results metadata, hashes and synthetic method labels are published; no credentials, student records, SQL dumps or private connection settings are included. Existing CI artifacts expire after 30 days and are supplementary; these repository metrics are durable. #41 can reuse this exact source-bound mixed run and classification proposal for its own report. #37/#38/#41/#43 ownership and independent teammate acceptance remain unchanged.
