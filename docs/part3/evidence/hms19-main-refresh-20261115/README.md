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

See `scope-baseline.json` and `scope-expanded.json` for the exact IDs and current
source pins. CI saves matching per-run summaries and test evidence as build
artifacts. Current metrics and the clean source revision will be recorded here
after the clean-commit rerun.
