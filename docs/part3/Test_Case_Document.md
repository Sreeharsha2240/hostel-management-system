
# HMS – Test Case Document and Requirements Traceability Matrix

## 1. Document Information

| Field | Details |
|---|---|
| Project | Hostel Management System (HMS) |
| Document | Test Case Document and RTM |
| Baseline | Software Test Plan dated 07-10-2026 |
| Revision | Part 3 – Updated Test Case Document |
| Date | 05-11-2026 |
| Original Test Cases | 33 |
| Requirements | 24 Functional + 12 Non-Functional |
| Test Data | Synthetic data only |

## 2. Purpose

This document updates the original Software Test Plan by maintaining the existing test cases, improving test coverage and mapping test cases to project requirements.

The document provides:
- Detailed test case descriptions.
- Expected test results.
- Test ownership.
- Requirements Traceability Matrix (RTM).
- Test execution status and evidence references.

All 33 original test case IDs are retained.

## 3. Testing Scope

The testing scope includes:

1. Authentication and session management.
2. User administration.
3. Student management.
4. Hostel, room and bed management.
5. Student allocation and transfers.
6. Payment processing and receipts.
7. Occupancy and payment reports.
8. Role-based access and security.
9. Performance and scalability.
10. Backup and recovery.
11. Browser compatibility and usability.

## 4. Test Environment

| Component | Planned Configuration |
|---|---|
| Programming Language | Python 3.11+ |
| Framework | Django 5.x |
| Database | MySQL 8.0 |
| Operating System | Windows 10+ / Ubuntu 20.04+ |
| Browsers | Chrome, Firefox, Edge |
| Functional Testing | Django Test Runner |
| Browser Automation | Selenium |
| API Testing | Postman |
| Security Testing | OWASP ZAP |
| Performance Testing | Apache JMeter |

The project CI configuration also uses MySQL 8.4 with Python 3.11 and 3.14. This differs from the original MySQL 8.0 baseline and should be considered when interpreting CI results.

Only synthetic test data is to be used. Real student information and credentials must not be included in test evidence.

## 5. Test Execution Summary

### 5.1 Focused Students and Hostels Test Execution

| Field | Result |
|---|---|
| Command | `python manage.py test students hostels --noinput` |
| Tested Commit | `649a4a5abe611c7970da3006902c64a505f27c46` |
| Tests Discovered | 56 |
| Passed | 56 |
| Failed | 0 |
| Errors | 0 |
| Execution Time | 26.699 seconds |
| Result | SUCCESS |

This execution covered the Students and Hostels application test suites only.

### 5.2 Complete Verification Run

| Field | Result |
|---|---|
| Command | `python scripts/run_checks.py` |
| Tested Commit | `649a4a5abe611c7970da3006902c64a505f27c46` |
| Python Version | 3.14.7 |
| Django Version | 5.2.18 |
| MySQL Version | 8.0.46 |
| Tests Discovered | 185 |
| Passed | 184 |
| Skipped | 1 |
| Failed | 0 |
| Errors | 0 |
| Test Execution Time | 51.393 seconds |
| Statement Coverage | 94.28% |
| Branch Coverage | 85.57% |
| Overall Coverage | 92.63% |
| Timing Smoke Test | Passed (1.989 seconds) |
| Result | SUCCESS |

The verification runner completed all 12 steps successfully, including linting, formatting, dependency checks, Django checks, migration checks, static-file checks, automated tests, coverage reports, and the timing smoke test.

Evidence directory:
`test-results/20261105T042453664905Z`

The run summary recorded `success: true`, with zero failures and zero errors.

**Important:** These automated test results do not establish that all 33 original test cases have individually passed. Individual test case statuses must be updated only when corresponding execution evidence is available. One automated test was skipped and is not counted as passed.

### 5.3 HMS-18 owner execution and evidence reconciliation

Devansh Gupta's contribution, reconciled **6 November 2026**, supplies the 13 original allocation, payment, report, performance and recovery case results. The linked observations were executed **5 November** on clean `0e358b4ce1fd02366184c7cb9c312b47dd093214` (tree `c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0`). [PR #50](https://github.com/Sreeharsha2240/hostel-management-system/pull/50) published this evidence and was merged by `harsha2240` on **5 November at 06:31:28 UTC** as `8d60e83f1ce57ad99a2b2a22b3b5878f1390995b`. No formal `APPROVED` review is recorded.

