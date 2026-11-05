# Current-candidate coverage evidence for #42

Measured 4 November 2026 at clean `6e349f2c07630e72b9151a575685d462e63cbc40` / tree `558190f7852283743ab9e20a4c9b3c9b99d0f806`. This evidence updates Devansh's Code and Branch Coverage Reports only. Current candidate; no independent teammate approval or accepted submission build is claimed. #41 owns the broader Test Plan unit classification; both coverage reports still require independent review.

- `coverage-metrics.json`: all measured files, executed/missing lines/arcs and module/configured/application subtotals for mixed, strict16 and proposed37; source/configuration/input hashes; unmeasured Python inventory; matching raw-artifact hashes and reexport checks.
- `coverage-mixed-run.json`, `coverage-strict16-run.json`, `coverage-proposed37-run.json`: sanitized original metadata/commands. Local repository paths are replaced with `<repository>`; exact original metadata hashes remain in the metrics.
- `coverage-junit-summary.json`: every method outcome in the 189-method mixed run, 16-method narrow diagnostic and 37-method proposed component diagnostic, plus the separate uninstrumented timing result.
- `coverage-unit-scope.json`: exact 16/37 method IDs and proposed 21-method addition; explicit nonexhaustive classification, Test Plan definition and startup attribution limit.

## Scope and interpretation

Strict16 is a narrow database-free diagnostic. Proposed37 adds 21 direct model/form component methods and is nonexhaustive. Test Plan section 5 explicitly permits Django TestCase model/form/view units; database use alone does not classify a method as integration. Both subsets omit startup/import/setup context while retaining full-file denominators, so declarations executed only at startup receive no subset credit. These diagnostics do not establish that all Test Plan units pass or fail the SRS 70% target.

The shared configured denominator is 1674 statements/392 outcomes across 51 files. The application subtotal removes only `scripts/run_checks.py`, retaining 1579 statements/378 outcomes. No omissions or thresholds changed. All 49 nonempty unique XML rows match JSON lines and branch counts. Working-file SHA-256 binds exact executed bytes; Git blob IDs bind normalized committed contents. 23 inventoried inputs differ only by CRLF/LF, and every input was compared with the tested commit.

## Reproduction and reconciliation

Run one Django/MySQL suite at a time, with synthetic fixtures and the documented environment. Choose a new ignored output directory; preserve older evidence. Full checks:

```powershell
python scripts/run_checks.py --output-dir test-results/owned-defects/<new-run>/checks
```

For each diagnostic, copy `.coveragerc` to that new diagnostic output and add only `dynamic_context = test_function` under `[run]` and its selected test-name contexts under `[report]`. The exact configurations and execution argument lists are retained in the metrics/run JSON. Set `COVERAGE_FILE` and `HMS_TEST_OUTPUT_DIR` to the new diagnostic data/JUnit paths in a separate shell. Strict16 selects the three helper modules; proposed37 selects those plus the exact 21 methods in `coverage-unit-scope.json`. Export JSON with `--show-contexts --fail-under=0`, and export XML through `scripts/run_checks.py --coverage-xml <output>/coverage.xml`, using `COVERAGE_RCFILE` for the diagnostic configuration. Ordinary XML export can incorrectly retain startup statement hits; the helper explicitly filters query contexts and preserves repository-relative class paths.

Verify all 16/37 selected method IDs against JUnit; measured runtime contexts must be a subset of that selection. This candidate observes 16/34 contexts; methods without measured runtime contexts are explicitly inventoried and receive no inferred coverage. Exclude empty startup context and preserve every measured file's original statement/branch denominator. Diagnostic `--fail-under=0` only retains low observations. The actual repository gate remains 70% combined and is checked by the full run.

Before generating these reports, the private generator loaded each original `.coverage` read-only, reexported JSON/XML, and compared every measured file/line/arc/total plus the selected context sets. Matching XML root totals, unique class paths, executed/missing line sets and per-file branch counts were checked; JUnit sums/method IDs and all recorded command exits were reconciled. No tests or database operations were performed by the generator. Raw data/XML/JSON/JUnit/logs remain in ignored test outputs; only sanitized metadata, synthetic method names, counts and hashes are retained here. Historical JSON in `evidence/issue42` is unchanged; its README now clarifies the earlier scope's methodological limits.
