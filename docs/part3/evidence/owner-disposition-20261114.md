# Project owner disposition — 14 November 2026

This records Sreeharsha's project-owner decisions made under his instruction to
complete his Part 3 responsibilities. The decisions are limited to owner/PO
scope. They do not stand in for Vaishnavi's QA review, Devansh's development
acceptance, a guide walkthrough, or instructor approval. The original Test Plan
results and its formal exit criteria remain visible and unchanged.

## Case priorities and RTM

- **Priorities:** The current 61-case proposal (34 High, 27 Medium) is accepted
  for the project owner's planning and exit review, effective 14 November. The
  original Test Plan assigned no per-case priorities; this decision is not
  retroactive. QA and Development still need to review the rationale and agree
  before reporting the High-priority exit criterion as satisfied. It is not
  satisfied now: TC-SEC-08 is proposed High and remains PARTIAL.
- **Core RTM:** The 36 original requirement-to-case mappings are accepted as
  design traceability. This does not mean each requirement has an accepted
  passed case, and it does not approve every condition or added SRS quality
  attribute. The 36-requirement accepted-pass measure remains UNVERIFIED until
  QA reviews case evidence and records its requirement-by-requirement result.

## REQ-24 student display boundary

For this mini-project, REQ-24 is interpreted as access to only the signed-in
student's own:

- name and Student ID;
- current allocation (hostel, floor, room, bed and allocation date) and
  allocation history;
- payment status, amount paid, balance due and payment history.

This is the current My Records page's field boundary. Additional contact,
guardian or other personal fields are not required by this PO interpretation.
The linked-account isolation requirement remains in force. QA should review
this interpretation against REQ-24 before final acceptance.

## SAD §4.4 mini-project limitation

The project owner accepts the existing documentation disposition for this
non-deployable mini-project: request-ID error logging and the full operational
monitoring set (login-failure count, HTTP 4xx/5xx rate, average response time,
backup-job success, database free space and weekly review) are not implemented
or evidenced, and will remain a disclosed limitation rather than new product
work for this submission. Existing audit events and backup evidence do not
meet or replace those SAD §4.4 items. No compliance claim is made for this
section. This is an owner scope decision, not an instructor-approved Test Plan
amendment; QA, the guide and instructor requirements remain controlling for
final course acceptance.

## Availability and security case limits

- **TC-QUAL-02:** Retain the prior owner-authorized #39 tracking closure with
  the workday availability observation NOT RUN. Do not count it as a measured
  pass or infer a formal Test Plan waiver from the tracking closure.
- **TC-SEC-08:** Accept the supplied 10 November QA handoff as the alert-level
  disposition for the passive loopback scan. Retain the Low server-banner and
  Informational `next` observations; the case remains PARTIAL because this
  evidence does not establish a deployed-host or broader scan.
- Physical-phone testing is excluded from this mini-project. Desktop browser
  and Windows/Linux portability conditions remain separate and unverified.

## Retrospective owner severity assessment of known closed defects

Severity below is assigned from the documented defect and retest evidence; it
does not add or relabel historical GitHub metadata. All four defects are
already closed and fixed.

For this retrospective assessment, **Medium** means a material report or
workflow risk with no demonstrated underlying record corruption and a
recoverable/corrected outcome; **Low** means a presentation defect with the
underlying values and records intact. These are owner-assigned review labels,
not historical issue labels or a claim that the repository defined a formal
severity scale.

| Issue | Owner-assessed severity | Basis | Current state |
|---|---|---|---|
| [#45](https://github.com/Sreeharsha2240/hostel-management-system/issues/45) | Medium | A required Bed field was missing from payment-status report outputs; totals and stored payment data were not reported as corrupted. | Closed; regression/browser evidence retained. |
| [#46](https://github.com/Sreeharsha2240/hostel-management-system/issues/46) | Medium | Missing confirmation on transfer/release could allow an unintended allocation change. | Closed; cancellation and acceptance paths retested. |
| [#47](https://github.com/Sreeharsha2240/hostel-management-system/issues/47) | Low | Allocation dates were displayed in the wrong format; underlying date data and JSON ISO format were preserved. | Closed; list/history formatting retested. |
| [#48](https://github.com/Sreeharsha2240/hostel-management-system/issues/48) | Low | Student self-service dates used a non-required display format; underlying allocation/payment data was unaffected. | Closed; focused date regression passed. |

This assessment supports **zero known open High/Critical defects among these
four issues only**. Whole-project inventory completeness, severity review of
any additional defect and QA acceptance remain UNVERIFIED.
