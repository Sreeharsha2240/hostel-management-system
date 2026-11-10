# HMS-17 Manual Test Execution Record

- **GitHub Issue:** #39
- **Historical execution date:** 7 November 2026
- **Additional execution date:** 9 November 2026
- **Test data:** Synthetic demonstration data

## 1. Historical Windows manual execution – 7 November 2026

### Environment

- Operating system: Windows
- Application URL: `http://127.0.0.1:8022/`
- Database: MySQL 8.0
- Browsers: Mozilla Firefox and Microsoft Edge
- Test data: Synthetic demo data
- Tested source commit recorded in the original execution record: `c9f30a48c6dc54ccaec799156f3e52fe7bc8666a`

### Test execution results

| Test Case | Description | Owner-reported status |
|---|---|---|
| TC-STU-01 | Student Registration | PASS |
| TC-STU-02 | Student Validation | PASS |
| TC-STU-03 | Student Search | PASS |
| TC-STU-04 | Update Student Details | PASS |
| TC-STU-05 | Student Deactivation | PASS |
| TC-HST-01 | Hostel and Room Creation | PASS |
| TC-HST-02 | Bed Availability and Filtering | PASS |
| TC-QUAL-01 | Warden Usability | PASS |

The owner-reported summary is retained as historical information. The reviewed evidence disposition is not identical to the owner-reported status.

### Reviewed evidence disposition

| Test Case | Evidence disposition |
|---|---|
| TC-STU-01 | NOT RUN: no case-specific registration result or screenshot was located in the reviewed evidence. |
| TC-STU-02 | OWNER PASS: duplicate-ID and mandatory-field validation screenshots are present. |
| TC-STU-03 | OWNER PASS: full ID, partial name and hostel search screenshots are present. |
| TC-STU-04 | OWNER PASS: update screenshot is present; the current-source automated companion asserts Student ID immutability. |
| TC-STU-05 | OWNER PASS: blocked-active-allocation and successful deactivation screenshots are present. |
| TC-HST-01 | OWNER PASS (reported): no named case screenshot was found in the listed evidence. |
| TC-HST-02 | OWNER PASS: available-bed and filter screenshots are present. |
| TC-QUAL-01 | PARTIAL: dashboard/navigation/Students/Beds page checks were reported; the guide-based new-Warden task and five-minute timing were not recorded. |

**Reviewed total: 6 OWNER PASS, 1 PARTIAL and 1 NOT RUN.**

The original owner-reported result of seven passes and one partial is preserved as a historical report, not treated as the reviewed evidence disposition.

## 2. Additional Linux runtime execution – 9 November 2026

### Environment

- Operating system: Ubuntu 26.04.1 LTS under WSL2 on Windows 11.
- Python: 3.14.4.
- Django: 5.2.18.
- Database: MySQL 8.4.11.
- Application URL: `http://127.0.0.1:8000/`.
- Browser: Mozilla Firefox.
- Account role: Warden.
- Warden username: `linux_warden`.
- Test data: Synthetic Linux demonstration data.

The application was run using Django's development server inside Ubuntu, bound to `0.0.0.0:8000`.

The application responded successfully inside WSL2. The root URL returned an HTTP 302 redirect to `/dashboard/`, as expected for the application. The listening socket was verified on `0.0.0.0:8000`.

### Observed execution

| Step | Action | Actual observation | Evidence |
|---|---|---|---|
| 1 | Open the application in Firefox | Login page displayed. | `TC-LINUX-01_Login_Page_Firefox.png` |
| 2 | Sign in to the application | Admin dashboard displayed in the Linux environment. | `TC-LINUX-02_Admin_Dashboard_Firefox.png` |
| 3 | Open Student List | Student list page displayed. | `TC-LINUX-03_Student_List_Firefox.png` |
| 4 | Open Bed Availability | Bed availability page displayed. | `TC-LINUX-04_Bed_Availability_Firefox.png` |
| 5 | Sign in using the Linux Warden account | Warden dashboard and Warden-specific navigation displayed. | `TC-QUAL-01_Linux_Warden_Dashboard.png` |
| 6 | Open the Warden Student List | Student list displayed under the Warden account. | `TC-QUAL-01_Linux_Warden_Student_List.png` |
| 7 | Open Warden Bed Availability | Bed availability page displayed. | `TC-QUAL-01_Linux_Warden_Bed_Availability.png` |

### Linux Warden walkthrough recording

Recording:

`docs/part3/evidence/issue39/recording/TC-QUAL-01_Linux_Warden_Walkthrough.mp4`

