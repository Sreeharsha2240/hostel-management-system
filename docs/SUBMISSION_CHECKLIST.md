# HMS submission checklist

This checklist covers the whole Team 3 submission: planning, design,
implementation, verification and packaging. Historical audit results are
identified below; use the checks on the final submission commit for current
automated evidence. Check the course rubric for required slides, live demo,
signatures and naming; those requirements cannot be inferred from the source
repository.

## Part 3: current testing and reports

Follow the [Part 3 team plan](PART3.md) and the instructor PDF linked there.
Its 2-6 November testing window and the submitted Test Plan govern current
acceptance; historical test totals and scope exclusions below remain context.
The 8 November technical review uses main `b523d4c`; it updates evidence/status
dispositions without claiming new application execution or human acceptance.

- [x] Published Part 3 issues #37-#43 with original case ownership, initial estimates, dependencies, acceptance criteria and the 6 November milestone date.
- [x] Added the instructor Part 3 PDF and a team plan defining the Test Case Document and four distinct report destinations under `docs/part3/`.
- [ ] Update the existing GitHub Project with the Part 3 tasks/estimates/iteration when access is available; the current token lacks `read:project`, so board synchronization remains blocked.
- [x] Publish the updated 61-case Test Case Document and 36-requirement RTM, preserving all 33 original IDs and mappings; merged PR #60 closed #37 for authorized documentation delivery.
- [x] Complete the authorized independent AI technical QA review of HMS-18's original 13 cases, scoped priorities and late-entry/tool/environment dispositions; see the [8 November review](part3/evidence/issue40-final/qa-review-20261108.md). This supplies no named human final approval.
- [x] Execute Devansh's nine remaining expanded regression recipes (HMS-26/#63) after independent technical review, with [clean-commit per-step evidence](part3/evidence/issue63/README.md); all nine passed. Other owners and final acceptance remain separate.
- [ ] Obtain remaining actual team case/priority/RTM and historical entry/deviation acceptance; scoped #40 closure does not execute expanded regression recipes or complete whole-plan acceptance.
- [ ] Complete each member's functional, security, performance/recovery and quality execution with current evidence, defects and retests (#38-#40).
- [x] Publish the System Validation checkpoint (#38), Code Coverage Report and Branch Coverage Report (#42) under `docs/part3/`, with source-bound evidence. Their publication is distinct from complete plan acceptance.
- [ ] Vaishnavi publishes and obtains review of the missing Unit Test Report (#41), using genuine module-owner results and reviewed unit/application-logic attribution. Devansh's [module-owner input](part3/Code_Coverage_Report.md#hms-19-module-owner-input--8-november-2026) is supplied; formal unit70 remains UNPROVEN.
- [ ] Meet the Test Plan exit criteria and record actual QA/Dev/PO approvals and the project-guide acceptance walkthrough; retain failed/blocked criteria and explicit deviations (#43).
- [ ] Verify the one-minute Sprint 1 and two-minute Sprint 2 outcome videos from Part 2 are genuinely available, and confirm submission channel, exact cutoff and export requirements (#43).
- [ ] Publish the final accepted revision and complete the agreed submission; use Sprint 3 only for actual owned development spillover while testing/reporting continue (#43).

## Planning and team records

- [x] Sprint schedule and estimated backlog are documented in `HMS_Part1_Sprint_Backlog.docx`.
- [x] Member responsibilities and test ownership are documented in `HMS_Part1_Work_Distribution.docx`.
- [x] Sprint implementation notes are available in `docs/SPRINT1_TESTING.md` and `docs/SPRINT2.md`.
- [x] Added a two-sprint burndown reconstruction: `docs/BURNDOWN.md`, `docs/burndown.svg` and `docs/BURNDOWN_DATA.csv`. It uses dated merge/closure history and backlog story points, not invented daily board data. The planned 24 Sprint 2 points are recorded as closed by 28 October. HMS-14 / issue #32 was opened on 27 October and was In Progress at the 29 October snapshot, with no estimate or Sprint field, so it is separate follow-up scope. Do not move it to Done just to complete the chart.
- [ ] Confirm the instructor accepts a merge-history reconstruction. If daily board history is required, export it and replace this chart with verified daily values. Confirm whether to estimate/assign HMS-14 to a sprint as an explicit scope change.

## Requirements and design package

- [x] SRS, SAD and Test Plan are present as DOCX files.
- [x] Five PDF copies are present in `pdf/`; compare them to their DOCX sources after any later edits.
- [x] `Design_README.md` and four UML diagrams are present in rendered PNG and editable Mermaid formats.
- [x] The Test Plan contains 33 test cases and an RTM, as listed in README.

## Implementation and Git

- [x] Django source, migrations, dependency manifests, `.env.example`, setup guide and CI workflow are present.
- [x] Bed availability is paginated at 50 rows; a regression test covers page size, total count and page two.
- [x] Pagination and audit fixes from `bf70a66` were included in merged PR #35.
- [ ] Confirm the final submission revision has passed CI and required teammate review. A local run does not replace remote CI or review.
- [ ] Confirm GitHub issue states and owners match the completed work. The Part 1 backlog is a planning artifact, not a current board export.
- [x] Added `.tmp/` to `.gitignore`; keep generated credentials, database dumps, JMeter results and downloaded tools out of the submission.

## Verification evidence

- [ ] Run `python scripts/run_checks.py` on the final revision and inspect all gates, test totals and coverage in `test-results/<run>/run.json`. CI runs the same command on MySQL 8.4 with Python 3.11 and 3.14; download the matching commit's `hms-test-evidence-*` artifacts.
- [x] Historical 29 October SQLite-compatible audit: 154 passed, 0 failures/errors; 163 discovered, with 9 MySQL-specific tests excluded. See `test-evidence/E2E_FINAL_TESTS.txt`. This is not the current MySQL verification result.
- [x] Historical CI run #29 passed MySQL 8.4 on Python 3.11 and 3.14; that run predates pagination. Board/issue status lists HMS-13 Done/closed, but PR #33 review explicitly called it partial and asked to keep it open until populated recovery and concurrent performance evidence. The later local audit supplied a populated restore and 50-user run, but the performance target was exceeded and the post-pagination comparison was blocked.
- [ ] Resolve historical entry and QA evidence/environment acceptance with the team before final acceptance. The original HMS-13 follow-up now has the separate 5 November owner load/recovery evidence linked below; ordinary unit/integration CI does not replace it.
- [x] Before pagination, a 50-user/10-minute-peak local JMeter run completed with no failed samples. The 2,000-bed listing averaged 12.2 seconds (p95 29.6 seconds, maximum 46.8 seconds), which prompted pagination.
- [x] Supply post-pagination owner load evidence: [5 November normal and volume workloads](part3/evidence/issue40-final/README.md), each 50 users for at least 600 seconds, with passing unchanged-threshold results. Retain the earlier blocked post-change attempt and the failed first volume run as history; scoped technical acceptance is recorded in the 8 November AI QA review; actual whole-team acceptance remains pending.
- [x] A populated local MySQL dump restore to a separate database had matching table counts; a manual timestamped backup ZIP passed integrity validation.
- [x] Supply the required daily-backup owner observation: [naturally scheduled populated recovery](part3/evidence/issue40-final/recovery-results.json), preserving all 18 table digests/counts and the live source/task. Earlier scheduling/permission blockers remain historical; the 8 November AI review accepts this scoped technical evidence while retaining historical entry limits and pending actual whole-team acceptance.
- [ ] Obtain required actual HTTP-to-HTTPS, TLS 1.2+ and authenticated Secure/HttpOnly session-cookie evidence (TC-SEC-06 PARTIAL), plus the separate Test Plan §5.1 ZAP baseline (TC-SEC-08 NOT RUN). An isolated real HTTPS endpoint suffices; settings checks alone do not. Record any actual instructor-approved criterion change separately while preserving original outcomes.
- [ ] Walk through Admin, Warden and Student accounts on the final demo host and save only rubric-requested screenshots. Local automated checks do not establish browser/OS compatibility on that host.

## Final packaging

- [ ] Check Git status and include only source, required documents, diagrams and evidence. Exclude `.tmp/`, `.env`, local databases, passwords, backups and raw load files.
- [ ] Follow the README setup from a clean environment and verify demo accounts are fresh, synthetic and distributed only through the instructor-approved channel.
- [ ] Check DOCX/PDF pairs, filenames, team names/IDs, page rendering, links, signatures and rubric-specific cover fields.
- [ ] Confirm whether slides, a demo video or live URL are required. No slide deck is present in this repository.
