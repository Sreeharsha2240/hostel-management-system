# Part 3: testing, reports and team delivery

**13 November HMS-19 completion:** PR #74 merged as `a41f884`, and issue #41 is closed. The owner-approved function-body unit-coverage boundary measures 946/946 (100%) across 288 isolated methods, meeting the 70% target under that definition. The companion all-application-statements result remains 946/1,703 (55.55%) and is disclosed in the [Unit Test Report](part3/Unit_Test_Report.md). See the [owner boundary decision](part3/evidence/hms19-function-body-boundary-20261113.md).

**14 November current scope and readiness:** real-phone testing is excluded from this mini-project. HMS-19/#41 is complete; the older issue and case snapshots below are historical. Remaining case work is TC-SEC-08 (PARTIAL ZAP disposition), TC-QUAL-02 (working-hours availability, NOT RUN), TC-QUAL-03 (desktop browser/OS portability, NOT RUN), plus review of remaining case/priority acceptance. The Sprint 1 demo is now included; the Sprint 2 video, final team approvals, instructor submission details, and final package/receipt remain outstanding. See the [current readiness checkpoint](part3/HMS21_Final_Readiness.md).

**10 November tracking update:** #38, #39 and #43 are now closed for their documented limited project scopes; #41 is the only open issue. The [HMS-16 QA handoff reconciliation](part3/evidence/issue38-security-20261110/qa-disposition-reconciliation.md) records the two ZAP alert assessments and locates the passing login `next` regression test. TC-SEC-08 remains PARTIAL, the desktop browser/OS matrix and working-hours availability are unverified, and the original Test Plan/submission package remains NOT READY. Dated issue states below are historical snapshots.

This is the team work plan for **2-6 November 2026**. The assigned contributors
execute their cases and prepare their own evidence. At the 8 November review,
#37's case-document delivery and #42's coverage-reporting task are closed;
#38/#39/#41/#43 retain outstanding work; the later [HMS-18 scoped AI QA review](part3/evidence/issue40-final/qa-review-20261108.md) accepts #40 for technical closure. Vaishnavi coordinates QA, Devansh leads
development/coverage, and Sreeharsha coordinates integration and final readiness.

## Instructions and baseline

The [Part 3 instructions](part3/SE_Mini_Project_Delivereables_Part-3.pdf), page 1,
require updated test cases and the Test Case Document, all testing according to
the submitted Test Plan, and four reports uploaded to `docs/`. Sprint 3 is
optional for actual development spillover, with testing/reporting in parallel.
The PDF gives the **2-6 November** window but no submission hour or report format.
The year 2026 follows the Part 1/2 project schedule. Intermediate dates,
estimates, Markdown filenames and the milestone are team planning choices.
The milestone represents the 6 November date, not a faculty-specified cutoff time.

Use these source documents together:

- [Test Plan](../Test_Plan_Hostel_Management_System.docx), especially sections 5,
  5.1, 6, 9, 13-15, and its [PDF](../pdf/Test_Plan_Hostel_Management_System.pdf).
- [SRS](../SRS_Hostel_Management_System.docx) and
  [SAD](../SAD_Hostel_Management_System.docx), with their copies under `pdf/`.
- [Work Distribution](../HMS_Part1_Work_Distribution.docx) and
  [Sprint Backlog](../HMS_Part1_Sprint_Backlog.docx) for existing ownership.
- [Sprint 1 testing](SPRINT1_TESTING.md), [Sprint 2 notes](SPRINT2.md) and the
  [submission checklist](SUBMISSION_CHECKLIST.md).

The original Test Plan contains **33 planned case IDs** and an RTM for
**36 requirements** (REQ-1 through REQ-24, NFR-1 through NFR-12), plus quality
attributes. The updated Test Case Document must retain these IDs, explain
revisions, add sprint regression cases and map automated methods to them.
The delivered register preserves the original IDs/mappings and contains 61
complete records. Its High/Medium priorities are proposals requiring QA review
because the original case table lacks priority fields. The register reconciles
TC-AUTH-03's old lockout-message wording with SRS REQ-2's generic credential-error
requirement while retaining the original wording and five-attempt/15-minute test.

