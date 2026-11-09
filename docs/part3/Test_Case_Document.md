# HMS Test Case Document and Requirements Traceability Matrix

## 1. Document information and revision history

| Field | Value |
|---|---|
| Project / team | Hostel Management System / Team 3 |
| Revision | Part 3 reconciliation, updated with HMS-16 transport/ZAP evidence 9 November 2026 |
| Code baseline inspected | `70c9fe20e462eb0b052e15434f19b347a793afa1` |
| Nine-case owner follow-up tested baseline | `6636098cb728aa17c2abf5e42c358a5d400261e7`; see section 5.6 |
| Case inventory | 33 original cases + 10 retained regression IDs + 14 new sprint-regression IDs + 4 explicit security/quality cases = **61** |
| Requirements | All original REQ-1..24 and NFR-1..12; separate SRS quality, BR and SO mapping |
| Data | Synthetic only; planned fixtures are distinguished from observed historical fixtures |
| Delivery state | Case-design/evidence reconciliation delivered; **whole-plan readiness NOT READY** |

| Date / source | Contributor | Actual contribution |
|---|---|---|
| 7 October, submitted Test Plan v1.2 | Sreeharsha, Vaishnavi, Devansh | Original plan/cases/RTM, strategy, security and traceability contributions as recorded in the submitted source |
| 5 November, PR #51 / `610ec1b` | Vaishnavi | Initial Part 3 document, original 33 and ten sprint regression IDs; retained historical 56/185-method summaries |
| 6 November, PR #54 | Devansh | Reconciled the 13 HMS-18 owner results and preserved raw partial/failure/retest evidence |
| 7 November, PR #58 | Vaishnavi | Published HMS-17 screenshots/manual record; reconciled six OWNER PASS, one NOT RUN and one PARTIAL |
| 7 November, case-document reconciliation | Devansh, with independent automated source/evidence reviews | Complete case fields, restored original steps/expectations, sprint additions, bidirectional RTM, source-bound evidence and explicit limitations |
| 8 November, HMS-26 / #63 | Devansh, with three independent automated reviewers | Executed nine remaining owned regression recipes on a clean reviewed commit; updated only their statuses and derived counts |
| 8 November, HMS-17 follow-up / PR #66 | Vaishnavi (publication); Devansh with three independent automated reviewers (technical reconciliation) | Added seven screenshots and historical raw CI; corrected unsupported complete passes; accepted S1-07/S2-07 for their existing automated scope, without claiming a new execution |
| 9 November, HMS-16 transport/ZAP follow-up | Sreeharsha owner evidence | Added isolated loopback HTTPS/TLS and passive ZAP evidence; recorded TC-SEC-06 as partial against its deployed-candidate prerequisite, TC-SEC-08 as partial pending QA disposition, and recalculated expanded totals |

Devansh authorized finishing and merging this documentation issue without collecting additional teammate messages. This is delivery authorization; no teammate signature, retrospective pre-execution QA approval, instructor waiver or final QA/Dev/PO acceptance is invented. Contributor ownership of execution and the remaining reports stays as recorded in issues #38-#43.

## 2. Authority and baseline preservation

The [official Part 3 PDF](SE_Mini_Project_Delivereables_Part-3.pdf) requires updating earlier cases for sprint changes, testing according to the submitted Test Plan during **2-6 November**, and four distinct reports under `docs/`. This reconciliation is dated 7 November and is not backdated into that window. The PDF gives no submission hour or export format.

The [submitted Test Plan DOCX](../../Test_Plan_Hostel_Management_System.docx) and [PDF](../../pdf/Test_Plan_Hostel_Management_System.pdf), [SRS](../../SRS_Hostel_Management_System.docx) and [SAD](../../SAD_Hostel_Management_System.docx) remain unchanged. Original section 13.1 steps and expectations are transcribed in section 13 below; formatting/line wrapping is normalized. Original IDs and every original core RTM mapping are retained. Added mappings supplement them. Detailed metadata and delivery workflow also satisfy issue #37; they are not extra faculty grading rules.

PR #36 actually merged on 2 November at 12:32:09 UTC as `649a4a5abe611c7970da3006902c64a505f27c46`. PR #44 fixed #45-#47; PR #49 fixed #48. The inspected code baseline includes those changes and the merged reports/evidence through PR #59. This chronology does not designate an accepted final submission build.

**TC-AUTH-03 wording decision:** preserve the original revealing expectation (quoted in its record), but use SRS REQ-2's generic credential response for the revised expectation. Five failures, rejection of correct credentials while locked, and recovery after 15 minutes remain mandatory. The historical SAD's revealing lockout text is an explicit cross-document discrepancy, not authority to weaken SRS security.

## 3. Scope, ownership and status conventions

Original execution ownership remains Sreeharsha's 12 authentication/security cases, Vaishnavi's eight student/hostel/quality cases, and Devansh's 13 allocation/payment/report/performance/recovery cases. Added cases follow the same module ownership; shared parser cases have component support without transferring other owners' deliverables.

| Status | Meaning |
|---|---|
| OWNER PASS | A retained owner execution observation; linked evidence/limits and independent acceptance must still be reviewed. It is not final QA acceptance. |
| PARTIAL | Some expected conditions have evidence; the full planned case is not established. |
| NOT RUN | No sufficiently scoped case-execution record is available; separately passing companions are shown without relabelling the case. |
| BLOCKED | A necessary input/decision for the complete case is absent. |
| FAIL / ERROR | Retain actual failing attempts and diagnostic evidence until a genuine retest; never erase or relabel them. |

An automated method and a planned case are different counting units. Adding a method mapping does not create a new run or convert an unverified UI/operational case to PASS.

## 4. Environment, planned data and declared deviations

Submitted Plan section 6: Python 3.11+, Django 5.x, MySQL 8.0; Windows 10+ **or** Ubuntu 20.04+; latest Chrome/Firefox/Edge and one real mobile phone. Planned tools include Django tests, Selenium, Postman, JMeter and ZAP. The SRS separately specifies broader Windows/Linux/latest-two-browser portability coverage; TC-QUAL-03 records it explicitly.

Current CI uses MySQL 8.4.13 on Linux with Python 3.11.18/3.14.10 and Django 5.2.19. HMS-18 uses Edge/Playwright and MySQL 8.4.9 in its recorded Windows environment; HMS-16/HMS-17 have their own MySQL 8.0 records. These substitutions and loopback HTTP results are usable as evidence with stated scope, but do not prove the submitted MySQL 8.0 environment, Selenium/Postman execution, real mobile coverage or deployed TLS. Acceptance of a requirement/tool deviation remains a real team/instructor decision; this document does not grant it.

### 4.1 Shared planned fixture

Use a disposable synthetic database and isolate independent cases. Active logins: `qa-admin`, `qa-warden`, `qa-student-a` linked only to student A, `qa-student-b` linked only to B, and `qa-student-unlinked`. Inject valid test passwords at runtime; no real credentials are recorded. `abc` is an intentional weak-password negative input.

Students A/B/C are `PES1UG24CS101` (Arjun QA, Male), `PES1UG24CS102` (Arun QA, Male), and `PES1UG24CS103` (Asha QA, Female). Provide date of birth, course/year, mobile/email, guardian name/mobile and optional address from each case's planned data. Use `example.test` addresses and dummy phone numbers. Plan two hostels, QA Boys/QA Girls: room 101 capacity 3 with 101-A/B/C; room 102 capacity 2; Girls room 201 capacity 1. Room fee is INR 10,000. Displayed dates: allocation 01-11-2026, transfer/payment 02-11-2026, vacate 03-11-2026. Submit ISO `YYYY-MM-DD` in JSON/form payloads and date-input values; the UI displays `DD-MM-YYYY`. Valid payment references use letters/numbers, for example `QAUPI0001`. Reset between cases. These are **future design fixtures**, not a claim they were used by every historical owner.

Performance fixtures retain 5,000 students/2,000 beds and 50 users/10 minutes where required. Recovery uses owned sandbox resources only. Historical HMS-18 fixtures (`issue40-warden`, `Issue40 Boys`, `I401-A`/`I402-A`) retain their recorded values and source; shared examples do not rewrite them.

## 5. Execution evidence and chronology

### 5.1 Historical focused run

PR #51 reports `python manage.py test students hostels --noinput`: 56 passed in 26.699 seconds, associated with base `649a4a5`. Its PR body explicitly records a dirty working tree. Raw local results are not committed. Retain this as an owner-reported historical summary, not exact-tree current acceptance.

### 5.2 Historical full run and current CI

PR #51 reports 185 mixed methods (184 passed, one skipped), a separate timing PASS and 12 passing gates; coverage 94.28% statements / 85.57% branches / 92.63% combined. The referenced local `test-results/20261105T042453664905Z` is not published evidence.

For the inspected `70c9fe2` tree, [main CI run 42397043317](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42397043317) passed both Python jobs. The [retained extraction](evidence/issue37/ci-methods.json) reconciles all **190 exact method identities** in each job: **189 PASS, one expected coverage timing skip**, 12 successful gates and a separate uninstrumented timing PASS. Its source JUnit/run hashes, command, platform and versions are retained. Each job also passed the 32 recovery-safety checks; those mocked/offline checks do not repeat the populated restore. No new local application, UI, full-load or recovery run is claimed by this documentation change.

### 5.3 HMS-18 owner execution and evidence reconciliation

Devansh Gupta's contribution, reconciled **6 November 2026**, supplies the 13 original allocation, payment, report, performance and recovery case results. The linked observations were executed **5 November** on clean `0e358b4ce1fd02366184c7cb9c312b47dd093214` (tree `c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0`). [PR #50](https://github.com/Sreeharsha2240/hostel-management-system/pull/50) published this evidence and was merged by `harsha2240` on **5 November at 06:31:28 UTC** as `8d60e83f1ce57ad99a2b2a22b3b5878f1390995b`. No formal `APPROVED` review is recorded.

The 13 linked **OWNER PASS** statuses below replace their stale NOT RUN entries. They record observed owner execution against the submitted Test Plan, with the originally pending technical QA dispositions now recorded in the [8 November scoped AI review](evidence/issue40-final/qa-review-20261108.md). Actual final human approvals remain pending. This update does not retroactively approve those entry criteria or accept the final submission build. Cases and statuses supplied by other owners are unchanged.

| Owned evidence | Observed result | Durable reference |
|---|---|---|
| Full mixed suite and focused checks | 190 methods: 189 PASS, one expected timing skip followed by a separate timing PASS; 71 focused methods and 32 recovery safety methods passed. These counts are not original cases or unit-only tests. | [Commands, environment and hashes](evidence/issue40-final/summary.json); [JUnit outcomes](evidence/issue40-final/junit-summary.json); [focused methods](evidence/issue40-final/focused-methods.json) |
| TC-ALC-01..06, TC-PAY-01..02, TC-RPT-01, TC-PERF-02 | Browser/HTTP/MySQL results include allocation, eligibility, transfer/release/history, payment receipts, required Bed and matching report formats; 20 committed allocations take 32.20–42.38 ms and overlapping conflicts preserve one winner. | [Browser observations](evidence/issue40-final/browser-results.json); [per-case actual results and defect/retest links](evidence/issue40-final/owner-cases.md) |
| TC-PERF-01 | 100 students / 80 beds; 50 users, each at least 600.106 seconds; 28,696 samples, zero errors, 99.99303% within two seconds. | [Full workload and retained failed attempt](evidence/issue40-final/load-results.json) |
| TC-PERF-03 | 5,000 students / 2,000 beds; 50 users, each at least 600.083 seconds; 29,096 samples, zero errors, every sample and search within two seconds. | [Full volume workload](evidence/issue40-final/load-results.json) |
| TC-OPS-01 | Naturally triggered daily sandbox backup, 5.379 seconds old; all 18 table counts/row/schema digests match after a separate populated restore. Live source and its installed daily task were preserved; owned resources were cleaned up. | [Recovery and cleanup](evidence/issue40-final/recovery-results.json); [reproduction](evidence/issue40-final/README.md) |

TC-ALC-05's raw browser result remains **PARTIAL** for fault injection; its linked, passing automated companion proves rollback and retry of the same transfer. The combined owner result records that qualification. The first volume attempt remains **FAIL** with 75 errors in 21,650 samples; the final volume result uses the complete unchanged-threshold rerun, not removal or relabelling of failed samples.

The [owner appendix](evidence/issue40-final/owner-cases.md) preserves original prerequisites, steps, expected and actual results, 14 SRS requirement mappings, source hashes and #45–#48 defect/retest references. The original plan has no per-case priorities; the 8 November AI review adopts nine High/four Medium for #40 only, without inferring historical or whole-team High-priority acceptance. Edge/Playwright in place of Selenium, MySQL 8.4.9 in place of 8.0, and loopback HTTP test flags are explicitly dispositioned as bounded #40 technical evidence in that review; original environment targets and whole-plan acceptance remain unchanged. Load and recovery figures describe their recorded source and host; they are not new measurements on this document's revision. All historical JSON remains unchanged. Whole-plan entry/exit criteria, integrated reporting and actual QA/Dev/PO approvals remain pending with #37/#38/#43.

<a id="54-manual-browser-testing--hms-17"></a>

### 5.4 Manual Browser Testing - HMS-17

The [owner manual record](evidence/issue39/manual-execution-20261107.md) reports eight case IDs exercised on 7 November, bound to application `c9f30a48c6dc54ccaec799156f3e52fe7bc8666a`, Windows/MySQL 8.0, Firefox and Edge, synthetic data. The [evidence index](evidence/issue39/README.md) and retained screenshots support the reviewed disposition: **6 OWNER PASS, 1 PARTIAL (TC-QUAL-01), 1 NOT RUN (TC-STU-01)**. The raw owner record remains unchanged and its different seven-pass summary is an unverified owner report for STU-01, not an accepted additional pass.

