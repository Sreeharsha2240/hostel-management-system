# HMS-21 final readiness checkpoint

**19 November: owner-scoped HMS-21/#43 CLOSED; original course readiness
NOT READY.** The verified execution source is
3a63cae0049565345f0c2f0687fbb9e54c620751. This assisted technical checkpoint
records actual results and scope decisions; it supplies no other person's
approval or a submission receipt.

| Requirement | Current disposition |
|---|---|
| Updated cases and RTM | Published: 61 records, original 33 IDs and all 36 original RTM mappings retained. |
| Four required reports | Unit, System Validation, Code Coverage and Branch Coverage Reports are present under docs/part3 and refreshed against current evidence. |
| Local automated verification | 13 gates PASS; 727 distinct mixed methods, 726 PASS / one expected timing SKIP; separate timing PASS. Mixed statements 2,995/3,381 (88.58%), branches 821/1,000 (82.10%), combined 87.10%. |
| Isolated-unit target | Clean 415/415 PASS, no DB attempts, 208 verified pins; function-body 1,547/1,740 (88.91%) under the owner boundary. Conservative all-statements companion 56.67%. Retained 288-method baseline passes its tests but measures 66.55%, below 70%. |
| Run provenance | Fresh full mixed, 288/415 isolated and nine-owned executions are clean on 3a63cae. Initial dirty/precommit and 0d9 unit evidence are separately archived; operational runs remain 0d9 with reviewed helper-only carry-forward. |
| Current execution ledger | 56 OWNER PASS / 2 technical PASS / 2 PARTIAL / 1 PENDING; original 33: 32 OWNER PASS / 1 PARTIAL. QUAL-01 follows its primary PARTIAL walkthrough; execution attribution is separate from accepted passage. |
| Current operational execution | Twelve browser workflows/228 observations and real 901.003-second idle PASS; bounded ZAP baseline/triage PASS with retained Medium/Low findings; both 600-second/50-user workloads PASS; fresh owned sandbox recovery plus read-only browser backup PASS. |
| Availability | QUAL-02 PENDING: real observer job job_c4c3658121 / PID 2322483 is installed for 19 November 08:00-20:00 IST. Exported WAITING snapshot has zero probes; no availability pass. |
| Current production corrections | Inventory/history, available-bed consistency, one confirmation per submission and canonical coverage exports corrected. Independent technical review reconciles 26 focused tests and full mixed artifacts; no concrete blocker established in that scope. Current GitHub states are #79 CLOSED / #80 OPEN; remote CI remains separate; [HMS-30 / #90](https://github.com/Sreeharsha2240/hostel-management-system/issues/90) tracks consolidated findings and has final CI/merge acceptance unchecked. |
| Original exit criteria | NOT MET / UNVERIFIED: QUAL-01/04 PARTIAL, QUAL-02 PENDING, OPEN #90 with High technical assessments, accepted-pass RTM coverage unverified. SEC-08 technical execution is now PASS. |
| Owner-scoped task exception | Actual 10 November #43 owner closure skips collecting teammate QA/Development/PO sign-offs and guide walkthrough. Task stays CLOSED; no new collection or approval gate. Original course criteria remain unmet and no such approvals are inferred. |
| Scope limits | Owner REQ-24 interpretation, excluded physical-phone activity and unimplemented SAD section 4.4 request-ID/monitoring items remain disclosed. |
| Sprint videos | Sprint 1 included at 51.719 seconds. Owner-selected Sprint 2 included at 115.148 seconds (1:55), approximately five seconds below the nominal two-minute target; no instructor acceptance of the shortfall is inferred. |
| Course submission | Instructor late-submission/channel/deadline/format decisions, accepted course package and genuine submission/receipt remain unrecorded. |

