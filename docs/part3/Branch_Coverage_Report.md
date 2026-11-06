# Branch Coverage Report

The mixed suite covers **342/392 branch outcomes (87.24%)**, with **50 missing**, including **46 partial missing outcomes**. The application subtotal is **330/378 (87.30%)**. Partial outcomes are already included in missing outcomes, not added to them. A branch is a measured source-to-destination outcome; `exit@N` denotes a negative code-object exit destination.

Separately attributed application statements: **405/1579 (25.65%)** for the conservative component proposal, and **629/1579 (39.84%)** for its broader sensitivity scope. Both observations are below 70% on this retained full-file proxy, whose all-method-context statement ceiling is **50.16% for this recorded dataset**, as quantified below. The formal SRS unit-coverage criterion remains **UNPROVEN**, pending joint QA review of the classification and application-logic denominator.

Owner: Devansh Gupta (`DevaOnL`), [HMS-20 / #42](https://github.com/Sreeharsha2240/hostel-management-system/issues/42). Measured **2026-11-06**.

Tested candidate: `9a0f814e403a6f83535e80a68db4150197eba74b`; tree: `c916feba77b7a2aad4d75626ddab4326948d6851`. The normal verification run records a **clean working tree**. Evidence and report additions follow measurement and do not relabel its SHA. **Candidate evidence; accepted submission revision, independent teammate review and joint #41 scope acceptance remain pending.**

After measurement, `docs/PART3.md` and `docs/part3/Test_Case_Document.md` received documentation updates. Their original measured hashes remain in the manifest; runtime, test and configuration inputs remain unchanged from this tested candidate.

Both coverage reports use [the same durable metrics](evidence/issue42-final/coverage-metrics.json), [normal verification metadata](evidence/issue42-final/checks-run.json), [context-run metadata](evidence/issue42-final/context-run.json), [JUnit outcomes](evidence/issue42-final/junit-summary.json), [exhaustive proposed classification](evidence/issue42-final/method-classification.json), [context attribution](evidence/issue42-final/attribution.json) and [reconciliation checks](evidence/issue42-final/validation.json). [Reproduction and limits](evidence/issue42-final/README.md) accompany them. Earlier `issue42` and `owned-defects` JSON remain historical and unchanged.

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

MySQL 8.4 is the recorded substitution for the original Test Plan's MySQL 8.0 baseline; it still needs team acceptance. Tests use synthetic fixtures and disposable `test_hms`. Django/MySQL suites run serially.

- Normal `python scripts/run_checks.py`: **190 methods: 189 PASS, 0 failures, 0 errors, 1 skipped**, with all **12 gates recording exit 0**. The intentional traced timing skip is followed by a separate **uninstrumented PASS**, which adds no coverage credit.
- Context-instrumented **full mixed-suite** collection: **190 methods: 189 PASS, 0 failures, 0 errors, 1 skipped**. Proposed component percentages are filtered attribution from this full run, **not separate standalone unit-suite executions**.
- The XML helper regression `tests.test_checks.VerificationRunnerTests.test_xml_keeps_same_named_package_files_and_only_selected_context_hits` is PASS in both current runs in this normal Windows environment. The restricted AppContainer failure previously documented for #38 was **not reproduced here**. These runs do not establish its root cause or that the other environment is fixed.

## Measurement scope and attribution

The unchanged collection configuration is:

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

This measures **51 Python files**, with **49 nonempty XML rows**. The application subtotal retains measured application packages, including admin and URL declarations, and excludes only `scripts/run_checks.py` tooling. Empty denominators receive **N/A**. Templates, static assets/JavaScript, SQL, browser/load/recovery activity and `scripts/part3` are outside this Python measurement; omitted files' behavior is not waived. No new product tests, denominator exclusions or threshold changes were introduced for this coverage refresh.

Every scope preserves the same measured file, statement and branch-outcome denominators. Unit attribution uses anchored, escaped exact method-context selections and excludes empty startup/import/shared setup context. Consequently, declarations and shared setup may remain in the full-file denominator without selected-method credit. This is a conservative attribution limitation, not a reviewed definition of application logic; do not credit shared startup execution to units or shrink the denominator to exercised files. Selected methods without measured runtime contexts receive no inferred coverage.

| Proposed scope | Selected methods | Observed measured method contexts | Without measured method context |
|---|---|---|---|
| component_proposal | 76 | 73 | 3 |
| component_sensitivity | 100 | 97 | 3 |

The exhaustive proposed classification inventories **190 methods** and records individual rationale. The **method decisions and selections** were frozen at `2026-11-06T03:27:27.875258+00:00`, before subset exports or unit-rate extraction. Original pre-export artifact SHA-256: `4bb5ccd486ea2da7c64029f484de923ea40846c8a9bf8d337dfe75688549ffe3`. At `2026-11-06T03:30:23.647384+00:00`, independent checking found and repaired a redundant summary index: the cached borderline list had 21 entries while its unchanged method rows flagged 24. Categories, reasons, flags and both selected method lists were unchanged. Current corrected artifact SHA-256: `67a5dc896137bf370f8060ff02b86effbb9218e1177eb85b428346e87242d2f7`; unchanged selection-core SHA-256: `654020d1bb897ed83e4d2dfc4a265e25d41932af0e6f3778d69e0ddcbbaf5679`. The corrected serialized artifact was produced after viewing rates; its selection core predates them.

The **85** primary component methods include **9** borderline cases excluded from the **76** conservative selections. The sensitivity selection adds **all 24** borderline cases (including those 9 and 15 cases with other primary categories) to produce **100** methods. This broader scope is reported transparently and does not replace the proposal to reach a target.

| Proposed class | Methods |
|---|---|
| component-unit | 85 |
| concurrency | 5 |
| integration | 87 |
| system | 4 |
| tooling | 9 |

| Application scope | Executed/measured statements | Statement coverage | Covered/measured outcomes | Branch coverage |
|---|---|---|---|---|
| mixed | 1505/1579 | 95.31% | 330/378 | 87.30% |
| context_all | 1505/1579 | 95.31% | 330/378 | 87.30% |
| component_proposal | 405/1579 | 25.65% | 173/378 | 45.77% |
| component_sensitivity | 629/1579 | 39.84% | 261/378 | 69.05% |

The [startup/shared-setup diagnostic](evidence/issue42-final/startup-context-diagnostic.json) quantifies a limit of this proxy: **all 181 recorded nonempty test-method contexts together** cover only **792/1579 application statements (50.16%)**, and **328/378 branch outcomes (86.77%)**. These contexts include integration, system and tooling checks as well as proposed units. Their union is an upper bound for any selection of the existing observed methods, not a unit result.

The empty context executes **735 statements**: **713 exclusively** there and **22 also within methods**. It mixes imports, declarations and shared setup. Thus reclassification alone cannot demonstrate 70% with this recorded method-only/full-file proxy. The 25.65%/39.84% figures do not establish inadequate unit tests or a formal SRS failure. QA must agree on application logic and appropriate attribution/instrumentation; this diagnostic does not credit shared setup to units or remove it from the denominator. Different execution, future tests or a reviewed denominator may differ. This later read-only analysis preserves the original data, frozen decisions and 76/100 selections; it is not a new unit run.

The submitted Test Plan §5 permits **Django TestCase for models, forms and views of each module**; it separately identifies views ↔ ORM ↔ MySQL interaction checks as integration. ORM fixture setup alone does not settle classification. The newly merged [Test Case Document](Test_Case_Document.md) supplies case references, but its merge does not establish QA review of this method classification or denominator. #41 owns the Unit Test Report; #42 provides coverage evidence and a proposed scope for their joint review.


## Mixed-suite branch coverage by module

| Module | Measured outcomes | Covered | Missing | Partial missing outcomes | Branch coverage |
|---|---|---|---|---|---|
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

## Per-file branch coverage and missing paths

Line/arc numbers refer to the exact tested candidate. Complete executed/missing inventories for all four scopes remain in the durable metrics JSON. Manual/browser evidence adds no Python coverage credit.

| File | Measured | Covered | Missing | Partial | Branch coverage | Missing arcs |
|---|---|---|---|---|---|---|
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

## Proposed component attribution and sensitivity

These are selected contexts from the full instrumented mixed-suite run. They do not claim independent standalone component execution or accepted classification.

| Application module | Measured outcomes | Proposal covered | Proposal coverage | Sensitivity covered | Sensitivity coverage |
|---|---|---|---|---|---|
| accounts | 68 | 21 | 30.88% | 38 | 55.88% |
| allocations | 92 | 34 | 36.96% | 62 | 67.39% |
| audit | 26 | 10 | 38.46% | 21 | 80.77% |
| hms | 26 | 22 | 84.62% | 22 | 84.62% |
| hostels | 58 | 30 | 51.72% | 43 | 74.14% |
| payments | 54 | 16 | 29.63% | 31 | 57.41% |
| reports | 20 | 20 | 100.00% | 20 | 100.00% |
| students | 34 | 20 | 58.82% | 24 | 70.59% |
| **Application subtotal** | 378 | 173 | 45.77% | 261 | 69.05% |

## Gate, SRS assessment and acceptance limits

The unchanged repository gate combines statement and branch outcomes: `(1584 + 342) / (1674 + 392) = 93.22%` against `fail_under = 70`. The normal verification run records the gate as passed. This is different from the separate statement and branch rates. The Part 3 instructions do not define a separate branch percentage threshold.

SRS §6.4 states that **unit tests cover at least 70% of application logic**. **UNPROVEN pending joint #41 scope/denominator review and independent acceptance.** The component proposal and sensitivity values are measured observations under proposed classifications. Neither the mixed-suite score nor a proposed percentage establishes a final SRS PASS or FAIL. Diagnostic `--fail-under=0` permits export of observations and does not pass or change a unit threshold.

Reports preserve actual missing lines/arcs and classification uncertainty. Coverage measures execution, not assertion quality, all-case execution, RTM acceptance, absence of defects or system readiness. #37/#38/#41/#43 retain their assigned deliverables and approvals. Both coverage reports and the final accepted revision require actual independent teammate review. Final source/test changes require matching evidence; previous results remain historical.


See the separate [Code Coverage Report](Code_Coverage_Report.md).
