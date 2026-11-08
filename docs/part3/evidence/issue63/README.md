# HMS-26: Devansh's remaining expanded case executions

**Issue:** [#63](https://github.com/Sreeharsha2240/hostel-management-system/issues/63).
**Executed:** 2026-11-08T07:53:43.853954+00:00 to 2026-11-08T07:53:57.274971+00:00.
**Measured clean commit:** `6636098cb728aa17c2abf5e42c358a5d400261e7`; tree `0faea77304a30ceb436e1411a2c513dd1f3c6f44`.
Owner: Devansh Gupta (`DevaOnL`).

The [pre-execution technical review](pre-execution-review.md) is included in that
commit. Three independent automated reviewers checked recipes, assertion scope,
runner safety and candidate evidence. The clean run recorded **nine PASS**, no
failures/errors/skips, with complete per-step expected/actual observations.
The register calls these OWNER PASS; named human final acceptance remains separate.

| Case / actual observations | Technical priority | Recorded steps | Result | Actual scope |
|---|---|---:|---|---|
| [TC-REG-S2-08](execution/TC-REG-S2-08.json) | High | 4 | OWNER PASS | Audit failures rolled back allocation and release; failed target-bed storage preserved both beds, original history/dates and audits; the same transfer retry created exactly one successor and actor event. |
| [TC-REG-S2-09](execution/TC-REG-S2-09.json) | High | 13 | OWNER PASS | Two original sequential receipts and actor audits were preserved through ten prohibited ORM mutations; a real adjusting entry created the next receipt and left original records unchanged. |
| [TC-REG-S2-10](execution/TC-REG-S2-10.json) | High | 16 | OWNER PASS | Thirteen invalid inputs, controlled audit failure and sequence exhaustion preserved payment/counter/audit state; retry used the next receipt; exhausted history remained intact. |
| [TC-REG-S2-11](execution/TC-REG-S2-11.json) | High | 2 | OWNER PASS | Distinct connections executed overlapping real service calls at the Student locking query. One correction succeeded, one over-reversal was rejected; receipt counter 2, net INR20 and exactly two actor audits remained. |
| [TC-REG-S2-12](execution/TC-REG-S2-12.json) | Medium | 3 | OWNER PASS | JSON/CSV/HTML reconciled payment totals, required Bed and current/latest valid location after transfer/release/correction; never-assigned and cancelled-only states were tested separately; zero-fee advance remained Pending. |
| [TC-REG-S2-13](execution/TC-REG-S2-13.json) | Medium | 9 | OWNER PASS | Nine CSV/HTML vectors preserved Unicode, quotes and newlines, neutralized each dangerous prefix and displayed escaped literal labels without an injected element. |
| [TC-REG-S2-14](execution/TC-REG-S2-14.json) | Medium | 7 | OWNER PASS | Both report routes passed empty, invalid/missing-hostel, populated leading-zero, unsupported-format and method-boundary checks; populated filter results matched the exact expected hostel/student/Bed. |
| [TC-REG-S2-15](execution/TC-REG-S2-15.json) | High | 64 | OWNER PASS | Documented malformed JSON categories were rejected with generic errors through parser and representative real endpoints; every rejected request preserved business-state hashes; valid scalar/Unicode/form controls passed. |
| [TC-REG-S2-16](execution/TC-REG-S2-16.json) | High | 65 | OWNER PASS | Typed dates/references and required/missing-reference requests returned the specified 400/404 error contracts without changing business state/counters/audits; valid optional-date controls passed. |

The full raw [execution record](execution/run.json), [console log](execution/execution.txt)
and `execution/junit/` preserve exact method identities, timestamps, versions,
commands, input hashes and raw-result SHA-256 values. Intermediate
ASSERTIONS_COMPLETED means assertions finished; only reconciled JUnit after
teardown establishes PASS. All data are synthetic; no database dump or credentials
are published. The concurrency observation proves service overlap and one-winner
correctness; it does not measure database lock-wait duration.

## Reproduce serially

Use the README MySQL setup and an absent disposable `test_hms`. Existing,
custom or mirrored test databases are refused; retain earlier output directories.
Run one database suite at a time from the repository root:

```sh
python -S -m unittest discover -s scripts/part3 -p test_owned_runner_safety.py -v
python scripts/part3/run_owned_regressions.py --output-dir test-results/NEW-owned-cases
python scripts/run_checks.py --output-dir test-results/NEW-core-checks
python -m unittest discover -s scripts/part3 -p test_issue40_recovery_safety.py -v
```

Local environment: Windows-11-10.0.26200-SP0; Python 3.14.7, Django
5.2.18, mysqlclient 2.3.0,
MySQL 8.4.9, xmlrunner 4.0.0.
The test-client HTTP run explicitly disables secure redirect/session/CSRF cookie
flags only for its child. It is not TLS, live-browser or deployment evidence.
MySQL 8.4 differs from the submitted 8.0 baseline. Review/execution on 8 November
is later than the original 2–6 November window; no extension or waiver is supplied.

## Core verification and scope

The [same clean commit's core record](core/run.json) passed **12 gates**,
**190 mixed methods: 189 PASS / one expected timing SKIP**, followed by a
[separate uninstrumented timing PASS](core/timing-smoke.txt).
[Recovery safety](recovery-safety.txt) passed 32 offline checks and
[owned-runner safety](runner-safety.txt) passed seven offline checks.
Core JUnit and gate logs are retained under `core/`; raw coverage JSON/XML and
the coverage database remain in the private run directory. Core coverage totals
and hashes of those originals remain in the record/manifest. The nine explicit
cases are outside ordinary discovery and coverage; they are not nine extra unit
tests or part of the 190-method denominator. Existing coverage reports and the
formal SRS unit70 **UNPROVEN** disposition are unchanged.

Candidate attempts `initial` and `review-corrections` and `full-candidate` remain
under ignored `test-results/owned-regressions-20261108/` on the execution machine.
They were dirty and are not represented as this clean run. Review corrections
strengthened actual locking-query overlap, separate never-assigned observations,
populated filter oracles, failure outcomes and database/output protection; no
production defect or changed application behavior was found in these nine cases.
Original failed load/harness attempts, browser PARTIAL and prior companion
evidence remain unchanged in their original evidence directories.

## Handoff and remaining acceptance

These executions finish all **27 exclusively Devansh-owned** case records:
13 original, five retained regressions and nine expanded recipes. They change
only these nine latest statuses. Expanded totals become **48 OWNER PASS / three
PARTIAL / nine NOT RUN / one BLOCKED**, with **51/61 (83.61%)** having some
exercise and **48/61 (78.69%)** owner-pass observations. Original 33 remain
30 OWNER PASS / two PARTIAL / one NOT RUN. These are not accepted-pass metrics.

Sreeharsha #38/#43 can integrate this published owner evidence; Vaishnavi #41 can
reference it as integration evidence alongside the existing module-owner input.
It does not publish her Unit Test Report. Shared TC-QUAL-04 remains BLOCKED;
SRS unit70, remaining security/quality cases, actual human QA/Dev/PO/guide
decisions, instructor packaging instructions and real submission receipt remain
unresolved. Whole-plan readiness remains **NOT READY**. #40's original scoped
technical closure is separate and unchanged.

[Artifact manifest](artifact-manifest.json) hashes every published raw input and
also identifies omitted local coverage artifacts. Publication/CI review is
recorded separately from this execution source.

The [final technical review](final-technical-review.md) records the independent
clean-run checks and preservation audit. Publication CI and merge results are
tracked on the linked issue and pull request.
