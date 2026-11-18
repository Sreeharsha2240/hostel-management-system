# Part 3 assessment — 19 November 2026

**Submission readiness: NOT READY.** The updated 61-case document, 36-row core
RTM and all four required reports are present. Their publication and the closed
tracking issues do not establish the submitted Test Plan's exit criteria.

The initial review-candidate source for this assessment is
`a679ca47c0d642f89b708b9e8473d3a2c62697a7`. Documentation and evidence may be
added after that freeze; each execution must retain its actual checkout,
dirty/clean state and source fingerprints. This is an assisted technical
assessment under the user's authorization across assignees. It supplies no
other person's signature or final acceptance.

**Successor verification in progress:** blind review found an HTML/API bed-
availability mismatch and a duplicate-confirmation problem. Corrections and
coverage-XML path normalization are being verified before the successor code
freeze. The runner now has 13 gates. Current results remain pending; any
measurement on `a679ca4` is evidence for that initial candidate, not for these
subsequent changes.

## Current evidence and case assessment

| Area | Current assessment | Evidence or remaining condition |
|---|---|---|
| Local automated verification | Fresh runner result awaiting durable evidence reconciliation here | The coordinator is publishing the source-bound checks under [current technical evidence](evidence/sprint-completion-20261118/). Do not substitute older CI or coverage figures for the frozen source. |
| Isolated-unit target | Fresh 415-method measurement awaiting durable evidence reconciliation here | Retain the original baseline selection, no-database enforcement and exact source pins. Apply the owner's function-body interpretation and disclose all-statements coverage separately. Earlier 288/294-method measurements remain historical. |
| TC-QUAL-01: browser compatibility and usability | **PARTIAL** | The [primary walkthrough](evidence/issue39/usability-walkthrough-20261109.md) explicitly retains overall PARTIAL. Its 93-second first-use result is owner-reported; exact guide revision, participant code and start/end timing trace were not retained. A visible automated browser workflow cannot establish a new participant's guide use. |
| TC-QUAL-02: office-hours availability | **NOT RUN** | No valid complete 08:00-20:00 working-day observation establishes ≥99%. The failed/aborted earlier attempts remain disclosed in the [follow-up](evidence/remaining-test-gaps-20261115.md). A 19 November 08:00-20:00 IST observation is prepared; job installation and review of its actual probe log and denominator remain pending. |
| TC-QUAL-03: desktop browser and server portability | **NOT RUN** pending current full workflow evidence | The [15 November checks](evidence/remaining-test-gaps-20261115.md) exercised login/pages and an HTTP Linux check, with Edge's previous version missing. Twelve current Windows/Linux browser workflows are in progress; no result is inferred before their versioned workflow records are reconciled. |
| TC-QUAL-04: maintainability | **PARTIAL** | The unit target is evaluated under the recorded owner boundary. Configured Ruff checks and modular apps support the style/design assessment; they do not certify every PEP 8 provision. |
| TC-SEC-08: ZAP/deployment inspection | **PARTIAL** | The historical authenticated passive scan has Low/Informational observations and local HTTP scope. A fresh passive scan is pending. Scanning, alert review, deployment-settings checks and real TLS evidence have distinct scopes. |
| TC-PERF-01 / TC-PERF-03 | Historical **OWNER PASS** observations retained; frozen-source revalidation pending | The [5 November owner results](evidence/issue40-final/README.md) retain both complete workloads and the failed first volume run. Fresh normal/volume workloads, each 50 users for at least 600 seconds, are in progress. |
| #79 / #80 inventory/history corrections | Implemented on the frozen source; final retest/review disposition pending | Local regression evidence is being reconciled. Do not infer issue closure, independent review or a new Development approval from the implementation alone. |

After correcting TC-QUAL-01's aggregate label to match its primary evidence,
the register contains **56 OWNER PASS / 3 PARTIAL / 2 NOT RUN / 0 BLOCKED**.
The original 33 contain **32 OWNER PASS / 1 PARTIAL**. These are attributed
execution dispositions, not accepted passes. OWNER PASS or PARTIAL dispositions
cover 59/61 cases (96.72%); 56/61 are OWNER PASS (91.80%). The three partial cases are
TC-QUAL-01, TC-QUAL-04 and TC-SEC-08. New evidence may change these counts only
after its case conditions have been checked.

