# HMS-16 Local TLS and ZAP Evidence — 9 November 2026

## Scope and setup

- Source base: `9286dbaef9ca0d237d12ea677a91f7aceda25209`; the follow-up code and tests in the same PR addendum were exercised before publication.
- Environment: Windows 11, Python 3.14.0, Django 5.2.19, ZAP 2.17.0, Java 25.0.2.
- Target: disposable HMS instance bound to loopback only (`127.0.0.1`), synthetic SQLite data, one synthetic administrator, short-lived self-signed certificate. No production database, public host, or teammate account was used.
- ZAP scope: one localhost site, 10 spidered URLs. Passive scan only; **no active scan or attack rules were run**. Raw ZAP output, certificate, local credentials, and test DB remain in ignored `.tmp/` and are not published.

## Network transport results

| Check | Result |
|---|---|
| HTTP `/login/` redirects to HTTPS | PASS — 301 to the same localhost app |
| TLS 1.2 handshake | PASS |
| TLS 1.3 handshake | PASS |
| TLS 1.0 and TLS 1.1 | PASS — both rejected |
| Authenticated HTTPS login reaches dashboard | PASS |
| `sessionid` attributes | Secure and HttpOnly |
| `csrftoken` attributes | Secure and HttpOnly |

These are actual loopback network exchanges with the application. The client explicitly trusted the short-lived local certificate. This evidence does not certify a public hostname, deployment TLS configuration, or production certificate chain.

## ZAP result and triage

ZAP 2.17.0's Automation Framework passive baseline completed successfully (exit code 0) on 9 November 2026. The first baseline found a missing Content-Security-Policy header and a CSRF cookie without HttpOnly. Both were addressed: HMS now sends a restrictive same-origin CSP with inline scripts disabled, uses an external script for the existing confirmation prompts, and sets the CSRF cookie HttpOnly. Neither finding appeared on the final rescan.

Final rescan: **0 High, 0 Medium, 1 Low, 1 Informational alert** (six instances total):

| Alert | Risk / confidence | Triage |
|---|---|---|
| Server Leaks Version Information via `Server` header | Low / High; four responses | The value is the temporary Python 3.14 `wsgiref` probe server banner. This is a probe-server fingerprint, not evidence about an eventual hosting server. Keep visible for QA disposition; no app-level fix or deployment claim is made. |
| User Controllable HTML Element Attribute (Potential XSS) | Informational / Low; two instances | ZAP describes this rule as a hotspot for analyst review. It points to `next=/dashboard/`. The login view does not consume or render `next`; a regression test submits an HTML-injection marker and confirms it is not reflected. Keep the low-confidence hotspot for QA disposition; do not report it as a confirmed vulnerability or as an accepted false positive. |

The complete sanitized alert counts and scope are in [transport-zap-summary.json](transport-zap-summary.json). The raw report is intentionally not included because it is unnecessary for the audit trail and contains scanner-generated request details.

## Code and local verification

Changes in this follow-up:

- Added the CSP middleware and enabled the CSRF cookie's HttpOnly flag.
- Replaced inline confirmation handlers with `data-confirm` attributes and `static/hms/app.js`, preserving the confirmation prompts while allowing a strict `script-src 'self'` policy.
- Added regression tests for the CSP, CSRF cookie, and unreflected `next` parameter; updated the allocation-form test to assert the new confirmation hook.

Verified locally: 12 focused security/confirmation tests passed; Django `check`, migration checks, Ruff lint/format, dependency check, and `node --check` passed. The all-in-one repository runner stops at its MySQL-only version probe when configured with the disposable SQLite test backend. A directly forced full SQLite test run is also not a valid suite result because MySQL information-schema/SQL-mode and row-lock concurrency cases require MySQL. Run fresh MySQL CI on the published follow-up before treating it as fully verified.

## Issue disposition

- TC-SEC-06: **PASS for the listed isolated localhost conditions**; production deployment claims remain out of scope.
- TC-SEC-08: **baseline executed**, with the two remaining observations awaiting QA disposition.
- HMS-16/#38 remains open pending QA's case/alert disposition and actual QA/Dev/PO decisions.
- HMS-21/#43 remains **NOT READY** pending the independent Unit Test Report/#41, remaining case and priority reviews, actual team/guide approvals, instructor submission instructions, final package review, and genuine submission receipt.
