# HMS-17 Student and Hostel Validation Evidence

GitHub issue: #39  
Evidence scope: Student management, hostel management, Warden usability, Linux runtime and responsive mobile-viewport checks.

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

The owner execution record says eight assigned cases were exercised on 7 November. The source manual record is retained in the manual execution record. This table separates that owner-reported result from the case-level evidence disposition.

| Test Case | Owner-reported result | QA evidence disposition |
|---|---|---|
| TC-STU-01 — Student Registration | PASS | NOT RUN: no case-specific registration result or screenshot was located in the reviewed evidence. The owner summary is preserved as an unverified report. |
| TC-STU-02 — Student Validation | PASS | OWNER PASS: duplicate-ID and mandatory-field screenshots are present; broader persistence checks still require case review. |
| TC-STU-03 — Student Search | PASS | OWNER PASS: full ID, partial name and hostel search screenshots are present. |
| TC-STU-04 — Update Student Details | PASS | OWNER PASS: update screenshot is present; the current-source automated companion asserts Student ID immutability. |
| TC-STU-05 — Student Deactivation | PASS | OWNER PASS: blocked-active-allocation and successful deactivation screenshots are present. |
| TC-HST-01 — Hostel and Room Creation | PASS | OWNER PASS (reported): no named case screenshot was found in the listed evidence. |
| TC-HST-02 — Bed Availability and Filtering | PASS | OWNER PASS: available-bed and filter screenshots are present. |
| TC-QUAL-01 — Warden Usability | PASS | PARTIAL: dashboard/navigation/Students/Beds page checks in Firefox and Edge are reported; the guide-based new-Warden task and five-minute timing are not recorded. |
| **Total** | **8 owner-reported cases** | **6 OWNER PASS, 1 PARTIAL, 1 NOT RUN** |

The OWNER PASS labels preserve the executor's observations and do not mean the entire Test Plan cases were independently accepted. Browser versions, exact participant experience, portability and SRS office-hours availability are not established by these runs.

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

### Warden Usability – Existing Evidence

- `TC-QUAL-01_Warden_Student_List.png`
- `TC-QUAL-01_Warden_Student_Search.png`

Additional Edge and Chrome desktop evidence is retained separately in the same screenshot directory.

## 6. Automated evidence files

No JUnit XML files are committed in this directory. The six-suite 5 November result remains an owner-reported summary with the dirty-tree limitation above. The separate [retained 7 November CI extraction](../issue37/ci-methods.json) supplies exact method outcomes on `70c9fe2`, with source JUnit hashes and job links; it is not the missing historical raw XML or a new manual run.

The original full verification output is retained locally under:

`test-results/20261105T084741151581Z/`

## 7. Follow-up publication and technical review – 8 November 2026

