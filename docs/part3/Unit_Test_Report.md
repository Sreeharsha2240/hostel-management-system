# Unit Test Report — Hostel Management System

**Project:** Hostel Management System (HMS)
**Report:** HMS-19 / Issue #41 — Unit Test Report
**Evidence baseline:** PR #67 coverage follow-up, merged source revision `7556822df38b23d4f302cf68d857bb35b963ff10`
**Source tree:** `781dd5195e1b6da718fe602ae67cdb04f495acd4`
**CI evidence:** PR CI run `42512163716` and merged-main CI run `42512481376`
**Report date:** 13 November 2026

---

## 1. Introduction

The Hostel Management System (HMS) is a web-based application for managing hostel-related activities. Its main areas include student records, hostel and room information, bed allocation, payments, reports and user access.

Testing was carried out to check whether the application behaves as expected, whether its modules work correctly together, and whether changes have affected existing functions. The testing work includes tests of individual logic, application components, module interactions, concurrency-related behaviour, system workflows and verification tools.

This report records the test approach, execution results, coverage measurements and the evidence used to reach the conclusions. Unit and component-level testing are the main focus. Other testing activities are included separately so that their results are not incorrectly presented as unit-test results.

## 2. Testing Objectives

The testing activities had the following objectives:

- Check the behaviour of individual functions and application components.
- Verify validation rules and application responses for valid and invalid inputs.
- Check interactions between application modules and database-backed operations.
- Check important workflows involving students, hostels, allocations, payments and reports.
- Check concurrency-related behaviour in allocation and payment operations.
- Check that changes do not break previously working behaviour.
- Check relevant security, recovery and verification-runner behaviour.
- Measure statement and branch coverage using the repository's configured coverage process.
- Preserve test results and supporting evidence so that the results can be reviewed and reproduced.

## 3. Testing Scope

The test evidence covers the following application areas and supporting functions:

| Area | Testing focus |
|---|---|
| Accounts and authentication | Authentication behaviour, password-related decisions, session and lockout behaviour |
| Students | Student records, validation, search, updates and student-related workflows |
| Hostels | Hostel and bed information, filtering and availability-related behaviour |
| Allocations | Allocation validation, dates, status rules, workflows and concurrency-related behaviour |
| Payments | Payment rules, configured fees, payment workflows and concurrency-related behaviour |
| Reports | Report generation and report input handling |
| Audit and security-related functions | Audit behaviour, security checks and retention-related behaviour |
| Verification tooling | Test runner, coverage export, result reporting and runner-safety checks |

The configured coverage measurement also includes application code that was not executed. In particular, the two demo-data management commands remain untested: together they contain 98 statements and 32 branch outcomes. These remain in the coverage denominator and are not excluded to increase the reported percentage.

## 4. Testing Types and Approach

The project test inventory distinguishes several types of testing. The categories below are kept separate because they check different things.

### 4.1 Unit Testing

Unit tests check a small piece of logic independently of a complete application workflow. The follow-up work added isolated tests for specific rules and response behaviour.

Ten additional isolated tests were added and separately verified:

| Area | Tests added | Focus |
|---|---:|---|
| Accounts | 2 | Backend password-decision behaviour |
| Allocations | 3 | Allocation date and status validation |
| HMS shared validation | 4 | JSON validation-response contracts |
| Payments | 1 | Configured-fee and payment-status rule |
| **Total** | **10** | |

These tests supplement the existing test inventory. They do not replace or rewrite the earlier test classifications.

### 4.2 Component Testing

Component tests check the behaviour of application parts such as models, forms, views and shared helpers. The project's test plan allows model, form and view tests to be considered at this level when the test verifies the component's own behaviour.

The historical classification contains 85 primary component candidates. The classification also records the test's actual dependencies and assertions; database use alone is not treated as enough information to decide that a test is an integration test.

### 4.3 Integration Testing

Integration tests check whether application parts work correctly together, including database-backed operations and connected workflows.