The recording shows the following sequence:

1. Warden dashboard.
2. Student list.
3. Hostel allocations page with an existing allocation record.
4. Payments page with an existing payment record.
5. Occupancy report.
6. Bed availability with the Available filter.
7. Changing the filter to Occupied.
8. Viewing the filtered occupied-bed result.

The allocation and payment records had been created before the recording started. The recording demonstrates viewing those records and navigating the pages; it does not demonstrate their creation.

### Linux execution scope and limitations

This execution demonstrates application operation in a local Ubuntu WSL2 environment. It does not establish deployment on a separate production Linux server.

The recording is supplementary Warden interface evidence. It does not establish the timed first-use task by a new Warden using the one-page guide or the five-minute completion requirement.

## 3. Additional responsive mobile-viewport execution – 9 November 2026

### Environment

- Browser: Google Chrome on Windows.
- Testing method: Chrome DevTools Device Mode.
- Device profile: iPhone 14.
- Viewport: 390 × 844.
- Orientation: Portrait.
- Application: Linux-hosted application accessed through Windows localhost forwarding.
- Account role: Warden.

**Testing classification:** Responsive mobile-viewport emulation. This was not a physical iPhone test or a real mobile-browser execution.

### Test results

| Page | Action / observation | Expected result | Actual result | Status |
|---|---|---|---|---|
| Warden Dashboard | Open dashboard in iPhone 14 emulation. | Dashboard and navigation should fit the mobile viewport without layout breakage. | Navigation wraps into multiple rows; dashboard cards stack vertically and remain visible. | PASS |
| Student List | Open Students page and inspect search and table. | Search controls should be accessible and table content should remain accessible. | Search field and button are visible. The table uses a horizontal scrollbar to access columns beyond the viewport. | PASS |
| Bed Availability | Open Bed Availability and inspect filters. | Filter controls should fit the mobile viewport and remain usable. | Filters stack vertically and controls and Apply Filters button are visible. | PASS |

### Screenshot evidence

- `Screenshot/TC-QUAL-01_Mobile_Warden_Dashboard.png`
- `Screenshot/TC-QUAL-01_Mobile_Warden_Student_List.png`
- `Screenshot/TC-QUAL-01_Mobile_Bed_Availability_Filters.png`

The horizontal scrollbar on the Student List is intentional and allows the user to access the remaining table columns. It is not treated as a defect.

### Mobile testing limitations

- Only the three listed Warden pages were checked.
- The viewport was emulated using Chrome DevTools.
- No physical mobile device was used.
- No separate mobile operating system/browser compatibility result is claimed.
- The results do not establish the complete SRS browser portability matrix.

## 4. Overall execution summary

The original 7 November manual execution and the additional 9 November Linux and responsive viewport checks are separate execution records.

| Evidence group | Result |
|---|---|
| Original 7 November manual cases | 6 OWNER PASS, 1 PARTIAL, 1 NOT RUN (reviewed evidence disposition) |
| Linux WSL2 runtime | Warden and application pages observed; supplementary walkthrough recorded |
| Responsive mobile viewport | 3 page checks PASS at iPhone 14 emulated viewport |

The additional Linux and responsive checks do not change the historical status totals for the eight original manual test cases.

**Overall HMS-17 status: PARTIAL.**

## 5. Outstanding conditions

The following conditions remain unestablished by the execution records above:

- Complete student registration sequence with case-specific evidence.
- Timed first-use task by a new Warden using the one-page guide, including the five-minute completion requirement.
- Complete latest-two-version Chrome, Firefox and Edge compatibility matrix.
- Physical mobile-device/browser execution.
- Separate production Linux server operation.
- SRS 99% availability target measurement during 08:00–20:00 working hours.

These conditions must be tested and recorded before claiming full HMS-17 acceptance.

## Additional usability execution — 9 November 2026

A separate owner-reported first-use walkthrough was completed using the
one-page Warden guide. The task was to register a student and successfully
allocate a bed. The owner confirms completion in less than five minutes,
against the SRS target of 300 seconds.

The exact elapsed time and guide revision/version were not retained.
The participant's non-identifying code and detailed assistance/error
observations were also not retained.

See [usability-walkthrough-20261109.md](usability-walkthrough-20261109.md).

This additional result does not change the historical 7 November PARTIAL
result. It records an owner-reported pass for the timed task only.
TC-QUAL-01 remains PARTIAL overall pending the missing execution details
and remaining browser/platform compatibility evidence.