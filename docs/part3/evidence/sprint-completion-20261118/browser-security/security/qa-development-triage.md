# Assisted QA and Development triage, 19 November 2026

Reviewer: Codex under Devansh's explicit cross-assignee review authorization.
This records the review actually performed. It is not Vaishnavi's signature,
project-guide participation, a PO decision or instructor approval.

Reviewed build: `0d9adb39f3adcb85e75449c85900b4c283868ded`. The retained
[baseline](sanitized-baseline.json), [execution metadata](execution-metadata.json),
[response follow-up](sanitized-response-followup.json) and
[deployment check](check-deploy-actual-environment.json) are the primary records.

## Execution and scope

The official ZAP 2.17.0 baseline completed against the actual isolated Fedora
HTTP application. Twelve explicit route proofs cover ten authenticated Warden
pages plus the exact JavaScript/CSS assets. The passive queue drained to zero;
the active-scan list was empty. The one-minute traditional spider is passive
inspection, not an active penetration test or exhaustive role/route coverage.

The scanner reported zero High findings and five warning rule IDs. Console
counts are retained separately from capped JSON instance samples. `-I` permits
warning-only exit zero; it does not erase or accept findings. Both form-processing
settings were false, but informational metadata contains two login POSTs.
Configured settings are not represented as proof of GET-only behavior.

## Finding dispositions

| Finding | Actual evidence | Technical disposition |
|---|---|---|
| Medium 10038: missing CSP, one instance | `/static/hms` is a directory-style request returning an actual 404 from Django's development static handler. The authenticated application pages inspected separately return restrictive CSP. | Retain the Medium observation as a development-static-handler limitation. It establishes missing protection on that response, not a demonstrated injection or missing CSP on the protected application. Do not claim the response was fixed. A deployed static/error server must apply CSP as appropriate and be rescanned. |
| Low 10021: missing nosniff, two instances | Exact frozen JavaScript/CSS return 200 with correct MIME types through the development static handler. Application page responses inspected separately include nosniff. | Retain the two observed static-response omissions. Set `X-Content-Type-Options: nosniff` on the intended static server and retest before deployment. No uploaded or attacker-controlled static file surface was demonstrated. |
| Low 10036: version banner, 16 console instances | Django development WSGI server identifies its WSGI/Python versions. | Accepted as disclosed information exposure of the isolated development server. Suppress identifying banners in any future production server; no production-hardening pass is claimed. |
| Low 10063: Permissions-Policy, 13 console instances | Header missing on inspected responses. | Defense-in-depth header omission retained. The current mini-project does not request camera, microphone or location capabilities. Apply a restrictive policy and verify it if deployed. |
| Low 90004: cross-origin isolation/resource policy, 20 console instances | Capped JSON samples include COEP/CORP variants. Protected application pages have COOP `same-origin`. | Retain observed omissions; COEP/CORP adoption requires checking real cross-origin resource dependencies. Missing isolation alone is not a demonstrated authorization bypass. It does not waive existing CSP or own-record restrictions. |
| Informational authentication/session and cache metadata | Authentication/session messages and non-storable responses were identified; cacheable samples include static resources and an allocation redirect. | Expected areas for review. Explicit authenticated privacy, post-logout Back and own-record browser checks passed in the versioned matrix; sampled application responses carry no-store/private. Static caching is intentional. These findings supply neither a vulnerability-free guarantee nor new TLS evidence. |

The actual `check --deploy` command returned exit zero with five warnings:
HSTS disabled, SSL redirect disabled, session Secure disabled, CSRF Secure
disabled, and DEBUG enabled. These are the disclosed loopback HTTP test flags,
not acceptable production deployment settings. The command's exit code is not
a clean deployment check. Existing separately recorded HTTPS/TLS evidence keeps
its own build/configuration boundary.

## Case decision

**TC-SEC-08 technical execution: PASS with the findings and limitations above.**
The submitted baseline procedure ran on a real application; reached routes,
tool/configuration, alerts and triage are recorded. The original case requires
completed inspection and triage, not zero informational or lower-severity
observations. No public host or active scan is added as an invented prerequisite.

This decision supersedes the earlier PARTIAL assessment only for completion of
that bounded baseline/triage procedure. The original whole-plan exit criteria,
unresolved quality observations, current defect/merge status, HTTPS obligation
and genuine submission remain separately assessed. Nothing here changes the
scanner findings, retroactively approves test entry, or supplies an instructor
waiver. The owner-scoped tracking exceptions remain attributed to their actual
recorded decisions.
