# Development review and HMS-19 classification handoff

**Date:** 8 November 2026. **Reviewed main:** `cae69ea2192838b7874ad5be240def842f5aab5e`, tree `4f81f4a5e100f6a3f22505acfa05b4dd0ff9bb1f`.

**Development decision: accept the reports as a documented NOT READY checkpoint; HOLD final development acceptance of HMS-16/#38 and HMS-21/#43.** This is Devansh's authorized AI-assisted technical review, supported by independent automated reviewers. It records a technical decision, not a named human signature, criterion waiver, new coverage run or acceptance of an unassembled final package. Harsha requested final sign-off when the remaining evidence is ready; that condition is not met.

## Reviewed evidence and current state

The authority is the submitted [Test Plan](../../Test_Plan_Hostel_Management_System.docx), [SRS](../../SRS_Hostel_Management_System.docx) and [Part 3 instructions](SE_Mini_Project_Delivereables_Part-3.pdf). The [System Validation Report](System_Validation_Report.md), [readiness checkpoint](HMS21_Final_Readiness.md), [case register](Test_Case_Document.md), [coverage report](Code_Coverage_Report.md) and retained evidence were reconciled with source and GitHub status. The [classification supplement](evidence/development-review-20261108/classification-supplement.json) contains exact method IDs, source hashes and corrections; the frozen proposal is preserved. The [read-only verification record](evidence/development-review-20261108/verification.json) reconciles the 190 AST/frozen/current-CI identities, 19 test-source hashes, source-equivalent measured inputs and both CI bundles.

PR #64 is merged; #40 and #63 are CLOSED. [Exact-main CI 42461981682](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42461981682) succeeded on Python 3.11 and 3.14. Each job reconciles 190 core methods (189 PASS / one expected timing SKIP), 12 gates, separate uninstrumented timing PASS, 32 recovery-safety tests, seven owned-runner safety tests and nine explicit expanded-case integration methods PASS. Two Python jobs do not double the distinct method count. This existing CI supplies integration verification, not fresh browser/load/restore/TLS or unit-only coverage evidence.

All 27 exclusively Devansh-owned case records have OWNER PASS observations. Original cases remain **30 OWNER PASS / 2 PARTIAL / 1 NOT RUN** out of 33; expanded records remain **48 / 3 / 9 / 1 BLOCKED** out of 61. These observations do not establish whole-plan QA acceptance. Historical measurements retain their dates/revisions, including coverage source `b936e4d8ef7efd37dd66fde022efcb44e5b386ee` and the earlier `b523d4c` report review.

## Development findings for HMS-16 and HMS-21

