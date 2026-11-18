# Reproducing the observations

Use a disposable MySQL database and synthetic accounts on the stated frozen commit. Do not run these mutating UI workflows against live records. Browser package URLs, checksums and binary/driver hashes are in `platform`; exact browser versions are in the platform result summaries. The original private host paths in metadata describe execution provenance and need to be adapted for a fresh machine.

The files under `harness` are byte-for-byte execution/preparation snapshots stored as `.py.txt`. Copy the required snapshots to a private directory and restore their `.py` filenames. The raw snapshots are not imported by the application. `matrix.py.txt` is the final helper used by the successful final Linux four-browser run and the scheduled observer. Retained older matrix snapshots explain the measured differences; consult run metadata before attributing a historical hash to a particular file.

Create a private JSON configuration with `authorized_frozen_run: true`, `source_root`, `expected_commit`, `expected_source_pins`, `base_url`, `django_env_file`, and `accounts.admin`/`accounts.warden` username/password objects. `expected_source_pins` points to the accepted pin manifest. Keep secrets outside Git. The app origin must be loopback. Supply private browser specifications with `id`, browser kind, exact expected version, and local browser/driver paths; the harness CLI and snapshots show the complete schema. Use the application Python interpreter with Django, mysqlclient, Selenium 4.53.0, pypdf and the project's receipt/font requirements.

```text
<application-python> matrix.py --config <private-config.json> --specs <browser-specs.json> --output <new-empty-output-directory>
<application-python> idle_session.py --config <private-config.json> --specs <browser-specs.json> --output <new-empty-output-directory>
<application-python> zap_baseline.py --config <private-config.json> --output <new-empty-output-directory>
```

The matrix uses real forms and reads committed database state to validate its unique fixtures. It saves source snapshots before and after, screenshots, exported reports, observations and browser results. The inactivity procedure waits 901 real seconds with a separate browser session and checks browser network records for application activity. Do not shorten its wait or manufacture clock advancement.

ZAP uses the pinned official image and the exact argument list recorded in [security execution metadata](security/execution-metadata.json). Its API is loopback-only, authentication is injected only for the isolated same-origin app, and its active scan list must remain empty. Keep the raw directory private. Publish only sanitized findings, route status/hash proofs, queue/scan metadata and technical dispositions. The configured form options and observed login POST metadata are both retained. Scan exit zero with `-I` permits warning-only completion.

For `manage.py check --deploy`, load the same private environment as the actual running application and retain stdout, stderr, exit code and non-secret relevant settings. The included run retained all five development-configuration warnings. Do not substitute hypothetical production settings for the environment being measured.

For availability, read the final observer's CLI/configuration in its snapshot and [observation plan](availability/observation-plan.json). It requires the accepted source manifest and the running server's startup provenance before probing. Preserve the fixed working-hours window, thirty-second schedule and full 1,440-slot denominator. Requests after a missed slot cannot fill that slot retrospectively. Run the seven offline negative probes before relying on a changed observer; they use temporary Git data and fake responses, without real application probes or clock changes. The existing real observer must remain undisturbed until its window finishes.

To verify the packaged artifact bytes, restore `harness/verify_published_evidence.py.txt` as a private `.py` file and pass this evidence directory as its sole argument. It validates the full artifact manifest, twelve browser results and screenshot/export hashes, source pin agreement, genuine idle evidence, scan completion metadata and the explicitly pending availability snapshot. A new completed availability export requires a new manifest and updated status verification.
