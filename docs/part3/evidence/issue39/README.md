# HMS-17 Student and Hostel Validation Evidence

GitHub issue: #39  
Branch: `test/HMS-17-system-validation`

## 1. Automated test execution

The following Student and Hostel test suites were executed using Django's test runner on 5 November 2026.

| Module | Test suite | Tests | Passed | Failed |
|---|---|---:|---:|---:|
| Hostel | BedFilteringViewTests | 11 | 11 | 0 |
| Hostel | HostelManagementViewTests | 6 | 6 | 0 |
| Hostel | HostelModelBehaviorTests | 11 | 11 | 0 |
| Student | StudentManagementViewTests | 15 | 15 | 0 |
| Student | StudentModelTests | 6 | 6 | 0 |
| Student | StudentSelfServiceTests | 8 | 8 | 0 |
| **Total** | **6 suites** | **57** | **57** | **0** |

All 57 tests passed with no failures, errors or skips.

## 2. Full repository verification

A full verification run completed successfully on 5 November 2026.

- Verification gates: 12 passed.
- Test methods discovered: 190.
- Passed: 189.
- Failures: 0.
- Errors: 0.
- Skipped under coverage instrumentation: 1.
- Separate uninstrumented timing smoke test: passed.
- Statement coverage: 93%.
- Branch coverage: 87%.
- Lint, formatting, dependency checks, Django checks, migrations and static-file checks: passed.

The timing test is intentionally skipped while coverage instrumentation is active because instrumentation affects wall-clock measurements. It was executed separately and passed.

## 3. Execution environment and source

### Automated execution – 5 November 2026

- Operating system: Windows 11
- Python: 3.14.7
- Django: 5.2.18
- MySQL: 8.0.46
- Coverage.py: 7.16.2
- Recorded source commit: `8d60e83f1ce57ad99a2b2a22b3b5878f1390995b`

The automated verification metadata records `git_dirty: true`. Therefore, this run must not be described as a clean-working-tree execution.

### Manual execution – 7 November 2026

- Operating system: Windows
- Application URL: `http://127.0.0.1:8022/`
- Database: MySQL 8.0
- Browsers: Mozilla Firefox and Microsoft Edge
- Test accounts: Admin, Warden and Student demo accounts
- Test data: Synthetic demo data
- Tested source commit: `c9f30a48c6dc54ccaec799156f3e52fe7bc8666a`

## 4. Manual browser testing – HMS-17

Eight assigned test cases were manually executed through the application interface on 7 November 2026.

| Test Case | Description | Result |
|---|---|---|
| TC-STU-01 | Student Registration | PASS |
| TC-STU-02 | Student Validation | PASS |
| TC-STU-03 | Student Search | PASS |
| TC-STU-04 | Update Student Details | PASS |
| TC-STU-05 | Student Deactivation | PASS |
| TC-HST-01 | Hostel and Room Creation | PASS |
| TC-HST-02 | Bed Availability and Filtering | PASS |
| TC-QUAL-01 | Warden Usability | PARTIAL |
| **Total** | **8 test cases** | **7 PASS, 1 PARTIAL** |

The tests covered student registration, validation, search, updates, deactivation, hostel and room creation, bed availability filtering, and Warden interface usability.

For student deactivation, the system correctly prevented deactivation while an active bed allocation existed. Deactivation succeeded after the allocation was completed.

Warden usability checks covered the dashboard, module navigation, Students page and Beds page in Firefox and Edge. A timed walkthrough by a new warden using the one-page guide, including the five-minute target, was not recorded; TC-QUAL-01 is therefore PARTIAL.

## 5. Screenshot evidence

Manual execution screenshots are retained in the repository's `Screenshot/` directory.

### Student Management

- `TC-STU-02-duplicate-id-validation.png`
- `TC-STU-02-mandatory-field-validation.png`
- `TC-STU-03-search-by-full-student-ID.png`
- `TC-STU-03-search-by-partial-name.png`
- `TC-STU-03-search-by-hostel.png`
- `TC-STU-04-update-student-details.png`
- `TC-STU-05_deactivation_blocked_active_allocation.png`
- `TC-STU-05_student_deactivation_success.png`

### Hostel and Bed Management

- `TC-HST-02_available-beds-default.png`
- `TC-HST-02-hostel-floor-filter.png`
- `TC-HST-02_bed_filters.png`

### Warden Usability

- `TC-QUAL-01_Warden_Student_List.png`
- `TC-QUAL-01_Warden_Student_Search.png`

Additional Edge browser evidence is retained separately in the same screenshot directory.

## 6. Automated evidence files

The six JUnit XML reports in this directory provide detailed automated results for the Student and Hostel suites.

The original full verification output is retained locally under:

`test-results/20261105T084741151581Z/`

## 7. Scope and limitations

The automated and manual results provide separate evidence for HMS-17.

- Automated evidence covers the Student and Hostel test suites and repository verification.
- Manual execution evidence covers all eight assigned HMS-17 case IDs: seven met their recorded expectations and TC-QUAL-01 is PARTIAL as described above.
- Browser usability checks were performed in Mozilla Firefox and Microsoft Edge.
- No testing of the latest two versions of Chrome/Firefox/Edge as a compatibility matrix, Linux server portability, a real mobile client, or the SRS 99% availability target is claimed. These remain outside the evidence collected for this local miniproject run and must not be inferred from the Firefox/Edge checks.

Test-case statuses are recorded individually against their expected results and supporting execution evidence. HMS-15 review and approval status remains separate from HMS-17 execution status.
