# HMS-19 current-source unit remeasurement — 18 November 2026

This successor refreshes the exact source pins after the PR #86 room and bed
history fixes. It keeps the 288-method baseline and 294-method expanded test
selection unchanged; the 15 November scopes and measurements remain
historical. CI now points to the new scope files in this directory.

The same database-forbidden harness and `.coveragerc` are used. Each run
verified all 179 expected source pins, passed its complete frozen selection,
and made no database connection attempts. The local remeasurement used Python
3.14.0 and coverage 7.16.2 on the PR #87 candidate tree. It is a diagnostic
coverage measurement, not a fresh full-suite coverage result or a new SRS
scope acceptance.

| Frozen selection | Tests | Function-body statements | All application statements |
|---|---:|---:|---:|
| Baseline | 288/288 PASS | 957/998 (95.89%) | 957/1,767 (54.16%) |
| Expanded | 294/294 PASS | 960/998 (96.19%) | 960/1,767 (54.33%) |

The function-body result remains above the previously owner-approved 70%
diagnostic target. All-application-statement coverage remains separately
reported and below 70%. CI run [#150](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/44313469371)
passed the full configured checks and MySQL test suite, then stopped because
the 15 November source hashes were stale. PR #87 includes the refreshed scopes.
CI run [#151](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/44315160437)
passed both Python 3.11 and 3.14 jobs on the PR merge candidate, including the
full checks, MySQL tests, both frozen selections and the owned regressions.
GitHub retained the test and measurement evidence as run artifacts.
