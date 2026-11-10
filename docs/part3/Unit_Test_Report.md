# Unit Test Report — Part 3

**Report status:** Evidence assembled; unit-scope acceptance pending. This report does not claim a formal SRS unit-coverage PASS or FAIL.

**Latest tested source:** main merge `24e12526a771d1ec9d3545de78512ed3fc229abe`, tree `c5dfa2d8f482ee023417db5967133f2881513f6a`. The exact pull-request head tested by CI was `2714884997b43cf3805b86d9180568f7f41ea9b1` with the same tree. The code/report change in PR #68 is merged; this report is a new contribution and still needs independent review.

## Purpose and scope

This report separates component-unit candidates from integration, concurrency, system-surrogate and tooling checks. The full verification suite is mixed-level. Its 70% configured combined statement/branch gate is distinct from SRS §6.4's requirement for unit tests to cover at least 70% of application logic.

The coverage owner's frozen classification is retained as an earlier proposal: 190 methods were classified as 85 primary component candidates, 87 integration, 5 concurrency, 4 system-surrogate and 9 tooling methods. The exact conservative selection contains 76 methods; the sensitivity selection contains 100. The selection was frozen before its original rates. See the [classification](evidence/issue42-final/method-classification.json), [attribution](evidence/issue42-main/attribution.json), [JUnit summary](evidence/issue42-main/junit-summary.json), [coverage report](Code_Coverage_Report.md) and [branch report](Branch_Coverage_Report.md).

The current 209-method CI suite includes 19 methods added after that frozen 190-method inventory. Their outcomes are verified, but no exact-source, separately attributed unit-coverage run has classified and measured a final approved unit scope. The 19 additions are disclosed below rather than silently folded into the frozen 76/100 selections.

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

The later 10-method isolated supplement passed 10/10 and the latest 209-method MySQL CI passed. Neither adds a separately attributed coverage measurement for the approved unit scope on the current source tree. The current CI's 88% mixed result must not be relabelled as unit coverage. The threshold, `.coveragerc` exclusions, source denominator and frozen selection were not lowered or altered to achieve a target.

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
