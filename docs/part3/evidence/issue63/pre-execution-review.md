# HMS-26: review before the committed execution

**Recorded:** 8 November 2026, after the candidate executions and before the
clean committed execution. **Owner:** Devansh (`DevaOnL`), issue #63.

The review covers the existing TC-REG-S2-08 through TC-REG-S2-16 recipes in the
[case register](../../Test_Case_Document.md#case-tc-reg-s2-08), the submitted
Test Plan/SRS/SAD, and the Part 3 assignment PDF. IDs, requirements, expected
results and thresholds are retained. These are synthetic integration cases,
not additional unit-only results or a repeat of the historical browser run.

| Case | Reviewed recipe | Current technical priority |
|---|---|---|
| S2-08 | Allocation/release audit rollback, transfer storage rollback, unchanged beds/history and same-transfer retry | High |
| S2-09 | Sequential original receipts, all ORM mutation guards and genuine adjusting entry | High |
| S2-10 | Invalid/faulted payments, audit/receipt rollback and retry, exhaustion preserving history | High |
| S2-11 | Two real connections competing at the service locking query; one correction, no over-reversal, counter 2 and net INR20 | High |
| S2-12 | Totals/Bed/latest valid location across JSON/CSV/HTML, transfer/release, never-assigned/cancelled-only and zero fee | Medium |
| S2-13 | Literal dangerous CSV prefixes, Unicode/quotes/newlines and escaped report HTML | Medium |
| S2-14 | Empty reports; invalid/missing/leading-zero filters; format and method boundaries on both routes | Medium |
| S2-15 | Malformed/invalid UTF-8/container/scalar/nonfinite/deep/surrogate JSON, real endpoints, generic errors and unchanged state | High |
| S2-16 | Typed dates/references, exact status/error contracts, valid controls and unchanged business state | High |

High reflects transaction, financial or validation integrity; Medium reflects
operational report correctness. These priorities are accepted for this current
automated technical review. Original priorities were unspecified; whole-team
priority/exit approval remains separate.

Three fresh automated reviewers worked without the earlier implementation
discussion: `blind_owned_transactions`, `blind_owned_reports_json` and
`blind_owned_runner_scope`. They independently inspected the requirements,
source and candidate raw evidence. The transaction reviewer required proof of
actual service overlap; both workers now synchronize at the real Student
locking-query boundary, using unchanged SQL. The report reviewer required
separate never-assigned coverage and a populated leading-zero filter oracle;
both are now asserted. The runner reviewer required truthful subtest/setup
outcomes, durable failure metadata, database/output race protection and source
provenance. Those corrections and seven offline safety tests were reviewed.
All three reported no remaining material blocker in their respective scopes.

The corrected candidate run `review-corrections` recorded nine PASS with
complete step observations, but its source was dirty. The separate full
candidate run passed all 12 gates: 190 mixed methods (189 PASS, one expected
timing SKIP) and a separate timing PASS. These candidate runs remain private
under `test-results/owned-regressions-20261108/`; they will not be relabelled as
the clean committed run. The final evidence will identify its own SHA/tree,
commands, versions, source hashes, outcomes and raw hashes.

Execution uses disposable MySQL `test_hms`, refuses an existing/custom/mirrored
database and runs serially with other database suites. Test-client HTTP disables
secure redirect/cookie flags only for these tests; no TLS, browser compatibility,
lock-wait duration or live transport claim is made. MySQL 8.4 differs from the
submitted 8.0 baseline. The 8 November review/execution is outside the original
2–6 November window; no instructor extension or waiver is recorded.

This current technical review cannot supply historical approved-SRS/entry
compliance, named human QA/Dev/PO decisions, a new-Warden guide walkthrough,
the missing Unit Test Report, formal SRS unit70 acceptance or a submission
receipt. Whole-plan readiness remains **NOT READY**. Other owners retain
#38/#39/#41/#43; #40's original 13-case closure and all earlier evidence remain
unchanged.
