# System Validation Report — HMS Part 3

**Historical HMS-16 owner-reported outcomes: 11 OWNER PASS, 1 PARTIAL. Whole-plan readiness: NOT READY.** The historical focused run tested the 5 November `main` revision `8322b4c20c067d512c4bb439fdedd19d4fa27223` using synthetic data and a disposable local MySQL 8.0.46 instance. It does not claim a deployed HTTPS endpoint, complete whole-plan acceptance, or team approvals.

**Independent technical review:** 8 November 2026, at merged main `b523d4c7abb77072bea48ac059be7f72396e8a79` (tree `56f7fb4307bc2ce4f3595aebfd5915ce301c3fb7`). This review was performed under Devansh's instruction with three fresh automated reviewers. It reviews existing evidence and supplies corrections; it is not a human QA/Dev/PO signature, a criterion change, a new owner execution or selection of the final submission revision. The [sanitized review extraction](evidence/issue38/independent-review-20261108.json) retains source hashes, arithmetic, actual issue dates and exact-main CI input hashes.

## HMS-16 execution environment and results

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

TC-SEC-06 remains PARTIAL until actual HTTP-to-HTTPS redirection, TLS protocol validation and authenticated Secure/HttpOnly session-cookie inspection are recorded. The submitted Test Plan explicitly requires these checks and separately requires an OWASP ZAP baseline (TC-SEC-08 in the updated register). A real isolated HTTPS test endpoint is sufficient; public hosting is unnecessary. Test-client flags and deployment-settings checks do not prove a network TLS handshake. Any actual instructor-approved change to the original criteria must be recorded separately with its authority, date and rationale, preserving the unmet original outcome.

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
| TC-SEC-06: redirect, TLS 1.2+, actual authenticated Secure/HttpOnly session cookie | PARTIAL | Sreeharsha #38: record endpoint/proxy configuration, tested revision, actual network output, versions/date/commands and cookie attributes with values removed. | PENDING; none approved in this review. |
| Test Plan §5.1 ZAP baseline, explicit TC-SEC-08 | NOT RUN | Sreeharsha #38: run against the agreed running synthetic application, preserve sanitized findings/coverage/exit status, triage alerts and link actual defects/retests. | PENDING; none approved in this review. |

A baseline need not have zero alerts. The original final exit gate is zero open critical/high defects, requiring a complete reviewed severity inventory. If the instructor approves a criterion change, preserve the original outcome and add the exact changed criterion, actual authority/source/date/rationale and affected cases; do not relabel unexecuted tests PASS.

## Integrated HMS-17 evidence — 7 November 2026

PR #58 merged to `main` as `896b4f343e1e3f467155352820124f5931d12c3d`. Its tested PR head was `99e4ff2dd75968d879c1d96f9ed81c7ae161eaca`; the merged main tree equals that tested tree. Fresh GitHub Actions jobs on the exact tree passed on Python 3.11 and 3.14 with MySQL 8.4. The downloaded job logs each show **190 tests run, one expected timing skip, no failures**, and all verification gates passing. Those CI observations describe the recorded PR #58 tree; they do not prove the root cause of the older Windows-only failure. Exact current-main CI is independently reconciled below.

