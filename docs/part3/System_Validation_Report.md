# System Validation Report — HMS Part 3

**14 November current status:** HMS-19/#41 is complete through PR #74 (`a41f884`), with 946/946 (100%) function-body statements covered by 288 isolated methods under the owner-approved definition; the all-application-statements result remains 55.55%. PR #76 is merged as `dd747ff`; it changes documentation and adds the Sprint 1 demo, not application/test/configuration code. The current case ledger is 57 OWNER PASS / 2 PARTIAL / 2 NOT RUN / 0 BLOCKED. TC-SEC-08 remains PARTIAL after QA assessed the two alerts in the supplied 10 November handoff; TC-QUAL-02 and desktop browser/OS TC-QUAL-03 remain NOT RUN; TC-QUAL-04 remains PARTIAL for style assessment beyond configured checks. Real-phone testing is out of scope. Whole-plan readiness remains NOT READY pending the stated project, team and instructor dependencies. Dated sections below preserve historical status and metrics.

## Current SAD alignment and project-scope gaps — 14 November 2026

The SAD §4.4 requires error logs to carry a request ID, operational monitoring of login failures, HTTP error rates, average response time, backup success and database free space, and weekly review. The current application code has no request-ID middleware/log field and no operational metrics/weekly review mechanism. Audit events are present, but they do not provide those operational measurements. These SAD items remain **not implemented/not evidenced**; this report does not imply production monitoring exists. They need an explicit QA/PO scope disposition or implementation before being claimed as complete.

The SRS REQ-24 promises each student their own profile, current allocation and payment status, but it does not enumerate all profile fields. The current My Records page shows the student's name and ID, own current allocation and allocation history, and own payment summary/history. This is the evidenced field boundary for the current implementation. Additional personal fields are not treated as required until QA/PO clarify the intended profile-field list. Existing owner/CI checks cover linked-account isolation; they do not settle that requirements ambiguity.

These documented scope questions supplement the case register and are separate from the owner-approved removal of physical-phone testing. No real-phone test is expected for this mini-project.

**10 November HMS-16 QA addendum:** The [supplied QA handoff and evidence reconciliation](evidence/issue38-security-20261110/qa-disposition-reconciliation.md) assesses the remaining ZAP observations: the Low `Server` banner belongs to the temporary probe server, and the Informational `next` hotspot has no demonstrated reflection or redirect use in the inspected login path. No HMS application fix or fix retest is indicated for either finding. The handoff's statement that the `next` regression test could not be found is corrected by `accounts/test_security.py` and a passing 10 November JUnit result. The recorded scan remains 0 High / 0 Medium / 1 Low / 1 Informational; **TC-SEC-08 remains PARTIAL** for the passive loopback scope. HMS-16/#38 was already closed for owner-authorized local-project tracking, while whole-plan readiness remains NOT READY.

**Historical 10 November HMS-17 completion snapshot:** [fresh isolated execution](evidence/issue39/completion-20261110/README.md)
passes four remaining regression recipes and Warden registration. Full verification:
211 mixed methods (210 PASS / one expected timing SKIP), separate timing PASS,
all 12 gates. All original 33 are now recorded as OWNER PASS; this is not
independent QA acceptance. At that dated snapshot, the expanded register was 57 OWNER PASS / 1 PARTIAL / 2 NOT RUN /
1 BLOCKED. The project owner explicitly authorized #39 tracking closure with the
then-recorded browser/real-phone matrix and working-hours availability unverified.
The current owner decision removes physical-phone testing from this mini-project;
the current ledger and remaining desktop/OS scope are stated at the top of this report.

**Historical HMS-16 owner-reported outcomes: 11 OWNER PASS, 1 PARTIAL. Whole-plan readiness: NOT READY.** The historical focused run tested the 5 November `main` revision `8322b4c20c067d512c4bb439fdedd19d4fa27223` using synthetic data and a disposable local MySQL 8.0.46 instance. It does not claim a deployed HTTPS endpoint, complete whole-plan acceptance, or team approvals.

