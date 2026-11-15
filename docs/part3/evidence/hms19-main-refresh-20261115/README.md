# HMS-19 current-main unit remeasurement — 15 November 2026

This successor refreshes the frozen source pins needed for CI after HMS-27
changed account models, migrations and test sources. The exact 288-method
baseline and 294-method expanded selection are retained. The historical
13 November and allocation-capacity evidence remains unchanged.

The scopes pin the configured Python sources, test files, coverage settings,
requirements, harness contracts and CI workflow. The remeasurement uses the
same database-forbidden harness and `.coveragerc`; it does not broaden the
owner-approved function-body boundary or claim review/acceptance from QA,
Development or the instructor.

## Clean local remeasurement

Both runs completed on clean commit `ff72065340d859c9512329d9406505c6e40fda15`
(tree `8263028d02eb1a128b8742e3c2b7ac7eee3eaa0b`) using Windows 11, Python
3.14.0 and coverage 7.16.2. All 179 expected source pins matched. No database
connections were attempted.

| Frozen selection | Tests | Function-body statements | All application statements | Application branches |
|---|---:|---:|---:|---:|
| Baseline | 288/288 PASS | 953/959 (99.37%) | 953/1,717 (55.50%) | 415/436 (95.18%) |
| Expanded | 294/294 PASS | 956/959 (99.69%) | 956/1,717 (55.68%) | 418/436 (95.87%) |

The expanded result remains above the owner-approved 70% function-body target.
The all-statements result is retained as a separate diagnostic and is not 70%.
These are isolated-unit measurements; they do not refresh the full mixed-suite
coverage result or constitute QA, Development, or instructor acceptance.

The clean summaries and test logs are retained in
[`measurement-baseline.json`](measurement-baseline.json),
[`measurement-expanded.json`](measurement-expanded.json),
[`tests-baseline.txt`](tests-baseline.txt), and
[`tests-expanded.txt`](tests-expanded.txt). CI saves matching per-run evidence
as build artifacts once the updated workflow completes on both Python versions.