The 13 linked **OWNER PASS** statuses below replace their stale NOT RUN entries. They record observed owner execution against the submitted Test Plan, with **independent QA review of the case batch, priorities, method mappings, entry criteria and environment deviations still pending**. This update does not retroactively approve those entry criteria or accept the final submission build. Cases and statuses supplied by other owners are unchanged.

| Owned evidence | Observed result | Durable reference |
|---|---|---|
| Full mixed suite and focused checks | 190 methods: 189 PASS, one expected timing skip followed by a separate timing PASS; 71 focused methods and 32 recovery safety methods passed. These counts are not original cases or unit-only tests. | [Commands, environment and hashes](evidence/issue40-final/summary.json); [JUnit outcomes](evidence/issue40-final/junit-summary.json); [focused methods](evidence/issue40-final/focused-methods.json) |
| TC-ALC-01..06, TC-PAY-01..02, TC-RPT-01, TC-PERF-02 | Browser/HTTP/MySQL results include allocation, eligibility, transfer/release/history, payment receipts, required Bed and matching report formats; 20 committed allocations take 32.20–42.38 ms and overlapping conflicts preserve one winner. | [Browser observations](evidence/issue40-final/browser-results.json); [per-case actual results and defect/retest links](evidence/issue40-final/owner-cases.md) |
| TC-PERF-01 | 100 students / 80 beds; 50 users, each at least 600.106 seconds; 28,696 samples, zero errors, 99.99303% within two seconds. | [Full workload and retained failed attempt](evidence/issue40-final/load-results.json) |
| TC-PERF-03 | 5,000 students / 2,000 beds; 50 users, each at least 600.083 seconds; 29,096 samples, zero errors, every sample and search within two seconds. | [Full volume workload](evidence/issue40-final/load-results.json) |
| TC-OPS-01 | Naturally triggered daily sandbox backup, 5.379 seconds old; all 18 table counts/row/schema digests match after a separate populated restore. Live source and its installed daily task were preserved; owned resources were cleaned up. | [Recovery and cleanup](evidence/issue40-final/recovery-results.json); [reproduction](evidence/issue40-final/README.md) |

TC-ALC-05's raw browser result remains **PARTIAL** for fault injection; its linked, passing automated companion proves rollback and retry of the same transfer. The combined owner result records that qualification. The first volume attempt remains **FAIL** with 75 errors in 21,650 samples; the final volume result uses the complete unchanged-threshold rerun, not removal or relabelling of failed samples.

The [owner appendix](evidence/issue40-final/owner-cases.md) preserves original prerequisites, steps, expected and actual results, 14 SRS requirement mappings, source hashes and #45–#48 defect/retest references. The original plan has no per-case priorities; QA must review them rather than infer High-priority acceptance. Edge/Playwright in place of Selenium, MySQL 8.4.9 in place of 8.0, and loopback HTTP test flags remain declared deviations requiring review. Load and recovery figures describe their recorded source and host; they are not new measurements on this document's revision. All historical JSON remains unchanged. Whole-plan entry/exit criteria, integrated reporting and actual QA/Dev/PO approvals remain pending with #37/#38/#43.

### 5.4 Manual Browser Testing – HMS-17

Manual functional and usability testing for HMS-17 was performed on **7 November 2026** using the locally deployed Hostel Management System.

#### 5.4.1 Test Environment

| Field | Details |
|---|---|
| Execution Type | Manual Functional and Usability Testing |
| Application URL | http://127.0.0.1:8022/ |
| Operating System | Windows |
| Browsers | Mozilla Firefox and Microsoft Edge |
| Database | MySQL 8.0 |
| Test Data | Synthetic demo data |
| Accounts Used | Admin, Warden and Student demo accounts |
| Tested Commit | [Record verified commit hash] |

Firefox was used to capture the retained functional screenshots. The application was also accessed and tested in Microsoft Edge, with additional browser evidence captured separately. All three demo accounts (Admin, Warden and Student) were used during the testing process.

#### 5.4.2 Manual Test Execution Results

