# Unit Test Report — Part 3

**Current measurements: 13 November 2026: all application statements 946/1,703 = 55.55% (below 70%); owner-approved function-body boundary 946/946 = 100.00%.** The subsequent [owner decision](evidence/hms19-function-body-boundary-20261113.md), committed by `harsha2240` in `20f12a9`, approves the narrower function-body interpretation of SRS application logic. It excludes imports and module/class/field declarations from that diagnostic. The all-statements decision relayed in the preceding handoff includes those statements and remains **NOT MET** under its own criterion. These are different acceptance boundaries, not two percentages for the same denominator. All 288 isolated tests pass with zero database attempts. Expanded isolated branches are **411/426 = 96.48%**; **378/426 = 88.73%** belongs to the earlier 255-method selection. No full all-statements pass or separate QA/instructor approval is inferred from the narrower owner decision. HMS-19/#41 remains open and PR #74 remains draft.

The [new follow-up](evidence/hms19-all-statements-20261113/README.md) adds **33 isolated behavior tests** after independently reviewing the uncovered-line report. On clean source `ee52be71c808abbebceb3d135a4e9fa76f9ec53d`, tree `8dc30e872684019779869677cd00d6ff9400c7ae`, the original **255** exact methods still pass at **894/1,703 = 52.50%**. The explicit additive **288-method** selection passes at **946/1,703 = 55.55%**, with **zero database attempts** in either run. Both selections use the unchanged harness, application denominator and exact method-only credit; no original method was removed. [Baseline evidence](evidence/hms19-all-statements-20261113/measurement-baseline.json) and [expanded evidence](evidence/hms19-all-statements-20261113/measurement-expanded.json) include exact IDs/outcomes, source hashes, dependencies, settings, timestamps and all per-file line sets.

All **52 previously missing callable-body statements** now execute under selected methods. The remaining **757** statements are declaration/import lines executed outside those contexts (731 during startup and 26 during later runner activity). For this unchanged source/method the optimistic ordinary-method ceiling is **946/1,703 = 55.549031%**. The target needs **1,193** covered statements, leaving **247** beyond that ceiling. Reads/assertions about a field do not retroactively execute its declaration line. The subsequent owner record accepts 946/946 (100%) under its function-body interpretation. It does not make the all-statements criterion reach 70%; the 55.55% result and this ceiling remain applicable when declarations stay in that denominator. The [verification](evidence/hms19-all-statements-20261113/verification.json) preserves the declaration line sets and ceiling assumptions.

The full local MySQL regression passed **all 12 gates** with **476 methods: 475 PASS, one expected coverage/timing SKIP**; the same timing test passed separately without coverage. Nine separate owned integration recipes passed. Recovery safety **32/32**, runner safety **7/7** and measurement-helper contracts **6/6** passed. The full and owned runs are honestly precommit/dirty; their surrounding source fingerprints match the later clean unit runs. [All mixed-suite JUnit outcomes](evidence/hms19-all-statements-20261113/junit-summary.json) reconcile with the manifest. Full configured mixed coverage is **1,782/1,798 statements**, **435/440 branches**, **99.06% combined**; it includes startup and integration execution and does not establish unit70. No test counts are added across runs or Python jobs.

New isolated units cover account/hostel/student permissions and invalid forms, allocation eligibility/search/history, receipt and payment errors, report dispatch, invalid dates and amount boundaries, inactive allocation mutation guards, queryset/save delegation, first full reversals, command retention options and exhausted demo beds. Module counts, synthetic fixtures, mocked boundaries, reproduction commands and the independent-review changes are detailed in the follow-up. No production code, historical evidence, `.coveragerc` or threshold changed in this follow-up; the earlier partial-room-save fix remains covered by its separate unit/integration regressions.

