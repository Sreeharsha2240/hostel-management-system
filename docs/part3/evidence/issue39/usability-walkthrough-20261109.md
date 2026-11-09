# HMS-17 — Additional Warden Usability Walkthrough

- **GitHub Issue:** #39
- **Test Case:** TC-QUAL-01
- **Additional execution date:** 9 November 2026
- **Execution type:** Owner-reported manual usability execution
- **Application:** Hostel Management System
- **Test data:** Synthetic data

## 1. Objective

Evaluate whether a new Warden can register a student and successfully allocate a bed using the one-page Warden user guide within the SRS five-minute usability target.

## 2. Task and Result

| Item | Recorded result |
|---|---|
| Participant | New Warden participant; non-identifying participant code was not retained |
| Guide | One-page Warden user guide / task instructions; exact revision or version was not retained |
| Task | Register a student and successfully allocate a bed |
| Target | Complete both actions within 300 seconds |
| Owner-reported result | Completed within five minutes |
| Exact elapsed time | 93 seconds (1 minute 33 seconds), as reported by the owner |
| Start/end timestamps | Not retained |
| Assistance | None reported |
| Errors | None reported |
| Execution status | OWNER-REPORTED PASS for the time-bound task; evidence limitations remain |

The owner reports that the participant completed the guide-based first-use task in 93 seconds, within the five-minute target. No assistance or errors were reported.

The recording provides visual evidence of the workflow, including Warden login, student registration, the registration confirmation, the newly registered student in the student list, bed allocation, the allocation confirmation and the bed availability filter.

The exact elapsed time is an owner-reported stopwatch result. The recording supports the visible workflow but is not treated as independent verification of the stopwatch measurement.

## 3. Execution Environment and Test Data

| Field | Details |
|---|---|
| Operating system | Ubuntu 26.04.1 LTS under WSL2 |
| Python | 3.14.4 |
| Django | 5.2.18 |
| Database | MySQL 8.4.11 |
| Server | Django development server |
| Browser | Firefox |
| User role | Warden |
| Student registered | Leo |
| Synthetic student ID | `LINUX000002` |
| Allocated bed | `LX-101-B` |

## 4. Evidence

**Screen recording:**

`docs/part3/evidence/issue39/recording/TC-QUAL-01_Linux_Warden_First_Use_20261109.mp4`

The recording shows the Warden workflow, including:

1. Warden login.
2. Student registration.
3. Successful registration confirmation.
4. Newly registered student appearing in the student list.
5. Bed allocation.
6. Successful allocation confirmation and resulting allocation record.
7. Bed availability filtering.

The recording is retained as supporting visual evidence for the execution. The reported 93-second duration remains an owner-reported measurement.

## 5. Evidence Limitations

- The exact revision or version identifier of the one-page Warden guide was not retained.
- The participant's non-identifying code was not retained.
- Start and end timestamps were not retained.
- The exact 93-second duration is based on the owner's stopwatch report and cannot be independently reconstructed from retained timestamps.
- No separate participant sign-off was retained.
- Assistance and errors were reported as none, but no separate structured observation sheet was retained.
- This is an owner-reported execution, not an independent participant sign-off.
- This result does not establish the full browser compatibility matrix, all Windows/Linux deployment configurations, physical-mobile compatibility or the SRS availability criteria.

## 6. Relationship to the Historical Execution

The 7 November 2026 TC-QUAL-01 execution remains **PARTIAL**.

That execution covered Warden dashboard, navigation, Students and Beds page checks, but did not record the timed guide-based first-use task.

This 9 November addendum records the later owner-reported task result. It does not rewrite, replace or change the historical execution record or its results.

The original 7 November execution totals remain unchanged.

## 7. Overall Case Disposition

**Guide-based Warden first-use task: OWNER-REPORTED PASS.**

The participant completed student registration and bed allocation in an owner-reported 93 seconds, within the SRS five-minute target. No assistance or errors were reported.

**Overall TC-QUAL-01: PARTIAL.**

The guide-based task has a recorded owner-reported pass, but the wider browser and platform compatibility requirements and the availability assessment remain outstanding. The guide revision and independent participant sign-off were also not retained.

**GitHub Issue #39 remains OPEN** pending the outstanding evidence, independent review and acceptance.