The historical classification contains 87 integration methods. In addition, nine owned integration/regression recipes were executed separately and passed. These results are reported as integration/regression evidence, not as isolated unit tests.

### 4.4 Concurrency Testing

Concurrency tests check behaviour when operations may overlap or compete for shared data. The historical classification identifies five concurrency methods. Allocation and payment concurrency behaviour is represented in the test evidence.

### 4.5 System and Workflow Testing

System-level and workflow tests check behaviour across connected application functions. The historical classification identifies four system-surrogate methods. The test evidence also includes student/hostel journey and allocation/payment workflow checks.

These automated results do not replace the separate manual acceptance records or the System Validation Report. A passing automated workflow test is not treated as proof that every manual system-acceptance case has been completed.

### 4.6 Regression Testing

Regression testing checks whether existing behaviour continues to work after changes. The full verification suite and the nine separately executed integration/regression recipes provide regression evidence. The ten new isolated tests also cover specific regression cases in accounts, allocations, shared validation and payments.

### 4.7 Security, Recovery and Verification-Runner Checks

Security-related checks are present in the wider test evidence, including authentication/session-related checks and audit-related behaviour. Separate safety evidence records 32 recovery-safety tests and seven verification-runner safety tests as passing.

These results are reported by their recorded purpose. They are not added to the unit-test count.

## 5. Test Environment and Tools

The PR #67 verification evidence records successful CI execution under Python 3.11 and Python 3.14. The same source revision was checked in the PR CI run and again in the merged-main CI run.

| Item | Recorded environment or evidence |
|---|---|
| Repository | `Sreeharsha2240/hostel-management-system` |
| Tested source revision | `7556822df38b23d4f302cf68d857bb35b963ff10` |
| Tested source tree | `781dd5195e1b6da718fe602ae67cdb04f495acd4` |
| Python CI environments | 3.11 and 3.14 |
| Framework | Django 5.2.18 |
| Test and verification process | Repository verification runner and automated CI workflow |
| Test result evidence | JUnit results and runner summaries |
| Coverage evidence | Coverage report and source-bound verification records |

The CI evidence identifies the tested source tree and records that the tested trees match the merged source tree. The two Python jobs are separate environment runs of the same suite; they are not counted as two sets of distinct test methods.

## 6. Test Case Execution Summary

The PR #67 handoff records 200 distinct ordinary test methods:

| Result | Count |
|---|---:|
| Passed | 199 |
| Failed | 0 |
| Errors | 0 |
| Expected timing skip during coverage run | 1 |
| **Distinct ordinary test methods** | **200** |

The timing-related test was skipped while coverage instrumentation was active. It passed when run separately without coverage instrumentation. It is therefore recorded as an expected skip in the coverage run, with a separate passing timing result.

Additional execution evidence records:

| Additional verification activity | Result |
|---|---:|
| Verification gates | 12 passed |
| Owned integration/regression recipes | 9 passed |
| Recovery-safety tests | 32 passed |
| Verification-runner safety tests | 7 passed |
| New isolated tests | 10 passed |

The Python 3.11 and Python 3.14 CI runs verify the same distinct test methods. Their counts are not added together.

## 7. Coverage Analysis

The coverage follow-up records the following exact measurements for the PR #67 evidence baseline.

| Coverage measure | Covered | Total | Achieved |
|---|---:|---:|---:|
| Statement coverage | 1,590 | 1,772 | **89.73%** |
| Branch coverage | 348 | 424 | **82.08%** |
| Combined coverage | 1,938 | 2,196 | **88.25%** |
| Required threshold | — | — | **70%** |

The combined result is calculated from the covered statement and branch outcomes:

`(1,590 + 348) / (1,772 + 424) × 100 = 88.25%`

The combined result is 18.25 percentage points above the required 70% threshold.

### 7.1 Requirement Interpretation and Result

SRS §6.4 states a 70% coverage requirement for application logic. The project guide/project owner has confirmed that the project's configured combined statement-and-branch coverage metric is the measure used for this 70% project gate.