**Matching CI verified:** [run 43440707669](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/43440707669) passed both Python 3.11.18 and 3.14.10 jobs with MySQL 8.4.13. Candidate `0d6d292df0c82b3f07babb911a1b16f387a165cd` and actual synthetic merge checkout `5d508bd84592b9da07e5fe7789eb74549624bdbe` share tree `d7b1023dcdd585f87318ce5ad8aa27a3e058b38c`. Both clean jobs reconcile all 12 gates, 476 exact mixed identities (475 PASS/one expected timing SKIP), separate timing PASS, nine owned recipes, exact 255/288 isolated PASS selections, zero database attempts and the same 178 frozen source pins. Per-file attribution matches the local clean measurements. Six downloaded ZIP digests match GitHub. The [durable independent extraction](evidence/hms19-all-statements-20261113/ci-summary.json) retains source/job/artifact and JUnit reconciliation. A later documentation commit recording these results is separate from the tested candidate; older historical CI below certifies its own revisions only. Formal teammate review, remaining #41 acceptance checks and final submission selection remain separate. Completing more ordinary behavior assertions cannot reach 70% under the all-statements method. Meeting that criterion would need a defensible declaration-attribution rule retaining its denominator and excluding unrelated/shared execution. Adopting the recorded narrower owner interpretation is a different explicit acceptance boundary, rather than an improvement of the all-statements measurement; both records and results remain disclosed.

## Historical snapshots

The sections below preserve earlier evidence and its original scope-pending interpretations. Their source revisions, test counts, and original interpretations remain historical. The later owner decision applies to the narrower function-body boundary; it does not rewrite the all-statements measurements.

**Current independent development follow-up — 13 November:** [255 frozen isolated methods passed](evidence/hms19-unit-review-20261113/README.md) on clean source `d990a3e1fa484c198c2649463181c10ef569095a`, tree `f668ffc4cc74f8f9ef0c0bf2e359f6d48bb07326`, with zero database attempts. There are 58 new isolated methods and three separate MySQL regression methods, including a fix for excluded room fields incorrectly changing beds during partial saves. The full local mixed run passed all 12 gates: 443 methods, 442 PASS and one expected timing SKIP; timing passed separately. That full run is honestly recorded as dirty/precommit, with matching source fingerprints around it. The isolated run is clean and exact-revision bound.

**Current independent CI verification:** [run 43435199043](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/43435199043) passed both Python 3.11 and 3.14 jobs for PR head `029e21d4d4a9d1580fdc032f5f959379c3ee3c91`. Actual checkout `7738622931e07427b340bf0963c675339a66f049` has the identical candidate tree `b8f19067063221f0bc47f7e60b8edec8dfd41217`. Both clean jobs reconcile all 12 gates, 443 distinct mixed identities (442 PASS/one expected SKIP), separate timing PASS, nine owned integration recipes, and 255 exact isolated PASS identities with zero database attempts. All 171 frozen input hashes and both coverage diagnostics match the local clean run. Six downloaded artifact ZIP digests match GitHub's digests; the [durable CI extraction](evidence/hms19-unit-review-20261113/ci-summary.json) preserves the checked sources, outcomes and artifact provenance. These are technical checks, not a QA scope decision or final submission selection.

| Current isolated observation | Result | Scope limit |
|---|---:|---|
| Full-file method-context statement diagnostic | **894/1,703 = 52.50%** | Retains all configured application files; imports/declarations outside methods receive no credit. |
| Separate function-body statement diagnostic | **894/946 = 94.50%** | Exact AST rule and every included/excluded line are published; genuine declarative application rules remain outside this denominator. |
| Application branch diagnostic | **378/426 = 88.73%** | No new branch threshold is inferred. |

**SRS §6.4 unit70: UNPROVEN pending actual scope acceptance.** The old full-file method-only attribution has an ordinary-method ceiling of 928/1,685 = 55.07% because 757 import/declaration statements execute before methods. Adding tests alone cannot make that particular diagnostic reach 70% without crediting other execution. The new behavior diagnostic exceeds 70% under its stated scope, but it is a proposal requiring QA/owner assessment of declarative rules and attribution; it is not a silently accepted replacement. The threshold and `.coveragerc` were not changed. See the [exact selection](evidence/hms19-unit-review-20261113/scope.json), [clean measurement](evidence/hms19-unit-review-20261113/measurement.json), [full-suite identities](evidence/hms19-unit-review-20261113/junit-summary.json) and [verification/history](evidence/hms19-unit-review-20261113/verification.json). CI now records this frozen isolated measurement separately in both supported Python jobs. #41 remains open, and no final package or teammate approval is asserted.

