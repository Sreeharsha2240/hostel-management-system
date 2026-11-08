# HMS-21 Final Readiness Checkpoint

**Checked:** 8 November 2026
**Reviewed main revision:** `b523d4c7abb77072bea48ac059be7f72396e8a79` (tree `56f7fb4307bc2ce4f3595aebfd5915ce301c3fb7`). Accepted final submission revision: **PENDING**.
**Readiness:** **NOT READY**. This checkpoint records verified deliverables and blockers; it is not an approval or submission receipt.

## Required Part 3 deliverables

| Deliverable | Current state | Remaining work |
|---|---|---|
| Test Case Document and RTM (#37) | Published through merged PR #60; #37 CLOSED for authorized documentation delivery: 61 complete case records and 36 core RTM rows, preserving original IDs/evidence. | Devansh authorized this documentation delivery without additional teammate messages. Actual case execution, priority agreement, historical entry/deviation acceptance and final QA/Dev/PO approvals remain distinct pending work. |
| Unit Test Report (#41) | **Missing** at `docs/part3/Unit_Test_Report.md`. | Vaishnavi and module owners must publish the current run, unit-level classification, scope/coverage disposition and evidence. Formal SRS unit70 remains unproven. |
| System Validation Report (#38) | Published through merged PR #59, with HMS-17/HMS-18 owner dispositions; this review adds consolidated metrics and explicit original-subcondition limits. | Maintain consolidated metrics and resolve remaining evidence/acceptance. TC-SEC-06 remains PARTIAL without real TLS evidence; the separate ZAP baseline is NOT RUN. Whole-plan readiness is NOT READY and approvals are pending. |
| Code Coverage Report (#42) | Published on main; PR #57 was independently reviewed and merged. | The reporting issue is closed, but unit70 interpretation remains unproven pending #41's scope/attribution agreement. |
| Branch Coverage Report (#42) | Published on main; PR #57 was independently reviewed and merged. | Same unit-scope limitation as the Code Coverage Report. |

The latest HMS-17 PR #58 merged as `896b4f3`; its tested tree is the same as the merge tree. Both CI jobs on that identical tree passed on Python 3.11 and 3.14. PR #59 then merged as `70c9fe2`, whose two main-branch CI jobs also passed. The corrected HMS-17 PR description preserves #39 as open. PR #60 then merged as `b523d4c`; [exact-main run 42399172513](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42399172513) passed both Python jobs. The 8 November [technical review and extraction](System_Validation_Report.md#independent-evidence-review-and-current-build) independently reconciles its 190 mixed identities (189 PASS / one expected SKIP), 12 gates and separate timing PASS per job. This is not a teammate signature, a new browser/load/recovery run or an accepted final package. The linked report records the original-subcondition evidence gaps, current metrics and required owner actions.

## Current issue dependencies

| Issue | State | Remaining readiness dependency |
|---|---|---|
| #37 HMS-15 | Closed — documentation delivered through PR #60 | Complete records, mappings and evidence reconciliation are delivered under Devansh's explicit instruction. The document retains execution gaps and proposed-priority/acceptance limits; closing this delivery does not complete the whole Test Plan. |
| #38 HMS-16 | Open | PR #59 is merged. Obtain the missing TLS/ZAP evidence or an actual authorized criterion change, integrate remaining case results/metrics, and record real QA/Dev/PO decisions. The old Windows failure/count remains honestly recorded as unreconciled historical evidence. |
| #39 HMS-17 | Open | PR #58 is merged; TC-STU-01 is NOT RUN for lack of case-specific evidence, TC-QUAL-01 is PARTIAL without a timed new-Warden guide walkthrough, and other issue-level SRS coverage remains outstanding. |
| #40 HMS-18 | Open | Owner evidence is published; QA still needs reviewed-case/entry disposition, priority review and environment/tool-deviation acceptance. All 13 original cases retain OWNER PASS observations; TC-ALC-05 preserves raw browser PARTIAL plus its passing rollback/same-transfer-retry companion. No new QA acceptance is inferred. |
| #41 HMS-19 | Open | Publish the missing Unit Test Report; classify unit versus integration/system tests and disposition the formal unit70 target. |
| #42 HMS-20 | Closed | Coverage reports are published and the reporting task is complete; the separate unit70 result is still UNPROVEN. |
| #43 HMS-21 | Open | Final submission cannot be approved until required reports, case reviews, entry/exit criteria, actual approvals and submission instructions/receipt are resolved. |

## Team review and pending decisions — 8 November 2026

An assisted development technical review of the published report/evidence is now recorded in the [System Validation Report](System_Validation_Report.md#team-actions-and-actual-approvals). Three fresh reviewers checked security assertions, counts/coverage, and original assignment/readiness requirements. Its corrections preserve all historical owner observations and do not supply human QA/Dev/PO final attestations. No new Harsha PR was open at the reviewed snapshot.

| Required action | Owner and concrete next step | Current state |
|---|---|---|
| Case outcomes, proposed priorities, RTM and deviations | Vaishnavi coordinates actual review with each case owner, identifying revision/evidence, original entry gaps and accepted environment/tool changes. | PENDING; no case status or priority is approved by this document edit. |
| Missing HTTPS/TLS and ZAP | Sreeharsha #38 collects isolated real transport/cookie evidence and the separate baseline. Development recommendation is to retain original criteria. | TC-SEC-06 PARTIAL; TC-SEC-08 NOT RUN. No actual team/instructor criterion change is supplied. |
| Unit Test Report | Vaishnavi #41 uses module-owner inputs, reviews unit/integration boundaries, denominator and attribution, then publishes her report. Devansh supplies the [exact existing module input](Code_Coverage_Report.md#hms-19-module-owner-input--8-november-2026). | Missing; SRS unit70 UNPROVEN. #42 reporting remains closed. |
| Remaining cases / quality | Existing case owners supply real execution or genuine authorized disposition of partial, unrun and blocked conditions. | Original 33: 30 OWNER PASS / 2 PARTIAL / 1 NOT RUN. Expanded 61: 39 OWNER PASS / 3 PARTIAL / 18 NOT RUN / 1 BLOCKED. |
| Actual final QA / Dev / PO decisions and guide walkthrough | Vaishnavi / Devansh / Sreeharsha and the actual guide each supply their own dated revision-bound record. | PENDING; technical reviews and PR approvals have limited scopes. |
| Instructor instructions and actual submission | Sreeharsha confirms real channel/cutoff/timezone/format, authentic recordings, complete accepted package and safe receipt. | PENDING; no format, extension, receipt or cutoff hour is invented. |

The report now calculates 32/33 (96.97%) original and 42/61 (68.85%) expanded cases with any exercise, including PARTIAL; these are not completed-case acceptance. Owner-pass proportions are 30/33 (90.91%) and 39/61 (63.93%). All 36 RTM rows have owner-pass mappings, but the Plan's accepted-passed-case requirement metric and complete-condition assessment remain UNVERIFIED. Four known bug-labelled issues are closed with actual ages; their severities are UNKNOWN and a complete severity-ranked inventory is not established. See the [metrics and limits](System_Validation_Report.md#consolidated-case-requirement-and-defect-metrics--8-november-2026).

## Submission checks

- **Test Plan exit criteria:** NOT MET / UNVERIFIED. The record does not establish 100% planned cases executed, all High-priority cases passed, zero open critical/high defects, or a passed case for every RTM requirement. Priority values and case acceptance still need review.
- **Team acceptance:** No complete QA/Dev/PO approval set or guide acceptance walkthrough is recorded. CI and merged PRs do not substitute for those decisions.
- **Videos:** Earlier tracked-file checks found no Sprint 1 one-minute or Sprint 2 two-minute outcome video. Locate genuine team recordings or record this submission gap; do not fabricate videos.
- **Instructor requirements:** The Part 3 PDF gives a 2–6 November window but no cutoff hour or export format. Confirm the actual submission channel, cutoff and required format with the instructor.
- **Final package:** No accepted final submission revision or submission receipt is recorded. Select the revision only after reviews and required reports are complete; run final tree/CI/secret checks on that revision and record the real receipt/link.

## Decision

Keep HMS-21 open and the submission marked **NOT READY**. HMS-15's case-document delivery and PR #59's report publication do not supply missing execution or approvals. Obtain the Unit Test Report, execute/dispose the remaining cases and priorities, update consolidated metrics, record actual team/instructor decisions, and then complete the final package and submission checks. No teammate approval is inferred by this checkpoint.
