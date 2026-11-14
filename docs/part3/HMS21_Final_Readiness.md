# HMS-21 Final Readiness Checkpoint

**Current disposition — 13 November 2026:** HMS-19/#41 is complete: PR #74 merged as `a41f884`, closing #41. The owner-approved function-body measure is 946/946 (100%) across 288 isolated methods; 55.55% all-application-statements coverage remains disclosed. Real-phone testing is out of this mini-project's scope. Current case follow-up is TC-SEC-08 (PARTIAL), TC-QUAL-02 (NOT RUN), TC-QUAL-03 desktop browser/OS portability (NOT RUN), and TC-QUAL-04 (unit target met under the approved boundary; broader style review remains limited to configured checks). Expanded register: 57 OWNER PASS / 2 PARTIAL / 2 NOT RUN / 0 BLOCKED. The dated snapshots below are historical where they conflict with this update.

**14 November recording update:** The owner-provided [Sprint 1 outcome demo](evidence/sprint-recordings/Sprint1_Outcome_Demo.mp4) is included and measures 51.719 seconds. The Sprint 2 two-minute outcome video remains unlocated.

**Owner decision — mini-project scope:** Real-phone testing is removed from this mini-project's acceptance scope. TC-QUAL-03 remains NOT RUN because the latest-two desktop-browser matrix and Windows/Linux workflows still need evidence. The project checklist records this owner-approved scope adjustment; it does not claim phone testing was performed.

**10 November local browser follow-up:** The [local observations](evidence/issue39/local-browser-20261110.md) record a successful synthetic Warden login and six page/navigation checks in connected Chrome. Edge was unavailable through the connected browser. This short run does not complete the browser matrix or measure working-hours availability.

**13 November overall readiness:** **NOT READY** for final submission. Desktop browser/OS evidence and working-hours availability remain unverified, along with case/priority acceptance, actual team decisions, instructor directions, final submission revision and receipt. Phone testing is excluded by the owner-approved mini-project scope decision above. HMS-19 is complete as recorded in the current disposition above.

**Current execution ledger:** The original 33 cases have 33 OWNER PASS observations, subject to independent acceptance of their evidence and prerequisites. The expanded 61 have 57 OWNER PASS / 2 PARTIAL / 2 NOT RUN / 0 BLOCKED. The remaining case conditions are TC-SEC-08 (passive loopback scan, PARTIAL), TC-QUAL-02 (working-hours availability, NOT RUN), TC-QUAL-03 (desktop browser/OS portability, NOT RUN) and TC-QUAL-04 (unit target met under the owner-approved function-body definition; broader PEP 8 review is limited to configured checks). Real-phone testing is out of scope.

**Additional SAD alignment gap:** SAD §4.4 request-ID error logging and operational monitoring (login-failure counts, HTTP 4xx/5xx rate, average response time, backup-job success, database free space and weekly review) are not implemented/evidenced in the current code. The current student self-service page shows name/ID, own allocation and payment summaries/history; the exact required profile-field list is not defined by REQ-24. See the [System Validation Report](System_Validation_Report.md).

**10 November HMS-17 follow-up:** [four remaining regression recipes](evidence/issue39/completion-20261110/README.md)
now pass with fresh registration evidence and all 12 verification gates (210 PASS,
one expected timing SKIP plus separate timing PASS). Owner-directed #39 closure
accepts limited local-project scope while retaining the desktop browser matrix
and working-hours availability as unverified exceptions. Current expanded61:
57 OWNER PASS / 1 PARTIAL / 2 NOT RUN / 1 BLOCKED. This supplies no QA signature,
instructor amendment or submission receipt; original whole-plan NOT READY remains.

**Checkpoint started:** 8 November 2026; security evidence updated 9 November 2026
**Reviewed main revision:** `b523d4c7abb77072bea48ac059be7f72396e8a79` (tree `56f7fb4307bc2ce4f3595aebfd5915ce301c3fb7`). Accepted final submission revision: **PENDING**.
**Readiness:** **NOT READY**. This checkpoint records verified deliverables and blockers; it is not an approval or submission receipt.

**Historical 10 November status update:** PR #68 was merged to main as `24e12526a771d1ec9d3545de78512ed3fc229abe` (tree `c5dfa2d8f482ee023417db5967133f2881513f6a). Its exact-head MySQL CI run 42569529411 passed both Python 3.11 and 3.14 jobs. The local TLS checks passed for the documented isolated conditions; ZAP baseline findings remained PARTIAL. The report's then-current unit70 UNPROVEN disposition was superseded by HMS-19/#41's completion in PR #74. Whole-plan readiness remains NOT READY for the remaining case acceptance, actual QA/Dev/PO decisions, instructor submission directions, final package selection and genuine submission receipt.