The manual HMS-17 run remains bound to application commit `c9f30a48c6dc54ccaec799156f3e52fe7bc8666a`, not the current submission tree. The owner record reports eight case IDs exercised. The reviewed evidence disposition is **6 OWNER PASS, TC-STU-01 NOT RUN** (no case-specific registration result or screenshot located), and **TC-QUAL-01 PARTIAL** (no timed first-use walkthrough by a new Warden using the one-page guide). Firefox and Edge page checks are recorded; they do not establish the full compatibility, platform, mobile or availability requirements. See the [HMS-17 evidence index](evidence/issue39/README.md), [manual record](evidence/issue39/manual-execution-20261107.md), and the [case register](Test_Case_Document.md#54-manual-browser-testing--hms-17).

HMS-18/#40 owner evidence for 13 cases is present under `docs/part3/evidence/issue40-final/`; recorded cases include the TC-ALC-05 browser PARTIAL, retained failed load attempt and passing unchanged-threshold rerun, and populated recovery result. QA still needs to disposition the reviewed-case/entry criteria, priorities and environment/tool deviations. The [HMS-15 case document](Test_Case_Document.md) now supplies complete case records, 61 planned IDs and the preserved 36-requirement RTM; this documentation delivery does not approve historical entry criteria or final case acceptance. Section 6 distinguishes original-case metrics from the expanded design denominator and current method evidence. HMS-19/#41's Unit Test Report is not present. HMS-20/#42 coverage reports are published and the issue is closed as a reporting task, while formal SRS unit70 remains UNPROVEN.

## Consolidated case, requirement and defect metrics — 8 November 2026

Counts are recalculated from all complete records and cross-checked against the index and original RTM. They preserve original and expanded denominators. No case status, proposed priority or owner execution is changed by this review.

| Recorded status / metric | Original 33 | Expanded 61 |
|---|---:|---:|
| OWNER PASS | 30 / 33 = 90.91% | 39 / 61 = 63.93% |
| PARTIAL | 2 / 33 = 6.06% | 3 / 61 = 4.92% |
| NOT RUN | 1 / 33 = 3.03% | 18 / 61 = 29.51% |
| BLOCKED | 0 / 33 = 0% | 1 / 61 = 1.64% |
| Latest recorded case FAIL / ERROR | 0 / 33 each | 0 / 61 each |
| Any exercise: OWNER PASS + PARTIAL | 32 / 33 = 96.97% | 42 / 61 = 68.85% |
| QA-accepted execution/pass percentage | UNVERIFIED | UNVERIFIED |

The exercised numerator includes partial work and is not the 100%-completed exit gate. Zero latest case FAIL/ERROR does not erase the historical failed load/harness attempts or establish accepted passes. Partial cases are TC-SEC-06, TC-QUAL-01 and TC-REG-S1-05; TC-QUAL-04 is BLOCKED. The 18 NOT RUN records include STU-01, the 14 separately specified new regressions, SEC-08 and QUAL-02/03. Passing automated companions do not silently execute those separate records. Original priorities remain proposals: 21 High/12 Medium; expanded priorities are 34 High/27 Medium. QA must review the priority rationale and actual evidence; no High-priority gate is approved here.

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

## Integrated report and exit criteria

Accordingly:

| Whole-plan criterion | Current status |
|---|---|
| 100% planned cases executed | NOT MET: original 33 retain 30 OWNER PASS / 2 PARTIAL / 1 NOT RUN; expanded 61 retain 39 OWNER PASS / 3 PARTIAL / 18 NOT RUN / 1 BLOCKED. Original subcondition/entry acceptance remains pending. |
| High-priority cases passed | UNVERIFIED until QA assigns/reviews priorities; the original plan has no priority values. |
| Zero open critical/high defects | UNVERIFIED: no complete severity-ranked whole-project defect inventory is available; one local verification-harness failure is recorded above. |
| Every RTM requirement backed by a passed case | UNVERIFIED: the 36 rows and closed #37 document delivery are present, but accepted case/requirement evidence remains pending. Design mapping and owner-pass proxies are insufficient. |
| Independent QA/Dev/PO approvals and project-guide walkthrough | PENDING; no approval is inferred. |

## Team actions and actual approvals

| Dependency | Responsible owner / exact next action | Current decision |
|---|---|---|
| Independent report/evidence technical review | Devansh's assisted review records the findings and corrections above; the new publication still needs teammate review. | Technical review performed; no final human approval inferred. |
| Cases, priorities, RTM and historical entry/tool deviations | Vaishnavi QA with case owners: record dated reviewed revision, scope, evidence acceptance and deviation disposition; a review now cannot retroactively establish earlier entry. | PENDING. |
| #41 Unit Test Report and unit70 | Vaishnavi publishes; module owners supply their existing results. Devansh's [module-owner handoff](Code_Coverage_Report.md#hms-19-module-owner-input--8-november-2026) supplies classifications, IDs and limitations. | Report missing; unit70 UNPROVEN. |
| Remaining security/browser/quality execution | Existing case owners execute or seek actual authorized disposition of each gap; keep original outcomes. | PENDING, including real elapsed-time browser/security and availability/portability evidence. |
| QA / Dev / PO final decisions | Vaishnavi / Devansh / Sreeharsha provide their own genuine dated decisions bound to the actual final revision. | PENDING; this assisted technical review is not a signature. |
| Guide acceptance and submission | Actual guide walkthrough; Sreeharsha coordinates instructor channel/cutoff/format, genuine videos, accepted package and actual receipt through #43. | PENDING; no submission receipt recorded. |

**Disposition:** historical HMS-16 observations remain 11 OWNER PASS / one PARTIAL with the original-subcondition limits above. TC-SEC-06 remains PARTIAL because actual redirect, TLS and live authenticated session-cookie evidence is unrecorded. The separately required ZAP baseline, TC-SEC-08, remains NOT RUN. Keep #38/#43 OPEN and whole-plan **NOT READY**. The technical recommendation is to obtain the required isolated HTTPS/ZAP evidence, not waive it; no team/instructor change or final QA/Dev/PO approval is invented. The 47 focused methods did not report an application security failure, but their pass summary does not establish all original conditions or complete security acceptance.
