---
name: fable-verify
description: "Falsify software implementations and gather fresh, machine-checked acceptance proof across tests, builds, typechecks, and runtime smoke checks before completion. Use when running test suites, checking type correctness, validating acceptance criteria, or verifying post-mutation code integrity — even if the user does not explicitly say \"fable-verify\" (e.g. \"verify my changes\", \"run all tests and typecheck\", \"check if everything passes\", \"prove this works\"). Do NOT use for planning (use fable-plan) or diff code review (use fable-review)."
version: 1.3.0
pack: core
inputs:
  - implementation_diff
requires:
  - test_suite
produces:
  - verification_evidence
  - falsification_verdict
gates:
  - fresh_mutation_covered
  - machine_checked
fallback: fable-recover
mutatesWorkspace: false
parallelSafe: true
neural_links:
  precursors:
    - fable-execute
    - fable-tdd
  continuations:
    - fable-review
    - fable-security
    - fable-release
  lateral_peers:
    - fable-simulator
    - fable-run
  recovery: fable-recover
---

# Fable Verify

Try to prove the implementation wrong, then report only the claims that survive fresh evidence.

## Mission
Verification is not "run the test suite." It is coverage of changed risk with evidence that is both relevant and fresh.

A green command proves only what it actually exercised. Build success does not prove runtime behavior. Security success does not prove functional correctness. Unit success does not prove a packaging or integration path. Old evidence does not prove a newer mutation.

## Activate When
- implementation or repair is ready for independent proof;
- a completion claim needs fresh evidence;
- a review/release gate requires test/build/runtime evidence;
- stale evidence must be refreshed after mutation;
- the suspected regression surface spans more than the focused TDD test.

## Do Not Activate When
- writing the implementation (`fable-execute`/`fable-tdd`);
- deciding architecture (`fable-plan`);
- reviewing design/maintainability from the diff (`fable-review`);
- diagnosing repeated confusing failures (`fable-recover`).

## Risk Classification
Map each changed surface to the evidence capable of falsifying it.

| Changed surface | Typical evidence |
| --- | --- |
| pure behavior | focused unit/property + affected suite |
| cross-module contract | integration/contract test |
| public CLI/API | invocation/smoke + contract tests |
| build/export/package | build + package/clean-install smoke |
| persistence/migration | integration + migration/compatibility fixtures |
| async/concurrency | deterministic ordering/stress supplement |
| config/feature flag | tests under relevant config branches |
| browser/UI | component/integration/E2E as appropriate |
| security boundary | security-specific checks **plus** functional evidence |
| performance-sensitive path | targeted measurement when requirement exists |

## Verification Protocol

### Stage 1 — Read the diff and execution packet
Do not choose commands from habit alone. Identify:
- behavior changed;
- files/contracts touched;
- tests added/changed;
- generated/package/config surfaces;
- residual risks from implementation;
- current mutation generation.

### Stage 2 — Build a verification matrix
For each material risk, write:
- claim;
- failure mode;
- evidence/command that would catch it;
- whether evidence must be narrow, integration, runtime, build, E2E, security, or package-level.

Remove duplicate checks that prove the same narrow fact; add missing checks for untested surfaces.

### Stage 3 — Run narrow, causal checks first
Start with the focused changed behavior and affected tests. Fast local evidence helps distinguish implementation failure from unrelated suite noise.

### Stage 4 — Expand according to blast radius
Run broader typecheck/build/test/integration/E2E/package gates only where the change can affect them or where repository release policy requires them.

Do not skip required project-wide gates merely because narrow tests pass.

### Stage 5 — Adversarial falsification
Actively probe the most plausible regression surfaces:
- boundary/empty/invalid inputs;
- error propagation;
- retries/idempotency;
- compatibility old/new formats;
- async ordering/concurrency;
- cleanup/resource lifecycle;
- package/export/runtime entry point;
- configuration branch.