**9 November HMS-16 evidence update:** isolated local TLS/HTTPS checks now pass and a ZAP 2.17.0 passive baseline completed. The app CSP and CSRF-cookie findings were corrected and absent on rescan. The remaining ZAP low server-banner finding is specific to the local Python WSGI probe server; its informational `next`-parameter hotspot awaits QA disposition. See the [transport/ZAP evidence](evidence/issue38-security-20261109/README.md). #38 still needs QA disposition and team approvals; #43 remains NOT READY for the independent report, case-review, approval, instructor and actual submission requirements below.

**Current-main development addendum — 8 November 2026:** [Development review and #41 classification handoff](Development_Review_20261108.md) reviews `cae69ea2192838b7874ad5be240def842f5aab5e` (tree `4f81f4a5e100f6a3f22505acfa05b4dd0ff9bb1f`). PR #64 and [exact-main CI 42461981682](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42461981682) are successful; #40 and #63 are CLOSED. Final development acceptance remains **HOLD** pending the remaining evidence and final package. The earlier review revision and historical measurements below are preserved.

**HMS-17 follow-up — 8 November 2026:** [PR #66 reconciliation](evidence/issue39/followup-20261108.md) accepts two historical automated recipes (S1-07/S2-07), with actual 7 November source/run provenance, and corrects unsupported complete passes. At the 8 November snapshot, expanded totals were 50 OWNER PASS / 3 PARTIAL / 7 NOT RUN / 1 BLOCKED; the 9 November ZAP execution subsequently updates current totals below. Original 33 dispositions remain unchanged. New screenshots support limited page/allocation observations; #39 remains OPEN for the original registration, guide/quality and broader coverage gaps. No final acceptance or unit70 change is supplied.

## Required Part 3 deliverables

| Deliverable | Current state | Remaining work |
|---|---|---|
| Test Case Document and RTM (#37) | Published through merged PR #60; #37 CLOSED for authorized documentation delivery: 61 complete case records and 36 core RTM rows, preserving original IDs/evidence. | Devansh authorized this documentation delivery without additional teammate messages. Actual case execution, priority agreement, historical entry/deviation acceptance and final QA/Dev/PO approvals remain distinct pending work. |
| Unit Test Report (#41) | Published and completed through merged PR #74; #41 is closed. | Owner-approved function-body coverage is 946/946 (100%) across 288 isolated methods. The 55.55% all-statements companion result remains disclosed. This does not by itself approve final project submission. |
| System Validation Report (#38) | Published through merged PR #59; #38 is closed for owner-authorized local-project scope. The supplied 10 November QA handoff assesses both remaining ZAP findings, with the missing-test assertion corrected in the reconciliation above. | TC-SEC-06 is OWNER PASS for isolated loopback conditions. TC-SEC-08 remains PARTIAL, with one Low and one Informational alert retained. Actual final QA/Dev/PO and whole-plan decisions remain pending; readiness is NOT READY. |
| Code Coverage Report (#42) | Published on main; PR #57 was independently reviewed and merged. | Reporting task complete; the later #41 unit result and owner-approved scope are recorded in the Unit Test Report. |
| Branch Coverage Report (#42) | Published on main; PR #57 was independently reviewed and merged. | Reporting task complete; unit-test coverage interpretation is documented separately in the Unit Test Report. |

The latest HMS-17 PR #58 merged as `896b4f3`; its tested tree is the same as the merge tree. Both CI jobs on that identical tree passed on Python 3.11 and 3.14. PR #59 then merged as `70c9fe2`, whose two main-branch CI jobs also passed. The corrected HMS-17 PR description preserves #39 as open. PR #60 then merged as `b523d4c`; [exact-main run 42399172513](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42399172513) passed both Python jobs. The 8 November [technical review and extraction](System_Validation_Report.md#independent-evidence-review-and-current-build) independently reconciles its 190 mixed identities (189 PASS / one expected SKIP), 12 gates and separate timing PASS per job. This is not a teammate signature, a new browser/load/recovery run or an accepted final package. The linked report records the original-subcondition evidence gaps, current metrics and required owner actions.

## Current issue dependencies

| Issue | State | Remaining readiness dependency |
|---|---|---|
| #37 HMS-15 | Closed — documentation delivered through PR #60 | Complete records, mappings and evidence reconciliation are delivered under Devansh's explicit instruction. The document retains execution gaps and proposed-priority/acceptance limits; closing this delivery does not complete the whole Test Plan. |
| #38 HMS-16 | CLOSED — owner-authorized local-project scope | PR #68 and report evidence are merged. The supplied QA handoff assesses both ZAP alerts; TC-SEC-08 remains PARTIAL for passive loopback coverage. The two findings remain in the record and final whole-plan decisions remain pending. |
| #39 HMS-17 | CLOSED — owner-authorized local-project scope | PR #71 adds a fresh registration and four passing regression recipes. Full latest-two desktop-browser coverage and working-hours availability remain unverified exceptions; real-phone testing is out of scope. |
| #40 HMS-18 | CLOSED — scoped technical delivery accepted | [8 November independent AI QA](evidence/issue40-final/qa-review-20261108.md), expressly authorized by Devansh, accepts the original 13 cases with current-priority, late-entry and bounded tool/environment dispositions. That #40 review preserved OWNER PASS observations, raw browser PARTIAL and expanded-case statuses; the separate #63 follow-up below subsequently executes nine expanded recipes. Actual named human final approvals and whole-plan acceptance remain pending. |
| #41 HMS-19 | CLOSED — PR #74 merged as `a41f884` | Owner-approved function-body coverage meets 70% at 946/946 (100%) across 288 isolated methods. The 55.55% all-statements diagnostic remains disclosed. |
| #42 HMS-20 | Closed | Coverage reports are published and the reporting task is complete; the later HMS-19 unit result is documented in the Unit Test Report. |
| #63 HMS-26 | CLOSED — PR #64 merged and exact-main CI verified | [Nine remaining Devansh-owned recipes](evidence/issue63/README.md) passed on clean `6636098cb728aa17c2abf5e42c358a5d400261e7` after independent pre-execution review, then in both Python jobs of main CI 42461981682 at `cae69ea`. Other owners and final acceptance remain separate. |
| #43 HMS-21 | CLOSED — scoped tracking checkpoint | Whole-plan submission readiness remains NOT READY. Complete case/entry/exit review, actual approvals and instructor instructions, then select a final package and record a genuine submission receipt. |

## Team review and pending decisions — 8 November 2026

An assisted development technical review of the published report/evidence is now recorded in the [System Validation Report](System_Validation_Report.md#team-actions-and-actual-approvals). Three fresh reviewers checked security assertions, counts/coverage, and original assignment/readiness requirements. Its corrections preserve all historical owner observations and do not supply human QA/Dev/PO final attestations. No new Harsha PR was open at the reviewed snapshot.

| Required action | Owner and concrete next step | Current state |
|---|---|---|
| Case outcomes, proposed priorities, RTM and deviations | Vaishnavi coordinates actual review with each case owner, identifying revision/evidence, original entry gaps and accepted environment/tool changes. | PENDING for whole-plan/team acceptance. The linked #40 AI review separately accepts its 13 original cases and scoped priorities; it does not approve other cases or final human decisions. |
| HTTPS/TLS and ZAP evidence | Sreeharsha #38's loopback transport checks and passive ZAP baseline are now recorded in the source-bound evidence addendum. | TC-SEC-06 OWNER PASS for the isolated test conditions; TC-SEC-08 PARTIAL pending QA alert disposition. The TLS evidence is not a production-host claim. |
| Unit Test Report | Completed through merged PR #74; see the current disposition above. | HMS-19/#41 is closed. This report does not by itself complete whole-plan acceptance or final submission. |
| Remaining cases / quality | Existing case owners supply real execution or genuine authorized disposition of partial, unrun and blocked conditions. | Original 33: 31 OWNER PASS / 1 PARTIAL / 1 NOT RUN. Expanded 61: 51 OWNER PASS / 3 PARTIAL / 6 NOT RUN / 1 BLOCKED. |
| Actual final QA / Dev / PO decisions and guide walkthrough | Vaishnavi / Devansh / Sreeharsha and the actual guide each supply their own dated revision-bound record. | PENDING; technical reviews and PR approvals have limited scopes. |
| Instructor instructions and actual submission | Sreeharsha confirms real channel/cutoff/timezone/format, authentic recordings, complete accepted package and safe receipt. | PENDING; no format, extension, receipt or cutoff hour is invented. |

The report now calculates 32/33 (96.97%) original and 54/61 (88.52%) expanded cases with any exercise, including PARTIAL; these are not completed-case acceptance. Owner-pass proportions are 31/33 (93.94%) and 51/61 (83.61%). All 36 RTM rows have owner-pass mappings, but the Plan's accepted-passed-case requirement metric and complete-condition assessment remain UNVERIFIED. Four known bug-labelled issues are closed with actual ages; their severities are UNKNOWN and a complete severity-ranked inventory is not established. See the [metrics and limits](System_Validation_Report.md#consolidated-case-requirement-and-defect-metrics--8-november-2026).

## Submission checks

- **Test Plan exit criteria:** Not complete for the expanded register: 57 OWNER PASS / 2 PARTIAL / 2 NOT RUN; the original 33 have 33 OWNER PASS observations. High-priority acceptance, severity-ranked defect status and accepted passed-case coverage for all 36 RTM requirements remain unverified.
- **Team acceptance:** No complete QA/Dev/PO approval set or guide acceptance walkthrough is recorded. CI and merged PRs do not substitute for those decisions.
- **Videos:** The owner-provided [Sprint 1 demo](evidence/sprint-recordings/Sprint1_Outcome_Demo.mp4) is now included; its duration is 51.7 seconds, within the one-minute target. The repository still lacks the Sprint 2 two-minute outcome video. The Warden usability clips remain separate deliverables.
- **Instructor requirements:** The Part 3 PDF lists a 2–6 November 2026 window but no cutoff hour or export format; that stated window has passed. Confirm whether late submission is accepted and obtain the current channel, deadline and required format from the instructor.
- **Final package:** No accepted final submission revision or submission receipt is recorded. Select the revision only after reviews and required reports are complete; run final tree/CI/secret checks on that revision and record the real receipt/link.

## Decision

Keep HMS-21 open and the submission marked **NOT READY**. HMS-19/#41 and its Unit Test Report are complete. Resolve or accept the remaining security, availability and desktop portability conditions; finish case/priority/RTM and defect-severity acceptance; record genuine QA/Dev/PO decisions; confirm instructor late-submission requirements; obtain the Sprint 2 outcome video; and complete final package checks and receipt capture. No teammate approval or instructor decision is inferred by this checkpoint.

The separate [#63 owner execution](evidence/issue63/README.md) completes nine expanded integration cases and all 27 exclusively Devansh-owned observations. Its source-bound clean run, current technical priorities and per-step results supplement the earlier reviewed-main snapshot above. Late execution, environment limits, shared QUAL-04/unit70 and actual human/final submission decisions remain explicit; this is not a final accepted submission revision.

### HMS-16 / coverage evidence update — 9 November 2026

The full configured project coverage run is now **PASS at 88.25%**, above its unchanged 70% gate, on candidate commit `7556822df38b23d4f302cf68d857bb35b963ff10` plus seven supplemental HMS-16 tests. It reconciles the previously circulated 53.14%: that value was from the selected `students hostels` subset, not the full project suite. See the [sanitized current execution record](evidence/issue38-execution-20261109/README.md). Formal SRS unit-only coverage remains UNPROVEN; #41 still requires Vaishnavi's unit/integration classification and denominator.

At the time of this earlier 9 November coverage snapshot, the local TLS rerun was blocked by the disposable MySQL file issue and ZAP had not yet been run. The same-day loopback TLS/ZAP follow-up below supersedes those two evidence gaps; HMS-21 and submission readiness remain NOT READY for the separate unit-report, case-review, approval, instructor and final-submission items.

### Superseding HMS-16 follow-up — 9 November 2026

The two transport/ZAP statements immediately above are historical and superseded by the later same-day loopback evidence in [issue38-security-20261109](evidence/issue38-security-20261109/README.md): TC-SEC-06 is OWNER PASS for its listed isolated test conditions, without claiming public/production TLS. TC-SEC-08's passive baseline ran and is PARTIAL with one Low server-banner alert and one Informational/Low-confidence `next` hotspot awaiting QA disposition. The expanded case totals above include these updated dispositions; no QA approval or false-positive acceptance is inferred.

The published PR #68 head `49851396796918103681aacf47394e5010426201` also has successful fresh MySQL CI: [run 42566973066](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42566973066), Python 3.11 and 3.14, 208 passed plus one expected skip in each 209-test run, all 12 verification gates passed, 88% full-project coverage against the unchanged 70% gate, and nine owned expanded regression cases passed. Formal SRS unit-only coverage and HMS-21 readiness remain unresolved as stated above; no human approval is inferred.
