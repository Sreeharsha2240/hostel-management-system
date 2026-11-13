# HMS-19: all-application-statements follow-up

Sreeharsha's decision, relayed by the user on 13 November 2026, requires counting **all application statements, including declarative rules**. The earlier 52.50% result does not meet the 70% requirement. The separate function-body figure is not accepted as proof of that requirement. This records the relayed decision; it does not invent a GitHub review or a team signature.

## Method and comparable selections

The [measurement harness](../hms19-unit-review-20261113/reproduce.py), `.coveragerc`, coverage 7.16.2, application denominator and exact method-context attribution remain unchanged. Database connections are forbidden during discovery and execution. Shared setup, startup and database regressions receive no unit-method credit. Scripts remain a separate subtotal, as before.

- [scope-baseline.json](scope-baseline.json) preserves exactly the previous 255 isolated method IDs and refreshes source pins for the current checkout.
- [scope-expanded.json](scope-expanded.json) contains those same 255 IDs plus 33 explicitly listed isolated methods. No original method was removed. The expansion is disclosed rather than silently growing module labels.
- Both scopes pin the same 178 source/configuration/harness inputs. Each measurement additionally fingerprints its own scope file. The workflow runs both selections on each Python version and uploads both results in the isolated-unit artifact.
- The old [scope](../hms19-unit-review-20261113/scope.json), harness and published historical evidence remain unchanged. Their old pins intentionally describe their old source, rather than pretending to apply after this test/workflow change.

The unchanged historical harness labels its output as a diagnostic with scope acceptance pending. That generic historical metadata is not the current disposition: under the decision above, **the measured all-statements requirement is NOT MET**. The function-body diagnostic remains useful only to locate untested callable paths.

## Additional behavior tests

| Module | Methods | Contracts exercised |
|---|---:|---|
| `accounts.test_remaining_view_units` | 5 | Logout method and redirect; audited HTML permission denial; new/invalid account forms; selected update account; admin password response delegation. |
| `allocations.test_remaining_view_units` | 4 | Available-bed eligibility; POST dispatch; normalized four-field search and empty pagination; selected student's HTML history. |
| `hostels.test_remaining_view_units` | 3 | Warden management denials; new/invalid hostel form; room/hostel edit instances and headings. |
| `payments.test_remaining_view_units` | 6 | POST dispatch; unsupported methods; successful receipt navigation; actual invalid student/amount errors; failed adjustment form/domain paths; receipt lookup. |
| `reports.test_remaining_view_units` | 1 | Correct report kind and refusal of writes before aggregation. |
| `students.test_remaining_view_units` | 3 | Permission denial; immutable student ID and hidden status; idempotent deactivation after querying that student's active allocation. |
| `hms.test_remaining_model_units` | 11 | Invalid dates/amounts; inactive allocation mutation guards; first full payment reversal; forbidden payment update modes; safe queryset delegation; active-student save; demo bed exhaustion/continuation; retention CLI defaults/errors; public display labels. |
| **Total** | **33** | Isolated `SimpleTestCase` methods; parameterized cases are not counted as extra methods. |

Mocks replace persistence and service collaborators. Documented `__wrapped__` calls isolate transaction-decorated decision bodies; these units do not establish locking, persistence, constraints or rollback. Those remain separate integration concerns. No production statements, exclusions or threshold were changed for this follow-up.

## Results and the remaining limit

| Selection | Isolated outcome | Application statement coverage |
|---|---:|---:|
| Original 255, on current source | 255 PASS; zero database attempts | 894 / 1,703 = **52.50%** |
| Explicit additive 288 | 288 PASS; zero database attempts | 946 / 1,703 = **55.55%** |

All 52 previously missing callable-body statements now receive selected-method credit. The denominator still includes 757 declaration/import statements, all of which execute outside selected methods: 731 during startup and 26 during later runner activity. Inspect the exported per-file included/executed line sets rather than treating reads of a field or validator as execution of its earlier declaration.

For this unchanged source and eager-import method, even the optimistic ordinary-method ceiling is **946 / 1,703 = 55.549031%**. At least **1,193** statements are needed for 70%, leaving **247** statements below that requirement after all callable-body lines are covered. This is a limitation of this attribution method, not a claim that declarative behavior cannot be tested.

Two independent technical reviewers checked the measurement and the new tests. Their fixture/assertion improvements were applied before final verification: valid inactive-allocation dates, exact normalized search predicates, real form-produced invalid-choice errors, and exact active-allocation lookup arguments. The preliminary pre-review runs remain ignored locally and are not the final evidence. Automated review is not a teammate's formal QA/PO approval.

HMS-19/#41 remains open and PR #74 remains draft. The next coverage decision must specify a defensible way to attribute declaration-rule evidence while retaining the all-statements denominator and excluding unrelated/shared execution, or explicitly amend the acceptance criteria. Reloading modules, crediting shared setup, shrinking the denominator or changing the threshold has not been used to manufacture a pass. Merely adding more ordinary behavior assertions cannot bridge this remaining gap under the frozen method.

## Reproduce

Use the pinned development requirements and documented Django test environment. Choose new output paths. The isolated runs do not require a database and block connection attempts; use disposable MySQL for full/owned regressions and run database suites serially.

```text
python docs/part3/evidence/hms19-unit-review-20261113/reproduce.py --scope docs/part3/evidence/hms19-all-statements-20261113/scope-baseline.json --output-dir test-results/all-statements-NEW/baseline
python docs/part3/evidence/hms19-unit-review-20261113/reproduce.py --scope docs/part3/evidence/hms19-all-statements-20261113/scope-expanded.json --output-dir test-results/all-statements-NEW/expanded
python scripts/run_checks.py --output-dir test-results/all-statements-full-NEW
python scripts/part3/run_owned_regressions.py --output-dir test-results/all-statements-owned-NEW
python docs/part3/evidence/hms19-unit-review-20261113/test_reproduce.py
python -m unittest discover -s scripts/part3 -p test_issue40_recovery_safety.py -v
python -S -m unittest discover -s scripts/part3 -p test_owned_runner_safety.py -v
```

Clean isolated source is `ee52be71c808abbebceb3d135a4e9fa76f9ec53d`, tree `8dc30e872684019779869677cd00d6ff9400c7ae`. [measurement-baseline.json](measurement-baseline.json) and [measurement-expanded.json](measurement-expanded.json) retain exact source, timestamps, dependencies, outcomes, hashes and per-file line sets. [verification.json](verification.json) and [junit-summary.json](junit-summary.json) reconcile the separately labelled precommit full regression: all 12 gates, 476 methods (475 PASS, one expected timing SKIP), separate timing PASS, nine owned recipes PASS, and the 32/7/6 offline checks PASS. Source fingerprints around the full run match the clean isolated source. CI evidence must name its actual tested checkout and PR candidate rather than assigning a later documentation commit to an earlier run.
