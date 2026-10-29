# HMS-14: End-to-End Testing Evidence

## Test Environment
- Application: Hostel Management System
- User role: Admin
- Test student ID: E2ETEST202601
- Test student: E2E Active Student
- Hostel: E2E Test Hostel
- Room: E2E-101
- Bed: E2E-101-A

## Test Results

| Test | Expected Result | Actual Result | Status |
|---|---|---|---|
| Student registration | Student registers successfully | Registration confirmation displayed | PASS |
| Student status | Student is active | Active status displayed | PASS |
| Hostel allocation | Available bed is allocated | Bed E2E-101-A allocated successfully | PASS |
| Occupancy report | Occupancy reflects allocation | 3 beds, 1 occupied, 2 available, 33.33% occupancy | PASS |
| First payment | Payment is recorded | INR 4500 recorded | PASS |
| Additional payment | Additional payment is recorded | INR 500 recorded | PASS |
| Payment history | Both payments are displayed | INR 4500 and INR 500 displayed | PASS |
| Payment status | Balance and status are correct | Fee INR 5000, paid INR 5000, due INR 0, status Paid | PASS |
| Occupancy CSV | CSV matches report | Bed counts and occupancy match | PASS |
| Payment status CSV | CSV matches report | Active student's fee, paid amount, due, and status match | PASS |

## Payment Verification
- Total fee: INR 5000
- First payment: INR 4500
- Second payment: INR 500
- Total paid: INR 5000
- Outstanding balance: INR 0
- Final status: Paid

## Evidence Files
- occupancy.csv
- payment-status.csv

## Scope
This evidence covers the active student's registration, allocation, payment, payment history, payment status, occupancy report, and CSV export workflows. Other HMS-14 scenarios have not yet been verified.