The [PR #66 follow-up](followup-20261108.md) indexes additional screenshot observations and the complete original PR #58 CI artifacts with [source-bound raw hashes](followup-20261108.json).

The historical sections above retain their original dates and revisions. The new Edge-labelled registration image is a student-list result; the allocation image shows a success message and Active row. Desktop Chrome dashboard/student/bed pages are also present. Capture date/build/exact browser versions were not recorded for those earlier screenshots.

The same technical review accepts S1-07 and S2-07 for their historical automated integration scope, using raw 7 November execution and unchanged relevant source, without requiring an artificial new run. Original HMS-17 dispositions remain six OWNER PASS / one PARTIAL / one NOT RUN. #39 remains OPEN; the earlier captures do not complete the original registration/guide/quality requirements.

## 8. Linux runtime and Warden walkthrough – 9 November 2026

A Linux runtime walkthrough was performed using Ubuntu under WSL2 on Windows.

### Environment

- Operating system: Ubuntu 26.04.1 LTS under WSL2.
- Python: 3.14.4.
- Django: 5.2.18.
- Database: MySQL 8.4.11.
- Application URL used locally: `http://127.0.0.1:8000/`.
- Browser: Mozilla Firefox.
- Account role: Warden.
- Warden account used: `linux_warden`.
- Test data: Synthetic Linux demonstration data.

The application was started inside Ubuntu using Django's development server bound to `0.0.0.0:8000`. The application responded successfully inside WSL2. This evidence demonstrates a local Linux/WSL2 runtime check; it does not establish deployment on a separate production Linux server.

### Captured screenshots

The following screenshots are retained in `Screenshot/`:

- `TC-LINUX-01_Login_Page_Firefox.png`
- `TC-LINUX-02_Admin_Dashboard_Firefox.png`
- `TC-LINUX-03_Student_List_Firefox.png`
- `TC-LINUX-04_Bed_Availability_Firefox.png`
- `TC-QUAL-01_Linux_Warden_Dashboard.png`
- `TC-QUAL-01_Linux_Warden_Student_List.png`
- `TC-QUAL-01_Linux_Warden_Bed_Availability.png`

### Recorded Warden walkthrough

The video walkthrough is retained at:

`docs/part3/evidence/issue39/recording/TC-QUAL-01_Linux_Warden_Walkthrough.mp4`

The recording shows the Warden dashboard, student list, allocations, payments, occupancy report and bed availability. It also shows changing the bed availability filter from Available to Occupied and viewing the filtered results.

The allocation and payment records had been created before recording began. The recording demonstrates viewing those records and navigating the corresponding pages; it does not show their original creation steps.

This walkthrough is supplementary interface evidence. It does not establish the timed first-use task by a new Warden using the one-page guide.

## 9. Responsive mobile-viewport testing – 9 November 2026

Responsive layout checks were performed using Chrome DevTools Device Mode with the iPhone 14 device profile.

### Test configuration

- Browser: Google Chrome on Windows.
- Testing method: Chrome DevTools mobile-device emulation.
- Device profile: iPhone 14.
- Viewport: 390 × 844.
- Orientation: Portrait.
- Application: Linux-hosted Warden application accessed through Windows localhost forwarding.
- Account role: Warden.

This is responsive mobile-viewport testing, not testing on a physical iPhone or a real mobile browser.

### Screenshots

The following screenshots are retained in `Screenshot/`:

- `TC-QUAL-01_Mobile_Warden_Dashboard.png`
- `TC-QUAL-01_Mobile_Warden_Student_List.png`
- `TC-QUAL-01_Mobile_Bed_Availability_Filters.png`

### Observed results

| Page | Result | Observation |
|---|---|---|
| Warden Dashboard | PASS | Navigation wraps into multiple rows and dashboard cards stack vertically within the mobile viewport. |
| Student List | PASS | Search controls are visible and the table columns can be accessed using the horizontal scrollbar. |
| Bed Availability | PASS | Filter controls stack vertically and remain visible and usable in the mobile viewport. |

The horizontal scrollbar on the Student List is intentional: it allows access to table columns that do not fit within the narrow viewport. It is not recorded as a defect.

These results apply only to the three pages and viewport configuration listed above. They do not establish complete mobile functionality, physical-device compatibility or the full SRS browser portability matrix.

## 10. Current scope and limitations

The collected evidence provides separate automated, manual browser, Linux runtime and responsive viewport observations.

- Automated evidence covers the Student and Hostel test suites and repository verification.
- The original manual case dispositions remain six OWNER PASS, one PARTIAL and one NOT RUN.
- Linux evidence demonstrates local WSL2 Ubuntu runtime operation and Warden page navigation.
- Responsive evidence demonstrates the dashboard, student list and bed availability pages at the iPhone 14 emulated viewport.
- The recording shows existing allocation/payment records and the related pages; it does not show the creation of those records.
- The new Warden guide-based task and five-minute timing are not established.
- The complete latest-two-version Chrome/Firefox/Edge compatibility matrix is not established.
- A physical mobile device/browser test is not established.
- A separate production Linux server deployment is not established.
- The SRS 99% availability target during 08:00–20:00 working hours has not been measured.

These observations must not be interpreted as whole-plan acceptance or final HMS-17 approval. Issue #39 remains OPEN until its outstanding acceptance conditions and reviews are addressed.
