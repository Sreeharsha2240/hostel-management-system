# HMS-19 independent development follow-up — 13 November 2026

The clean isolated measurement tests commit `d990a3e1fa484c198c2649463181c10ef569095a`, tree `f668ffc4cc74f8f9ef0c0bf2e359f6d48bb07326`, on Windows/Python 3.14.7. The run started at 13:31:04 UTC and completed at 13:31:13 UTC. This is Devansh's development contribution to PR #74; Vaishnavi and Sreeharsha retain their assigned coordination and scope-acceptance responsibilities. No teammate signature or final submission acceptance is asserted.

## Test additions and defect correction

There are **58 new isolated tests and three separate MySQL integration regressions**. The frozen isolated selection contains **255 methods: the 197 existing isolated candidates plus these 58 additions**. The 60 database-backed methods in the historical 257-method component proposal are excluded from this isolated run. Their historical observations remain intact.

| New unit module | Methods | Assertion scope and related case support |
|---|---:|---|
| `accounts.test_private_middleware_units` | 6 | Private cache headers across anonymous, authenticated, login and logout transitions; supports TC-AUTH-04. |
| `allocations.test_view_error_units` | 14 | Malformed JSON/identifiers, missing records, domain errors, HTML/JSON contracts and supplied completion dates; supports TC-ALC-01/05/06. |
| `audit.test_view_units` | 5 | Action filters, complete actor/record/time serialization, real in-memory pagination and template context; supports TC-SEC-07. |
| `hostels.test_model_contract_units` | 16 | Safe mutation rules, fee validation, preserved allocation history, failure ordering and partial-save decisions; supports TC-HST-01/02. |
| `hostels.test_form_rule_units` | 5 | Active-bed capacity boundaries and actual model-field validators; supports TC-HST-01/02. |
| `payments.test_service_query_units` | 6 | Unevaluated billing expressions, deterministic allocation choice, independent payment totals, decimal fallbacks and caller scope; supports TC-PAY-02 and report components. |
| `students.test_form_contract_units` | 6 | Linked-login isolation and normalized/duplicate ID rules; supports TC-STU-01/02/04 and TC-SEC-02. |

These are support mappings to the existing [case register](../../Test_Case_Document.md). A method does not by itself complete every manual/browser/system subcondition. Mocked persistence decisions do not establish atomicity, locking or concurrency; query construction does not prove MySQL result semantics. Existing integration cases remain separate.

The new regressions exposed an existing `Room.save(update_fields=...)` defect. A fee-only save could rename or create beds from an in-memory room number/capacity that was excluded from the database update. The fix respects the explicit field set, uses locked persisted values for excluded synchronization fields, skips unrelated bed writes and preserves empty/iterable/positional field-set behavior. A seven-method isolated regression batch exposed the failure before the fix and passed afterward. Three new `hostels.test_partial_room_save` integration methods verify actual persisted fee-only, number-only and capacity-only updates, including preservation of maintenance status. All three passed on the disposable MySQL 8.4.9 instance.

## Measurement review and results

The original SRS §6.4 requires at least 70% unit coverage of application logic. It does not define a particular statement/branch formula. The Test Plan permits model/form/view component units and distinguishes ORM/MySQL integration. The updated isolated proposal conservatively requires database-forbidden `SimpleTestCase` methods, exact frozen IDs and zero database connection attempts. The harness blocks Django connections before setup/discovery and during execution, rejects database-enabled test classes, and reconciles discovery, execution and JUnit identities.

| Observation | Result | Interpretation |
|---|---:|---|
| Clean frozen isolated execution | **255 PASS**, no skips/failures/errors or database attempts | Exact IDs in [scope.json](scope.json); actual outcomes and provenance in [measurement.json](measurement.json). |
| Selected-method statements / all configured application statements | **894 / 1,703 = 52.50%** | Preserves the earlier conservative full-file diagnostic and all configured application files/exclusions. |
| Selected-method function-body statements | **894 / 946 = 94.50%** | Separate behavior diagnostic under the explicit AST rule below; its denominator excludes declaration-time logic. |
| Selected-method application branches | **378 / 426 = 88.73%** | Additional diagnostic; no new branch threshold is inferred from the SRS. |
| Full local mixed regression | **443 methods: 442 PASS, one expected timing SKIP** | All 12 gates passed; the same timing method passed separately without coverage. This was a dirty precommit run, not a clean-commit claim. |
| Full configured mixed coverage | **1,767 / 1,798 statements; 424 / 440 branches; 97.90% combined** | Includes verification tooling and startup; does not establish unit-only coverage. |
| Separate owned integration recipes | **9 PASS** | Separate cases, not nine additional ordinary-suite identities. |
| Offline safety suites | **32 recovery-safety PASS; 7 runner-safety PASS** | Separate tooling checks, not application units. |
| Measurement-helper contracts | **6 PASS** | Check AST boundaries, exact identities, JUnit reconciliation, rejected DB classes and portable hashes. |

