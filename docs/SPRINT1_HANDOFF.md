# Sprint 1 review handoff

The checked-in backlog assigns Sprint 1 to 19–23 October 2026. Devansh's #1 and
#2 are merged. Sreeharsha also merged #3/#4 through PR #16. With Devansh's
authorization, this work helps with the remaining Sprint 1 issues without
changing issue assignees, story points, sprint assignments or product ownership.

## Review order

| PR | Issue / change | Current owner | Review dependency |
| --- | --- | --- | --- |
| [#17](https://github.com/Sreeharsha2240/hostel-management-system/pull/17) | Review fixture convention and authentication startup syntax fix | Devansh, follow-up to #2/#4 | `main` |
| [#18](https://github.com/Sreeharsha2240/hostel-management-system/pull/18) | #5 session protection and retained audit events | Sreeharsha | #17 |
| [#19](https://github.com/Sreeharsha2240/hostel-management-system/pull/19) | #7 hostel, room and bed management | Vaishnavi | #18 |
| [#20](https://github.com/Sreeharsha2240/hostel-management-system/pull/20) | #6 student records and allocation read checks | Vaishnavi | #19 |
| [#21](https://github.com/Sreeharsha2240/hostel-management-system/pull/21) | #10 repeatable checks, integration tests and evidence | Vaishnavi | #20 |

The feature PRs are drafts for review. Each targets its dependency branch so its
diff contains only that issue's work. After the base is merged, retarget the
dependent PR to `main` and review its resulting diff. Student management uses
the hostel models for its hostel filter, which explains the implementation
order #7 before #6. No feature PR closes an issue automatically.

Part-2 requires the assigned team member to raise the submission PR and the repo
owner to review/merge. These drafts are authored by Devansh as an implementation
handoff. The assigned owners should review/adopt the branches and raise their
own final submission PRs under their accounts. Product ownership stays with
Sreeharsha; acceptance and merging remain team responsibilities.

## Review findings addressed

Sreeharsha withdrew the missing-password objection on PR #15, approved it and
merged it. PR #17 still changes that fixture to `create_user()` as originally
requested. It also fixes a separate literal `\r\n` token in the merged
`accounts/admin.py` which prevents Django startup.

The Sprint 1 follow-up closes the Django-admin lockout bypass by using one
authentication backend, logs both login routes and account-management routes,
protects authenticated responses from caching and guards audit records against
ordinary update, deletion and upsert paths. Audit cleanup preserves at least
366 days. Audit and business changes share a transaction.

Student records follow Appendix B, retain immutable unique IDs and use soft
deactivation. Hostel/room/bed changes use Admin permissions, automatic bed
creation and atomic resizing. Current-allocation read adapters protect
deactivation and bed availability/status once HMS-08 supplies the model.

## Acceptance and remaining integration

Run the instructions in [TESTING.md](TESTING.md) and review the evidence in
[test-evidence/sprint1.md](test-evidence/sprint1.md). The combined implementation
is on `feature/HMS-10-sprint1-verification` and can be run using the README's
normal migration/setup steps.

HMS-08 must supply the documented Allocation model, lock the Student before
allocation, preserve historical references and call the shared audit recorder
inside each allocation/transfer/release transaction. Payment services must do
the same for payment events. Integration tests must be repeated against those
actual models. The current contract tests use a temporary MySQL fixture table.
Allocation/payment/report/self-service operations remain in Sprint 2.

The UI uses local responsive CSS rather than the planned Bootstrap 5 dependency.
Record this presentation-library deviation for the demo. The browser login
routes remain the existing `/login/` and `/logout/` paths; the SRS/SAD's
`/auth/...` aliases and complete JSON authentication response contract are not
added by this Sprint 1 follow-up. TLS is configured at deployment and still
requires deployment testing. Wider load, backup, browser/usability checks and
the Sprint 1 one-minute outcome video remain with the planned team acceptance
activities; no such results or recording are claimed here.
