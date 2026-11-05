# System Validation Report — HMS-16

**Readiness: NOT READY against the submitted Test Plan.** This report records the available Sreeharsha authentication/security evidence and current team handoffs as of 5 November 2026. It does not claim that the 12 assigned system cases have passed on an accepted final build, that deployment security checks are complete, or that whole-project approval has been granted.

## Current source and team handoffs

- HMS-15 Test Case Document and RTM are merged through PR #51, merge commit d981c1b. It preserves 33 original case IDs, adds 10 Sprint 1/2 regression cases, and maps 24 functional plus 12 non-functional requirements. The 12 assigned HMS-16 case rows (TC-AUTH-01..04, TC-USR-01, TC-SEC-01..07) remain NOT RUN in that document. Its original Test Plan does not establish per-case priority values; QA still needs to record its entry review.
- HMS-18 owner evidence is merged through PR #50, merge commit 8d60e83. It supplies current-source execution evidence and the 13-case owner appendix. Its limitations remain: QA review and whole-plan acceptance are pending; the browser transfer fault-injection step is partial with companion regression evidence; load evidence is local-host specific; prior failed load results remain failed.
- HMS-17 (#39) is still open. Its owner evidence is not integrated here.
- The application source referenced by HMS-18 is 0e358b4ce1fd02366184c7cb9c312b47dd093214. The local audit checkout used for prior HMS-16 automated testing is branch codex/hms-e2e-audit, commit 7f8cd0281b383342843e1018aea27fbf6cbf6040, with pre-existing modified and untracked files. It is not a clean checkout of current main; its results are supporting historical evidence only.

## HMS-16 automated evidence available

The retained local run .tmp/hms16-security-tests.log records:

| Field | Result |
|---|---|
| Command | python manage.py test accounts audit students.test_self_service --noinput -v 1 --settings=test_settings_sqlite |
| Result | 45 passed, 0 failures, 0 errors; 31.269 seconds |
| Database | Isolated in-memory SQLite; synthetic fixtures |
| Source | Local dirty snapshot 7f8cd0281b383342843e1018aea27fbf6cbf6040 |

This provides supporting automated coverage for login and generic failure behavior, five-attempt lockout, role gates and account administration, session expiry/logout, cookie flags when enabled by settings, student self-record isolation, audit attribution/secret minimization, audit immutability/retention and audit rollback. It is not a per-case system execution record and does not establish a pass for any of the 12 case IDs on current main.

A separate MySQL attempt is retained in .tmp/hms16-security-mysql-tests.log; it stopped before test execution because the configured account could not create test_hms_audit (MySQL error 1044). The local test app/database were not listening when checked during this update. No fresh MySQL-backed HMS-16 suite was run.

The earlier interim report records manage.py check --deploy as passing under temporary production-style settings. That is a settings check only, not deployed-host verification. No current staging URL or test window was supplied. No live TLS 1.2+, HTTPS redirect, secure-cookie exchange, or OWASP ZAP baseline result is available. No ZAP report was found in the retained local evidence.

## Assigned cases and current disposition

The merged HMS-15 document contains the authoritative case names and expected results. Until cases are run and evidenced on the accepted build, retain their case-level status as NOT RUN; matching automated methods below are supporting evidence only.

| Case | Supporting automated evidence in the local run | Case-level status / remaining work |
|---|---|---|
| TC-AUTH-01 — valid login | accounts.tests.test_login_shows_role_dashboard_and_logout_clears_session; role dashboard test | NOT RUN on accepted build; verify real login and role redirect. |
| TC-AUTH-02 — invalid login | Generic invalid-password and locked-account tests | NOT RUN on accepted build; record generic response for invalid credentials. |
| TC-AUTH-03 — five failures / 15-minute lockout | Lockout tests exercise five failures and active lockout | NOT RUN on accepted build; record lock and expiry/recovery behavior against case steps. |
| TC-AUTH-04 — logout / session timeout | Logout clears session; expired session requires login; rolling expiry/cookie test | NOT RUN on accepted build; include protected-page and browser-back behavior. |
| TC-USR-01 — user administration | Admin create/update/deactivate and non-admin denial tests | NOT RUN on accepted build; execute authorized and unauthorized account operations. |
| TC-SEC-01 — role access control | Role dashboard, non-admin account and audit endpoint access tests | NOT RUN on accepted build; exercise direct requests for each role. |
| TC-SEC-02 — student record isolation | Self-service test checks the authenticated student's allocation/payment view | NOT RUN on accepted build; attempt direct access to another student's records and capture denial. |
| TC-SEC-03 — SQL/script injection | Related escaping/literal-search test exists in students/tests.py, outside the prior focused command | NOT RUN; run reviewed inputs and record safe rendering/no unauthorized results. |
| TC-SEC-04 — password storage/policy | Account creation verifies check_password; password policy tests | NOT RUN on accepted build; record encoded storage and policy rejection. |
| TC-SEC-05 — CSRF | Existing CSRF regression tests are supporting evidence only | NOT RUN on accepted build; submit an invalid-token write request and capture rejection. |
| TC-SEC-06 — HTTPS/session cookies | Automated tests assert flags when secure settings are enabled | BLOCKED for deployed acceptance; no agreed HTTPS host to verify redirect, TLS and actual cookies. |
| TC-SEC-07 — administrative audit | Actor attribution, immutable events, retention and rollback tests | NOT RUN on accepted build; perform and inspect the reviewed admin operations. |

No defects were indicated by the 45-test SQLite run. It is not a complete severity-ranked defect inventory, so the zero open critical/high defects criterion remains unverified.

## Test Plan exit criteria

| Original exit criterion | Current outcome |
|---|---|
| 100% of planned cases executed | NOT MET / unverified. HMS-15 still lists the 12 assigned cases as NOT RUN; team-wide statuses must be reconciled. |
| All high-priority cases passed | UNVERIFIED. The original plan and current case document do not establish per-case priority values. QA must confirm priority mapping. |
| Zero open critical/high defects | UNVERIFIED. No complete severity-ranked defect inventory was provided. |
| Every RTM requirement covered by at least one passed case | UNVERIFIED. The RTM is merged, but statuses and evidence are incomplete for all cases. |
| Independent QA/Dev/PO approvals and project-guide walkthrough | PENDING; no approval or walkthrough is inferred. |

## Blockers and next actions

1. Use the merged HMS-15 register to execute all 12 HMS-16 cases individually on the accepted current application build; capture expected/actual result, environment, exact source SHA and sanitized evidence for each.
2. Obtain the agreed reachable test deployment, account/access and test window. Then run the sanitized ZAP baseline and verify TLS 1.2+, HTTPS redirection and actual Secure/HttpOnly cookie attributes. Keep credentials and raw scans out of Git.
3. Obtain current MySQL test permission or an approved disposable database, then rerun the focused security suite on the accepted build. The earlier local MySQL attempt failed before tests because CREATE DATABASE was denied.
4. Integrate HMS-17 evidence after its owner submits it; retain the merged HMS-18 evidence and its stated limitations.
5. Reconcile severity-ranked defects, all original exit criteria, independent approvals and the required project-guide walkthrough. Preserve NOT READY until each original criterion is met or an instructor-approved change is separately recorded.
