# Sprint 1 test evidence

Verified on 21 October 2026 (Asia/Kolkata), from the original development
checkout. The tested code revision was
`26d8bd0a1c18da3085d7a282ec5f9b6bf8781243`; the working tree was clean when
the runner started. Later evidence and handoff edits are documentation only.

## Reproducible command and environment

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe scripts\run_checks.py
```

| Component | Verified version |
| --- | --- |
| OS | Windows 11, build 26200 |
| Python | 3.14.7 |
| Django | 5.2.18 |
| Database | MySQL 8.4.9, InnoDB |
| Coverage.py | 7.16.2 |
| Ruff | 0.17.1 |

## Local results

| Check | Result |
| --- | --- |
| Ruff lint | Passed |
| Ruff format | Passed; 58 files already formatted |
| Django database system checks | Passed; zero issues |
| Migration consistency | Passed; no model changes detected |
| Django test suite | 83 passed, zero failures/errors, zero skipped |
| Test execution time | 21.391 seconds, excluding database setup/teardown |
| Branch-inclusive coverage | 92.08%; required minimum 70% |
| Statement coverage | 926 / 984 statements, 94.11% |
| Branch coverage | 190 / 228 branches, 83.33% |
| Coverage XML | Generated successfully |
| Complete runner | Passed, 19:01:31-19:02:05 UTC on 20 October |

The suite creates and removes the separate `test_hms` database. It applies all
migrations from scratch and checks MySQL 8, strict SQL modes, InnoDB and local-date
lookups. It exercises role permissions, both login routes, lockout, rolling
session expiry, CSRF, audit privacy/retention/immutability, atomic rollback,
student validation and search, and hostel/room/bed validation and resizing.

Integration checks include a real-login staff workflow with enforced CSRF,
five simultaneous failed logins and two simultaneous duplicate student
registrations. Paginated searches over 5,000 synthetic student records pass the
two-second local request target. A temporary MySQL fixture exercises the future
Allocation model's read contract; it does not verify allocation operations.

The existing development database was backed up privately before applying
`accounts.0002`, `audit.0001`, `hostels.0001` and `students.0001`. All four
migrations and the subsequent database check passed. No volume-test fixtures
were inserted into the development database. Backup restoration was not tested.

## Saved evidence and CI

The original checkout's ignored `test-results/` directory contains `run.json`,
all eight command logs and `coverage.xml`. `run.json` records the tested commit,
clean-tree status, versions, commands, durations and exit codes. Every recorded
command exited with code zero. The workflow also passed actionlint 1.7.12.

[GitHub Actions run 39480140291](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/39480140291)
passed both jobs on Ubuntu with Django 5.2.18 and fresh MySQL 8.4.11 databases:

| Python | Tests | Test duration | Branch-inclusive coverage | Result |
| --- | --- | --- | --- | --- |
| 3.11.17 | 83 | 28.075 seconds | 92.08% | Passed |
| 3.14.8 | 83 | 25.392 seconds | 92.08% | Passed |

The PR workflow tested generated merge revision
`f5971e275be8981c3d34d13fd84e4c45c7673aa9` for head `26d8bd0`. Both jobs
record a clean working tree and eight zero exit codes. Their uploaded
`sprint1-python-3.11` and `sprint1-python-3.14` artifacts were downloaded and
checked against the local results. The corresponding push workflow
[also passed](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/39480139353).

## Acceptance boundaries

These results cover the implemented Sprint 1 behavior. Allocation and payment
operation tests must be added when HMS-08/HMS-09 exist; the read adapters must be
retested against the actual Allocation model. The 50-user load test, 2,000-bed
system test, browser/usability checks, deployed HTTPS, backup/restore testing
and the team's one-minute outcome video remain separate acceptance work.

See [testing instructions](../TESTING.md) for setup and failure investigation,
and the [handoff](../SPRINT1_HANDOFF.md) for review dependencies and documented
interface/presentation deviations.
