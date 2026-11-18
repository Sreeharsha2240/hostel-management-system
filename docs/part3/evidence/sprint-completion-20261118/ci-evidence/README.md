# Exact-revision CI evidence

Reviewed head: `e2fe45fa7877bccbe9a864ff4cb3097efd3e2bdf`, tree
`1c30b1e73f2bf466821e0bdd749c544ff6010424`. [PR #91](https://github.com/Sreeharsha2240/hostel-management-system/pull/91)
merged as `9ad6cf9a076d3b87f3287e46f73e118bc80ec0b0` with that same tree.
The later evidence-only checkpoint retains all 208 frozen application/test/tool
input hashes. No application code changed to make coverage reports agree.

Both Python 3.11 and 3.14 passed in the explicit exact-head
[run 44383638276](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/44383638276)
and automatic [PR run 44383945828](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/44383945828).
The complete [strict reconciliation](ci-summary.json) downloaded all six explicit-run
ZIPs and verified their API digests, extracted bytes, raw artifacts, clean source,
full Git tree, source pins, exact method outcomes, attribution and denominators.
All 14 recorded audit checks passed. This is assisted technical verification,
not another person's signature or original course acceptance.

Per job: 13 successful gates; 727 mixed identities (726 PASS/one expected timing
SKIP), separate timing PASS, 288/415 isolated PASS with zero DB attempts, nine
owned recipes PASS. Two Python jobs do not double the distinct test count.

## Interpreter-specific statement boundaries

| Measurement | Python 3.11 | Python 3.14 |
|---|---:|---:|
| Mixed application statements | 2,686/2,733 | 2,683/2,730 |
| Mixed configured statements, including verification scripts | 2,998/3,384 | 2,995/3,381 |
| Mixed configured branch outcomes | 821/1,000 | 821/1,000 |
| Baseline method-attributed function-body statements | 1,158/1,740 | 1,158/1,740 |
| Expanded method-attributed function-body statements | 1,547/1,740 (88.91%) | 1,547/1,740 (88.91%) |
| Expanded all-application-statements companion | 1,547/2,733 (56.60%) | 1,547/2,730 (56.67%) |

The only interpreter-dependent lines are the three annotation-only `_Cluster`
fields at `payments/receipts.py:117-119`. Python 3.11 emits eager class-annotation
operations; Python 3.14 emits deferred `__annotate__` code, which pinned coverage
7.16.2 explicitly excludes from its bytecode boundary. The declarations get
**no selected-method credit** in either job. Callable-body lines, method hits,
contexts and all branch outcomes agree. The private read-only audit predicts
only those six resulting measurement-field differences from the pinned source
AST; unrelated differences remain failures. The frozen measurement harness and
`.coveragerc` remain byte-identical to their historical accepted versions.

## Namespace script inventory

Raw isolated coverage has 59 files; mixed coverage has 64. All application files
and all shared-file statement/branch boundaries match exactly. The five mixed-only
paths are the pinned `scripts/part3/` backup helper, unit gate, focused security
runner, browser runner and load runner. Namespace discovery depends on imported
modules because these verification directories have no `__init__.py`.

Each exact mixed-only Git object was independently parsed: all 538 statements and
174 branch outcomes across the five files match the raw mixed reports. Their
configured mixed metrics are retained. No absent unit row, execution or unit
credit is invented. The application-unit subtotal excludes verification scripts
under the unchanged documented method. Positive and adversarial probes and two
independent reviews checked both narrow reconciliations before the complete
audit passed.

- [Python 3.11 per-file metrics](coverage-metrics-py3.11.json) and [tables](coverage-tables-py3.11.md)
- [Python 3.14 per-file metrics](coverage-metrics-py3.14.json) and [tables](coverage-tables-py3.14.md)

The official artifacts retain their provider expiry dates; the source-bound
metrics, hashes, method identities and audit record above are committed here.
Raw local observations and the initial measurement archive keep their actual
source revisions rather than being relabelled as a later publication.
