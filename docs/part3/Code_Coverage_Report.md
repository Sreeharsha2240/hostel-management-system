# Code Coverage Report

Owner: Devansh Gupta (`DevaOnL`), [issue #42](https://github.com/Sreeharsha2240/hostel-management-system/issues/42). Measured **4 November 2026**.

Tested current candidate: `6e349f2c07630e72b9151a575685d462e63cbc40`; tree: `558190f7852283743ab9e20a4c9b3c9b99d0f806`; **clean working tree at all three executions**. Documentation/evidence additions follow the measurement and do not relabel its commit. Current candidate; no independent teammate approval or accepted submission build is claimed. #41 owns the broader Test Plan unit classification; both coverage reports still require independent review.

Environment: Windows-11-10.0.26200-SP0, Python **3.14.7**, Django **5.2.18**, coverage.py **7.16.2**, mysqlclient **2.3.0**, MySQL **8.4.9**, unittest-xml-reporting **4.0.0**, Ruff **0.17.1**. MySQL 8.4 substitutes for the Test Plan's 8.0 baseline, pending team acceptance. Tests use synthetic fixtures and disposable `test_hms`.

Both reports share [complete metrics/input hashes](evidence/owned-defects/coverage-metrics.json), [mixed-run metadata](evidence/owned-defects/coverage-mixed-run.json), [strict16 metadata](evidence/owned-defects/coverage-strict16-run.json), [proposed37 metadata](evidence/owned-defects/coverage-proposed37-run.json), [JUnit outcomes](evidence/owned-defects/coverage-junit-summary.json), [scope/method inventory](evidence/owned-defects/coverage-unit-scope.json) and [reproduction notes](evidence/owned-defects/coverage-notes.md). Historical [issue42 evidence](evidence/issue42/README.md) remains available for its earlier candidate.

## Result

The mixed suite executes **1584/1674 statements (94.62%)**, with **90 missing**. The application subtotal is **1505/1579 (95.31%)**. Strict16 attributes **31/1579 (1.96%)** application statements; proposed37 attributes **144/1579 (9.12%)**. These are nonexhaustive diagnostics: the complete Test Plan unit result remains **undetermined** pending #41 classification.

## Measurement scope

The unchanged `.coveragerc` enables branches for `accounts,allocations,audit,hms,hostels,payments,reports,scripts,students`, omitting `*/migrations/*`, `*/tests.py`, `*/test_*.py`, `*/apps.py`, `*/__init__.py`, `*/settings.py`, `*/asgi.py`, `*/wsgi.py`. These omissions do not waive testing their behavior. No coverage exclusions or threshold changes were introduced for this refresh.

The configured measure contains **51 files** and **49 nonempty XML rows**. The application subtotal retains every measured file in the eight application packages, including admin/URL declarations, and removes only `scripts/run_checks.py` tooling. Empty files have zero denominators and **N/A** rates. The denominator includes declarations and is not an agreed definition of application logic. The [unmeasured Python inventory](evidence/owned-defects/coverage-metrics.json) explains absent Python files; templates/static assets, JavaScript, SQL, browser/load/recovery execution and `scripts/part3` are outside this measured Python scope.

Fresh exports from each original `.coverage` reconcile all file statements/arcs/totals with JSON. Every nonempty XML class has a unique repository-relative path; every executed/missing line and per-file branch count agrees with JSON. Input hashes distinguish exact Windows bytes from committed Git blobs, with line-ending-only differences listed.

## Test execution

The full suite discovered **189 methods**: **188 passed**, zero failures/errors, and one intentional timing skip under coverage. The runner then passed that timing check without tracing, adding no coverage credit. All **12 repository gates passed**. These are mixed unit/component/integration/concurrency/system checks. The separate strict16 and proposed37 runs passed **16/16** and **37/37**, respectively, without skips. Selected method IDs match JUnit, with **16** and **34** observed measured contexts respectively; startup context is excluded. A selected method can pass without executing measured application code in its method context; those methods are listed in the scope inventory and receive no inferred coverage. Passing this suite does not by itself approve all planned cases or establish absence of defects.

## Mixed-suite statement coverage by module

| Module | Measured statements | Executed | Missing | Statement coverage |
|---|---:|---:|---:|---:|
| accounts | 271 | 260 | 11 | 95.94% |
| allocations | 303 | 281 | 22 | 92.74% |
| audit | 158 | 152 | 6 | 96.20% |
| hms | 79 | 76 | 3 | 96.20% |
| hostels | 255 | 236 | 19 | 92.55% |
| payments | 256 | 245 | 11 | 95.70% |
| reports | 86 | 86 | 0 | 100.00% |
| scripts | 95 | 79 | 16 | 83.16% |
| students | 171 | 169 | 2 | 98.83% |
| **Configured total** | 1674 | 1584 | 90 | 94.62% |
| **Application subtotal (excludes scripts)** | 1579 | 1505 | 74 | 95.31% |

## Per-file statements and missing lines

Line numbers refer to the tested candidate. Complete executed/missing line inventories for all three scopes are retained in the metrics JSON.

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
| [allocations/views.py](../../allocations/views.py) | 132 | 124 | 8 | 93.94% | 40, 62, 70, 100, 149, 152, 154-155 |
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

## Separately attributed diagnostics and SRS 6.4

SRS 6.4 states: **"unit tests cover at least 70% of the application logic."** Test Plan section 5 defines units as **"Django TestCase for models, forms and views of each module"** and integration as **"views ↔ ORM ↔ MySQL"**, for example allocation transactions and constraints. The previous report's database-free subset was narrower than the Test Plan definition; real ORM setup alone cannot exclude every model/form/view method from unit classification.

| Diagnostic scope | Methods | Selection |
|---|---:|---|
| Strict16 | 16 | Database-free `SimpleTestCase` methods in `hms.test_forms` (3), `hms.test_http` (10), `hms.test_responses` (3) |
| Proposed37 | 37 | Strict16 plus 21 directly invoked model/form component methods; exact method IDs are in the scope inventory |

**Proposed37 is nonexhaustive and pending #41 review.** Additional Test Plan units may exist, including view checks; this report does not classify every remaining test as integration. The measured subsets cannot determine whether the complete agreed unit scope meets or misses 70%.

Both diagnostics use `dynamic_context = test_function`, exclude empty startup/import/setup context from their numerators, and retain the same full-file denominators as the mixed suite. Startup-only model/form/view declarations therefore remain in the denominator without subset credit. This attribution asymmetry and the definition of application logic require #41's review before any SRS verdict. The denominator is not reduced to exercised files. Diagnostic exports use `--fail-under=0` to preserve the observations; export exit 0 is not a passing unit threshold.

| Application module | Measured statements | Strict16 executed | Strict16 coverage | Proposed37 executed | Proposed37 coverage |
|---|---:|---:|---:|---:|---:|
| accounts | 271 | 0 | 0.00% | 16 | 5.90% |
| allocations | 303 | 0 | 0.00% | 47 | 15.51% |
| audit | 158 | 0 | 0.00% | 5 | 3.16% |
| hms | 79 | 31 | 39.24% | 31 | 39.24% |
| hostels | 255 | 0 | 0.00% | 26 | 10.20% |
| payments | 256 | 0 | 0.00% | 0 | 0.00% |
| reports | 86 | 0 | 0.00% | 0 | 0.00% |
| students | 171 | 0 | 0.00% | 19 | 11.11% |
| **Application subtotal** | 1579 | 31 | 1.96% | 144 | 9.12% |

## Gate, limitations and review

The unchanged repository `fail_under = 70` gate combines statements and branch outcomes: `(1584 + 342) / (1674 + 392) = 93.22%`. It **passed**. This differs from standalone statement/branch rates and does not settle the SRS unit requirement. **The Part 3 PDF specifies no separate branch threshold.**

The earlier PR #36 setup baseline and 3 November issue42 measurements are historical; current tables bind to the candidate above. Source changes require matching reruns. Coverage measures execution, not assertion quality, requirement acceptance or defect absence. #41 owns the broader unit classification and Unit Test Report; #37/#38/#43 retain RTM/system/final review ownership. Both coverage reports and the submission build still need independent acceptance.

See the separate [Branch Coverage Report](Branch_Coverage_Report.md).
