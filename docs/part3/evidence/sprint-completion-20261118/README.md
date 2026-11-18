# Sprint completion verification, 18-19 November 2026

Application freeze: `0d9adb39f3adcb85e75449c85900b4c283868ded`, tree
`37f15fa2d2acadae9072dd082da1816b3174cf69`. This is an AI-assisted technical
execution and independent blind review under the user's authorization to work
across assignees. It does not attribute this execution to another teammate.
Original requirements, case IDs, historical evidence and recorded owner scope
decisions remain visible.

## Initial frozen-source local results

- All **13 gates passed**: lint, formatting, dependency consistency, Django and
  database checks, applied migrations, migration consistency, static collection,
  mixed tests, canonical coverage data, text/XML/JSON coverage and separate timing.
- **727 distinct mixed tests:** 726 PASS, one expected timing SKIP. The skipped
  timing method passed separately without tracing. No failures or errors.
- Mixed statement coverage **2,994/3,380 (88.58%)**; branch coverage
  **821/1,000 (82.10%)**. XML and JSON agree for every covered line in all
  62 nonempty source files. Scripts are included in this mixed denominator.
- The clean frozen **415-method** isolated selection passed with zero database
  attempts and validated **208 source pins**. Method-attributed application
  function-body coverage is **1,547/1,740 (88.91%)**, above the recorded
  owner-approved 70% boundary. Its all-application-statements companion is
  **1,547/2,730 (56.67%)**; this is not an all-statements 70% claim.
- All original 288 baseline identities and all 294 previous expanded identities
  are retained. The new selection adds 121 methods to the previous expanded set.
  The original baseline is remeasured against the same current source, rather
  than compared with a historical, smaller denominator.
- A fresh blind reviewer independently reran 26 focused tests, checked original
  requirements and production paths, reproduced the availability defect before
  its correction, and reconciled the full mixed-run artifacts. No remaining
  concrete production blocker was established in that reviewed scope.

The full mixed run was executed on staged source: its manifest truthfully records
`a679ca47` with `git_dirty=true`. That source was then committed as `9b36871`;
the two integration merges retain its tree unchanged as `0d9adb39`. Clean
isolated measurements independently validated the frozen source pins afterward.
The mixed run is **not** relabelled as a clean `0d9adb39` execution. Clean CI
results will provide a separate revision-bound verification.

## Corrections and regression evidence

Inventory changes enforce eligibility, capacity, partial-save semantics and
allocation history under consistent locks. The Appendix B validators retain
existing storage widths and data. New SAD JSON endpoints retain session CSRF,
strict role/field/type checks and audited access-denial behavior. Concurrent
account/password/student edits preserve current protected state. Payment
references reject final-newline bypasses and invalid JSON scalar coercion.

Unicode receipts use bundled licensed fonts and shaping, preserve multiline
fields across pages, and clean up receipt-specific font registrations. Unsupported
code points are printed explicitly with an explanatory note. See the
[font sources, licenses, checksums and limitations](../../../../payments/fonts/README.md).

The final blind review also found that default HTML bed availability could list
a historical spare in a full room and beds in inactive hostels, while the API
correctly refused allocation. Two dedicated database regressions failed before
the fix and passed afterward. Occupied, Maintenance and unfiltered inventory
views retain their inventory scope.

Browser preparation exposed duplicate confirmation dialogs: a form-level
confirmation was handled on both click and submit. The submitter/form message
now prompts once on actual submission, while non-submit controls retain their
click behavior. Real browser cancel/accept verification is recorded separately.

PR #89's proposed XML-only short-path mapping was independently shown to make
XML disagree with JSON for actual Windows 8.3 source paths. The replacement
retains raw data and creates one canonical-path data copy **before all three
exports**. A real short-path regression verifies matching line/branch results,
selected test contexts, distinct same-named modules and unchanged raw evidence.
Existing-test-database protections remain in place.

## Reproduction

Install the pinned development requirements against an isolated MySQL `hms`
environment and apply migrations. Use synthetic data and run database suites
serially. Do not replace an existing `test_hms` database.

```powershell
python scripts/run_checks.py --output-dir test-results/verification-NEW
python docs/part3/evidence/hms19-unit-review-20261113/reproduce.py --scope docs/part3/evidence/sprint-completion-20261118/scope-baseline.json --output-dir test-results/unit-baseline-NEW
python docs/part3/evidence/hms19-unit-review-20261113/reproduce.py --scope docs/part3/evidence/sprint-completion-20261118/scope-expanded.json --output-dir test-results/unit-expanded-NEW
python scripts/part3/check_unit_coverage.py test-results/unit-expanded-NEW/summary.json --minimum 70
```

Use a clean checkout of the measured revision. The unchanged attribution harness
and `.coveragerc` remain the measurement method; the separate CI gate applies the
[recorded owner boundary](../hms19-function-body-boundary-20261113.md).
Imports, shared setup and database tests receive no unit credit.

## Durable evidence and remaining execution

- [Technical results, source pins, file metrics and missing lines](technical-verification.json)
- [727 mixed JUnit identities and outcomes](mixed-junit-outcomes.json)
- [Clean 288-method baseline attribution](isolated-baseline-summary.json)
- [Clean 415-method expanded attribution](isolated-expanded-summary.json)
- [Frozen baseline](scope-baseline.json) and [expanded selection](scope-expanded.json)

## Completed operational verification and final-source boundary

The [browser/security package](browser-security/README.md) retains all 12 actual
Windows/Fedora browser workflows, 228 observations/screenshots, 36 exports,
269 canonical source/font pins, genuine 901.003-second idle expiry, authenticated
ZAP output and actual deployment-check warnings. The
[assisted finding triage](browser-security/security/qa-development-triage.md)
accepts bounded baseline-procedure completion while preserving the Medium
development-static-404 observation and all lower findings. This is not deployment
approval.

Both [full load scenarios](operations/load-results.json) passed with 50 real
participants each measured for at least 600 seconds: baseline 28,952 HTTP
transactions (maximum 1,599 ms), volume 28,806 (maximum 1,519 ms) on 5,000
students/2,000 beds. Zero errors; every HTTP transaction was under two seconds.
The compressed raw CSVs are retained and independently reconciled.

The [fresh recovery](operations/recovery-results.json) demonstrated a natural
daily trigger, exact populated restore and 17 zero-violation consistency checks.
The separate browser-source backup was read-only. Its temporary task/server were
removed; the existing daily task was preserved. This demonstrates one real
trigger, not an ongoing daily schedule for the temporary browser instance.

These operational runs retain their actual `0d9adb39` attribution and hashes.
Only two helpers changed afterward: the recovery report now correctly describes
read-only backup without falsely assuming the source is empty; the pre-existing
original-checkout seven-line change hiding backup child-process windows is
preserved. Independent review confirmed no application/model/view/service,
template, asset, dependency or load-harness change. All 32 recovery-safety checks
passed after that delta. Final clean regression/coverage and CI are recorded
separately; raw observations are not relabelled with a later helper hash.

The real 19 November 08:00-20:00 IST availability observer is installed remotely
and remains PENDING until its actual window completes. An automated or owner
observation supplies no invented guide, QA, PO or instructor signature. The
[current assessment](../../Final_Assessment_20261119.md) distinguishes the owner's
tracking exceptions from unmet original course acceptance and submission rules.
