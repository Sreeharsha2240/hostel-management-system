# Code Coverage Report

Mixed statements: **1584/1772 (89.39%)**; mixed branches: **342/424 (80.66%)**. Application statements: **1505/1677 (89.74%)**; branches: **330/410 (80.49%)**.

The previously frozen **76 proposed component methods now also execute as a standalone suite**: 76 methods: 76 PASS, 0 failures, 0 errors, 0 skipped. Its complete coverage includes imports and shared fixture execution; method-only and empty-context observations are reported separately. **Formal SRS section 6.4 unit70 remains UNPROVEN** pending joint #41/#42 scope and application-logic agreement.

Owner: Devansh Gupta (`DevaOnL`), [HMS-20 / #42](https://github.com/Sreeharsha2240/hostel-management-system/issues/42). Measured **2026-11-06** on clean current main `b936e4d8ef7efd37dd66fde022efcb44e5b386ee`, tree `1191cfa0aed5201d3529e2f63120c5b99a29e781`. This is a measured candidate; the team retains the accepted final submission-build decision. The source manifest retains the measured `docs/PART3.md` hash as its pre-publication documentation snapshot; its later owner index update does not relabel the measured SHA. `Test_Case_Document.md` remains unchanged in this refresh.

Both reports use [current source metrics](evidence/issue42-main/coverage-metrics.json), [normal verification](evidence/issue42-main/checks-run.json), [serial collection commands](evidence/issue42-main/collection-run.json), [all JUnit outcomes](evidence/issue42-main/junit-summary.json), [attribution and frozen selection](evidence/issue42-main/attribution.json), [startup/setup partition](evidence/issue42-main/startup-context-diagnostic.json) and [reconciliation](evidence/issue42-main/validation.json). [Reproduction and limits](evidence/issue42-main/README.md) accompany them. All earlier evidence JSON, including `issue42-final`, is preserved unchanged.

## Environment and execution

| Component | Recorded version |
|---|---|
| Platform | Windows-11-10.0.26200-SP0 |
| Python | 3.14.7 |
| MySQL | 8.4.9 |
| Django | 5.2.18 |
| coverage | 7.16.2 |
| mysqlclient | 2.3.0 |
| pypdf | 6.21.2 |
| python-dotenv | 1.2.4 |
| reportlab | 4.5.1 |
| ruff | 0.17.1 |
| unittest-xml-reporting | 4.0.0 |

MySQL 8.4 remains the recorded substitution for the Test Plan's MySQL 8.0 baseline, pending team acceptance. Synthetic fixtures and disposable `test_hms` are used, with suites executed serially and preflight/postflight ownership checks.

Normal checks pass **all 12 gates**. Normal full suite: 190 methods: 189 PASS, 0 failures, 0 errors, 1 skipped. Context full suite: 190 methods: 189 PASS, 0 failures, 0 errors, 1 skipped. The single timing skip is expected under tracing; its separate uninstrumented rerun passes without adding coverage credit. Standalone76 contains no timing test and no skips. Application, test and configuration sources are unchanged by this coverage/reporting refresh.

The unchanged collection/report configuration is:

```ini
[run]
branch = True
source = accounts,allocations,audit,hms,hostels,payments,reports,scripts,students
omit =
    */migrations/*
    */tests.py
    */test_*.py
    */apps.py
    */__init__.py
    */settings.py
    */asgi.py
    */wsgi.py

[report]
fail_under = 70
show_missing = True
skip_empty = True
```

The context and standalone collections add only `dynamic_context = test_function`. All observations retain the complete current file/line/arc denominator, including declarations. The application subtotal excludes only runner tooling under `scripts/`; it remains a full-file proxy, not a reviewed definition of application logic. Missing-context methods receive no inferred credit.

## Current source gaps

Main incorporated the seed/demo-data commands after the earlier `9a0f814` measurement. They remain measured at zero executed statements in this run; the denominator includes them. No percentage-driven tests or exclusions were added, and the commands were not invoked against the application database.

| New measured file since issue42-final | Statements | Executed | Branch outcomes | Covered |
|---|---|---|---|---|
| accounts/management/commands/create_demo_accounts.py | 43 | 0 | 10 | 0 |
| accounts/management/commands/create_demo_data.py | 55 | 0 | 22 | 0 |

Historical October/PR #36 values (94.28% statements, 85.57% branches, 92.63% combined) and the earlier 6 November 1,674/392 configured denominator are baselines only. The current configured denominator is **1772 statements / 424 outcomes**; application denominator is **1677 / 410**. All actual missing paths remain visible below.

## Mixed-suite statement coverage by module

| Module | Measured statements | Executed | Missing | Statement coverage |
|---|---|---|---|---|
| accounts | 369 | 260 | 109 | 70.46% |
| allocations | 303 | 281 | 22 | 92.74% |
| audit | 158 | 152 | 6 | 96.20% |
| hms | 79 | 76 | 3 | 96.20% |
| hostels | 255 | 236 | 19 | 92.55% |
| payments | 256 | 245 | 11 | 95.70% |
| reports | 86 | 86 | 0 | 100.00% |
| scripts | 95 | 79 | 16 | 83.16% |
| students | 171 | 169 | 2 | 98.83% |
| **Configured total** | 1772 | 1584 | 188 | 89.39% |
| **Application subtotal (excludes scripts)** | 1677 | 1505 | 172 | 89.74% |

## Per-file statement coverage and missing paths

Line/arc numbers refer to this exact tested revision. Partial missing outcomes are already included in missing branches; `exit@N` is a negative code-object exit destination. Complete inventories for every scope are in the durable JSON; browser/manual evidence adds no Python coverage credit.

| File | Measured | Executed | Missing | Statement coverage | Missing lines |
|---|---|---|---|---|---|
| [accounts/admin.py](../../accounts/admin.py) | 23 | 20 | 3 | 86.96% | 26, 29, 35 |
| [accounts/backends.py](../../accounts/backends.py) | 36 | 34 | 2 | 94.44% | 19, 34 |
| [accounts/decorators.py](../../accounts/decorators.py) | 22 | 22 | 0 | 100.00% | none |
| [accounts/forms.py](../../accounts/forms.py) | 38 | 37 | 1 | 97.37% | 19 |
| [accounts/management/commands/create_demo_accounts.py](../../accounts/management/commands/create_demo_accounts.py) | 43 | 0 | 43 | 0.00% | 3, 5-9, 11, 14-15, 17, 23-25, 29-36, 39-46, 49, 51-62, 64 |
| [accounts/management/commands/create_demo_data.py](../../accounts/management/commands/create_demo_data.py) | 55 | 0 | 55 | 0.00% | 3, 5-8, 10-16, 19-20, 22, 31-34, 36-39, 44, 48, 53, 69-70, 81, 83-85, 88, 104, 106-110, 112, 118-120, 123-124, 133-134, 139-140, 142, 162-165, 174 |
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

## Proposed component scope and standalone evidence

The original behavior-based classification remains [unchanged](evidence/issue42-final/method-classification.json) at source `9a0f814e403a6f83535e80a68db4150197eba74b`. All **19** referenced test-source hashes match the current measured source. Its method choices and exact 76/100 lists were frozen at `2026-11-06T03:27:27.875258+00:00` before the original subset rates. This execution reuses that proposal; it does not claim a new blind classification after seeing previous rates.

Classification SHA-256: `67a5dc896137bf370f8060ff02b86effbb9218e1177eb85b428346e87242d2f7`. Unchanged selection-core SHA-256: `654020d1bb897ed83e4d2dfc4a265e25d41932af0e6f3778d69e0ddcbbaf5679`. The historical borderline-index repair changed no method category, rationale, flag or selected list; its original/current hashes and chronology are retained in current attribution. Conservative76 excludes all nine primary-component borderlines; sensitivity100 adds all 24 flagged methods. No scope choice was revised to improve a percentage.

| Proposed observation | Selected methods | Observed contexts | Without runtime context |
|---|---|---|---|
| component_proposal | 76 | 73 | 3 |
| component_sensitivity | 100 | 97 | 3 |
| standalone76_methods | 76 | 73 | 3 |

| Application scope | Executed/measured statements | Statements | Covered/measured outcomes | Branches |
|---|---|---|---|---|
| Normal full mixed suite | 1505/1677 | 89.74% | 330/410 | 80.49% |
| Context full mixed suite | 1505/1677 | 89.74% | 330/410 | 80.49% |
| Mixed-run conservative76 method contexts | 405/1677 | 24.15% | 173/410 | 42.20% |
| Mixed-run sensitivity100 method contexts | 629/1677 | 37.51% | 261/410 | 63.66% |
| Standalone76 including startup/shared setup | 1127/1677 | 67.20% | 175/410 | 42.68% |
| Standalone76 method contexts only | 414/1677 | 24.69% | 173/410 | 42.20% |
| Standalone76 empty startup/shared-setup context | 735/1677 | 43.83% | 13/410 | 3.17% |

The first two component selections are filtered from the full mixed run. The final three observations come from a separate process executing exactly the frozen76 IDs, reconciled against its exact JUnit identity set. Standalone aggregate coverage includes imports, declarations and startup/shared fixtures. The empty context also includes framework/database setup and teardown: this instrumentation cannot separate those causes or assign them to unit assertions. Method and empty counts overlap and must not be added without subtracting overlap.

| Execution | Observed method contexts | Method statements | Empty-context statements | Empty-only statements | Overlap statements |
|---|---|---|---|---|---|
| mixed | 181 | 792 | 735 | 713 | 22 |
| standalone76 | 73 | 414 | 735 | 713 | 22 |

Standalone76 method attribution executes 414 application statements versus 405 for the same76 selected from the full mixed run. All nine additional lines are imports/class/function declarations in `accounts/backends.py` (3, 5, 6, 7, 8, 11, 12, 13, 15). Their context differs with import timing and test order; no additional tested behavior is inferred. The method-context percentage is an execution observation, not a comparison of assertion strength.

The submitted Test Plan permits Django model/form/view component unit tests and separately describes ORM/MySQL interaction integration checks. ORM fixtures alone do not settle classification. Persistent fixture execution is disclosed, not treated as independent scope acceptance. #41 retains the Unit Test Report and case mapping; #42 provides these owner coverage inputs.

## Gate and acceptance limits

The unchanged configured gate combines statements and branch outcomes: `(1584 + 342) / (1772 + 424) = 87.70%` against `fail_under = 70`. Normal verification passes this combined gate. It is a different metric from statement coverage, branch coverage and SRS unit70. No separate Part 3 branch threshold is specified. Diagnostic exports use `fail_under = 0` only to preserve observations, without changing the normal gate.

**SRS section 6.4 unit-test application-logic coverage of at least 70%: UNPROVEN.** Neither a startup-inclusive standalone percentage nor a mixed-suite percentage establishes its PASS or FAIL. The proposed classification and full-file denominator require joint independent #41/#42 review.

PR #54 received an actual independent approval from `harsha2240` and merged on 6 November at `af3da3af513e8d413093132486ff1206c0d1f312`. That review accepted the previous documentation/evidence reconciliation while preserving the unit70 and QA acceptance limitations. **These refreshed current-main reports and new standalone evidence require fresh independent review.** Earlier review and CI do not approve the new evidence, select the final submission build or complete the Unit/System reports. Source/test/configuration changes require refreshed affected evidence. Coverage does not establish assertion quality, RTM completion or whole-system readiness.

See the separate [Branch Coverage Report](Branch_Coverage_Report.md).