**Earlier 13 November follow-up:** [257 selected tests passed](evidence/hms19-scope-20261113/README.md), including 171 new focused tests. The provisional method-context measurement covered 860/1,685 application statements (51.04%); its isolated subset covered 811/1,685 (48.13%). Imports and shared setup outside test contexts are not credited. The separate mixed regression run passed all 12 gates, with 382 tests run and one expected skip. HMS-19 remains open: the 70% unit-only requirement is not yet established.

**13 November test follow-up:** [151 selected component/isolated tests](evidence/hms19-scope-20261113/README.md) passed, including 65 new focused tests. Method-attributed application statement coverage was 586/1,685 (34.78%) under a provisional conservative boundary; an isolated-only subset covered 392/1,685 (23.26%). These are diagnostics, not an accepted SRS result. The separate 276-method mixed suite passed with one expected skip, but its full runner failed its timing gate once (admin login 2.146 seconds); a later standalone timing rerun passed. HMS-19 and the unit-only 70% requirement remain open and UNPROVEN.

**Report status:** Evidence assembled; unit-scope acceptance pending. This report does not claim a formal SRS unit-coverage PASS or FAIL.

**CI baseline reported below:** main merge `24e12526a771d1ec9d3545de78512ed3fc229abe`, tree `c5dfa2d8f482ee023417db5967133f2881513f6a`. The exact pull-request head tested by CI was `2714884997b43cf3805b86d9180568f7f41ea9b1` with the same tree. A later local run is separately identified below. This report is published as a candidate and still needs independent review.

## Project and testing overview

HMS supports student records, hostel and bed management, allocations, payments, reporting and access control. The verification evidence covers validation and small logic contracts, model/form/view components, database-backed workflows, concurrency, security-related behavior and verification tooling. Unit, component, integration and system results have different scopes; an automated test does not by itself complete a manual acceptance case.

The ten separately verified isolated additions cover password-backend decisions (2), allocation date/status rules (3), shared JSON validation responses (4), and a payment status rule (1). The earlier 190-method classification lists 85 component candidates, 87 integration, five concurrency, four system-surrogate and nine tooling methods. Those categories are proposals describing the earlier inventory, not a final approved unit-only selection.

## Execution snapshots and coverage gate

Results below are separate runs, not additional sets of unique tests to add together. Coverage figures are for the configured **mixed** suite, including measured verification tooling; they are not unit-only application-logic coverage.

| Evidence | Source and scope | Result |
|---|---|---|
| PR #67 follow-up | Local source base `482ef795e0c538f1bf25b9a2f79266051727ab7e` plus four new test files; dirty worktree. The [follow-up](evidence/coverage-followup-20261109/README.md) also links PR and merged-main CI for merged source `7556822df38b23d4f302cf68d857bb35b963ff10`. | 200 mixed methods: 199 PASS, one expected timing SKIP; timing passed separately. All 12 local gates passed; 10 isolated additions passed separately. Mixed statement coverage 1,590/1,772 (89.73%), branch coverage 348/424 (82.08%), combined (1,590+348)/(1,772+424) = 88.25%, passing the configured 70% gate. |
| PR #68 exact-tree CI | Head `2714884997b43cf3805b86d9180568f7f41ea9b1`, same tree as merge `24e1252`; Python 3.11 and 3.14 with MySQL 8.4. | 209 mixed methods per job: 208 PASS, one expected timing SKIP, no failures/errors; separate timing PASS and all 12 gates passed. [CI metadata](evidence/unit-test-report-20261110/current-ci-summary.json) |
| HMS-17 local follow-up | Base `65d6c1233b1b184858b36ff93cd32e440534ebbb` plus the documented test/evidence changes in a dirty worktree; Windows, Python 3.14.0, MySQL 8.0.46. | 211 mixed methods: 210 PASS, one expected timing SKIP; separate timing PASS and all 12 gates passed. [Source-bound execution record](evidence/issue39/completion-20261110/README.md) |

