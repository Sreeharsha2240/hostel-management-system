# HMS-21 Final Readiness Checkpoint

**Checkpoint started:** 8 November 2026; security evidence updated 9 November 2026
**Reviewed main revision:** `b523d4c7abb77072bea48ac059be7f72396e8a79` (tree `56f7fb4307bc2ce4f3595aebfd5915ce301c3fb7`). Accepted final submission revision: **PENDING**.
**Readiness:** **NOT READY**. This checkpoint records verified deliverables and blockers; it is not an approval or submission receipt.

**9 November HMS-16 evidence update:** isolated local TLS/HTTPS checks now pass and a ZAP 2.17.0 passive baseline completed. The app CSP and CSRF-cookie findings were corrected and absent on rescan. The remaining ZAP low server-banner finding is specific to the local Python WSGI probe server; its informational `next`-parameter hotspot awaits QA disposition. See the [transport/ZAP evidence](evidence/issue38-security-20261109/README.md). #38 still needs QA disposition and team approvals; #43 remains NOT READY for the independent report, case-review, approval, instructor and actual submission requirements below.

**Current-main development addendum — 8 November 2026:** [Development review and #41 classification handoff](Development_Review_20261108.md) reviews `cae69ea2192838b7874ad5be240def842f5aab5e` (tree `4f81f4a5e100f6a3f22505acfa05b4dd0ff9bb1f`). PR #64 and [exact-main CI 42461981682](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42461981682) are successful; #40 and #63 are CLOSED. Final development acceptance remains **HOLD** pending the remaining evidence and final package. The earlier review revision and historical measurements below are preserved.

**HMS-17 follow-up — 8 November 2026:** [PR #66 reconciliation](evidence/issue39/followup-20261108.md) accepts two historical automated recipes (S1-07/S2-07), with actual 7 November source/run provenance, and corrects unsupported complete passes. At the 8 November snapshot, expanded totals were 50 OWNER PASS / 3 PARTIAL / 7 NOT RUN / 1 BLOCKED; the 9 November ZAP execution subsequently updates current totals below. Original 33 dispositions remain unchanged. New screenshots support limited page/allocation observations; #39 remains OPEN for the original registration, guide/quality and broader coverage gaps. No final acceptance or unit70 change is supplied.

## Required Part 3 deliverables

| Deliverable | Current state | Remaining work |
|---|---|---|
| Test Case Document and RTM (#37) | Published through merged PR #60; #37 CLOSED for authorized documentation delivery: 61 complete case records and 36 core RTM rows, preserving original IDs/evidence. | Devansh authorized this documentation delivery without additional teammate messages. Actual case execution, priority agreement, historical entry/deviation acceptance and final QA/Dev/PO approvals remain distinct pending work. |
| Unit Test Report (#41) | **Missing** at `docs/part3/Unit_Test_Report.md`. | Vaishnavi and module owners must publish the current run, unit-level classification, scope/coverage disposition and evidence. Formal SRS unit70 remains unproven. |
| System Validation Report (#38) | Published through merged PR #59, with HMS-17/HMS-18 owner dispositions; 9 November transport/ZAP evidence is added in this branch. | Integrate the local TLS pass and ZAP alert dispositions. QA acceptance and real QA/Dev/PO approvals remain pending; whole-plan readiness is NOT READY. |
| Code Coverage Report (#42) | Published on main; PR #57 was independently reviewed and merged. | The reporting issue is closed, but unit70 interpretation remains unproven pending #41's scope/attribution agreement. |
| Branch Coverage Report (#42) | Published on main; PR #57 was independently reviewed and merged. | Same unit-scope limitation as the Code Coverage Report. |

The latest HMS-17 PR #58 merged as `896b4f3`; its tested tree is the same as the merge tree. Both CI jobs on that identical tree passed on Python 3.11 and 3.14. PR #59 then merged as `70c9fe2`, whose two main-branch CI jobs also passed. The corrected HMS-17 PR description preserves #39 as open. PR #60 then merged as `b523d4c`; [exact-main run 42399172513](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42399172513) passed both Python jobs. The 8 November [technical review and extraction](System_Validation_Report.md#independent-evidence-review-and-current-build) independently reconciles its 190 mixed identities (189 PASS / one expected SKIP), 12 gates and separate timing PASS per job. This is not a teammate signature, a new browser/load/recovery run or an accepted final package. The linked report records the original-subcondition evidence gaps, current metrics and required owner actions.

## Current issue dependencies

| Issue | State | Remaining readiness dependency |
|---|---|---|
| #37 HMS-15 | Closed — documentation delivered through PR #60 | Complete records, mappings and evidence reconciliation are delivered under Devansh's explicit instruction. The document retains execution gaps and proposed-priority/acceptance limits; closing this delivery does not complete the whole Test Plan. |
| #38 HMS-16 | Open | Local TLS checks and the passive ZAP baseline are recorded in this branch. QA must disposition the local WSGI server-banner finding and informational `next`-parameter hotspot, then review integrated results and record actual QA/Dev/PO decisions. The old Windows failure/count remains honestly recorded as unreconciled historical evidence. |
| #39 HMS-17 | Open | PR #58 is merged; TC-STU-01 is NOT RUN for lack of case-specific evidence, TC-QUAL-01 is PARTIAL without a timed new-Warden guide walkthrough, and other issue-level SRS coverage remains outstanding. |
| #40 HMS-18 | CLOSED — scoped technical delivery accepted | [8 November independent AI QA](evidence/issue40-final/qa-review-20261108.md), expressly authorized by Devansh, accepts the original 13 cases with current-priority, late-entry and bounded tool/environment dispositions. That #40 review preserved OWNER PASS observations, raw browser PARTIAL and expanded-case statuses; the separate #63 follow-up below subsequently executes nine expanded recipes. Actual named human final approvals and whole-plan acceptance remain pending. |
| #41 HMS-19 | Open | Publish the missing Unit Test Report; classify unit versus integration/system tests and disposition the formal unit70 target. |
| #42 HMS-20 | Closed | Coverage reports are published and the reporting task is complete; the separate unit70 result is still UNPROVEN. |
| #63 HMS-26 | CLOSED — PR #64 merged and exact-main CI verified | [Nine remaining Devansh-owned recipes](evidence/issue63/README.md) passed on clean `6636098cb728aa17c2abf5e42c358a5d400261e7` after independent pre-execution review, then in both Python jobs of main CI 42461981682 at `cae69ea`. Other owners and final acceptance remain separate. |
| #43 HMS-21 | Open | Before submission, resolve required reports, case reviews, entry/exit criteria, actual approvals and instructor instructions. Record the genuine receipt after submission to complete #43; the receipt is not a prerequisite for reviewing the package. |

## Team review and pending decisions — 8 November 2026

An assisted development technical review of the published report/evidence is now recorded in the [System Validation Report](System_Validation_Report.md#team-actions-and-actual-approvals). Three fresh reviewers checked security assertions, counts/coverage, and original assignment/readiness requirements. Its corrections preserve all historical owner observations and do not supply human QA/Dev/PO final attestations. No new Harsha PR was open at the reviewed snapshot.

| Required action | Owner and concrete next step | Current state |
|---|---|---|
| Case outcomes, proposed priorities, RTM and deviations | Vaishnavi coordinates actual review with each case owner, identifying revision/evidence, original entry gaps and accepted environment/tool changes. | PENDING for whole-plan/team acceptance. The linked #40 AI review separately accepts its 13 original cases and scoped priorities; it does not approve other cases or final human decisions. |
| HTTPS/TLS and ZAP evidence | Sreeharsha #38's loopback transport checks and passive ZAP baseline are now recorded in the source-bound evidence addendum. | TC-SEC-06 and TC-SEC-08 PARTIAL; deployed-candidate/scope and QA alert dispositions remain pending. No team/instructor criterion change is supplied. |
| Unit Test Report | Vaishnavi #41 uses module-owner inputs, reviews unit/integration boundaries, denominator and attribution, then publishes her report. Devansh supplies the [exact existing module input](Code_Coverage_Report.md#hms-19-module-owner-input--8-november-2026). | Missing; SRS unit70 UNPROVEN. #42 reporting remains closed. |
| Remaining cases / quality | Existing case owners supply real execution or genuine authorized disposition of partial, unrun and blocked conditions. | Original 33: 30 OWNER PASS / 2 PARTIAL / 1 NOT RUN. Expanded 61: 50 OWNER PASS / 4 PARTIAL / 6 NOT RUN / 1 BLOCKED. |
| Actual final QA / Dev / PO decisions and guide walkthrough | Vaishnavi / Devansh / Sreeharsha and the actual guide each supply their own dated revision-bound record. | PENDING; technical reviews and PR approvals have limited scopes. |
| Instructor instructions and actual submission | Sreeharsha confirms real channel/cutoff/timezone/format, authentic recordings, complete accepted package and safe receipt. | PENDING; no format, extension, receipt or cutoff hour is invented. |

The report now calculates 32/33 (96.97%) original and 54/61 (88.52%) expanded cases with any exercise, including PARTIAL; these are not completed-case acceptance. Owner-pass proportions are 30/33 (90.91%) and 50/61 (81.97%). All 36 RTM rows have owner-pass mappings, but the Plan's accepted-passed-case requirement metric and complete-condition assessment remain UNVERIFIED. Four known bug-labelled issues are closed with actual ages; their severities are UNKNOWN and a complete severity-ranked inventory is not established. See the [metrics and limits](System_Validation_Report.md#consolidated-case-requirement-and-defect-metrics--8-november-2026).

## Submission checks

- **Test Plan exit criteria:** NOT MET / UNVERIFIED. The record does not establish 100% planned cases executed, all High-priority cases passed, zero open critical/high defects, or a passed case for every RTM requirement. Priority values and case acceptance still need review.
- **Team acceptance:** No complete QA/Dev/PO approval set or guide acceptance walkthrough is recorded. CI and merged PRs do not substitute for those decisions.
- **Videos:** Earlier tracked-file checks found no Sprint 1 one-minute or Sprint 2 two-minute outcome video. Locate genuine team recordings or record this submission gap; do not fabricate videos.
- **Instructor requirements:** The Part 3 PDF gives a 2–6 November window but no cutoff hour or export format. Confirm the actual submission channel, cutoff and required format with the instructor.
- **Final package:** No accepted final submission revision or submission receipt is recorded. Select the revision only after reviews and required reports are complete; run final tree/CI/secret checks on that revision and record the real receipt/link.

## Decision

Keep HMS-21 open and the submission marked **NOT READY**. HMS-15's case-document delivery and PR #59's report publication do not supply missing execution or approvals. Obtain the Unit Test Report, execute/dispose the remaining cases and priorities, update consolidated metrics, record actual team/instructor decisions, and then complete the final package and submission checks. No teammate approval is inferred by this checkpoint.

The separate [#63 owner execution](evidence/issue63/README.md) completes nine expanded integration cases and all 27 exclusively Devansh-owned observations. Its source-bound clean run, current technical priorities and per-step results supplement the earlier reviewed-main snapshot above. Late execution, environment limits, shared QUAL-04/unit70 and actual human/final submission decisions remain explicit; this is not a final accepted submission revision.

### HMS-16 / coverage evidence update — 9 November 2026

The full configured project coverage run is now **PASS at 88.25%**, above its unchanged 70% gate, on candidate commit `7556822df38b23d4f302cf68d857bb35b963ff10` plus seven supplemental HMS-16 tests. It reconciles the previously circulated 53.14%: that value was from the selected `students hostels` subset, not the full project suite. See the [sanitized current execution record](evidence/issue38-execution-20261109/README.md). Formal SRS unit-only coverage remains UNPROVEN; #41 still requires Vaishnavi's unit/integration classification and denominator.

HMS-16 is not fully accepted: the local TLS probe could not be rerun because the disposable MySQL data file was not writable after server restart, so TC-SEC-06 remains PARTIAL. ZAP was intentionally skipped at the user's direction, so TC-SEC-08 remains NOT RUN. HMS-21 and submission readiness remain NOT READY while the unit report, case gaps/acceptance, actual QA/Dev/PO decisions and instructor/submission details remain unresolved.

### Superseding HMS-16 follow-up — 9 November 2026

The two transport/ZAP statements immediately above are historical and superseded by the later same-day loopback evidence in [issue38-security-20261109](evidence/issue38-security-20261109/README.md): the explicit TC-SEC-06 local transport conditions pass, but that case remains PARTIAL because no deployed/staging candidate or scope acceptance is recorded. TC-SEC-08's passive baseline ran and is PARTIAL with one Low server-banner alert and one Informational/Low-confidence `next` hotspot awaiting QA disposition. Neither result constitutes production-host evidence or QA-approved false-positive acceptance.

The published PR #68 head `49851396796918103681aacf47394e5010426201` also has successful fresh MySQL CI: [run 42566973066](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42566973066), Python 3.11 and 3.14, 208 passed plus one expected skip in each 209-test run, all 12 verification gates passed, 88% full-project coverage against the unchanged 70% gate, and nine owned expanded regression cases passed. Formal SRS unit-only coverage and HMS-21 readiness remain unresolved as stated above; no human approval is inferred.
