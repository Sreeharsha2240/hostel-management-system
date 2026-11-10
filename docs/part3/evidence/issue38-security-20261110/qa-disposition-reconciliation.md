# HMS-16 ZAP QA handoff reconciliation — 10 November 2026

## Source and boundary

The project owner supplied `HMS-16_Issue-38_QA_Disposition.md`, a document identifying Vaishnavi as its QA reviewer and dated 10 November 2026. This note records its two alert assessments and independently checks its test-evidence question against the repository. The handoff was provided outside the repository; this note does not claim an independent ZAP rerun, a new teammate signature, or a Test Plan amendment.

## Alert dispositions from the supplied handoff

| Final ZAP observation | Supplied QA assessment | Case implication |
|---|---|---|
| `Server` header, Low / High confidence, four responses, `WSGIServer/0.2 CPython/3.14.0` | The banner belongs to the temporary `wsgiref` probe server. No HMS application defect or application-fix retest is indicated. Check the actual deployment server if one becomes available. | Retain the Low finding and the isolated-loopback limit. |
| `next=/dashboard/` HTML-attribute hotspot, Informational / Low confidence, two instances | The login view does not consume `next` and the template does not render it. No exploitable behavior was demonstrated in that path; no application fix or fix retest is indicated. | Retain the informational finding; do not call it a confirmed XSS or silently erase it. |

The scan total remains **0 High, 0 Medium, 1 Low, 1 Informational**. The supplied review recommends retaining **TC-SEC-08 PARTIAL** because the scan was passive on loopback, did not cover a deployment server, and did not itself rerun ZAP. That status is unchanged here.

## Corrected regression-test trace

The handoff says it could not locate the regression test claimed by the 9 November scan report. The repository check found it in `accounts/test_security.py` as `SessionAndLockoutTests.test_login_does_not_reflect_untrusted_next_parameter` at line 143. It sends `'"><svg/onload=alert(1)>'` in `next` to the login route and asserts that neither the complete payload nor the `<svg/onload` fragment appears in the response. `git show 24e1252:accounts/test_security.py` confirms the test was already present at the handoff's inspected HEAD.

The 10 November HMS-17 verification contains a passing JUnit entry for that exact method in `../issue39/completion-20261110/checks/junit/TEST-accounts.test_security.SessionAndLockoutTests-20261110225942.xml`. The matching `manifest.json` also lists the exact identity as PASS. This corrects the handoff's *test not located* assertion; it does not turn the reviewer's source inspection into a claimed personal test execution or expand the passive scan's scope.

## Project decision

HMS-16/#38 was already closed for the project owner's limited local-project tracking scope. This later handoff supports alert-level triage within that scope and introduces no new application defect. It does not change the original Test Plan result, remove the two alerts, promote TC-SEC-08 to PASS, or provide final QA/Dev/PO or instructor approval.
