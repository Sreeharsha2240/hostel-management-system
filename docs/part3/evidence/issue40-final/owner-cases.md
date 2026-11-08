# HMS-18 / #40 owner case appendix

**Current disposition, 8 November:** the [independent AI QA review](qa-review-20261108.md) accepts these 13 original cases and nine High/four Medium priorities for authorized #40 technical closure. It explicitly dispositions late review and bounded tool/environment evidence. Historical owner outcomes, original unspecified priorities and raw JSON remain unchanged; named final human approvals and whole-plan readiness remain pending.

Owner: Devansh Gupta (`DevaOnL`). This appendix supplies the original **13 owned cases** to the [HMS-15 / #37 case-document owner](https://github.com/Sreeharsha2240/hostel-management-system/issues/37) and [HMS-16 / #38 system-report owner](https://github.com/Sreeharsha2240/hostel-management-system/issues/38). It does not replace their team deliverables or transfer ownership of #39, #41, #42 or #43. Owner execution/handoff status is separate from QA case review, integrated system acceptance and PO signoff.

Fresh tested application: `0e358b4ce1fd02366184c7cb9c312b47dd093214`, tree `c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0`, clean at the recorded verification steps. Execution date: **5 November 2026**. The later evidence-only publication does not change the recorded tested source. See [the final execution record](README.md) for durable result artifacts, commands, hashes and environment limits.

## Original source and field conventions

Original case IDs, titles, requirement mappings, types, steps/inputs and expected results below are transcribed from [Test Plan revision 1.2, 7 October 2026, §13.1–13.2](../../../../Test_Plan_Hostel_Management_System.docx). DOCX line wrapping is normalized; no step or expected condition is removed. Requirement wording is from [SRS revision 1.2, §§5.4–5.6 and 6.1–6.2](../../../../SRS_Hostel_Management_System.docx). The original Test Plan provides **no per-case priority values**. Every case therefore retains its historical **Unspecified in original plan; QA review under #37** field; the linked 8 November review supplies the separate current #40 priority decision. SRS module priorities are not silently substituted for test-case priorities.

The original cases are system/operational execution cases. Their listed Django model/view/workflow/concurrency methods are automated component or integration companions. They retain the original case IDs; method counts are not additional original test cases. TC-OPS-01 retains the original plan's Functional type even though it traces to a nonfunctional requirement.

The plan's shared dummy-data provision includes male/female students, Boys/Girls hostels and users for each role. The owned browser fixture uses a Warden and linked Student login, male/female students and a Boys hostel to exercise the assigned cases; this appendix does not imply execution of every other owner's shared-data scenario. All data is synthetic. Disposable database suites run serially on `test_hms`; private recovery uses its separate synthetic server.

## Requirement traceability (original SRS text)

| Requirement | Original requirement | Owned case(s) |
|---|---|---|
| REQ-14 | The Admin or Warden shall be able to allocate an available bed to an active student, and the system shall save the allocation date and mark the bed Occupied in one atomic transaction. | TC-ALC-01 |
| REQ-15 | The system shall not allow allocation of an occupied bed, or allocation to a student who already has an active allocation, and shall show the reason. | TC-ALC-02, TC-ALC-03 |
| REQ-16 | The system shall allow allocation only if the student's gender matches the hostel type. | TC-ALC-04 |
| REQ-17 | The Admin or Warden shall be able to transfer a student to another available bed, and the old bed shall be released and the new bed occupied in one atomic transaction. | TC-ALC-05 |
| REQ-18 | The Admin or Warden shall be able to release an allocation by entering a vacate date, and the bed shall become "Available". | TC-ALC-06 |
| REQ-19 | The system shall keep all past allocations and show a student's allocation history in date order. | TC-ALC-06 |
| REQ-20 | The Admin or Warden shall be able to record a payment for a student with amount greater than zero, payment date, mode (Cash / UPI / Bank Transfer) and optional reference number. | TC-PAY-01 |
| REQ-21 | The system shall generate a receipt with a unique sequential receipt number for every payment, which can be viewed and downloaded as PDF. | TC-PAY-01 |
| REQ-22 | The system shall show the payment status of each student as Paid, Partial or Pending based on the payments recorded against the fee amount for the student's room type (Room Fee, Appendix B). | TC-PAY-02 |
| REQ-23 | The system shall generate an occupancy report for each hostel showing total beds, occupied beds, available beds and occupancy %, and a payment status report listing each student's fee amount, amount paid and status (Appendix B); both downloadable as CSV. | TC-RPT-01 |
| NFR-1 | At least 95% of page requests shall complete within 2 seconds with up to 50 users at the same time. | TC-PERF-01 |
| NFR-2 | Allocating a bed (REQ-14) shall take less than 3 seconds including saving to the database. | TC-PERF-02 |
| NFR-3 | The system shall support 5,000 student records and 2,000 beds without exceeding the response time in NFR-1. | TC-PERF-03 |
| NFR-4 | The database shall be backed up once every day and shall be restorable with at most 24 hours of data loss. | TC-OPS-01 |

REQ-23 also incorporates SRS Appendix B. Its occupancy fields are Hostel Name, Total Beds, Occupied Beds, Available Beds, Beds Under Maintenance and Occupancy %. Its payment fields are Student ID, Student Name, **Hostel / Room / Bed**, Fee Amount, Amount Paid and Payment Status. Both reports require CSV export. These are requirement-derived checks accompanying the original TC-RPT-01 text; the Bed field cannot be omitted from a complete-PASS claim.

## Owner execution register

PASS below means the owned expected behavior has observed execution evidence for the tested source. It is not a teammate approval or whole-Test-Plan exit decision. PENDING/FAIL/ERROR remain visible until their actual artifact supports a change. Browser TC-ALC-05 deliberately remains PARTIAL in its raw artifact; combined evidence supplies its injected failure and retry step.

| Original case | Original requirement(s) | Original type | Current owner execution |
|---|---|---|---|
| TC-ALC-01 — Allocate available bed | REQ-14 | Functional | PASS |
| TC-ALC-02 — Block allocation of occupied bed | REQ-15 | Functional | PASS |
| TC-ALC-03 — Block second allocation for a student | REQ-15 | Functional | PASS |
| TC-ALC-04 — Gender and hostel type mismatch | REQ-16 | Functional | PASS |
| TC-ALC-05 — Transfer student | REQ-17 | Functional | PASS (combined evidence) |
| TC-ALC-06 — Release allocation and history | REQ-18, REQ-19 | Functional | PASS |
| TC-PAY-01 — Record payment and receipt | REQ-20, REQ-21 | Functional | PASS |
| TC-PAY-02 — Payment status | REQ-22 | Functional | PASS |
| TC-RPT-01 — Occupancy report | REQ-23 | Functional | PASS |
| TC-PERF-01 — Response time under load | NFR-1 | Performance | PASS |
| TC-PERF-02 — Allocation time and concurrency | NFR-2 | Performance | PASS |
| TC-PERF-03 — Data volume | NFR-3 | Performance | PASS |
| TC-OPS-01 — Backup and restore | NFR-4 | Functional | PASS |

Fresh supporting checks: repository runner **190 methods**, zero failures/errors, **1 deliberate coverage timing skip** followed by a separate passing timing run; focused allocation/payment/report/journey/self-service execution **71 passed**; offline recovery safety **32 passed**. These are mixed/component/integration verification counts, not the Test Plan's case denominator or a unit-only coverage claim.

## TC-ALC-01 — Allocate available bed

**Owner:** Devansh Gupta. **Original requirement(s):** REQ-14. **Original type:** Functional. **Priority:** Unspecified in original plan; QA review under #37.

**Original steps / input:**

> Select an active male student and an available bed in the Boys hostel; confirm.

**Original expected result:**

> Allocation saved with date; bed status becomes Occupied; confirmation shown.

**Execution prerequisites/data:** Warden `issue40-warden`; active male `PES1UG24CS101`; Boys hostel `Issue40 Boys`; available `I401-A`; run-local allocation date.

**Actual result / status — PASS:** Browser form saved allocation/date and displayed confirmation; a separate bed-list page showed Occupied after commit.

**Current automated cross-reference(s):**

- Browser/HTTP method: [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../../../scripts/part3/test_issue40_browser.py#L45); raw observation `TC-ALC-01` in `browser/browser-results.json`.
- [`allocations.tests.AllocationViewTests.test_admin_can_create_allocation`](../../../../allocations/tests.py#L146).
- [`allocations.tests.AllocationModelTests.test_active_allocation_occupies_bed`](../../../../allocations/tests.py#L21).
- [`allocations.tests.AllocationViewTests.test_allocation_creation_rolls_back_if_audit_event_fails`](../../../../allocations/tests.py#L176).

## TC-ALC-02 — Block allocation of occupied bed

**Owner:** Devansh Gupta. **Original requirement(s):** REQ-15. **Original type:** Functional. **Priority:** Unspecified in original plan; QA review under #37.

**Original steps / input:**

> Try to allocate an already occupied bed to another student.

**Original expected result:**

> Request rejected with reason; no second active allocation exists for the bed.

**Execution prerequisites/data:** A stale browser form for male `PES1UG24CS102` selects `I401-A` before TC-ALC-01 occupies it, then submits after the first allocation commits.

**Actual result / status — PASS:** A different student using a stale form was rejected with the occupied-bed reason; no duplicate allocation.

**Current automated cross-reference(s):**

- Browser/HTTP method: [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../../../scripts/part3/test_issue40_browser.py#L45); raw observation `TC-ALC-02` in `browser/browser-results.json`.
- [`allocations.test_workflows.AllocationWorkflowTests.test_json_workflow_conflicts_validation_and_permissions`](../../../../allocations/test_workflows.py#L415).
- [`allocations.tests.AllocationModelTests.test_bed_cannot_have_two_active_allocations`](../../../../allocations/tests.py#L48).

## TC-ALC-03 — Block second allocation for a student

**Owner:** Devansh Gupta. **Original requirement(s):** REQ-15. **Original type:** Functional. **Priority:** Unspecified in original plan; QA review under #37.

**Original steps / input:**

> Try to allocate a second bed to a student who already has an active allocation.

**Original expected result:**

> Request rejected with reason; original allocation unchanged.

**Execution prerequisites/data:** A stale form for the same `PES1UG24CS101` selects available `I402-A` and submits after the original allocation commits.

**Actual result / status — PASS:** Second allocation for the same student was rejected; original ID and bed unchanged.

**Current automated cross-reference(s):**

- Browser/HTTP method: [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../../../scripts/part3/test_issue40_browser.py#L45); raw observation `TC-ALC-03` in `browser/browser-results.json`.
- [`allocations.test_workflows.AllocationWorkflowTests.test_json_workflow_conflicts_validation_and_permissions`](../../../../allocations/test_workflows.py#L415).
- [`allocations.tests.AllocationModelTests.test_student_cannot_have_two_active_allocations`](../../../../allocations/tests.py#L36).

## TC-ALC-04 — Gender and hostel type mismatch

**Owner:** Devansh Gupta. **Original requirement(s):** REQ-16. **Original type:** Functional. **Priority:** Unspecified in original plan; QA review under #37.

**Original steps / input:**

> Try to allocate a female student to a bed in a Boys hostel.

**Original expected result:**

> Allocation rejected with a gender mismatch message.

**Execution prerequisites/data:** Female `PES1UG24CS103`; available `I402-A` in the Boys hostel.

**Actual result / status — PASS:** Browser rejected female student / Boys hostel with a gender mismatch reason; MySQL verifies no write.

**Current automated cross-reference(s):**

- Browser/HTTP method: [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../../../scripts/part3/test_issue40_browser.py#L45); raw observation `TC-ALC-04` in `browser/browser-results.json`.
- [`allocations.test_workflows.AllocationWorkflowTests.test_invalid_eligibility_gender_status_and_dates_are_rejected`](../../../../allocations/test_workflows.py#L174).

## TC-ALC-05 — Transfer student

**Owner:** Devansh Gupta. **Original requirement(s):** REQ-17. **Original type:** Functional. **Priority:** Unspecified in original plan; QA review under #37.

**Original steps / input:**

> 1. Transfer an allocated student to another available bed. 2. Force a failure while saving the new bed (for example, DB error in test) and retry.

**Original expected result:**

> Step 1: old bed Available, new bed Occupied. Step 2: transaction rolled back, old allocation still active (atomic).

**Execution prerequisites/data:** Browser transfers the TC-ALC-01 allocation from `I401-A` to `I402-A`. The companion's independent fixture uses the same original allocation/student/target for its forced `Bed.save` failure and retry.

**Actual result / status — PASS (combined evidence):** Transfer confirmation was cancelled with zero POSTs and unchanged allocation/bed states, then accepted once to preserve original and create successor; storage-failure rollback requires the companion regression. The fresh focused method `test_transfer_failure_rolls_back_both_beds_and_history` passed: it injects a target-bed save failure, checks original active allocation/both beds/history and unchanged audit count, removes the fault, retries the same transfer, and verifies the successor, both bed states, preserved history and exactly one attributed transfer audit. Browser-only status remains PARTIAL.

**Current automated cross-reference(s):**

- Browser/HTTP method: [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../../../scripts/part3/test_issue40_browser.py#L45); raw observation `TC-ALC-05` in `browser/browser-results.json`.
- [`allocations.test_workflows.AllocationWorkflowTests.test_transfer_and_release_preserve_history_and_emit_actor_audit`](../../../../allocations/test_workflows.py#L142).
- [`allocations.test_workflows.AllocationWorkflowTests.test_transfer_failure_rolls_back_both_beds_and_history`](../../../../allocations/test_workflows.py#L234).
- [`allocations.test_workflows.AllocationWorkflowTests.test_only_transfer_and_release_forms_require_submit_confirmation`](../../../../allocations/test_workflows.py#L39).

## TC-ALC-06 — Release allocation and history

**Owner:** Devansh Gupta. **Original requirement(s):** REQ-18, REQ-19. **Original type:** Functional. **Priority:** Unspecified in original plan; QA review under #37.

**Original steps / input:**

> 1. Release an allocation with a vacate date. 2. Open the student's allocation history.

**Original expected result:**

> Bed becomes Available; vacate date stored; history lists all past and current allocations in date order.

**Execution prerequisites/data:** Browser releases the transfer successor using the run-local vacate date. The companion creates three valid nonoverlapping stays with allocation dates opposing insertion/primary-key order.

**Actual result / status — PASS:** Release confirmation was cancelled with zero POSTs and unchanged allocation/bed states, then accepted once; list/history show DD-MM-YYYY while JSON retains ISO dates. Fresh `test_history_orders_backdated_records_by_allocation_date_in_json_and_html` passed for distinct counterordered dates, supplying date-order proof beyond the browser's same-day records.

**Current automated cross-reference(s):**

- Browser/HTTP method: [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../../../scripts/part3/test_issue40_browser.py#L45); raw observation `TC-ALC-06` in `browser/browser-results.json`.
- [`allocations.test_workflows.AllocationWorkflowTests.test_transfer_and_release_preserve_history_and_emit_actor_audit`](../../../../allocations/test_workflows.py#L142).
- [`allocations.test_workflows.AllocationWorkflowTests.test_history_orders_backdated_records_by_allocation_date_in_json_and_html`](../../../../allocations/test_workflows.py#L304).

## TC-PAY-01 — Record payment and receipt

**Owner:** Devansh Gupta. **Original requirement(s):** REQ-20, REQ-21. **Original type:** Functional. **Priority:** Unspecified in original plan; QA review under #37.

**Original steps / input:**

> 1. Record payment (amount 5000, UPI, date, reference). 2. Record a payment with amount 0 and one with negative amount. 3. Download the receipt.

**Original expected result:**

> Step 1 saved with a unique sequential receipt number. Step 2 rejected. Step 3 gives a PDF receipt with correct details.

**Execution prerequisites/data:** `PES1UG24CS101`; INR 5,000 UPI payment, run-local date, reference `PART340A`; invalid amounts 0 and -1; PDF for the first receipt; second INR 5,000 payment in TC-PAY-02 supplies a consecutive receipt comparison.

**Actual result / status — PASS:** Browser recorded INR 5000 UPI payment and downloaded PDF; zero/negative submissions displayed server-side form-validation errors (HTTP 200), without additional receipts.

**Current automated cross-reference(s):**

- Browser/HTTP method: [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../../../scripts/part3/test_issue40_browser.py#L45); raw observation `TC-PAY-01` in `browser/browser-results.json`.
- [`payments.test_workflows.PaymentWorkflowTests.test_invalid_amounts_modes_dates_and_references_do_not_consume_numbers`](../../../../payments/test_workflows.py#L91).
- [`payments.test_workflows.PaymentWorkflowTests.test_json_workflow_receipts_adjustments_and_real_pdf_contents`](../../../../payments/test_workflows.py#L311).
- [`payments.test_workflows.PaymentConcurrencyTests.test_simultaneous_payments_receive_unique_sequential_numbers`](../../../../payments/test_workflows.py#L549).

## TC-PAY-02 — Payment status

**Owner:** Devansh Gupta. **Original requirement(s):** REQ-22. **Original type:** Functional. **Priority:** Unspecified in original plan; QA review under #37.

**Original steps / input:**

> Record no payment, then partial payment, then full payment for a student.

**Original expected result:**

> Status shows Pending, then Partial, then Paid.

**Execution prerequisites/data:** Configured room fee INR 10,000; no payment, INR 5,000 partial payment, then another INR 5,000 payment (`PART340B`).

**Actual result / status — PASS:** Browser payment statuses: Pending -> Partial -> Paid; final paid INR 10000, due INR 0 checked in MySQL.

**Current automated cross-reference(s):**

- Browser/HTTP method: [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../../../scripts/part3/test_issue40_browser.py#L45); raw observation `TC-PAY-02` in `browser/browser-results.json`.
- [`payments.test_workflows.PaymentWorkflowTests.test_status_tracks_pending_partial_paid_and_adjustments_without_join_multiplication`](../../../../payments/test_workflows.py#L218).
- [`payments.test_workflows.PaymentWorkflowTests.test_no_allocation_or_unconfigured_fee_remains_pending_with_advance_payment`](../../../../payments/test_workflows.py#L253).

## TC-RPT-01 — Occupancy report

**Owner:** Devansh Gupta. **Original requirement(s):** REQ-23. **Original type:** Functional. **Priority:** Unspecified in original plan; QA review under #37.

**Original steps / input:**

> Open the occupancy report and the payment status report for a hostel with known counts; export CSV for both.

**Original expected result:**

> Total, occupied, available beds and occupancy % match database counts; CSV downloads with same values.

**Execution prerequisites/data:** Known Boys-hostel fixture: five beds (one occupied, three available, one maintenance); released `PES1UG24CS101` has last historical bed `I402-A` and INR 10,000 paid; resident `PES1UG24CS104` has `I401-C` and no payment.

**Actual result / status — PASS:** Browser filtered both reports and downloaded CSV; payment HTML/JSON identify the latest historical Bed after Room, with Python reconciling HTML/CSV/JSON against MySQL.

**Current automated cross-reference(s):**

- Browser/HTTP method: [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../../../scripts/part3/test_issue40_browser.py#L45); raw observation `TC-RPT-01` in `browser/browser-results.json`.
- [`reports.test_reports.ReportTests.test_occupancy_counts_current_records_maintenance_and_empty_hostels`](../../../../reports/test_reports.py#L56).
- [`reports.test_reports.ReportTests.test_occupancy_csv_and_html_match_json_and_preserve_filters`](../../../../reports/test_reports.py#L93).
- [`reports.test_reports.ReportTests.test_payment_report_sums_once_across_allocation_history_and_filters_last_room`](../../../../reports/test_reports.py#L117).
- [`reports.test_reports.ReportTests.test_payment_report_excludes_cancelled_locations_and_keeps_unassigned_blank`](../../../../reports/test_reports.py#L176).
- [`reports.test_reports.ReportTests.test_payment_report_csv_and_html_match_json_after_corrections`](../../../../reports/test_reports.py#L218).
- Requirement-derived result also checks `Bed` in HTML headings/rows, JSON and CSV, including transfer/released history, cancelled-only and unassigned records, filters and monetary totals. This corrects defect #45 and the earlier incomplete-PASS inference.

## TC-PERF-01 — Response time under load

**Owner:** Devansh Gupta. **Original requirement(s):** NFR-1. **Original type:** Performance. **Priority:** Unspecified in original plan; QA review under #37.

**Original steps / input:**

> JMeter: 50 concurrent users for 10 minutes doing login, student search and available-beds view.

**Original expected result:**

> At least 95% of requests complete within 2 seconds; no errors.

**Execution prerequisites/data:** Baseline: exactly 100 synthetic students and 80 available beds, 50 distinct Warden sessions with normal password hashing/audit writes; login form/login, authenticated student search and available-bed requests; five-second ramp, shared barrier, one-second think time, at least 600 measured seconds per user.

**Actual result / status — PASS:** Fresh `baseline` scenario is PASS in `load-results.json`; fixture counts, complete 50-user measurement windows, route/thread results, timings and raw SHA-256 values are retained there and summarized in [the final evidence](README.md).

**Current automated cross-reference(s):**

- [`scripts.part3.test_issue40_load.Issue40LoadExecution.test_baseline_and_volume_jmeter`](../../../../scripts/part3/test_issue40_load.py#L178).
- Harness: [JMeter plan](../../../../scripts/part3/issue40_load.jmx) and [guarded load runner](../../../../scripts/part3/run_issue40_load.py); only full PASS scenario artifacts establish acceptance, not a smoke run.

## TC-PERF-02 — Allocation time and concurrency

**Owner:** Devansh Gupta. **Original requirement(s):** NFR-2. **Original type:** Performance. **Priority:** Unspecified in original plan; QA review under #37.

**Original steps / input:**

> 1. Allocate beds 20 times and measure time. 2. Send two simultaneous requests for the same bed.

**Original expected result:**

> Each allocation takes under 3 seconds. Only one concurrent request succeeds; the bed has exactly one active allocation.

**Execution prerequisites/data:** 20 active male synthetic students `PES1UG24CS200`–`219`, each with a separate available single-room bed; two additional students `PES1UG24CS300`/`301` submit overlapping requests for one separate conflict bed.

**Actual result / status — PASS:** 20 successful real HTTP allocations with durable commits; overlapping client same-bed requests returned one 201 and one 409; MySQL verifies a single winner. Observed committed response intervals were 32.20–42.38 ms (median 35.93 ms); the client intervals overlap and HTTP statuses are 201/409.

**Current automated cross-reference(s):**

- Browser/HTTP method: [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../../../scripts/part3/test_issue40_browser.py#L45); raw observation `TC-PERF-02` in `browser/browser-results.json`.
- [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../../../scripts/part3/test_issue40_browser.py#L45).
- [`allocations.test_workflows.AllocationConcurrencyTests.test_simultaneous_same_bed_or_same_student_has_one_winner`](../../../../allocations/test_workflows.py#L555).

## TC-PERF-03 — Data volume

**Owner:** Devansh Gupta. **Original requirement(s):** NFR-3. **Original type:** Performance. **Priority:** Unspecified in original plan; QA review under #37.

**Original steps / input:**

> Load 5,000 students and 2,000 beds; repeat TC-PERF-01 and student search.

**Original expected result:**

> Response times still meet NFR-1; search returns within 2 seconds.

**Execution prerequisites/data:** Volume: exactly 5,000 synthetic students and 2,000 available beds; the same 50-user, full-ten-minute workload and an additional every-search-under-two-seconds gate.

**Actual result / status — PASS:** Fresh `volume` scenario is PASS in `load-results.json`; fixture counts, complete 50-user measurement windows, route/thread results, timings and raw SHA-256 values are retained there and summarized in [the final evidence](README.md).

**Current automated cross-reference(s):**

- [`scripts.part3.test_issue40_load.Issue40LoadExecution.test_baseline_and_volume_jmeter`](../../../../scripts/part3/test_issue40_load.py#L178).
- Harness: [JMeter plan](../../../../scripts/part3/issue40_load.jmx) and [guarded load runner](../../../../scripts/part3/run_issue40_load.py); only full PASS scenario artifacts establish acceptance, not a smoke run.

## TC-OPS-01 — Backup and restore

**Owner:** Devansh Gupta. **Original requirement(s):** NFR-4. **Original type:** Functional. **Priority:** Unspecified in original plan; QA review under #37.

**Original steps / input:**

> Check that the daily backup job ran; restore the latest backup into a test database.

**Original expected result:**

> Backup file exists for the last 24 hours; restore succeeds and data is complete up to the backup time.

**Execution prerequisites/data:** A separate, previously owned private MySQL synthetic source, a newly naturally scheduled private backup, and a previously absent test restore database. Actual populated counts, backup age, digest/consistency results and cleanup must come from the completed recovery artifact; no live source is seeded or restored.

**Actual result / status — PASS:** Fresh recovery status is `PASS`; [the final evidence](README.md) records the natural daily trigger, populated restore digests/consistency checks, backup age, unchanged live task definition and owned-resource cleanup. The synthetic restore and the preserved installed live daily job are separate observations.

**Current automated cross-reference(s):**

- [`scripts.part3.test_issue40_recovery_safety.RecoverySafetyTests.test_existing_restore_target_is_never_overwritten_or_dropped`](../../../../scripts/part3/test_issue40_recovery_safety.py#L451).
- [`scripts.part3.test_issue40_recovery_safety.RecoverySafetyTests.test_tampered_dump_is_refused_before_target_connection`](../../../../scripts/part3/test_issue40_recovery_safety.py#L505).
- [`scripts.part3.test_issue40_recovery_safety.RecoverySafetyTests.test_recovery_fails_on_logical_inconsistency_and_still_drops_owned_target`](../../../../scripts/part3/test_issue40_recovery_safety.py#L517).
- Operational implementation: [backup/restore helpers](../../../../scripts/part3/backup_issue40.py) and [recovery runner](../../../../scripts/part3/run_issue40_recovery.py), plus the fresh source-bound private orchestration archived/hash-referenced in the final evidence. The listed safety tests verify guards; they do not by themselves prove a populated restore or daily scheduler execution.

## Defects, corrections and retest provenance

The earlier [issue40 JSON](../issue40/reverification.json), [completion artifacts](../issue40/README.md) and [4 November defect retest](../owned-defects/retest.json) remain unchanged. Their source hashes, dates, failures and then-pending fields are historical observations; the fresh appendix supersedes only their aggregate completeness inference for the current revision.

| Item | What was corrected | Current evidence / boundary |
|---|---|---|
| RV-01 | Backup output accepted repository ancestors and could change their permissions. | Resolved repository/ancestor/root refusal occurs before mkdir/ACL changes. Historical old-code negative proof is retained; current 32-method safety execution includes ancestor/direct-helper/error-path guards. |
| RV-02 | Removing inherited ACLs left a pre-existing explicit Everyone Allow grant. | Guard refuses unrelated explicit grants/untrusted owners and checks the protected result. Historical real Windows negative/positive ACL proofs remain historical; the fresh safety suite reruns the guards. |
| RV-03 / TC-ALC-05 | The earlier fault-injection method verified rollback but stopped before retry. | Fresh same-transfer rollback-and-retry method passes. Browser-only result remains PARTIAL; combined case status identifies its companion explicitly. |
| RV-04 / TC-ALC-06 | Same-day fixtures did not prove allocation-date order. | Fresh counterordered-date JSON/HTML method passes. Historical deliberate PK-only-order negative control remains preserved; no new negative-control run is invented. |
| [#45](https://github.com/Sreeharsha2240/hostel-management-system/issues/45) | Payment status report omitted Bed required by REQ-23 / Appendix B. Earlier TC-RPT-01 complete-PASS claim was incomplete. | CLOSED; implemented in merged [PR #44](https://github.com/Sreeharsha2240/hostel-management-system/pull/44). Fresh browser reconciles HTML/CSV/JSON with MySQL, and current report regressions check Bed across location/history edge cases. |
| [#46](https://github.com/Sreeharsha2240/hostel-management-system/issues/46) | SAD §4.5 transfer/release confirmation dialogs were missing. | CLOSED; merged PR #44. Fresh native Edge cancellation sends zero POSTs and preserves state; acceptance sends one POST/action. Release cancellation uses Enter from the date field. Creation requires no dialog. |
| [#47](https://github.com/Sreeharsha2240/hostel-management-system/issues/47) | Staff allocation list/history dates did not follow SRS §7 DD-MM-YYYY. | CLOSED; merged PR #44. Fresh browser checks list/history date cells; counterordered-date regression checks formatting/order, missing vacated-date fallback and unchanged ISO JSON. |
| [#48](https://github.com/Sreeharsha2240/hostel-management-system/issues/48) | Student self-service allocation/history/payment dates used `d M Y`. | CLOSED; Sreeharsha's implementation in merged [PR #49](https://github.com/Sreeharsha2240/hostel-management-system/pull/49). Fresh `students.test_self_service.StudentSelfServiceTests.test_student_dates_are_dd_mm_yyyy_and_keep_vacated_fallback` passes. The browser only checks student allocation/payment content integration; it does not assert every self-service date cell. Ownership remains Sreeharsha's. |

The #45–#47 historical negative controls specifically failed against original production code, then passed with the fixes restored. Their original logs/hashes are in the retained defect retest record. This final run reruns the corrected behavior; it does not relabel those older controls as fresh runs.

## Prior interrupted execution

The first current-source volume execution returned FAIL with 75 authenticated-content assertion errors after Windows recorded Modern Standby (lid) at 04:24:37 UTC and resumed at 04:59:11 UTC. Its raw results and all failures remain in `load-results.json` under `previous_attempts`; they are not relabelled PASS. Final TC-PERF-03 status uses the complete new 600-second volume-only rerun on identical clean source, fixtures, harness and thresholds. Session expiry is consistent with the errors around resume, but raw response bodies were not retained to prove that cause.

## Review and handoff boundary

Actual teammate integration is recorded: `harsha2240` merged Devansh's PR #44 on **5 November 2026 at 03:23:04 UTC** (merge `206a846`) and Sreeharsha's module follow-up PR #49 at **03:55:39 UTC** (merge/tested head `0e358b4`). The PR review arrays contain no formal `APPROVED` review. The teammate's merge of PR #44 establishes independent integration of Devansh's changes; it does not establish a separately recorded formal review or signed QA/PO approval. Automated/model audits and parallel agent verification are technical checks and are not independent teammate reviews.

The delivered #37 case document/RTM retains its historical fields; Vaishnavi coordinates remaining whole-plan priority, deviation and RTM acceptance; Sreeharsha retains #38's complete System Validation Report and integrated readiness; their other assignments stay with their owners. [PR #50](https://github.com/Sreeharsha2240/hostel-management-system/pull/50) was merged by `harsha2240` on **5 November 2026 at 06:31:28 UTC** as `8d60e83f1ce57ad99a2b2a22b3b5878f1390995b`. This records independent integration; its review array contains no formal `APPROVED` review. On 6 November, the [shared register](../../Test_Case_Document.md#53-hms-18-owner-execution-and-evidence-reconciliation) was reconciled to these 13 linked OWNER PASS results. At that historical checkpoint, issue #40 remained open pending reviewed-case/entry disposition and independent evidence acceptance; the linked 8 November review now resolves its scoped technical delivery; no team deliverable is marked finished by this appendix. Historical JSON retains its execution-time publication status unchanged. Final whole-plan entry/exit criteria, 33-case execution percentages, all-high-priority-case acceptance, all-requirement acceptance and actual PO signoff require their recorded decisions.

Recorded environment deviations remain visible for QA review: Edge/Playwright for the plan's named Selenium UI tool, MySQL 8.4.9 for MySQL 8.0, and local loopback Django HTTP with test-only secure redirect/cookie flags disabled. The full local JMeter/recovery measurements describe this candidate and host. They are not production HTTPS, service uptime, cross-browser compatibility or unit-attributable coverage evidence.

## Source fingerprints

| Reference | SHA-256 |
|---|---|
| `Test_Plan_Hostel_Management_System.docx` | `fec6b15aab87d2c91029937a4116a9fb26fd966ba26a4a3eec0d96cf158c78b3` |
| `SRS_Hostel_Management_System.docx` | `505b53c2cc66c631412db8bef9954ad49bf8c05ce3298db8699bcc781e5d311c` |

Original test-case fields above are extracted from these files, so the owner handoff can be reconciled with the baseline without silently editing the source plan or its historical JSON.
