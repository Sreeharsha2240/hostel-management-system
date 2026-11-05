# Branch Coverage Report

Owner: Devansh Gupta (`DevaOnL`), [issue #42](https://github.com/Sreeharsha2240/hostel-management-system/issues/42). Measured **4 November 2026**.

Tested current candidate: `6e349f2c07630e72b9151a575685d462e63cbc40`; tree: `558190f7852283743ab9e20a4c9b3c9b99d0f806`; **clean working tree at all three executions**. Documentation/evidence additions follow the measurement and do not relabel its commit. Current candidate; no independent teammate approval or accepted submission build is claimed. #41 owns the broader Test Plan unit classification; both coverage reports still require independent review.

Environment: Windows-11-10.0.26200-SP0, Python **3.14.7**, Django **5.2.18**, coverage.py **7.16.2**, mysqlclient **2.3.0**, MySQL **8.4.9**, unittest-xml-reporting **4.0.0**, Ruff **0.17.1**. MySQL 8.4 substitutes for the Test Plan's 8.0 baseline, pending team acceptance. Tests use synthetic fixtures and disposable `test_hms`.

Both reports share [complete metrics/input hashes](evidence/owned-defects/coverage-metrics.json), [mixed-run metadata](evidence/owned-defects/coverage-mixed-run.json), [strict16 metadata](evidence/owned-defects/coverage-strict16-run.json), [proposed37 metadata](evidence/owned-defects/coverage-proposed37-run.json), [JUnit outcomes](evidence/owned-defects/coverage-junit-summary.json), [scope/method inventory](evidence/owned-defects/coverage-unit-scope.json) and [reproduction notes](evidence/owned-defects/coverage-notes.md). Historical [issue42 evidence](evidence/issue42/README.md) remains available for its earlier candidate.

## Result and definitions

The mixed suite covers **342/392 branch outcomes (87.24%)**, with **50 missing**. Of these, **46** originate on executed lines (`num_partial_branches`); **4** originate on unexecuted lines. Partial missing outcomes are already included in missing outcomes. The application subtotal is **330/378 (87.30%)**.

A branch is a measured source-to-destination outcome, not a count of `if` statements. A source line can have multiple missing outcomes. `exit@N` denotes coverage.py's negative destination for leaving the code object beginning at line N. Files without outcomes have **N/A** rates.

## Measurement scope

The unchanged `.coveragerc` enables branches for `accounts,allocations,audit,hms,hostels,payments,reports,scripts,students`, omitting `*/migrations/*`, `*/tests.py`, `*/test_*.py`, `*/apps.py`, `*/__init__.py`, `*/settings.py`, `*/asgi.py`, `*/wsgi.py`. These omissions do not waive testing their behavior. No coverage exclusions or threshold changes were introduced for this refresh.

The configured measure contains **51 files** and **49 nonempty XML rows**. The application subtotal retains every measured file in the eight application packages, including admin/URL declarations, and removes only `scripts/run_checks.py` tooling. Empty files have zero denominators and **N/A** rates. The denominator includes declarations and is not an agreed definition of application logic. The [unmeasured Python inventory](evidence/owned-defects/coverage-metrics.json) explains absent Python files; templates/static assets, JavaScript, SQL, browser/load/recovery execution and `scripts/part3` are outside this measured Python scope.

Fresh exports from each original `.coverage` reconcile all file statements/arcs/totals with JSON. Every nonempty XML class has a unique repository-relative path; every executed/missing line and per-file branch count agrees with JSON. Input hashes distinguish exact Windows bytes from committed Git blobs, with line-ending-only differences listed.

## Test execution

The full suite discovered **189 methods**: **188 passed**, zero failures/errors, and one intentional timing skip under coverage. The runner then passed that timing check without tracing, adding no coverage credit. All **12 repository gates passed**. These are mixed unit/component/integration/concurrency/system checks. The separate strict16 and proposed37 runs passed **16/16** and **37/37**, respectively, without skips. Selected method IDs match JUnit, with **16** and **34** observed measured contexts respectively; startup context is excluded. A selected method can pass without executing measured application code in its method context; those methods are listed in the scope inventory and receive no inferred coverage. Passing this suite does not by itself approve all planned cases or establish absence of defects.

## Mixed-suite branch coverage by module

| Module | Measured outcomes | Covered | Missing | Partial missing outcomes | Branch coverage |
|---|---:|---:|---:|---:|---:|
| accounts | 68 | 55 | 13 | 13 | 80.88% |
| allocations | 92 | 78 | 14 | 14 | 84.78% |
| audit | 26 | 23 | 3 | 3 | 88.46% |
| hms | 26 | 23 | 3 | 3 | 88.46% |
| hostels | 58 | 50 | 8 | 4 | 86.21% |
| payments | 54 | 49 | 5 | 5 | 90.74% |
| reports | 20 | 20 | 0 | 0 | 100.00% |
| scripts | 14 | 12 | 2 | 2 | 85.71% |
| students | 34 | 32 | 2 | 2 | 94.12% |
| **Configured total** | 392 | 342 | 50 | 46 | 87.24% |
| **Application subtotal (excludes scripts)** | 378 | 330 | 48 | 44 | 87.30% |

## Per-file branch outcomes and remaining paths

These unobserved arcs refer to the tested candidate; browser/manual evidence does not add Python coverage credit. Full executed/missing arc inventories for all three scopes remain in the metrics JSON.

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
| [allocations/views.py](../../allocations/views.py) | 46 | 40 | 6 | 6 | 86.96% | 38 -> 40; 61 -> 62; 69 -> 70; 99 -> 100; 116 -> 123; 147 -> 149 |
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

## Separately attributed diagnostic branch coverage

| Application module | Measured outcomes | Strict16 covered | Strict16 coverage | Proposed37 covered | Proposed37 coverage |
|---|---:|---:|---:|---:|---:|
| accounts | 68 | 0 | 0.00% | 3 | 4.41% |
| allocations | 92 | 0 | 0.00% | 28 | 30.43% |
| audit | 26 | 0 | 0.00% | 2 | 7.69% |
| hms | 26 | 16 | 61.54% | 16 | 61.54% |
| hostels | 58 | 0 | 0.00% | 16 | 27.59% |
| payments | 54 | 0 | 0.00% | 0 | 0.00% |
| reports | 20 | 0 | 0.00% | 0 | 0.00% |
| students | 34 | 0 | 0.00% | 7 | 20.59% |
| **Application subtotal** | 378 | 16 | 4.23% | 72 | 19.05% |

Strict16 is a narrow database-free diagnostic. Proposed37 adds 21 direct model/form component methods and is nonexhaustive. Test Plan section 5 explicitly permits Django TestCase model/form/view units; database use alone does not classify a method as integration. Both subsets omit startup/import/setup context while retaining full-file denominators, so declarations executed only at startup receive no subset credit. These diagnostics do not establish that all Test Plan units pass or fail the SRS 70% target. See [Code Coverage Report](Code_Coverage_Report.md) for the Test Plan definition and statement comparison.

## Gate, limitations and review

The unchanged repository `fail_under = 70` gate combines statements and branch outcomes: `(1584 + 342) / (1674 + 392) = 93.22%`. It **passed**. This differs from standalone statement/branch rates and does not settle the SRS unit requirement. **The Part 3 PDF specifies no separate branch threshold.**

The earlier PR #36 setup baseline and 3 November issue42 measurements are historical; current tables bind to the candidate above. Source changes require matching reruns. Coverage measures execution, not assertion quality, requirement acceptance or defect absence. #41 owns the broader unit classification and Unit Test Report; #37/#38/#43 retain RTM/system/final review ownership. Both coverage reports and the submission build still need independent acceptance.
