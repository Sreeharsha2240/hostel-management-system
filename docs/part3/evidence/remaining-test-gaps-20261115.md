# Availability, desktop compatibility and passive ZAP follow-up

Tested on 15 November 2026 against the application source at
`1f3ae5b9f89967f13845ef520a9f7c509abdbec8`, whose application code matches
the PR #84 merge `324f460`. The servers used Django 5.2.19 and a disposable
SQLite database with synthetic test data. Windows used Python 3.14 and Linux
used Python 3.12.3 on Ubuntu 24.04.4 LTS under WSL2.

## TC-QUAL-03 — desktop compatibility

| Browser or host | Observed result |
| --- | --- |
| Windows Chrome 157.0.8103.51 | Sign-in and seven protected page checks passed |
| Windows Chrome for Testing 157.0.8103.78 | Sign-in and seven protected page checks passed |
| Windows Chrome for Testing 156.0.8078.80 | Sign-in and seven protected page checks passed |
| Windows Edge 157.0.4341.60 | Sign-in and seven protected page checks passed |
| Windows Firefox 147.0.3 | Sign-in and seven protected page checks passed |
| Windows Firefox 160.0 | Sign-in and seven protected page checks passed |
| Windows Firefox 159.0 | Sign-in and seven protected page checks passed |
| Ubuntu 24.04.4 server | Unauthorized redirect, sign-in and HTTP 200 for all seven protected pages |

The protected pages were the dashboard, students, beds, allocations, payments,
occupancy report and payment status report. The desktop runs checked page
rendering after login. The Ubuntu check used an HTTP client on a live Linux
server. The checks did not exercise the corresponding create/update forms or
MySQL on either test host. Chrome 156/157 and Firefox 159/160 were checked
against their respective official release feeds. The older Edge 156.0.4314.84
package was downloaded and verified against Microsoft's published checksum.
The package could not be unpacked into a runnable standalone browser, so Edge
156 remains untested. The full case remains pending for that version and the
remaining main workflows. Physical-phone testing is out of scope by the
owner’s decision.

## TC-SEC-08 — authenticated passive inspection

ZAP 2.17.0 inspected ordinary Chrome traffic through a localhost proxy in safe
mode on the isolated HTTP instance. The test covered a Warden sign-in, the
seven protected pages above and the application JavaScript and stylesheet.
ZAP's passive queue finished at zero. No High or Medium alerts were reported.

| Risk | Rule | Instances | Disposition |
| --- | --- | ---: | --- |
| Low | 10021, missing X-Content-Type-Options | 2 | Observed on the two static files served by Django's development static handler. Review headers on the intended static file server before making a deployment claim. |
| Low | 10036, server banner | 11 | Development server responses. Preserve the prior QA disposition and record the same observation on the wider route set. |
| Informational | 10031, possible HTML attribute reflection | 1 | Login route hotspot. Retain the existing QA reconciliation and the regression evidence associated with it. |
| Informational | 10111, authentication request identified | 1 | ZAP identified the test sign-in request. |
| Informational | 10112, session management response identified | 9 | ZAP identified session handling on the exercised routes. |

Keep the case PARTIAL pending review of the current findings and acceptance of
the exercised scope. The run adds authenticated Warden coverage to the earlier
baseline. Its evidence is limited to those local HTTP transactions and does not
include deployed HTTPS, other roles, or active testing.

## TC-QUAL-02 — working-hours availability

The 16 November attempt recorded zero probes because Windows restarted before
the window and the background observer was no longer running. A later partial
run was stopped at the owner's request and its temporary log was removed.
Neither attempt establishes a measured availability result. TC-QUAL-02 remains
NOT RUN. A valid measurement requires an agreed full observation window,
timestamped probes at thirty-second intervals, a five-second timeout and the
synthetic application running at `127.0.0.1`. Failed and missing slots count
against availability, without exclusions. At least 1,426 of 1,440 successful
probes are required for 99%.
