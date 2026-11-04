# Owned Part 3 defects and retest evidence

Owner: Devansh Gupta (`DevaOnL`). Measured **4 November 2026**, clean candidate
`6e349f2c07630e72b9151a575685d462e63cbc40`, tree
`558190f7852283743ab9e20a4c9b3c9b99d0f806`. The subsequent evidence commit
changes documentation only. Existing PR #44 carries these changes; actual
independent teammate review and accepted-build/report integration remain pending.

| Issue | Original requirement | Correction and current evidence |
|---|---|---|
| [#45](https://github.com/Sreeharsha2240/hostel-management-system/issues/45) | SRS REQ-23 p.14 / Appendix B p.21: Hostel / Room / Bed | Payment HTML/JSON/CSV include the selected allocation's bed label. Regression tests cover transfer, released history, cancelled-only/unassigned records, filters, financial totals and format parity. Browser output reconciles against MySQL. |
| [#46](https://github.com/Sreeharsha2240/hostel-management-system/issues/46) | SAD 4.5 p.19: transfer/release confirmation dialogs | Form submit handlers retain confirmation after invalid input. Actual Edge dialogs were dismissed with zero POSTs and unchanged allocation/bed state, then accepted with one POST and one attributed action each. Release cancellation uses Enter from the date field. Creation requires no dialog. |
| [#47](https://github.com/Sreeharsha2240/hostel-management-system/issues/47) | SRS section 7 p.18: DD-MM-YYYY displayed dates | Allocation list/history display allocated/vacated dates explicitly; absent vacated date remains an em dash. Browser and counterordered-date regression agree; JSON remains ISO. |

## Verification

- Original-production negative controls fail specifically for missing Bed,
  confirmation handlers and formatted dates. Restoring the fixes makes the same
  regressions pass. Raw negative logs remain private; hashes and labels are in
  [retest.json](retest.json).
- Focused allocation/payment/report/system-journey checks: **63 passed**.
- Clean full runner: **12 gates passed**, **189 methods**, zero failures/errors,
  one expected coverage timing skip followed by a passing uninstrumented timing
  run. [JUnit outcomes](coverage-junit-summary.json) retain method identities.
- **32** offline recovery-safety methods passed. No live data was seeded or
  restored. Database suites and browser execution ran serially on disposable
  `test_hms`; its database was removed afterward.
- Actual Edge/Playwright browser run: **passed**, including native dialogs,
  dates, report formats, receipts, payments and integration. All **20** committed
  allocation timings passed the under-three-second gate; overlapping conflict
  requests produced one winner. [Browser evidence](browser-results.json)
  retains synthetic rows, native dialog observations and database checks.
- Fresh configured mixed coverage: **1,584/1,674 statements (94.62%)**,
  **342/392 branch outcomes (87.24%)**, **93.22% combined**. All **49** nonempty
  XML file rows reconcile with JSON. See the separate
  [Code](../../Code_Coverage_Report.md) and
  [Branch](../../Branch_Coverage_Report.md) Coverage Reports and
  [coverage reproduction notes](coverage-notes.md).

The strict 16 database-free helpers and proposed 37-method component subset
passed separately. Both are nonexhaustive diagnostics. The original Test Plan
allows Django model/form/view component units; the 1.96% narrow result does not
classify or measure all such units. The broader classification and SRS 70%
application-logic target remain undetermined under existing #41/#42, with
Vaishnavi retaining Unit Test Report ownership. No duplicate issue is needed.

A separate blind review found the self-service `/my-records/` template still
uses `d M Y`. [#48](https://github.com/Sreeharsha2240/hostel-management-system/issues/48)
tracks that defect under Sreeharsha's existing HMS-12 ownership; this work does
not claim application-wide date compliance or implement his module changes.

## Corrections, limits and reproduction

The earlier TC-RPT-01 complete-PASS claim omitted Bed and is superseded by these
schema/output checks. Historical issue40/issue42 JSON remains unchanged.
Browser TC-ALC-05 remains PARTIAL for storage-failure injection; the current full
and focused suite's transfer rollback/same-transfer retry regression supplies
that step. Prior full load and populated recovery evidence describes its older
candidate only. Those workloads' student/bed routes and backup tools are
unchanged; no fresh full load, populated restore or live scheduler result is
claimed here. These fixes do not constitute complete system/RTM acceptance.

Use the documented MySQL environment and fresh ignored output directories.
Run the full checks and component coverage commands in the coverage notes.
Run browser verification serially with optional Playwright available through
`NODE_PATH` and Microsoft Edge installed:

```powershell
python scripts/part3/run_issue40_browser.py --output-dir test-results/owned-defects/<new-run>/browser
```

The browser wrapper refuses an existing `test_hms`. Preserve earlier evidence
and identify any database owner before starting a new run. Private raw artifacts
are hashed in the durable JSON; source manifests cover application, templates,
verification scripts and reference documents. No credentials or raw SQL dumps
are committed. Two invocation errors (a wrong initial journey label and optional
browser tooling path) were corrected before the passing runs and are recorded
in `retest.json`.
