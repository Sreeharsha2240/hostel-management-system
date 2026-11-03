# Branch Coverage Report

Owner: Devansh Gupta (`DevaOnL`), [issue #42](https://github.com/Sreeharsha2240/hostel-management-system/issues/42). Measured **3 November 2026**.

Tested candidate commit: `bf70f53e10fecdfdc34e2e63bb33590b0990eb40`; tree: `6fa3a7a6614d3f79d6e56e70eb92c807c805f3c5`; **clean working tree at both executions**. The reports/evidence are later documentation-only additions; they do not relabel the measurement commit. The [source manifest](evidence/issue42/coverage-metrics.json) binds every tracked Python input, test, coverage configuration, requirements file and CI workflow to that tested commit. PR #44 remains awaiting independent acceptance. These are candidate measurements, not an approved submission build.

Environment: Windows-11-10.0.26200-SP0, Python **3.14.7**, Django **5.2.18**, coverage.py **7.16.2**, mysqlclient **2.3.0**, MySQL **8.4.9**, unittest-xml-reporting **4.0.0**, Ruff **0.17.1**. MySQL 8.4 is a documented substitution for the original Test Plan's 8.0 baseline, pending team acceptance. Only synthetic fixtures and Django's disposable `test_hms` are used; live `hms` is neither populated nor restored by these runs.

Both reports use the **same mixed run and separately attributed unit run**. Durable [metrics/source inventory](evidence/issue42/coverage-metrics.json), [mixed run](evidence/issue42/mixed-run.json), [unit run](evidence/issue42/unit-run.json), [JUnit summary](evidence/issue42/junit-summary.json), [unit classification](evidence/issue42/unit-scope.json) and [reproduction/extraction notes](evidence/issue42/README.md) retain definitions, commands and raw-artifact hashes. Raw `.coverage`, XML, JSON and JUnit files are retained privately and reconciled before publishing sanitized evidence.

## Result and definitions

The mixed suite covers **336/392 branch outcomes (85.71%)**, with **56 missing outcomes**. Of those, **52 missing outcomes originate on executed lines** (coverage.py's `num_partial_branches`); the other 4 originate on unexecuted lines. Partial outcomes are a subset of missing outcomes and are not added to the denominator. A source line can have more than one missing outcome. The application subtotal is **324/378 (85.71%)**.

A branch is a measured source-to-destination outcome, not a count of `if` statements. `source -> destination` below denotes an unobserved arc; `exit@N` is coverage.py's negative destination for leaving the code object starting at line N. A file with no measured branch outcomes has **N/A**, not an invented 100%. No `pragma: no cover`/`no branch` exclusions were introduced; all measured files report zero excluded statements.

## Measurement scope

`.coveragerc` enables branch measurement for `accounts,allocations,audit,hms,hostels,payments,reports,scripts,students`. It omits `*/migrations/*`, `*/tests.py`, `*/test_*.py`, `*/apps.py`, `*/__init__.py`, `*/settings.py`, `*/asgi.py`, `*/wsgi.py`. These exclude generated schema history, tests, registration/bootstrap and environment configuration from this application-code measure; they do not waive testing of those behaviors. Empty `reports/admin.py` and `reports/models.py` have zero denominators and N/A rates.

This issue fixes the runner's XML-only export to retain repository-relative package names. Previously, identical filenames across package source roots overwrote class rows: 17 XML entries could not represent the 49 nonempty files despite correct root totals. The corrected export has all 49 unique file rows, each reconciled to JSON. `.coveragerc` and its collection source list, omission patterns, branch setting and 70% gate are unchanged. The application denominator is unchanged; the modified verification tooling has its own measured subtotal. No application code changed.

Coverage.py discovers **51 files**, including `scripts/run_checks.py` tooling. The application subtotal retains all 50 files in the eight application packages, including admin/URL declarations; only the tooling file is removed from that subtotal. The denominator is conservative and explicitly defined, not a claim that every Python declaration is business logic. `manage.py`, test factories, JavaScript/JMX, templates/static files, SQL and `scripts/part3` (not discovered by this source scan because its namespace directories lack `__init__.py`) are outside this measured scope; the full unmeasured Python inventory states why each file is absent. Browser/load/recovery evidence is separate and adds no coverage credit. No new exclusions or artificial tests were added to raise percentages.

## Test execution

The complete suite discovered **187 methods**: **186 passed**, zero failures/errors, and one intentional timing skip while tracing. The skipped login/dashboard response check then **passed separately without tracing**, contributing no additional coverage. All **12 repository gates passed**. These are mixed unit/component/integration/concurrency/system checks, not 187 unit tests or proof of all planned cases. The isolated run passed **16/16**, with no skips and no database queries. Details and expected/actual method outcomes are in the JUnit summary. No application failure was found by these runs; the XML tooling defect was fixed and actual coverage gaps remain below.

## Mixed-suite branch coverage by module

| Module | Measured outcomes | Covered | Missing | Partial missing outcomes | Branch coverage |
|---|---:|---:|---:|---:|---:|
| accounts | 68 | 55 | 13 | 13 | 80.88% |
| allocations | 92 | 72 | 20 | 20 | 78.26% |
| audit | 26 | 23 | 3 | 3 | 88.46% |
| hms | 26 | 23 | 3 | 3 | 88.46% |
| hostels | 58 | 50 | 8 | 4 | 86.21% |
| payments | 54 | 49 | 5 | 5 | 90.74% |
| reports | 20 | 20 | 0 | 0 | 100.00% |
| scripts | 14 | 12 | 2 | 2 | 85.71% |
| students | 34 | 32 | 2 | 2 | 94.12% |
| **Configured total** | 392 | 336 | 56 | 52 | 85.71% |
| **Application subtotal (excludes scripts)** | 378 | 324 | 54 | 50 | 85.71% |

## Per-file branch outcomes and remaining paths

Line numbers refer to the exact tested source. These paths were not covered by this instrumented suite; browser/manual runs do not silently fill these gaps.

| File | Measured | Covered | Missing | Partial | Branch coverage | Missing arcs |
|---|---:|---:|---:|---:|---:|---|
| [accounts/admin.py](../../accounts/admin.py) | 0 | 0 | 0 | 0 | N/A | none |
| [accounts/backends.py](../../accounts/backends.py) | 12 | 10 | 2 | 2 | 83.33% | 18 -> 19; 33 -> 34 |
| [accounts/decorators.py](../../accounts/decorators.py) | 8 | 8 | 0 | 0 | 100.00% | none |
| [accounts/forms.py](../../accounts/forms.py) | 6 | 4 | 2 | 2 | 66.67% | 18 -> 19; 28 -> 30 |
| [accounts/middleware.py](../../accounts/middleware.py) | 2 | 2 | 0 | 0 | 100.00% | none |
| [accounts/models.py](../../accounts/models.py) | 4 | 3 | 1 | 1 | 75.00% | 29 -> 30 |
| [accounts/urls.py](../../accounts/urls.py) | 0 | 0 | 0 | 0 | N/A | none |
| [accounts/validators.py](../../accounts/validators.py) | 2 | 2 | 0 | 0 | 100.00% | none |
| [accounts/views.py](../../accounts/views.py) | 34 | 26 | 8 | 8 | 76.47% | 23 -> 24; 77 -> 96; 87 -> 96; 136 -> 146; 138 -> 147; 139 -> 144; 158 -> 159; 160 -> 166 |
| [allocations/admin.py](../../allocations/admin.py) | 0 | 0 | 0 | 0 | N/A | none |
| [allocations/forms.py](../../allocations/forms.py) | 0 | 0 | 0 | 0 | N/A | none |
| [allocations/models.py](../../allocations/models.py) | 40 | 33 | 7 | 7 | 82.50% | 82 -> 83; 84 -> 85; 91 -> 94; 97 -> 98; 101 -> 102; 137 -> 138; 151 -> 152 |
| [allocations/services.py](../../allocations/services.py) | 6 | 5 | 1 | 1 | 83.33% | 53 -> 54 |
| [allocations/urls.py](../../allocations/urls.py) | 0 | 0 | 0 | 0 | N/A | none |
| [allocations/views.py](../../allocations/views.py) | 46 | 34 | 12 | 12 | 73.91% | 38 -> 40; 41 -> 43; 61 -> 62; 69 -> 70; 99 -> 100; 116 -> 123; 137 -> 159; 140 -> 142; 147 -> 149; 156 -> 160; 174 -> 195; 193 -> 195 |
| [audit/admin.py](../../audit/admin.py) | 0 | 0 | 0 | 0 | N/A | none |
| [audit/management/commands/purge_audit_logs.py](../../audit/management/commands/purge_audit_logs.py) | 4 | 4 | 0 | 0 | 100.00% | none |
| [audit/mixins.py](../../audit/mixins.py) | 4 | 4 | 0 | 0 | 100.00% | none |
| [audit/models.py](../../audit/models.py) | 6 | 5 | 1 | 1 | 83.33% | 19 -> 21 |
| [audit/services.py](../../audit/services.py) | 4 | 4 | 0 | 0 | 100.00% | none |
| [audit/signals.py](../../audit/signals.py) | 4 | 2 | 2 | 2 | 50.00% | 22 -> 24; 34 -> exit@32 |
| [audit/urls.py](../../audit/urls.py) | 0 | 0 | 0 | 0 | N/A | none |
| [audit/views.py](../../audit/views.py) | 4 | 4 | 0 | 0 | 100.00% | none |
| [hms/decorators.py](../../hms/decorators.py) | 2 | 1 | 1 | 1 | 50.00% | 17 -> 19 |
| [hms/forms.py](../../hms/forms.py) | 4 | 4 | 0 | 0 | 100.00% | none |
| [hms/http.py](../../hms/http.py) | 14 | 14 | 0 | 0 | 100.00% | none |
| [hms/responses.py](../../hms/responses.py) | 6 | 4 | 2 | 2 | 66.67% | 22 -> 23; 31 -> 37 |
| [hms/urls.py](../../hms/urls.py) | 0 | 0 | 0 | 0 | N/A | none |
| [hostels/admin.py](../../hostels/admin.py) | 2 | 0 | 2 | 0 | 0.00% | 26 -> 27; 26 -> 32 |
| [hostels/forms.py](../../hostels/forms.py) | 4 | 3 | 1 | 1 | 75.00% | 52 -> 53 |
| [hostels/models.py](../../hostels/models.py) | 26 | 22 | 4 | 2 | 84.62% | 38 -> 43; 157 -> 158; 166 -> exit@113; 166 -> 167 |
| [hostels/urls.py](../../hostels/urls.py) | 0 | 0 | 0 | 0 | N/A | none |
| [hostels/views.py](../../hostels/views.py) | 26 | 25 | 1 | 1 | 96.15% | 123 -> 124 |
| [payments/admin.py](../../payments/admin.py) | 0 | 0 | 0 | 0 | N/A | none |
| [payments/forms.py](../../payments/forms.py) | 0 | 0 | 0 | 0 | N/A | none |
| [payments/models.py](../../payments/models.py) | 22 | 20 | 2 | 2 | 90.91% | 94 -> 96; 118 -> 123 |
| [payments/receipts.py](../../payments/receipts.py) | 2 | 2 | 0 | 0 | 100.00% | none |
| [payments/services.py](../../payments/services.py) | 4 | 4 | 0 | 0 | 100.00% | none |
| [payments/urls.py](../../payments/urls.py) | 0 | 0 | 0 | 0 | N/A | none |
| [payments/views.py](../../payments/views.py) | 26 | 23 | 3 | 3 | 88.46% | 42 -> 43; 91 -> 97; 94 -> 96 |
| [reports/admin.py](../../reports/admin.py) | 0 | 0 | 0 | 0 | N/A | none |
| [reports/models.py](../../reports/models.py) | 0 | 0 | 0 | 0 | N/A | none |
| [reports/services.py](../../reports/services.py) | 6 | 6 | 0 | 0 | 100.00% | none |
| [reports/urls.py](../../reports/urls.py) | 0 | 0 | 0 | 0 | N/A | none |
| [reports/views.py](../../reports/views.py) | 14 | 14 | 0 | 0 | 100.00% | none |
| [scripts/run_checks.py](../../scripts/run_checks.py) | 14 | 12 | 2 | 2 | 85.71% | 162 -> 167; 249 -> 250 |
| [students/admin.py](../../students/admin.py) | 0 | 0 | 0 | 0 | N/A | none |
| [students/forms.py](../../students/forms.py) | 6 | 6 | 0 | 0 | 100.00% | none |
| [students/models.py](../../students/models.py) | 8 | 7 | 1 | 1 | 87.50% | 9 -> 13 |
| [students/urls.py](../../students/urls.py) | 0 | 0 | 0 | 0 | N/A | none |
| [students/views.py](../../students/views.py) | 20 | 19 | 1 | 1 | 95.00% | 158 -> 159 |

## Meaning of the remaining gaps

- Authentication/account gaps include missing credentials, a password changing during row-lock acquisition, optional/deferred form saves, and account/profile response alternatives.
- Allocation gaps include direct model date/status guards, inactive-hostel rejection, same-bed transfer rejection, and HTML/JSON/filter/error response alternatives.
- Audit gaps include upsert/conflict handling and login/logout signal alternatives; hostel gaps include admin bulk operations and capacity changes.
- Payment gaps include correction validation and response/filter alternatives; student gaps include a queryset status-update path and already-inactive handling.
- The two tooling gaps in `scripts/run_checks.py` are XML export without a configured context filter and the process-entry path. Both are distinct from application behavior.

The per-file arcs are the authoritative gap list. These observations do not justify waiving a path or asking other contributors to implement tests within this issue. Owners/QA can review risks under #41/#37. No additional tests, production changes, omissions or thresholds were introduced to inflate coverage.

## Unit attribution, gate and acceptance

The separately attributed conservative unit subset covers **16/378 application branch outcomes (4.23%)**, with startup/import context excluded and the full application denominator retained. Its application statement result is **31/1579 (1.96%)**. The SRS requires unit tests to cover at least 70% of application logic; this proposal does not establish that target and awaits #41's classification review. See the separate [Code Coverage Report](Code_Coverage_Report.md) for method classification and statement assessment.

The repository gate is **70% combined statements/branches**, calculated as `(1580 + 336) / (1674 + 392) = 92.74%` and passed. It is neither a 70% standalone branch target nor proof of the SRS unit criterion. **The Part 3 PDF specifies no separate branch threshold.**

The original 94.28% statement / 85.57% branch / 92.63% combined PR #36 setup figures remain a historical baseline; the tables above are fresh measurements. Coverage does not establish system/RTM acceptance, assertion quality or no defects. Independent teammate review of both reports, the #41 unit scope, and the accepted submission build remain pending. Rerun on source changes. The Unit Test Report, System Validation Report and final approvals remain with their assigned owners.
