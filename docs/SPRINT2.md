# Sprint 2 implementation and verification

Sprint 2 runs from 26 to 30 October 2026. Devansh owns #8 allocations, #9
payments/receipts and #11 reports. Work builds on the accepted student/hostel
implementation in PRs #22–#24. Earlier drafts #19–#21 were closed and are not
the integration base.

## HMS-08: allocations (REQ-14–REQ-19, BR-1–BR-3)

Admin and Warden users allocate beds at `/allocations/create/`, transfer at
`/allocations/<id>/transfer/`, and release with a vacate date at
`/allocations/<id>/release/`. The existing POST-only completion action remains
compatible and supplies today's date. Student users cannot access staff routes.
The list is paginated; a student's history is available at
`/students/<student-pk>/allocations/` in descending date/ID order.

JSON clients use a session and CSRF token, `Content-Type: application/json`
for writes and `Accept: application/json` for reads. POST `/allocations/`
accepts `{student_id: <SRN>, bed_id: <integer>, allocated_on?: <ISO date>}`.
Transfer accepts `{new_bed_id: <integer>}` and release accepts
`{vacate_date: <ISO date>}`. Responses identify the allocation and bed;
conflicts return 409 and gender/eligibility violations return 422.

Transfers close the original allocation and create a new record, preserving
the old bed and dates. Allocation, transfer, release, bed updates and their
actor-specific audit events commit together. Failed writes or audit errors
roll back the whole operation. History is read-only in Django admin, and
ordinary ORM bulk writes/deletions are blocked.

Operations lock Student first, then Rooms and Beds in increasing PK order,
then Allocation. Student deactivation takes the same Student lock. Unique
active IDs and database checks prevent conflicting or forged active records
on MySQL, including inserts that bypass application validation.

Migration `allocations.0003` repairs the derived active IDs left null by
`0002` and synchronizes available beds with active records. It first validates
existing conflicts and dates. It stops for ambiguous/inconsistent records;
it never invents a historical vacate date. Correct such records using verified
business dates before retrying. Apply migrations with application writes paused.

Run `python manage.py test allocations students hostels --noinput` for focused
checks, or `python manage.py test --noinput` for all applications. Added tests
exercise transfers/history, role access, CSRF, rollback, audit failure,
database checks, upgrade/backfill behavior, competing allocation requests,
deactivation races and simultaneous transfers between rooms.

The full MySQL suite passed 110 tests after the allocation implementation.
Payment/report results will be recorded with those implementations.
