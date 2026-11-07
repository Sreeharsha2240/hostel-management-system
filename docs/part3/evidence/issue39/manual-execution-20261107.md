# HMS-17 Manual Test Execution Record

- **GitHub Issue:** #39
- **Branch:** `test/HMS-17-system-validation`
- **Execution Date:** 7 November 2026
- **Tested Commit:** `c9f30a48c6dc54ccaec799156f3e52fe7bc8666a`
- **Application:** `http://127.0.0.1:8022/`
- **Browsers:** Mozilla Firefox, Microsoft Edge
- **Test Data:** Synthetic demo data

## 1. Test Execution Results

| Test Case | Description | Status |
|---|---|---|
| TC-STU-01 | Student Registration | PASS |
| TC-STU-02 | Student Validation | PASS |
| TC-STU-03 | Student Search | PASS |
| TC-STU-04 | Update Student Details | PASS |
| TC-STU-05 | Student Deactivation | PASS |
| TC-HST-01 | Hostel and Room Creation | PASS |
| TC-HST-02 | Bed Availability and Filtering | PASS |
| TC-QUAL-01 | Warden Usability | PARTIAL |

## 2. Screenshot Evidence

Screenshots are stored in the repository's `Screenshot/` directory.

- Student validation, search, update and deactivation screenshots.
- Bed availability and filtering screenshots.
- Warden usability screenshots.
- Edge browser screenshot: `TC-QUAL-01_Edge_Student_Dashboard.png`

## 3. Overall Result

**8 test cases exercised – 7 passed, 1 partial, 0 failed, 0 blocked.**

TC-QUAL-01 is partial because no timed first-use walkthrough by a new warden using the one-page guide was recorded. The Firefox/Edge page checks do not establish the five-minute criterion or the broader browser/platform/availability matrix.

**Final Status: PARTIAL**
