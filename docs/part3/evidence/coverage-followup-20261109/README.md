# Coverage follow-up for Vaishnavi's todo

Measured **9 November 2026 in Asia/Kolkata** (8 November UTC), using Python 3.14.7, Django 5.2.18, MySQL 8.4.9 and coverage.py 7.16.2. The local source was base commit `482ef795e0c538f1bf25b9a2f79266051727ab7e`, tree `5885d94dba039dbcd0155c2310b11e5d1a8c36a3`, plus the four new test files hashed in [verification.json](verification.json). The local run correctly records **git_dirty=true**. Publication documentation was added afterwards; this is not described as a clean-checkout run.

## What the todo measured

A fresh process running only `manage.py test students hostels` reproduces **every one of the todo's 23 file percentages and all its totals**: 1,034 covered statements out of 1,772, 738 missed statements, 424 branches, 41 partial branches, and **53.14207650% combined coverage**. Its 57 selected tests all pass. Coverage reporting exits **2**, as expected when measuring that selection against the unchanged full-project gate.

The todo supplies no original command, tested revision or raw artifact. This reproduction establishes that the same result occurs with that partial selection; it does not identify the author's original command. The 53% is combined statement/branch coverage; its statement-only percentage is 58.35%. It cannot establish a failing full-suite run.

## Fresh complete verification

| Observation | Result |
|---|---|
| Complete verification runner | All **12 gates PASS** |
| Ordinary mixed suite | **200 methods: 199 PASS, 1 expected timing SKIP, zero failures/errors** |
| Timing outside coverage | **1 PASS** |
| Configured statements | **1,590 / 1,772 = 89.73%** |
| Configured branches | **348 / 424 = 82.08%** |
| Combined configured gate | **1,938 / 2,196 = 88.25%; PASS against 70%** |
| Application subtotal, excluding scripts | 1,511 / 1,677 statements; 336 / 410 branches |
| New isolated supplement | **10 / 10 PASS**, database setup skipped |
| Separate owned integration recipes | **9 / 9 PASS**, exact TC-REG-S2-08 through TC-REG-S2-16 identities |
| Offline recovery / owned-runner safety | **32 / 32 and 7 / 7 PASS** |

The configured source, exclusions and 70% threshold are unchanged. Demo commands and other unexecuted files remain in the denominator. The ordinary JUnit identities are exactly the frozen historical 190 plus the new ten, with no duplicates. All 19 frozen classified test-source hashes still match. Historical classification, conservative76, sensitivity100, case statuses and evidence remain unchanged.

The ten additions address specific contracts independently identified by reviewers:

| New file | Methods | Assertion scope |
|---|---:|---|
| `accounts/test_backend_regressions.py` | 2 | A replaced password is rejected and its replacement accepted after the backend reread; returned identity and failed-attempt state are checked. Real unsaved users/password hashes, with persistence and the transaction boundary mocked. This does not prove real lock/concurrency behavior. |
| `allocations/test_validation_units.py` | 3 | Direct `Allocation.clean()` rejects status/date conflicts and dates outside the allocation period, and accepts inclusive boundaries. Unsaved raw-ID models and a fixed date; no claim about database constraints. |
| `hms/test_validation_response.py` | 4 | Exact JSON status/code/message for missing records, all conflict/domain codes, unknown codes and uncoded multiple errors. |
| `payments/test_status_units.py` | 1 | A configured fee of 1000.00 with payment 1000.01 remains Paid with due 0.00. Plain input object; query/transaction behavior is outside this test. |

All four classes use `SimpleTestCase`. A separate execution points at dummy credentials on `127.0.0.1:1`; it passes all ten and explicitly skips the unused database. The supplemental method identities, source hashes, dependency disclosures and outcomes are recorded separately in `new_classification_supplement`.

## Additional areas and ownership (todo section 4)

The Part-1 Work Distribution responsibility matrix assigns accounts and audit to Sreeharsha, allocations/payments/reports to Devansh, and test-report coordination to Vaishnavi. These existing responsibilities guide this handoff; no new teammate assignment or acceptance is inferred.

