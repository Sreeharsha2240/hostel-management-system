# System Validation Report — HMS-16

**HMS-16 owner-case execution: 11 PASS, 1 PARTIAL. Whole-plan readiness: NOT READY.** The historical focused run tested the 5 November `main` revision `8322b4c20c067d512c4bb439fdedd19d4fa27223` using synthetic data and a disposable local MySQL 8.0.46 instance. It does not claim a deployed HTTPS endpoint, complete whole-plan acceptance, or team approvals.

## HMS-16 execution environment and results

| Field | Result |
|---|---|
| Tested source | `8322b4c20c067d512c4bb439fdedd19d4fa27223` (`main`, fetched 5 November 2026) |
| Environment | Windows 11; Python 3.14.0; Django 5.2.19; mysqlclient 2.3.0; MySQL 8.0.46 |
| Database | New disposable local MySQL instance on loopback; Django test database created and destroyed by the test runner; synthetic fixtures only |
| Focused command | `python manage.py test accounts.tests accounts.test_security audit.tests students.test_self_service students.tests.StudentManagementViewTests.test_student_list_escapes_script_payload_and_search_treats_sql_as_literal --noinput -v 1` |
| Focused result | **47 passed, 0 failures, 0 errors; 104.605 seconds** |
| Deployment-settings check | `python manage.py check --deploy --database default`: passed with secure-cookie, HTTPS-redirect and HSTS settings enabled; no warnings |
| Migration checks | `python manage.py migrate --check` and `python manage.py makemigrations --check --dry-run`: passed after applying migrations to the disposable base database |

The focused suite exercises login and role redirects, generic invalid-credential responses, five-failure lockout and expired-lock recovery, session timeout/logout, administrator account create/update/deactivate and non-admin denial, student self-record isolation, password hashing/policy, CSRF rejection, injection handling and audit actor/integrity behavior.

A separate full-runner attempt on the same source reported the verification-harness test `tests.test_checks.VerificationRunnerTests.test_xml_keeps_same_named_package_files_and_only_selected_context_hits` failed: on this Windows run, generated Cobertura XML reported 0 covered lines instead of 4 while the test fixture was under the restricted AppContainer temporary path. The root cause is not confirmed. The old report's count line listed 190 discovered tests, 189 passed, one skipped and one failed; those outcome counts sum to 191, and the raw JUnit report is not retained in the published HMS-16 evidence. Treat the Windows outcome as a recorded historical harness failure, not a reconciled 190-test total. A fresh current-source CI run is recorded below. The old run's 93.22% branch-aware figure is informational because that run failed. Its initial `migrate --check` also ran before the new local application database had been migrated; the check passed after migrations were applied.

## HMS-16 case outcomes

The test-case register statuses below reflect the focused MySQL execution. Method names are from the current-source automated suite; the full command and environment are recorded above.

| Case | Result and evidence | Status |
|---|---|---|
| TC-AUTH-01 — valid login | `AuthenticationTests.test_login_shows_role_dashboard_and_logout_clears_session`; `test_each_role_can_access_dashboard_and_dashboard_reflects_role` | PASS |
| TC-AUTH-02 — invalid login | `AuthenticationTests.test_invalid_password_is_generic_and_locks_after_five_attempts`; locked-account generic-response check | PASS |
| TC-AUTH-03 — five failures / lockout | Five failed attempts activate the lock; expired-lock recovery and reset are exercised. The application policy is 15 minutes. | PASS |
| TC-AUTH-04 — logout / timeout | `AuthenticationTests.test_expired_session_requires_login`; `SessionAndLockoutTests.test_server_session_expiry_logout_and_cache_control` | PASS |
| TC-USR-01 — user administration | Admin create/update/deactivate and Warden/Student denial tests; password is stored as a hash and weak passwords are rejected | PASS |
| TC-SEC-01 — role access | Role dashboards, account-management denial and audit endpoint role checks | PASS |
| TC-SEC-02 — student data isolation | `StudentSelfServiceTests.test_student_sees_only_own_allocation_and_payment_details` | PASS |
| TC-SEC-03 — injection handling | `StudentManagementViewTests.test_student_list_escapes_script_payload_and_search_treats_sql_as_literal` | PASS |
| TC-SEC-04 — password storage/policy | Account creation verifies `check_password`; weak and similar passwords are rejected | PASS |
| TC-SEC-05 — CSRF | `SessionAndLockoutTests.test_login_post_is_protected_by_csrf` rejects a tokenless POST with HTTP 403 | PASS |
| TC-SEC-06 — HTTPS/cookies | Secure/HttpOnly session and CSRF cookie flags pass in the Django test client; production-style `check --deploy` passes. No real TLS endpoint or HTTP-to-HTTPS exchange was tested. | PARTIAL |
| TC-SEC-07 — administrative audit | Admin actor attribution, create/update/deactivate events, secret minimization and immutable audit-event tests | PASS |

