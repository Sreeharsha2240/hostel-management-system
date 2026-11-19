# Laptop deployment: se.d3va.dev

The owner chose this Windows laptop as the temporary host. Cloudflare provides
public HTTPS and a named Tunnel; Django and MySQL run on the laptop. This is a
live deployment, not GitHub Pages. GitHub Actions checks code but does not host
the application. The public address is https://se.d3va.dev/.

The laptop must remain awake, online and signed in as its deployment user.
Signing out, sleeping or shutting down interrupts service. Locking the desktop
does not sign out. This setup does not promise continuous availability; moving
the origin to an always-on server is the permanent-hosting path.

## Running installation

Private state is in `%LOCALAPPDATA%\HMSDeployment`, protected by an explicit
user/SYSTEM-only inherited ACL. It is outside the repository and delivery ZIPs.

| Component | Configuration |
| --- | --- |
| Public hostname | `se.d3va.dev`, Cloudflare proxied CNAME to the named Tunnel |
| Tunnel | `hms-se-laptop`, ingress for this hostname only, rejecting fallback |
| Origin | Waitress 3.0.2 at `127.0.0.1:8110`, eight threads |
| Django | `deployment.settings`, DEBUG disabled, WhiteNoise 6.12.0 |
| Database | Dedicated MySQL 8.4 instance at `127.0.0.1:33081`; MySQL X disabled |
| Application schema | `hms_live`; `hms_app` has SELECT/INSERT/UPDATE/DELETE only |
| Data | Private `mysql-data` directory, separate from the development/global server |
| Startup | Current-user logon task `HMS-se.d3va.dev`, limited privilege, no execution time limit |
| Backups | Private `backups` directory; successful startup and every 24 running hours; newest 14 retained |
| Logs | Private `logs` directory; child/event logs rotate at 5 MiB, four older files retained |

The operator's initial administrator login is in the private `OWNER_LOGIN.txt`.
Change the generated password after first login, then securely remove that
initial-password file. There are no public/shared default passwords. Use the
application's account-management page to create individual teammate accounts.
The pre-existing development database and any independent test observation are
not the production database.

From the repository root, in PowerShell:

```powershell
.\deployment\laptop.ps1 -Action Status
.\deployment\laptop.ps1 -Action Stop
.\deployment\laptop.ps1 -Action Start
```

`Stop` writes a private, latched `stop.request` and waits for owned children to
exit. Only `Start` removes that latch. Use it before planned maintenance. Do not
stop processes by executable name, kill the global MySQL service, or use
`Stop-ScheduledTask` for ordinary maintenance. The supervisor stops tunnel and
web processes before authenticating to shut down its owned MySQL process;
requests in progress can be interrupted. It never imports migrations at startup.

`InstallStartup` registers the current user's logon task, and `RemoveStartup`
removes that task without stopping an existing host. The installed private
`control.ps1` reads `operations.json`, so it follows that file's selected release.
The task does not change Windows sleep or power policies.
Its console-free Python launcher avoids dependence on a PowerShell console.
A Windows job owns the supervisor and its descendants so an abrupt supervisor
exit cannot leave an unmonitored web server or tunnel running. Task Scheduler
retries failed launches; an explicit Stop remains latched. MySQL's separate
monitor process is disabled because this supervisor owns restart behavior.

## Trust and secrets

Cloudflare terminates browser TLS and carries traffic through an authenticated,
outbound HTTP/2 Tunnel. No router port-forwarding is needed. The local origin,
database and tunnel metrics bind only to loopback. Public HTTP redirects to the
same HTTPS host. The tunnel has only this hostname rule and a final HTTP 404 rule.

Waitress trusts `X-Forwarded-Proto` from its loopback peer only and normalizes
`wsgi.url_scheme`. Django's `SECURE_PROXY_SSL_HEADER` is deliberately unset;
forwarded Host and Port are not trusted. This design assumes local processes
under the hosting user's account are trusted. Do not change the origin bind to
`0.0.0.0` or expose it on the LAN. Cloudflare's edge overwrites client-supplied
scheme headers; verify that again after any proxy/hosting change.