| Test Case ID | Test Scenario | Actual Result | Status |
|---|---|---|---|
| TC-STU-01 | Student Registration | Student record was created successfully using valid information. | PASS |
| TC-STU-02 | Student Validation | Duplicate Student ID and missing mandatory fields were correctly rejected with validation messages. | PASS |
| TC-STU-03 | Student Search | Full Student ID, partial name and hostel searches returned matching records. | PASS |
| TC-STU-04 | Update Student Details | Student contact information was updated and saved successfully. | PASS |
| TC-STU-05 | Student Deactivation | Deactivation was blocked while an active allocation existed. After completing the allocation, deactivation succeeded. | PASS |
| TC-HST-01 | Hostel and Room Creation | Hostel and room creation succeeded. Duplicate rooms and invalid capacities were rejected, and beds were generated automatically. | PASS |
| TC-HST-02 | Bed Availability and Filtering | Bed availability and filters for hostel, floor, room type and status were verified. | PASS |
| TC-QUAL-01 | Warden Usability | Dashboard, navigation, Students page and Beds page were checked for clarity and ease of use in Firefox and Edge. | PASS |

#### 5.4.3 Screenshot Evidence

Screenshots are retained in the repository's `Screenshot/` directory.

**Student Management**

- TC-STU-02: `TC-STU-02-duplicate-id-validation.png`
- TC-STU-02: `TC-STU-02-mandatory-field-validation.png`
- TC-STU-03: `TC-STU-03-search-by-full-student-ID.png`
- TC-STU-03: `TC-STU-03-search-by-partial-name.png`
- TC-STU-03: `TC-STU-03-search-by-hostel.png`
- TC-STU-04: `TC-STU-04-update-student-details.png`
- TC-STU-05: `TC-STU-05_deactivation_blocked_active_allocation.png`
- TC-STU-05: `TC-STU-05_student_deactivation_success.png`

**Hostel and Bed Management**

- TC-HST-02: `TC-HST-02_available-beds-default.png`
- TC-HST-02: `TC-HST-02-hostel-floor-filter.png`
- TC-HST-02: `TC-HST-02_bed_filters.png`

**Usability and Browser Evidence**

- TC-QUAL-01: `TC-QUAL-01_Warden_Student_List.png`
- TC-QUAL-01: `TC-QUAL-01_Warden_Student_Search.png`
- TC-QUAL-01: `TC-QUAL-01_Edge_Student_Dashboard.png`

#### 5.4.4 Overall Execution Summary

| Result | Count |
|---|---:|
| Total Test Cases | 8 |
| Passed | 8 |
| Failed | 0 |
| Blocked | 0 |
| Not Run | 0 |

**Overall Result: PASS**

All eight assigned HMS-17 test cases passed manual execution. The results are documented separately from the historical automated test results in Sections 5.1 and 5.2. Supporting screenshots are retained in the `Screenshot/` directory.

## 6. Test Case Status Definitions

| Status | Meaning |
|---|---|
| NOT RUN | Test has not been individually executed or verified. |
| PASS | Actual result matches the expected result. |
| OWNER PASS | The owner observed the expected behavior on the linked recorded source; independent QA case/scope/entry acceptance is pending. |
| FAIL | Actual result differs from the expected result. |
| BLOCKED | Execution cannot proceed due to an identified blocker. |
| PARTIAL | Some expected behavior passed, but an identified portion remains unverified. |


## 7. Detailed Test Cases

### 7.1 Authentication and User Management

| Test Case ID | Requirement | Test Scenario | Expected Result | Owner | Status |
|---|---|---|---|---|---|
| TC-AUTH-01 | REQ-1 | Login using valid credentials. | User is authenticated and redirected to the appropriate dashboard. | Sreeharsha | PASS |
| TC-AUTH-02 | REQ-2 | Login using invalid credentials. | Login is rejected and a generic error message is displayed. | Sreeharsha | PASS |
| TC-AUTH-03 | REQ-2, NFR-12 | Enter an incorrect password five consecutive times. | Account is temporarily locked. Login becomes available again after 15 minutes. | Sreeharsha | PASS |
| TC-AUTH-04 | REQ-3, NFR-9 | Logout and test session timeout. | User session ends and protected pages cannot be accessed without authentication. | Sreeharsha | PASS |
| TC-USR-01 | REQ-4 | Administrator creates, updates and manages user accounts. | Only authorized administrators can perform user-management operations. | Sreeharsha | PASS |

### 7.2 Student Management

