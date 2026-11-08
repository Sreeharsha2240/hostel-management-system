# Linux offline fixture correction and retained failed CI

[PR #64 run 42461324489](https://github.com/Sreeharsha2240/hostel-management-system/actions/runs/42461324489)
on head `f3ae4618bcb26a04e714a07b667f2ad5445dee50` **FAILED** on Python 3.11
and 3.14. Both core checks passed, but the offline runner-safety fixture failed
with `AssertionError: 2 != 1`. The nine-case step was consequently skipped and
its artifact upload found no output. This failed run is not a nine-case pass.
The [retained extraction](failed-ci-42461324489.json) identifies both passing
core bundles and their raw hashes alongside the actual failure.

The fixture mocked the shared `subprocess.run` function and counted every call.
On Linux, `platform.platform()` can obtain its processor information through
`subprocess.check_output(['uname', '-p'])`, which calls that same mocked
function. Windows did not make this incidental probe in the measured local
run. The extra metadata call was mistaken for a launched test child.

The correction isolates `platform.platform()` inside this offline fixture and
asserts the exact sole `git check-ignore` call. Database refusal still must
preserve failure metadata and must never launch the Django test child. No production code,
execution runner, case recipe, threshold or expected result changes. A blind
reviewer independently traced the stdlib path and accepted this fixture-only
correction.

The [controlled reproduction](platform-fixture-reproduction.json) simulates
that incidental platform probe: the previous fixture fails, and the corrected
fixture passes. No database or actual external process is invoked. All seven
offline safety methods then passed locally. Replacement matching-head CI is
required before merge and is recorded on the pull request/issue.
The [local retest log](runner-safety-retest.txt) preserves the seven outcomes.

The original clean nine-case execution at `6636098` and all its hashes remain
unchanged. Its safety-fixture source hash identifies the old fixture; the
subsequent correction is explicit and is not relabelled as part of that earlier
measurement. Current delivery validation verifies all 162 historical inputs,
checks the other 160 current input hashes, and separately identifies this fixture
and the case document's post-run metadata as the only measured-input changes.