TC-SEC-06 remains PARTIAL until actual HTTP-to-HTTPS redirection, TLS protocol validation and authenticated Secure/HttpOnly session-cookie inspection are recorded. The submitted Test Plan explicitly requires these checks and separately requires an OWASP ZAP baseline (TC-SEC-08 in the updated register). A real isolated HTTPS test endpoint is sufficient; public hosting is unnecessary. Test-client flags and deployment-settings checks do not prove a network TLS handshake. Any authorized change to the original criteria must be recorded separately, preserving the unmet original outcome.

## Integrated HMS-17 evidence — 7 November 2026

PR #58 merged to `main` as `896b4f343e1e3f467155352820124f5931d12c3d`. Its tested PR head was `99e4ff2dd75968d879c1d96f9ed81c7ae161eaca`; the merged main tree equals that tested tree. Fresh GitHub Actions jobs on the exact tree passed on Python 3.11 and 3.14 with MySQL 8.4. The downloaded job logs each show **190 tests run, one expected timing skip, no failures**, and all verification gates passing. These current CI results supersede the old local Windows harness failure as a statement about the current tree; they do not prove the root cause of that Windows-only failure.

The manual HMS-17 run remains bound to application commit `c9f30a48c6dc54ccaec799156f3e52fe7bc8666a`, not the current submission tree. The owner record reports eight case IDs exercised. The reviewed evidence disposition is **6 OWNER PASS, TC-STU-01 NOT RUN** (no case-specific registration result or screenshot located), and **TC-QUAL-01 PARTIAL** (no timed first-use walkthrough by a new Warden using the one-page guide). Firefox and Edge page checks are recorded; they do not establish the full compatibility, platform, mobile or availability requirements. See the [HMS-17 evidence index](evidence/issue39/README.md), [manual record](evidence/issue39/manual-execution-20261107.md), and the [case register](Test_Case_Document.md#54-manual-browser-testing--hms-17).

HMS-18/#40 owner evidence for 13 cases is present under `docs/part3/evidence/issue40-final/`; recorded cases include the TC-ALC-05 browser PARTIAL, retained failed load attempt and passing unchanged-threshold rerun, and populated recovery result. QA still needs to disposition the reviewed-case/entry criteria, priorities and environment/tool deviations. The [HMS-15 case document](Test_Case_Document.md) now supplies complete case records, 61 planned IDs and the preserved 36-requirement RTM; this documentation delivery does not approve historical entry criteria or final case acceptance. Section 6 distinguishes original-case metrics from the expanded design denominator and current method evidence. HMS-19/#41's Unit Test Report is not present. HMS-20/#42 coverage reports are published and the issue is closed as a reporting task, while formal SRS unit70 remains UNPROVEN.

## Integrated report and exit criteria

Accordingly:

| Whole-plan criterion | Current status |
|---|---|
| All original cases executed | NOT MET: HMS-16 has 11 PASS / 1 PARTIAL; HMS-17 has one NOT RUN and one PARTIAL; HMS-18 QA disposition and remaining owners' cases are not fully accepted. |
| High-priority cases passed | UNVERIFIED until QA assigns/reviews priorities; the original plan has no priority values. |
| Zero open critical/high defects | UNVERIFIED: no complete severity-ranked whole-project defect inventory is available; one local verification-harness failure is recorded above. |
| RTM requirements covered by passed cases | PARTIAL; HMS-16 evidence is reported above, but HMS-15's shared-register review and complete team RTM acceptance remain outstanding. |
| Independent QA/Dev/PO approvals and project-guide walkthrough | PENDING; no approval is inferred. |

**Disposition:** HMS-16's 12 owner cases have 11 PASS and one PARTIAL for the mini-project evidence collected. The 47 focused MySQL-backed checks passed; fresh full-source CI on the merged tree also passed. TC-SEC-06 remains PARTIAL because no live TLS endpoint or ZAP baseline was available. The System Validation Report is now integrated with the published HMS-17 owner evidence and HMS-18 handoff, but the whole plan is **NOT READY**. Keep issue #38 open until the TC-SEC-06 scope is resolved with the team/instructor, security evidence receives independent review, the incomplete Test Plan criteria are honestly dispositioned, and actual QA/Dev/PO approvals are recorded. No application authentication/security defect was exposed by the 47 focused tests; no application-code change was indicated by that evidence.