The configured 70% combined gate is a repository verification threshold. The submitted SRS §6.4 separately requires unit tests to cover at least 70% of application logic. The teammate's 13 November report says a guide/project owner approved using the combined metric for the project gate; a dated approval and its precise scope are not included in the available evidence. The mixed-suite PASS above is therefore not an accepted unit-only SRS PASS. Obtain and link any actual approval or amendment before relying on it as an interpretation of the SRS requirement.

The PR #67 follow-up also identifies two demo-data management commands with 98 statements and 32 branch outcomes that were unexecuted in that run. They remained in its configured denominator. The 10 isolated tests are included in the 200 ordinary methods; the nine separate integration/regression recipes and the 32 recovery-safety and seven runner-safety methods are separately reported, not added to the ordinary test count.

## Purpose and scope

This report separates component-unit candidates from integration, concurrency, system-surrogate and tooling checks. The full verification suite is mixed-level. Its 70% configured combined statement/branch gate is distinct from SRS §6.4's requirement for unit tests to cover at least 70% of application logic.

The coverage owner's frozen classification is retained as an earlier proposal: 190 methods were classified as 85 primary component candidates, 87 integration, 5 concurrency, 4 system-surrogate and 9 tooling methods. The exact conservative selection contains 76 methods; the sensitivity selection contains 100. The selection was frozen before its original rates. See the [classification](evidence/issue42-final/method-classification.json), [attribution](evidence/issue42-main/attribution.json), [JUnit summary](evidence/issue42-main/junit-summary.json), [coverage report](Code_Coverage_Report.md) and [branch report](Branch_Coverage_Report.md).

The PR #68 209-method CI suite includes 19 methods added after that frozen 190-method inventory. Their outcomes are verified, but no exact-source, separately attributed unit-coverage run has classified and measured a final approved unit scope. The 19 additions are disclosed below rather than silently folded into the frozen 76/100 selections. The later local run has 211 methods, as recorded above.

## Environment and execution evidence

| Item | Result |
|---|---|
| Exact-head CI | [GitHub Actions run 42569529411](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42569529411), on commit `2714884997b43cf3805b86d9180568f7f41ea9b1` |
| CI environment | Ubuntu; Python 3.11 and 3.14; MySQL 8.4 service; synthetic fixtures and isolated `test_hms` test database |
| Full verification | Both Python jobs passed all 12 repository gates |
| Ordinary mixed suite | 209 methods per job: 208 PASS, 0 failures, 0 errors, 1 expected timing skip |
| Timing | Separate uninstrumented timing smoke passed; the timing method's coverage skip is expected and is not an application failure |
| Owned expanded regression cases | Nine recipes passed in each CI job; these are separate integration/regression evidence, not additional JUnit identities |
| Configured full-project coverage | CI summary reports 88% and a pass against the unchanged 70% configured gate; this is a mixed-suite result, not SRS unit70 |
| Matching CI evidence | Both Python test-evidence artifacts and both owned-regression artifacts were downloaded on 10 November while unexpired. GitHub's originals expire 9 December 2026. The durable sanitized run metadata is in [current-ci-summary.json](evidence/unit-test-report-20261110/current-ci-summary.json). |

The CI workflow runs lint, format, dependency, Django, migration, static-file, test/JUnit, coverage and timing gates, plus separate recovery-safety, runner-safety and owned-regression checks. Its exact-head checks are successful. The raw Actions artifacts contain full logs/JUnit and remain available until their stated expiry; the committed summary preserves the tested revision, job outcomes, counts and artifact hashes without copying unnecessary raw logs.

## Current added test outcomes by module

These 19 methods were added after the frozen 190-method selection and all passed in both Python CI jobs. The scope labels below are conservative proposals based on what the assertions exercise; they do not change the historic classification artifact.

| Module | Added methods | Outcome | Proposed level / note |
|---|---:|---|---|
| Accounts | 11 | 11 PASS | Two `SimpleTestCase` backend regressions are isolated component candidates; seven HMS-16 cases exercise multi-model authorization/audit workflows and are integration tests; two view/security assertions remain component candidates for independent boundary review. |
| Allocations | 3 | 3 PASS | `SimpleTestCase` validation against unsaved models and fixed dates; component-unit candidates. |
| HMS shared responses | 4 | 4 PASS | `SimpleTestCase` JSON validation-response contracts; component-unit candidates. |
| Payments | 1 | 1 PASS | `SimpleTestCase` fee/status rule with plain input data; component-unit candidate. |
| **Total** | **19** | **19 PASS** | Ten new isolated methods have separately documented 10/10 PASS evidence; seven HMS-16 multi-model methods have focused 7/7 PASS evidence. The remaining two view checks are included in the exact-head full-suite CI. |