| Additional area | Fresh full-suite combined coverage | Disposition |
|---|---:|---|
| `audit/mixins.py` | 100% | Existing audit/admin tests exercise it; Sreeharsha's audit scope. |
| `audit/views.py` | 100% | Existing permissions/filter tests exercise it; Sreeharsha's audit scope. |
| `audit/signals.py` | 91.30% | 19/19 statements and 2/4 branch outcomes; remaining paths are disclosed in the JSON, without a new per-file coverage requirement. Sreeharsha's audit scope. |
| `audit/management/commands/purge_audit_logs.py` | 100% | Existing retention-command tests exercise minimum retention, dry-run and purge behavior; no duplicate test group added. Sreeharsha's audit scope. |
| Both `accounts/management/commands/create_demo_*.py` commands | 0% | Genuinely unexecuted by this suite; all 98 statements and 32 branch outcomes remain included. Sreeharsha authored these in PRs #55/#56. Owner/QA can prioritize dedicated command regressions; this handoff does not claim those tests exist or invoke demo commands against installed application data. |
| `scripts/run_checks.py` | 83.49% | 79/95 statements and 12/14 branch outcomes. Devansh supplies runner/coverage evidence under #42; existing runner tests and this fresh 12-gate execution provide tooling verification, outside an application-unit numerator. |

No per-file 70% threshold is specified by the configured gate. The two demo commands' zero coverage is a disclosed remaining test opportunity, rather than evidence of the todo's alleged failing full-project gate. QA retains the application-logic scope and report decisions under #41.

## Reproduce and interpret

Use the repository's installed development requirements and a dedicated MySQL 8.4 test instance with a fresh `hms` schema, migrations applied, and no existing `test_hms` schema. Run database suites serially. This execution used a newly initialized private loopback server on an unused port; the installed MySQL service was not changed. The owned server was validated before use and shut down afterwards. The stale repository-root `.coverage` was preserved byte-for-byte.

For the partial diagnostic, clear inherited coverage controls and set `COVERAGE_FILE` and `HMS_TEST_OUTPUT_DIR` to new diagnostic paths. With the unchanged `.coveragerc`, execute:

```text
python -m coverage run manage.py test students hostels --noinput --testrunner=xmlrunner.extra.djangotestrunner.XMLTestRunner
python -m coverage report
python -m coverage json -o <new-diagnostic-directory>/coverage.json
```

The last two commands intentionally return 2 for this selected suite. Use fresh output locations for the full run:

```text
python scripts/run_checks.py --output-dir test-results/<new-run>/checks
python -m unittest discover -s scripts/part3 -p test_issue40_recovery_safety.py -v
python -S -m unittest discover -s scripts/part3 -p test_owned_runner_safety.py -v
python scripts/part3/run_owned_regressions.py --output-dir test-results/<new-run>/owned
```

`run_checks.py` runs lint, format, dependency, Django, applied-migration, migration-consistency and static checks, then ordinary coverage/JUnit collection, reports and separate uninstrumented timing. It allocates its own coverage/JUnit paths. The measured local output is `test-results/todo-20261108T184656Z/`; raw data, logs and XML remain ignored. The durable JSON exports exact method outcomes, file-level statements/branch arcs, totals, source identities, commands, dependency versions, exit codes and raw artifact hashes. It preserves the expected failing diagnostic exit codes separately from the passing complete checks. The offline owned-runner safety log's deliberately generated NOT RUN fixture is not the actual nine-case execution result.

## HMS-19 handoff and remaining scope

The full-project **configured 70% gate is verified PASS**. Vaishnavi can use these results and the separately classified ten additions in her [HMS-19 / #41](https://github.com/Sreeharsha2240/hostel-management-system/issues/41) report. This supplement supplies module-owner evidence; it does not author her distinct `Unit_Test_Report.md` or supply a QA signature.

**Formal SRS section 6.4 unit application-logic coverage remains UNPROVEN.** The submitted Test Plan permits Django model/form/view units and separately identifies ORM/MySQL transaction/constraint integration. Apply behavior-based classification and disclose dependencies. QA must still record actual boundary decisions, an appropriate application-logic denominator and attributable selected-unit measurement. Mixed coverage includes startup/shared setup, integration, concurrency, system surrogates and tooling; 88.25% cannot be relabeled as unit-only coverage. The historical 76/100 selections were not rerun or silently expanded in this follow-up.

The [previous development handoff](../../Development_Review_20261108.md) retains its original scoped observations. This work neither closes #41 nor establishes whole-plan acceptance, transport/ZAP completion, teammate approval or final submission readiness.