| Gate | Outstanding review and submission work | Responsible owner |
|---|---|---|
| Transport | TC-SEC-06 stays PARTIAL. Record real HTTP redirect, TLS protocol acceptance/rejection and authenticated Secure/HttpOnly session-cookie attributes with values removed, on a revision-bound isolated HTTPS target. Public hosting is unnecessary; settings/client flags do not prove a handshake. | Sreeharsha #38 |
| Security baseline and original conditions | TC-SEC-08 stays NOT RUN pending sanitized ZAP scope/findings/exit status, severity triage and defect/retest links. Address or obtain actual disposition of the [original security subconditions](System_Validation_Report.md#independent-review-of-original-security-subconditions). A baseline need not have zero alerts. | Sreeharsha with QA |
| Unit Test Report | `Unit_Test_Report.md` is absent. Publish classification decisions, selected IDs, module outcomes/case mappings, source/run/environment, denominator and attribution. SRS unit70 remains UNPROVEN. | Vaishnavi #41, with module-owner input below |
| Remaining execution | Complete or obtain genuine authorized disposition of registration, timed new-Warden guide walkthrough, remaining S1/S2 cases, browser/mobile/platform and availability gaps. Preserve unmet originals if criteria change. | Vaishnavi #39 and existing case owners; Sreeharsha for his cases |
| Test Plan entry/exit | Review priorities, historical entry deviations, accepted outcomes, 36-row passed-case RTM and complete severity-ranked defect inventory. Exits require 100% cases executed, all High cases passed, zero critical/high open defects and a passed case per RTM requirement. | QA with case/development owners |
| Final package | Select the candidate revision after evidence review; obtain actual QA/Dev/PO decisions, guide walkthrough, instructor instructions, authentic recordings and final package verification before submission. Record the real receipt after submission to complete #43; a receipt is not a prerequisite for reviewing the package. The PDF specifies 2–6 November testing, without a cutoff hour/export format; an extension is not inferred. | Sreeharsha #43 coordinates; each reviewer supplies their own decision |

Development recommends retaining the original transport/ZAP criteria and collecting evidence. This review records no team/instructor change. An honest limitation in a checkpoint is acceptable documentation; final compliance remains unmet.

## Apply the submitted unit and integration definitions

Test Plan §5 calls unit testing **“Django TestCase for models, forms and views of each module”** and integration **“views ↔ ORM ↔ MySQL, for example allocation transaction and constraints.”** These overlap for DB-backed view components. A universal DB-free requirement would narrow the submitted plan. Classify the asserted contract and disclose actual execution:

| Report scope | Decision rule |
|---|---|
| Isolated helper unit | Direct helper contract without real client/database workflow. |
| Model/form/view component with DB | Module-component assertions with persisted fixtures, validation or Django client. Candidate under the plan's broad definition; disclose `isolated=false` and obtain boundary review. |
| Integration / concurrency | Real constraints, atomicity/rollback, coordinated persistence, audit coupling, reconciliation or concurrent operations are asserted. Patching one failure point does not isolate the remaining dependencies. |
| System test-client surrogate | Cross-module smoke/journey through Django clients; actual browser evidence is separate. |
| Tooling / configuration | Runner/configuration contracts outside the application-unit numerator. An application retention command is not tooling merely because it is a command. |

The immutable [190-method proposal](evidence/issue42-final/method-classification.json) remains **85 component / 87 integration / 5 concurrency / 4 system / 9 tooling**. Conservative76 excludes all nine primary-component borderlines; sensitivity100 adds all 24 flagged methods. Keep exact lists, outcomes and original rationales as historical data. Corrections below do not silently reclassify tests or recompute percentages.

The **16 isolated helpers** are `hms.test_http.RequestDataTests` (10), `hms.test_forms.DateFieldTests` (2), `hms.test_forms.ModelChoiceFieldTests` (1), and `hms.test_responses.FormErrorResponseTests` (3). They use DB-forbidding `SimpleTestCase`. ModelChoice rejects invalid types before querying with `.none()`; a model import alone does not imply DB execution. Exact IDs/source references are in the supplement.

## Devansh's exact module input for #41

Existing evidence supplies **62 passing mixed methods**: allocations 31, payments 19, reports 12, historically proposed as **18 component / 39 integration / 5 concurrency**. Their standalone76 intersection is **11 PASS** (4 / 2 / 5 respectively). **Zero of the owned62 are isolated units as executed.** These 11 are DB-backed component candidates under the submitted plan:

| Exact method ID | Actual dependencies and asserted contract |
|---|---|
| `allocations.tests.AllocationViewTests.test_admin_can_view_allocation_list` | Authenticated client GET, routing/templates and DB fixtures. |
| `allocations.tests.AllocationViewTests.test_admin_can_open_allocation_form` | Client GET renders choices from persisted Student/Bed data. |
| `allocations.tests.AllocationViewTests.test_student_cannot_manage_allocations` | Persisted user and real client check route permissions. |
| `allocations.test_workflows.AllocationWorkflowTests.test_history_orders_backdated_records_by_allocation_date_in_json_and_html` | Real allocation/release setup, then history ordering/presentation assertions; inline services are also measured. |
| `payments.test_workflows.PaymentWorkflowTests.test_edit_delete_bulk_and_primary_key_replay_are_blocked` | Model/queryset immutability over a numbered, audited Payment, with atomic save and real DB reads. |
| `payments.test_workflows.PaymentWorkflowTests.test_form_encoded_missing_student_preserves_json_not_found_response` | Client/form lookup checks structured 404 and persisted non-effects. |
| `reports.test_reports.ReportTests.test_csv_quotes_unicode_and_formula_text_and_html_escapes_names` | Real Hostel/Student mutations and allocation feed CSV/HTML escaping assertions. |
| `reports.test_reports.ReportTests.test_empty_reports_and_invalid_filters_formats_and_methods` | Client validation, missing-hostel lookup and empty/zero-bed ORM reports. |
| `reports.test_reports.ReportTests.test_numeric_hostel_filter_accepts_leading_zeros` | Real route compared with an actual ORM report-service result. |
| `reports.test_reports.ReportTests.test_reports_allow_admin_warden_and_deny_students_and_anonymous_for_all_formats` | Persisted roles and actual clients check HTML/JSON/CSV permissions. |
| `reports.test_reports.ReportTests.test_reports_landing_redirects_to_occupancy_report` | `assertRedirects` follows the target by default, invoking the DB-backed report. |

Keep all nine historical primary-component borderlines outside conservative76. Development recommends integration for a new conservative binary disposition of their multi-route/persistence assertions, pending QA review; historical categories and measured selections remain unchanged. The six allocation-model tests, payment adjustment-date test and payment multi-route/PDF permission test retain their historical integration recommendation. Mock-injected audit/storage failures still test real DB rollback. Do not split mixed methods into fictional independently executed unit portions.

The nine explicit `TC-REG-S2-08..16` recipes are integration evidence outside historical190/owned62; S2-11 also exercises concurrency. Offline runner/recovery safety suites are tooling. Neither supplies an application-unit numerator.

## Corrected assertion scope and execution disclosures

The supplement retains the original rows and records these deltas separately:

| Method / source | Correct asserted scope and development recommendation |
|---|---|
| `accounts.tests.AuthenticationTests.test_admin_can_update_account` — [source](../../accounts/tests.py) | Redirect and saved `first_name`/`role`; no audit-row or rollback assertion. Retain historical integration; add a view+DB component boundary candidate for QA. |
| `students.tests.StudentManagementViewTests.test_warden_can_register_student` — [source](../../students/tests.py) | Redirect and created Student existence; no AuditEvent assertion. Same separate boundary candidate, without changing historical selection. |
| `accounts.tests.AuthenticationTests.test_admin_can_create_and_deactivate_accounts` — [source](../../accounts/tests.py) | Creation, password verification and deactivation. Audited code executes, but auditing is not asserted. Persisted lifecycle integration remains defensible. |
| `StudentModelTests.test_student_can_be_deactivated_without_deleting_record` | `Student.save()` locks/queries Student and checks active Allocations even without an allocation fixture. |
| `HostelModelBehaviorTests.test_reducing_capacity_removes_unallocated_beds` | `Room.save()` queries allocation history while removing Room-owned Beds; disclose the relationship. |
| `StudentSelfServiceTests.test_student_account_picker_excludes_staff_and_accounts_linked_elsewhere` | Form contract uses an actual User↔Student relational queryset; it is not isolated. |
| `StudentSelfServiceTests.test_student_dates_are_dd_mm_yyyy_and_keep_vacated_fallback` | Presentation assertions execute inline allocation/release/payment setup too; the whole method context is not date-formatting-only coverage. |

Model `full_clean()` can query uniqueness/constraints on unsaved objects. `tests/factories.py` persists real records despite synthetic values. Stubbed admin-parent methods do not isolate tests persisting Users/Students and asserting AuditEvents. These are execution disclosures, not newly measured outcomes.

## Coverage interpretation and report procedure

Existing [metrics](evidence/issue42-main/coverage-metrics.json), [JUnit](evidence/issue42-main/junit-summary.json), [exact attribution](evidence/issue42-main/attribution.json) and [startup diagnostic](evidence/issue42-main/startup-context-diagnostic.json) retain their measured source/date. Mixed application statements are 1505/1677 (89.74%). Standalone76 is 1127/1677 (67.20%) including startup/shared setup, or 414/1677 (24.69%) in method contexts. Empty context has 735 statements, 713 empty-only and 22 overlapping. Do not add overlapping counts without subtracting overlap.

Empty context includes imports, declarations, shared fixtures and framework/database setup/teardown. Method contexts may include inline fixture/service work. Execution attribution does not establish assertion causality; the full-file denominator remains a proxy for application logic. Three selected JUnit passes have no measured application context: `HostelModelBehaviorTests.test_create_hostel`, `StudentModelTests.test_mobile_must_have_ten_digits` and `StudentModelTests.test_student_year_must_be_between_one_and_five`. Assign no invented coverage credit.

**SRS §6.4 unit70 remains UNPROVEN: neither PASS nor FAIL is established by these diagnostics.** The target concerns application logic, not the percentage of methods labelled unit.

1. Start from frozen190. Record historical category, asserted contract, dependencies, proposed scope, boundary rationale and actual QA disposition, incorporating the supplemental corrections.
2. Review the nine excluded primary-component borderlines, other flagged methods and two new successful-write boundary candidates with owners. Agree which DB-backed components satisfy the submitted definition. Publish any changed exact selection separately before measurement; do not relabel old rates.
3. Agree the application-logic denominator and attribution method with development/QA, disclosing setup/import limitations. Do not change exclusions/thresholds to achieve a percentage.
4. When refreshed measurement is needed, run serially against a verified disposable test DB. Retain clean source/tree, commands, dependencies, selected IDs, JUnit failures/errors/skips and raw evidence. Reuse source-equivalent historical evidence only with explicit hash/scope reconciliation and its original date/revision.
5. Publish Vaishnavi's distinct `Unit_Test_Report.md` with module results, case/RTM links, classification decisions and honest coverage/target disposition. This owner handoff does not author or sign her report.

## Trigger for final development sign-off

Provide completed evidence and the proposed package revision through #38/#43. Development can then review revision differences, security findings, Unit Test Report/scope decisions, case/RTM/defect dispositions, final CI and package contents, and record a dated revision-bound ACCEPT or HOLD. QA/PO/guide decisions remain their own records. Until that evidence exists, keep #38/#43 OPEN and final development acceptance **HOLD**.
