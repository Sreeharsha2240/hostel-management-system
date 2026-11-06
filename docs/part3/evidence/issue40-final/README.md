# HMS-18 final owner execution and handoff

Owner: Devansh Gupta (`DevaOnL`), [issue #40](https://github.com/Sreeharsha2240/hostel-management-system/issues/40). Executed **5 November 2026** on clean merged application `0e358b4ce1fd02366184c7cb9c312b47dd093214`, tree `c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0`. This execution includes Sreeharsha's merged self-service correction in PR #49. The later publication contains owner evidence and documentation only.

**All 13 original owned cases have passing execution evidence for the recorded source.** [PR #50](https://github.com/Sreeharsha2240/hostel-management-system/pull/50) was merged by `harsha2240` on **5 November 2026 at 06:31:28 UTC** as `8d60e83f1ce57ad99a2b2a22b3b5878f1390995b`. This records independent integration; its review array contains no formal `APPROVED` review. The [case register](../../Test_Case_Document.md#53-hms-18-owner-execution-and-evidence-reconciliation) now links these 13 owner results as **OWNER PASS**, with QA acceptance pending. **Issue #40 remains open** pending #37's reviewed-case/entry-criterion disposition and actual independent evidence acceptance. This evidence does not approve the complete Test Plan, the updated team case register/RTM, the final System Validation Report or QA/PO readiness. Those remain with #37/#38/#43 and their assigned owners. The historical `summary.json` review/merge wording records the pre-merge execution snapshot and is preserved unchanged; this dated reconciliation supersedes that publication status. The owner [case appendix](owner-cases.md) retains original steps, expected results, requirements, test level/type, unspecified original priorities, actual results and companion-method links.

## Fresh observed results

- Full repository verification: **12 gates passed**, **190 methods**, **189 PASS**, zero failures/errors and one expected timing skip under coverage followed by a passing uninstrumented timing run. These are mixed-level methods, not 190 original cases or a unit-only coverage result.
- Allocation/payment/report/journey/self-service focused checks: **71 passed**. This includes current self-service DD-MM-YYYY/fallback assertions, transfer rollback and same-transfer retry, counterordered allocation history, report Bed and cross-format parity.
- Offline recovery-safety suite: **32 passed**. Previous defect negative controls remain historical; this run verifies the corrected guards.
- Actual Edge/Playwright browser/HTTP execution: **passed**, including forms, native transfer/release dialogs, zero POSTs/state changes on cancellation, one POST/action on acceptance, Enter from the release date field, staff display dates, ISO JSON, reports, receipts and own-student integration. The student page's date-format assertion comes from the focused self-service test; browser checks its allocation/payment content integration.
- TC-PERF-02: **20 committed HTTP allocations**, 32.20–42.38 ms; all under three seconds. Overlapping conflict requests returned **201/409**, preserving one winner.

| Full load case | Students / beds | Users / measured duration | All HTTP samples | Errors | Within 2 seconds | HTTP p95 | Search maximum |
|---|---:|---|---:|---:|---:|---:|---:|
| TC-PERF-01 / baseline | 100 / 80 | 50 / 600.106s minimum each | 28,696 | 0 | 99.99303% | 82 ms | 1459 ms |
| TC-PERF-03 / volume | 5000 / 2000 | 50 / 600.083s minimum each | 29,096 | 0 | 100.00000% | 49 ms | 114 ms |

Both workloads use normal hashing, sessions and audit writes, a five-second ramp, a one-second think time on login/search/bed samplers and a shared measurement barrier. The initial setup login-form sampler has no timer; the raw load summary's broader timer note is corrected here without changing its samples or metrics. Every user appears on every route and has complete start/end markers. Login/form samplers and every content/controller error are included. No slow/error sample is discarded. The volume test also requires **every search within two seconds**, and passes that separate gate. Results describe this loopback test host and exact source.

The first volume attempt **failed** with 75 authenticated-content assertion errors after the laptop entered Modern Standby at 04:24:37 UTC and resumed at 04:59:11 UTC. Its results, failures and raw hashes remain in `load-results.json` under `previous_attempts`, alongside the relevant Windows power events. They are not relabelled PASS. The table uses the original passing baseline and a complete volume-only rerun on identical clean source/harness/fixtures/thresholds. The rerun used a process-scoped idle-awake request, released afterward, without changing Windows power policy. Session expiry is consistent with failures around resume; response bodies were not saved, so that cause is not asserted as proven.

## Fresh naturally scheduled populated recovery

TC-OPS-01 **passed** using an existing private synthetic MySQL server on a separate non-live loopback port. A newly and uniquely named temporary **daily** task ran the current backup script through its natural trigger; no on-demand task start was used. Its fresh populated dump was **5.379 seconds old** at restore, within the original 24-hour requirement.

All **18 table counts, row digests and schema digests match** the unchanged populated source. Required student/bed/allocation/payment/audit tables are nonempty. The logical checks report no violations, and no data loss was observed at comparison. Only the sandbox's previously absent `test_hms` was created/restored and then removed.

The temporary task was removed, its owned sandbox server stopped, original synthetic backup artifacts remained unchanged, and the installed live daily task's action, exported definition, trigger and next run remained unchanged. The live `hms` was never seeded or restored. Separate live-task metadata records its successful existing daily backup today; its retained manifest has no embedded code SHA, so the new source-bound synthetic trigger supplies current-code scheduling/restore proof. The existing daily task still requires the Windows user session, computer and MySQL to be available.

The retained wrapper records the final recovery invocation as `python <private-evidence>/refresh_ops_private.py --private-dir <retained-synthetic-instance> --output-dir <private-recovery-run>`. The helper SHA-256 is `9f8952dcdcb0c3a4ea4422f82f12f7eaa565cf06dd5ab59813393768929b05a0`; the operation started at **2026-11-05 05:12:05.089969 UTC**, completed at **05:13:24.088897 UTC**, and records **PASS** in [recovery-results.json](recovery-results.json). These sanitized arguments supplement the historical `summary.json` command list, which omitted this private orchestration. The helper and connection material remain private; the tracked fresh-machine workflow below supplies the supported reproduction.

## Durable artifacts

| File | Evidence |
|---|---|
| [owner-cases.md](owner-cases.md) | Original 13 cases, 14 SRS requirements, expected/actual steps, test methods, defects and review boundary |
| [summary.json](summary.json) | Case status map, tested commit/tree, source hashes, exact commands, raw artifact hashes and acceptance limits |
| [checks-run.json](checks-run.json) | All 12 gate results, source, environment/tool versions and aggregate coverage |
| [junit-summary.json](junit-summary.json) | All 190 exact method identities/outcomes plus separate timing PASS |
| [focused-methods.json](focused-methods.json) | All 71 focused passing method identities |
| [browser-results.json](browser-results.json) | Synthetic UI/JSON/CSV/MySQL reconciliation, native dialogs, timings, conflicts and receipt checks |
| [load-results.json](load-results.json) | Both full workloads, fixtures, per-route/per-thread metrics, sampler inclusion and raw hashes |
| [recovery-results.json](recovery-results.json) | Fresh natural trigger, populated restore, daily-task preservation, digests and cleanup |

Raw JTL, logs, `.coverage`, full XML/JUnit, credentials, private task actions, connection settings and SQL dumps stay ignored/outside Git. Private orchestration is fingerprinted; repository scripts below implement the measured workloads and guarded backup/restore. Historical issue40 and owned-defects JSON is preserved unchanged. The older TC-RPT-01 complete-PASS claim omitted Bed and was corrected by #45; current evidence verifies the full schema. Browser TC-ALC-05 remains PARTIAL for fault injection; the current companion rollback/same-transfer-retry test supplies that step explicitly.

## Reproduction and handoff

Use the documented MySQL environment and synthetic fixtures. Run one database suite at a time. Choose new ignored evidence directories and refuse existing `test_hms`; preserve previous results. Run from the repository:

```powershell
python scripts/run_checks.py --output-dir test-results/hms18-finish/<new-run>/checks
python manage.py test allocations payments reports hms.test_system_journey students.test_self_service --noinput -v 2
python -S -m unittest discover -s scripts/part3 -p test_issue40_recovery_safety.py -v
python scripts/part3/run_issue40_browser.py --output-dir test-results/hms18-finish/<new-run>/browser
python scripts/part3/run_issue40_load.py --java <external-java.exe> --jmeter <external-ApacheJMeter.jar> --seconds 600 --scenario both --output-dir test-results/hms18-finish/<new-run>/load
```

Browser verification requires optional Playwright through `NODE_PATH` and installed Edge; Java 17 and JMeter 5.6.3 are external test tools. Exact tool versions, sampler configuration and hashes are retained in the artifacts. The committed JMeter plan matches the executed bytes.

For recovery, use only a dedicated populated synthetic MySQL instance and private connection file. The tracked `backup_issue40.py backup` and `recover` commands enforce private output, dump integrity, age, populated tables, source consistency and an absent `test_hms`. A natural daily Task Scheduler trigger must run the backup before recovery. On a fresh machine with no existing HMS task, `run_issue40_recovery.py --private-dir <new-private-directory>` provides the complete initial workflow. This final run preserved the already installed live task: a separate uniquely named temporary daily task invoked the same backup CLI on the retained synthetic sandbox; after natural completion, exact-action/description ownership checks removed that temporary task and the guarded `recover` CLI restored its dump. Validate launcher/child identity and connected server port/datadir before recovery/shutdown, as in the tracked runner. Never replace the installed live task or restore into live `hms` to repeat this proof.

The submitted Test Plan's 13 original owned cases are preserved and technically reconciled here. Updated-case/priority/RTM review and disposition of the reviewed-case entry criterion remain under #37. Tool/environment deviations (Edge/Playwright versus named Selenium, MySQL 8.4 versus 8.0, local HTTP test flags) remain visible for team review. Sreeharsha's #38 consumes this evidence; final whole-plan execution/requirements, exit criteria and actual QA/Dev/PO approvals remain under #38/#43. Publishing this owner handoff does not claim those reviews already occurred. New documentation follows the repository's independent teammate PR review/merge workflow.