Production settings enforce the exact allowed host, secure HttpOnly cookies,
same-origin CSRF, HTTPS redirect, one-year HSTS and DENY framing. HSTS
includeSubDomains/preload directives apply to `se.d3va.dev` and its descendants;
they do not change the parent domain's configuration or register a preload
submission. No CSRF exemptions or wildcard origins are used. WhiteNoise serves
only collected static output, with hashed assets and compression.

`runtime.json` contains exactly the six required environment keys
`DJANGO_SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`,
and optional `HMS_PORT`. It accepts no arbitrary environment settings. The
development `.env` is disabled. `mysql-client.cnf` contains the dedicated
instance's administrative credentials for backup, migrations and shutdown;
runtime uses the restricted application account. Tunnel credentials and the
Cloudflare management certificate also stay private. Never paste those files,
session cookies, SQL backups or initial passwords into GitHub or chat.

## Release and recovery

The running application uses a private source snapshot, not the mutable working
checkout. `operations.json` records the release path, Python executable, runtime
config, MySQL binary/defaults files, cloudflared binary, tunnel config and UUID.
All paths are absolute. The supervisor validates the dedicated database bind,
port, datadir and option-file groups before starting. One OS lock prevents
duplicate supervisors. Authentication and origin readiness precede tunnel start;
child failures restart the owned stack with bounded backoff.

For an update:

1. Verify the prospective source, both existing CI jobs and deployment checks.
   Preserve frozen historical evidence and source pins.
2. Copy the runtime source and `deployment` package to a **new** private release
   directory. Exclude `.env`, private files, Git metadata and environments.
   Install `deployment/requirements.txt` into the private deployment environment.
3. Request `Stop` and take a completed MySQL backup before changing schema.
   Start only the dedicated MySQL instance for maintenance, using its explicit
   private `--defaults-file`; verify its port/datadir before any database work.
4. Apply migrations explicitly using the dedicated administrative credentials
   supplied privately in the process environment. Never grant schema-changing
   rights to the normal `hms_app` account or pass passwords as command arguments.
5. With explicit production environment values, run `manage.py collectstatic
   --noinput`, `manage.py check --deploy --fail-level=WARNING`, and
   `python -m deployment.windows --config <private-runtime.json> --check` from
   the new release. Stop the maintenance database gracefully.
6. Change only `operations.json`'s release path, refresh private `control.ps1`
   from `deployment/laptop.ps1`, refresh private `launch.py`, re-register startup
   if its action changed, then `Start`. Check public workflows and data
   persistence. Keep the preceding release and backup for rollback. A source
   rollback cannot undo an incompatible schema migration; restore its matching
   backup in isolation and verify it before selecting that database.

Backups use `mysqldump --single-transaction --quick --no-tablespaces
--set-gtid-purged=OFF` and the private defaults file. A failed/incomplete dump
does not replace a successful backup or trigger retention deletion. A successful
dump is atomically renamed from `.partial` to `.sql`. Restoring must first target
a separately named disposable schema/instance, verify migration and application
table contents, then remove only that verified disposable target. Never test a
restore over `hms_live` or the global development database.

These backups share the laptop's disk and do not protect against disk loss.
Keep a protected off-device copy before relying on this host for real records.

## Verification

Production checks have their own GitHub Actions workflow,
`.github/workflows/deployment.yml`, on Windows/Python 3.11 and 3.14. They do not
rewrite the existing frozen Django/coverage workflow or historical results.
With the production requirements installed and explicit dummy environment
values (a strong test-only secret and unused DB credentials), run:

```powershell
python -m unittest deployment.verify_windows deployment.verify_supervise deployment.verify_launch -v
python manage.py test deployment.verification --settings=deployment.settings --noinput
python manage.py check --settings=deployment.settings --deploy --fail-level=WARNING
```

The explicit modules check startup validation, loopback/proxy trust, security
settings, same-origin CSRF, actual collected/hashed/gzipped assets, secret
redaction, duplicate locking, process ownership, restart/stop and backup failure
behavior. They use dummy configuration and do not need a database. They are
named explicitly so the legacy test job needs no production-only dependencies.

Operational acceptance also checks the actual public certificate and HTTP
redirect, all role logins/access boundaries, uncached private pages, CSV/PDF
downloads, database persistence through restart, backup restoration and the
scheduled task configuration. Keep raw secrets and authenticated requests
private; publish only sanitized results. Real public uptime is distinct from
the separate historical/course availability observation.
