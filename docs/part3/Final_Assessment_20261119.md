# Part 3 assessment — 19 November 2026

**Latest CI/merge checkpoint:** [PR #91](https://github.com/Sreeharsha2240/hostel-management-system/pull/91)
merged as 9ad6cf9a076d3b87f3287e46f73e118bc80ec0b0 at 18 November 20:11:20 UTC.
Exact tested head: e2fe45fa7877bccbe9a864ff4cb3097efd3e2bdf;tree 1c30b1e73f2bf466821e0bdd749c544ff6010424.
ManualCI44383638276 and automatic PR CI 44383945828 both passed Python 3.11/3.14.
The [six-ZIP audit](evidence/sprint-completion-20261118/ci-evidence/ci-summary.json)
passes all fourteen checks. All tracked issues,including #80/#90, are CLOSED;
the current query has no open issues: zero known open High/Critical among those
tracked fixed defects. Final main verification after this docs checkpoint
and the candidate package remain pending.

Python 3.11 mixed coverage is 2,998/3,384 statements; Python 3.14 is 2,995/3,381.
Both cover 821/1,000 branches and 1,547/1,740 function-body statements (88.91%).
Unit all-statements companions are 1,547/2,733 (56.60%) and 1,547/2,730 (56.67%).
The only interpreter variance is three source-proved eager class annotations;
method credit, harness and thresholds are unchanged. [Per-version coverage](evidence/sprint-completion-20261118/ci-evidence/coverage-tables-py3.11.md)
retains the actual totals. Local3a63cae and operational 0d9adb39 evidence below
is preserved at its own execution source.

**Original course-submission readiness: NOT READY. Owner-scoped HMS-21/#43:
CLOSED.** The updated 61-case document, 36-row core RTM and four required
reports are present. Publication and scoped tracking closure do not establish
every original Test Plan/course criterion.

The verified clean execution source is
3a63cae0049565345f0c2f0687fbb9e54c620751 (tree
e4b06445ea710139ad8b4a64885606ec62411fa1). All 13 local gates passed:
727 mixed methods, 726 PASS/one expected timing SKIP, separate timing PASS,
2,995/3,381 statements, 821/1,000 branches and 87.10% combined.
Both isolated runs are clean with 208 verified pins/zero DB attempts; 415 methods
cover 1,547/1,740 function-body statements (88.91%) and 1,547/2,730 all-statements
(56.67%). Nine separate owned recipes also pass cleanly.

The [initial 0d9 evidence archive](evidence/sprint-completion-20261118/initial-candidate-0d9adb3.json.gz)
preserves original dirty/precommit mixed results and initial clean unit results.
Browser, scan, load, idle and recovery runs remain bound to 0d9adb39. Application
behavior/assets/dependencies are unchanged; the two helper-only changes are
verified by 32 recovery-safety tests and the new clean run. No old run is relabelled.

The [actual 10 November owner closure of #43](https://github.com/Sreeharsha2240/hostel-management-system/issues/43)
explicitly skips collecting teammate QA/Development/PO sign-offs and the
project-guide walkthrough for this mini-project. Respect that scope exception:
the task stays closed and this assessment imposes no new collection or
approval gate. Those people did not thereby approve the project; original
course criteria remain unmet and no instructor-approved amendment or actual
submission/receipt is recorded. Technical work across assignees is authorized;
today's automated executions are not attributed to another teammate.

Fresh independent technical review covered 26 focused tests and the full mixed
artifacts. Inventory/history and HTML/API availability consistency corrections,
single submission confirmation and canonical coverage export normalization are
verified in that scope; no remaining concrete production blocker was established.
Browser, scan, load and recovery now have the bounded technical results below;
the real availability window remains pending. Historical Development HOLD and its source remain recorded;
no fresh human Development signature is invented.

## Current evidence and case assessment

| Area | Current assessment | Evidence or remaining condition |
|---|---|---|
| Local automated verification | **13 gates PASS; 727 distinct mixed methods, 726 PASS / one expected SKIP; separate timing PASS** | Mixed coverage: 2,995/3,381 statements (88.58%), 821/1,000 branches (82.10%), 87.10% combined. [Exact outcomes/source provenance](evidence/sprint-completion-20261118/technical-verification.json) record the fresh clean mixed execution and separately archived initial provenance. |
| Isolated-unit target | **415/415 PASS; 1,547/1,740 function-body statements (88.91%) under the owner boundary** | Clean freeze, 208 verified source pins and zero DB attempts. The retained 288-method baseline passes its tests but covers 1,158/1,740 (66.55%), below 70%. Expanded all-statements companion is 1,547/2,730 (56.67%), not a 70% pass. |
| TC-QUAL-01: browser compatibility and usability | **PARTIAL** | The [primary walkthrough](evidence/issue39/usability-walkthrough-20261109.md) explicitly retains overall PARTIAL. Its 93-second first-use result is owner-reported; exact guide revision, participant code and start/end timing trace were not retained. A visible automated browser workflow cannot establish a new participant's guide use. |
| TC-QUAL-02: office-hours availability | **PENDING** | Real observer job job_c4c3658121/PID 2322483 is installed for 19 November 08:00-20:00 IST. [Exported WAITING snapshot](evidence/sprint-completion-20261118/browser-security/availability/summary.json): 0/1,440 probes; no pass. Missing/failures count; 1,426 successes required. |
| TC-QUAL-03: desktop browser/server portability | **PASS - Codex technical execution** | [Twelve Windows 11/Fedora 44 workflows](evidence/sprint-completion-20261118/browser-security/README.md), nineteen observations each, all 269 accepted source/font pins matched. Real writes/downloads/security/browser-Back/confirmation paths exercised; no human first-use claim. |
| TC-QUAL-04: maintainability | **PARTIAL** | The unit target is evaluated under the recorded owner boundary. Configured Ruff checks and modular apps support the style/design assessment; they do not certify every PEP 8 provision. |
| TC-SEC-08: baseline and triage | **PASS - Codex bounded technical execution** | [Actual triage](evidence/sprint-completion-20261118/browser-security/security/qa-development-triage.md): completed authenticated passive baseline,12 explicit HTTP-200 routes, drained queue. Retain one Medium static 404 CSP finding,Low/Informational observations and five insecure-loopback deploy warnings; no production/TLS approval. |
| TC-PERF-01 / TC-PERF-03 | **Current technical PASS; historical owner passes retained** | [Both full workloads](evidence/sprint-completion-20261118/operations/load-results.json):50 users/600 s each. Baseline 28,952 requests/maximum 1,599 ms; volume 28,806 at 5,000 students/2,000 beds/maximum 1,519 ms; zero errors, 100% under 2 s. |
| #79 / #80 inventory/history corrections | CLOSED | #79 closed earlier; #80 closed with the verified PR #91 correction. Actual source-bound retests and CI remain linked. |
| [HMS-30/#90](https://github.com/Sreeharsha2240/hostel-management-system/issues/90) | CLOSED | Consolidated corrections/retests delivered in merged PR #91 with both supported-Python CI runs passing. Prior High technical assessments and fix history remain retained. |

The current register is **56 historical OWNER PASS / 2 current Codex
technical PASS / 2 PARTIAL / 1 PENDING**. The original 33 remain 32 OWNER PASS /
1 PARTIAL. Passing observations total 58/61 (95.08%); passing or partial
dispositions total 60/61 (98.36%). QUAL-01 usability and QUAL-04 style remain
PARTIAL; QUAL-02 has no completed availability result. The two new technical
passes do not attribute execution to a teammate.

Fresh [session evidence](evidence/sprint-completion-20261118/browser-security/session/result.json)
records 901.003 actual idle seconds without application requests before protected
revisit redirected to login. Historical login-control outliers remain retained;
browser NavigationTiming and WebDriver-inclusive measurements are labelled
separately. [Fresh recovery](evidence/sprint-completion-20261118/operations/recovery-results.json)
records a real natural daily trigger, 3.299-second-old populated restore with
matching counts/row/schema digests and 17 zero-violation checks, plus a stable
read-only browser backup. The temporary task/server were removed; no ongoing
current-browser daily schedule is claimed.

## Requirements and exit criteria

The [Part 3 PDF](SE_Mini_Project_Delivereables_Part-3.pdf) requires updating
earlier cases, completing testing according to the submitted Test Plan and
publishing four distinct reports under `docs/`. Its 2–6 November window has
passed; it specifies no cutoff hour or export format. No instructor acceptance
of late submission is recorded.

| Submitted requirement | Assessment |
|---|---|
| Test Plan section 5: 100% planned cases executed | **NOT MET:** QUAL-01/04 remain PARTIAL and the real QUAL-02 window is PENDING. |
| Test Plan section 5: all High-priority cases passed | SEC-08 technical execution is PASS. Original case/priority acceptance remains distinct; no human agreement is invented. Tracked High defects are now closed. |
| Test Plan section 5: zero open Critical/High defects | **MET for the known tracked fixed inventory:** current GitHub query returns no open issues and #80/#90 are CLOSED. This is a bounded inventory result, not a claim about unreported defects. |
| Test Plan section 5 / section 13.2: every RTM requirement covered by a passed case | **UNVERIFIED.** All 36 original mappings are preserved and accepted as design traceability by the PO and recorded Development review. Accepted passed-case coverage must be decided requirement by requirement. |
| Test Plan section 5: project-guide acceptance walkthrough | **Unmet original course criterion; collection skipped by the actual #43 owner exception.** No guide session/approval is invented; the new-Warden usability task is separate. |
| Test Plan section 15: QA / Development / PO approvals | **Unmet original course criterion; collection skipped by the actual #43 owner exception.** Historical Development HOLD stays recorded; no final human approvals are inferred. |
| SRS section 6.4 unit tests cover >=70% of application logic | **Met under the actual [owner function-body decision](evidence/hms19-function-body-boundary-20261113.md): 88.91%.** The conservative all-statements companion is 56.67%; no instructor endorsement is invented. |
| SRS section 6.4 portability and usability | Desktop/latest-two Windows/Linux workflows and a new-Warden guide task are separate conditions. Physical-phone testing is excluded by the owner; the reported laptop-browser phone-mode check has no retained version/viewport/workflow detail. |
| SAD section 4.4 request-ID error logs and operational monitoring | **Disclosed limitation.** The [PO disposition](evidence/owner-disposition-20261114.md) records these items as unimplemented/unverified for the mini-project. Audit/backup checks do not satisfy them. QA/guide/instructor acceptance remains separate. |

Historical entry approval, late execution and tool/environment substitutions
remain explicit: current testing cannot retroactively establish approved SRS,
reviewed cases or approved environments before earlier runs. Preserve original
MySQL 8.0, Selenium/Postman and browser requirements alongside the actual tools
and MySQL versions used. A mapped test or passing companion proves only its
asserted conditions; the original browser timing, Back/idle and script-execution
subconditions need their own evidence or an actual bounded acceptance decision.

Clean local verification,strict CI artifact reconciliation and PR #91 merge are
complete. Final main verification after this documentation checkpoint and the
candidate package remain pending. Operational0d9adb39 evidence and reviewed
helper-only carry-forward are preserved. Availability and original course
submission criteria keep their separately recorded state.

## Package and external decisions

The owner selected the included [Sprint 2 outcome video](evidence/sprint-recordings/Sprint2_Outcome_Demo.md)
on 18 November. It is 115.148 seconds (1:55), about five seconds shorter than
the nominal two-minute target. Part 2 says "Record a two minute video" and gives
no strict duration bounds or tolerance; instructor tolerance/acceptance is
unspecified. Retain the owner-selected final clip without inventing a need for
replacement or extra footage. The [Sprint 1 recording](evidence/sprint-recordings/README.md)
is 51.719 seconds against the nominal one-minute wording. Neither recording
supplies a guide walkthrough or a final submission receipt.

The owner has excluded collection of final teammate sign-offs and guide
walkthrough from the scoped task, without claiming those original criteria
passed. Instructor late-submission/channel/deadline/format decisions, accepted
course package and a genuine submission receipt remain unrecorded. GitHub
Project synchronization and acceptance of the merge-history burndown
reconstruction remain unconfirmed. See the [submission checklist](../SUBMISSION_CHECKLIST.md).
No issue reopening, external message, submission or human approval is asserted
by this assessment.
