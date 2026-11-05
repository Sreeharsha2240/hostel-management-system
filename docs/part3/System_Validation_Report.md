# System Validation Report — HMS-16

**HMS-16 owner-case execution: 11 PASS, 1 PARTIAL. Whole-plan readiness: NOT READY.** This update records testing on current `main` (`8322b4c20c067d512c4bb439fdedd19d4fa27223`) using synthetic data and a disposable local MySQL 8.0.46 instance. It applies the mini-project scope set by the project owner. It does not claim a deployed HTTPS endpoint, complete whole-plan acceptance, or team approvals.

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

A separate full-runner attempt on the same source discovered **190 tests: 189 passed, 1 skipped, 1 failed**. The skip is the expected wall-clock timing test under coverage. The single failure was `tests.test_checks.VerificationRunnerTests.test_xml_keeps_same_named_package_files_and_only_selected_context_hits`: this Windows run generated Cobertura XML with 0 covered lines instead of 4 while the test fixture was under the restricted AppContainer temporary path. The root cause is not confirmed. This is a verification-harness/environment discrepancy, not an HMS authentication or security-flow failure. The same `python scripts/run_checks.py --output-dir test-results/ci` command completed in GitHub Actions run [42010910487](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42010910487) on Ubuntu 24.04 with Python 3.11 and 3.14: **190 tests, 189 passed, 1 expected timing skip, 0 failures and 0 errors** in each matrix job. The local failure is therefore not reproduced in clean CI; retain it as a Windows-specific unresolved discrepancy, but do not treat the current CI run as failing. The local run measured 93.22% branch-aware coverage; that value is informational because that local run failed. Its initial `migrate --check` also ran before the new local application database had been migrated; the check passed after migrations were applied.

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

TC-SEC-06 is partial because the mini-project runs locally and has no deployed HTTPS host. I did not label a test-client HTTPS request as evidence of a real TLS handshake. The project owner has scoped this as a mini-project rather than a deployment-level website; this is a scope preference, not instructor approval or test evidence. **Owner and next action:** Sreeharsha must check the submission rubric and obtain instructor/team disposition of the scope deviation. If real transport validation is required, the team must provide an approved HTTPS test host and access for the sanitized ZAP baseline; until then, retain PARTIAL.

## Integrated report and exit criteria

HMS-18/#40 evidence is present on `main` in `docs/part3/evidence/issue40-final/` and is published by merged PR #50. QA's independent evidence/entry-criteria review and the reviewed-case disposition assigned to HMS-15/#37 remain pending. HMS-17/#39 remains open and its owner evidence is not present in this report; Vaishnavi must provide that evidence or explicitly record blocked cases and next actions. Accordingly:

| Whole-plan criterion | Current status |
|---|---|
| All original cases executed | NOT MET: HMS-16 has 11 PASS / 1 PARTIAL; HMS-17 evidence is outstanding; the other owner register entries must be reconciled. |
| High-priority cases passed | UNVERIFIED until QA assigns/reviews priorities; the original plan has no priority values. |
| Zero open critical/high defects | UNVERIFIED: no complete severity-ranked whole-project defect inventory is available. The local verification-harness failure was not reproduced by the passing 3.11/3.14 CI run above. |
| RTM requirements covered by passed cases | PARTIAL; this report supplies current HMS-16 evidence, while team-wide statuses remain outstanding. |
| Independent QA/Dev/PO approvals and project-guide walkthrough | PENDING; no approval is inferred. |

**Disposition:** HMS-16 owner testing is substantially complete for the mini-project scope. The CI suite passes on Python 3.11 and 3.14; the prior Windows-only verification-harness failure remains documented but is not reproduced in CI. Keep issue #38 open until the TC-SEC-06 scope is formally dispositioned, HMS-17 evidence is incorporated, whole-plan case/RTM exit criteria are evaluated, and actual QA/Dev/PO reviews and the project-guide walkthrough are recorded. No application authentication/security defect was exposed by the 47 focused tests; no application-code change was indicated.