The 257-method baseline was independently reproduced before the source fix: **860/1,685 = 51.04%** for its component proposal and **811/1,685 = 48.13%** for its isolated subset. The new room-save guards add 18 application statements and 16 branch outcomes; the denominator increase is a real source change, not a coverage exclusion. The full local run is labelled dirty/precommit in [verification.json](verification.json). Its 171 frozen source/configuration/harness hashes match the snapshots before and after that run and the later clean isolated run. [junit-summary.json](junit-summary.json) retains all 443 ordinary identities/outcomes and raw JUnit hashes.

### Why the earlier full-file method-only result cannot reach 70% by more ordinary assertions

At the baseline, the parser identifies **928 function-body statements and 757 import/declaration statements** among 1,685. Import/declaration execution occurs before ordinary method contexts, so those contexts can credit at most **55.07%** under this eager-import attribution. The current source similarly has **946 + 757 = 1,703**. No import reloads, statement deletion or denominator omissions were added to raise a percentage.

The behavior diagnostic selects executable statements within every function/async-function body in every configured application file. It also includes decorators of nested definitions created inside functions. It intersects those lines with the pinned coverage parser's executable statements, then credits only exact selected test-method contexts. The rule was selected before measuring the new tests, independently of which lines were hit. All included/excluded/executed line sets and source hashes are exported per file.

The excluded declarations contain genuine model validators/constraints, field definitions, routes, permissions and admin registrations. Tests inspect some of those contracts, but that does not make their declaration lines method-executed, and this metric does not quantify complete declarative-rule coverage. The 94.50% behavior result therefore **must not be silently substituted for the whole SRS requirement**. Standard startup/shared-setup-inclusive coverage also remains a separate observation. Startup, selected-method and other execution sets are retained without crediting startup as unit assertions.

**Formal SRS unit70 remains UNPROVEN pending the actual scope/attribution decision.** QA/owners must decide whether this behavior boundary, together with separately assessed declarative contracts, adequately represents application logic, or specify another defensible rule and rerun it. They must preserve the original 52.50% diagnostic and the missing conditions. The project threshold and tracked `.coveragerc` remain unchanged; issue #41 and PR #74 remain open/draft. Automated independent review is technical review, not fabricated human QA/PO acceptance.

## Reproduce and audit

Use the pinned development requirements and the documented Django environment. The isolated harness refuses database access; running it does not migrate, create or destroy a database. For ordinary/full and owned integration suites, use the documented disposable MySQL environment and run those suites serially.

```text
python docs/part3/evidence/hms19-unit-review-20261113/test_reproduce.py
python docs/part3/evidence/hms19-unit-review-20261113/reproduce.py --scope docs/part3/evidence/hms19-unit-review-20261113/scope.json --output-dir test-results/unit-review-NEW
python scripts/run_checks.py --output-dir test-results/full-review-NEW
python scripts/part3/run_owned_regressions.py --output-dir test-results/owned-review-NEW
```

Choose new output directories; previous attempts are preserved. The frozen scope verifies 171 source/configuration/harness hashes, including the workflow. Adding tests or changing source requires an explicitly reviewed new selection/hash record rather than silently growing module labels. New CI runs the frozen isolated measurement in both Python 3.11 and 3.14 jobs and publishes separate `hms-isolated-unit-evidence-*` artifacts. Those artifacts retain the 255-method JUnit, coverage contexts and source provenance for independent inspection. CI evidence is added separately after execution; no future run is presumed successful.

Source hashes normalize CRLF to LF. Selection hashes use sorted-key compact UTF-8 JSON with a final LF. The older `measurement-v11.json` selection digest hashes the CRLF representation, while Git stores LF; [verification.json](verification.json) preserves both exact digests and the explanation without rewriting historical files. It also records the initial formatting failure, safe preflight-blocked owned attempt, corrected form-test design error, and genuine pre-fix room regression. Earlier timing failures and the teammate's interrupted runs remain historical rather than being relabelled PASS.