The 10 isolated additions are documented with source hashes, assertion boundaries and a no-database execution in [coverage-followup-20261109](evidence/coverage-followup-20261109/README.md). The seven focused HMS-16 tests and their run provenance are in [issue38-execution-20261109](evidence/issue38-execution-20261109/README.md). Current full-suite JUnit outcomes are in the linked exact-head CI artifacts. Test statuses do not themselves establish what percentage of application logic an accepted unit-test scope covers.

## Coverage interpretation

The 6 November coverage publication on clean source `b936e4d8ef7efd37dd66fde022efcb44e5b386ee` reports the mixed suite at 1,584/1,772 statements (89.39%) and 342/424 branch outcomes (80.66%), with a configured combined gate of 87.70%. The frozen standalone 76-method proposal passed 76/76. On that same older source, startup/shared-setup-inclusive application execution was 1,127/1,677 statements (67.20%); exact method-context execution was 414/1,677 (24.69%). These are different diagnostic observations, not the formal SRS unit-coverage result.

The later 10-method isolated supplement passed 10/10 and the PR #68 209-method MySQL CI passed. Neither adds a separately attributed coverage measurement for an approved unit scope on its tested source tree. That CI's 88% mixed result must not be relabelled as unit coverage. The threshold, `.coveragerc` exclusions, source denominator and frozen selection were not lowered or altered to achieve a target.

**SRS §6.4 unit application-logic coverage of at least 70%: UNPROVEN.** An accepted unit boundary, application-logic denominator, and exact-source attribution run remain necessary before PASS or FAIL can be concluded. Do not infer unit coverage from test counts, mixed coverage, startup execution or the standalone proposal's aggregate.

## Cases, defects and limitations

- The case register remains the source of case IDs, expected/actual results, owners and links. Automated suite methods are not counted as completion of manual/system acceptance cases.
- The 19 new methods all passed on the exact PR #68 CI head. No new test failure or defect is indicated by that run. Defects and retests from the broader Part 3 execution remain in the System Validation Report and case evidence.
- MySQL 8.4 is the workflow's database service and differs from the Test Plan's MySQL 8.0 baseline; acceptance of that environment substitution remains a team/QA decision.
- The tested revision is not yet a selected final submission package. Independent review of this report and actual QA/Dev/PO approvals remain pending.
- This report does not close #41, accept the unit70 scope, or declare the project ready to submit.

## Reproduction and evidence

The matching CI run is [42569529411](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42569529411). Re-run its workflow on the accepted final revision rather than treating an older report as final. To reproduce locally, use the repository's documented dependency and MySQL setup and run database suites serially:

```text
python scripts/run_checks.py --output-dir test-results/<new-run>/checks
python -m unittest discover -s scripts/part3 -p test_issue40_recovery_safety.py -v
python -S -m unittest discover -s scripts/part3 -p test_owned_runner_safety.py -v
python scripts/part3/run_owned_regressions.py --output-dir test-results/<new-run>/owned
```

Do not run competing suites against `test_hms`. Keep credentials, real student information, database dumps and unredacted scanner output out of the repository. See [current CI metadata](evidence/unit-test-report-20261110/current-ci-summary.json) and the linked historical coverage evidence for scope, commands, raw-artifact hashes and interpretation limits.

## Review disposition

This is an evidence-backed report contribution by Sreeharsha (`harsha2240`) after being added as a co-assignee to #41. Vaishnavi remains the QA coordinator. Independent QA review must confirm or revise the proposed boundaries, agree the application-logic denominator and issue the SRS unit70 disposition. Until that review and any required exact-source measurement are recorded, the report remains **UNPROVEN** for unit70 and the overall Part 3 package remains **NOT READY**.