| Test Case ID | Requirement | Test Scenario | Expected Result | Owner | Status |
|---|---|---|---|---|---|
| TC-STU-01 | REQ-5 | Register a student using valid information. | Student record is created successfully. | Vaishnavi | PASS |
| TC-STU-02 | REQ-5, REQ-6 | Submit invalid or duplicate student information. | Invalid or duplicate records are rejected with validation messages. | Vaishnavi | PASS |
| TC-STU-03 | REQ-7 | Search students using student ID or supported search fields. | Matching student records are displayed. | Vaishnavi | PASS |
| TC-STU-04 | REQ-8 | Update an existing student's information. | Changes are saved correctly and the student ID remains unchanged. | Vaishnavi | PASS |
| TC-STU-05 | REQ-9, NFR-5 | Deactivate an existing student. | Student is deactivated while the existing record is retained. | Vaishnavi | PASS |


### 7.3 Hostel and Room Management

| Test Case ID | Requirement | Test Scenario | Expected Result | Owner | Status |
|---|---|---|---|---|---|
| TC-HST-01 | REQ-10, REQ-11 | Add a hostel and create rooms with valid details. | Hostel and room records are created successfully. Invalid details are rejected. | Vaishnavi | PASS |
| TC-HST-02 | REQ-12, REQ-13 | Create beds and view bed availability. | Beds are created correctly and availability excludes occupied or unavailable beds. | Vaishnavi | PASS |

### 7.4 Allocation Management

