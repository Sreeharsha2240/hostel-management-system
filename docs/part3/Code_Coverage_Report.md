# Code Coverage Report

Owner: Devansh Gupta (`DevaOnL`), [issue #42](https://github.com/Sreeharsha2240/hostel-management-system/issues/42). Measured **3 November 2026**.

Tested candidate commit: `bf70f53e10fecdfdc34e2e63bb33590b0990eb40`; tree: `6fa3a7a6614d3f79d6e56e70eb92c807c805f3c5`; **clean working tree at both executions**. The reports/evidence are later documentation-only additions; they do not relabel the measurement commit. The [source manifest](evidence/issue42/coverage-metrics.json) binds every tracked Python input, test, coverage configuration, requirements file and CI workflow to that tested commit. PR #44 remains awaiting independent acceptance. These are candidate measurements, not an approved submission build.

Environment: Windows-11-10.0.26200-SP0, Python **3.14.7**, Django **5.2.18**, coverage.py **7.16.2**, mysqlclient **2.3.0**, MySQL **8.4.9**, unittest-xml-reporting **4.0.0**, Ruff **0.17.1**. MySQL 8.4 is a documented substitution for the original Test Plan's 8.0 baseline, pending team acceptance. Only synthetic fixtures and Django's disposable `test_hms` are used; live `hms` is neither populated nor restored by these runs.

Both reports use the **same mixed run and separately attributed unit run**. Durable [metrics/source inventory](evidence/issue42/coverage-metrics.json), [mixed run](evidence/issue42/mixed-run.json), [unit run](evidence/issue42/unit-run.json), [JUnit summary](evidence/issue42/junit-summary.json), [unit classification](evidence/issue42/unit-scope.json) and [reproduction/extraction notes](evidence/issue42/README.md) retain definitions, commands and raw-artifact hashes. Raw `.coverage`, XML, JSON and JUnit files are retained privately and reconciled before publishing sanitized evidence.

## Result and interpretation

The mixed suite executes **1580/1674 statements (94.38%)**, leaving **94** missing. The application-only subtotal is **1501/1579 (95.06%)**.

**The SRS unit-test target is not established.** Under the proposed conservative isolated-unit classification, selected tests execute **31/1579 application statements (1.96%)**, below 70%. This measured subset is not a final team-approved classification or a definitive rejection of another justified Test Plan classification. #41 must review it and obtain separately attributable evidence for any broader agreed unit scope; the high mixed-suite figure cannot substitute for that evidence.

## Measurement scope

`.coveragerc` enables branch measurement for `accounts,allocations,audit,hms,hostels,payments,reports,scripts,students`. It omits `*/migrations/*`, `*/tests.py`, `*/test_*.py`, `*/apps.py`, `*/__init__.py`, `*/settings.py`, `*/asgi.py`, `*/wsgi.py`. These exclude generated schema history, tests, registration/bootstrap and environment configuration from this application-code measure; they do not waive testing of those behaviors. Empty `reports/admin.py` and `reports/models.py` have zero denominators and N/A rates.

This issue fixes the runner's XML-only export to retain repository-relative package names. Previously, identical filenames across package source roots overwrote class rows: 17 XML entries could not represent the 49 nonempty files despite correct root totals. The corrected export has all 49 unique file rows, each reconciled to JSON. `.coveragerc` and its collection source list, omission patterns, branch setting and 70% gate are unchanged. The application denominator is unchanged; the modified verification tooling has its own measured subtotal. No application code changed.

Coverage.py discovers **51 files**, including `scripts/run_checks.py` tooling. The application subtotal retains all 50 files in the eight application packages, including admin/URL declarations; only the tooling file is removed from that subtotal. The denominator is conservative and explicitly defined, not a claim that every Python declaration is business logic. `manage.py`, test factories, JavaScript/JMX, templates/static files, SQL and `scripts/part3` (not discovered by this source scan because its namespace directories lack `__init__.py`) are outside this measured scope; the full unmeasured Python inventory states why each file is absent. Browser/load/recovery evidence is separate and adds no coverage credit. No new exclusions or artificial tests were added to raise percentages.

## Test execution

The complete suite discovered **187 methods**: **186 passed**, zero failures/errors, and one intentional timing skip while tracing. The skipped login/dashboard response check then **passed separately without tracing**, contributing no additional coverage. All **12 repository gates passed**. These are mixed unit/component/integration/concurrency/system checks, not 187 unit tests or proof of all planned cases. The isolated run passed **16/16**, with no skips and no database queries. Details and expected/actual method outcomes are in the JUnit summary. No application failure was found by these runs; the XML tooling defect was fixed and actual coverage gaps remain below.

## Mixed-suite statement coverage by module

| Module | Measured | Executed | Missing | Statement coverage |
|---|---:|---:|---:|---:|
| accounts | 271 | 260 | 11 | 95.94% |
| allocations | 303 | 277 | 26 | 91.42% |
| audit | 158 | 152 | 6 | 96.20% |
| hms | 79 | 76 | 3 | 96.20% |
| hostels | 255 | 236 | 19 | 92.55% |
| payments | 256 | 245 | 11 | 95.70% |
| reports | 86 | 86 | 0 | 100.00% |
| scripts | 95 | 79 | 16 | 83.16% |
| students | 171 | 169 | 2 | 98.83% |
| **Configured total** | 1674 | 1580 | 94 | 94.38% |
| **Application subtotal (excludes scripts)** | 1579 | 1501 | 78 | 95.06% |

## Per-file statements and actual gaps

Line numbers refer to the tested commit. Missing statements are observations, not proof that paths are unreachable. Full executed/missing sets are retained in the metrics JSON.

| File | Measured | Executed | Missing | Statement coverage | Missing lines |
|---|---:|---:|---:|---:|---|
| [accounts/admin.py](../../accounts/admin.py) | 23 | 20 | 3 | 86.96% | 26, 29, 35 |
| [accounts/backends.py](../../accounts/backends.py) | 36 | 34 | 2 | 94.44% | 19, 34 |
| [accounts/decorators.py](../../accounts/decorators.py) | 22 | 22 | 0 | 100.00% | none |
| [accounts/forms.py](../../accounts/forms.py) | 38 | 37 | 1 | 97.37% | 19 |
| [accounts/middleware.py](../../accounts/middleware.py) | 10 | 10 | 0 | 100.00% | none |
| [accounts/models.py](../../accounts/models.py) | 20 | 19 | 1 | 95.00% | 30 |
| [accounts/urls.py](../../accounts/urls.py) | 3 | 3 | 0 | 100.00% | none |
| [accounts/validators.py](../../accounts/validators.py) | 8 | 8 | 0 | 100.00% | none |
| [accounts/views.py](../../accounts/views.py) | 111 | 107 | 4 | 96.40% | 24, 146-147, 159 |
| [allocations/admin.py](../../allocations/admin.py) | 12 | 9 | 3 | 75.00% | 20, 23, 26 |
| [allocations/forms.py](../../allocations/forms.py) | 13 | 13 | 0 | 100.00% | none |
| [allocations/models.py](../../allocations/models.py) | 96 | 86 | 10 | 89.58% | 83, 85, 94, 98, 102, 122-123, 138, 152, 212 |
| [allocations/services.py](../../allocations/services.py) | 47 | 46 | 1 | 97.87% | 54 |
| [allocations/urls.py](../../allocations/urls.py) | 3 | 3 | 0 | 100.00% | none |
| [allocations/views.py](../../allocations/views.py) | 132 | 120 | 12 | 90.91% | 40, 43, 62, 70, 100, 149, 152, 154-155, 159-160, 195 |
| [audit/admin.py](../../audit/admin.py) | 17 | 13 | 4 | 76.47% | 16, 19, 22, 25 |
| [audit/management/commands/purge_audit_logs.py](../../audit/management/commands/purge_audit_logs.py) | 19 | 19 | 0 | 100.00% | none |
| [audit/mixins.py](../../audit/mixins.py) | 23 | 23 | 0 | 100.00% | none |
| [audit/models.py](../../audit/models.py) | 50 | 48 | 2 | 96.00% | 21, 92 |
| [audit/services.py](../../audit/services.py) | 8 | 8 | 0 | 100.00% | none |
| [audit/signals.py](../../audit/signals.py) | 19 | 19 | 0 | 100.00% | none |
| [audit/urls.py](../../audit/urls.py) | 3 | 3 | 0 | 100.00% | none |
| [audit/views.py](../../audit/views.py) | 19 | 19 | 0 | 100.00% | none |
| [hms/decorators.py](../../hms/decorators.py) | 15 | 14 | 1 | 93.33% | 19 |
| [hms/forms.py](../../hms/forms.py) | 13 | 13 | 0 | 100.00% | none |
| [hms/http.py](../../hms/http.py) | 32 | 32 | 0 | 100.00% | none |
| [hms/responses.py](../../hms/responses.py) | 15 | 13 | 2 | 86.67% | 23, 37 |
| [hms/urls.py](../../hms/urls.py) | 4 | 4 | 0 | 100.00% | none |
| [hostels/admin.py](../../hostels/admin.py) | 42 | 34 | 8 | 80.95% | 25-27, 30-32, 43, 54 |
| [hostels/forms.py](../../hostels/forms.py) | 29 | 28 | 1 | 96.55% | 53 |
| [hostels/models.py](../../hostels/models.py) | 92 | 86 | 6 | 93.48% | 43, 158, 160, 166-167, 173 |
| [hostels/urls.py](../../hostels/urls.py) | 3 | 3 | 0 | 100.00% | none |
| [hostels/views.py](../../hostels/views.py) | 89 | 85 | 4 | 95.51% | 124-126, 131 |
| [payments/admin.py](../../payments/admin.py) | 14 | 11 | 3 | 78.57% | 14, 17, 20 |
| [payments/forms.py](../../payments/forms.py) | 18 | 18 | 0 | 100.00% | none |
| [payments/models.py](../../payments/models.py) | 80 | 74 | 6 | 92.50% | 88, 123, 126-127, 150-151 |
| [payments/receipts.py](../../payments/receipts.py) | 21 | 21 | 0 | 100.00% | none |
| [payments/services.py](../../payments/services.py) | 29 | 29 | 0 | 100.00% | none |
| [payments/urls.py](../../payments/urls.py) | 3 | 3 | 0 | 100.00% | none |
| [payments/views.py](../../payments/views.py) | 91 | 89 | 2 | 97.80% | 43, 96 |
| [reports/admin.py](../../reports/admin.py) | 0 | 0 | 0 | N/A | none |
| [reports/models.py](../../reports/models.py) | 0 | 0 | 0 | N/A | none |
| [reports/services.py](../../reports/services.py) | 26 | 26 | 0 | 100.00% | none |
| [reports/urls.py](../../reports/urls.py) | 4 | 4 | 0 | 100.00% | none |
| [reports/views.py](../../reports/views.py) | 56 | 56 | 0 | 100.00% | none |
| [scripts/run_checks.py](../../scripts/run_checks.py) | 95 | 79 | 16 | 83.16% | 35-36, 39-41, 46-48, 50-51, 53-56, 58, 250 |
| [students/admin.py](../../students/admin.py) | 9 | 9 | 0 | 100.00% | none |
| [students/forms.py](../../students/forms.py) | 27 | 27 | 0 | 100.00% | none |
| [students/models.py](../../students/models.py) | 46 | 45 | 1 | 97.83% | 13 |
| [students/urls.py](../../students/urls.py) | 3 | 3 | 0 | 100.00% | none |
| [students/views.py](../../students/views.py) | 86 | 85 | 1 | 98.84% | 159 |

## Separately attributable unit coverage and SRS 6.4

SRS 6.4 states: **"unit tests cover at least 70% of the application logic."** The original Test Plan names model/form/view unit testing, but the existing model/view tests use real ORM persistence, transactions and database-dependent setup. This report conservatively separates those component/integration checks from isolated units rather than classifying by filename or `TestCase` inheritance.

| Proposed category | Methods | Included scope |
|---|---:|---|
| Isolated application unit | 16 | `hms.test_forms` (3), `hms.test_http` (10), `hms.test_responses` (3) |
| Settings configuration | 1 | `hms.test_settings` |
| Verification tooling | 8 | `tests.test_checks` |
| Database/component/integration/concurrency/system | 162 | Other normal-suite methods; includes the intended timing skip |

Only the 16 `SimpleTestCase` methods directly exercising validation/parser/response helpers are selected. Database access is prohibited. `dynamic_context = test_function` and a test-name filter exclude the empty startup/import/setup context, while retaining the **same full-file denominator**. All 16 expected contexts are verified. Coverage of just the three exercised files is not used as the SRS denominator. Module declarations executed only at Django startup receive no unit credit.

| Module | Measured application statements | Unit-executed | Missing from unit execution | Unit statement coverage |
|---|---:|---:|---:|---:|
| accounts | 271 | 0 | 271 | 0.00% |
| allocations | 303 | 0 | 303 | 0.00% |
| audit | 158 | 0 | 158 | 0.00% |
| hms | 79 | 31 | 48 | 39.24% |
| hostels | 255 | 0 | 255 | 0.00% |
| payments | 256 | 0 | 256 | 0.00% |
| reports | 86 | 0 | 86 | 0.00% |
| students | 171 | 0 | 171 | 0.00% |
| **Application subtotal** | 1579 | 31 | 1548 | 1.96% |

## Gate, limitations and next review

The unchanged repository `fail_under = 70` gate combines statements and branch outcomes: `(1580 + 336) / (1674 + 392) = 92.74%`. It **passed**. This is distinct from 94.38% statement coverage, 85.71% branch coverage, and the SRS unit requirement. Unit diagnostic exports explicitly use `--fail-under=0` to save low results; that extraction success is not a passing threshold.

PR #36's setup baseline (94.28% statements / 85.57% branches / 92.63% combined) is historical only. These numbers come from the fresh 3 November run. Coverage measures execution, not assertion quality, requirement coverage or absence of defects. Report/build acceptance and the proposed unit scope await independent teammate review in #41/#42; final accepted-build source changes require a matching rerun. Unit Test Report (#41), System Validation Report (#38), RTM (#37) and final approvals (#43) remain with their owners. See the separate [Branch Coverage Report](Branch_Coverage_Report.md).