**Independent technical review:** 8 November 2026, at merged main `b523d4c7abb77072bea48ac059be7f72396e8a79` (tree `56f7fb4307bc2ce4f3595aebfd5915ce301c3fb7`). This review was performed under Devansh's instruction with three fresh automated reviewers. It reviews existing evidence and supplies corrections; it is not a human QA/Dev/PO signature, a criterion change, a new owner execution or selection of the final submission revision. The [sanitized review extraction](evidence/issue38/independent-review-20261108.json) retains source hashes, arithmetic, actual issue dates and exact-main CI input hashes.

## HMS-16 execution environment and results

**Current-main development addendum — 8 November 2026:** the [development review and #41 handoff](Development_Review_20261108.md) reviews `cae69ea2192838b7874ad5be240def842f5aab5e` (tree `4f81f4a5e100f6a3f22505acfa05b4dd0ff9bb1f`). PR #64 is merged; #40/#63 are CLOSED. [Main CI 42461981682](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42461981682) passes both Python jobs, including nine explicit expanded integration cases. The final development decision is **HOLD**: missing Unit Test Report, transport/ZAP evidence and whole-plan/package acceptance remain unresolved. This supplements the earlier `b523d4c` review; historical executions below retain their actual source and dates.

| Field | Result |
|---|---|
| Tested source | `8322b4c20c067d512c4bb439fdedd19d4fa27223` (`main`, fetched 5 November 2026) |
| Environment | Windows 11; Python 3.14.0; Django 5.2.19; mysqlclient 2.3.0; MySQL 8.0.46 |
| Database | New disposable local MySQL instance on loopback; Django test database created and destroyed by the test runner; synthetic fixtures only |
| Focused command | `python manage.py test accounts.tests accounts.test_security audit.tests students.test_self_service students.tests.StudentManagementViewTests.test_student_list_escapes_script_payload_and_search_treats_sql_as_literal --noinput -v 1` |
| Focused result | Historical owner report: **47 passed, 0 failures, 0 errors; 104.605 seconds** |
| Deployment-settings check | Historical owner report: `python manage.py check --deploy --database default` passed with secure-cookie, HTTPS-redirect and HSTS settings enabled; no warnings |
| Migration checks | Historical owner report: `python manage.py migrate --check` and `python manage.py makemigrations --check --dry-run`: passed after applying migrations to the disposable base database |

The published HMS-16 evidence retains the command, environment and owner summary; raw focused JUnit/stdout and effective deployment-check configuration are not committed. No raw result is reconstructed.

The focused suite exercises login and role redirects, generic invalid-credential responses, five-failure lockout and expired-lock recovery, session timeout/logout, administrator account create/update/deactivate and non-admin denial, student self-record isolation, password hashing/policy, CSRF rejection, injection handling and audit actor/integrity behavior.

A separate full-runner attempt on the same source reported the verification-harness test `tests.test_checks.VerificationRunnerTests.test_xml_keeps_same_named_package_files_and_only_selected_context_hits` failed: on this Windows run, generated Cobertura XML reported 0 covered lines instead of 4 while the test fixture was under the restricted AppContainer temporary path. The root cause is not confirmed. The old report's count line listed 190 discovered tests, 189 passed, one skipped and one failed; those outcome counts sum to 191, and the raw JUnit report is not retained in the published HMS-16 evidence. Treat the Windows outcome as a recorded historical harness failure, not a reconciled 190-test total. A fresh current-source CI run is recorded below. The old run's 93.22% branch-aware figure is informational because that run failed. Its initial `migrate --check` also ran before the new local application database had been migrated; the check passed after migrations were applied.

<a id="hms-16-case-outcomes"></a>

## HMS-16 case outcomes

The table preserves the historical owner-reported outcomes: 11 OWNER PASS and TC-SEC-06 PARTIAL. Passing focused methods do not independently establish every original case subcondition. Original-case gaps, separate companion evidence and pending QA dispositions remain recorded in the [complete case register](Test_Case_Document.md#13-complete-case-records). Method names below describe companion scope; the historical command and environment are recorded above.

| Case | Result and evidence | Status |
|---|---|---|
| TC-AUTH-01 — valid login | `AuthenticationTests.test_login_shows_role_dashboard_and_logout_clears_session`; `test_each_role_can_access_dashboard_and_dashboard_reflects_role` | OWNER PASS |
| TC-AUTH-02 — invalid login | `AuthenticationTests.test_invalid_password_is_generic_and_locks_after_five_attempts`; locked-account generic-response check | OWNER PASS |
| TC-AUTH-03 — five failures / lockout | Five failed attempts activate the lock; expired-lock recovery and reset are exercised. The application policy is 15 minutes. | OWNER PASS |
| TC-AUTH-04 — logout / timeout | `AuthenticationTests.test_expired_session_requires_login`; `SessionAndLockoutTests.test_server_session_expiry_logout_and_cache_control` | OWNER PASS |
| TC-USR-01 — user administration | Admin create/update/deactivate and Warden/Student denial tests; password is stored as a hash and weak passwords are rejected | OWNER PASS |
| TC-SEC-01 — role access | Role dashboards, account-management denial and audit endpoint role checks | OWNER PASS |
| TC-SEC-02 — student data isolation | `StudentSelfServiceTests.test_student_sees_only_own_allocation_and_payment_details` | OWNER PASS |
| TC-SEC-03 — injection handling | `StudentManagementViewTests.test_student_list_escapes_script_payload_and_search_treats_sql_as_literal` | OWNER PASS |
| TC-SEC-04 — password storage/policy | Account creation verifies `check_password`; weak and similar passwords are rejected | OWNER PASS |
| TC-SEC-05 — CSRF | `SessionAndLockoutTests.test_login_post_is_protected_by_csrf` rejects a tokenless POST with HTTP 403 | OWNER PASS |
| TC-SEC-06 — HTTPS/cookies | Secure and HttpOnly session-cookie flags, plus Secure CSRF-cookie flags pass in the Django test client; production-style `check --deploy` passes. No real TLS endpoint or HTTP-to-HTTPS exchange was tested. | PARTIAL |
| TC-SEC-07 — administrative audit | Admin actor attribution, create/update/deactivate events, secret minimization and immutable audit-event tests | OWNER PASS |

At the time of this historical review, TC-SEC-06 remained PARTIAL pending actual HTTP-to-HTTPS redirection, TLS protocol validation and authenticated Secure/HttpOnly session-cookie inspection. The 9 November loopback probe below subsequently supplied those observations for an isolated test instance. The submitted Test Plan separately requires an OWASP ZAP baseline (TC-SEC-08 in the updated register). Public hosting is unnecessary for the recorded local probe; it does not claim production TLS. Any actual instructor-approved change to original criteria must be recorded separately with authority, date and rationale.

### Independent review of original security subconditions

These are evidence gaps requiring owner execution or actual QA disposition, rather than demonstrated application failures. Retain the historical OWNER PASS labels as attributed observations; they are not accepted full-case passes.

| Original case | Limit in the retained focused evidence / next evidence needed |
|---|---|
| TC-AUTH-01 | Existing timing measures login POST and dashboard GET separately; no retained submit-to-visible-dashboard browser timing establishes the original two-second journey. |
| TC-AUTH-02 | Wrong-password generic text is asserted; unknown-user response equality and logged-out state are not asserted by the cited focused methods. |
| TC-AUTH-03 | Expired-lock recovery shortens the stored deadline; static policy is five failures/15 minutes, without a retained real-duration observation. Preserve the register's original-wording/SRS generic-response reconciliation. |
| TC-AUTH-04 | Simulated expiry and cache headers do not observe browser Back or an actual 15-minute idle interval. |
| TC-SEC-01 | The focused selection does not execute the full hostel/student/allocation direct-URL matrix. Current Warden hostel denial is HTTP 403 with a different message from the original literal `Access denied`; obtain a precise wording disposition rather than claim equality. |
| TC-SEC-02 | The own-records route has no ID path segment. Own-page filtering is supported; execute/dispose the actual alternate-ID routes and record the adaptation. |
| TC-SEC-03 | Escaped ORM-seeded student-name/search output is supported; login-username SQL payload, actual form-path storage and real-browser script nonexecution are not established by that method. |
| TC-SEC-04 | Password verification and other weak-password checks are supported; PBKDF2 metadata inspection and the original exact `abc` negative input lack a retained assertion. Publish no hash/password values. |
| TC-SEC-05 / broader NFR-10 | The tokenless login POST is a valid state-changing POST example for the original case. Broader authenticated-form protection and unchanged database state after rejected requests need separately scoped evidence; do not add that broader matrix as a new original-case requirement. |
| TC-SEC-07 | Authentication/account audit methods do not alone execute the original student-add/allocation/release/payment audit sequence. Link separate companion runs with their actual source and inspect actor/action/record/time. |

### HTTPS and ZAP decision record

**Development technical recommendation:** retain the submitted criteria and collect the missing evidence on an isolated real HTTPS test endpoint. Public hosting is unnecessary. There is no recorded team agreement or instructor-approved change supplied by Harsha's message. This technical review accepts an honest limitation in a NOT READY checkpoint; it does not waive the requirement.

| Obligation | Original outcome retained | Owner / next action | Actual change decision |
|---|---|---|---|
| TC-SEC-06: redirect, TLS 1.2+, actual authenticated Secure/HttpOnly session cookie | OWNER PASS (isolated local conditions) | Loopback HTTPS probe evidence is recorded; scope is limited to the synthetic local test instance and does not claim production/staging deployment. | Actual network conditions observed; independent QA acceptance pending. |
| Test Plan §5.1 ZAP baseline, explicit TC-SEC-08 | PARTIAL | Passive loopback baseline and two remaining observations are documented; QA must disposition them and decide whether defect records/retests are needed. | Scan executed; QA alert disposition pending. |

A baseline need not have zero alerts. The original final exit gate is zero open critical/high defects, requiring a complete reviewed severity inventory. If the instructor approves a criterion change, preserve the original outcome and add the exact changed criterion, actual authority/source/date/rationale and affected cases; do not relabel unexecuted tests PASS.

## Integrated HMS-17 evidence — 7 November 2026

PR #58 merged to `main` as `896b4f343e1e3f467155352820124f5931d12c3d`. Its tested PR head was `99e4ff2dd75968d879c1d96f9ed81c7ae161eaca`; the merged main tree equals that tested tree. Fresh GitHub Actions jobs on the exact tree passed on Python 3.11 and 3.14 with MySQL 8.4. The downloaded job logs each show **190 tests run, one expected timing skip, no failures**, and all verification gates passing. Those CI observations describe the recorded PR #58 tree; they do not prove the root cause of the older Windows-only failure. Exact current-main CI is independently reconciled below.

The manual HMS-17 run remains bound to application commit `c9f30a48c6dc54ccaec799156f3e52fe7bc8666a`, not the current submission tree. The owner record reports eight case IDs exercised. The reviewed evidence disposition is **6 OWNER PASS, TC-STU-01 NOT RUN** (no case-specific registration result or screenshot located), and **TC-QUAL-01 PARTIAL** (no timed first-use walkthrough by a new Warden using the one-page guide). Firefox and Edge page checks are recorded; they do not establish the full compatibility, platform, mobile or availability requirements. See the [HMS-17 evidence index](evidence/issue39/README.md), [manual record](evidence/issue39/manual-execution-20261107.md), and the [case register](Test_Case_Document.md#54-manual-browser-testing--hms-17).

HMS-18/#40 owner evidence for 13 cases is present under `docs/part3/evidence/issue40-final/`; recorded cases include the TC-ALC-05 browser PARTIAL, retained failed load attempt and passing unchanged-threshold rerun, and populated recovery result. The [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), explicitly authorized by Devansh, now accepts the original 13 cases for scoped #40 technical closure and records current priorities, late-entry and environment/tool dispositions. It does not supply historical entry compliance, actual named human approvals or full-plan acceptance. The [HMS-15 case document](Test_Case_Document.md) now supplies complete case records, 61 planned IDs and the preserved 36-requirement RTM; this documentation delivery does not approve historical entry criteria or final case acceptance. Section 6 distinguishes original-case metrics from the expanded design denominator and current method evidence. This paragraph's earlier assertion that the #41 Unit Test Report was missing and unit70 unproven is superseded by the current 13 November status at the top of this report and in the [Unit Test Report](Unit_Test_Report.md). HMS-20/#42 coverage-report publication remains complete.

## Consolidated case, requirement and defect metrics — historical snapshot through 10 November 2026

Counts are recalculated from all complete records and cross-checked against the index and original RTM. They preserve original and expanded denominators. The earlier consolidated review changed no case status. The separately dated #63 execution below changes only S2-08..16. The later [PR #66 review](evidence/issue39/followup-20261108.md) reconciles S1-07/S2-07 against historical raw CI; current totals include both updates.

| Recorded status / metric | Original 33 | Expanded 61 |
|---|---:|---:|
| OWNER PASS | 31 / 33 = 93.94% | 51 / 61 = 83.61% |
| PARTIAL | 1 / 33 = 3.03% | 3 / 61 = 4.92% |
| NOT RUN | 1 / 33 = 3.03% | 6 / 61 = 9.84% |
| BLOCKED | 0 / 33 = 0% | 1 / 61 = 1.64% |
| Latest recorded case FAIL / ERROR | 0 / 33 each | 0 / 61 each |
| Any exercise: OWNER PASS + PARTIAL | 32 / 33 = 96.97% | 54 / 61 = 88.52% |
| QA-accepted execution/pass percentage | UNVERIFIED | UNVERIFIED |

The historical 10 November snapshot's exercised numerator included partial work and was not the 100%-completed exit gate. Its current partial/blocked labels and counts are superseded by the 14 November current status at the top of this report. The original priorities remain proposals: 21 High/12 Medium; expanded priorities are 34 High/27 Medium. QA still needs to review the priority rationale and evidence before applying the High-priority exit criterion.

| Requirement metric | Result / meaning |
|---|---|
| Original core RTM design mapping | 36 / 36 = 100%; every original mapping pair is preserved. |
| Core rows with some mapped OWNER PASS | 36 / 36 = 100%; owner-observation proxy only. |
| Test Plan §14: requirements with at least one accepted passed case / 36 | UNVERIFIED; no complete case/requirement acceptance ledger is supplied. |
| Assessment of all conditions within each requirement | UNVERIFIED / incomplete; distinct from the literal passed-case mapping metric. |

For example, a negative-registration pass does not prove the unrecorded positive STU-01 journey; AUTH-04's mapped owner observation does not establish NFR-9's live cookie conditions; AUTH-03 does not establish NFR-12's TLS conditions. Keep SRS quality attributes, BR-1..6 and SO-1..4 in the separate assessment without silently changing the original 36-row denominator.

The review queries every public issue with pagination and selects all non-PR issues carrying the `bug` label. The four known labelled defects are closed. Technical module counts are reports **1**, allocations **2**, student self-service **1**; these are known defects/module, not a complete whole-project density or proof other modules have zero defects. No severity labels are present.

| Defect | Technical module | State | Age in days: actual closure minus creation |
|---|---|---|---:|
| [#45](https://github.com/Sreeharsha2240/hostel-management-system/issues/45) | reports | CLOSED | 1.002882 |
| [#46](https://github.com/Sreeharsha2240/hostel-management-system/issues/46) | allocations | CLOSED | 1.002870 |
| [#47](https://github.com/Sreeharsha2240/hostel-management-system/issues/47) | allocations | CLOSED | 1.002847 |
| [#48](https://github.com/Sreeharsha2240/hostel-management-system/issues/48) | student self-service | CLOSED | 1.019699 |

Actual creation/closure timestamps and the query's UTC acquisition time are retained in the [review extraction](evidence/issue38/independent-review-20261108.json). For an open defect, age would be acquisition time minus creation. Severity is UNKNOWN; zero open critical/high defects and whole-project inventory completeness remain UNVERIFIED. Retain PR #44/#49 and the [owner retest appendix](evidence/issue40-final/owner-cases.md), the failed volume attempt and the unreconciled historical harness failure separately.

## Independent evidence review and current build

Freshly downloaded [main run 42399172513](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42399172513) is bound to exact `b523d4c7abb77072bea48ac059be7f72396e8a79`. Each clean-checkout Python 3.11/3.14 MySQL bundle reconciles 190 exact mixed-level identities: 189 PASS and one expected timing SKIP, all 12 gates, plus a separate uninstrumented timing PASS. The recovery-safety step also succeeded; this review does not claim a new populated restore. JUnit and `run.json` input hashes and environments are retained in the review extraction. Two jobs are not 380 distinct methods.

The earlier [retained method extraction](evidence/issue37/ci-methods.json) remains bound to `70c9fe2` / run 42397043317. This new review neither relabels that earlier run nor retests historical browser/load/recovery observations. No application/test/configuration change or fresh local application, security scan, load or recovery execution is claimed by these documentation corrections.

## Current whole-plan exit criteria — 14 November 2026

Accordingly:

| Whole-plan criterion | Current status |
|---|---|
| 100% planned cases executed | Original 33 have 33 OWNER PASS observations. The expanded 61-case register still has 2 NOT RUN and 2 PARTIAL, so the expanded scope is NOT MET; independent QA acceptance of case conditions remains pending. |
| High-priority cases passed | UNVERIFIED: priorities were absent from the original plan and the current values are proposals; TC-SEC-08 is proposed High and remains PARTIAL. |
| Zero open critical/high defects | UNVERIFIED: no complete severity-ranked whole-project defect inventory is available. Four known defects were closed, but their severities are unknown. |
| Every RTM requirement backed by a passed case | Design mapping and OWNER PASS proxy are recorded for all 36 core rows; accepted requirement-by-requirement passed-case coverage remains UNVERIFIED. |
| Independent QA/Dev/PO approvals and project-guide walkthrough | PENDING final revision-bound decisions. A Warden walkthrough was owner-reported, but exact guide revision and participant code were not retained; team acceptance is not inferred. |

## Historical team action ledger — 8 November 2026

| Dependency | Responsible owner / exact next action | Current decision |
|---|---|---|
| Independent report/evidence technical review | Devansh's assisted review records the findings and corrections above; the new publication still needs teammate review. | Technical review performed; no final human approval inferred. |
| Cases, priorities, RTM and historical entry/tool deviations | Vaishnavi QA with case owners: record dated reviewed revision, scope, evidence acceptance and deviation disposition; a review now cannot retroactively establish earlier entry. | PENDING. |
| #41 Unit Test Report and unit70 | Historical 8 November action item; later completed in merged PR #74. | Superseded by the current disposition at the top of this report and in the [Unit Test Report](Unit_Test_Report.md). |
| Remaining security/browser/quality execution | Existing case owners execute or seek actual authorized disposition of each gap; keep original outcomes. | TC-SEC-06 is OWNER PASS for its isolated loopback conditions. TC-SEC-08 is PARTIAL pending QA alert disposition. Other browser, availability and portability evidence remains pending. |
| QA / Dev / PO final decisions | Vaishnavi / Devansh / Sreeharsha provide their own genuine dated decisions bound to the actual final revision. | PENDING; this assisted technical review is not a signature. |
| Guide acceptance and submission | Actual guide walkthrough; Sreeharsha coordinates instructor channel/cutoff/format, genuine videos, accepted package and actual receipt through #43. | PENDING; no submission receipt recorded. |

**Historical disposition:** 11 OWNER PASS / one PARTIAL remains the 5 November owner-reported snapshot. **Current case register:** TC-SEC-06 is OWNER PASS for the recorded isolated loopback test conditions: redirect, TLS 1.2/1.3, legacy-protocol rejection and live cookie flags. This is not a production-host claim. TC-SEC-08 is PARTIAL: the passive ZAP baseline completed, with the server-banner and low-confidence `next` hotspot awaiting QA disposition. See the [source-bound supplemental evidence](evidence/issue38-security-20261109/README.md). Keep #38/#43 OPEN and whole-plan **NOT READY**. No team/instructor change or final QA/Dev/PO approval is inferred. Fresh MySQL CI passed on PR #68 head `4985139` as recorded below; this verifies code but cannot substitute for remaining QA acceptance decisions.

## HMS-26 owner follow-up — 8 November 2026

[#63 execution evidence](evidence/issue63/README.md) records nine reviewed
Devansh-owned integration cases (S2-08..16), all PASS on clean
`6636098cb728aa17c2abf5e42c358a5d400261e7` (tree `0faea77304a30ceb436e1411a2c513dd1f3c6f44`).
Three independent automated reviewers checked the recipes/assertions and
candidate evidence before the committed execution. Per-step observations,
JUnit, commands, versions and source/raw hashes are published. The same clean
commit passed all 12 core gates, 190 mixed methods (189 PASS/one expected SKIP)
and separate timing PASS; seven owned-runner and 32 recovery-safety checks passed.
This is separate from the earlier exact-main and historical companion runs.

Only these nine current case statuses and derived counts change: expanded
48 OWNER PASS / 3 PARTIAL / 9 NOT RUN / 1 BLOCKED; 51/61 (83.61%) have some
exercise and 48/61 (78.69%) owner-pass observations. Original 33 and the 36 RTM
rows remain unchanged. All 27 exclusively Devansh-owned records have OWNER PASS
observations; shared QUAL-04 remains BLOCKED. This integration execution supplies
no unit-only coverage, new browser/load/recovery/TLS evidence, retrospective
entry approval, instructor extension or named human final approval. The
8 November date, MySQL 8.4 difference and test-only HTTP settings are explicit
limits. #38/#39/#41/#43 retain their actual remaining work; unit70 stays
**UNPROVEN** and whole-plan readiness **NOT READY**.

## HMS-17 follow-up reconciliation — 8 November 2026

The [PR #66 review](evidence/issue39/followup-20261108.md) retains original screenshot/run provenance, restores the two omitted raw files per historical CI bundle and reconciles S1-07/S2-07 against eleven passing methods per Python job. Product/test/template sources in the declared scope match historical `32e6f563`. The 8 and 9 November totals in this paragraph are historical snapshots only; see the 14 November current status at the top of this report for updated counts and the owner-approved #41 disposition. The 13 November phone-testing scope decision supersedes the physical-mobile requirement reference in this historical evidence. Whole-plan readiness remains NOT READY.

## Current-main supplemental full-suite verification — 9 November 2026

A fresh Windows local run at main commit `7556822df38b23d4f302cf68d857bb35b963ff10` (tree `781dd5195e1b6da718fe602ae67cdb04f495acd4`) added seven focused HMS-16 gap tests and a small evidence runner in a dirty candidate tree. The full `scripts/run_checks.py` completed all gates successfully: 207 methods, 206 passed, zero failures/errors, one expected timing skip, and **88.25% combined project coverage** (1,590/1,772 statements; 348/424 branch outcomes). The configured 70% project gate passes. The earlier 53.14% number was the `students hostels` partial-suite diagnostic and must not be presented as the full-suite result. See the [sanitized execution record](evidence/issue38-execution-20261109/README.md) and its JSON.

This mixed project-wide measure does not establish the formal SRS unit-only 70%; #41 must classify unit vs integration/system tests and publish its denominator and result. At this 9 November coverage snapshot, the isolated MySQL file issue blocked a local TLS rerun and ZAP had not yet been run; the later same-day transport/ZAP addendum below supersedes those statements. This update does not change original case dispositions or close #38.

## Local transport and ZAP follow-up — 9 November 2026

This follow-up supersedes the preceding transport/ZAP limitation for the isolated local probe only. It does not replace deployed-candidate evidence or change the independent QA/Dev/PO acceptance requirement.

On a disposable SQLite database containing synthetic data, a short-lived self-signed HTTPS endpoint bound only to `127.0.0.1` was exercised on the HMS-16 source tree. The network probe passed HTTP-to-HTTPS redirection (301), TLS 1.2 and 1.3 handshakes, rejection of TLS 1.0 and 1.1, authenticated login and dashboard access, and Secure/HttpOnly session-cookie plus Secure/HttpOnly CSRF-cookie attributes. Cookie values and credentials were not retained. The CA was trusted only by the local probe client; this is real loopback transport evidence, not public-domain or deployment certification.

OWASP ZAP 2.17.0 completed an Automation Framework passive baseline against that same localhost app. The spider found 10 URLs; no active scan was run. The initial baseline identified a missing CSP and a CSRF cookie without HttpOnly. A same-origin restrictive CSP was added, the existing confirmation prompts were moved to an external script so inline script execution could remain disabled, and `CSRF_COOKIE_HTTPONLY` was enabled. The rescan no longer reported either finding.

The rescan exited 0 and reported two remaining observations: one Low-confidence server-version-header alert (four responses) containing `WSGIServer/0.2 CPython/3.14.0`, which identifies the temporary Python WSGI probe server and does not establish what any deployment server exposes; and one Informational, Low-confidence potential-XSS hotspot (two request instances) associated with `next=/dashboard/`. The `next` parameter is not used or rendered by the login view. A regression test sends an HTML-injection marker in that parameter and verifies it is not reflected. The ZAP rule itself describes these as hotspots requiring analyst review. Preserve them for QA disposition rather than claiming the alert count is zero or closing them as accepted false positives.

The focused security and changed confirmation-form tests passed 12/12 on SQLite, as did Django system/migration checks, Ruff lint/format, dependency validation, and JavaScript syntax validation. A forced full SQLite run is not a valid substitute for the configured MySQL suite: MySQL-only information-schema/SQL-mode assertions and concurrent row-lock tests require MySQL. The repository runner also stops at its MySQL `SELECT VERSION()` probe under SQLite. **Superseding verification:** fresh MySQL CI on PR #68 head `49851396796918103681aacf47394e5010426201` passed on Python 3.11 and 3.14 in [run 42566973066](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42566973066). Each job ran 209 tests (208 passed and one expected skip), passed all 12 repository verification gates, and the full coverage report was 88% (1,780 statements; the 70% configured gate passed). Nine owned expanded regression cases passed. The remaining gap is human QA disposition/acceptance, not a pending full-suite CI run. Exact sanitized transport and ZAP details are in [issue38-security-20261109](evidence/issue38-security-20261109/README.md).

**Current technical disposition:** TC-SEC-06 is OWNER PASS for the specified loopback test conditions; no production/staging TLS claim is made. TC-SEC-08's passive baseline ran and is PARTIAL pending QA disposition of the above alerts. The case register and expanded totals in this report and the HMS case document are reconciled to these statuses. These scoped results do not constitute an approved test-plan deviation, a full #38 acceptance, or a completion of #43.