| Test Case ID | Requirement | Test Scenario | Expected Result | Owner | Status |
|---|---|---|---|---|---|
| TC-ALC-01 | REQ-14 | Allocate an available bed to an eligible student. | Allocation is completed successfully. | Devansh | [OWNER PASS](evidence/issue40-final/owner-cases.md#tc-alc-01--allocate-available-bed) |
| TC-ALC-02 | REQ-15 | Attempt to allocate an already occupied bed. | The system rejects the allocation. | Devansh | [OWNER PASS](evidence/issue40-final/owner-cases.md#tc-alc-02--block-allocation-of-occupied-bed) |
| TC-ALC-03 | REQ-15 | Attempt a second active allocation for the same student. | The system prevents duplicate active allocations. | Devansh | [OWNER PASS](evidence/issue40-final/owner-cases.md#tc-alc-03--block-second-allocation-for-a-student) |
| TC-ALC-04 | REQ-16 | Allocate a student to an incompatible hostel type. | The system rejects the invalid allocation. | Devansh | [OWNER PASS](evidence/issue40-final/owner-cases.md#tc-alc-04--gender-and-hostel-type-mismatch) |
| TC-ALC-05 | REQ-17 | Transfer a student from one allocation to another. | Transfer is processed correctly and allocation records remain consistent. | Devansh | [OWNER PASS](evidence/issue40-final/owner-cases.md#tc-alc-05--transfer-student) |
| TC-ALC-06 | REQ-18, REQ-19 | Release a student's allocation. | Bed availability is updated and allocation history is retained. | Devansh | [OWNER PASS](evidence/issue40-final/owner-cases.md#tc-alc-06--release-allocation-and-history) |

### 7.5 Payment and Reporting

| Test Case ID | Requirement | Test Scenario | Expected Result | Owner | Status |
|---|---|---|---|---|---|
| TC-PAY-01 | REQ-20, REQ-21 | Record a valid payment. | Payment record is saved and the appropriate receipt is generated. | Devansh | [OWNER PASS](evidence/issue40-final/owner-cases.md#tc-pay-01--record-payment-and-receipt) |
| TC-PAY-02 | REQ-22 | Check the payment status of a student. | Correct payment status is displayed. | Devansh | [OWNER PASS](evidence/issue40-final/owner-cases.md#tc-pay-02--payment-status) |
| TC-RPT-01 | REQ-23 | Generate occupancy and payment-status reports. | Reports display accurate information. | Devansh | [OWNER PASS](evidence/issue40-final/owner-cases.md#tc-rpt-01--occupancy-report) |


### 7.6 Security Testing

| Test Case ID | Requirement | Test Scenario | Expected Result | Owner | Status |
|---|---|---|---|---|---|
| TC-SEC-01 | REQ-4, NFR-7 | Attempt to access restricted functions using different user roles. | Users can access only functions permitted by their assigned roles. | Sreeharsha | PASS |
| TC-SEC-02 | REQ-24, NFR-8 | Login as a student and attempt to view another student's information. | Student can access only their own permitted information. | Sreeharsha | PASS |
| TC-SEC-03 | NFR-10 | Submit SQL injection and script injection inputs. | Malicious input is safely handled and does not execute. | Sreeharsha | PASS |
| TC-SEC-04 | NFR-6 | Inspect password storage and password policy enforcement. | Passwords are stored securely and policy requirements are enforced. | Sreeharsha | PASS |
| TC-SEC-05 | NFR-10 | Submit a request without valid CSRF protection. | The request is rejected. | Sreeharsha | PASS |
| TC-SEC-06 | NFR-12, NFR-9 | Check HTTPS and secure session-cookie configuration. | Secure transport and cookie settings meet deployment requirements. | Sreeharsha | PARTIAL |
| TC-SEC-07 | NFR-11 | Perform important administrative operations and inspect audit logs. | Relevant actions are recorded in audit logs. | Sreeharsha | PASS |

### 7.7 Performance Testing

| Test Case ID | Requirement | Test Scenario | Expected Result | Owner | Status |
|---|---|---|---|---|---|
| TC-PERF-01 | NFR-1 | Measure application response time under the planned load. | Response time meets the defined performance target. | Devansh | [OWNER PASS](evidence/issue40-final/owner-cases.md#tc-perf-01--response-time-under-load) |
| TC-PERF-02 | NFR-2 | Measure allocation processing time and test concurrent allocation requests. | Allocation remains correct and consistent under concurrent requests. | Devansh | [OWNER PASS](evidence/issue40-final/owner-cases.md#tc-perf-02--allocation-time-and-concurrency) |
| TC-PERF-03 | NFR-3 | Test the application using the planned large dataset. | Application handles the planned data volume correctly. | Devansh | [OWNER PASS](evidence/issue40-final/owner-cases.md#tc-perf-03--data-volume) |

### 7.8 Backup and Recovery

| Test Case ID | Requirement | Test Scenario | Expected Result | Owner | Status |
|---|---|---|---|---|---|
| TC-OPS-01 | NFR-4 | Create a database backup and restore it in a test environment. | Restored database contains the expected data and records. | Devansh | [OWNER PASS](evidence/issue40-final/owner-cases.md#tc-ops-01--backup-and-restore) |

### 7.9 Compatibility and Usability

| Test Case ID | Requirement | Test Scenario | Expected Result | Owner | Status |
|---|---|---|---|---|---|
| TC-QUAL-01 | Quality attributes | Access the application using supported browsers and check basic usability. | Application functions correctly across supported browsers and remains usable. | Vaishnavi | PASS |

### 7.10 Sprint 1 and Sprint 2 Regression Test Cases

The following additional test cases extend the original 33 test cases
to cover regression scenarios introduced during Sprint 1 and Sprint 2.
The original test case IDs remain unchanged.

#### Sprint 1 Regression Tests

| Test Case ID | Requirement | Test Scenario | Expected Result | Owner | Status |
|---|---|---|---|---|---|
| TC-REG-S1-01 | REQ-7, NFR-1 | Search students using a dataset of 5,000 records. | Search results are correct and response time meets the defined target. | Vaishnavi | PASS |
| TC-REG-S1-02 | REQ-8 | Update student contact, course and year details. | Details are updated while the Student ID remains unchanged. | Vaishnavi | PASS |
| TC-REG-S1-03 | REQ-11, REQ-12 | Create a room and verify automatic bed creation. | The expected number of beds is created automatically. | Vaishnavi | PASS |
| TC-REG-S1-04 | REQ-12, REQ-13 | Attempt to reduce room capacity below active allocations. | The operation is rejected and existing allocations remain unchanged. | Vaishnavi | PASS |
| TC-REG-S1-05 | REQ-13 | Apply combined bed filters and navigate paginated results. | Only matching available beds are displayed and filters are preserved across pages. | Vaishnavi | PASS |

#### Sprint 2 Regression Tests

| Test Case ID | Requirement | Test Scenario | Expected Result | Owner | Status |
|---|---|---|---|---|---|
| TC-REG-S2-01 | REQ-17, REQ-18, REQ-19 | Transfer and release allocations. | Allocation history is preserved and audit events are recorded correctly. | Devansh | PASS |
| TC-REG-S2-02 | REQ-15 | Submit simultaneous allocation requests for the same bed or student. | Only one valid allocation succeeds. | Devansh | PASS |
| TC-REG-S2-03 | REQ-20, REQ-21 | Submit simultaneous payment requests. | Each payment receives a unique sequential receipt number. | Devansh | PASS |
| TC-REG-S2-04 | REQ-20, REQ-21 | Apply payment adjustments to an existing payment. | Original payment history is preserved and adjustment amounts are validated. | Devansh | PASS |
| TC-REG-S2-05 | REQ-23 | Compare occupancy report results in HTML, CSV and JSON formats. | All formats contain consistent report data and preserve filters. | Devansh | PASS |

## 8. Requirements Traceability Matrix (RTM)

The RTM maps all 24 functional requirements and 12 non-functional requirements to their corresponding original test cases.

### 8.1 Functional Requirements

| Requirement ID | Mapped Test Case IDs |
|---|---|
| REQ-1 | TC-AUTH-01 |
| REQ-2 | TC-AUTH-02, TC-AUTH-03 |
| REQ-3 | TC-AUTH-04 |
| REQ-4 | TC-USR-01, TC-SEC-01 |
| REQ-5 | TC-STU-01, TC-STU-02 |
| REQ-6 | TC-STU-02 |
| REQ-7 | TC-STU-03, TC-REG-S1-01 |
| REQ-8 | TC-STU-04, TC-REG-S1-02 |
| REQ-9 | TC-STU-05 |
| REQ-10 | TC-HST-01 |
| REQ-11 | TC-HST-01, TC-REG-S1-03 |
| REQ-12 | TC-HST-02, TC-REG-S1-03, TC-REG-S1-04 |
| REQ-13 | TC-HST-02, TC-REG-S1-04, TC-REG-S1-05 |
| REQ-14 | TC-ALC-01 |
| REQ-15 | TC-ALC-02, TC-ALC-03, TC-REG-S2-02 |
| REQ-16 | TC-ALC-04 |
| REQ-17 | TC-ALC-05, TC-REG-S2-01 |
| REQ-18 | TC-ALC-06, TC-REG-S2-01 |
| REQ-19 | TC-ALC-06, TC-REG-S2-01 |
| REQ-20 | TC-PAY-01, TC-REG-S2-03, TC-REG-S2-04 |
| REQ-21 | TC-PAY-01, TC-REG-S2-03, TC-REG-S2-04 |
| REQ-22 | TC-PAY-02 |
| REQ-23 | TC-RPT-01, TC-REG-S2-05 |
| REQ-24 | TC-SEC-02 |

### 8.2 Non-Functional Requirements

| Requirement ID | Mapped Test Case IDs |
|---|---|
| NFR-1 | TC-PERF-01, TC-REG-S1-01 |
| NFR-2 | TC-PERF-02, TC-REG-S2-02 |
| NFR-3 | TC-PERF-03 |
| NFR-4 | TC-OPS-01 |
| NFR-5 | TC-STU-05 |
| NFR-6 | TC-SEC-04 |
| NFR-7 | TC-SEC-01 |
| NFR-8 | TC-SEC-02 |
| NFR-9 | TC-AUTH-04, TC-SEC-06 |
| NFR-10 | TC-SEC-03, TC-SEC-05 |
| NFR-11 | TC-SEC-07 |
| NFR-12 | TC-AUTH-03, TC-SEC-06 |


## 9. Testing Strategy

### 9.1 Test Levels

| Test Level | Purpose |
|---|---|
| Unit Testing | Verify individual functions and components. |
| Integration Testing | Verify interactions between application modules. |
| System Testing | Verify complete application workflows. |
| Acceptance Testing | Verify that the system meets user and project requirements. |

### 9.2 Test Types

| Test Type | Purpose |
|---|---|
| Functional Testing | Verify that application features work as expected. |
| Regression Testing | Ensure existing features continue working after code changes. |
| Security Testing | Identify authentication, authorization and security weaknesses. |
| Performance Testing | Measure response time, load handling and scalability. |
| Recovery Testing | Verify database backup and restoration. |
| Compatibility Testing | Verify functionality across supported browsers. |
| Usability Testing | Evaluate ease of use and interface behavior. |

## 10. Automation and Test Evidence

The repository contains automated test suites in the following modules:

| Module | Testing Area |
|---|---|
| `students/tests.py` | Student management |
| `hostels/tests.py` | Hostel and room management |
| `accounts/tests.py` | Account functionality |
| `accounts/test_security.py` | Account security |
| `allocations/tests.py` | Allocation functionality |
| `allocations/test_workflows.py` | Allocation workflows |
| `payments/test_workflows.py` | Payment workflows |
| `reports/test_reports.py` | Reporting |
| `audit/tests.py` | Audit functionality |

### 10.1 Automated Regression Test Mapping

The following automated test methods support the additional Sprint 1 and Sprint 2 regression test cases:

| Test Case ID | Automated Test Method | Test Module |
|---|---|---|
| TC-REG-S1-01 | test_student_search_handles_5000_records_within_two_seconds | students/tests.py |
| TC-REG-S1-02 | test_admin_can_update_contact_course_and_year_but_not_student_id | students/tests.py |
| TC-REG-S1-03 | test_room_creation_automatically_creates_beds | hostels/tests.py |
| TC-REG-S1-04 | test_capacity_cannot_be_reduced_below_active_allocations | hostels/tests.py |
| TC-REG-S1-05 | test_combined_filters_return_only_matching_available_beds; test_bed_list_is_paginated_and_keeps_filters_on_next_page | hostels/tests.py |
| TC-REG-S2-01 | test_transfer_and_release_preserve_history_and_emit_actor_audit | allocations/test_workflows.py |
| TC-REG-S2-02 | test_simultaneous_same_bed_or_same_student_has_one_winner | allocations/test_workflows.py |
| TC-REG-S2-03 | test_simultaneous_payments_receive_unique_sequential_numbers | payments/test_workflows.py |
| TC-REG-S2-04 | test_adjustments_preserve_original_and_validate_their_source_and_net_amount | payments/test_workflows.py |
| TC-REG-S2-05 | test_occupancy_csv_and_html_match_json_and_preserve_filters | reports/test_reports.py |

These methods are included in the project's automated test suite. Their individual test case execution status should be updated only after reviewing the corresponding execution results.

The combined project test runner is:

```powershell
python scripts/run_checks.py
```

Focused student and hostel tests can be executed using:

```powershell
python manage.py test students hostels --noinput
```

Test evidence should record:
- Test case ID.
- Tested commit hash.
- Test environment.
- Execution command.
- Actual result and status.
- Evidence file reference.
- Defect and retest details, if applicable.

Evidence should be stored under:

`docs/part3/evidence/`

Database dumps, credentials, real student information and sensitive test data must not be committed.

## 11. Entry and Exit Criteria

### 11.1 Entry Criteria

- Software Requirements Specification is approved.
- Application build is deployed.
- Required synthetic test data is available.
- Test cases have been reviewed.
- Test environment is ready.

### 11.2 Exit Criteria

- 100% of planned test cases have been executed.
- All high-priority test cases have passed.
- No critical or high-severity defects remain open.
- Every RTM requirement is covered by at least one passed test case.

The exit criteria must be evaluated using actual execution evidence.

## 12. Revision Notes and Limitations

1. All 33 original test case IDs have been retained.
2. All 24 functional and 12 non-functional requirements are mapped in the RTM.
3. TC-AUTH-03 retains the five-failed-attempt lockout and 15-minute recovery behavior. Error wording should remain generic, consistent with REQ-2.
4. Ten additional Sprint 1 and Sprint 2 regression test cases have been added with unique IDs and mapped to their corresponding requirements in the RTM.
5. Regression test statuses have been updated based on targeted automated test execution results.
6. The 56-test Students and Hostels result is a focused execution result, not proof that the entire application has passed.
7. The System Validation Report and combined project report are separate deliverables.
8. The full automated verification run reported 185 tests, with 184 passed, 1 skipped and 0 failures or errors. Overall coverage was 92.63%.

9. On 6 November, Devansh reconciled only his 13 original HMS-18 cases to linked OWNER PASS evidence from 5 November and recorded the actual PR #50 merge. Original case IDs, other owners' rows, priorities and RTM mappings are preserved; QA acceptance is pending.

---
**End of Test Case Document**
