# HMS-14 Mini-project E2E Results

Date: 2026-10-29  
Application revision exercised: `7f8cd0281b383342843e1018aea27fbf6cbf6040`  
Test setup: Disposable local MySQL 8.0.46 database; Django views; Admin, Warden, and Student roles; synthetic records only. Passwords are intentionally omitted.  
Outcome: **28 checks passed. No high-severity functional defect was found.**

| Scenario | Expected result | Actual result | Result |
|---|---|---|---|
| Roles and permissions | Staff dashboards load and role gates protect restricted pages. | Admin and Warden dashboards returned HTTP 200; Warden was denied the audit page. Desktop Chrome confirmed role-appropriate navigation. | PASS |
| Student account/profile | Admin creates a linked student login; Warden updates it; search finds it. | Account and profile were created and linked; Warden update persisted; student-ID search returned the record. | PASS |
| Hostel, room, bed | Setup persists; maintenance beds are visible and cannot be allocated. | Hostel, rooms, and two beds were created; maintenance filtering worked; transfer to a maintenance bed was rejected. | PASS |
| Allocation lifecycle | Allocate, transfer with history, release, and restore availability. | Allocation succeeded; transfer preserved history and changed bed states; release made the destination bed available. | PASS |
| Payment and receipt | Record payment, verify receipt/PDF and student status. | Payment was recorded; receipt page and PDF loaded; student payment status loaded. | PASS |
| Student self-service | Linked student sees own records only; logout protects routes. | Student login succeeded; own allocation/payment appeared; another student's record did not; logout cleared session and protected the route. | PASS |
| Reports and CSV | Filters apply and export values match report totals. | Occupancy JSON/CSV filters matched; payment report and CSV showed INR 5,000 paid for the test student. | PASS |
| Audit trail | Admin can review events; restricted role is denied; sensitive data is omitted. | Admin audit response contained approved fields; Warden received HTTP 403; passwords, tokens, and private request fields were absent. | PASS |
| Validation/errors | Invalid operation is rejected; no critical/high issue appears in tested journeys. | Maintenance-bed transfer and restricted-role access were rejected as expected; no critical/high defect was observed. | PASS |

## Scope

This is a course mini-project. Desktop core workflows, basic role authorization, and data consistency are the acceptance bar. Mobile, multi-browser, timed usability, deployment TLS/ZAP, scheduled backup automation, and extended performance checks are outside this scope unless the course rubric requires them.

The full local Django suite discovered 163 tests but could not start because the local MySQL user cannot create the test database (MySQL error 1044). GitHub Actions run 40811227742 passed on revision `7f8cd02` with MySQL 8.4 and Python 3.11/3.14. The local suite setup failure is not counted as a test failure.

## Final desktop website review — 2026-10-29

- Reviewed the live desktop preview: sign-in, Admin dashboard, Students, Allocations, Payments, Reports, Hostels, Beds, Accounts, and Audit log loaded with expected content and no browser console errors or warnings.
- The sign-in card looked too narrow at desktop size. Its local stylesheet now allows an 860px maximum width and enlarges the heading and form controls, while retaining the narrow-screen override. The refreshed page visibly renders at 860px. The synthetic local demo Admin login was verified and signed out.
- No further functional defect was found. This visual adjustment is a follow-up usability fix; the 28-check workflow results above remain the functional test evidence.