[PR #36](https://github.com/Sreeharsha2240/hostel-management-system/pull/36)
was still open at setup on 2 November; `main` was `0abb29a` and the verified code
candidate was `d77a1c0`. Its [CI baseline](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/41334260491)
recorded 185 mixed unit/integration/system methods, one expected timing skip
under coverage followed by a separate timing pass, 94.28% statement coverage,
85.57% branch coverage and 92.63% combined coverage. Final reports must identify
the accepted submission revision and its own evidence; the baseline does not
establish execution of all planned cases.

## Assigned backlog

The seven planned tasks and subsequent defects belong to the [Part 3 milestone](https://github.com/Sreeharsha2240/hostel-management-system/milestone/1). Estimates
are initial planning values for team review, not historical effort or an
instructor requirement. The historical Sprint 1/2 issues stay closed.

| Work | Accountable contributor | Initial points | Dependency / output |
|---|---|---:|---|
| [HMS-15 / #37](https://github.com/Sreeharsha2240/hostel-management-system/issues/37) | Vaishnavi (`VaishnaviCH6`); Devansh completed reconciliation | 3 | [Complete case document and RTM](part3/Test_Case_Document.md): 33 original IDs, ten retained regression IDs, 18 explicit additions, source-bound results and remaining execution gaps |
| [HMS-16 / #38](https://github.com/Sreeharsha2240/hostel-management-system/issues/38) | Sreeharsha (`harsha2240`) | 8 | 12 auth/user/security cases; System Validation Report integrates other owners' evidence with QA |
| [HMS-17 / #39](https://github.com/Sreeharsha2240/hostel-management-system/issues/39) | Vaishnavi (`VaishnaviCH6`) | 5 | 8 student/hostel/quality cases; feeds System Validation Report |
| [HMS-18 / #40](https://github.com/Sreeharsha2240/hostel-management-system/issues/40) | Devansh (`DevaOnL`) | 8 | 13 allocation/payment/report/performance/recovery cases; [recorded execution and owner appendix](part3/evidence/issue40-final/README.md), merged evidence with [authorized scoped AI QA acceptance](part3/evidence/issue40-final/qa-review-20261108.md); feeds System Validation Report, with actual final human approvals separate |
| [HMS-19 / #41](https://github.com/Sreeharsha2240/hostel-management-system/issues/41) | Vaishnavi (`VaishnaviCH6`); Sreeharsha co-assignee | 3 | Completed in merged PR #74: 288 isolated methods pass; 946/946 (100%) function-body statement coverage under the owner-approved boundary; 55.55% all-statements result remains disclosed |
| [HMS-20 / #42](https://github.com/Sreeharsha2240/hostel-management-system/issues/42) | Devansh (`DevaOnL`) | 3 | Two distinct coverage reports are published and the reporting issue is closed; the later owner function-body interpretation is recorded above; the separate all-statements unit measure remains below 70% |
| [HMS-21 / #43](https://github.com/Sreeharsha2240/hostel-management-system/issues/43) | Sreeharsha (`harsha2240`) | 2 | [Final readiness checkpoint](part3/HMS21_Final_Readiness.md); final review, required approvals and submission confirmation remain open |

The 4 November requirements audit found actual development spillover in
Devansh's scope. These Sprint 3 defects were fixed in merged PR #44 and
Sreeharsha's merged PR #49; #45-#48 are closed. The Part 3 reporting
assignments continue in parallel:

| Defect | Owner | Required correction |
|---|---|---|
| [HMS-22 / #45](https://github.com/Sreeharsha2240/hostel-management-system/issues/45) | Devansh | Payment report Bed field in HTML/JSON/CSV; correct TC-RPT-01 evidence |
| [HMS-23 / #46](https://github.com/Sreeharsha2240/hostel-management-system/issues/46) | Devansh | Transfer/release confirmation dialogs, cancellation and acceptance checks |
| [HMS-24 / #47](https://github.com/Sreeharsha2240/hostel-management-system/issues/47) | Devansh | DD-MM-YYYY allocation list/history dates; preserve ISO JSON |
| [HMS-25 / #48](https://github.com/Sreeharsha2240/hostel-management-system/issues/48) | Sreeharsha | DD-MM-YYYY student self-service allocation/history/payment dates |

See the [source-bound retest evidence](part3/evidence/owned-defects/README.md).
Historical case JSON and coverage measurements are preserved. Unit-scope
clarification belongs to existing #41/#42, rather than a duplicate issue.

Devansh's [5 November current-main execution and owner appendix](part3/evidence/issue40-final/README.md)
provide fresh results for all 13 HMS-18 cases after PRs #44/#49 merged, including
both full load workloads and naturally scheduled populated recovery. The first
volume attempt failed after confirmed laptop standby; its raw metrics and the
complete unchanged-threshold rerun are both retained. Handoff is supplied for
#37's case document and #38's report. PR #50 was merged by `harsha2240` on
5 November; no formal APPROVED review is recorded. The [shared case register](part3/Test_Case_Document.md#53-hms-18-owner-execution-and-evidence-reconciliation)
links Devansh's 13 original results as OWNER PASS; their scoped AI technical acceptance is now recorded in the later review.
Sreeharsha approved and merged [PR #54](https://github.com/Sreeharsha2240/hostel-management-system/pull/54)
on 6 November. That review accepts the documentation/evidence reconciliation
while explicitly preserving the open QA acceptance and unproven unit-coverage
criterion; it does not approve the reviewed-case entry criterion retrospectively.
At that checkpoint, #40 remained open for reviewed-case/entry, priority and
environment/evidence dispositions. The later [authorized independent AI QA review](part3/evidence/issue40-final/qa-review-20261108.md)
resolves those technical dispositions for #40 closure, with nine High/four Medium
priorities and explicit historical-entry/environment limits. #37's documentation
delivery and this scoped review do not supply actual final human approvals or
retroactively establish pre-execution entry compliance.
The appendix does not complete either teammate's deliverable or global readiness.

The 8 November technical review of main `b523d4c` is recorded in the
[HMS-21 readiness checkpoint](part3/HMS21_Final_Readiness.md). PR #58 is
merged, but issue #39 remains open: its evidence disposition includes one
NOT RUN case and one PARTIAL quality case. HMS-16's report now incorporates
that evidence without claiming team-wide acceptance. The required Unit Test
Report is still absent, so the four-report package is incomplete and the
submission remains NOT READY. The [independent report review](part3/System_Validation_Report.md#independent-evidence-review-and-current-build)
adds source-bound CI/case/defect metrics, original security subcondition limits
and explicit owner actions. Devansh's [module-owner inputs for #41](part3/Code_Coverage_Report.md#hms-19-module-owner-input--8-november-2026)
reuse published classifications/results without claiming accepted unit70 or
writing Vaishnavi's report. Development recommends retaining the original TLS/ZAP
criteria and collecting isolated real evidence; no team/instructor criterion
change or final QA/Dev/PO approval is recorded by that technical review.

Original execution ownership is preserved:

| Owner | Existing case IDs | Count |
|---|---|---:|
| Sreeharsha | TC-AUTH-01 to TC-AUTH-04; TC-USR-01; TC-SEC-01 to TC-SEC-07 | 12 |
| Vaishnavi | TC-STU-01 to TC-STU-05; TC-HST-01 to TC-HST-02; TC-QUAL-01 | 8 |
| Devansh | TC-ALC-01 to TC-ALC-06; TC-PAY-01 to TC-PAY-02; TC-RPT-01; TC-PERF-01 to TC-PERF-03; TC-OPS-01 | 13 |

Vaishnavi coordinates the case register, execution summaries and QA review;
Sreeharsha coordinates the integrated System Validation Report and PO readiness;
Devansh supports unit tests, coverage, triage and technical fixes. Each author
opens their own focused PR and receives independent teammate review as described
in [README](../README.md#team-collaboration-hms-03). Record actual contributors
and approvals; preserve truthful contribution/signature histories.

GitHub Project synchronization is **blocked**: the current token lacks
`read:project` scope. Issues, labels and the milestone are the published planning
view. The final coordination task tracks adding these issues to the existing
Project and setting Status, Estimate and Part 3 iteration when access is available.
Preserve Sprint 1/2 history and record the Project update only once it happens.

## Order and dates

| Date | Internal team plan |
|---|---|
| 2 November | Confirm accepted test build/environment and access; start case review, unit/coverage work, deployment/load/backup setup and execution of reviewed cases |
| 3 November | Target initial reviewed Test Case Document/RTM; continue all three owners' execution in parallel |
| 3-5 November | Functional, security, performance/recovery and quality testing; log owned defects, fix and retest affected cases; draft reports continuously |
| 6 November | Finish report reconciliation, independent review, QA/Dev/PO approvals, guide acceptance walkthrough and publication/submission checks |

Only real development spillover or newly discovered defects justify Sprint 3.
Create owned, estimated defect/spillover issues linked to the failed case and
parent execution task; record dependencies and rerun evidence. Add a Sprint 3
milestone/iteration if needed for that scope. Continue testing and report
preparation in parallel during 2-6 November. Pending report writing alone does
not establish another development sprint. Confirm the exact submission channel,
cutoff and export requirements with the instructor through the normal team process.

## Deliverable destinations and completion evidence

The table lists the required outputs and their current owners. HMS-19's Unit Test
Report is published and its owner-approved function-body result meets the 70%
target; the all-statements result remains disclosed. The whole-plan package is
still NOT READY. Markdown is the team's working format; confirm whether the
instructor also needs PDF/DOCX exports.

| Output under `docs/` | Owner / contributors | Required content |
|---|---|---|
| [Test Case Document and RTM](part3/Test_Case_Document.md) | Vaishnavi; all original case owners; Devansh reconciliation | Revision history, retained/new case IDs, proposed priorities, requirement/RTM, level/type, owner, prerequisites/data, steps, expected/actual results, status, tested commit, evidence and defects/retests |
| [Unit Test Report](part3/Unit_Test_Report.md) | Vaishnavi coordinates; Sreeharsha supplies this report contribution; module owners supply results | Published through merged PR #74; owner-approved function-body unit coverage is 100% (946/946); companion all-statements result is 55.55% and remains disclosed |
| [System Validation Report](part3/System_Validation_Report.md) | Sreeharsha integrates; QA consolidates; all owners execute | Entry/exit criteria, all planned functional/security/performance/recovery/quality cases, RTM, observed results, execution/pass/fail/requirement percentages, defect density/aging, blockers, deviations, readiness and actual approvals |
| [Code Coverage Report](part3/Code_Coverage_Report.md) | Devansh; independent reviewer | Per-module/total measured, executed and missing statements, statement percentages, application-logic scope, omissions and SRS coverage assessment |
| [Branch Coverage Report](part3/Branch_Coverage_Report.md) | Devansh; independent reviewer | Per-module/total measured, covered, missing and partial branches, branch percentages, gaps/exclusions and interpretation |

**Historical 6 November coverage report snapshot:** The two coverage reports then used [main measurements](part3/evidence/issue42-main/README.md) on clean `b936e4d`: all 12 gates passed, with 190 methods (189 PASS, one expected timing skip followed by a separate timing PASS). Mixed coverage was **1,584/1,772 statements (89.39%)**, **342/424 branches (80.66%)**, and **87.70% combined**. These are historical project-wide coverage results; the later HMS-19 result is recorded above.

The historical proposed conservative76 selection passed **76/76** on that snapshot. Its startup-inclusive application statement observation was **1,127/1,677 (67.20%)**, while exact selected-method attribution was **414/1,677 (24.69%)**. These are retained historical diagnostics, superseded for HMS-19 by the current disposition at the top of this document.

The original proposed classification and 76/100 selection are preserved as historical work. PR #57 merged as `c9f30a4` and closed #42 as the reporting task. The later owner-approved function-body unit result and closed #41 are recorded at the top of this document. The [earlier 6 November evidence](part3/evidence/issue42-final/README.md), [4 November diagnostics](part3/evidence/owned-defects/coverage-notes.md) and [3 November evidence](part3/evidence/issue42/README.md) remain historical. Accepted submission-build decisions and teammates' deliverables remain with their assigned owners.

Keep four distinct reports. Every report names the exact tested commit/tree,
run date, tool/environment versions, data/setup, reproducible commands/steps,
results and limits. Store relevant sanitized supporting logs/metrics under
`docs/part3/evidence/`, with links from reports and the case register. Record
PASS, FAIL, BLOCKED and NOT RUN accurately. Include owned defects and rerun
results after changes. Preserve historical evidence under `test-evidence/`;
its October scope statements do not waive the submitted Test Plan for Part 3.

## Execution and acceptance checks

Existing automation is available. Use the documented MySQL environment and run
**one database suite at a time** against the disposable test database:

```sh
python scripts/run_checks.py
```

Inspect all 12 gates and the matching JUnit, `coverage.json`, `coverage.xml`,
`run.json` and `timing-smoke.txt` under `test-results/<run>/`. The runner records
a timing skip under coverage and runs that check separately without tracing.
Classify actual unit results; the complete Django suite includes integration,
concurrency and system tests. Reuse a matching verified run between unit and
coverage reports, coordinating execution rather than launching competing suites.
The `.coveragerc` gate is **70% combined statement/branch coverage**; the SRS
requires **unit tests to cover at least 70% of application logic**. Define and
review the unit-test scope in #41/#42 and measure or separately attribute its
coverage; record the target as unproven if that evidence is unavailable. The
mixed-suite percentage alone cannot establish this unit-test target. Report
statements and branches separately with scope/denominators. The Part 3 PDF specifies no separate branch
percentage threshold. Coverage alone does not establish RTM/system acceptance.

Download the final revision's Python 3.11/3.14 MySQL CI artifacts before their
30-day expiry. Save durable sanitized evidence in the repository; temporary
artifacts and links alone do not satisfy the four required reports. Record
differences from the original Test Plan environment/tools (for example MySQL 8.4
versus its 8.0 baseline) and their rationale. Use synthetic students and isolated
test resources; keep credentials, real student data, database dumps and
unredacted scan/load data private.

The assigned execution issues explicitly cover these acceptance areas:

- Security: generic credential errors, five-attempt/15-minute lockout, role and
  own-record isolation, CSRF/injection/XSS handling, audit retention/attribution,
  ZAP/deployment checks, actual TLS 1.2+ and secure session behavior.
- Performance: 50 concurrent users for 10 minutes, at least 95% of page requests
  within 2 seconds with no errors in the normal workload; 20 allocation timings under 3 seconds including save and
  concurrent-conflict correctness; 5,000 students/2,000 beds and search within
  2 seconds. The completed post-pagination comparison and full volume rerun are
  linked in the HMS-18 evidence above; earlier failed/blocked attempts remain
  historical evidence alongside those recorded passing results.
- Recovery: actual daily backup execution, a last-24-hour backup, populated
  restore into a separate database, completeness/consistency and at most
  24 hours of data loss. A one-off dump does not demonstrate scheduling.
- Quality: latest two Chrome/Firefox/Edge versions, Windows/Linux server
  portability, a new-warden guide task within 5 minutes,
  and the at-least-99% availability target during 8 AM-8 PM on working days
  with an observation method/period and stated limits.

The owner-approved mini-project scope removes real-phone testing from the quality
acceptance criteria; TC-QUAL-03 still requires desktop browser and server OS
portability evidence. Test Plan section 5 requires reviewed cases, an approved SRS, a deployed test
build and loaded data before execution. Its exit criteria are: **100% of planned
cases executed, all High-priority cases passed, zero critical/high defects open,
and every RTM requirement covered by a passed case**. Missing access, failed
thresholds and unexecuted cases remain explicit blockers with owners/next steps.
Record actual QA/Dev/PO approvals and the guide acceptance walkthrough; an
unmet original criterion means not ready against the submitted Test Plan. Record
any instructor-approved requirement/criterion change separately with its
authority, date and rationale, retaining the original outcome. Failed, blocked
and not-run cases keep their actual statuses. Never infer a pass from an old issue's closed state.

The final coordination task also checks inherited Part 2 obligations: the
owner-provided [Sprint 1 demo](part3/evidence/sprint-recordings/Sprint1_Outcome_Demo.mp4)
is now tracked and is 51.7 seconds, within the one-minute target. The two-minute
Sprint 2 outcome video is still missing; locate/publish it or record the gap.
Keep the original documents, diagrams, historical charts and evidence intact;
record changes and confirm DOCX/PDF pairs and any final instructor packaging rules.

## 8 November owner follow-up

[HMS-26 / #63](https://github.com/Sreeharsha2240/hostel-management-system/issues/63)
tracks Devansh's nine remaining expanded recipes S2-08..16 (initial estimate:
3 points, Part 3 milestone). The [clean owner execution](part3/evidence/issue63/README.md)
records nine PASS after independent technical review, completing all 27
exclusively Devansh-owned case observations. Expanded totals are 48 OWNER PASS /
3 PARTIAL / 9 NOT RUN / 1 BLOCKED; original 33 remain 30/2/1. The nine cases are
separate from the 190 mixed core methods and do not establish unit70.
Review/execution on 8 November is late against the original window; no waiver
is implied. Existing teammate issues and actual final approvals/submission
remain pending; whole-plan readiness stays NOT READY.