Prefer tests/commands that can fail meaningfully over speculative prose.

### Stage 6 — Detect nondeterminism and stale execution
If identical commands alternate outcomes, stop counting passes. Capture the variability and route to recovery.

If results do not reflect known source changes, check source-vs-build, cache, branch, env, process, and artifact path before accepting output.

### Stage 7 — Record typed, fresh evidence
Evidence should include:
- kind (`test`, `build`, `runtime`, `review`, `security` where applicable);
- exact command/probe;
- exit/result and relevant counts;
- mutation generation/artifact SHA when available;
- scope/claim the evidence proves.

### Stage 8 — State the verdict narrowly
Use:
- **PASS**: every required claim has fresh relevant evidence;
- **FAIL**: at least one required claim is falsified;
- **INCOMPLETE**: required evidence cannot be obtained or does not cover the risk.

Never convert INCOMPLETE to PASS because the remaining check is inconvenient.

## Decision Rules
- Evidence generation older than current relevant mutation → stale, rerun.
- Test passes but does not execute changed path → irrelevant evidence, not PASS.
- Security-only evidence for functional bug → require functional proof.
- Build/typecheck-only evidence for runtime behavior → require runtime/test proof.
- Focused test green but integration contract changed → run integration/contract evidence.
- Package/export change → inspect/package/smoke the distributed artifact, not only source tests.
- Flaky alternating outcomes → route to `fable-recover`; do not cherry-pick a green run.
- New verification failure caused by a bounded obvious implementation defect → return one repair card; repeated/ambiguous failure → recover.
- If a command is unavailable in current environment, mark evidence incomplete and name the external gate instead of fabricating a result.

## Invariants
- Verification is read-only with respect to product behavior; any repair starts a new mutation/evidence cycle.
- Every completion claim maps to fresh evidence.
- Evidence kinds are not interchangeable.
- The final verdict covers the current mutation generation/artifact.
- Required failures/warnings are not hidden by truncating output or rerunning until green.

## Failure Taxonomy
### Relevant test failure
Changed behavior is falsified. Return bounded repair or recover depending on clarity/repetition.

### Unrelated suite failure
Prove it is unrelated before excluding it; do not dismiss merely because it predates the change.

### Stale evidence/artifact
Output corresponds to older mutation/build. Refresh build/path/env before evaluating implementation.

### Nondeterministic verification
Same state produces inconsistent result. Diagnose shared state/timing/environment before verdict.

### Coverage gap
Available checks do not exercise material changed risk. Add/locate suitable evidence or mark incomplete.

### Environment limitation
Required external service/browser/platform/release environment unavailable. Report exact missing evidence; do not emulate a pass.

## Anti-Patterns
- `tests passed` as the entire verification report;
- running only tests the implementer just wrote;
- rerunning flaky tests until green;
- trusting old screenshots/logs after code changed;
- treating typecheck/build/security as functional proof;
- ignoring packaging/export paths;
- broad full-suite runs with no affected-risk reasoning;
- claiming pass when an external required gate was never run.

## Verification Packet

```text
Current mutation/artifact:
Changed risks:
Verification matrix:
- claim → evidence → result
Adversarial probes:
Stale/nondeterministic evidence detected:
Required external evidence not run:
Verdict: PASS | FAIL | INCOMPLETE
Repair/recovery recommendation:
```

## Completion Criteria
Verification completes when:
- changed risks have relevant checks;
- required project gates are executed or explicitly marked unavailable;
- evidence is fresh for current mutation/artifact;
- likely edge/failure surfaces were actively probed;
- nondeterminism/stale output is not hidden;
- verdict is no broader than the evidence supports.

## Progressive Resources
- Deep matrix guide: `references/verification-matrix-and-evidence-strength.md`
- Existing falsification heuristics: `references/falsification-heuristics.md`
- Evidence recording: `references/evidence-recording.md`
- Example: `examples/falsification-session.md`
