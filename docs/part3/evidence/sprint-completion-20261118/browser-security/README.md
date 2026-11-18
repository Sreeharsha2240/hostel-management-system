# Browser, session, security and availability evidence

The selected browser workflows passed on twelve official browser builds at application commit `0d9adb39f3adcb85e75449c85900b4c283868ded`: current and previous major Chrome, Firefox and Edge on Windows 11 and Fedora 44 Linux. Each selected result contains nineteen observations, actual browser capabilities, executable and driver hashes, screenshots, a parsed receipt PDF and both CSV exports. These are automated browser checks using synthetic records. Responsive screenshots use browser emulation; no physical-phone or human first-use result is claimed.

| Browser | Windows 11 | Fedora 44 Linux |
| --- | --- | --- |
| Chrome for Testing | 158.0.8127.36 / 157.0.8103.78 | 158.0.8127.36 / 157.0.8103.78 |
| Firefox | 160.0.1 / 159.0.1 | 160.0.1 / 159.0.1 |
| Edge | 157.0.4341.60 / 156.0.4314.84 | 157.0.4341.60 / 156.0.4314.58 |

Microsoft published different previous-major Edge patches for the two operating systems. Package URLs, official feed snapshots, vendor checksums where supplied, and observed SHA256 hashes are retained under [platform](platform). The private Windows downloads were extracted without replacing the installed browser. Linux used isolated downloads and MySQL 8.4.13; Windows used MySQL 8.4.9. Both used Python 3.14.7 and Selenium 4.53.0.

The workflows cover Admin account/inventory/student creation and updates; Warden allocation, transfer, release, payment and adjustment; receipt contents and report CSVs; Student record isolation; stored-script escaping; missing-CSRF rejection; logout and browser Back; and responsive layout. Transfer, keyboard release and button-level deactivation each exercise cancellation and acceptance, including persisted-state checks and exactly one confirmation. The genuine session-expiry test separately observed **901.003 actual seconds** without an application request, then confirmed a protected revisit returned to `/login/`: [result](session/result.json), [screenshot](session/expired-session-login.png).

- [Combined summary](summary.json), [Windows results](windows/summary.json), [Linux results](linux/summary.json).
- [Accepted Git-object source pins](source/accepted-git-pins.json), measured source before/after files and [running-server startup provenance](source/linux-server-startup.json).
- [Authenticated ZAP baseline](security/sanitized-baseline.json), [execution metadata and console warning counts](security/execution-metadata.json), [selected-header follow-up](security/sanitized-response-followup.json), [actual-environment deployment check](security/check-deploy-actual-environment.json), and [assisted QA/development triage](security/qa-development-triage.md).
- [Availability observation plan](availability/observation-plan.json), [pending snapshot](availability/summary.json), [observer guard checks](availability/observer-negative-probes.json).
- [Execution history and measurement limits](RUN_HISTORY.md), [reproduction procedure](REPRODUCING.md), [artifact hashes](artifact-manifest.json), and [artifact verification](artifact-verification.json).

All 269 canonical source/font pins match across both hosts and remained unchanged in their recorded before/after measurements. Windows snapshots include one additional ignored `payments/fonts/__pycache__/rebuild_subsets.cpython-314.pyc`; the 270-versus-269 measured count is explained by that bytecode file. Evidence/report edits are outside this application fingerprint scope.

The passive scan completed with ZAP 2.17.0, twelve explicitly checked HTTP-200 routes (ten protected Warden pages and two static assets), an empty passive queue, and zero active scans. It reported zero high findings, one medium finding, five low finding variants and four informational variants. The medium finding concerns `/static/hms`, an actual development-server static 404. Application dashboard/allocation pages returned CSP, `nosniff`, private/no-store and COOP headers. Findings and the five unsilenced `check --deploy` warnings remain visible for technical disposition. Exit zero with ZAP's `-I` option does not establish that there were no warnings. The raw JSON exporter caps instance samples; the console counts are retained separately. Form processing was configured false, but informational metadata contains two login POST messages; no GET-only claim is made.

**Availability is PENDING.** The live observer is job `job_c4c3658121`, PID `2322483`, under `/opt/mainbox/workspace/hms-browser-20261118/availability-20261119-0d9adb3-final`. Its real window is 19 November 2026, 08:00–20:00 IST: 1,440 slots at thirty-second intervals, a strict five-second deadline, and at least 1,426 successful authenticated HTTP-200 dashboard responses. Failed and missing slots count in the full denominator. The exported snapshot is WAITING with zero probes; it cannot establish a pass. The service and observer remain running. The selected one-day synthetic observation will apply only to its measured window and sampling interval.

Credentials, cookies, raw driver/scanner logs, raw HTTP bodies, private configuration and database content are excluded from this directory. The scan covers the actual isolated loopback HTTP application and authenticated Warden routes; it does not establish TLS or production-host behavior. Human approvals and whole-plan exit decisions require their own actual evidence.