## Requirements and exit criteria

The [Part 3 PDF](SE_Mini_Project_Delivereables_Part-3.pdf) requires updating
earlier cases, completing testing according to the submitted Test Plan and
publishing four distinct reports under `docs/`. Its 2–6 November window has
passed; it specifies no cutoff hour or export format. No instructor acceptance
of late submission is recorded.

| Submitted requirement | Assessment |
|---|---|
| Test Plan §5: 100% of planned cases executed | **NOT MET.** The expanded plan has two NOT RUN cases and incomplete cases. A partial observation is not complete execution of every expected condition. |
| Test Plan §5: all High-priority cases passed | **NOT MET.** TC-SEC-08 is High and PARTIAL. The PO and recorded Development review agree to the current 34 High / 27 Medium proposal; actual QA agreement and case acceptance remain pending. The original plan had no per-case priorities. |
| Test Plan §5: zero open Critical/High defects | **UNVERIFIED** for the complete frozen-source inventory. Closed defects and implemented fixes do not certify inventory completeness, severity review or acceptance of all current retests. |
| Test Plan §5 / §13.2: every RTM requirement covered by a passed case | **UNVERIFIED.** All 36 original mappings are preserved and accepted as design traceability by the PO and recorded Development review. Accepted passed-case coverage must be decided requirement by requirement. |
| Test Plan §5: project-guide acceptance walkthrough | **PENDING.** A real guide must review the revision-bound main flows and record findings and a decision. The owner-reported new-Warden task is a separate usability observation. |
| Test Plan §15: QA / Development / PO approvals | **PENDING** for the final revision and package. The [14 November Development decision](Development_Review_20261114.md) is HOLD; later fixes do not silently convert it to approval. |
| SRS §6.4 unit tests cover ≥70% of application logic | Apply the actual [owner function-body decision](evidence/hms19-function-body-boundary-20261113.md); retain the conservative all-statements diagnostic. This is a project-owner interpretation, with no invented instructor endorsement. |
| SRS §6.4 portability and usability | Desktop/latest-two Windows/Linux workflows and a new-Warden guide task are separate conditions. Physical-phone testing is excluded by the owner; the reported laptop-browser phone-mode check has no retained version/viewport/workflow detail. |
| SAD section 4.4 request-ID error logs and operational monitoring | **Disclosed limitation.** The [PO disposition](evidence/owner-disposition-20261114.md) records these items as unimplemented/unverified for the mini-project. Audit/backup checks do not satisfy them. QA/guide/instructor acceptance remains separate. |

Historical entry approval, late execution and tool/environment substitutions
remain explicit: current testing cannot retroactively establish approved SRS,
reviewed cases or approved environments before earlier runs. Preserve original
MySQL 8.0, Selenium/Postman and browser requirements alongside the actual tools
and MySQL versions used. A mapped test or passing companion proves only its
asserted conditions; the original browser timing, Back/idle and script-execution
subconditions need their own evidence or an actual bounded acceptance decision.

## Package and external decisions

The owner selected the included [Sprint 2 outcome video](evidence/sprint-recordings/Sprint2_Outcome_Demo.md)
on 18 November. It is 115.148 seconds (1:55), about five seconds below the
two-minute minimum; owner publication authorization is recorded, while team
and instructor acceptance of the shortfall is not. The [Sprint 1 recording](evidence/sprint-recordings/README.md)
is 51.719 seconds. Neither recording supplies a guide walkthrough or a final
submission receipt.

Final QA/Development/PO decisions, case-owner evidence acceptance, guide
walkthrough, instructor late-submission/channel/deadline/format decisions,
accepted final package and a genuine submission receipt remain outstanding.
GitHub Project synchronization and the acceptability of the merge-history
burndown reconstruction also remain unconfirmed. See the [submission
checklist](../SUBMISSION_CHECKLIST.md). No issue-state change, external message,
submission or human approval is asserted by this assessment.
