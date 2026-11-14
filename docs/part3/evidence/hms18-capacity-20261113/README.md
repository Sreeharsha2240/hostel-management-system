# Allocation-capacity regression and coverage refresh - 13 November 2026

Clean implementation `918477c2767161aa49526a57350a54eea0bd4c3e`, tree `76d2f64d5ad5ace8c6c2322c7823052600b23a72`, follows merged main `a41f884`. Devansh's allocation follow-up fixes admissions through available historical beds after shrinking a room. The model checks active count against the locked Room, excludes itself, and fails closed on a bed moved between lookup and lock. Full rooms disappear from creation choices; transfers discount only the departing source. ROOM_FULL/BED_MOVED return 409. Historical beds and physical-bed occupancy report semantics are preserved.

## Verification

All 12 gates passed on the clean implementation: 497 mixed methods, 496 PASS/one expected coverage timing SKIP; separate timing PASS. Nine owned integration recipes passed. Recovery safety 32, runner safety 7, harness contracts 6 and actionlint passed. The 15 new MySQL regression methods include one real two-student/different-bed race and one controlled same-transaction relocation interleaving; the latter is not evidence of arbitrary concurrent admin operations. Original red failures and subsequent green outcomes are retained in the four `.txt` logs, with raw/sanitized hashes in [verification.json](verification.json).

The retained 288 unit IDs pass on updated source at 952/955 function-body statements (99.69%); six additions give 294 PASS, 955/955 (100%), 955/1713 (55.75%) all-application statements, and 417/432 (96.53%) application branches. Both isolated runs have zero database attempts. The source-pinned unchanged harness excludes import/shared setup credit. Its raw generic scope-pending label remains untouched; the separate [owner decision](../hms19-function-body-boundary-20261113.md) supplies the accepted function-body interpretation. No declarations are credited retroactively. Application subtotal excludes only scripts; configured totals include scripts. The original coverage configuration/70% combined gate is unchanged.

## Durable evidence

- `scope-baseline.json` / `scope-expanded.json`: exact 288/294 IDs, additions and 179 canonical-LF pins; previous scopes remain unchanged.
- `measurement-baseline.json` / `measurement-expanded.json`: exact clean revision, environment, settings, commands, per-file full/body line sets, method branch totals and outcomes.
- `coverage-metrics.json` / `coverage-tables.md`: reconciled per-file/module line+arc inventories for both isolated runs and the mixed run; raw hashes and JUnit inventories.
- `mixed-coverage.json`, `checks-run.json`, `junit-summary.json`: mixed raw coverage, 12-gate manifest and 497 exact outcomes.
- `verification.json`: owned case outcomes, offline checks, independent-review corrections and retained attempts.

The tracked reports are [Code Coverage Report](../../Code_Coverage_Report.md), [Branch Coverage Report](../../Branch_Coverage_Report.md) and the refreshed Unit Test Report summary. Historical evidence is unchanged. Both Python CI jobs passed for publication candidate `eebb30afeb63d27618fdd3be4cc4c2b76392fc32`. The [independent CI extraction](ci-summary.json) verifies their actual checkout tree, source pins, exact outcomes, raw hashes and coverage. The commit publishing this record is a subsequent documentation update; current head checks are linked from PR #75.

Publication uses UTF-8 LF line endings as required by `.gitattributes`. Raw hashes identify the original runtime artifacts; published log hashes identify the sanitized LF copies. Normalized JSON preserves the original data.

## Reproduce

Install `requirements-dev.txt`, configure an isolated MySQL test account as in README, apply migrations to the disposable application database, and run serially from the repository root. Use new ignored output paths for every attempt.

```sh
python scripts/run_checks.py --output-dir test-results/capacity-clean-full
python docs/part3/evidence/hms19-unit-review-20261113/reproduce.py --scope docs/part3/evidence/hms18-capacity-20261113/scope-baseline.json --output-dir test-results/capacity-clean-units/baseline
python docs/part3/evidence/hms19-unit-review-20261113/reproduce.py --scope docs/part3/evidence/hms18-capacity-20261113/scope-expanded.json --output-dir test-results/capacity-clean-units/expanded
python scripts/part3/run_owned_regressions.py --output-dir test-results/capacity-clean-owned
python docs/part3/evidence/hms19-unit-review-20261113/test_reproduce.py
python -m unittest discover -s scripts/part3 -p test_issue40_recovery_safety.py -v
python -S -m unittest discover -s scripts/part3 -p test_owned_runner_safety.py -v
```

The harness refuses a changed pinned source. For a future implementation create a versioned successor scope with all prior exact IDs and fresh pins, retaining this snapshot. Do not edit historical pins or broaden unit credit to database regressions.

| Component | Measured version |
|---|---|
| Python | 3.14.7 |
| Platform | Windows-11-10.0.26200-SP0 |
| MySQL | 8.4.9 |
| Django | 5.2.18 |
| mysqlclient | 2.3.0 |
| python-dotenv | 1.2.4 |
| reportlab | 4.5.1 |
| pypdf | 6.21.2 |
| coverage | 7.16.2 |
| unittest-xml-reporting | 4.0.0 |
| ruff | 0.17.1 |

MySQL 8.4 is the recorded substitution for the plan's 8.0 baseline. This is technical evidence for the tested revision. Final named reviews/approvals, remaining browser/availability evidence or accepted deviations, instructor format/channel/cutoff, accepted submission SHA and actual receipt remain team responsibilities. Hostel admin relocation of already active beds is a separate existing module defect; the admission guard does not implement a new bed retirement/reassignment policy.