The [current assessment](Final_Assessment_20261119.md) and
[technical evidence](evidence/sprint-completion-20261118/README.md) give scope,
source and per-file results. The [checklist](../SUBMISSION_CHECKLIST.md) respects
the [actual owner closure](https://github.com/Sreeharsha2240/hostel-management-system/issues/43).
The owner-reported 93-second new-Warden guide task lacks exact guide revision,
participant code and start/end timing trace; it is separate from a project-guide
walkthrough. Historical pre-execution entry approval is not backdated.

Final source pins and clean local regression are verified on 3a63cae.
Operational runs remain bound to 0d9adb39 and their actual helper hashes, with
reviewed helper-only carry-forward. Remote Python 3.11/3.14 CI reconciliation,
merge/main verification and the candidate package remain pending. Availability
and original course criteria keep their separately recorded states.

<details>
<summary>Historical readiness records through 18 November (original source/date scopes)</summary>

The dated checkpoint text below is retained for provenance. Its then-current
counts, metrics, issue states and pending-video language must not override the
19 November assessment above. Historical OWNER PASS summaries for QUAL-01 are
superseded by reconciliation with the primary PARTIAL walkthrough.

# HMS-21 Final Readiness Checkpoint

**18 November mobile-view update:** The owner reports that a friend checked the
website in phone mode in a laptop browser. Record this as an informal browser-
emulated mobile-layout check, not a physical-phone test; details and captured
evidence were not supplied. See the [mobile browser-mode note](evidence/mobile-browser-mode-check-20261118.md).

**18 November Sprint 2 decision:** The owner selected the included 1:55
Sprint 2 outcome video as the final demo. It supersedes the earlier candidate
status. The five-second difference from the nominal two-minute target remains
disclosed; team and instructor acceptance are separate decisions.

**18 November acceptance review:** The recorded Development review agrees with
the proposed 34 High / 27 Medium priorities and accepts the original 36 RTM
mappings as design traceability, but its final build decision is **HOLD**. The
owner's priority/scope decisions do not supply QA agreement or instructor
approval. The expanded case register remains 57 OWNER PASS / 2 PARTIAL / 2 NOT
RUN; TC-SEC-08 is High and PARTIAL, so the submitted High-case exit gate is not
met. Accepted-pass coverage for all 36 requirements is unverified. #79 and #80
remain open; the 14 November Development review needs a fresh decision against
the current source after those defects and review dependencies are resolved.
The laptop-browser phone-mode check is owner-reported with no retained test
details; it is not evidence of physical-device behavior. This is an independent
document review, not a QA or Development sign-off. See the [Development
review](Development_Review_20261114.md), [owner decisions](evidence/owner-disposition-20261114.md),
and [current validation report](System_Validation_Report.md).

**18 November #79/#80 follow-up:** PR #86 merged as `306d240`. Room and bed
saves reject reassignments that would rewrite allocation history; regular and
Django Admin room forms show errors, queryset and bulk updates are guarded, and
bed moves lock affected rooms. The merge's MySQL CI run failed because two
isolated room tests hit the database through model validation, and a race test
used the normal bed-save path that now rejects historical moves. PR #87 removes
the extra database read from `Room.clean`, uses the protected `RoomForm` in
Django Admin, and makes the race test simulate only its concurrent database
write. The focused affected selection passes 21/21 on local SQLite, and Ruff
checks pass. PR #87's full MySQL suite passed, then its job stopped because the
15 November coverage source pins were stale. The unchanged 288/294 selections
have now been remeasured against 18 November pins and both local selections
passed without database access (95.89% and 96.19% function-body diagnostics).
CI run [#151](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/44315160437)
passed both Python 3.11 and 3.14 jobs on PR #87's merge candidate, including the
MySQL suite and refreshed coverage scopes. Issues #79 and #80 remain open for
QA retest and acceptance. See the [18 November coverage refresh](evidence/hms19-main-refresh-20261118/README.md).

The [15 November test follow-up](evidence/remaining-test-gaps-20261115.md)
records additional Windows and Ubuntu checks, authenticated passive ZAP
findings and the scheduled working-hours availability observation.

**15 November follow-up (historical; updated by the 18 November Sprint 2 decision above):** The [14 November Development review](Development_Review_20261114.md) remains recorded with final Development acceptance **HOLD**. PR #75 has since merged as `3d16967`; issue #78 was closed by PR #81. Issues [#79](https://github.com/Sreeharsha2240/hostel-management-system/issues/79) and [#80](https://github.com/Sreeharsha2240/hostel-management-system/issues/80) remain open for their module owners and QA triage. [Devansh's contribution](evidence/sprint-recordings/devansh-contribution-20261114/README.md) and the owner's final 1:55 [Sprint 2 demo](evidence/sprint-recordings/Sprint2_Outcome_Demo.md) are both recorded. The 57 OWNER PASS / 2 PARTIAL / 2 NOT RUN ledger is not final case acceptance. QA, guide and instructor decisions and the actual submission/receipt remain pending.

**Current disposition — 15 November 2026:** HMS-19/#41 remains complete. The refreshed isolated selection passes 294/294 with zero database attempts and covers 956/959 function-body statements (99.69%) under the owner-approved definition; the 55.68% all-application-statements result is also disclosed. See the [current source-pinned evidence](evidence/hms19-main-refresh-20261115/README.md). This refresh is included in PR #84, merged as `324f460`; both Python 3.11 and 3.14 jobs passed in [CI run 43736427332](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/43736427332). Real-phone testing is out of this mini-project's scope. Expanded register: 57 OWNER PASS / 2 PARTIAL / 2 NOT RUN / 0 BLOCKED. TC-SEC-08 remains PARTIAL after the supplied QA handoff assessed its Low and Informational findings; the limitation is passive loopback scope. TC-QUAL-02 remains NOT RUN; TC-QUAL-03 remains NOT RUN for desktop browser/OS coverage; TC-QUAL-04 remains PARTIAL because style claims stop at configured checks. PO decisions for priorities, RTM design mapping, REQ-24 fields, SAD §4.4 scope and known defect severities are recorded in the [owner disposition](evidence/owner-disposition-20261114.md); QA/Dev and instructor acceptance remain pending. Whole-plan submission is still NOT READY.

**Owner work completed or remaining:** Coverage-report freshness, Sprint 1 video inclusion, HMS-16 local HTTPS/ZAP execution, the supplied QA alert reconciliation, the owner-authorized #39 tracking closure with TC-QUAL-02 left NOT RUN, and project-owner dispositions for case priorities, RTM design mappings, REQ-24 fields, the SAD §4.4 limitation and the four known defect severities are recorded in the [owner decision](evidence/owner-disposition-20261114.md). QA and Development still need to agree to priorities and review the scoped dispositions; accepted requirement-by-requirement case results remain pending. The owner selected the included 1:55 Sprint 2 clip as the final demo and approved publishing it despite the five-second shortfall; team/instructor acceptance remains separate. Sreeharsha's remaining items are to coordinate those reviews, obtain instructor submission instructions, and prepare the final package/receipt. TC-QUAL-03 is assigned to Vaishnavi for desktop/browser/OS evidence. Teammate, guide and instructor approvals must come from those people. The #39 tracking closure does not change TC-QUAL-02 to PASS or waive whole-plan acceptance.

**14 November recording update:** The owner-provided [Sprint 1 outcome demo](evidence/sprint-recordings/Sprint1_Outcome_Demo.mp4) is included and measures 51.719 seconds. The owner-provided [Sprint 2 outcome video](evidence/sprint-recordings/Sprint2_Outcome_Demo.mp4) is included and measures 1:55; the owner selected it as the final demo on 18 November. Its metadata and shown workflows are documented in [the recording assessment](evidence/sprint-recordings/Sprint2_Outcome_Demo.md).

**Owner decision — mini-project scope:** Physical-phone testing is replaced by a laptop-browser phone-mode check. The owner reports that a friend performed this emulated mobile-layout check; its details and evidence were not supplied. TC-QUAL-03 remains NOT RUN because the latest-two desktop-browser matrix and Windows/Linux workflows still need evidence.

**10 November local browser follow-up:** The [local observations](evidence/issue39/local-browser-20261110.md) record a successful synthetic Warden login and six page/navigation checks in connected Chrome. Edge was unavailable through the connected browser. This short run does not complete the browser matrix or measure working-hours availability.

**Overall readiness:** **NOT READY** for final submission. Desktop browser/OS evidence and working-hours availability remain unverified; QA/Development agreement, accepted case/priority/RTM results, instructor review of the scope dispositions, submission directions, review of Sprint 2 video content/duration, final revision and receipt are also pending. The reported laptop-browser phone-mode check is documented above; physical-phone testing is not required under this mini-project scope. HMS-19 is complete as recorded in the current disposition above.

**Current execution ledger:** The original 33 cases have 33 OWNER PASS observations, subject to independent acceptance of their evidence and prerequisites. The expanded 61 have 57 OWNER PASS / 2 PARTIAL / 2 NOT RUN / 0 BLOCKED. The remaining case conditions are TC-SEC-08 (passive loopback scan, PARTIAL), TC-QUAL-02 (working-hours availability, NOT RUN), TC-QUAL-03 (desktop browser/OS portability, NOT RUN) and TC-QUAL-04 (unit target met under the owner-approved function-body definition; broader PEP 8 review is limited to configured checks). The friend-reported laptop-browser phone-mode check is separate from this case and lacks supporting details.

**Additional SAD alignment gap:** SAD §4.4 request-ID error logging and operational monitoring remain unimplemented/unverified; the project owner records them as a mini-project limitation. REQ-24's current profile field boundary is now defined by the project owner; QA review remains pending. See the [System Validation Report](System_Validation_Report.md) and [owner decision](evidence/owner-disposition-20261114.md).

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
| Unit Test Report (#41) | Published and completed through merged PR #74; #41 is closed. | Latest source refresh passes 294/294 methods at 956/959 function-body statements (99.69%); 55.68% all-statements is disclosed. Both Python 3.11 and 3.14 CI jobs passed in PR #84 before merge. This does not by itself approve final project submission. |
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
| #41 HMS-19 | CLOSED — PR #74 merged as `a41f884` | Latest source refresh in PR #84 meets 70% at 956/959 (99.69%) function-body statements across 294 isolated methods. The 55.68% all-statements diagnostic remains disclosed; both Python CI jobs passed before PR #84 merged. |
| #42 HMS-20 | Closed | Coverage reports are published and the reporting task is complete; the later HMS-19 unit result is documented in the Unit Test Report. |
| #63 HMS-26 | CLOSED — PR #64 merged and exact-main CI verified | [Nine remaining Devansh-owned recipes](evidence/issue63/README.md) passed on clean `6636098cb728aa17c2abf5e42c358a5d400261e7` after independent pre-execution review, then in both Python jobs of main CI 42461981682 at `cae69ea`. Other owners and final acceptance remain separate. |
| #43 HMS-21 | CLOSED — scoped tracking checkpoint | Whole-plan submission readiness remains NOT READY. Complete case/entry/exit review, actual approvals and instructor instructions, then select a final package and record a genuine submission receipt. |

## Team review and pending decisions — 8 November 2026

An assisted development technical review of the published report/evidence is now recorded in the [System Validation Report](System_Validation_Report.md#team-actions-and-actual-approvals). Three fresh reviewers checked security assertions, counts/coverage, and original assignment/readiness requirements. Its corrections preserve all historical owner observations and do not supply human QA/Dev/PO final attestations. No new Harsha PR was open at the reviewed snapshot.

| Required action | Owner and concrete next step | Current state |
|---|---|---|
| Case outcomes, priorities, RTM and deviations | Vaishnavi coordinates actual review with each case owner, identifying revision/evidence, original entry gaps and accepted environment/tool changes. The owner disposition accepts the current priority proposals and original RTM pairs at PO level. | QA/Development agreement and whole-plan acceptance remain PENDING. The linked #40 AI review separately accepts its 13 original cases and scoped priorities; it does not approve other cases or final human decisions. |
| HTTPS/TLS and ZAP evidence | Sreeharsha #38's loopback transport checks, passive ZAP baseline and 10 November supplied QA alert assessment are recorded in source-bound evidence. | TC-SEC-06 OWNER PASS for isolated test conditions; TC-SEC-08 remains PARTIAL because loopback passive scope is limited. The TLS evidence is not a production-host claim. |
| Unit Test Report | Completed through merged PR #74; see the current disposition above. | HMS-19/#41 is closed. This report does not by itself complete whole-plan acceptance or final submission. |
| Remaining cases / quality | Existing case owners supply real execution or genuine authorized disposition of partial, unrun and blocked conditions. | Original 33: 31 OWNER PASS / 1 PARTIAL / 1 NOT RUN. Expanded 61: 51 OWNER PASS / 3 PARTIAL / 6 NOT RUN / 1 BLOCKED. |
| Actual final QA / Dev / PO decisions and guide walkthrough | Vaishnavi / Devansh / Sreeharsha and the actual guide each supply their own dated revision-bound record. | PENDING; technical reviews and PR approvals have limited scopes. |
| Instructor instructions and actual submission | Sreeharsha confirms real channel/cutoff/timezone/format, authentic recordings, complete accepted package and safe receipt. | PENDING; no format, extension, receipt or cutoff hour is invented. |

The report now calculates 32/33 (96.97%) original and 54/61 (88.52%) expanded cases with any exercise, including PARTIAL; these are not completed-case acceptance. Owner-pass proportions are 31/33 (93.94%) and 51/61 (83.61%). All 36 RTM rows have owner-pass mappings, but the Plan's accepted-passed-case requirement metric and complete-condition assessment remain UNVERIFIED. Four known bug-labelled issues are closed with actual ages; their severities are UNKNOWN and a complete severity-ranked inventory is not established. See the [metrics and limits](System_Validation_Report.md#consolidated-case-requirement-and-defect-metrics--8-november-2026).

## Submission checks

- **Test Plan exit criteria:** Not complete for the expanded register: 57 OWNER PASS / 2 PARTIAL / 2 NOT RUN; the original 33 have 33 OWNER PASS observations. High-priority acceptance, severity-ranked defect status and accepted passed-case coverage for all 36 RTM requirements remain unverified.
- **Team acceptance:** No complete QA/Dev/PO approval set or guide acceptance walkthrough is recorded. CI and merged PRs do not substitute for those decisions.
- **Videos:** The owner-provided [Sprint 1 demo](evidence/sprint-recordings/Sprint1_Outcome_Demo.mp4) is included; its duration is 51.7 seconds, within the one-minute target. The owner selected the [Sprint 2 demo](evidence/sprint-recordings/Sprint2_Outcome_Demo.mp4) as final; it runs 1:55, five seconds short of the nominal two-minute target. Team/instructor acceptance remains separate. See the [recording assessment](evidence/sprint-recordings/Sprint2_Outcome_Demo.md). The Warden usability clips remain separate deliverables.
- **Instructor requirements:** Obtain the required submission channel and format from the instructor. Late-submission acceptance is excluded from the owner's current project checklist.
- **Final package:** No accepted final submission revision or submission receipt is recorded. Select the revision only after reviews and required reports are complete; run final tree/CI/secret checks on that revision and record the real receipt/link.

## Decision

HMS-21/#43 is CLOSED as a scoped tracking checkpoint; submission remains **NOT READY**. HMS-19/#41 and its Unit Test Report are complete. The 14 November Development review is recorded with final acceptance HOLD. Resolve or formally disposition the current defects and remaining in-scope conditions; finish QA/case-owner/RTM acceptance; record genuine final QA/Dev/PO and guide decisions; confirm the instructor's submission channel/format; obtain team/instructor acceptance of the owner-selected final Sprint 2 demo; and complete final package checks and receipt capture. No teammate approval or instructor decision is inferred by this checkpoint.

The separate [#63 owner execution](evidence/issue63/README.md) completes nine expanded integration cases and all 27 exclusively Devansh-owned observations. Its source-bound clean run, current technical priorities and per-step results supplement the earlier reviewed-main snapshot above. Late execution, environment limits, shared QUAL-04/unit70 and actual human/final submission decisions remain explicit; this is not a final accepted submission revision.

### HMS-16 / coverage evidence update — 9 November 2026

The full configured project coverage run is now **PASS at 88.25%**, above its unchanged 70% gate, on candidate commit `7556822df38b23d4f302cf68d857bb35b963ff10` plus seven supplemental HMS-16 tests. It reconciles the previously circulated 53.14%: that value was from the selected `students hostels` subset, not the full project suite. See the [sanitized current execution record](evidence/issue38-execution-20261109/README.md). Formal SRS unit-only coverage remains UNPROVEN; #41 still requires Vaishnavi's unit/integration classification and denominator.

At the time of this earlier 9 November coverage snapshot, the local TLS rerun was blocked by the disposable MySQL file issue and ZAP had not yet been run. The same-day loopback TLS/ZAP follow-up below supersedes those two evidence gaps; HMS-21 and submission readiness remain NOT READY for the separate unit-report, case-review, approval, instructor and final-submission items.

### Superseding HMS-16 follow-up — 9 November 2026

The two transport/ZAP statements immediately above are historical and superseded by the later same-day loopback evidence in [issue38-security-20261109](evidence/issue38-security-20261109/README.md): TC-SEC-06 is OWNER PASS for its listed isolated test conditions, without claiming public/production TLS. TC-SEC-08's passive baseline ran and is PARTIAL with one Low server-banner alert and one Informational/Low-confidence `next` hotspot awaiting QA disposition. The expanded case totals above include these updated dispositions; no QA approval or false-positive acceptance is inferred.

The published PR #68 head `49851396796918103681aacf47394e5010426201` also has successful fresh MySQL CI: [run 42566973066](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42566973066), Python 3.11 and 3.14, 208 passed plus one expected skip in each 209-test run, all 12 verification gates passed, 88% full-project coverage against the unchanged 70% gate, and nine owned expanded regression cases passed. Formal SRS unit-only coverage and HMS-21 readiness remain unresolved as stated above; no human approval is inferred.

</details>
