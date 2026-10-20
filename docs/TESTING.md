# Automated testing

Configure the MySQL application account and `.env` using the README. The account
must have privileges on both the application database and `test_<DB_NAME>`.
Tests use a separate database which Django creates and removes; they do not seed
the development database with the volume-test records.

Install the development requirements and run the checks from the repository root:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe scripts\run_checks.py
```

On Linux, use `.venv/bin/python` in place of the Windows executable. Activation
also allows the shorter `python scripts/run_checks.py` command on either OS.

The runner checks lint and formatting, the actual MySQL connection, migration
consistency, the complete Django suite and branch-inclusive coverage with a 70%
minimum. It exits with a nonzero code on failure. The lint rules cover Python
errors, imports and whitespace; E501 is excluded for long messages/strings, and
Ruff formatting uses an 88-character target. Generated migrations are excluded
from formatting. Coverage excludes tests, migrations and declarative project
configuration; application models, forms, views, services, authentication,
authorization, audit and admin logic remain measured.

## Test structure

| Location | Coverage |
| --- | --- |
| `hms/tests.py` | MySQL 8, SQL modes, InnoDB and India-date lookups |
| `accounts/tests.py`, `accounts/test_security.py` | Login, roles, lockout on both login routes, session expiry, cookies, CSRF and password policy |
| `audit/tests.py` | Required event metadata, privacy, administration, atomic rollback, append-only behavior, retention and pagination |
| `hostels/tests.py` | Hostel/room validation, database constraints, generated beds, safe capacity changes, permissions, filtering and failed-write rollback |
| `students/tests.py` | SRS fields, ID uniqueness/immutability, search, soft deletion, permissions, audit rollback, 5,000-record searches and allocation read-contract queries |
| `tests/factories.py` | Synthetic student fields matching SRS Appendix B |
| `tests/test_sprint1_integration.py` | Staff workflow using real login and CSRF, rolling idle expiry, concurrent failed logins and concurrent duplicate registration |

Run a module directly when investigating a defect, for example
`python manage.py test hostels --noinput --verbosity 2`. Run the complete checks
after a behavioral change or before review. New allocation/payment tests should
live in their respective apps when those Sprint 2 features are implemented.

The allocation contract test temporarily creates a table **inside the test
database** containing Student/Bed foreign keys and a vacate date. It exercises
the real SQL used by current-hostel search, deactivation restrictions, bed-status
restrictions and availability filtering. This fixture does not implement or
verify Sprint 2 allocation operations. Repeat integration against the actual
Allocation model when HMS-08 is available. That implementation must lock Student
before allocation and protect historical Student/Bed references from deletion.

## Evidence and failures

`test-results/` contains one log per check, `coverage-report.log`, `coverage.xml`
and `run.json` with the code revision, dirty-tree flag, versions, commands, exit
codes and durations. These generated files are ignored by Git. The reviewed
summary is in `docs/test-evidence/sprint1.md`.

A failed test is recorded in `django-tests.log` with its test name and traceback;
the runner still attempts to save coverage. Fix defects in a focused commit and
preserve the failing log when reporting a defect. Do not replace MySQL with
SQLite to make the database or concurrency tests pass.

The GitHub Actions workflow applies migrations to fresh MySQL 8.4, then runs the
same checks on Ubuntu with Python 3.11 and 3.14. Each job uploads its logs and
coverage as a `sprint1-python-<version>` artifact, including on failure. CI
credentials are disposable values for the service container; deployment uses
environment-specific secrets. The local verified environment is Windows 11,
Python 3.14.7, Django 5.2.18 and MySQL 8.4.9.

The two-second tests measure local test-client requests. The 50-user load test,
2,000-bed capacity test, browser compatibility/usability, deployment TLS and
backup/restore verification remain the separately planned system work.