The later [PR #66 follow-up](evidence/issue39/followup-20261108.md) adds a visible student-list result, allocation-success result, bed/filter observations and three desktop Chrome pages. Their capture date/build/version are unrecorded; they are not silently assigned the historical metadata above. STU-01 still lacks its registration submission/success sequence; QUAL-01 still lacks the timed new-warden guide task and complete latest-browser main flows. The SRS latest-two/browser/server targets and real-mobile execution remain incomplete. HST-01 retains its historical reported result without a named case screenshot.

### 5.5 HMS-16 authentication/security handoff

The [owner report](System_Validation_Report.md) and [focused evidence](evidence/issue38/README.md) report 47 focused MySQL-backed methods passing on `8322b4c20c067d512c4bb439fdedd19d4fa27223` (5 November), with **11 OWNER PASS / TC-SEC-06 PARTIAL**. They contain command/environment and per-case mappings but no committed raw case-level JUnit. Preserve the older Windows harness failure and inconsistent count as historical/unreconciled; current Linux CI does not prove that Windows-only root cause. Original subconditions absent from the retained focused evidence remain visible in the records below.

TC-SEC-06 requires a real HTTP-to-HTTPS exchange, TLS scan accepting only TLS 1.2+, and actual authenticated Secure/HttpOnly session cookies. A real isolated HTTPS endpoint is sufficient; public hosting is unnecessary. Test-client `secure=True` and `check --deploy` do not prove transport. Test Plan section 5.1 separately requires a ZAP baseline, made explicit as TC-SEC-08.

### 5.6 HMS-26 remaining Devansh-owned regression execution

On 8 November, [#63 owner evidence](evidence/issue63/README.md) records the clean
`6636098cb728aa17c2abf5e42c358a5d400261e7` / tree `0faea77304a30ceb436e1411a2c513dd1f3c6f44` run of TC-REG-S2-08..16:
**nine PASS** with complete case-specific observations. The
[pre-execution technical review](evidence/issue63/pre-execution-review.md)
preceded this committed execution. A separate same-commit core run passed all
12 gates and 190 mixed methods (189 PASS, one expected timing SKIP), with a
separate timing PASS. Seven runner-safety and 32 recovery-safety checks passed.
These explicit integration cases do not change ordinary discovery or unit70.
Review/execution is late against the original 2–6 November window. Historical
entry approval, original environment targets and final human decisions remain
unproven; the original browser/load/recovery evidence is not relabelled.

### 5.7 HMS-17 follow-up and historical automated-scope reconciliation

The [8 November follow-up review](evidence/issue39/followup-20261108.md) links seven new screenshot observations and the complete original PR #58 CI bundles. The clean tested source is `32e6f563335a1ed20e2c6f619ba7e82de56dbd1f`, executed 7 November; it is not a fresh PR #66 browser run. Source and raw JUnit reconciliation establish S1-07 (five methods) and S2-07 (six methods) for their automated integration scope in both Python jobs. Their case records now bind actual steps/results to that historical execution. A separately named rerun is not required merely because the recipe was specified later. S1-07 uses the observed Student fixture; S2-07 navigation means rendered link presence, with response-wide date assertions. No complete original browser/portability case or whole-plan acceptance is inferred. Other proposed complete-pass changes lack sufficient scoped evidence and retain NOT RUN. #39 remains OPEN.

## 6. Counts, metrics and defect/retest interpretation

Current original-case evidence disposition is **31 OWNER PASS, 1 PARTIAL, 1 NOT RUN = 33**. Thus evidence reports 32/33 cases exercised (96.97%), 31/33 passing owner observations (93.94%), 1/33 partial (3.03%) and 1/33 not run (3.03%). TC-SEC-06's loopback evidence is limited to the local test instance; these percentages describe owner observations, not QA-accepted exit criteria. They do not remove other case evidence gaps.

Expanded register (61-case design denominator; case-level status distinct from method outcomes; updated 9 November for the completed passive ZAP execution):

| Disposition | Cases | Percentage |
|---|---:|---:|
| OWNER PASS | 51 | 83.61% |
| PARTIAL | 3 | 4.92% |
| NOT RUN | 6 | 9.84% |
| BLOCKED | 1 | 1.64% |

The ten existing regression IDs retain their historical owner observations except S1-05, whose combined-filter navigation gap is PARTIAL with passing method support. Of fourteen new regression recipes, nine Devansh-owned cases have complete reviewed execution records and OWNER PASS; the later PR #66 technical reconciliation accepts S1-07/S2-07 against their historical raw automated execution, while three other-owner recipes remain NOT RUN. Expanded any-exercise count is 54/61 (88.52%), including PARTIAL; owner-pass observations are 51/61 (83.61%). The 9 November loopback TLS probe supplies all specified TC-SEC-06 network conditions, so its current owner observation is OWNER PASS within that isolated test environment; this does not certify a public or production host. The passive ZAP run changes TC-SEC-08 from NOT RUN to PARTIAL: its 10-URL scan and two remaining alert dispositions are documented, but QA disposition remains pending. Other scan/quality cases retain their actual missing/blocked evidence. Do not silently retain the old 43-case denominator when applying a 100%-planned-cases exit criterion.

Test Plan section 14 also requires defect density (defects/module), aging (days open), and requirement coverage. Known linked development defects #45-#48 are closed with retest references in the HMS-18 appendix; the failed volume attempt (75 errors / 21,650 samples) and its complete unchanged-threshold rerun remain retained. No complete severity-ranked defect inventory or accepted requirement-by-requirement pass assessment is recorded, so whole-plan defect density/aging, zero-critical/high status and complete accepted coverage are **UNVERIFIED**, not zero. Calculate them from actual issue creation/closure/severity and reviewed case evidence in the integrated System Validation Report. A mapped requirement or a single partially relevant passed method is not full requirement acceptance (notably NFR-5, NFR-9 and NFR-12).

## 7. Detailed test case index

Every original and existing regression ID links to its complete source-bound record in section 13. Priority proposals originate on 7 November; original per-case priorities were unspecified and are not retrospectively approved. The nine #63 entries identify the later scoped technical review; its dispositions do not supply whole-team acceptance.

| Case | Owner | Proposed priority | Disposition |
|---|---|---|---|
| [TC-AUTH-01](#case-tc-auth-01) - Valid login | Sreeharsha | High (proposed) | OWNER PASS |
| [TC-AUTH-02](#case-tc-auth-02) - Invalid login | Sreeharsha | High (proposed) | OWNER PASS |
| [TC-AUTH-03](#case-tc-auth-03) - Account lockout after failed attempts | Sreeharsha | High (proposed) | OWNER PASS |
| [TC-AUTH-04](#case-tc-auth-04) - Logout and session timeout | Sreeharsha | High (proposed) | OWNER PASS |
| [TC-USR-01](#case-tc-usr-01) - Admin manages user accounts | Sreeharsha | High (proposed) | OWNER PASS |
| [TC-STU-01](#case-tc-stu-01) - Register student (valid data) | Vaishnavi | Medium (proposed) | NOT RUN |
| [TC-STU-02](#case-tc-stu-02) - Register student (invalid / duplicate) | Vaishnavi | Medium (proposed) | OWNER PASS |
| [TC-STU-03](#case-tc-stu-03) - Search students | Vaishnavi | Medium (proposed) | OWNER PASS |
| [TC-STU-04](#case-tc-stu-04) - Update student details | Vaishnavi | Medium (proposed) | OWNER PASS |
| [TC-STU-05](#case-tc-stu-05) - Deactivate student | Vaishnavi | Medium (proposed) | OWNER PASS |
| [TC-HST-01](#case-tc-hst-01) - Add hostel and room | Vaishnavi | Medium (proposed) | OWNER PASS |
| [TC-HST-02](#case-tc-hst-02) - Bed creation and availability list | Vaishnavi | Medium (proposed) | OWNER PASS |
| [TC-ALC-01](#case-tc-alc-01) - Allocate available bed | Devansh | High (proposed) | OWNER PASS |
| [TC-ALC-02](#case-tc-alc-02) - Block allocation of occupied bed | Devansh | High (proposed) | OWNER PASS |
| [TC-ALC-03](#case-tc-alc-03) - Block second allocation for a student | Devansh | High (proposed) | OWNER PASS |
| [TC-ALC-04](#case-tc-alc-04) - Gender and hostel type mismatch | Devansh | High (proposed) | OWNER PASS |
| [TC-ALC-05](#case-tc-alc-05) - Transfer student | Devansh | High (proposed) | OWNER PASS |
| [TC-ALC-06](#case-tc-alc-06) - Release allocation and history | Devansh | High (proposed) | OWNER PASS |
| [TC-PAY-01](#case-tc-pay-01) - Record payment and receipt | Devansh | High (proposed) | OWNER PASS |
| [TC-PAY-02](#case-tc-pay-02) - Payment status | Devansh | High (proposed) | OWNER PASS |
| [TC-RPT-01](#case-tc-rpt-01) - Occupancy report | Devansh | Medium (proposed) | OWNER PASS |
| [TC-SEC-01](#case-tc-sec-01) - Role-based access control | Sreeharsha | High (proposed) | OWNER PASS |
| [TC-SEC-02](#case-tc-sec-02) - Student sees only own data | Sreeharsha | High (proposed) | OWNER PASS |
| [TC-SEC-03](#case-tc-sec-03) - SQL injection and script injection | Sreeharsha | High (proposed) | OWNER PASS |
| [TC-SEC-04](#case-tc-sec-04) - Password storage and policy | Sreeharsha | High (proposed) | OWNER PASS |
| [TC-SEC-05](#case-tc-sec-05) - CSRF protection | Sreeharsha | High (proposed) | OWNER PASS |
| [TC-SEC-06](#case-tc-sec-06) - HTTPS and secure cookies | Sreeharsha | High (proposed) | OWNER PASS |
| [TC-SEC-07](#case-tc-sec-07) - Audit log | Sreeharsha | High (proposed) | OWNER PASS |
| [TC-PERF-01](#case-tc-perf-01) - Response time under load | Devansh | Medium (proposed) | OWNER PASS |
| [TC-PERF-02](#case-tc-perf-02) - Allocation time and concurrency | Devansh | Medium (proposed) | OWNER PASS |
| [TC-PERF-03](#case-tc-perf-03) - Data volume | Devansh | Medium (proposed) | OWNER PASS |
| [TC-OPS-01](#case-tc-ops-01) - Backup and restore | Devansh | High (proposed) | OWNER PASS |
| [TC-QUAL-01](#case-tc-qual-01) - Browser compatibility and usability | Vaishnavi | Medium (proposed) | PARTIAL |
| [TC-REG-S1-01](#case-tc-reg-s1-01) - Search 5,000 student records | Vaishnavi | Medium (proposed) | OWNER PASS |
| [TC-REG-S1-02](#case-tc-reg-s1-02) - Update student without changing Student ID | Vaishnavi | Medium (proposed) | OWNER PASS |
| [TC-REG-S1-03](#case-tc-reg-s1-03) - Create one Available bed per capacity unit | Vaishnavi | Medium (proposed) | OWNER PASS |
| [TC-REG-S1-04](#case-tc-reg-s1-04) - Reject capacity below active allocations | Vaishnavi | Medium (proposed) | OWNER PASS |
| [TC-REG-S1-05](#case-tc-reg-s1-05) - Combined bed filters and pagination | Vaishnavi | Medium (proposed) | PARTIAL |
| [TC-REG-S2-01](#case-tc-reg-s2-01) - Transfer/release preserve history and actor audit | Devansh | High (proposed) | OWNER PASS |
| [TC-REG-S2-02](#case-tc-reg-s2-02) - Same bed/student concurrent allocation has one winner | Devansh | High (proposed) | OWNER PASS |
| [TC-REG-S2-03](#case-tc-reg-s2-03) - Concurrent payments receive unique sequential receipts | Devansh | High (proposed) | OWNER PASS |
| [TC-REG-S2-04](#case-tc-reg-s2-04) - Adjustments preserve original and validate net amount | Devansh | High (proposed) | OWNER PASS |
| [TC-REG-S2-05](#case-tc-reg-s2-05) - Occupancy HTML/CSV/JSON match with filter | Devansh | Medium (proposed) | OWNER PASS |
| [TC-REG-S1-06](#case-tc-reg-s1-06) - Empty student/hostel/room submissions are rejected | Vaishnavi | Medium (proposed) | NOT RUN |
| [TC-REG-S1-07](#case-tc-reg-s1-07) - Numeric bed-filter boundaries and escaped errors | Vaishnavi | Medium (proposed) | OWNER PASS |
| [TC-REG-S1-08](#case-tc-reg-s1-08) - Student/room changes roll back on audit failure | Vaishnavi | High (proposed) | NOT RUN |
| [TC-REG-S2-06](#case-tc-reg-s2-06) - Explicit Student login link scopes My Records | Sreeharsha / Vaishnavi | High (proposed) | NOT RUN |
| [TC-REG-S2-07](#case-tc-reg-s2-07) - My Records empty/access/navigation/date behavior | Sreeharsha | Medium (proposed) | OWNER PASS |
| [TC-REG-S2-08](#case-tc-reg-s2-08) - Allocation/release/transfer rollback and retry | Devansh | High (#63 technical review) | OWNER PASS |
| [TC-REG-S2-09](#case-tc-reg-s2-09) - Payments and original receipts are permanent | Devansh | High (#63 technical review) | OWNER PASS |
| [TC-REG-S2-10](#case-tc-reg-s2-10) - Rejected/failed payments preserve receipt counter | Devansh | High (#63 technical review) | OWNER PASS |
| [TC-REG-S2-11](#case-tc-reg-s2-11) - Competing corrections cannot over-reverse | Devansh | High (#63 technical review) | OWNER PASS |
| [TC-REG-S2-12](#case-tc-reg-s2-12) - Payment reports use correct totals, Bed and latest valid location | Devansh | Medium (#63 technical review) | OWNER PASS |
| [TC-REG-S2-13](#case-tc-reg-s2-13) - CSV text stays literal and report HTML escapes labels | Devansh | Medium (#63 technical review) | OWNER PASS |
| [TC-REG-S2-14](#case-tc-reg-s2-14) - Report empty/filter/format/method boundaries | Devansh | Medium (#63 technical review) | OWNER PASS |
| [TC-REG-S2-15](#case-tc-reg-s2-15) - Malformed JSON is a safe validation error | Devansh | High (#63 technical review) | OWNER PASS |
| [TC-REG-S2-16](#case-tc-reg-s2-16) - Typed JSON dates/references keep correct errors and state | Devansh | High (#63 technical review) | OWNER PASS |
| [TC-SEC-08](#case-tc-sec-08) - OWASP ZAP baseline on the running application | Sreeharsha | High (proposed) | PARTIAL |
| [TC-QUAL-02](#case-tc-qual-02) - Working-hours service availability | Sreeharsha | Medium (proposed) | NOT RUN |
| [TC-QUAL-03](#case-tc-qual-03) - SRS portability and real mobile coverage | Vaishnavi | Medium (proposed) | NOT RUN |
| [TC-QUAL-04](#case-tc-qual-04) - Application-logic unit coverage and maintainability | Vaishnavi (QA), Devansh (coverage evidence), Sreeharsha (PO review) | Medium (proposed) | BLOCKED |

## 8. Requirements Traceability Matrix (RTM)

The 36 core rows preserve every original Test Plan section 13.2 mapping; additions trace accepted implementation changes and missing original SRS scope. These are coverage **plans**, not accepted pass claims.

| Requirement ID | Mapped Test Case IDs |
|---|---|
| REQ-1 | TC-AUTH-01 |
| REQ-2 | TC-AUTH-02, TC-AUTH-03 |
| REQ-3 | TC-AUTH-04 |
| REQ-4 | TC-USR-01, TC-SEC-01 |
| REQ-5 | TC-STU-01, TC-STU-02, TC-REG-S1-06, TC-REG-S1-08, TC-REG-S2-06 |
| REQ-6 | TC-STU-02 |
| REQ-7 | TC-STU-03, TC-REG-S1-01 |
| REQ-8 | TC-STU-04, TC-REG-S1-02, TC-REG-S2-06 |
| REQ-9 | TC-STU-05, TC-REG-S1-08 |
| REQ-10 | TC-HST-01, TC-REG-S1-06 |
| REQ-11 | TC-HST-01, TC-REG-S1-03, TC-REG-S1-06, TC-REG-S1-08 |
| REQ-12 | TC-HST-02, TC-REG-S1-03, TC-REG-S1-04 |
| REQ-13 | TC-HST-02, TC-REG-S1-04, TC-REG-S1-05, TC-REG-S1-07 |
| REQ-14 | TC-ALC-01, TC-REG-S2-08, TC-REG-S2-15, TC-REG-S2-16 |
| REQ-15 | TC-ALC-02, TC-ALC-03, TC-REG-S1-04, TC-REG-S2-02 |
| REQ-16 | TC-ALC-04 |
| REQ-17 | TC-ALC-05, TC-REG-S2-01, TC-REG-S2-08, TC-REG-S2-15, TC-REG-S2-16 |
| REQ-18 | TC-ALC-06, TC-REG-S2-01, TC-REG-S2-08, TC-REG-S2-15, TC-REG-S2-16 |
| REQ-19 | TC-ALC-06, TC-REG-S2-01, TC-REG-S2-08, TC-REG-S2-12 |
| REQ-20 | TC-PAY-01, TC-REG-S2-03, TC-REG-S2-04, TC-REG-S2-09, TC-REG-S2-10, TC-REG-S2-11, TC-REG-S2-15, TC-REG-S2-16 |
| REQ-21 | TC-PAY-01, TC-REG-S2-03, TC-REG-S2-04, TC-REG-S2-09, TC-REG-S2-10, TC-REG-S2-11, TC-REG-S2-16 |
| REQ-22 | TC-PAY-02, TC-REG-S2-04, TC-REG-S2-11, TC-REG-S2-12 |
| REQ-23 | TC-RPT-01, TC-REG-S2-05, TC-REG-S2-12, TC-REG-S2-13, TC-REG-S2-14 |
| REQ-24 | TC-SEC-02, TC-REG-S2-06, TC-REG-S2-07 |
| NFR-1 | TC-PERF-01, TC-REG-S1-01 |
| NFR-2 | TC-PERF-02, TC-REG-S2-02 |
| NFR-3 | TC-PERF-03 |
| NFR-4 | TC-OPS-01 |
| NFR-5 | TC-STU-05, TC-ALC-06, TC-REG-S2-01, TC-REG-S2-04, TC-REG-S2-09 |
| NFR-6 | TC-SEC-04 |
| NFR-7 | TC-SEC-01, TC-REG-S2-07, TC-SEC-08 |
| NFR-8 | TC-SEC-02, TC-REG-S2-06, TC-REG-S2-07 |
| NFR-9 | TC-AUTH-04, TC-SEC-06 |
| NFR-10 | TC-SEC-03, TC-SEC-05, TC-REG-S1-06, TC-REG-S1-07, TC-REG-S2-10, TC-REG-S2-13, TC-REG-S2-14, TC-REG-S2-15, TC-REG-S2-16, TC-SEC-08 |
| NFR-11 | TC-SEC-07, TC-REG-S1-02, TC-REG-S2-01, TC-REG-S1-08, TC-REG-S2-08, TC-REG-S2-09, TC-REG-S2-10 |
| NFR-12 | TC-AUTH-03, TC-SEC-06, TC-SEC-08 |

### 8.1 SRS quality attributes, business rules and security objectives

Exact targets below come from SRS sections 6.3-6.5. They remain separate from the 36 core rows and the narrower original Plan environment. Mapping does not imply all conditions passed.

| SRS attribute/rule/objective | Submitted source text | Case mapping / evidence limit |
|---|---|---|
| Usability | A new warden can register a student and allocate a bed within 5 minutes using a one page user guide. | TC-QUAL-01. Actual new-warden registration and allocation with one-page guide, timed at no more than five minutes. Page inspection alone is insufficient. |
| Reliability | System available at least 99% of the time during office hours (8 AM - 8 PM) on working days. | TC-QUAL-02. No existing dedicated case establishes availability during office hours. Add an identified case with observation method/period and retain NOT RUN until measured. |
| Data Integrity | The database itself shall make sure a bed has at most one active allocation and a student has at most one active allocation. | TC-ALC-02, TC-ALC-03, TC-ALC-05, TC-REG-S2-02, TC-REG-S2-08. Check database enforcement and concurrent one-winner behavior; form rejection alone is insufficient. |
| Portability | Runs on both Windows and Linux servers; works on the latest two versions of Chrome, Firefox and Edge. | TC-QUAL-01, TC-QUAL-03. Extend original browser case to both server operating systems and latest two versions of all three browsers. Record actual versions and missing matrix entries. |
| Maintainability | Code follows PEP 8 and is split into separate Django apps per module; unit tests cover at least 70% of the application logic. | TC-QUAL-04. Add identified PEP 8/modular-app verification and reviewed unit-only application-logic coverage case. Mixed-suite coverage is not unit-only coverage. |
| BR-1 | A bed can have only one active allocation at a time. | TC-ALC-02, TC-PERF-02, TC-REG-S2-02. At most one active allocation per bed, including database/concurrent paths. |
| BR-2 | A student can have only one active allocation at a time. | TC-ALC-03, TC-PERF-02, TC-REG-S2-02. At most one active allocation per student, including concurrent paths. |
| BR-3 | Boys can be allocated only to Boys hostels and girls only to Girls hostels (domain requirement). | TC-ALC-04. Female student/Boys hostel is original mismatch fixture; also consider reverse mismatch in extended accepted-code coverage. |
| BR-4 | Only Admin can add or change hostels, rooms, beds and user accounts. | TC-USR-01, TC-HST-01, TC-HST-02, TC-SEC-01. Pair successful Admin operations with direct-route write denial for Warden/Student across users, hostels, rooms and beds. |
| BR-5 | A recorded payment cannot be edited or deleted; corrections are made by a new adjusting entry (domain requirement). | TC-PAY-01, TC-REG-S2-04, TC-REG-S2-09, TC-REG-S2-11. Original payment creation alone does not prove permanence. Add explicit edit/delete/replay denial and adjusting-entry validation. |
| BR-6 | A student can access only their own data. | TC-SEC-02, TC-REG-S2-06, TC-REG-S2-07. Cover own profile/allocation/history/payment data and linked/unlinked accounts, including modified identifiers. |
| SO-1 | Only authorised users can access the system and each user can only do what their role allows. | TC-AUTH-01, TC-AUTH-02, TC-AUTH-03, TC-AUTH-04, TC-USR-01, TC-SEC-01, TC-SEC-04, TC-SEC-05, TC-SEC-06. Authentication, roles on every request, passwords, session/transport protection and direct-route denial. |
| SO-2 | Allocation and payment records can only be created or changed through valid operations by authorised staff, and every change can be traced to a user. | TC-ALC-01, TC-ALC-05, TC-ALC-06, TC-PAY-01, TC-SEC-03, TC-SEC-05, TC-SEC-07, TC-REG-S2-01, TC-REG-S2-04. Valid staff operations, atomic transactions, server validation/CSRF and attributable audit; supplement rollback/payment-permanence coverage. |
| SO-3 | Personal details of students (contact, guardian and payment details) are kept confidential. | TC-SEC-01, TC-SEC-02, TC-SEC-06, TC-SEC-07. Own-data confidentiality, HTTPS and sanitized audit/logging; supplement profile/linking/self-service regressions. |
| SO-4 | The system stays usable for staff during office hours and resists simple attacks such as repeated password guessing. | TC-AUTH-03, TC-SEC-06, TC-PERF-01, TC-PERF-03, TC-OPS-01. Lockout, load and recovery support the objective but do not establish separate 99% office-hours availability. |

Allocation permanence additionally has `allocations.test_workflows.AllocationWorkflowTests.test_model_deactivation_and_history_cannot_bypass_guards` as a passing companion; payment permanence is explicit in TC-REG-S2-09. Original NFR-5-to-STU-05 is retained for historical traceability, with allocation/payment permanence now added rather than inferred from student soft deletion.

## 9. Test strategy and review disposition

The separate [#63 pre-execution review](evidence/issue63/pre-execution-review.md) accepts six High/three Medium priorities for the nine current automated recipes; their clean execution is in section 5.6. This does not resolve whole-plan High-priority acceptance.

The [8 November HMS-18 review](evidence/issue40-final/qa-review-20261108.md) adds issue-specific independent AI technical acceptance for the original 13 cases under Devansh's explicit authorization. Its current-priority, late-entry and environment decisions are bounded to #40; it does not execute separately specified regressions, change the status counts or supply named final approvals.

Original cases are system/browser or operational cases. Automated companions are model, form, view, integration/concurrency or parser checks as indicated in their records; the mixed suite is not all unit tests. Planned cases may be refined after implementation per Test Plan section 11, with IDs/history retained. Run affected checks after defects; preserve failed attempts and use isolated synthetic data.

Devansh's 7 November reconciliation proposes risk-based priorities, checks source/method identity, reconciles owner observations and exposes unproven conditions. Independent automated audits validate source fidelity, evidence links and mappings. These are current technical/document reviews. Historical execution predates this revision; the reviewed-case entry criterion is **not retrospectively satisfied**, and actual final QA/Dev/PO/guide approvals remain pending. Delivery proceeds under Devansh's explicit delivery authorization without additional teammate-message collection; it does not resolve instructor-controlled requirement changes.

Environment review records MySQL 8.4, Edge/Playwright and loopback HTTP as explicit evidence limitations; the original environment and transport targets are preserved. Method mappings indicate exactly what is asserted and what is absent. Case priority proposals require genuine agreement before reporting the High-priority exit criterion as met.

## 10. Automation and durable evidence

### 10.1 Automated Regression Test Mapping

The complete mapping below is checked against Python AST identities and the retained current CI extraction. Each listed regression companion passed in both CI jobs; its planned-case status still depends on the full expected conditions and review. Methods in a row are supporting assertions, not extra original test cases.

| Test Case ID | Automated Test Method | Scope |
|---|---|---|
| TC-REG-S1-01 | `students.tests.StudentManagementViewTests.test_student_search_handles_5000_records_within_two_seconds` | Integration / timing smoke |
| TC-REG-S1-02 | `students.tests.StudentManagementViewTests.test_admin_can_update_contact_course_and_year_but_not_student_id` | View / database integration |
| TC-REG-S1-03 | `hostels.tests.HostelModelBehaviorTests.test_room_creation_automatically_creates_beds` | Model / database integration |
| TC-REG-S1-04 | `hostels.tests.HostelModelBehaviorTests.test_capacity_cannot_be_reduced_below_active_allocations` | Model / database integration |
| TC-REG-S1-05 | `hostels.tests.BedFilteringViewTests.test_combined_filters_return_only_matching_available_beds`; `hostels.tests.BedFilteringViewTests.test_bed_list_is_paginated_and_keeps_filters_on_next_page` | View / database integration plus UI |
| TC-REG-S2-01 | `allocations.test_workflows.AllocationWorkflowTests.test_transfer_and_release_preserve_history_and_emit_actor_audit`; `allocations.test_workflows.AllocationWorkflowTests.test_history_orders_backdated_records_by_allocation_date_in_json_and_html`; `allocations.test_workflows.AllocationWorkflowTests.test_only_transfer_and_release_forms_require_submit_confirmation`; `allocations.test_workflows.AllocationWorkflowTests.test_model_deactivation_and_history_cannot_bypass_guards` | Service / API / HTML integration |
| TC-REG-S2-02 | `allocations.test_workflows.AllocationConcurrencyTests.test_simultaneous_same_bed_or_same_student_has_one_winner`; `allocations.test_workflows.AllocationWorkflowTests.test_database_rejects_forged_or_missing_active_keys` | MySQL concurrency integration |
| TC-REG-S2-03 | `payments.test_workflows.PaymentConcurrencyTests.test_simultaneous_payments_receive_unique_sequential_numbers` | MySQL concurrency integration |
| TC-REG-S2-04 | `payments.test_workflows.PaymentWorkflowTests.test_adjustments_preserve_original_and_validate_their_source_and_net_amount`; `payments.test_workflows.PaymentWorkflowTests.test_adjustment_cannot_predate_original` | Service / model integration |
| TC-REG-S2-05 | `reports.test_reports.ReportTests.test_occupancy_csv_and_html_match_json_and_preserve_filters` | Service / API / HTML integration |
| TC-REG-S1-06 | `students.tests.StudentManagementViewTests.test_empty_student_submissions_show_required_errors_without_saving`; `hostels.tests.HostelManagementViewTests.test_empty_management_submissions_show_required_errors_without_saving` | View / database integration |
| TC-REG-S1-07 | `hostels.tests.BedFilteringViewTests.test_invalid_numeric_filters_return_400_without_bed_results`; `hostels.tests.BedFilteringViewTests.test_invalid_floor_is_escaped_and_other_filter_values_are_preserved`; `hostels.tests.BedFilteringViewTests.test_zero_and_upper_boundary_floor_filters_match_only_their_beds`; `hostels.tests.BedFilteringViewTests.test_maximum_hostel_id_is_valid_and_has_no_matches`; `hostels.tests.BedFilteringViewTests.test_invalid_filters_do_not_bypass_login` | View / database integration |
| TC-REG-S1-08 | `students.tests.StudentManagementViewTests.test_student_creation_rolls_back_if_audit_recording_fails`; `students.tests.StudentManagementViewTests.test_student_deactivation_rolls_back_if_audit_recording_fails`; `hostels.tests.HostelManagementViewTests.test_room_creation_rolls_back_if_audit_recording_fails` | Fault-injected view / database integration |
| TC-REG-S2-06 | `students.test_self_service.StudentSelfServiceTests.test_student_account_picker_excludes_staff_and_accounts_linked_elsewhere`; `students.test_self_service.StudentSelfServiceTests.test_student_sees_only_own_allocation_and_payment_details` | Form / view / database integration plus UI link-save check |
| TC-REG-S2-07 | `students.test_self_service.StudentSelfServiceTests.test_empty_allocation_and_payment_history_is_explained`; `students.test_self_service.StudentSelfServiceTests.test_unlinked_student_login_gets_helpful_empty_state`; `students.test_self_service.StudentSelfServiceTests.test_dashboard_and_navigation_link_to_my_records`; `students.test_self_service.StudentSelfServiceTests.test_student_dates_are_dd_mm_yyyy_and_keep_vacated_fallback`; `students.test_self_service.StudentSelfServiceTests.test_only_student_role_can_open_self_service_page`; `students.test_self_service.StudentSelfServiceTests.test_login_is_required_for_self_service_page` | View / HTML integration |
| TC-REG-S2-08 | `allocations.test_workflows.AllocationWorkflowTests.test_audit_failure_rolls_back_allocation_and_release`; `allocations.test_workflows.AllocationWorkflowTests.test_transfer_failure_rolls_back_both_beds_and_history` | Fault-injected service / database integration |
| TC-REG-S2-09 | `payments.test_workflows.PaymentWorkflowTests.test_numbered_payments_are_permanent_and_audited_for_the_actor`; `payments.test_workflows.PaymentWorkflowTests.test_edit_delete_bulk_and_primary_key_replay_are_blocked` | Model / ORM / database integration |
| TC-REG-S2-10 | `payments.test_workflows.PaymentWorkflowTests.test_invalid_amounts_modes_dates_and_references_do_not_consume_numbers`; `payments.test_workflows.PaymentWorkflowTests.test_audit_failure_rolls_back_the_payment_and_receipt_counter`; `payments.test_workflows.PaymentWorkflowTests.test_receipt_range_exhaustion_fails_without_overwriting_history` | Service / model / database integration |
| TC-REG-S2-11 | `payments.test_workflows.PaymentConcurrencyTests.test_competing_corrections_cannot_reverse_a_payment_twice` | MySQL concurrency integration |
| TC-REG-S2-12 | `reports.test_reports.ReportTests.test_payment_report_sums_once_across_allocation_history_and_filters_last_room`; `reports.test_reports.ReportTests.test_payment_report_excludes_cancelled_locations_and_keeps_unassigned_blank`; `reports.test_reports.ReportTests.test_payment_report_csv_and_html_match_json_after_corrections`; `payments.test_workflows.PaymentWorkflowTests.test_status_tracks_pending_partial_paid_and_adjustments_without_join_multiplication`; `payments.test_workflows.PaymentWorkflowTests.test_no_allocation_or_unconfigured_fee_remains_pending_with_advance_payment` | Service / API / HTML integration |
| TC-REG-S2-13 | `reports.test_reports.ReportTests.test_csv_quotes_unicode_and_formula_text_and_html_escapes_names` | API / HTML integration |
| TC-REG-S2-14 | `reports.test_reports.ReportTests.test_empty_reports_and_invalid_filters_formats_and_methods`; `reports.test_reports.ReportTests.test_numeric_hostel_filter_accepts_leading_zeros` | API / HTML integration |
| TC-REG-S2-15 | `hms.test_http.RequestDataTests.test_malformed_json_and_invalid_utf8_raise_validation_error`; `hms.test_http.RequestDataTests.test_non_object_json_raises_validation_error`; `hms.test_http.RequestDataTests.test_container_field_values_raise_validation_error`; `hms.test_http.RequestDataTests.test_unpaired_unicode_surrogates_raise_validation_error`; `hms.test_http.RequestDataTests.test_nonfinite_numbers_are_rejected_including_exponent_overflow`; `hms.test_http.RequestDataTests.test_parser_recursion_error_becomes_validation_error`; `hms.test_http.RequestDataTests.test_deeply_nested_input_raises_validation_error`; `hms.test_http.RequestDataTests.test_json_object_preserves_finite_scalar_values`; `hms.test_http.RequestDataTests.test_valid_unicode_strings_and_surrogate_pairs_are_preserved`; `hms.test_http.RequestDataTests.test_form_encoded_data_is_returned_unchanged`; `allocations.test_workflows.AllocationWorkflowTests.test_json_workflow_conflicts_validation_and_permissions`; `payments.test_workflows.PaymentWorkflowTests.test_invalid_json_fields_missing_records_and_methods` | Parser unit checks plus API integration |
| TC-REG-S2-16 | `allocations.test_workflows.AllocationWorkflowTests.test_json_date_types_return_400_without_changing_allocations`; `allocations.test_workflows.AllocationWorkflowTests.test_json_reference_types_cannot_select_a_different_integer_key`; `allocations.test_workflows.AllocationWorkflowTests.test_json_form_errors_preserve_reference_and_validation_status_codes`; `payments.test_workflows.PaymentWorkflowTests.test_json_date_types_return_400_without_consuming_receipts`; `payments.test_workflows.PaymentWorkflowTests.test_form_encoded_missing_student_preserves_json_not_found_response`; `hms.test_forms.DateFieldTests.test_unexpected_json_types_produce_validation_errors`; `hms.test_forms.DateFieldTests.test_dates_text_and_optional_empty_values_keep_standard_behavior`; `hms.test_forms.ModelChoiceFieldTests.test_non_integer_json_keys_are_rejected_without_a_query`; `hms.test_responses.FormErrorResponseTests.test_invalid_reference_preserves_field_errors_and_returns_not_found`; `hms.test_responses.FormErrorResponseTests.test_other_invalid_choices_and_required_references_remain_bad_requests`; `hms.test_responses.FormErrorResponseTests.test_invalid_choices_require_an_explicit_reference_field_to_return_404` | Form unit checks plus API/database integration |

For the nine case-specific executions, run `python scripts/part3/run_owned_regressions.py --output-dir test-results/NEW-owned-cases` serially, after the offline safety checks; see [reproduction and evidence](evidence/issue63/README.md). Each changed case record links its exact explicit method; the table above retains historical companions.

Run `python scripts/run_checks.py` for repository checks, full mixed suite, coverage and separate uninstrumented timing. Run focused Django suites as needed. Preserve exact code SHA/tree, clean/dirty state, versions, commands, expected/actual results and evidence. The current extraction links the GitHub jobs and hashes the downloaded original inputs; it creates no fictitious local run. The Plan's JMeter, ZAP, actual browser/guide and populated-recovery work retain their distinct operational evidence requirements.

## 11. Entry and exit criteria

### 11.1 Original entry criteria

Test Plan section 5 requires **SRS approved; build deployed to test environment; data loaded; test cases reviewed**. Owner records establish local deployment/data for their own runs. Complete approved-SRS and pre-execution reviewed-case decisions for all batches are not recorded; no retrospective approval is inferred. New case design and current CI do not backdate that entry decision.

### 11.2 Original exit criteria

| Original criterion | Current disposition |
|---|---|
| 100% of planned test cases executed | NOT MET: original STU-01 lacks reconciled case evidence; partial/security/quality and added case-execution gaps remain visible. |
| All High-priority cases passed | UNVERIFIED: original case priorities were unspecified; current proposals and complete evidence require actual review. |
| Zero critical/high defects open | UNVERIFIED: no complete reviewed severity inventory is recorded; known fixed issues alone do not establish zero. |
| Every RTM requirement covered by at least one passed case | UNVERIFIED/PARTIAL: all 36 are mapped, but passed method/owner observations do not establish every full requirement. |

Actual QA/Dev/PO approvals (Plan section 15) and the project-guide acceptance walkthrough (section 5) remain separate final-readiness work. Any authorized instructor change must retain original unmet outcomes and record authority/date/rationale. **Whole-plan readiness: NOT READY.**

## 12. Revision notes and remaining execution

All 33 original IDs, ten existing sprint IDs and original 36-requirement mappings are preserved. This revision restores full original inputs/expectations, documents AUTH-03's wording resolution, supplies every case's owner/priority/type/level/setup/data/steps/expected/actual/status/SHA/evidence/defect fields, adds sprint/quality coverage and corrects the contradictory HMS-17 totals. The original owner manual record, historical JSON, failed load attempt, successful full rerun and raw transfer PARTIAL are preserved unchanged.

Issue #37 is the case-document/traceability delivery. This document does not complete #38's security/integrated report, #39's missing UI/quality evidence, #41's Unit Test Report or #43's real final approvals/submission. #40's separate technical QA delivery and #42's reporting delivery are closed; formal unit70 remains UNPROVEN. Original Test Plan/SRS/SAD DOCX/PDF baselines remain intact. The publication date and review scope are explicit.

## 13. Complete case records

For every record, **Priority review** distinguishes proposed planning from approved historical priority. **QA disposition** is separate from owner execution. A passing current method is supplementary evidence at `70c9fe2`; original owner results remain attached to the earlier SHA/date/environment actually observed.

### TC-AUTH-01: Valid login

<a id="case-tc-auth-01"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; High (proposed). Risk: authentication, privacy or security failure can expose protected data or operations.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-1

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden exists, active, correct role; browser logged out; deployed candidate ready. {"actor": "qa-warden", "password": "valid runtime-injected test value", "measure": "login-to-Warden-dashboard elapsed time &lt;=2 seconds"}

**Steps:**

Pre: Warden account exists.
1. Open login page.
2. Enter correct username and password.

**Expected:** Warden dashboard is shown within 2 seconds.

**Actual:** Owner reports valid login and role dashboard PASS; focused suite includes real credential login for each role and less-than-two-second login/dashboard timing.

**Execution status:** OWNER PASS

**Tested commit:** `8322b4c20c067d512c4bb439fdedd19d4fa27223`

**Execution date and environment:** Owner-reported focused execution on 5 November 2026: Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable loopback MySQL 8.0.46, synthetic fixtures; 47 PASS, zero failures/errors, 104.605 seconds. Published command and summary are retained; case-level raw JUnit is absent from issue38 directory.

**Evidence:** [evidence/issue38/README.md](evidence/issue38/README.md); [System_Validation_Report.md#hms-16-case-outcomes](System_Validation_Report.md#hms-16-case-outcomes)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`accounts.tests.AuthenticationTests.test_login_shows_role_dashboard_and_logout_clears_session`](../../accounts/tests.py#L28); [`accounts.tests.AuthenticationTests.test_each_role_can_access_dashboard_and_dashboard_reflects_role`](../../accounts/tests.py#L44); [`accounts.tests.AuthenticationTests.test_login_and_role_dashboard_respond_within_two_seconds`](../../accounts/tests.py#L74)

**Current companion outcomes:** 2 PASS and 1 expected timing SKIP in each current CI bundle; the uninstrumented timing-smoke step separately passed. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Role-content test uses force_login; actual credentials/timing use the timing method. No retained real-browser timing trace is claimed.

### TC-AUTH-02: Invalid login

<a id="case-tc-auth-02"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; High (proposed). Risk: authentication, privacy or security failure can expose protected data or operations.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-2

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden active/unlocked; separate clean sessions for comparisons. {"known_username": "qa-warden", "password": "intentionally wrong test value", "unknown_username": "qa-no-such-user", "message": "Invalid username or password"}

**Steps:**

1. Enter valid username with wrong password.
2. Enter an unknown username.

**Expected:** Message "Invalid username or password" is shown in both cases; the message does not say which field was wrong; user stays logged out.

**Actual:** Owner reports generic invalid-credential and locked-account responses PASS; wrong-password generic message is asserted and unknown username is exercised in audit tests.

**Execution status:** OWNER PASS

**Tested commit:** 8322b4c20c067d512c4bb439fdedd19d4fa27223

**Execution date and environment:** Owner-reported focused execution on 5 November 2026: Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable loopback MySQL 8.0.46, synthetic fixtures; 47 PASS, zero failures/errors, 104.605 seconds. Published command and summary are retained; case-level raw JUnit is absent from issue38 directory.

**Evidence:** [evidence/issue38/README.md](evidence/issue38/README.md); [System_Validation_Report.md#hms-16-case-outcomes](System_Validation_Report.md#hms-16-case-outcomes)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`accounts.tests.AuthenticationTests.test_invalid_password_is_generic_and_locks_after_five_attempts`](../../accounts/tests.py#L133); [`accounts.tests.AuthenticationTests.test_locked_account_keeps_generic_error`](../../accounts/tests.py#L147); [`audit.tests.AuditTests.test_unknown_username_failure_is_logged_without_storing_input`](../../audit/tests.py#L68)

**Current companion outcomes:** 3 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Unknown-username audit method checks log privacy, not exact generic wording or logged-out assertion for that request. Original two-input case requires review disposition.

### TC-AUTH-03: Account lockout after failed attempts

<a id="case-tc-auth-03"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Original expected (historical wording):** Step 2 is rejected with a lockout message; step 3 succeeds.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; High (proposed). Risk: authentication, privacy or security failure can expose protected data or operations.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-2, NFR-12

**Level:** System / operational; companions have component/integration scope

**Type:** Security

**Prerequisites and data:** qa-warden active with zero failed attempts and no lock; controlled clock or actual wall-clock start recorded. {"wrong_attempts": 5, "during_lock": "correct injected password", "retry": "same correct credential after15minutes"}

**Steps:**

1. Enter wrong password 5 times in a row.
2. Enter the correct password.
3. Retry after 15 minutes.

**Expected:** Five consecutive wrong passwords activate a 15-minute lock. Correct credentials during the lock are rejected with the same generic "Invalid username or password" as other credential failures. After lock expiry the correct password succeeds. The failed-attempt threshold and duration are unchanged.

**Actual:** Owner reports five-failure lockout, rejection during lock, expired-lock recovery/reset PASS; application policy is15minutes.

**Execution status:** OWNER PASS

**Tested commit:** 8322b4c20c067d512c4bb439fdedd19d4fa27223

**Execution date and environment:** Owner-reported focused execution on 5 November 2026: Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable loopback MySQL 8.0.46, synthetic fixtures; 47 PASS, zero failures/errors, 104.605 seconds. Published command and summary are retained; case-level raw JUnit is absent from issue38 directory.

**Evidence:** [evidence/issue38/README.md](evidence/issue38/README.md); [System_Validation_Report.md#hms-16-case-outcomes](System_Validation_Report.md#hms-16-case-outcomes)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`accounts.tests.AuthenticationTests.test_invalid_password_is_generic_and_locks_after_five_attempts`](../../accounts/tests.py#L133); [`accounts.test_security.SessionAndLockoutTests.test_django_admin_login_enforces_five_attempt_lockout`](../../accounts/test_security.py#L22); [`accounts.test_security.SessionAndLockoutTests.test_lockout_is_shared_between_application_and_admin_logins`](../../accounts/test_security.py#L55); [`accounts.test_security.SessionAndLockoutTests.test_success_resets_failed_attempts_and_expired_lock_starts_a_new_count`](../../accounts/test_security.py#L71)

**Current companion outcomes:** 4 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Recovery uses controlled stored expiry rather than retained actual15minute wait. Generic wording follows REQ2; original lockout-specific-message wording needs recorded disposition.

### TC-AUTH-04: Logout and session timeout

<a id="case-tc-auth-04"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; High (proposed). Risk: authentication, privacy or security failure can expose protected data or operations.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-3, NFR-9

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; protected URL known; browser cache/server session behavior observable. {"logout": "Logout then browserBack/protectedGET", "timeout": "separate login;15minutes with no requests;protected link"}

**Steps:**

1. Click Logout, then press browser Back.
2. Log in, stay idle for 15 minutes, then click any link.

**Expected:** After logout, protected pages redirect to login. After 15 idle minutes, session ends and login is required.

**Actual:** Owner reports logout and session-expiry PASS; tests invalidate stored sessions, redirect after expiry/logout and assert no-store cache control.

**Execution status:** OWNER PASS

**Tested commit:** 8322b4c20c067d512c4bb439fdedd19d4fa27223

**Execution date and environment:** Owner-reported focused execution on 5 November 2026: Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable loopback MySQL 8.0.46, synthetic fixtures; 47 PASS, zero failures/errors, 104.605 seconds. Published command and summary are retained; case-level raw JUnit is absent from issue38 directory.

**Evidence:** [evidence/issue38/README.md](evidence/issue38/README.md); [System_Validation_Report.md#hms-16-case-outcomes](System_Validation_Report.md#hms-16-case-outcomes)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`accounts.tests.AuthenticationTests.test_login_shows_role_dashboard_and_logout_clears_session`](../../accounts/tests.py#L28); [`accounts.tests.AuthenticationTests.test_expired_session_requires_login`](../../accounts/tests.py#L155); [`accounts.tests.AuthenticationTests.test_session_cookie_is_http_only_and_uses_fifteen_minute_rolling_expiry`](../../accounts/tests.py#L108); [`accounts.test_security.SessionAndLockoutTests.test_server_session_expiry_logout_and_cache_control`](../../accounts/test_security.py#L103)

**Current companion outcomes:** 4 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Server-client expiry simulation does not itself reproduce browser Back or an actual15minute idle browser interval.

### TC-USR-01: Admin manages user accounts

<a id="case-tc-usr-01"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; High (proposed). Risk: authentication, privacy or security failure can expose protected data or operations.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-4

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-admin authenticated; qa-warden-new does not exist. {"new_username": "qa-warden-new", "role": "Warden", "duplicate": "same username", "deactivate": "created user", "retry_login": "otherwise correct credentials"}

**Steps:**

1. Admin creates a Warden account.
2. Create another account with the same username.
3. Deactivate the Warden and try to log in.

**Expected:** Account created with role; duplicate username rejected; deactivated user cannot log in.

**Actual:** Owner reports Admin create/update/deactivate, duplicate rejection, non-admin denial and inactive-account authentication refusal PASS.

**Execution status:** OWNER PASS

**Tested commit:** 8322b4c20c067d512c4bb439fdedd19d4fa27223

**Execution date and environment:** Owner-reported focused execution on 5 November 2026: Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable loopback MySQL 8.0.46, synthetic fixtures; 47 PASS, zero failures/errors, 104.605 seconds. Published command and summary are retained; case-level raw JUnit is absent from issue38 directory.

**Evidence:** [evidence/issue38/README.md](evidence/issue38/README.md); [System_Validation_Report.md#hms-16-case-outcomes](System_Validation_Report.md#hms-16-case-outcomes)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`accounts.tests.AuthenticationTests.test_admin_can_create_and_deactivate_accounts`](../../accounts/tests.py#L165); [`accounts.tests.AuthenticationTests.test_duplicate_username_is_rejected`](../../accounts/tests.py#L225); [`accounts.tests.AuthenticationTests.test_admin_can_update_account`](../../accounts/tests.py#L241); [`accounts.tests.AuthenticationTests.test_non_admin_cannot_manage_accounts`](../../accounts/tests.py#L185); [`accounts.test_security.SessionAndLockoutTests.test_inactive_account_cannot_sign_in`](../../accounts/test_security.py#L91)

**Current companion outcomes:** 5 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Created/deactivated Warden and inactive-account login checks use separate fixtures rather than one retained browser sequence.

### TC-STU-01: Register student (valid data)

<a id="case-tc-stu-01"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-5

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; studentA ID absent; AddStudent available. {"registration": "Shared studentA with all mandatory AppendixB fields", "verify": "success message,list entry,saved database row"}

**Steps:**

1. Warden opens Add Student.
2. Fill all mandatory fields from Appendix B with valid data and submit.

**Expected:** Student saved; success message shown; student appears in student list.

**Actual:** Historical owner summary reports registration PASS. The new PR #66 screenshot shows the demo student in a Warden list/search result, but no registration submission or success message. Automated POST/redirect/persisted-row companions pass separately; the complete original manual sequence remains unverified.

**Execution status:** NOT RUN

**Tested commit:** c9f30a48c6dc54ccaec799156f3e52fe7bc8666a

**Execution date and environment:** Manual owner report on 7 November 2026: Windows, Firefox and Microsoft Edge (versions unrecorded), http://127.0.0.1:8022/, MySQL 8.0, synthetic demo data, Admin/Warden/Student accounts. The separate 5 November automated owner report names commit 8d60e83f1ce57ad99a2b2a22b3b5878f1390995b with git_dirty: true. Six claimed JUnit XML reports are absent from the published issue39 directory; 57/57 and the full 190-method (189 PASS, one SKIP, separate timing PASS) results remain published owner summaries.

**Evidence:** [Historical evidence index](evidence/issue39/README.md); [8 November follow-up review](evidence/issue39/followup-20261108.md); [student-list observation](../../Screenshot/TC-QUAL-01_Edge_Warden_Student_Registration.png).

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`students.tests.StudentManagementViewTests.test_admin_can_register_student`](../../students/tests.py#L132); [`students.tests.StudentManagementViewTests.test_warden_can_register_student`](../../students/tests.py#L177)

**Current companion outcomes:** 2 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Missing original manual sequence: Warden submits all mandatory Appendix B fields, record persists, success message shown and student appears in list. The added list image establishes only its visible result; its capture revision/date are not recorded. Retain NOT RUN until sufficiently scoped case evidence is supplied.

### TC-STU-02: Register student (invalid / duplicate)

<a id="case-tc-stu-02"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-5, REQ-6

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; studentA exists; count recorded. {"missing": "omit Name from otherwise valid studentC input", "duplicate": "complete valid record using PES1UG24CS101", "message": "Student ID already registered", "assertion": "neither invalid submission saves new row"}

**Steps:**

1. Submit with a mandatory field empty.
2. Submit with an existing Student ID.

**Expected:** Step 1: field-level error, nothing saved. Step 2: "Student ID already registered" shown, no second record.

**Actual:** Owner reports duplicate ID and missing mandatory fields rejected; both screenshots exist. Historical companions assert field errors and no extra record.

**Execution status:** OWNER PASS

**Tested commit:** c9f30a48c6dc54ccaec799156f3e52fe7bc8666a

**Execution date and environment:** Manual owner report on 7 November 2026: Windows, Firefox and Microsoft Edge (versions unrecorded), http://127.0.0.1:8022/, MySQL 8.0, synthetic demo data, Admin/Warden/Student accounts. The separate 5 November automated owner report names commit 8d60e83f1ce57ad99a2b2a22b3b5878f1390995b with git_dirty: true. Six claimed JUnit XML reports are absent from the published issue39 directory; 57/57 and the full 190-method (189 PASS, one SKIP, separate timing PASS) results remain published owner summaries.

**Evidence:** [evidence/issue39/README.md](evidence/issue39/README.md); [evidence/issue39/manual-execution-20261107.md](evidence/issue39/manual-execution-20261107.md); [../../Screenshot/TC-STU-02-duplicate-id-validation.png](../../Screenshot/TC-STU-02-duplicate-id-validation.png); [../../Screenshot/TC-STU-02-mandatory-field-validation.png](../../Screenshot/TC-STU-02-mandatory-field-validation.png); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`students.tests.StudentManagementViewTests.test_empty_student_submissions_show_required_errors_without_saving`](../../students/tests.py#L148); [`students.tests.StudentManagementViewTests.test_duplicate_registration_shows_required_message`](../../students/tests.py#L235)

**Current companion outcomes:** 2 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Screenshots show validation, not database non-persistence; that original condition uses separate historical companion evidence.

### TC-STU-03: Search students

<a id="case-tc-stu-03"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-7

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; A/B/C exist; A currently in QA Boys/101-A; B unallocated; C currently in QA Girls/201-A. {"queries": ["PES1UG24CS101", "Ar", "QA Boys hostel filter", "no-such-student"], "expected": "A forID;A/B forpartialAr;A forQA Boys;empty-result message for no match"}

**Steps:**

Search by (a) full Student ID, (b) partial name, (c) hostel.

**Expected:** Correct matching students are listed for each search; no match shows an empty-result message.

**Actual:** Owner reports/screenshots show correct full-ID, partial-name and hostel searches.

**Execution status:** OWNER PASS

**Tested commit:** c9f30a48c6dc54ccaec799156f3e52fe7bc8666a

**Execution date and environment:** Manual owner report on 7 November 2026: Windows, Firefox and Microsoft Edge (versions unrecorded), http://127.0.0.1:8022/, MySQL 8.0, synthetic demo data, Admin/Warden/Student accounts. The separate 5 November automated owner report names commit 8d60e83f1ce57ad99a2b2a22b3b5878f1390995b with git_dirty: true. Six claimed JUnit XML reports are absent from the published issue39 directory; 57/57 and the full 190-method (189 PASS, one SKIP, separate timing PASS) results remain published owner summaries.

**Evidence:** [evidence/issue39/README.md](evidence/issue39/README.md); [evidence/issue39/manual-execution-20261107.md](evidence/issue39/manual-execution-20261107.md); [../../Screenshot/TC-STU-03-search-by-full-student-ID.png](../../Screenshot/TC-STU-03-search-by-full-student-ID.png); [../../Screenshot/TC-STU-03-search-by-partial-name.png](../../Screenshot/TC-STU-03-search-by-partial-name.png); [../../Screenshot/TC-STU-03-search-by-hostel.png](../../Screenshot/TC-STU-03-search-by-hostel.png); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`students.tests.StudentManagementViewTests.test_search_matches_student_id_partial_name_and_hostel`](../../students/tests.py#L245)

**Current companion outcomes:** 1 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Original no-match empty-result message absent from listed screenshots and mapped search companion; case-review/retest needed.

### TC-STU-04: Update student details

<a id="case-tc-stu-04"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-8

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; studentA exists; ID recorded. {"student": "PES1UG24CS101", "new_mobile": "9000000191", "attempted_ID": "PES1UG24CS199", "supplemental_changes": {"course": "B.Tech IT", "year": 3}, "assertion": "mobile persists,originalID retained"}

**Steps:**

1. Edit mobile number and save.
2. Try to edit Student ID.

**Expected:** Mobile number updated; Student ID field is read-only / change rejected.

**Actual:** Owner reports saved contact update with screenshot; historical companion asserts updated contact/course/year and unchanged StudentID after forged edit.

**Execution status:** OWNER PASS

**Tested commit:** c9f30a48c6dc54ccaec799156f3e52fe7bc8666a

**Execution date and environment:** Manual owner report on 7 November 2026: Windows, Firefox and Microsoft Edge (versions unrecorded), http://127.0.0.1:8022/, MySQL 8.0, synthetic demo data, Admin/Warden/Student accounts. The separate 5 November automated owner report names commit 8d60e83f1ce57ad99a2b2a22b3b5878f1390995b with git_dirty: true. Six claimed JUnit XML reports are absent from the published issue39 directory; 57/57 and the full 190-method (189 PASS, one SKIP, separate timing PASS) results remain published owner summaries.

**Evidence:** [evidence/issue39/README.md](evidence/issue39/README.md); [evidence/issue39/manual-execution-20261107.md](evidence/issue39/manual-execution-20261107.md); [../../Screenshot/TC-STU-04-update-student-details.png](../../Screenshot/TC-STU-04-update-student-details.png); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`students.tests.StudentManagementViewTests.test_admin_can_update_contact_course_and_year_but_not_student_id`](../../students/tests.py#L209)

**Current companion outcomes:** 1 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Screenshot alone does not establish StudentID immutability; original edit-ID step has separate historical automated companion.

### TC-STU-05: Deactivate student

<a id="case-tc-stu-05"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-9, NFR-5

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; A has active101-A allocation; B has no active allocation; rowIDs/counts recorded. {"blocked_student": "PES1UG24CS101", "allowed_student": "PES1UG24CS102", "verify": "A refusal shows bed;B Inactive;database row retained"}

**Steps:**

1. Deactivate a student with an active allocation.
2. Deactivate a student with no allocation.

**Expected:** Step 1 refused and allocated bed shown. Step 2 marks student Inactive; record still exists in the database.

**Actual:** Owner reports blocked deactivation during active allocation and success after allocation completed; both screenshots exist. Historical companions assert bed message, inactive status and record retention.

**Execution status:** OWNER PASS

**Tested commit:** c9f30a48c6dc54ccaec799156f3e52fe7bc8666a

**Execution date and environment:** Manual owner report on 7 November 2026: Windows, Firefox and Microsoft Edge (versions unrecorded), http://127.0.0.1:8022/, MySQL 8.0, synthetic demo data, Admin/Warden/Student accounts. The separate 5 November automated owner report names commit 8d60e83f1ce57ad99a2b2a22b3b5878f1390995b with git_dirty: true. Six claimed JUnit XML reports are absent from the published issue39 directory; 57/57 and the full 190-method (189 PASS, one SKIP, separate timing PASS) results remain published owner summaries.

**Evidence:** [evidence/issue39/README.md](evidence/issue39/README.md); [evidence/issue39/manual-execution-20261107.md](evidence/issue39/manual-execution-20261107.md); [../../Screenshot/TC-STU-05_deactivation_blocked_active_allocation.png](../../Screenshot/TC-STU-05_deactivation_blocked_active_allocation.png); [../../Screenshot/TC-STU-05_student_deactivation_success.png](../../Screenshot/TC-STU-05_student_deactivation_success.png); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`students.tests.StudentManagementViewTests.test_student_with_active_allocation_cannot_be_deactivated`](../../students/tests.py#L317); [`students.tests.StudentManagementViewTests.test_unallocated_student_can_be_deactivated`](../../students/tests.py#L291); [`students.tests.StudentModelTests.test_student_can_be_deactivated_without_deleting_record`](../../students/tests.py#L58)

**Current companion outcomes:** 3 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Precise database retention/invariants use historical companions rather than screenshot-only proof.

### TC-HST-01: Add hostel and room

<a id="case-tc-hst-01"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-10, REQ-11

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-admin authenticated; QA Boys/101 absent for isolated case. {"hostel": {"name": "QA Boys", "type": "Boys"}, "room": {"number": "101", "floor": 1, "room_type": "Triple", "capacity": 3, "fee_inr": "10000.00"}, "invalid": ["same room101/same hostel", "capacity5"], "capacity_range": "1..4"}

**Steps:**

1. Admin adds a Boys hostel.
2. Add room 101 (capacity 3).
3. Add room 101 again in the same hostel.
4. Add room with capacity 5.

**Expected:** Hostel and room saved; duplicate room number rejected; capacity 5 rejected (allowed range 1 to 4).

**Actual:** Owner reports hostel/room creation, duplicate-room and invalid-capacity rejection plus auto-bed generation; no named HST01 screenshot. Historical model/view companions passed.

**Execution status:** OWNER PASS

**Tested commit:** c9f30a48c6dc54ccaec799156f3e52fe7bc8666a

**Execution date and environment:** Manual owner report on 7 November 2026: Windows, Firefox and Microsoft Edge (versions unrecorded), http://127.0.0.1:8022/, MySQL 8.0, synthetic demo data, Admin/Warden/Student accounts. The separate 5 November automated owner report names commit 8d60e83f1ce57ad99a2b2a22b3b5878f1390995b with git_dirty: true. Six claimed JUnit XML reports are absent from the published issue39 directory; 57/57 and the full 190-method (189 PASS, one SKIP, separate timing PASS) results remain published owner summaries.

**Evidence:** [evidence/issue39/README.md](evidence/issue39/README.md); [evidence/issue39/manual-execution-20261107.md](evidence/issue39/manual-execution-20261107.md); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`hostels.tests.HostelManagementViewTests.test_admin_can_create_hostel_and_room`](../../hostels/tests.py#L47); [`hostels.tests.HostelModelBehaviorTests.test_room_creation_automatically_creates_beds`](../../hostels/tests.py#L208); [`hostels.tests.HostelModelBehaviorTests.test_room_numbers_must_be_unique_within_hostel`](../../hostels/tests.py#L239); [`hostels.tests.HostelModelBehaviorTests.test_room_capacity_cannot_exceed_four`](../../hostels/tests.py#L227)

**Current companion outcomes:** 4 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** OWNER PASS(reported):original Admin/Boys-hostel/room101-capacity3/duplicate101/capacity5 sequence has no named retained manual screenshot. Historical companions use their own fixtures.

### TC-HST-02: Bed creation and availability list

<a id="case-tc-hst-02"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-12, REQ-13

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** HST01-equivalent setup;101-A/B/C Available; second hostel/floor/type; separately identified Maintenance bed. {"filters": ["QA Boys", "floor1", "Triple"], "initial": ["101-A", "101-B", "101-C"], "allocate": "A to101-A then refresh", "exclude": "occupied101-A andMaintenance bed"}

**Steps:**

1. After TC-HST-01, open Available Beds.
2. Filter by hostel, floor, room type.
3. Allocate one bed and refresh.

**Expected:** Beds 101-A, 101-B, 101-C exist as Available; filters work; allocated bed disappears from the list.

**Requirement-derived additions:** SRS REQ-13 also excludes Maintenance beds from Available results.

**Actual:** Owner reports available-bed and hostel/floor/type/status filters; three screenshots exist. Historical companions establish auto labels and occupied/maintenance exclusion.

**Execution status:** OWNER PASS

**Tested commit:** c9f30a48c6dc54ccaec799156f3e52fe7bc8666a

**Execution date and environment:** Manual owner report on 7 November 2026: Windows, Firefox and Microsoft Edge (versions unrecorded), http://127.0.0.1:8022/, MySQL 8.0, synthetic demo data, Admin/Warden/Student accounts. The separate 5 November automated owner report names commit 8d60e83f1ce57ad99a2b2a22b3b5878f1390995b with git_dirty: true. Six claimed JUnit XML reports are absent from the published issue39 directory; 57/57 and the full 190-method (189 PASS, one SKIP, separate timing PASS) results remain published owner summaries.

**Evidence:** [evidence/issue39/README.md](evidence/issue39/README.md); [evidence/issue39/manual-execution-20261107.md](evidence/issue39/manual-execution-20261107.md); [../../Screenshot/TC-HST-02_available-beds-default.png](../../Screenshot/TC-HST-02_available-beds-default.png); [../../Screenshot/TC-HST-02-hostel-floor-filter.png](../../Screenshot/TC-HST-02-hostel-floor-filter.png); [../../Screenshot/TC-HST-02_bed_filters.png](../../Screenshot/TC-HST-02_bed_filters.png); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`hostels.tests.HostelModelBehaviorTests.test_room_creation_automatically_creates_beds`](../../hostels/tests.py#L208); [`hostels.tests.BedFilteringViewTests.test_available_filter_excludes_occupied_and_maintenance_beds`](../../hostels/tests.py#L447); [`hostels.tests.BedFilteringViewTests.test_combined_filters_return_only_matching_available_beds`](../../hostels/tests.py#L489)

**Current companion outcomes:** 3 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Manual evidence does not document entire original room101-A/B/C then allocate-one-and-refresh sequence. Occupied exclusion has separate historical companion.

### TC-ALC-01: Allocate available bed

<a id="case-tc-alc-01"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #40 technical review 8 November). Risk: allocation inconsistency or unrecoverable data can corrupt live hostel records.

**Priority review:** High accepted for #40's [8 November AI technical review](evidence/issue40-final/qa-review-20261108.md); original priorities were unspecified. Whole-team exit approval is separate.

**Requirements:** REQ-14

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; A active,male,unallocated;101-A Available in QA Boys. {"student": "PES1UG24CS101", "bed": "101-A", "date": "2026-11-01", "verify": ["savedDate", "Occupied", "confirmation"]}

**Steps:**

Select an active male student and an available bed in the Boys hostel; confirm.

**Expected:** Allocation saved with date; bed status becomes Occupied; confirmation shown.

**Actual:** Browser form saved allocation/date and displayed confirmation; a separate bed-list page showed Occupied after commit.

**Execution status:** OWNER PASS

**Tested commit:** 0e358b4ce1fd02366184c7cb9c312b47dd093214

**Execution date and environment:** 5 November 2026, clean source and tree c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0; Windows 11, Python 3.14.7, Django 5.2.18, disposable MySQL 8.4.9; Edge 156.0.4314.58 with Playwright 1.64.1; JMeter 5.6.3 and Java 17; synthetic isolated recovery source.

**Evidence:** [evidence/issue40-final/owner-cases.md#tc-alc-01--allocate-available-bed](evidence/issue40-final/owner-cases.md#tc-alc-01--allocate-available-bed); [evidence/issue40-final/browser-results.json](evidence/issue40-final/browser-results.json); [evidence/issue40-final/focused-methods.json](evidence/issue40-final/focused-methods.json); [evidence/issue40-final/summary.json](evidence/issue40-final/summary.json)

**Defects and retests:** RV01/RV02 safety corrections and #45-#48 provenance retained in owner appendix/evidence/owned-defects/retest.json. PR44/49/50 merges establish integration, not formal APPROVED reviews or QA/PO signoff.

**QA disposition:** Accepted for scoped #40 technical closure by the [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), including explicit late-entry/tool/environment limits. No retrospective entry or human final approval is claimed.

**Automation:** [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../scripts/part3/test_issue40_browser.py#L45); [`allocations.tests.AllocationViewTests.test_admin_can_create_allocation`](../../allocations/tests.py#L146); [`allocations.tests.AllocationModelTests.test_active_allocation_occupies_bed`](../../allocations/tests.py#L21); [`allocations.tests.AllocationViewTests.test_allocation_creation_rolls_back_if_audit_event_fails`](../../allocations/tests.py#L176)

**Current companion outcomes:** 3 PASS and 0 expected timing SKIP in each current CI bundle; outside this CI selection: scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The 8 November independent AI review accepts this original case, scoped priority and bounded environment/tool evidence for #40. Historical approved-SRS/pre-execution case review is not established; actual whole-team acceptance remains pending. Original plan provides no per-case priority. Edge/Playwright for Selenium, MySQL8.4.9 for8.0, and loopbackHTTP/test-only disabled secure redirect/cookie flags are declared deviations. Historical observations are not new current-tree measurements.

### TC-ALC-02: Block allocation of occupied bed

<a id="case-tc-alc-02"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #40 technical review 8 November). Risk: allocation inconsistency or unrecoverable data can corrupt live hostel records.

**Priority review:** High accepted for #40's [8 November AI technical review](evidence/issue40-final/qa-review-20261108.md); original priorities were unspecified. Whole-team exit approval is separate.

**Requirements:** REQ-15

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; A occupies101-A; B active/unallocated; stale form/API can attempt occupied target. {"attempt_student": "PES1UG24CS102", "bed": "101-A", "baseline": "original activeID/count", "verify": "reason,no second active row"}

**Steps:**

Try to allocate an already occupied bed to another student.

**Expected:** Request rejected with reason; no second active allocation exists for the bed.

**Actual:** A different student using a stale form was rejected with the occupied-bed reason; no duplicate allocation.

**Execution status:** OWNER PASS

**Tested commit:** 0e358b4ce1fd02366184c7cb9c312b47dd093214

**Execution date and environment:** 5 November 2026, clean source and tree c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0; Windows 11, Python 3.14.7, Django 5.2.18, disposable MySQL 8.4.9; Edge 156.0.4314.58 with Playwright 1.64.1; JMeter 5.6.3 and Java 17; synthetic isolated recovery source.

**Evidence:** [evidence/issue40-final/owner-cases.md#tc-alc-02--block-allocation-of-occupied-bed](evidence/issue40-final/owner-cases.md#tc-alc-02--block-allocation-of-occupied-bed); [evidence/issue40-final/browser-results.json](evidence/issue40-final/browser-results.json); [evidence/issue40-final/focused-methods.json](evidence/issue40-final/focused-methods.json); [evidence/issue40-final/summary.json](evidence/issue40-final/summary.json)

**Defects and retests:** RV01/RV02 safety corrections and #45-#48 provenance retained in owner appendix/evidence/owned-defects/retest.json. PR44/49/50 merges establish integration, not formal APPROVED reviews or QA/PO signoff.

**QA disposition:** Accepted for scoped #40 technical closure by the [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), including explicit late-entry/tool/environment limits. No retrospective entry or human final approval is claimed.

**Automation:** [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../scripts/part3/test_issue40_browser.py#L45); [`allocations.test_workflows.AllocationWorkflowTests.test_json_workflow_conflicts_validation_and_permissions`](../../allocations/test_workflows.py#L415); [`allocations.tests.AllocationModelTests.test_bed_cannot_have_two_active_allocations`](../../allocations/tests.py#L48)

**Current companion outcomes:** 2 PASS and 0 expected timing SKIP in each current CI bundle; outside this CI selection: scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The 8 November independent AI review accepts this original case, scoped priority and bounded environment/tool evidence for #40. Historical approved-SRS/pre-execution case review is not established; actual whole-team acceptance remains pending. Original plan provides no per-case priority. Edge/Playwright for Selenium, MySQL8.4.9 for8.0, and loopbackHTTP/test-only disabled secure redirect/cookie flags are declared deviations. Historical observations are not new current-tree measurements.

### TC-ALC-03: Block second allocation for a student

<a id="case-tc-alc-03"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #40 technical review 8 November). Risk: allocation inconsistency or unrecoverable data can corrupt live hostel records.

**Priority review:** High accepted for #40's [8 November AI technical review](evidence/issue40-final/qa-review-20261108.md); original priorities were unspecified. Whole-team exit approval is separate.

**Requirements:** REQ-15

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; A occupies101-A;102-A Available. {"student": "PES1UG24CS101", "target": "102-A", "baseline": "original allocationID/bed", "verify": "reason,original unchanged"}

**Steps:**

Try to allocate a second bed to a student who already has an active allocation.

**Expected:** Request rejected with reason; original allocation unchanged.

**Actual:** Second allocation for the same student was rejected; original ID and bed unchanged.

**Execution status:** OWNER PASS

**Tested commit:** 0e358b4ce1fd02366184c7cb9c312b47dd093214

**Execution date and environment:** 5 November 2026, clean source and tree c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0; Windows 11, Python 3.14.7, Django 5.2.18, disposable MySQL 8.4.9; Edge 156.0.4314.58 with Playwright 1.64.1; JMeter 5.6.3 and Java 17; synthetic isolated recovery source.

**Evidence:** [evidence/issue40-final/owner-cases.md#tc-alc-03--block-second-allocation-for-a-student](evidence/issue40-final/owner-cases.md#tc-alc-03--block-second-allocation-for-a-student); [evidence/issue40-final/browser-results.json](evidence/issue40-final/browser-results.json); [evidence/issue40-final/focused-methods.json](evidence/issue40-final/focused-methods.json); [evidence/issue40-final/summary.json](evidence/issue40-final/summary.json)

**Defects and retests:** RV01/RV02 safety corrections and #45-#48 provenance retained in owner appendix/evidence/owned-defects/retest.json. PR44/49/50 merges establish integration, not formal APPROVED reviews or QA/PO signoff.

**QA disposition:** Accepted for scoped #40 technical closure by the [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), including explicit late-entry/tool/environment limits. No retrospective entry or human final approval is claimed.

**Automation:** [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../scripts/part3/test_issue40_browser.py#L45); [`allocations.test_workflows.AllocationWorkflowTests.test_json_workflow_conflicts_validation_and_permissions`](../../allocations/test_workflows.py#L415); [`allocations.tests.AllocationModelTests.test_student_cannot_have_two_active_allocations`](../../allocations/tests.py#L36)

**Current companion outcomes:** 2 PASS and 0 expected timing SKIP in each current CI bundle; outside this CI selection: scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The 8 November independent AI review accepts this original case, scoped priority and bounded environment/tool evidence for #40. Historical approved-SRS/pre-execution case review is not established; actual whole-team acceptance remains pending. Original plan provides no per-case priority. Edge/Playwright for Selenium, MySQL8.4.9 for8.0, and loopbackHTTP/test-only disabled secure redirect/cookie flags are declared deviations. Historical observations are not new current-tree measurements.

### TC-ALC-04: Gender and hostel type mismatch

<a id="case-tc-alc-04"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #40 technical review 8 November). Risk: allocation inconsistency or unrecoverable data can corrupt live hostel records.

**Priority review:** High accepted for #40's [8 November AI technical review](evidence/issue40-final/qa-review-20261108.md); original priorities were unspecified. Whole-team exit approval is separate.

**Requirements:** REQ-16

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; C active,female,unallocated;102-A Available in QA Boys. {"student": "PES1UG24CS103", "target": "QA Boys/102-A", "verify": "gender mismatch reason,no write"}

**Steps:**

Try to allocate a female student to a bed in a Boys hostel.

**Expected:** Allocation rejected with a gender mismatch message.

**Actual:** Browser rejected female student / Boys hostel with a gender mismatch reason; MySQL verifies no write.

**Execution status:** OWNER PASS

**Tested commit:** 0e358b4ce1fd02366184c7cb9c312b47dd093214

**Execution date and environment:** 5 November 2026, clean source and tree c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0; Windows 11, Python 3.14.7, Django 5.2.18, disposable MySQL 8.4.9; Edge 156.0.4314.58 with Playwright 1.64.1; JMeter 5.6.3 and Java 17; synthetic isolated recovery source.

**Evidence:** [evidence/issue40-final/owner-cases.md#tc-alc-04--gender-and-hostel-type-mismatch](evidence/issue40-final/owner-cases.md#tc-alc-04--gender-and-hostel-type-mismatch); [evidence/issue40-final/browser-results.json](evidence/issue40-final/browser-results.json); [evidence/issue40-final/focused-methods.json](evidence/issue40-final/focused-methods.json); [evidence/issue40-final/summary.json](evidence/issue40-final/summary.json)

**Defects and retests:** RV01/RV02 safety corrections and #45-#48 provenance retained in owner appendix/evidence/owned-defects/retest.json. PR44/49/50 merges establish integration, not formal APPROVED reviews or QA/PO signoff.

**QA disposition:** Accepted for scoped #40 technical closure by the [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), including explicit late-entry/tool/environment limits. No retrospective entry or human final approval is claimed.

**Automation:** [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../scripts/part3/test_issue40_browser.py#L45); [`allocations.test_workflows.AllocationWorkflowTests.test_invalid_eligibility_gender_status_and_dates_are_rejected`](../../allocations/test_workflows.py#L174)

**Current companion outcomes:** 1 PASS and 0 expected timing SKIP in each current CI bundle; outside this CI selection: scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The 8 November independent AI review accepts this original case, scoped priority and bounded environment/tool evidence for #40. Historical approved-SRS/pre-execution case review is not established; actual whole-team acceptance remains pending. Original plan provides no per-case priority. Edge/Playwright for Selenium, MySQL8.4.9 for8.0, and loopbackHTTP/test-only disabled secure redirect/cookie flags are declared deviations. Historical observations are not new current-tree measurements.

### TC-ALC-05: Transfer student

<a id="case-tc-alc-05"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #40 technical review 8 November). Risk: allocation inconsistency or unrecoverable data can corrupt live hostel records.

**Priority review:** High accepted for #40's [8 November AI technical review](evidence/issue40-final/qa-review-20261108.md); original priorities were unspecified. Whole-team exit approval is separate.

**Requirements:** REQ-17

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; A active101-A;102-A Available; both beds/history/audit baseline recorded; disposable companion supports fault injection. {"date": "2026-11-02", "old": "101-A", "target": "102-A", "fault": "inject target-bed save failure then remove fault and retry same transfer", "verify": ["success oldAvailable/newOccupied", "failure originalActive/bothBeds/history rollback"]}

**Steps:**

1. Transfer an allocated student to another available bed.
2. Force a failure while saving the new bed (for example, DB error in test) and retry.

**Expected:** Step 1: old bed Available, new bed Occupied. Step 2: transaction rolled back, old allocation still active (atomic).

**Actual:** Transfer confirmation was cancelled with zero POSTs and unchanged allocation/bed states, then accepted once to preserve original and create successor; storage-failure rollback requires the companion regression. The fresh focused method `test_transfer_failure_rolls_back_both_beds_and_history` passed: it injects a target-bed save failure, checks original active allocation/both beds/history and unchanged audit count, removes the fault, retries the same transfer, and verifies the successor, both bed states, preserved history and exactly one attributed transfer audit. Browser-only status remains PARTIAL.

**Execution status:** OWNER PASS

**Tested commit:** 0e358b4ce1fd02366184c7cb9c312b47dd093214

**Execution date and environment:** 5 November 2026, clean source and tree c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0; Windows 11, Python 3.14.7, Django 5.2.18, disposable MySQL 8.4.9; Edge 156.0.4314.58 with Playwright 1.64.1; JMeter 5.6.3 and Java 17; synthetic isolated recovery source.

**Evidence:** [evidence/issue40-final/owner-cases.md#tc-alc-05--transfer-student](evidence/issue40-final/owner-cases.md#tc-alc-05--transfer-student); [evidence/issue40-final/browser-results.json](evidence/issue40-final/browser-results.json); [evidence/issue40-final/focused-methods.json](evidence/issue40-final/focused-methods.json); [evidence/issue40-final/summary.json](evidence/issue40-final/summary.json)

**Defects and retests:** RV01/RV02 safety corrections and #45-#48 provenance retained in owner appendix/evidence/owned-defects/retest.json. PR44/49/50 merges establish integration, not formal APPROVED reviews or QA/PO signoff. RV03 earlier fault proof omitted retry; corrected focused companion checks rollback, retry, both beds/history and exactly one attributed audit.

**QA disposition:** Accepted for scoped #40 technical closure by the [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), including explicit late-entry/tool/environment limits. No retrospective entry or human final approval is claimed.

**Automation:** [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../scripts/part3/test_issue40_browser.py#L45); [`allocations.test_workflows.AllocationWorkflowTests.test_transfer_and_release_preserve_history_and_emit_actor_audit`](../../allocations/test_workflows.py#L142); [`allocations.test_workflows.AllocationWorkflowTests.test_transfer_failure_rolls_back_both_beds_and_history`](../../allocations/test_workflows.py#L234); [`allocations.test_workflows.AllocationWorkflowTests.test_only_transfer_and_release_forms_require_submit_confirmation`](../../allocations/test_workflows.py#L39)

**Current companion outcomes:** 3 PASS and 0 expected timing SKIP in each current CI bundle; outside this CI selection: scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The 8 November independent AI review accepts this original case, scoped priority and bounded environment/tool evidence for #40. Historical approved-SRS/pre-execution case review is not established; actual whole-team acceptance remains pending. Original plan provides no per-case priority. Edge/Playwright for Selenium, MySQL8.4.9 for8.0, and loopbackHTTP/test-only disabled secure redirect/cookie flags are declared deviations. Historical observations are not new current-tree measurements. Raw browser status remains PARTIAL for fault injection; combined OWNER PASS uses passing same-transfer failure/rollback/retry companion; do not relabel raw artifact.

### TC-ALC-06: Release allocation and history

<a id="case-tc-alc-06"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #40 technical review 8 November). Risk: allocation inconsistency or unrecoverable data can corrupt live hostel records.

**Priority review:** High accepted for #40's [8 November AI technical review](evidence/issue40-final/qa-review-20261108.md); original priorities were unspecified. Whole-team exit approval is separate.

**Requirements:** REQ-18, REQ-19, NFR-5 (NFR-5 is supplemental; original REQ-18/REQ-19 mapping retained).

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; A active allocation plus at least three historical entries with distinct dates opposing insertion order. {"vacate": "2026-11-03", "verify": ["Available bed", "stored vacateDate", "all past/current history by allocation date"]}

**Steps:**

1. Release an allocation with a vacate date.
2. Open the student's allocation history.

**Expected:** Bed becomes Available; vacate date stored; history lists all past and current allocations in date order.

**Actual:** Release confirmation was cancelled with zero POSTs and unchanged allocation/bed states, then accepted once; list/history show DD-MM-YYYY while JSON retains ISO dates. Fresh `test_history_orders_backdated_records_by_allocation_date_in_json_and_html` passed for distinct counterordered dates, supplying date-order proof beyond the browser's same-day records.

**Execution status:** OWNER PASS

**Tested commit:** 0e358b4ce1fd02366184c7cb9c312b47dd093214

**Execution date and environment:** 5 November 2026, clean source and tree c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0; Windows 11, Python 3.14.7, Django 5.2.18, disposable MySQL 8.4.9; Edge 156.0.4314.58 with Playwright 1.64.1; JMeter 5.6.3 and Java 17; synthetic isolated recovery source.

**Evidence:** [evidence/issue40-final/owner-cases.md#tc-alc-06--release-allocation-and-history](evidence/issue40-final/owner-cases.md#tc-alc-06--release-allocation-and-history); [evidence/issue40-final/browser-results.json](evidence/issue40-final/browser-results.json); [evidence/issue40-final/focused-methods.json](evidence/issue40-final/focused-methods.json); [evidence/issue40-final/summary.json](evidence/issue40-final/summary.json)

**Defects and retests:** RV01/RV02 safety corrections and #45-#48 provenance retained in owner appendix/evidence/owned-defects/retest.json. PR44/49/50 merges establish integration, not formal APPROVED reviews or QA/PO signoff. RV04 counterordered-date JSON/HTML method replaces incomplete same-day order inference; #46 confirmation/#47date-format fixes retested.

**QA disposition:** Accepted for scoped #40 technical closure by the [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), including explicit late-entry/tool/environment limits. No retrospective entry or human final approval is claimed.

**Automation:** [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../scripts/part3/test_issue40_browser.py#L45); [`allocations.test_workflows.AllocationWorkflowTests.test_transfer_and_release_preserve_history_and_emit_actor_audit`](../../allocations/test_workflows.py#L142); [`allocations.test_workflows.AllocationWorkflowTests.test_history_orders_backdated_records_by_allocation_date_in_json_and_html`](../../allocations/test_workflows.py#L304)

**Current companion outcomes:** 2 PASS and 0 expected timing SKIP in each current CI bundle; outside this CI selection: scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The 8 November independent AI review accepts this original case, scoped priority and bounded environment/tool evidence for #40. Historical approved-SRS/pre-execution case review is not established; actual whole-team acceptance remains pending. Original plan provides no per-case priority. Edge/Playwright for Selenium, MySQL8.4.9 for8.0, and loopbackHTTP/test-only disabled secure redirect/cookie flags are declared deviations. Historical observations are not new current-tree measurements.

### TC-PAY-01: Record payment and receipt

<a id="case-tc-pay-01"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #40 technical review 8 November). Risk: incorrect money or receipt history can corrupt the financial record.

**Priority review:** High accepted for #40's [8 November AI technical review](evidence/issue40-final/qa-review-20261108.md); original priorities were unspecified. Whole-team exit approval is separate.

**Requirements:** REQ-20, REQ-21

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; A with RoomFee10000; receipt counter/rows recorded. {"valid": {"student": "PES1UG24CS101", "amount": "5000.00", "mode": "UPI", "date": "2026-11-02", "reference": "QAUPI0001"}, "invalid_amounts": ["0", "-1"], "receipt": "actualPDF with correct number/student/amount/date/mode/reference", "verify": "unique sequential receipt;invalid attempts save nothing"}

**Steps:**

1. Record payment (amount 5000, UPI, date, reference).
2. Record a payment with amount 0 and one with negative amount.
3. Download the receipt.

**Expected:** Step 1 saved with a unique sequential receipt number. Step 2 rejected. Step 3 gives a PDF receipt with correct details.

**Actual:** Browser recorded INR 5000 UPI payment and downloaded PDF; zero/negative submissions displayed server-side form-validation errors (HTTP 200), without additional receipts.

**Execution status:** OWNER PASS

**Tested commit:** 0e358b4ce1fd02366184c7cb9c312b47dd093214

**Execution date and environment:** 5 November 2026, clean source and tree c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0; Windows 11, Python 3.14.7, Django 5.2.18, disposable MySQL 8.4.9; Edge 156.0.4314.58 with Playwright 1.64.1; JMeter 5.6.3 and Java 17; synthetic isolated recovery source.

**Evidence:** [evidence/issue40-final/owner-cases.md#tc-pay-01--record-payment-and-receipt](evidence/issue40-final/owner-cases.md#tc-pay-01--record-payment-and-receipt); [evidence/issue40-final/browser-results.json](evidence/issue40-final/browser-results.json); [evidence/issue40-final/focused-methods.json](evidence/issue40-final/focused-methods.json); [evidence/issue40-final/summary.json](evidence/issue40-final/summary.json)

**Defects and retests:** RV01/RV02 safety corrections and #45-#48 provenance retained in owner appendix/evidence/owned-defects/retest.json. PR44/49/50 merges establish integration, not formal APPROVED reviews or QA/PO signoff.

**QA disposition:** Accepted for scoped #40 technical closure by the [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), including explicit late-entry/tool/environment limits. No retrospective entry or human final approval is claimed.

**Automation:** [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../scripts/part3/test_issue40_browser.py#L45); [`payments.test_workflows.PaymentWorkflowTests.test_invalid_amounts_modes_dates_and_references_do_not_consume_numbers`](../../payments/test_workflows.py#L91); [`payments.test_workflows.PaymentWorkflowTests.test_json_workflow_receipts_adjustments_and_real_pdf_contents`](../../payments/test_workflows.py#L311); [`payments.test_workflows.PaymentConcurrencyTests.test_simultaneous_payments_receive_unique_sequential_numbers`](../../payments/test_workflows.py#L549)

**Current companion outcomes:** 3 PASS and 0 expected timing SKIP in each current CI bundle; outside this CI selection: scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The 8 November independent AI review accepts this original case, scoped priority and bounded environment/tool evidence for #40. Historical approved-SRS/pre-execution case review is not established; actual whole-team acceptance remains pending. Original plan provides no per-case priority. Edge/Playwright for Selenium, MySQL8.4.9 for8.0, and loopbackHTTP/test-only disabled secure redirect/cookie flags are declared deviations. Historical observations are not new current-tree measurements.

### TC-PAY-02: Payment status

<a id="case-tc-pay-02"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #40 technical review 8 November). Risk: incorrect money or receipt history can corrupt the financial record.

**Priority review:** High accepted for #40's [8 November AI technical review](evidence/issue40-final/qa-review-20261108.md); original priorities were unspecified. Whole-team exit approval is separate.

**Requirements:** REQ-22

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; A allocated RoomFee10000; initially zero effective payments. {"sequence": [{"paid": "0.00", "status": "Pending"}, {"paid": "5000.00", "status": "Partial"}, {"paid": "10000.00", "status": "Paid"}]}

**Steps:**

Record no payment, then partial payment, then full payment for a student.

**Expected:** Status shows Pending, then Partial, then Paid.

**Actual:** Browser payment statuses: Pending -&gt; Partial -&gt; Paid; final paid INR 10000, due INR 0 checked in MySQL.

**Execution status:** OWNER PASS

**Tested commit:** 0e358b4ce1fd02366184c7cb9c312b47dd093214

**Execution date and environment:** 5 November 2026, clean source and tree c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0; Windows 11, Python 3.14.7, Django 5.2.18, disposable MySQL 8.4.9; Edge 156.0.4314.58 with Playwright 1.64.1; JMeter 5.6.3 and Java 17; synthetic isolated recovery source.

**Evidence:** [evidence/issue40-final/owner-cases.md#tc-pay-02--payment-status](evidence/issue40-final/owner-cases.md#tc-pay-02--payment-status); [evidence/issue40-final/browser-results.json](evidence/issue40-final/browser-results.json); [evidence/issue40-final/focused-methods.json](evidence/issue40-final/focused-methods.json); [evidence/issue40-final/summary.json](evidence/issue40-final/summary.json)

**Defects and retests:** RV01/RV02 safety corrections and #45-#48 provenance retained in owner appendix/evidence/owned-defects/retest.json. PR44/49/50 merges establish integration, not formal APPROVED reviews or QA/PO signoff.

**QA disposition:** Accepted for scoped #40 technical closure by the [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), including explicit late-entry/tool/environment limits. No retrospective entry or human final approval is claimed.

**Automation:** [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../scripts/part3/test_issue40_browser.py#L45); [`payments.test_workflows.PaymentWorkflowTests.test_status_tracks_pending_partial_paid_and_adjustments_without_join_multiplication`](../../payments/test_workflows.py#L218); [`payments.test_workflows.PaymentWorkflowTests.test_no_allocation_or_unconfigured_fee_remains_pending_with_advance_payment`](../../payments/test_workflows.py#L253)

**Current companion outcomes:** 2 PASS and 0 expected timing SKIP in each current CI bundle; outside this CI selection: scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The 8 November independent AI review accepts this original case, scoped priority and bounded environment/tool evidence for #40. Historical approved-SRS/pre-execution case review is not established; actual whole-team acceptance remains pending. Original plan provides no per-case priority. Edge/Playwright for Selenium, MySQL8.4.9 for8.0, and loopbackHTTP/test-only disabled secure redirect/cookie flags are declared deviations. Historical observations are not new current-tree measurements.

### TC-RPT-01: Occupancy report

<a id="case-tc-rpt-01"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Devansh

**Priority:** Unspecified in original plan; Medium (proposed 7 November; adopted for scoped #40 technical review 8 November). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Medium accepted for #40's [8 November AI technical review](evidence/issue40-final/qa-review-20261108.md); original priorities were unspecified. Whole-team exit approval is separate.

**Requirements:** REQ-23

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** qa-warden authenticated; known QA Boys/Girls counts;Available/Occupied/Maintenance beds;assigned/unassigned students;Pending/Partial/Paid examples;database oracle captured. {"outputs": ["occupancyHTML/JSON/CSV", "payment-statusHTML/JSON/CSV"], "filters": ["eachhostel", "allwhereaccepted"], "occupancy_fields": ["Hostel Name", "Total Beds", "Occupied Beds", "Available Beds", "Beds Under Maintenance", "Occupancy %", "Generated On"], "payment_fields": ["Student ID", "Student Name", "Hostel / Room / Bed", "Fee Amount", "Amount Paid", "Payment Status", "Generated On"], "verify": "database counts and consistent values acrossformats,includingBed"}

**Steps:**

Open the occupancy report and the payment status report for a hostel with known counts; export CSV for both.

**Expected:** Total, occupied, available beds and occupancy % match database counts; CSV downloads with same values.

**Requirement-derived additions:** SRS Appendix B additionally requires maintenance counts and payment Student ID/Name, Hostel/Room/Bed, Fee Amount, Amount Paid and Payment Status, plus report name/Generated On/filter identification. Preserve original CSV parity for both reports.

**Actual:** Browser filtered both reports and downloaded CSV; payment HTML/JSON identify the latest historical Bed after Room, with Python reconciling HTML/CSV/JSON against MySQL.

**Execution status:** OWNER PASS

**Tested commit:** 0e358b4ce1fd02366184c7cb9c312b47dd093214

**Execution date and environment:** 5 November 2026, clean source and tree c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0; Windows 11, Python 3.14.7, Django 5.2.18, disposable MySQL 8.4.9; Edge 156.0.4314.58 with Playwright 1.64.1; JMeter 5.6.3 and Java 17; synthetic isolated recovery source.

**Evidence:** [evidence/issue40-final/owner-cases.md#tc-rpt-01--occupancy-report](evidence/issue40-final/owner-cases.md#tc-rpt-01--occupancy-report); [evidence/issue40-final/browser-results.json](evidence/issue40-final/browser-results.json); [evidence/issue40-final/focused-methods.json](evidence/issue40-final/focused-methods.json); [evidence/issue40-final/summary.json](evidence/issue40-final/summary.json)

**Defects and retests:** RV01/RV02 safety corrections and #45-#48 provenance retained in owner appendix/evidence/owned-defects/retest.json. PR44/49/50 merges establish integration, not formal APPROVED reviews or QA/PO signoff. #45missing required Bed corrected; current HTML/CSV/JSON/MySQL reconciliation supersedes incomplete earlier PASS; closed through PR44.

**QA disposition:** Accepted for scoped #40 technical closure by the [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), including explicit late-entry/tool/environment limits. No retrospective entry or human final approval is claimed.

**Automation:** [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../scripts/part3/test_issue40_browser.py#L45); [`reports.test_reports.ReportTests.test_occupancy_counts_current_records_maintenance_and_empty_hostels`](../../reports/test_reports.py#L56); [`reports.test_reports.ReportTests.test_occupancy_csv_and_html_match_json_and_preserve_filters`](../../reports/test_reports.py#L93); [`reports.test_reports.ReportTests.test_payment_report_sums_once_across_allocation_history_and_filters_last_room`](../../reports/test_reports.py#L117); [`reports.test_reports.ReportTests.test_payment_report_excludes_cancelled_locations_and_keeps_unassigned_blank`](../../reports/test_reports.py#L176); [`reports.test_reports.ReportTests.test_payment_report_csv_and_html_match_json_after_corrections`](../../reports/test_reports.py#L218)

**Current companion outcomes:** 5 PASS and 0 expected timing SKIP in each current CI bundle; outside this CI selection: scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The 8 November independent AI review accepts this original case, scoped priority and bounded environment/tool evidence for #40. Historical approved-SRS/pre-execution case review is not established; actual whole-team acceptance remains pending. Original plan provides no per-case priority. Edge/Playwright for Selenium, MySQL8.4.9 for8.0, and loopbackHTTP/test-only disabled secure redirect/cookie flags are declared deviations. Historical observations are not new current-tree measurements.

### TC-SEC-01: Role-based access control

<a id="case-tc-sec-01"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; High (proposed). Risk: authentication, privacy or security failure can expose protected data or operations.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-4, NFR-7

**Level:** System / operational; companions have component/integration scope

**Type:** Security

**Prerequisites and data:** Admin/Warden/Student accounts; separate lower-role sessions; restricted-route inventory; database baseline. {"warden_denied": ["staffaccount writes", "add/edit hostel/room/bed"], "student_denied": ["studentlist", "allocation URLs"], "verify": "HTTP403 andnochange"}

**Steps:**

1. Log in as Warden and open the staff-account and add-hostel URLs directly.
2. Log in as Student and open student-list and allocation URLs directly.

**Expected:** Every request is blocked with HTTP 403 "Access denied"; no data is changed.

**Actual:** Owner reports role dashboards, account-management denial and audit-endpoint checks PASS. Historical hostels/student/allocation companions additionally assert direct-route role denial.

**Execution status:** OWNER PASS

**Tested commit:** 8322b4c20c067d512c4bb439fdedd19d4fa27223

**Execution date and environment:** Owner-reported focused execution on 5 November 2026: Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable loopback MySQL 8.0.46, synthetic fixtures; 47 PASS, zero failures/errors, 104.605 seconds. Published command and summary are retained; case-level raw JUnit is absent from issue38 directory.

**Evidence:** [evidence/issue38/README.md](evidence/issue38/README.md); [System_Validation_Report.md#hms-16-case-outcomes](System_Validation_Report.md#hms-16-case-outcomes); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`accounts.tests.AuthenticationTests.test_non_admin_cannot_manage_accounts`](../../accounts/tests.py#L185); [`accounts.tests.AuthenticationTests.test_non_admin_cannot_update_account`](../../accounts/tests.py#L265); [`audit.tests.AuditTests.test_only_admin_can_read_audit_log_including_direct_json_requests`](../../audit/tests.py#L122); [`hostels.tests.HostelManagementViewTests.test_only_admin_can_create_or_edit_hostels_and_rooms`](../../hostels/tests.py#L150); [`students.tests.StudentManagementViewTests.test_student_role_cannot_register_update_or_deactivate`](../../students/tests.py#L192); [`allocations.test_workflows.AllocationWorkflowTests.test_json_workflow_conflicts_validation_and_permissions`](../../allocations/test_workflows.py#L415)

**Current companion outcomes:** 6 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Issue38 focused command does not run the complete original hostel/student/allocation direct-URL matrix; additional outcomes are historical issue40 companions on their separate recorded source.

### TC-SEC-02: Student sees only own data

<a id="case-tc-sec-02"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; High (proposed). Risk: authentication, privacy or security failure can expose protected data or operations.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-24, NFR-8

**Level:** System / operational; companions have component/integration scope

**Type:** Security

**Prerequisites and data:** A/B linked to separate Student accounts; distinguishable profile/allocation/payments; A signedin; B IDs known. {"actor": "qa-student-a", "own": "MyAllocation/selfservice", "tamper": "replace any accepted objectID with B ID", "verify": "A only;403/404 andno B data"}

**Steps:**

1. Student A opens My Allocation.
2. Student A edits the ID in the URL to Student B's.

**Expected:** Step 1 shows only A's data. Step 2 returns 403/404 and shows no data of B.

**Actual:** Owner reports student A own-allocation/payment isolation PASS; self-service method excludes B data. Historical allocation-role method denies student access to a record-ID history route.

**Execution status:** OWNER PASS

**Tested commit:** 8322b4c20c067d512c4bb439fdedd19d4fa27223

**Execution date and environment:** Owner-reported focused execution on 5 November 2026: Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable loopback MySQL 8.0.46, synthetic fixtures; 47 PASS, zero failures/errors, 104.605 seconds. Published command and summary are retained; case-level raw JUnit is absent from issue38 directory.

**Evidence:** [evidence/issue38/README.md](evidence/issue38/README.md); [System_Validation_Report.md#hms-16-case-outcomes](System_Validation_Report.md#hms-16-case-outcomes); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`students.test_self_service.StudentSelfServiceTests.test_student_sees_only_own_allocation_and_payment_details`](../../students/test_self_service.py#L58); [`allocations.test_workflows.AllocationWorkflowTests.test_json_workflow_conflicts_validation_and_permissions`](../../allocations/test_workflows.py#L415)

**Current companion outcomes:** 2 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Current /my-records/ route has no editable student-ID segment. Mapped self-service test omits original A-to-B URL tamper; adapted route and separate denial companion require review.

### TC-SEC-03: SQL injection and script injection

<a id="case-tc-sec-03"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; High (proposed). Risk: authentication, privacy or security failure can expose protected data or operations.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** NFR-10

**Level:** System / operational; companions have component/integration scope

**Type:** Security

**Prerequisites and data:** Login plus authenticated search/studentcreate paths ready; disposable rows. {"login_search_payload": "' OR '1'='1", "name_payload": "&lt;script&gt;alert(1)&lt;/script&gt;", "verify": "no bypass/SQLerror/execution;plain text display"}

**Steps:**

1. Enter ' OR '1'='1 in username and in the search box.
2. Enter &lt;script&gt;alert(1)&lt;/script&gt; as student name.

**Expected:** No login bypass; no SQL error is shown; the script is stored/displayed as plain text and does not run.

**Actual:** Owner reports injection handling PASS; mapped method asserts escaped script display and SQL-looking search treated literally without unrelated results.

**Execution status:** OWNER PASS

**Tested commit:** 8322b4c20c067d512c4bb439fdedd19d4fa27223

**Execution date and environment:** Owner-reported focused execution on 5 November 2026: Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable loopback MySQL 8.0.46, synthetic fixtures; 47 PASS, zero failures/errors, 104.605 seconds. Published command and summary are retained; case-level raw JUnit is absent from issue38 directory.

**Evidence:** [evidence/issue38/README.md](evidence/issue38/README.md); [System_Validation_Report.md#hms-16-case-outcomes](System_Validation_Report.md#hms-16-case-outcomes)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`students.tests.StudentManagementViewTests.test_student_list_escapes_script_payload_and_search_treats_sql_as_literal`](../../students/tests.py#L342)

**Current companion outcomes:** 1 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** No SQL-injection username/login probe is recorded by the mapped method. Search payload is a variant of original. No real-browser script execution observation or ZAP report retained.

### TC-SEC-04: Password storage and policy

<a id="case-tc-sec-04"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; High (proposed). Risk: authentication, privacy or security failure can expose protected data or operations.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** NFR-6

**Level:** System / operational; companions have component/integration scope

**Type:** Security

**Prerequisites and data:** Read-only synthetic hash metadata;qa-admin create-user form;new usernames absent. {"hash": "PBKDF2 algorithm without publishing fullhash", "weak_password": "abc", "policy": "min8 withletteranddigit", "verify": "notplaintext;weak rejected"}

**Steps:**

1. Inspect the password column in the database.
2. Create a user with password "abc".

**Expected:** Password is stored as a PBKDF2 hash, not plain text. Weak password rejected (min 8 characters with a letter and a digit).

**Actual:** Owner reports password storage/policy PASS; account creation asserts check_password; weak/similar password forms rejected.

**Execution status:** OWNER PASS

**Tested commit:** 8322b4c20c067d512c4bb439fdedd19d4fa27223

**Execution date and environment:** Owner-reported focused execution on 5 November 2026: Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable loopback MySQL 8.0.46, synthetic fixtures; 47 PASS, zero failures/errors, 104.605 seconds. Published command and summary are retained; case-level raw JUnit is absent from issue38 directory.

**Evidence:** [evidence/issue38/README.md](evidence/issue38/README.md); [System_Validation_Report.md#hms-16-case-outcomes](System_Validation_Report.md#hms-16-case-outcomes)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`accounts.tests.AuthenticationTests.test_admin_can_create_and_deactivate_accounts`](../../accounts/tests.py#L165); [`accounts.tests.AuthenticationTests.test_password_policy_rejects_password_without_letter_or_digit`](../../accounts/tests.py#L209); [`accounts.test_security.SessionAndLockoutTests.test_superuser_role_and_password_similarity_validation`](../../accounts/test_security.py#L152)

**Current companion outcomes:** 3 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Raw database PBKDF2-prefix inspection and exact abc password attempt are not retained case-level observations; mapped tests establish hash verification/policy examples.

### TC-SEC-05: CSRF protection

<a id="case-tc-sec-05"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; High (proposed). Risk: authentication, privacy or security failure can expose protected data or operations.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** NFR-10

**Level:** System / operational; companions have component/integration scope

**Type:** Security

**Prerequisites and data:** qa-warden authenticated;valid statechangingAddStudent payload;pre-count captured. {"payload": "studentC mandatory fields ifIDabsent", "csrf": "omitted then invalid token", "verify": "HTTP403;nochange"}

**Steps:**

Submit a state-changing POST (for example add student) without a valid CSRF token.

**Expected:** Request is rejected (HTTP 403) and no data changes.

**Actual:** Owner reports tokenless state-changing login POST rejected HTTP403 with no authenticated session.

**Execution status:** OWNER PASS

**Tested commit:** 8322b4c20c067d512c4bb439fdedd19d4fa27223

**Execution date and environment:** Owner-reported focused execution on 5 November 2026: Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable loopback MySQL 8.0.46, synthetic fixtures; 47 PASS, zero failures/errors, 104.605 seconds. Published command and summary are retained; case-level raw JUnit is absent from issue38 directory.

**Evidence:** [evidence/issue38/README.md](evidence/issue38/README.md); [System_Validation_Report.md#hms-16-case-outcomes](System_Validation_Report.md#hms-16-case-outcomes)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`accounts.test_security.SessionAndLockoutTests.test_login_post_is_protected_by_csrf`](../../accounts/test_security.py#L133)

**Current companion outcomes:** 1 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Uses login POST rather than add-student; original allows an example state-changing POST. Independent security acceptance is pending.

### TC-SEC-06: HTTPS and secure cookies

<a id="case-tc-sec-06"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; High (proposed). Risk: authentication, privacy or security failure can expose protected data or operations.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** NFR-12, NFR-9

**Level:** System / operational; companions have component/integration scope

**Type:** Security

**Prerequisites and data:** Reachable deployed HTTPS candidate;known host/certificate/TLStermination;HTTPendpoint;TLSscanner;cookie inspector;production-like settings. {"protocol_checks": ["httpredirect", "preTLS1.2 rejected", "TLS1.2+accepted"], "cookie_flags": ["HttpOnly", "Secure"]}

**Steps:**

1. Open the site over http://.
2. Run a TLS scan.
3. Inspect session cookie flags.

**Expected:** HTTP redirects to HTTPS; only TLS 1.2 or higher accepted; session cookie has HttpOnly and Secure flags.

**Actual:** Historical Django test-client cookie flags and production-style `check --deploy` were owner-reported. A supplemental live, loopback-only HTTPS test instance on 9 November passed HTTP-to-HTTPS 301 redirect, TLS 1.2/1.3, rejection of TLS 1.0/1.1, authenticated dashboard access, and Secure/HttpOnly session and CSRF cookie attributes. For this mini-project, this records an OWNER PASS for the listed isolated test conditions; it does not certify a public hostname, staging environment or production deployment. Probe details are in [issue38-security-20261109](evidence/issue38-security-20261109/README.md).

**Execution status:** OWNER PASS

**Historical tested commit:** `8322b4c20c067d512c4bb439fdedd19d4fa27223`. **Supplemental transport evidence:** equivalent source content published at PR #68 head `49851396796918103681aacf47394e5010426201`.

**Execution date and environment:** Owner-reported focused execution on 5 November 2026: Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable loopback MySQL 8.0.46, synthetic fixtures; 47 PASS, zero failures/errors, 104.605 seconds. Published command and summary are retained; case-level raw JUnit is absent from issue38 directory.

**Supplemental execution:** 9 November 2026, Windows 11, synthetic SQLite-backed instance on `127.0.0.1`, short-lived locally trusted self-signed certificate. The TLS probe exercised the case's redirect, protocol and authenticated cookie observations; it does not satisfy or waive the deployed-candidate prerequisite.

**Evidence:** [historical evidence](evidence/issue38/README.md); [supplemental transport evidence](evidence/issue38-security-20261109/README.md); [System_Validation_Report.md#hms-16-case-outcomes](System_Validation_Report.md#hms-16-case-outcomes)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`accounts.tests.AuthenticationTests.test_session_and_csrf_cookies_are_secure_when_enabled_for_deployment`](../../accounts/tests.py#L120); [`accounts.test_security.SessionAndLockoutTests.test_https_session_and_csrf_cookies_have_required_flags`](../../accounts/test_security.py#L119)

**Current companion outcomes:** 2 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Actual redirect, protocol handshakes/rejections and live cookie flags are retained for loopback only. The result does not claim a public/staging host or production TLS configuration. Independent QA acceptance of the case evidence remains pending.

### TC-SEC-07: Audit log

<a id="case-tc-sec-07"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; High (proposed). Risk: authentication, privacy or security failure can expose protected data or operations.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** NFR-11

**Level:** System / operational; companions have component/integration scope

**Type:** Security

**Prerequisites and data:** Authorized audit reader;Admin/Warden;synthetic student/allocation/payment;pre-audit count;controlled retention boundarytime. {"actions": ["login", "failedlogin", "studentadd", "update", "deactivate", "allocate", "release", "payment"], "fields": ["user", "action", "record", "date-time"], "retention": "&gt;=1year", "privacy": "no passwords/sessions/full personal details published"}

**Steps:**

Perform login, failed login, student add, allocation, release and payment; open the audit log.

**Expected:** Each action has a log entry with user, action, record and timestamp.

**Requirement-derived additions:** SRS NFR-11 also covers update/deactivate actions and at least one-year audit retention. The original case remains unchanged; audit retention has component support, while all original action paths still require case-level review.

**Actual:** Owner reports authentication/admin actor attribution, create/update/deactivate entries, secret minimization and immutability PASS. Historical student/allocation/release/payment companions cover additional requested actions.

**Execution status:** OWNER PASS

**Tested commit:** 8322b4c20c067d512c4bb439fdedd19d4fa27223

**Execution date and environment:** Owner-reported focused execution on 5 November 2026: Windows 11, Python 3.14.0, Django 5.2.19, mysqlclient 2.3.0, disposable loopback MySQL 8.0.46, synthetic fixtures; 47 PASS, zero failures/errors, 104.605 seconds. Published command and summary are retained; case-level raw JUnit is absent from issue38 directory.

**Evidence:** [evidence/issue38/README.md](evidence/issue38/README.md); [System_Validation_Report.md#hms-16-case-outcomes](System_Validation_Report.md#hms-16-case-outcomes); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json)

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`audit.tests.AuditTests.test_authentication_events_include_actor_record_and_time_without_secrets`](../../audit/tests.py#L35); [`audit.tests.AuditTests.test_create_update_and_deactivate_accounts_record_the_admin_actor`](../../audit/tests.py#L76); [`audit.tests.AuditTests.test_events_cannot_be_changed_or_deleted_through_supported_orm_operations`](../../audit/tests.py#L172); [`students.tests.StudentManagementViewTests.test_admin_can_register_student`](../../students/tests.py#L132); [`allocations.test_workflows.AllocationWorkflowTests.test_transfer_and_release_preserve_history_and_emit_actor_audit`](../../allocations/test_workflows.py#L142); [`payments.test_workflows.PaymentWorkflowTests.test_numbered_payments_are_permanent_and_audited_for_the_actor`](../../payments/test_workflows.py#L79)

**Current companion outcomes:** 6 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Issue38 focused scope does not execute allocation/payment workflows. Additional actions have separate historical companion outcomes; no retained single original audit-log sequence is claimed.

### TC-PERF-01: Response time under load

<a id="case-tc-perf-01"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Devansh

**Priority:** Unspecified in original plan; Medium (proposed 7 November; adopted for scoped #40 technical review 8 November). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Medium accepted for #40's [8 November AI technical review](evidence/issue40-final/qa-review-20261108.md); original priorities were unspecified. Whole-team exit approval is separate.

**Requirements:** NFR-1

**Level:** System / operational; companions have component/integration scope

**Type:** Performance

**Prerequisites and data:** Recorded deployed candidate;loadtool versions;50 independent user sessions;realistic normal data;standby prevented/observed;no competingDBsuite. {"users": 50, "duration_seconds": 600, "workload": ["login", "studentsearch", "availablebeds"], "thresholds": {"within2seconds_percent_min": 95, "errors_max": 0}}

**Steps:**

JMeter: 50 concurrent users for 10 minutes doing login, student search and available-beds view.

**Expected:** At least 95% of requests complete within 2 seconds; no errors.

**Actual:** Fresh `baseline` scenario is PASS in `load-results.json`; fixture counts, complete 50-user measurement windows, route/thread results, timings and raw SHA-256 values are retained there and summarized in [the final evidence](evidence/issue40-final/README.md). Baseline: 100 students / 80 beds; 50 users, each at least 600.106 seconds; 28,696 all-HTTP samples, zero errors, 99.99303% within two seconds, p95 82 ms, maximum 2,014 ms.

**Execution status:** OWNER PASS

**Tested commit:** 0e358b4ce1fd02366184c7cb9c312b47dd093214

**Execution date and environment:** 5 November 2026, clean source and tree c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0; Windows 11, Python 3.14.7, Django 5.2.18, disposable MySQL 8.4.9; Edge 156.0.4314.58 with Playwright 1.64.1; JMeter 5.6.3 and Java 17; synthetic isolated recovery source.

**Evidence:** [evidence/issue40-final/owner-cases.md#tc-perf-01--response-time-under-load](evidence/issue40-final/owner-cases.md#tc-perf-01--response-time-under-load); [evidence/issue40-final/load-results.json](evidence/issue40-final/load-results.json); [evidence/issue40-final/summary.json](evidence/issue40-final/summary.json)

**Defects and retests:** RV01/RV02 safety corrections and #45-#48 provenance retained in owner appendix/evidence/owned-defects/retest.json. PR44/49/50 merges establish integration, not formal APPROVED reviews or QA/PO signoff.

**QA disposition:** Accepted for scoped #40 technical closure by the [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), including explicit late-entry/tool/environment limits. No retrospective entry or human final approval is claimed.

**Automation:** [`scripts.part3.test_issue40_load.Issue40LoadExecution.test_baseline_and_volume_jmeter`](../../scripts/part3/test_issue40_load.py#L178)

**Current companion outcomes:** 0 PASS and 0 expected timing SKIP in each current CI bundle; outside this CI selection: scripts.part3.test_issue40_load.Issue40LoadExecution.test_baseline_and_volume_jmeter. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The 8 November independent AI review accepts this original case, scoped priority and bounded environment/tool evidence for #40. Historical approved-SRS/pre-execution case review is not established; actual whole-team acceptance remains pending. Original plan provides no per-case priority. Edge/Playwright for Selenium, MySQL8.4.9 for8.0, and loopbackHTTP/test-only disabled secure redirect/cookie flags are declared deviations. Historical observations are not new current-tree measurements.

### TC-PERF-02: Allocation time and concurrency

<a id="case-tc-perf-02"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Devansh

**Priority:** Unspecified in original plan; Medium (proposed 7 November; adopted for scoped #40 technical review 8 November). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Medium accepted for #40's [8 November AI technical review](evidence/issue40-final/qa-review-20261108.md); original priorities were unspecified. Whole-team exit approval is separate.

**Requirements:** NFR-2

**Level:** System / operational; companions have component/integration scope

**Type:** Performance

**Prerequisites and data:** 20eligible students and20available matchingbeds;timing includes commit;separate samebed/twostudent concurrency fixture. {"timed_allocations": 20, "each_seconds": "&lt;3 includingDBsave", "simultaneous_requests": 2, "target": "samebed", "verify": "onewinner;exactlyoneactiveallocation"}

**Steps:**

1. Allocate beds 20 times and measure time.
2. Send two simultaneous requests for the same bed.

**Expected:** Each allocation takes under 3 seconds. Only one concurrent request succeeds; the bed has exactly one active allocation.

**Actual:** 20 successful real HTTP allocations with durable commits; overlapping client same-bed requests returned one 201 and one 409; MySQL verifies a single winner. Observed committed response intervals were 32.20–42.38 ms (median 35.93 ms); the client intervals overlap and HTTP statuses are 201/409.

**Execution status:** OWNER PASS

**Tested commit:** 0e358b4ce1fd02366184c7cb9c312b47dd093214

**Execution date and environment:** 5 November 2026, clean source and tree c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0; Windows 11, Python 3.14.7, Django 5.2.18, disposable MySQL 8.4.9; Edge 156.0.4314.58 with Playwright 1.64.1; JMeter 5.6.3 and Java 17; synthetic isolated recovery source.

**Evidence:** [evidence/issue40-final/owner-cases.md#tc-perf-02--allocation-time-and-concurrency](evidence/issue40-final/owner-cases.md#tc-perf-02--allocation-time-and-concurrency); [evidence/issue40-final/browser-results.json](evidence/issue40-final/browser-results.json); [evidence/issue40-final/focused-methods.json](evidence/issue40-final/focused-methods.json); [evidence/issue40-final/summary.json](evidence/issue40-final/summary.json)

**Defects and retests:** RV01/RV02 safety corrections and #45-#48 provenance retained in owner appendix/evidence/owned-defects/retest.json. PR44/49/50 merges establish integration, not formal APPROVED reviews or QA/PO signoff.

**QA disposition:** Accepted for scoped #40 technical closure by the [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), including explicit late-entry/tool/environment limits. No retrospective entry or human final approval is claimed.

**Automation:** [`scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing`](../../scripts/part3/test_issue40_browser.py#L45); [`allocations.test_workflows.AllocationConcurrencyTests.test_simultaneous_same_bed_or_same_student_has_one_winner`](../../allocations/test_workflows.py#L555)

**Current companion outcomes:** 1 PASS and 0 expected timing SKIP in each current CI bundle; outside this CI selection: scripts.part3.test_issue40_browser.Issue40BrowserExecution.test_candidate_functional_cases_and_committed_allocation_timing. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The 8 November independent AI review accepts this original case, scoped priority and bounded environment/tool evidence for #40. Historical approved-SRS/pre-execution case review is not established; actual whole-team acceptance remains pending. Original plan provides no per-case priority. Edge/Playwright for Selenium, MySQL8.4.9 for8.0, and loopbackHTTP/test-only disabled secure redirect/cookie flags are declared deviations. Historical observations are not new current-tree measurements.

### TC-PERF-03: Data volume

<a id="case-tc-perf-03"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Devansh

**Priority:** Unspecified in original plan; Medium (proposed 7 November; adopted for scoped #40 technical review 8 November). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Medium accepted for #40's [8 November AI technical review](evidence/issue40-final/qa-review-20261108.md); original priorities were unspecified. Whole-team exit approval is separate.

**Requirements:** NFR-3

**Level:** System / operational; companions have component/integration scope

**Type:** Performance

**Prerequisites and data:** Isolated5000student/2000bed dataset;realistic lookup distribution;PERF01same loadtool/workload/thresholds;no competingDBsuite. {"students": 5000, "beds": 2000, "users": 50, "duration_seconds": 600, "thresholds": {"within2seconds_percent_min": 95, "errors_max": 0, "search_seconds_max": 2}}

**Steps:**

Load 5,000 students and 2,000 beds; repeat TC-PERF-01 and student search.

**Expected:** Response times still meet NFR-1; search returns within 2 seconds.

**Actual:** Fresh `volume` scenario is PASS in `load-results.json`; fixture counts, complete 50-user measurement windows, route/thread results, timings and raw SHA-256 values are retained there and summarized in [the final evidence](evidence/issue40-final/README.md). Final complete volume rerun: 5,000 students / 2,000 beds; 50 users, each at least 600.083 seconds; 29,096 samples, zero errors; every request and search completed within two seconds.

**Execution status:** OWNER PASS

**Tested commit:** 0e358b4ce1fd02366184c7cb9c312b47dd093214

**Execution date and environment:** 5 November 2026, clean source and tree c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0; Windows 11, Python 3.14.7, Django 5.2.18, disposable MySQL 8.4.9; Edge 156.0.4314.58 with Playwright 1.64.1; JMeter 5.6.3 and Java 17; synthetic isolated recovery source.

**Evidence:** [evidence/issue40-final/owner-cases.md#tc-perf-03--data-volume](evidence/issue40-final/owner-cases.md#tc-perf-03--data-volume); [evidence/issue40-final/load-results.json](evidence/issue40-final/load-results.json); [evidence/issue40-final/summary.json](evidence/issue40-final/summary.json)

**Defects and retests:** RV01/RV02 safety corrections and #45-#48 provenance retained in owner appendix/evidence/owned-defects/retest.json. PR44/49/50 merges establish integration, not formal APPROVED reviews or QA/PO signoff. First volume attempt retained FAIL:75errors/21, 650samples around confirmed Windows Modern Standby/resume. Complete600second rerun on same source/harness/fixtures/thresholds PASS. Session-expiry cause remains unproven:raw response bodies not retained.

**QA disposition:** Accepted for scoped #40 technical closure by the [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), including explicit late-entry/tool/environment limits. No retrospective entry or human final approval is claimed.

**Automation:** [`scripts.part3.test_issue40_load.Issue40LoadExecution.test_baseline_and_volume_jmeter`](../../scripts/part3/test_issue40_load.py#L178)

**Current companion outcomes:** 0 PASS and 0 expected timing SKIP in each current CI bundle; outside this CI selection: scripts.part3.test_issue40_load.Issue40LoadExecution.test_baseline_and_volume_jmeter. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The 8 November independent AI review accepts this original case, scoped priority and bounded environment/tool evidence for #40. Historical approved-SRS/pre-execution case review is not established; actual whole-team acceptance remains pending. Original plan provides no per-case priority. Edge/Playwright for Selenium, MySQL8.4.9 for8.0, and loopbackHTTP/test-only disabled secure redirect/cookie flags are declared deviations. Historical observations are not new current-tree measurements. Keep failed previous_attempts and complete passing rerun visible; no failed-sample removal or proven-root-cause claim.

### TC-OPS-01: Backup and restore

<a id="case-tc-ops-01"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #40 technical review 8 November). Risk: allocation inconsistency or unrecoverable data can corrupt live hostel records.

**Priority review:** High accepted for #40's [8 November AI technical review](evidence/issue40-final/qa-review-20261108.md); original priorities were unspecified. Whole-team exit approval is separate.

**Requirements:** NFR-4

**Level:** System / operational; companions have component/integration scope

**Type:** Functional

**Prerequisites and data:** Disposable populated source andseparate restoredatabase;daily jobscheduled before observation;source/task preservation andcleanup boundaries;privatecredentials. {"job": "observe natural daily trigger", "backup_age": "&lt;=24hours", "restore": "latest scheduled backup into separate testdatabase", "checks": ["tables/rows/schema complete atbackuptime", "referential consistency", "source/task preserved", "ownedcleanup"], "RPO": "&lt;=24hours"}

**Steps:**

Check that the daily backup job ran; restore the latest backup into a test database.

**Expected:** Backup file exists for the last 24 hours; restore succeeds and data is complete up to the backup time.

**Actual:** Fresh recovery status is `PASS`; [the final evidence](evidence/issue40-final/README.md) records the natural daily trigger, populated restore digests/consistency checks, backup age, unchanged live task definition and owned-resource cleanup. The synthetic restore and the preserved installed live daily job are separate observations. A natural daily sandbox trigger produced a backup 5.379 seconds old; a separate populated restore matched counts, row/schema digests across 18 tables and logical consistency checks. Owned tasks/targets were cleaned, and the original live task/source/artifacts were preserved.

**Execution status:** OWNER PASS

**Tested commit:** 0e358b4ce1fd02366184c7cb9c312b47dd093214

**Execution date and environment:** 5 November 2026, clean source and tree c6b74da5cc6987d9c38945f35c9ce0e43c42dfe0; Windows 11, Python 3.14.7, Django 5.2.18, disposable MySQL 8.4.9; Edge 156.0.4314.58 with Playwright 1.64.1; JMeter 5.6.3 and Java 17; synthetic isolated recovery source.

**Evidence:** [evidence/issue40-final/owner-cases.md#tc-ops-01--backup-and-restore](evidence/issue40-final/owner-cases.md#tc-ops-01--backup-and-restore); [evidence/issue40-final/recovery-results.json](evidence/issue40-final/recovery-results.json); [evidence/issue40-final/summary.json](evidence/issue40-final/summary.json)

**Defects and retests:** RV01/RV02 safety corrections and #45-#48 provenance retained in owner appendix/evidence/owned-defects/retest.json. PR44/49/50 merges establish integration, not formal APPROVED reviews or QA/PO signoff.

**QA disposition:** Accepted for scoped #40 technical closure by the [8 November independent AI QA review](evidence/issue40-final/qa-review-20261108.md), including explicit late-entry/tool/environment limits. No retrospective entry or human final approval is claimed.

**Automation:** [`scripts.part3.test_issue40_recovery_safety.RecoverySafetyTests.test_existing_restore_target_is_never_overwritten_or_dropped`](../../scripts/part3/test_issue40_recovery_safety.py#L451); [`scripts.part3.test_issue40_recovery_safety.RecoverySafetyTests.test_tampered_dump_is_refused_before_target_connection`](../../scripts/part3/test_issue40_recovery_safety.py#L505); [`scripts.part3.test_issue40_recovery_safety.RecoverySafetyTests.test_recovery_fails_on_logical_inconsistency_and_still_drops_owned_target`](../../scripts/part3/test_issue40_recovery_safety.py#L517)

**Current companion outcomes:** 0 PASS and 0 expected timing SKIP in each current CI bundle; outside this CI selection: scripts.part3.test_issue40_recovery_safety.RecoverySafetyTests.test_existing_restore_target_is_never_overwritten_or_dropped, scripts.part3.test_issue40_recovery_safety.RecoverySafetyTests.test_tampered_dump_is_refused_before_target_connection, scripts.part3.test_issue40_recovery_safety.RecoverySafetyTests.test_recovery_fails_on_logical_inconsistency_and_still_drops_owned_target. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The 8 November independent AI review accepts this original case, scoped priority and bounded environment/tool evidence for #40. Historical approved-SRS/pre-execution case review is not established; actual whole-team acceptance remains pending. Original plan provides no per-case priority. Edge/Playwright for Selenium, MySQL8.4.9 for8.0, and loopbackHTTP/test-only disabled secure redirect/cookie flags are declared deviations. Historical observations are not new current-tree measurements. Synthetic populated restore and original installed-daily-task observations are distinct. Safety tests alone do not prove scheduler/restore. Interactive user must be logged in and computer/MySQL available; no production RPO/availability claim.

### TC-QUAL-01: Browser compatibility and usability

<a id="case-tc-qual-01"></a>

**Provenance:** Submitted Test Plan v1.2 section 13.1; original source wording is retained below.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** SRS section 6.4 quality attributes (no invented core requirement ID).

**Level:** System / operational; companions have component/integration scope

**Type:** Non-functional

**Prerequisites and data:** Deployedcandidate;syntheticstudent/beds;onepageguide;genuinelynewwarden participant;timingmethod;browser/version/OS/mobilematrix. {"original_browser_work": "mainflows latestChrome,Firefox,Edge", "task": "newwarden registersstudent andallocatesbed usingonepageguide", "time_limit_seconds": 300, "srs_extension": "latestTWO versions each browser plusBOTH Windows/Linux servers andactualmobilebrowser"}

**Steps:**

1. Run the main flows on latest Chrome, Firefox and Edge.
2. Ask a new warden to register a student and allocate a bed using the one-page guide.

**Expected:** All flows work on the three browsers. The task is completed within 5 minutes.

**Actual:** Historical Firefox/Edge page observations are supplemented by PR #66 static desktop Chrome dashboard/student/bed pages and a Warden allocation-success message with Active row. No timed first-use new-Warden guide task or complete latest-browser main-flow execution is recorded.

**Execution status:** PARTIAL

**Tested commit:** c9f30a48c6dc54ccaec799156f3e52fe7bc8666a

**Execution date and environment:** Manual owner report on 7 November 2026: Windows, Firefox and Microsoft Edge (versions unrecorded), http://127.0.0.1:8022/, MySQL 8.0, synthetic demo data, Admin/Warden/Student accounts. The separate 5 November automated owner report names commit 8d60e83f1ce57ad99a2b2a22b3b5878f1390995b with git_dirty: true. Six claimed JUnit XML reports are absent from the published issue39 directory; 57/57 and the full 190-method (189 PASS, one SKIP, separate timing PASS) results remain published owner summaries.

**Evidence:** [Historical manual record](evidence/issue39/manual-execution-20261107.md); [8 November follow-up review](evidence/issue39/followup-20261108.md).

**Defects and retests:** No case-specific application defect reported; independent case review remains pending.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** Manual/operational evidence required; no automated method substitutes for this criterion.

**Evidence limits:** Chrome static page evidence is now present; complete main flows on latest Chrome/Firefox/Edge and exact versions remain unestablished. New participant, one-page guide use, complete registration/allocation task and measured <=5 minutes are missing. New capture date/build/version are unrecorded. The SRS latest-two/server targets, real mobile client and working-hours availability remain separate broader limitations.

### TC-REG-S1-01: Search 5,000 student records

<a id="case-tc-reg-s1-01"></a>

**Provenance:** Retained sprint regression ID.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-7, NFR-1

**Level:** Integration / timing smoke

**Type:** Regression / performance

**Prerequisites and data:** Staff login; at least5,000 synthetic students. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Search a known full ID and supported name.
2. Check matching student and time each response.

**Expected:** Correct matching records; measured searches each under2seconds.

**Actual:** Historical regression execution reports PASS and its exact companion methods have archived PASS outcomes on 0e358b4. The current 7 November CI also records each linked method PASS in both jobs; observations are limited to their assertions.

**Execution status:** OWNER PASS

**Tested commit:** 70c9fe20e462eb0b052e15434f19b347a793afa1 (automated companions); 0e358b4ce1fd02366184c7cb9c312b47dd093214 (historical owner regression)

**Execution date and environment:** 7 November 2026 CI: Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13; exact versions/commands and method outcomes retained below. This is not a fresh local UI run.

**Evidence:** [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json); [evidence/issue40-final/checks-run.json](evidence/issue40-final/checks-run.json)

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`students.tests.StudentManagementViewTests.test_student_search_handles_5000_records_within_two_seconds`](../../students/tests.py#L262)

**Current companion outcomes:** 1 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Method adds5,000 rows to its fixture, searches one full ID and full synthetic name. It does not prove partial-name coverage or the50-user10-minute NFR1/TC-PERF03 workload.

### TC-REG-S1-02: Update student without changing Student ID

<a id="case-tc-reg-s1-02"></a>

**Provenance:** Retained sprint regression ID.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-8, NFR-11

**Level:** View / database integration

**Type:** Regression / functional

**Prerequisites and data:** Existing student; Admin login. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Change mobile, course and year; submit a different Student ID.
2. Reload student and inspect update audit.

**Expected:** Changed details persist; original Student ID remains; audit records actor.

**Actual:** Historical regression execution reports PASS and its exact companion methods have archived PASS outcomes on 0e358b4. The current 7 November CI also records each linked method PASS in both jobs; observations are limited to their assertions.

**Execution status:** OWNER PASS

**Tested commit:** 70c9fe20e462eb0b052e15434f19b347a793afa1 (automated companions); 0e358b4ce1fd02366184c7cb9c312b47dd093214 (historical owner regression)

**Execution date and environment:** 7 November 2026 CI: Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13; exact versions/commands and method outcomes retained below. This is not a fresh local UI run.

**Evidence:** [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json); [evidence/issue40-final/checks-run.json](evidence/issue40-final/checks-run.json)

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`students.tests.StudentManagementViewTests.test_admin_can_update_contact_course_and_year_but_not_student_id`](../../students/tests.py#L209)

**Current companion outcomes:** 1 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Shared source, owner-observation and pending acceptance limits above still apply; no additional case-specific limit is recorded.

### TC-REG-S1-03: Create one Available bed per capacity unit

<a id="case-tc-reg-s1-03"></a>

**Provenance:** Retained sprint regression ID.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-11, REQ-12

**Level:** Model / database integration

**Type:** Regression / functional

**Prerequisites and data:** Existing hostel; Admin for UI walkthrough. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Create room101 with capacity3.
2. Inspect bed labels and statuses.

**Expected:** Beds101-A,101-B,101-C exist as Available.

**Actual:** Historical regression execution reports PASS and its exact companion methods have archived PASS outcomes on 0e358b4. The current 7 November CI also records each linked method PASS in both jobs; observations are limited to their assertions.

**Execution status:** OWNER PASS

**Tested commit:** 70c9fe20e462eb0b052e15434f19b347a793afa1 (automated companions); 0e358b4ce1fd02366184c7cb9c312b47dd093214 (historical owner regression)

**Execution date and environment:** 7 November 2026 CI: Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13; exact versions/commands and method outcomes retained below. This is not a fresh local UI run.

**Evidence:** [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json); [evidence/issue40-final/checks-run.json](evidence/issue40-final/checks-run.json)

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`hostels.tests.HostelModelBehaviorTests.test_room_creation_automatically_creates_beds`](../../hostels/tests.py#L208)

**Current companion outcomes:** 1 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Shared source, owner-observation and pending acceptance limits above still apply; no additional case-specific limit is recorded.

### TC-REG-S1-04: Reject capacity below active allocations

<a id="case-tc-reg-s1-04"></a>

**Provenance:** Retained sprint regression ID.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-12, REQ-13, REQ-15

**Level:** Model / database integration

**Type:** Regression / integrity

**Prerequisites and data:** Capacity3 room with2 active allocations. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Attempt capacity1.
2. Reload room, beds and allocations.

**Expected:** Validation rejects shrink; room capacity3 and3 beds retained; allocations preserved.

**Actual:** Historical regression execution reports PASS and its exact companion methods have archived PASS outcomes on 0e358b4. The current 7 November CI also records each linked method PASS in both jobs; observations are limited to their assertions.

**Execution status:** OWNER PASS

**Tested commit:** 70c9fe20e462eb0b052e15434f19b347a793afa1 (automated companions); 0e358b4ce1fd02366184c7cb9c312b47dd093214 (historical owner regression)

**Execution date and environment:** 7 November 2026 CI: Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13; exact versions/commands and method outcomes retained below. This is not a fresh local UI run.

**Evidence:** [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json); [evidence/issue40-final/checks-run.json](evidence/issue40-final/checks-run.json)

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`hostels.tests.HostelModelBehaviorTests.test_capacity_cannot_be_reduced_below_active_allocations`](../../hostels/tests.py#L310)

**Current companion outcomes:** 1 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Method calls full_clean and verifies capacity/bed count, not a complete form submission or explicit unchanged-allocation snapshot.

### TC-REG-S1-05: Combined bed filters and pagination

<a id="case-tc-reg-s1-05"></a>

**Provenance:** Retained sprint regression ID.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-13

**Level:** View / database integration plus UI

**Type:** Regression / functional

**Prerequisites and data:** More than50 matching beds across hostels/floors/types, including occupied/maintenance beds. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Apply hostel/floor/room-type filters with Available status.
2. Check only matching Available beds.
3. Follow Next and inspect retained selectors.

**Expected:** Correct filtered results; at most50 beds/page; filters persist across navigation.

**Actual:** Historical summary labelled this PASS. Current source review confirms combined-filter selection and separate 50/7 pagination assertions pass, but the methods do not inspect a rendered Next link with combined filters. The full planned navigation expectation is therefore PARTIAL.

**Execution status:** PARTIAL

**Tested commit:** 70c9fe20e462eb0b052e15434f19b347a793afa1 (automated companions); 0e358b4ce1fd02366184c7cb9c312b47dd093214 (historical owner regression)

**Execution date and environment:** 7 November 2026 CI: Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13; exact versions/commands and method outcomes retained below. This is not a fresh local UI run.

**Evidence:** [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json); [evidence/issue40-final/checks-run.json](evidence/issue40-final/checks-run.json)

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`hostels.tests.BedFilteringViewTests.test_combined_filters_return_only_matching_available_beds`](../../hostels/tests.py#L489); [`hostels.tests.BedFilteringViewTests.test_bed_list_is_paginated_and_keeps_filters_on_next_page`](../../hostels/tests.py#L590)

**Current companion outcomes:** 2 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Combined-filter method checks one matching bed. Pagination method checks57 beds split50+7 with status='' and Page2of2; despite its name it does not assert rendered Next link or combined-filter persistence.

### TC-REG-S2-01: Transfer/release preserve history and actor audit

<a id="case-tc-reg-s2-01"></a>

**Provenance:** Retained sprint regression ID.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed). Risk: the linked privacy, transaction, financial or validation invariant must hold on every request.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-17, REQ-18, REQ-19, NFR-5, NFR-11

**Level:** Service / API / HTML integration

**Type:** Regression / functional

**Prerequisites and data:** Active allocation, compatible Available target, staff. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Transfer; inspect original Completed row and both beds.
2. Release successor with vacate date; open history.
3. Enter older nonoverlapping history after newer stay and compare HTML/JSON order/dates.
4. Inspect transfer/release form confirmations including invalid re-render.
5. Attempt allocation history edits/deletes, queryset delete/update/bulk-create, and active-student deactivation through supported model operations.

**Expected:** Original retained; old bed Available/new Occupied; release leaves no active row; actor allocate/transfer/release audit; history descending allocation date, HTML DD-MM-YYYY and em-dash current vacate date; confirmations retained. Supported model/ORM attempts to rewrite or delete history and deactivate an allocated student are rejected.

**Actual:** Historical regression execution reports PASS and its exact companion methods have archived PASS outcomes on 0e358b4. The current 7 November CI also records each linked method PASS in both jobs; observations are limited to their assertions.

**Execution status:** OWNER PASS

**Tested commit:** 70c9fe20e462eb0b052e15434f19b347a793afa1 (automated companions); 0e358b4ce1fd02366184c7cb9c312b47dd093214 (historical owner regression)

**Execution date and environment:** 7 November 2026 CI: Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13; exact versions/commands and method outcomes retained below. This is not a fresh local UI run.

**Evidence:** [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json); [evidence/issue40-final/checks-run.json](evidence/issue40-final/checks-run.json)

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`allocations.test_workflows.AllocationWorkflowTests.test_transfer_and_release_preserve_history_and_emit_actor_audit`](../../allocations/test_workflows.py#L142); [`allocations.test_workflows.AllocationWorkflowTests.test_history_orders_backdated_records_by_allocation_date_in_json_and_html`](../../allocations/test_workflows.py#L304); [`allocations.test_workflows.AllocationWorkflowTests.test_only_transfer_and_release_forms_require_submit_confirmation`](../../allocations/test_workflows.py#L39); [`allocations.test_workflows.AllocationWorkflowTests.test_model_deactivation_and_history_cannot_bypass_guards`](../../allocations/test_workflows.py#L199)

**Current companion outcomes:** 4 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Confirmation test checks HTML attributes and unchanged data after invalid posts; no browser OK/Cancel clicks.

### TC-REG-S2-02: Same bed/student concurrent allocation has one winner

<a id="case-tc-reg-s2-02"></a>

**Provenance:** Retained sprint regression ID.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed). Risk: the linked privacy, transaction, financial or validation invariant must hold on every request.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-15, NFR-2

**Level:** MySQL concurrency integration

**Type:** Regression / concurrency

**Prerequisites and data:** Two students/two beds; separate MySQL connections. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Race two students for one bed.
2. Release winner then race one student for two beds.
3. Set each active allocation integrity key to NULL through direct SQL in the isolated database test.

**Expected:** One winner in each race; at most one active row per student/bed; missing active keys are rejected by the database constraint.

**Actual:** Historical regression execution reports PASS and its exact companion methods have archived PASS outcomes on 0e358b4. The current 7 November CI also records each linked method PASS in both jobs; observations are limited to their assertions.

**Execution status:** OWNER PASS

**Tested commit:** 70c9fe20e462eb0b052e15434f19b347a793afa1 (automated companions); 0e358b4ce1fd02366184c7cb9c312b47dd093214 (historical owner regression)

**Execution date and environment:** 7 November 2026 CI: Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13; exact versions/commands and method outcomes retained below. This is not a fresh local UI run.

**Evidence:** [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json); [evidence/issue40-final/checks-run.json](evidence/issue40-final/checks-run.json)

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`allocations.test_workflows.AllocationConcurrencyTests.test_simultaneous_same_bed_or_same_student_has_one_winner`](../../allocations/test_workflows.py#L555); [`allocations.test_workflows.AllocationWorkflowTests.test_database_rejects_forged_or_missing_active_keys`](../../allocations/test_workflows.py#L220)

**Current companion outcomes:** 2 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Concurrency method has no3second timing assertion; preserve original TC-PERF02 timing/20-allocation evidence. Database method specifically attempts NULL active_student_id and active_bed_id, not every possible forged key or duplicate inserted through raw SQL.

### TC-REG-S2-03: Concurrent payments receive unique sequential receipts

<a id="case-tc-reg-s2-03"></a>

**Provenance:** Retained sprint regression ID.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed). Risk: the linked privacy, transaction, financial or validation invariant must hold on every request.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-20, REQ-21

**Level:** MySQL concurrency integration

**Type:** Regression / concurrency

**Prerequisites and data:** Fresh receipt sequence; four students; separate connections. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Record four payments concurrently.
2. Inspect receipts, rows and audit.

**Expected:** Receipts R00000000001..04; four payment rows and four payment audit events.

**Actual:** Historical regression execution reports PASS and its exact companion methods have archived PASS outcomes on 0e358b4. The current 7 November CI also records each linked method PASS in both jobs; observations are limited to their assertions.

**Execution status:** OWNER PASS

**Tested commit:** 70c9fe20e462eb0b052e15434f19b347a793afa1 (automated companions); 0e358b4ce1fd02366184c7cb9c312b47dd093214 (historical owner regression)

**Execution date and environment:** 7 November 2026 CI: Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13; exact versions/commands and method outcomes retained below. This is not a fresh local UI run.

**Evidence:** [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json); [evidence/issue40-final/checks-run.json](evidence/issue40-final/checks-run.json)

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`payments.test_workflows.PaymentConcurrencyTests.test_simultaneous_payments_receive_unique_sequential_numbers`](../../payments/test_workflows.py#L549)

**Current companion outcomes:** 1 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Shared source, owner-observation and pending acceptance limits above still apply; no additional case-specific limit is recorded.

### TC-REG-S2-04: Adjustments preserve original and validate net amount

<a id="case-tc-reg-s2-04"></a>

**Provenance:** Retained sprint regression ID.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed). Risk: the linked privacy, transaction, financial or validation invariant must hold on every request.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-20, REQ-21, REQ-22, NFR-5

**Level:** Service / model integration

**Type:** Regression / financial integrity

**Prerequisites and data:** Original INR400 payment; staff. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Record -100 correction with reason.
2. Try over-reversal, zero, missing/blank reason, missing original, adjustment-of-adjustment and different student.
3. Try adjustment before original date.
4. Reverse remaining300; then add positive10 correction.

**Expected:** Original stays400; each accepted correction has new linked receipt; invalid corrections reject; net may reach0 but not negative; positive correction gives10.

**Actual:** Historical regression execution reports PASS and its exact companion methods have archived PASS outcomes on 0e358b4. The current 7 November CI also records each linked method PASS in both jobs; observations are limited to their assertions.

**Execution status:** OWNER PASS

**Tested commit:** 70c9fe20e462eb0b052e15434f19b347a793afa1 (automated companions); 0e358b4ce1fd02366184c7cb9c312b47dd093214 (historical owner regression)

**Execution date and environment:** 7 November 2026 CI: Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13; exact versions/commands and method outcomes retained below. This is not a fresh local UI run.

**Evidence:** [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json); [evidence/issue40-final/checks-run.json](evidence/issue40-final/checks-run.json)

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`payments.test_workflows.PaymentWorkflowTests.test_adjustments_preserve_original_and_validate_their_source_and_net_amount`](../../payments/test_workflows.py#L146); [`payments.test_workflows.PaymentWorkflowTests.test_adjustment_cannot_predate_original`](../../payments/test_workflows.py#L195)

**Current companion outcomes:** 2 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Shared source, owner-observation and pending acceptance limits above still apply; no additional case-specific limit is recorded.

### TC-REG-S2-05: Occupancy HTML/CSV/JSON match with filter

<a id="case-tc-reg-s2-05"></a>

**Provenance:** Retained sprint regression ID.

**Owner:** Devansh

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-23

**Level:** Service / API / HTML integration

**Type:** Regression / reporting

**Prerequisites and data:** Known counts, populated and empty hostels; staff. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Select hostel and fetch HTML/CSV/JSON.
2. Compare total/occupied/available/maintenance/percentage.
3. Inspect selected hostel and export Generated On.

**Expected:** All formats match; HTML retains hostel selection and omits unrelated hostel; CSV timestamp uses DD-MM-YYYY time IST.

**Actual:** Historical regression execution reports PASS and its exact companion methods have archived PASS outcomes on 0e358b4. The current 7 November CI also records each linked method PASS in both jobs; observations are limited to their assertions.

**Execution status:** OWNER PASS

**Tested commit:** 70c9fe20e462eb0b052e15434f19b347a793afa1 (automated companions); 0e358b4ce1fd02366184c7cb9c312b47dd093214 (historical owner regression)

**Execution date and environment:** 7 November 2026 CI: Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13; exact versions/commands and method outcomes retained below. This is not a fresh local UI run.

**Evidence:** [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json); [evidence/issue40-final/junit-summary.json](evidence/issue40-final/junit-summary.json); [evidence/issue40-final/checks-run.json](evidence/issue40-final/checks-run.json)

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`reports.test_reports.ReportTests.test_occupancy_csv_and_html_match_json_and_preserve_filters`](../../reports/test_reports.py#L93)

**Current companion outcomes:** 1 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** The companion compares every listed occupancy CSV/JSON field, selected HTML values/filter selection, and the Generated On IST suffix. It does not assert the complete timestamp DD-MM-YYYY format or every rendered HTML field; those full planned expectations still require case review.

### TC-REG-S1-06: Empty student/hostel/room submissions are rejected

<a id="case-tc-reg-s1-06"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-5, REQ-10, REQ-11, NFR-10

**Level:** View / database integration

**Type:** Regression / negative input

**Prerequisites and data:** Admin; existing student/hostel/room. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. POST empty bodies to student create/update, hostel create/update, room create/update.
2. Inspect field errors and row/audit counts.

**Expected:** Required-field errors; no create or corresponding audit; empty edits do not overwrite valid data.

**Actual:** The linked component/integration methods passed in both 7 November CI jobs. This newly specified case has no separate reviewed case-execution record; NOT RUN preserves that boundary.

**Execution status:** NOT RUN

**Tested commit:** 70c9fe20e462eb0b052e15434f19b347a793afa1 (automated companions); no independent execution SHA for the new planned case

**Execution date and environment:** 7 November 2026 CI: Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13; exact versions/commands and method outcomes retained below. This is not a fresh local UI run.

**Evidence:** [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json)

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`students.tests.StudentManagementViewTests.test_empty_student_submissions_show_required_errors_without_saving`](../../students/tests.py#L148); [`hostels.tests.HostelManagementViewTests.test_empty_management_submissions_show_required_errors_without_saving`](../../hostels/tests.py#L81)

**Current companion outcomes:** 2 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Methods assert field errors, row counts, absence of relevant audit; not every stored field is explicitly reasserted.

### TC-REG-S1-07: Numeric bed-filter boundaries and escaped errors

<a id="case-tc-reg-s1-07"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-13, NFR-10

**Level:** View / database integration

**Type:** Regression / boundaries / input safety

**Prerequisites and data:** Observed authenticated Student fixture (hostels/tests.py setup), synthetic rooms/beds; separate floors 0/65535 are created by the boundary method. Methods execute independently in the Django test database. The previous Staff label was not the actual fixture and is corrected; no staff/browser execution is claimed.

**Steps:**

1. Try bad/fractional/negative/out-of-range hostel/floor values and5000-digit inputs.
2. Submit script-shaped floor alongside valid other selectors.
3. Try floor0/65535 and maximum signed64-bit unmatched hostel.
4. Repeat bad-filter request logged out.

**Expected:** Bad filters return400, field errors and no beds; submitted script escaped and other selections retained. Valid floor bounds match only own beds; unmatched valid hostel returns200 empty; authentication remains required.

**Actual:** All four automated recipe steps are represented by five passing historical methods in both Python jobs: invalid filters/empty results/errors, escaped payload/preserved selectors, valid numeric bounds/unmatched hostel and logged-out redirect. The actual authenticated fixture is Student. Accepted for this declared integration scope by the 8 November technical reconciliation; no new browser run.

**Execution status:** OWNER PASS

**Tested commit:** 32e6f563335a1ed20e2c6f619ba7e82de56dbd1f (historical PR #58 merge checkout); reviewed application/test/template/configuration scope is source-equivalent to initial PR #66.

**Execution date and environment:** 7 November 2026 around 11:07–11:08 UTC; Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13, synthetic Django test DB. Reviewed 8 November; no new local/browser execution.

**Evidence:** [8 November follow-up review](evidence/issue39/followup-20261108.md); [original bundle metadata and hashes](evidence/issue39/followup-20261108.json); [Python 3.11 raw JUnit](evidence/hms-test-evidence-py3.11/junit); [Python 3.14 raw JUnit](evidence/hms-test-evidence-py3.14/junit).

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Accepted for the stated historical automated recipe scope in Devansh's authorized AI-assisted technical reconciliation with independent reviewers. Priorities remain proposals; this is not historical entry approval, a named human signature or whole-plan acceptance.

**Automation:** [`hostels.tests.BedFilteringViewTests.test_invalid_numeric_filters_return_400_without_bed_results`](../../hostels/tests.py#L503); [`hostels.tests.BedFilteringViewTests.test_invalid_floor_is_escaped_and_other_filter_values_are_preserved`](../../hostels/tests.py#L527); [`hostels.tests.BedFilteringViewTests.test_zero_and_upper_boundary_floor_filters_match_only_their_beds`](../../hostels/tests.py#L549); [`hostels.tests.BedFilteringViewTests.test_maximum_hostel_id_is_valid_and_has_no_matches`](../../hostels/tests.py#L572); [`hostels.tests.BedFilteringViewTests.test_invalid_filters_do_not_bypass_login`](../../hostels/tests.py#L579)

**Current companion outcomes:** Five PASS, zero failures/errors/skips in each retained 32e6f563 bundle. These historical method outcomes support the reviewed automated recipe; no new execution or unit-only claim.

**Evidence limits:** Historical automated integration scope uses authenticated Student, not Staff, followed by a logged-out request. It proves the listed filter/HTML assertions, not browser execution, all staff-role behavior or complete original TC-HST-02 acceptance.

### TC-REG-S1-08: Student/room changes roll back on audit failure

<a id="case-tc-reg-s1-08"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; High (proposed). Risk: partial audited writes can leave the database inconsistent.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-5, REQ-9, REQ-11, NFR-11

**Level:** Fault-injected view / database integration

**Type:** Regression / atomicity

**Prerequisites and data:** Synthetic student/hostel; controlled record_event fault in tests. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Fail audit during student create.
2. Fail audit during room create.
3. Fail audit during permitted student deactivation.

**Expected:** No failed student/room/automatic-bed create survives; deactivation failure leaves student Active; no corresponding audit survives.

**Actual:** The linked component/integration methods passed in both 7 November CI jobs. This newly specified case has no separate reviewed case-execution record; NOT RUN preserves that boundary.

**Execution status:** NOT RUN

**Tested commit:** 70c9fe20e462eb0b052e15434f19b347a793afa1 (automated companions); no independent execution SHA for the new planned case

**Execution date and environment:** 7 November 2026 CI: Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13; exact versions/commands and method outcomes retained below. This is not a fresh local UI run.

**Evidence:** [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json)

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`students.tests.StudentManagementViewTests.test_student_creation_rolls_back_if_audit_recording_fails`](../../students/tests.py#L165); [`students.tests.StudentManagementViewTests.test_student_deactivation_rolls_back_if_audit_recording_fails`](../../students/tests.py#L307); [`hostels.tests.HostelManagementViewTests.test_room_creation_rolls_back_if_audit_recording_fails`](../../hostels/tests.py#L109)

**Current companion outcomes:** 3 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Controlled automated faults only; not deployed-database disruption.

### TC-REG-S2-06: Explicit Student login link scopes My Records

<a id="case-tc-reg-s2-06"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Sreeharsha / Vaishnavi

**Priority:** Unspecified in original plan; High (proposed). Risk: the linked privacy, transaction, financial or validation invariant must hold on every request.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-5, REQ-8, REQ-24, NFR-8

**Level:** Form / view / database integration plus UI link-save check

**Type:** Regression / authorization

**Prerequisites and data:** Two linked Student logins/profiles with allocations/payments; unlinked Student and staff accounts. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Inspect create picker: unlinked Student accounts only.
2. Inspect edit picker: current link retained; other linked accounts and staff excluded.
3. Save a permitted link as staff in UI and sign in with it.
4. Open My Records and check own records; ensure other student details absent.

**Expected:** Eligible optional link can save; picker restricts accounts; My Records resolves authenticated login's profile and exposes only its allocation/payment/status.

**Actual:** The linked component/integration methods passed in both 7 November CI jobs. This newly specified case has no separate reviewed case-execution record; NOT RUN preserves that boundary.

**Execution status:** NOT RUN

**Tested commit:** 70c9fe20e462eb0b052e15434f19b347a793afa1 (automated companions); no independent execution SHA for the new planned case

**Execution date and environment:** 7 November 2026 CI: Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13; exact versions/commands and method outcomes retained below. This is not a fresh local UI run.

**Evidence:** [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json)

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** [`students.test_self_service.StudentSelfServiceTests.test_student_account_picker_excludes_staff_and_accounts_linked_elsewhere`](../../students/test_self_service.py#L130); [`students.test_self_service.StudentSelfServiceTests.test_student_sees_only_own_allocation_and_payment_details`](../../students/test_self_service.py#L58)

**Current companion outcomes:** 2 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Methods inspect querysets and use fixture-created links. No link-assignment POST, forged-link POST or relink is asserted; UI save evidence needed for whole proposed case.

### TC-REG-S2-07: My Records empty/access/navigation/date behavior

<a id="case-tc-reg-s2-07"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** REQ-24, NFR-7, NFR-8

**Level:** View / HTML integration

**Type:** Regression / usability / authorization

**Prerequisites and data:** Unlinked login; linked Student with no history; linked Student with current/historical stay and payment dated5/6April2026; staff/anonymous sessions. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Open unlinked and linked-empty portal.
2. Use Student dashboard/navigation to reach My Records.
3. Inspect populated allocation/payment/vacate dates.
4. Attempt portal as Admin/Warden/anonymous.

**Expected:** Unlinked message directs to staff and exposes no other profile; empty state explains no active allocation/history/payments and Pending. Dashboard links portal; dates DD-MM-YYYY and active vacate date em dash. Admin/Warden403; anonymous browser login redirect.

**Actual:** Six historical methods PASS in both Python jobs: linked-empty/unlinked messages, dashboard portal link, populated DD-MM-YYYY dates/em-dash fallback, Admin/Warden denial and anonymous redirect. Accepted for the declared View/HTML integration scope by the 8 November technical reconciliation; no new browser run.

**Execution status:** OWNER PASS

**Tested commit:** 32e6f563335a1ed20e2c6f619ba7e82de56dbd1f (historical PR #58 merge checkout); reviewed application/test/template/configuration scope is source-equivalent to initial PR #66.

**Execution date and environment:** 7 November 2026 around 11:07–11:08 UTC; Linux, Python 3.11.18 / 3.14.10, Django 5.2.19, MySQL 8.4.13, synthetic Django test DB. Reviewed 8 November; no new local/browser execution.

**Evidence:** [8 November follow-up review](evidence/issue39/followup-20261108.md); [original bundle metadata and hashes](evidence/issue39/followup-20261108.json); [Python 3.11 raw JUnit](evidence/hms-test-evidence-py3.11/junit); [Python 3.14 raw JUnit](evidence/hms-test-evidence-py3.14/junit).

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Accepted for the stated historical automated recipe scope in Devansh's authorized AI-assisted technical reconciliation with independent reviewers. Priorities remain proposals; this is not historical entry approval, a named human signature or whole-plan acceptance.

**Automation:** [`students.test_self_service.StudentSelfServiceTests.test_empty_allocation_and_payment_history_is_explained`](../../students/test_self_service.py#L84); [`students.test_self_service.StudentSelfServiceTests.test_unlinked_student_login_gets_helpful_empty_state`](../../students/test_self_service.py#L93); [`students.test_self_service.StudentSelfServiceTests.test_dashboard_and_navigation_link_to_my_records`](../../students/test_self_service.py#L126); [`students.test_self_service.StudentSelfServiceTests.test_student_dates_are_dd_mm_yyyy_and_keep_vacated_fallback`](../../students/test_self_service.py#L150); [`students.test_self_service.StudentSelfServiceTests.test_only_student_role_can_open_self_service_page`](../../students/test_self_service.py#L106); [`students.test_self_service.StudentSelfServiceTests.test_login_is_required_for_self_service_page`](../../students/test_self_service.py#L118)

**Current companion outcomes:** Six PASS, zero failures/errors/skips in each retained 32e6f563 bundle. These historical method outcomes support the reviewed automated recipe; no new execution or unit-only claim.

**Evidence limits:** Navigation evidence is rendered dashboard-link presence, not a browser click. Date assertions are response-wide rather than individually targeted to every cell; static template review corroborates date formatting/fallback. This bounded integration result does not establish complete original REQ-24 or whole-plan acceptance.

### TC-REG-S2-08: Allocation/release/transfer rollback and retry

<a id="case-tc-reg-s2-08"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #63 technical review 8 November). Risk: the linked privacy, transaction, financial or validation invariant must hold on every request.

**Priority review:** Current priority accepted for this scoped automated technical review on 8 November; see [pre-execution review](evidence/issue63/pre-execution-review.md). Historical entry and whole-team exit acceptance remain separate.

**Requirements:** REQ-14, REQ-17, REQ-18, REQ-19, NFR-11

**Level:** Fault-injected service / database integration

**Type:** Regression / atomicity

**Prerequisites and data:** Eligible student, source/target beds, staff; controlled audit/storage faults. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Fail allocate audit.
2. Create allocation then fail release audit.
3. Fail saving target Occupied during transfer; inspect both beds/history/dates/audits.
4. Remove fault and retry same transfer.

**Expected:** Failed allocate leaves no allocation and Available bed; failed release leaves Active/Occupied; failed transfer leaves original fields/history unchanged, source Occupied, target Available and no transfer audit. Retry produces one successor, completes original and records one actor transfer event.

**Actual:** Audit failures rolled back allocation and release; failed target-bed storage preserved both beds, original history/dates and audits; the same transfer retry created exactly one successor and actor event. 4 recorded observations completed; exact expected/actual values are in [the case record](evidence/issue63/execution/TC-REG-S2-08.json).

**Execution status:** OWNER PASS

**Tested commit:** 6636098cb728aa17c2abf5e42c358a5d400261e7 (clean execution; tree 0faea77304a30ceb436e1411a2c513dd1f3c6f44). Historical companion commit: 70c9fe20e462eb0b052e15434f19b347a793afa1.

**Execution date and environment:** 8 November 2026, Windows-11-10.0.26200-SP0, Python 3.14.7, Django 5.2.18, MySQL 8.4.9; synthetic disposable test_hms, Django HTTP test client/service/ORM. [Exact command/settings/versions](evidence/issue63/execution/run.json). Earlier 7 November Linux companion observations retain their separate provenance below.

**Evidence:** [Case observations](evidence/issue63/execution/TC-REG-S2-08.json); [execution/JUnit/hash index](evidence/issue63/README.md); historical [companion extraction](evidence/issue37/ci-methods.json).

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Three independent automated reviewers checked the recipe, assertions and candidate evidence before the clean committed run; current scoped technical review found no remaining blocker. Final actual human approval and whole-plan entry/exit acceptance are not supplied.

**Automation:** [`scripts.part3.test_owned_transactions.OwnedAllocationTransactions.test_tc_reg_s2_08_rollback_and_retry`](../../scripts/part3/test_owned_transactions.py#L82); retained historical companions: [`allocations.test_workflows.AllocationWorkflowTests.test_audit_failure_rolls_back_allocation_and_release`](../../allocations/test_workflows.py#L390); [`allocations.test_workflows.AllocationWorkflowTests.test_transfer_failure_rolls_back_both_beds_and_history`](../../allocations/test_workflows.py#L234)

**Historical companion outcomes (7 November):** 2 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Current execution is synthetic integration evidence with explicit late-entry, MySQL8.4 and HTTP test-flag limits; no new browser/TLS or unit-only claim. Whole-team acceptance remains pending. Historical companion limitation (not the new execution): This is automated companion evidence for original TC-ALC05 forced-failure/retry; preserve raw browser PARTIAL and combined-scope qualification.

### TC-REG-S2-09: Payments and original receipts are permanent

<a id="case-tc-reg-s2-09"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #63 technical review 8 November). Risk: the linked privacy, transaction, financial or validation invariant must hold on every request.

**Priority review:** Current priority accepted for this scoped automated technical review on 8 November; see [pre-execution review](evidence/issue63/pre-execution-review.md). Historical entry and whole-team exit acceptance remain separate.

**Requirements:** REQ-20, REQ-21, NFR-5, NFR-11

**Level:** Model / ORM / database integration

**Type:** Regression / financial integrity

**Prerequisites and data:** Staff and recorded synthetic payment. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Record two payments; inspect receipt sequence/audit.
2. Try save/edit/delete, queryset update/delete, bulk update/create, primary-key replay and receipt reuse.
3. Reload original.

**Expected:** Payments retain original amount/identity; guarded mutations reject; genuine payments have sequential unique receipts and actor audit; correction uses new adjusting entry.

**Actual:** Two original sequential receipts and actor audits were preserved through ten prohibited ORM mutations; a real adjusting entry created the next receipt and left original records unchanged. 13 recorded observations completed; exact expected/actual values are in [the case record](evidence/issue63/execution/TC-REG-S2-09.json).

**Execution status:** OWNER PASS

**Tested commit:** 6636098cb728aa17c2abf5e42c358a5d400261e7 (clean execution; tree 0faea77304a30ceb436e1411a2c513dd1f3c6f44). Historical companion commit: 70c9fe20e462eb0b052e15434f19b347a793afa1.

**Execution date and environment:** 8 November 2026, Windows-11-10.0.26200-SP0, Python 3.14.7, Django 5.2.18, MySQL 8.4.9; synthetic disposable test_hms, Django HTTP test client/service/ORM. [Exact command/settings/versions](evidence/issue63/execution/run.json). Earlier 7 November Linux companion observations retain their separate provenance below.

**Evidence:** [Case observations](evidence/issue63/execution/TC-REG-S2-09.json); [execution/JUnit/hash index](evidence/issue63/README.md); historical [companion extraction](evidence/issue37/ci-methods.json).

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Three independent automated reviewers checked the recipe, assertions and candidate evidence before the clean committed run; current scoped technical review found no remaining blocker. Final actual human approval and whole-plan entry/exit acceptance are not supplied.

**Automation:** [`scripts.part3.test_owned_transactions.OwnedPaymentTransactions.test_tc_reg_s2_09_payment_permanence`](../../scripts/part3/test_owned_transactions.py#L294); retained historical companions: [`payments.test_workflows.PaymentWorkflowTests.test_numbered_payments_are_permanent_and_audited_for_the_actor`](../../payments/test_workflows.py#L79); [`payments.test_workflows.PaymentWorkflowTests.test_edit_delete_bulk_and_primary_key_replay_are_blocked`](../../payments/test_workflows.py#L116)

**Historical companion outcomes (7 November):** 2 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Current execution is synthetic integration evidence with explicit late-entry, MySQL8.4 and HTTP test-flag limits; no new browser/TLS or unit-only claim. Whole-team acceptance remains pending. Historical companion limitation (not the new execution): Application ORM protection is verified; not a claim of privileged raw SQL immutability.

### TC-REG-S2-10: Rejected/failed payments preserve receipt counter

<a id="case-tc-reg-s2-10"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #63 technical review 8 November). Risk: the linked privacy, transaction, financial or validation invariant must hold on every request.

**Priority review:** Current priority accepted for this scoped automated technical review on 8 November; see [pre-execution review](evidence/issue63/pre-execution-review.md). Historical entry and whole-team exit acceptance remain separate.

**Requirements:** REQ-20, REQ-21, NFR-10, NFR-11

**Level:** Service / model / database integration

**Type:** Regression / input boundaries / atomicity

**Prerequisites and data:** Known receipt counter; synthetic student; controlled audit fault. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Try ordinary payment0/negative, nonfinite/nonnumeric/overprecision/oversize amounts, unsupported mode, future/invalid date, invalid/overlength reference.
2. Fail audit during valid record_payment.
3. Remove fault and retry valid payment.
4. Exhaust sequence in isolated test and attempt another payment.

**Expected:** Invalid/faulted attempts create no payment and consume no receipt; fresh retry gets R00000000001; exhausted range rejects without overwriting history.

**Actual:** Thirteen invalid inputs, controlled audit failure and sequence exhaustion preserved payment/counter/audit state; retry used the next receipt; exhausted history remained intact. 16 recorded observations completed; exact expected/actual values are in [the case record](evidence/issue63/execution/TC-REG-S2-10.json).

**Execution status:** OWNER PASS

**Tested commit:** 6636098cb728aa17c2abf5e42c358a5d400261e7 (clean execution; tree 0faea77304a30ceb436e1411a2c513dd1f3c6f44). Historical companion commit: 70c9fe20e462eb0b052e15434f19b347a793afa1.

**Execution date and environment:** 8 November 2026, Windows-11-10.0.26200-SP0, Python 3.14.7, Django 5.2.18, MySQL 8.4.9; synthetic disposable test_hms, Django HTTP test client/service/ORM. [Exact command/settings/versions](evidence/issue63/execution/run.json). Earlier 7 November Linux companion observations retain their separate provenance below.

**Evidence:** [Case observations](evidence/issue63/execution/TC-REG-S2-10.json); [execution/JUnit/hash index](evidence/issue63/README.md); historical [companion extraction](evidence/issue37/ci-methods.json).

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Three independent automated reviewers checked the recipe, assertions and candidate evidence before the clean committed run; current scoped technical review found no remaining blocker. Final actual human approval and whole-plan entry/exit acceptance are not supplied.

**Automation:** [`scripts.part3.test_owned_transactions.OwnedPaymentTransactions.test_tc_reg_s2_10_rejected_failed_and_exhausted_receipts`](../../scripts/part3/test_owned_transactions.py#L412); retained historical companions: [`payments.test_workflows.PaymentWorkflowTests.test_invalid_amounts_modes_dates_and_references_do_not_consume_numbers`](../../payments/test_workflows.py#L91); [`payments.test_workflows.PaymentWorkflowTests.test_audit_failure_rolls_back_the_payment_and_receipt_counter`](../../payments/test_workflows.py#L205); [`payments.test_workflows.PaymentWorkflowTests.test_receipt_range_exhaustion_fails_without_overwriting_history`](../../payments/test_workflows.py#L283)

**Historical companion outcomes (7 November):** 3 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Current execution is synthetic integration evidence with explicit late-entry, MySQL8.4 and HTTP test-flag limits; no new browser/TLS or unit-only claim. Whole-team acceptance remains pending. Historical companion limitation (not the new execution): Shared source, owner-observation and pending acceptance limits above still apply; no additional case-specific limit is recorded.

### TC-REG-S2-11: Competing corrections cannot over-reverse

<a id="case-tc-reg-s2-11"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #63 technical review 8 November). Risk: the linked privacy, transaction, financial or validation invariant must hold on every request.

**Priority review:** Current priority accepted for this scoped automated technical review on 8 November; see [pre-execution review](evidence/issue63/pre-execution-review.md). Historical entry and whole-team exit acceptance remain separate.

**Requirements:** REQ-20, REQ-21, REQ-22

**Level:** MySQL concurrency integration

**Type:** Regression / concurrency / financial integrity

**Prerequisites and data:** Original INR100; staff; separate connections. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Race two -80 adjustments against original.
2. Inspect payment count/receipts/net.

**Expected:** One correction succeeds with R00000000002; other rejects; two rows/counter2 and net20 remain.

**Actual:** Distinct connections executed overlapping real service calls at the Student locking query. One correction succeeded, one over-reversal was rejected; receipt counter 2, net INR20 and exactly two actor audits remained. 2 recorded observations completed; exact expected/actual values are in [the case record](evidence/issue63/execution/TC-REG-S2-11.json).

**Execution status:** OWNER PASS

**Tested commit:** 6636098cb728aa17c2abf5e42c358a5d400261e7 (clean execution; tree 0faea77304a30ceb436e1411a2c513dd1f3c6f44). Historical companion commit: 70c9fe20e462eb0b052e15434f19b347a793afa1.

**Execution date and environment:** 8 November 2026, Windows-11-10.0.26200-SP0, Python 3.14.7, Django 5.2.18, MySQL 8.4.9; synthetic disposable test_hms, Django HTTP test client/service/ORM. [Exact command/settings/versions](evidence/issue63/execution/run.json). Earlier 7 November Linux companion observations retain their separate provenance below.

**Evidence:** [Case observations](evidence/issue63/execution/TC-REG-S2-11.json); [execution/JUnit/hash index](evidence/issue63/README.md); historical [companion extraction](evidence/issue37/ci-methods.json).

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Three independent automated reviewers checked the recipe, assertions and candidate evidence before the clean committed run; current scoped technical review found no remaining blocker. Final actual human approval and whole-plan entry/exit acceptance are not supplied.

**Automation:** [`scripts.part3.test_owned_transactions.OwnedPaymentCorrectionConcurrency.test_tc_reg_s2_11_competing_corrections`](../../scripts/part3/test_owned_transactions.py#L530); retained historical companions: [`payments.test_workflows.PaymentConcurrencyTests.test_competing_corrections_cannot_reverse_a_payment_twice`](../../payments/test_workflows.py#L562)

**Historical companion outcomes (7 November):** 1 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Current execution is synthetic integration evidence with explicit late-entry, MySQL8.4 and HTTP test-flag limits; no new browser/TLS or unit-only claim. Whole-team acceptance remains pending. Historical companion limitation (not the new execution): Shared source, owner-observation and pending acceptance limits above still apply; no additional case-specific limit is recorded.

### TC-REG-S2-12: Payment reports use correct totals, Bed and latest valid location

<a id="case-tc-reg-s2-12"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Devansh

**Priority:** Unspecified in original plan; Medium (proposed 7 November; adopted for scoped #63 technical review 8 November). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Current priority accepted for this scoped automated technical review on 8 November; see [pre-execution review](evidence/issue63/pre-execution-review.md). Historical entry and whole-team exit acceptance remain separate.

**Requirements:** REQ-19, REQ-22, REQ-23

**Level:** Service / API / HTML integration

**Type:** Regression / reporting

**Prerequisites and data:** Transfers/releases, multiple payments/correction, unassigned/cancelled-only students. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Compare after transfer/release; filter old/new hostel.
2. Compare corrected balance HTML/CSV/JSON.
3. Inspect unassigned/cancelled-only records and zero/unconfigured room fee.

**Expected:** Payments counted once despite history; current otherwise latest noncancelled allocation provides location/fee. Cancelled location excluded. Unassigned location blank in JSON/CSV and Unassigned in HTML; Bed present in all formats.1000 less250 gives paid750/due250/Partial. Unconfigured fee remains Pending even with advance.

**Actual:** JSON/CSV/HTML reconciled payment totals, required Bed and current/latest valid location after transfer/release/correction; never-assigned and cancelled-only states were tested separately; zero-fee advance remained Pending. 3 recorded observations completed; exact expected/actual values are in [the case record](evidence/issue63/execution/TC-REG-S2-12.json).

**Execution status:** OWNER PASS

**Tested commit:** 6636098cb728aa17c2abf5e42c358a5d400261e7 (clean execution; tree 0faea77304a30ceb436e1411a2c513dd1f3c6f44). Historical companion commit: 70c9fe20e462eb0b052e15434f19b347a793afa1.

**Execution date and environment:** 8 November 2026, Windows-11-10.0.26200-SP0, Python 3.14.7, Django 5.2.18, MySQL 8.4.9; synthetic disposable test_hms, Django HTTP test client/service/ORM. [Exact command/settings/versions](evidence/issue63/execution/run.json). Earlier 7 November Linux companion observations retain their separate provenance below.

**Evidence:** [Case observations](evidence/issue63/execution/TC-REG-S2-12.json); [execution/JUnit/hash index](evidence/issue63/README.md); historical [companion extraction](evidence/issue37/ci-methods.json).

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Three independent automated reviewers checked the recipe, assertions and candidate evidence before the clean committed run; current scoped technical review found no remaining blocker. Final actual human approval and whole-plan entry/exit acceptance are not supplied.

**Automation:** [`scripts.part3.test_owned_reports_inputs.OwnedReportInputCases.test_tc_reg_s2_12_report_history_balances_and_locations`](../../scripts/part3/test_owned_reports_inputs.py#L238); retained historical companions: [`reports.test_reports.ReportTests.test_payment_report_sums_once_across_allocation_history_and_filters_last_room`](../../reports/test_reports.py#L117); [`reports.test_reports.ReportTests.test_payment_report_excludes_cancelled_locations_and_keeps_unassigned_blank`](../../reports/test_reports.py#L176); [`reports.test_reports.ReportTests.test_payment_report_csv_and_html_match_json_after_corrections`](../../reports/test_reports.py#L218); [`payments.test_workflows.PaymentWorkflowTests.test_status_tracks_pending_partial_paid_and_adjustments_without_join_multiplication`](../../payments/test_workflows.py#L218); [`payments.test_workflows.PaymentWorkflowTests.test_no_allocation_or_unconfigured_fee_remains_pending_with_advance_payment`](../../payments/test_workflows.py#L253)

**Historical companion outcomes (7 November):** 5 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Current execution is synthetic integration evidence with explicit late-entry, MySQL8.4 and HTTP test-flag limits; no new browser/TLS or unit-only claim. Whole-team acceptance remains pending. Historical companion limitation (not the new execution): Shared source, owner-observation and pending acceptance limits above still apply; no additional case-specific limit is recorded.

### TC-REG-S2-13: CSV text stays literal and report HTML escapes labels

<a id="case-tc-reg-s2-13"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Devansh

**Priority:** Unspecified in original plan; Medium (proposed 7 November; adopted for scoped #63 technical review 8 November). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Current priority accepted for this scoped automated technical review on 8 November; see [pre-execution review](evidence/issue63/pre-execution-review.md). Historical entry and whole-team exit acceptance remain separate.

**Requirements:** REQ-23, NFR-10

**Level:** API / HTML integration

**Type:** Regression / output safety

**Prerequisites and data:** Labels with quotes/comma/newline/Unicode/formula-prefix/HTML text. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Export occupancy/payment CSV and parse values.
2. Compare Unicode/quoted/newline/formula-shaped labels.
3. View payment HTML.

**Expected:** CSV valid quoting preserves labels; apostrophe makes formula-shaped text literal; HTML user markup escaped.

**Actual:** Nine CSV/HTML vectors preserved Unicode, quotes and newlines, neutralized each dangerous prefix and displayed escaped literal labels without an injected element. 9 recorded observations completed; exact expected/actual values are in [the case record](evidence/issue63/execution/TC-REG-S2-13.json).

**Execution status:** OWNER PASS

**Tested commit:** 6636098cb728aa17c2abf5e42c358a5d400261e7 (clean execution; tree 0faea77304a30ceb436e1411a2c513dd1f3c6f44). Historical companion commit: 70c9fe20e462eb0b052e15434f19b347a793afa1.

**Execution date and environment:** 8 November 2026, Windows-11-10.0.26200-SP0, Python 3.14.7, Django 5.2.18, MySQL 8.4.9; synthetic disposable test_hms, Django HTTP test client/service/ORM. [Exact command/settings/versions](evidence/issue63/execution/run.json). Earlier 7 November Linux companion observations retain their separate provenance below.

**Evidence:** [Case observations](evidence/issue63/execution/TC-REG-S2-13.json); [execution/JUnit/hash index](evidence/issue63/README.md); historical [companion extraction](evidence/issue37/ci-methods.json).

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Three independent automated reviewers checked the recipe, assertions and candidate evidence before the clean committed run; current scoped technical review found no remaining blocker. Final actual human approval and whole-plan entry/exit acceptance are not supplied.

**Automation:** [`scripts.part3.test_owned_reports_inputs.OwnedReportInputCases.test_tc_reg_s2_13_csv_literals_unicode_and_html`](../../scripts/part3/test_owned_reports_inputs.py#L357); retained historical companions: [`reports.test_reports.ReportTests.test_csv_quotes_unicode_and_formula_text_and_html_escapes_names`](../../reports/test_reports.py#L242)

**Historical companion outcomes (7 November):** 1 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Current execution is synthetic integration evidence with explicit late-entry, MySQL8.4 and HTTP test-flag limits; no new browser/TLS or unit-only claim. Whole-team acceptance remains pending. Historical companion limitation (not the new execution): Method tests whitespace+= and @ formulas plus quote/comma/newline/Unicode/HTML; source's +,-,leading tab/CR/LF branches are not each exercised.

### TC-REG-S2-14: Report empty/filter/format/method boundaries

<a id="case-tc-reg-s2-14"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Devansh

**Priority:** Unspecified in original plan; Medium (proposed 7 November; adopted for scoped #63 technical review 8 November). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Current priority accepted for this scoped automated technical review on 8 November; see [pre-execution review](evidence/issue63/pre-execution-review.md). Historical entry and whole-team exit acceptance remain separate.

**Requirements:** REQ-23, NFR-10

**Level:** API / HTML integration

**Type:** Regression / negative input

**Prerequisites and data:** Empty and populated hostels; staff. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Request empty payment report and zero-bed occupancy CSV.
2. Try malformed/zero/negative/fractional/non-ASCII/extreme hostel IDs.
3. Try missing well-formed hostel, unsupported format and POST.
4. Request known hostel with thousands of leading zeros.

**Expected:** Empty payment rows; zero-bed occupancy0.00%; invalid value400; absent well-formed ID404; unsupported format400; POST405. Leading zeros resolve to correct known hostel.

**Actual:** Both report routes passed empty, invalid/missing-hostel, populated leading-zero, unsupported-format and method-boundary checks; populated filter results matched the exact expected hostel/student/Bed. 7 recorded observations completed; exact expected/actual values are in [the case record](evidence/issue63/execution/TC-REG-S2-14.json).

**Execution status:** OWNER PASS

**Tested commit:** 6636098cb728aa17c2abf5e42c358a5d400261e7 (clean execution; tree 0faea77304a30ceb436e1411a2c513dd1f3c6f44). Historical companion commit: 70c9fe20e462eb0b052e15434f19b347a793afa1.

**Execution date and environment:** 8 November 2026, Windows-11-10.0.26200-SP0, Python 3.14.7, Django 5.2.18, MySQL 8.4.9; synthetic disposable test_hms, Django HTTP test client/service/ORM. [Exact command/settings/versions](evidence/issue63/execution/run.json). Earlier 7 November Linux companion observations retain their separate provenance below.

**Evidence:** [Case observations](evidence/issue63/execution/TC-REG-S2-14.json); [execution/JUnit/hash index](evidence/issue63/README.md); historical [companion extraction](evidence/issue37/ci-methods.json).

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Three independent automated reviewers checked the recipe, assertions and candidate evidence before the clean committed run; current scoped technical review found no remaining blocker. Final actual human approval and whole-plan entry/exit acceptance are not supplied.

**Automation:** [`scripts.part3.test_owned_reports_inputs.OwnedReportInputCases.test_tc_reg_s2_14_report_boundaries`](../../scripts/part3/test_owned_reports_inputs.py#L404); retained historical companions: [`reports.test_reports.ReportTests.test_empty_reports_and_invalid_filters_formats_and_methods`](../../reports/test_reports.py#L259); [`reports.test_reports.ReportTests.test_numeric_hostel_filter_accepts_leading_zeros`](../../reports/test_reports.py#L297)

**Historical companion outcomes (7 November):** 2 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Current execution is synthetic integration evidence with explicit late-entry, MySQL8.4 and HTTP test-flag limits; no new browser/TLS or unit-only claim. Whole-team acceptance remains pending. Historical companion limitation (not the new execution): Reports return complete filtered result set. Report pagination is neither implemented nor asserted.

### TC-REG-S2-15: Malformed JSON is a safe validation error

<a id="case-tc-reg-s2-15"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #63 technical review 8 November). Risk: the linked privacy, transaction, financial or validation invariant must hold on every request.

**Priority review:** Current priority accepted for this scoped automated technical review on 8 November; see [pre-execution review](evidence/issue63/pre-execution-review.md). Historical entry and whole-team exit acceptance remain separate.

**Requirements:** REQ-14, REQ-17, REQ-18, REQ-20, NFR-10

**Level:** Parser unit checks plus API integration

**Type:** Regression / negative input

**Prerequisites and data:** Direct parser fixtures; staff for endpoint companions. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Try malformed JSON/UTF8; scalar/array/null body; container-valued fields; lone surrogate; nonfinite/exponent-overflow number; excessive nesting.
2. Use valid finite scalar object and paired Unicode as controls.
3. Exercise representative malformed payment/allocation bodies.

**Expected:** Bad parser shapes raise generic ValidationError; API companion returns400 instead of unhandled error. Valid finite scalars/Unicode preserved; form data returned unchanged.

**Actual:** Documented malformed JSON categories were rejected with generic errors through parser and representative real endpoints; every rejected request preserved business-state hashes; valid scalar/Unicode/form controls passed. 64 recorded observations completed; exact expected/actual values are in [the case record](evidence/issue63/execution/TC-REG-S2-15.json).

**Execution status:** OWNER PASS

**Tested commit:** 6636098cb728aa17c2abf5e42c358a5d400261e7 (clean execution; tree 0faea77304a30ceb436e1411a2c513dd1f3c6f44). Historical companion commit: 70c9fe20e462eb0b052e15434f19b347a793afa1.

**Execution date and environment:** 8 November 2026, Windows-11-10.0.26200-SP0, Python 3.14.7, Django 5.2.18, MySQL 8.4.9; synthetic disposable test_hms, Django HTTP test client/service/ORM. [Exact command/settings/versions](evidence/issue63/execution/run.json). Earlier 7 November Linux companion observations retain their separate provenance below.

**Evidence:** [Case observations](evidence/issue63/execution/TC-REG-S2-15.json); [execution/JUnit/hash index](evidence/issue63/README.md); historical [companion extraction](evidence/issue37/ci-methods.json).

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Three independent automated reviewers checked the recipe, assertions and candidate evidence before the clean committed run; current scoped technical review found no remaining blocker. Final actual human approval and whole-plan entry/exit acceptance are not supplied.

**Automation:** [`scripts.part3.test_owned_reports_inputs.OwnedReportInputCases.test_tc_reg_s2_15_malformed_json_and_controls`](../../scripts/part3/test_owned_reports_inputs.py#L508); retained historical companions: [`hms.test_http.RequestDataTests.test_malformed_json_and_invalid_utf8_raise_validation_error`](../../hms/test_http.py#L45); [`hms.test_http.RequestDataTests.test_non_object_json_raises_validation_error`](../../hms/test_http.py#L53); [`hms.test_http.RequestDataTests.test_container_field_values_raise_validation_error`](../../hms/test_http.py#L61); [`hms.test_http.RequestDataTests.test_unpaired_unicode_surrogates_raise_validation_error`](../../hms/test_http.py#L78); [`hms.test_http.RequestDataTests.test_nonfinite_numbers_are_rejected_including_exponent_overflow`](../../hms/test_http.py#L92); [`hms.test_http.RequestDataTests.test_parser_recursion_error_becomes_validation_error`](../../hms/test_http.py#L103); [`hms.test_http.RequestDataTests.test_deeply_nested_input_raises_validation_error`](../../hms/test_http.py#L111); [`hms.test_http.RequestDataTests.test_json_object_preserves_finite_scalar_values`](../../hms/test_http.py#L16); [`hms.test_http.RequestDataTests.test_valid_unicode_strings_and_surrogate_pairs_are_preserved`](../../hms/test_http.py#L69); [`hms.test_http.RequestDataTests.test_form_encoded_data_is_returned_unchanged`](../../hms/test_http.py#L34); [`allocations.test_workflows.AllocationWorkflowTests.test_json_workflow_conflicts_validation_and_permissions`](../../allocations/test_workflows.py#L415); [`payments.test_workflows.PaymentWorkflowTests.test_invalid_json_fields_missing_records_and_methods`](../../payments/test_workflows.py#L377)

**Historical companion outcomes (7 November):** 12 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Current execution is synthetic integration evidence with explicit late-entry, MySQL8.4 and HTTP test-flag limits; no new browser/TLS or unit-only claim. Whole-team acceptance remains pending. Historical companion limitation (not the new execution): Parser methods are SimpleTestCase; endpoint methods cover representative shapes, not every parser vector at every route. Does not replace original UI SQL/XSS/CSRF execution.

### TC-REG-S2-16: Typed JSON dates/references keep correct errors and state

<a id="case-tc-reg-s2-16"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Devansh

**Priority:** Unspecified in original plan; High (proposed 7 November; adopted for scoped #63 technical review 8 November). Risk: the linked privacy, transaction, financial or validation invariant must hold on every request.

**Priority review:** Current priority accepted for this scoped automated technical review on 8 November; see [pre-execution review](evidence/issue63/pre-execution-review.md). Historical entry and whole-team exit acceptance remain separate.

**Requirements:** REQ-14, REQ-17, REQ-18, REQ-20, REQ-21, NFR-10

**Level:** Form unit checks plus API/database integration

**Type:** Regression / type validation / error contract

**Prerequisites and data:** Staff; student/beds/allocation/payment and state/counter/audit snapshot. Use the exact synthetic setup/values in the linked method sources; isolate each method in the Django-created test database. Shared design fixtures below are examples for future UI execution, not replacements for archived run fixtures.

**Steps:**

1. Try number/bool/container dates for allocate/release/payment/adjustment.
2. Try fractional/integral float and bool bed/new-bed references.
3. Try omitted required bed/new_bed/form references, supplied nonexistent references, missing JSON create student_id, a missing required date and a non-reference invalid choice.
4. Compare state/counter/audit after rejection.

**Expected:** Integer/bool dates return 400 with field code invalid and unchanged state/receipt counter/audit. Containers may be rejected earlier by the shared parser. Float/bool bed references cannot select integer keys and return 404/NOT_FOUND. Supplied invalid/nonexistent form references return 404 with field errors; omitted required form references, ordinary invalid choices and missing required dates return 400/VALIDATION_ERROR. JSON allocation/payment create has a separate missing student_id lookup returning 404 without form field errors.

**Actual:** Typed dates/references and required/missing-reference requests returned the specified 400/404 error contracts without changing business state/counters/audits; valid optional-date controls passed. 65 recorded observations completed; exact expected/actual values are in [the case record](evidence/issue63/execution/TC-REG-S2-16.json).

**Execution status:** OWNER PASS

**Tested commit:** 6636098cb728aa17c2abf5e42c358a5d400261e7 (clean execution; tree 0faea77304a30ceb436e1411a2c513dd1f3c6f44). Historical companion commit: 70c9fe20e462eb0b052e15434f19b347a793afa1.

**Execution date and environment:** 8 November 2026, Windows-11-10.0.26200-SP0, Python 3.14.7, Django 5.2.18, MySQL 8.4.9; synthetic disposable test_hms, Django HTTP test client/service/ORM. [Exact command/settings/versions](evidence/issue63/execution/run.json). Earlier 7 November Linux companion observations retain their separate provenance below.

**Evidence:** [Case observations](evidence/issue63/execution/TC-REG-S2-16.json); [execution/JUnit/hash index](evidence/issue63/README.md); historical [companion extraction](evidence/issue37/ci-methods.json).

**Defects and retests:** #45 (payment-report Bed), #46 (allocation confirmation), #47 (allocation dates), #48 (self-service dates) are retained in the source/evidence chronology where relevant; no new defect is inferred solely from adding a case.

**QA disposition:** Three independent automated reviewers checked the recipe, assertions and candidate evidence before the clean committed run; current scoped technical review found no remaining blocker. Final actual human approval and whole-plan entry/exit acceptance are not supplied.

**Automation:** [`scripts.part3.test_owned_reports_inputs.OwnedReportInputCases.test_tc_reg_s2_16_typed_dates_references_and_contracts`](../../scripts/part3/test_owned_reports_inputs.py#L651); retained historical companions: [`allocations.test_workflows.AllocationWorkflowTests.test_json_date_types_return_400_without_changing_allocations`](../../allocations/test_workflows.py#L67); [`allocations.test_workflows.AllocationWorkflowTests.test_json_reference_types_cannot_select_a_different_integer_key`](../../allocations/test_workflows.py#L111); [`allocations.test_workflows.AllocationWorkflowTests.test_json_form_errors_preserve_reference_and_validation_status_codes`](../../allocations/test_workflows.py#L494); [`payments.test_workflows.PaymentWorkflowTests.test_json_date_types_return_400_without_consuming_receipts`](../../payments/test_workflows.py#L53); [`payments.test_workflows.PaymentWorkflowTests.test_form_encoded_missing_student_preserves_json_not_found_response`](../../payments/test_workflows.py#L471); [`hms.test_forms.DateFieldTests.test_unexpected_json_types_produce_validation_errors`](../../hms/test_forms.py#L20); [`hms.test_forms.DateFieldTests.test_dates_text_and_optional_empty_values_keep_standard_behavior`](../../hms/test_forms.py#L12); [`hms.test_forms.ModelChoiceFieldTests.test_non_integer_json_keys_are_rejected_without_a_query`](../../hms/test_forms.py#L29); [`hms.test_responses.FormErrorResponseTests.test_invalid_reference_preserves_field_errors_and_returns_not_found`](../../hms/test_responses.py#L14); [`hms.test_responses.FormErrorResponseTests.test_other_invalid_choices_and_required_references_remain_bad_requests`](../../hms/test_responses.py#L31); [`hms.test_responses.FormErrorResponseTests.test_invalid_choices_require_an_explicit_reference_field_to_return_404`](../../hms/test_responses.py#L46)

**Historical companion outcomes (7 November):** 11 PASS and 0 expected timing SKIP in each current CI bundle. These are method outcomes, not a new case-level execution or unit-only result.

**Evidence limits:** Current execution is synthetic integration evidence with explicit late-entry, MySQL8.4 and HTTP test-flag limits; no new browser/TLS or unit-only claim. Whole-team acceptance remains pending. Historical companion limitation (not the new execution): Containers can fail shared parser before field validation; code invalid field assertions specifically apply integer/bool date values.

### TC-SEC-08: OWASP ZAP baseline on the running application

<a id="case-tc-sec-08"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; High (proposed). Risk: authentication, privacy or security failure can expose protected data or operations.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** NFR-7, NFR-10, NFR-12

**Level:** System / security scan

**Type:** Security

**Prerequisites and data:** A real isolated test deployment with synthetic data is running and reachable by the scanner; record exact build/configuration and tested scan scope. A public host is unnecessary. Synthetic data only; retain the source-bound setup with actual execution.

**Steps:**

1. Run the OWASP ZAP baseline against the isolated application using the tool's documented baseline procedure; record tool/version, target and command.
2. Retain sanitized results, reached URLs and any authentication/coverage limits.
3. Triage findings by severity, link defects and retest after fixes; distinguish unavailable or excluded authenticated areas.

**Expected:** Baseline completes against the actual running application; findings are recorded as defects and triaged. Scan coverage/limitations are explicit. The whole-plan exit criterion requires zero open critical/high defects; a baseline is not required to have zero informational alerts.

**Actual:** ZAP 2.17.0 passive baseline completed on 9 November against the isolated loopback app (one site, 10 spidered URLs, exit 0; no active scan). Final result: 0 High, 0 Medium, 1 Low server-banner alert (four responses, temporary Python `wsgiref` probe server), and 1 Informational/Low-confidence `next`-parameter hotspot (two instances); the HTML-injection regression test confirms the supplied marker is not reflected. Initial CSP and CSRF-cookie findings disappeared after code fixes and rescan. Sanitized details and limitations are recorded in [issue38-security-20261109](evidence/issue38-security-20261109/README.md) and its JSON.

**Execution status:** PARTIAL

**Tested commit:** PR #68 head `49851396796918103681aacf47394e5010426201` (probe evidence generated on equivalent pre-publication source; published code was subsequently confirmed at this exact head by CI).

**Execution date and environment:** 9 November 2026; Windows 11, OWASP ZAP 2.17.0, Java 25.0.2, synthetic SQLite-backed app bound only to `127.0.0.1`; passive baseline only.

**Evidence:** [sanitized transport/ZAP report](evidence/issue38-security-20261109/README.md); [machine-readable summary](evidence/issue38-security-20261109/transport-zap-summary.json); [full-suite MySQL CI](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42566973066)

**Defects and retests:** CSP and CSRF-cookie findings were fixed and absent on rescan. The remaining low server-banner and informational hotspot are recorded with QA disposition pending; no defect IDs or false-positive acceptance are invented. No high/medium ZAP findings were observed in this passive baseline.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** Manual/operational evidence required; no automated method substitutes for this criterion.

**Evidence limits:** The scan is passive and loopback-only, reached 10 URLs, and does not claim authenticated-area coverage or a deployed environment. Remaining alerts have not received QA disposition; no active scanning was run. Test Plan section 5.1 already requires this scan. This ID makes that existing obligation explicit; it is not a newly invented faculty requirement.

### TC-QUAL-02: Working-hours service availability

<a id="case-tc-qual-02"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Sreeharsha

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** SRS section 6.4 quality attributes (no invented core requirement ID).

**Level:** Operational / quality

**Type:** Reliability

**Prerequisites and data:** Agreed observation period covering working days, a defined reachable application endpoint, timestamped probes and a recorded downtime policy. Record host/build and the period before interpreting percentages. Synthetic data only; retain the source-bound setup with actual execution.

**Steps:**

1. Observe service availability during 08:00-20:00 on the agreed working days.
2. Retain timestamped successful and failed probes/downtime intervals, including exclusions approved in advance.
3. Calculate available monitored working-hours time divided by total agreed working-hours time.

**Expected:** At least 99% availability during the SRS-defined working hours (8 am to 8 pm on working days), with reproducible monitoring/period evidence.

**Actual:** No working-hours availability observation is published; short CI, load and recovery runs do not measure this target.

**Execution status:** NOT RUN

**Tested commit:** No complete case execution recorded; supporting observations retain their original SHAs.

**Execution date and environment:** No complete case run recorded.

**Evidence:** [HMS21_Final_Readiness.md](HMS21_Final_Readiness.md)

**Defects and retests:** No result or severity is inferred; record genuine findings/retests when execution occurs.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** Manual/operational evidence required; no automated method substitutes for this criterion.

**Evidence limits:** SRS section 6.4 quality attribute; the original 33-case table had no dedicated availability case.

### TC-QUAL-03: SRS portability and real mobile coverage

<a id="case-tc-qual-03"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Vaishnavi

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** SRS section 6.4 quality attributes (no invented core requirement ID).

**Level:** System / platform compatibility

**Type:** Portability

**Prerequisites and data:** Record the candidate build, Windows/Linux server versions, current and previous browser versions and one actual mobile browser/device. Define main flows from the submitted Plan, retaining synthetic data and roles. Synthetic data only; retain the source-bound setup with actual execution.

**Steps:**

1. Execute the main application flows on latest two versions of Chrome, Firefox and Edge, retaining exact versions and results.
2. Verify supported Windows and Linux operation, recording deployment/configuration and exercised flows on each.
3. Exercise main browser flows on a real mobile phone; retain device/browser and responsive navigation/form observations.

**Expected:** SRS portability target (Windows/Linux and latest two Chrome/Firefox/Edge versions) and the Test Plan's real-mobile environment are evidenced. Original TC-QUAL-01 still separately covers the latest-browser main flows and timed new-warden guide task.

**Actual:** Historical Windows Firefox/Edge pages, three new desktop Chrome page captures and historical Linux CI are supporting observations. They do not establish the latest-two browser targets, Windows/Linux deployed workflows or actual mobile execution. The new screenshots have no recorded capture build/date/version.

**Execution status:** NOT RUN

**Tested commit:** No complete case execution recorded; supporting observations retain their original SHAs.

**Execution date and environment:** No complete case run recorded.

**Evidence:** [Historical HMS-17 index](evidence/issue39/README.md); [8 November follow-up review](evidence/issue39/followup-20261108.md); [retained earlier CI extraction](evidence/issue37/ci-methods.json).

**Defects and retests:** No result or severity is inferred; record genuine findings/retests when execution occurs.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** Manual/operational evidence required; no automated method substitutes for this criterion.

**Evidence limits:** The submitted Plan permits Windows 10+ OR Ubuntu 20.04+ and latest Chrome/Firefox/Edge; SRS section 6.4 separately requires Windows AND Linux/latest-two targets, and the Plan includes a real mobile phone. No full Cartesian product is imposed. Current supporting pages/CI do not supply a scoped complete execution of this case.

### TC-QUAL-04: Application-logic unit coverage and maintainability

<a id="case-tc-qual-04"></a>

**Provenance:** Added 7 November to represent accepted sprint changes or explicit submitted Plan/SRS scope; no backdated execution.

**Owner:** Vaishnavi (QA), Devansh (coverage evidence), Sreeharsha (PO review)

**Priority:** Unspecified in original plan; Medium (proposed). Risk: an incorrect operational result, user workflow or quality target disrupts staff work.

**Priority review:** Proposed 7 November; no historical approval inferred. Agree before applying the High-priority exit criterion.

**Requirements:** SRS section 6.4 quality attributes (no invented core requirement ID).

**Level:** Component / unit evaluation

**Type:** Maintainability

**Prerequisites and data:** Publish #41's Unit Test Report and agree unit/integration classification, application-logic scope and execution attribution. Preserve application code in the denominator; retain measured evidence and any approved interpretation. Synthetic data only; retain the source-bound setup with actual execution.

**Steps:**

1. Run repository lint/format checks and review modular app boundaries and PEP 8 adherence, recording configured rules, results and any style exceptions outside those rules.
2. Identify modular Django application logic and distinguish unit methods from integration/system methods.
3. Measure agreed unit-only coverage against the recorded application-logic denominator, with imports/startup/fixtures and omissions explicit.
4. Assess the SRS threshold, retaining failing or unproven outcomes and exact revision/commands.

**Expected:** The complete SRS section 6.4 maintainability target is assessed: modular Django apps, PEP 8 adherence and unit tests covering at least 70% of application logic. Repository lint/format checks support the style assessment; mixed-suite statement/branch percentages alone cannot establish unit70.

**Actual:** Current CI lint and format gates passed under the repository's configured rules. Full PEP 8 adherence beyond those rules is not certified. #41 Unit Test Report and agreed scope/attribution are missing. Published coverage reports deliver measurements but leave formal unit70 UNPROVEN.

**Execution status:** BLOCKED

**Tested commit:** No complete case execution recorded; supporting observations retain their original SHAs.

**Execution date and environment:** No complete case run recorded.

**Evidence:** [Code_Coverage_Report.md](Code_Coverage_Report.md); [Branch_Coverage_Report.md](Branch_Coverage_Report.md); [evidence/issue42-main/README.md](evidence/issue42-main/README.md); [evidence/issue37/ci-methods.json](evidence/issue37/ci-methods.json)

**Defects and retests:** No result or severity is inferred; record genuine findings/retests when execution occurs.

**QA disposition:** Owner/companion evidence and limits are documented; final case/entry/deviation acceptance is not inferred by this documentation merge.

**Automation:** Manual/operational evidence required; no automated method substitutes for this criterion.

**Evidence limits:** Coverage evidence delivery #42 is closed; this separate application-logic interpretation remains unresolved. Configured lint/format success is supporting PEP 8 evidence, with rule coverage/exceptions requiring review. No new branch-percentage grading target is introduced.
