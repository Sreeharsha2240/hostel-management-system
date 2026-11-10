# HMS-17 remaining regression execution — 10 November 2026

This follow-up closes four regression evidence gaps and records a fresh Warden
registration. It does **not** waive the outstanding original compatibility or
availability requirements. The owner-authorized tracking closure below preserves
those unmet conditions explicitly.

## Source and environment

- Base: `65d6c1233b1b184858b36ff93cd32e440534ebbb`; dirty worktree containing
  `students/test_issue39_regressions.py` and these evidence files. Source hashes
  and raw result hashes are retained in `manifest.json`.
- Windows 11 build 26300; Python 3.14.0, Django 5.2.19, mysqlclient 2.3.1,
  MySQL 8.0.46. New isolated MySQL data directory; loopback port 3307,
  database `hms_issue39`, separate Django-created `test_hms_issue39`.
- Browser: connected desktop Chrome, exact version not established. Local
  Django server at `http://127.0.0.1:8017`; no production or physical-phone claim.
- Synthetic users and records only. Credentials and database files are kept in
  ignored `.tmp`, excluded from publication.

## Executed case results

| Case | Actual observations | Disposition |
|---|---|---|
| TC-STU-01 | Warden submitted `HMS1700000001`, all mandatory fields, and saw `Student HMS1700000001 registered successfully.` The new Active row persisted after browser reload. | OWNER PASS; fresh browser companion to retained original evidence |
| TC-REG-S1-05 | 60 beds in target hostel/floor/type: one occupied, one maintenance, 58 available; separate nonmatching hostel. Applied all four selectors in UI. Page 1 had 50 matching Available rows and rendered Next retained every query parameter. Clicked Next: eight matching rows, Page 2 of 2, all selector values retained. Excluded `F00-A`, `F00-B`, and other-hostel rows. | OWNER PASS |
| TC-REG-S1-06 | Six empty create/edit submissions show field errors; every editable stored field of the original student, hostel and room remains equal; student/hostel/room/bed/audit counts unchanged after each request. | OWNER PASS |
| TC-REG-S1-08 | Injected failure **after an actual audit write** in student creation, room/automatic-bed creation and student deactivation. Entity/bed/audit counts remain unchanged and original student stays Active after each failure. | OWNER PASS |
| TC-REG-S2-06 | Warden edit picker contained unlinked Student accounts only, excluding staff and the other linked account. Saved `hms17-student` to own profile, saw success, reopened edit and verified selected link persisted. Registration picker then excluded that linked account. Signed out and authenticated as the linked Student; My Records showed only own profile/bed/fee. Other fixture name, ID and hostel were absent. Existing passing self-service methods separately exercise own/other payments and picker boundaries. | OWNER PASS for combined browser and automated evidence |

`filters-page1.json` / `filters-page2.json` preserve actual rendered rows,
selectors, URLs and Next query. Registration and isolation `.txt` files preserve
the visible main-content observations. Screenshot capture repeatedly timed out;
no screenshot file or successful screenshot export is claimed.

## Verification

Command: `python scripts/run_checks.py --output-dir test-results/issue39-20261110`
with isolated database environment supplied privately by the local launcher.
All 12 gates passed. **211 distinct mixed methods: 210 PASS, one expected timing
SKIP**; separate uninstrumented timing PASS. This is not unit-only coverage or
an additional 211 planned cases. `run.json`, `test-results.txt`, `timing-smoke.txt`
and raw JUnit are retained under `checks/`.

An initial execution of the two new methods used an incorrect test-fixture role
(`Admin` instead of the model's `admin` enum); it produced nine subtest failures
before exercising the intended contracts. Correcting the fixture to
`User.Role.ADMIN` produced two passing methods and the successful full run.
This was a test setup error, not a discovered application defect.

## Remaining original acceptance conditions

The merged 9 November record already reports a new-Warden guide task completed
in 93 seconds and supports the eight original OWNER PASS dispositions. Its
missing guide revision, participant code and stopwatch timestamps stay disclosed;
no participant identity, new timing or independent signature is manufactured.

- **TC-QUAL-03:** full latest-two Chrome/Firefox/Edge matrix and real mobile
  execution remain NOT RUN for the complete case. Historical Windows and WSL2
  Linux observations remain valid within their recorded boundaries.
- **TC-QUAL-02:** working-hours >=99% availability remains NOT RUN. This new
  local execution occurred after 20:00 India time and cannot establish that
  requirement. It needs an identified agreed host, observation period, actual
  measurements and an explicit assessment.
- QA acceptance of owner results and any authorized scope changes remain
  separate decisions. No scoped closure exception is inferred from #38/#43.

## Owner-directed project-scope closure

On 10 November 2026, project owner `harsha2240` explicitly selected:
“Close with those documented project-scope exceptions.” The stated exceptions
were the full browser/real-phone matrix and working-hours availability, using
the same limited local-project tracking scope as HMS-16.

HMS-17/#39 is therefore complete for this owner-directed tracking scope. Original
TC-QUAL-02 and TC-QUAL-03 remain NOT RUN/unverified for their full criteria.
The owner decision is not QA sign-off, an instructor-approved Test Plan amendment,
or a claim of production readiness. Original whole-plan readiness remains
NOT READY/unverified where criteria are unmet. No human signature or independent
review is inferred from this execution or closure.