On that project-approved interpretation, the recorded combined result is **88.25% against a 70% threshold — PASS**.

The statement and branch percentages are also shown separately so that the two measurements remain visible. The report does not state that the SRS text itself defines the combined formula, and it does not describe the 88.25% full-suite configured result as a unit-only percentage.

The approval of the measurement interpretation and the measured result are separate facts: the project guidance defines which configured metric is compared with the threshold; the coverage evidence supplies the measured values.

## 8. Defects, Failures and Observations

The PR #67 handoff records no failed or errored ordinary test methods in the 200-method execution summary. One timing test was expected to skip while coverage instrumentation was active and passed separately without instrumentation.

The following coverage observation remains important:

- The two demo-data management commands were not executed by the suite.
- They contain 98 statements and 32 branch outcomes.
- They remain included in the configured coverage denominator.
- Their unexecuted paths are therefore reflected in the reported coverage result.

The historical test classification is preserved as recorded:

| Historical classification | Methods |
|---|---:|
| Primary component candidates | 85 |
| Integration | 87 |
| Concurrency | 5 |
| System-surrogate | 4 |
| Verification tooling | 9 |
| **Total historical inventory** | **190** |

The ten new isolated tests are additions to this inventory and are not used to silently change the earlier 190-method classification or its frozen selections.

## 9. Evidence and Reproducibility

The following repository evidence supports this report:

| Evidence | Purpose |
|---|---|
| `docs/part3/evidence/coverage-followup-20261109/README.md` | PR #67 coverage follow-up, execution summary and handoff |
| `docs/part3/evidence/coverage-followup-20261109/verification.json` | Source-bound verification details and machine-readable results |
| `docs/part3/Development_Review_20261108.md` | Development classification review and related QA handoff |
| `docs/part3/evidence/development-review-20261108/classification-supplement.json` | Supplementary test-classification evidence |
| `docs/part3/evidence/development-review-20261108/verification.json` | Verification evidence for the development review |
| `docs/part3/evidence/hms-test-evidence-py3.11/` | Python 3.11 test, coverage, JUnit and runner evidence |
| `docs/part3/evidence/hms-test-evidence-py3.14/` | Python 3.14 test, coverage, JUnit and runner evidence |
| `docs/part3/evidence/issue63/` | Separate integration, recovery-safety and runner-safety evidence |

CI records:

- [PR CI run 42512163716](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42512163716)
- [Merged-main CI run 42512481376](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42512481376)

The verification records link the test results and coverage measurements to the tested source revision. The PR and merged-main runs are kept as separate execution records; their test counts are not combined.

## 10. Conclusion

The recorded verification results show that the HMS test suite executed 200 distinct ordinary test methods, with 199 passing and one expected timing skip during coverage instrumentation. The timing test passed separately without instrumentation. The verification evidence also records 12 passing gates, nine passing integration/regression recipes, 32 passing recovery-safety tests, seven passing runner-safety tests and ten passing isolated tests.

The coverage report records 89.73% statement coverage, 82.08% branch coverage and 88.25% combined coverage. The combined result exceeds the project-approved 70% threshold.

Based on the recorded results, we conclude that the configured combined coverage gate is **PASS** for the PR #67 evidence baseline. The report keeps the full-suite combined result distinct from unit-only coverage and records the untested demo-data commands as remaining coverage gaps. Manual system acceptance and overall project submission readiness remain covered by their separate records.

---

## Appendix A — Key Evidence References

- PR #67 source revision: `7556822df38b23d4f302cf68d857bb35b963ff10`
- Tested source tree: `781dd5195e1b6da718fe602ae67cdb04f495acd4`
- PR CI run: `42512163716`
- Merged-main CI run: `42512481376`
- Coverage handoff: `docs/part3/evidence/coverage-followup-20261109/README.md`
- Machine-readable verification: `docs/part3/evidence/coverage-followup-20261109/verification.json`
