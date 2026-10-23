---
name: fable-recover
description: "Diagnose repeated command failures, stale build caches, branch drift, or contradictory evidence before attempting further code edits. Use when commands fail repeatedly, tests stay red after attempted fixes, build output contradicts source code, or the execution path is confused — even if the user does not explicitly say \"fable-recover\" (e.g. \"still failing\", \"why did this fail again\", \"stuck in a failure loop\", \"diagnose this error\"). Do NOT use for routine first-time test failures in fresh TDD (use fable-tdd)."
version: 1.3.0
pack: core
inputs:
  - failure_evidence
requires:
  - failure_streak
produces:
  - revised_hypothesis
  - bounded_repair
gates:
  - diagnosis_changed
fallback: fable-discover
mutatesWorkspace: false
parallelSafe: false
neural_links:
  precursors:
    - fable-tdd
    - fable-execute
    - fable-verify
  continuations:
    - fable-discover
    - fable-plan
    - fable-execute
  lateral_peers:
    - fable-discover
  recovery: fable-discover
---

# Fable Recover

Stop spending mutations on a failing hypothesis. Rebuild causal confidence before changing code again.

## Mission
Recovery exists for the moment an agent is most likely to become expensive and irrational: the same task has failed more than once, output contradicts expectations, or edits appear to have no effect.

The goal is not to "try something different." The goal is to explain why previous attempts failed, falsify competing causes, and issue one repair that is justified by new evidence.

## Activate When
- the same command/test/behavior fails after two materially similar implementation attempts;
- output appears stale or unaffected by known source changes;
- tests/runtime disagree;
- evidence contradicts a load-bearing assumption;
- failures alternate or depend on timing/environment;
- the agent is about to repeat a command/patch without new diagnostic information.

## Do Not Activate When
- first failure is a trivial syntax/type error introduced by the current edit;
- architecture is simply unknown and no repeated failure occurred (`fable-discover`);
- expected RED in TDD is being observed correctly;
- a narrow review finding already has an obvious bounded repair.

## Failure Classification
Start by classifying the evidence, not the code.

| Class | Typical signals | First probes |
| --- | --- | --- |
| Harness | assertion never reached, fixture/mock/setup error | prove test path and fixture |
| Environment | local/CI/OS/env-specific | versions, env, cwd, permissions |
| Artifact/cache | source changes not reflected | entrypoint, build timestamps, cache, dist |
| Execution path | edited code never executes | tracing/instrumentation/registration |
| Dependency/version | unexpected API/runtime semantics | lockfile, resolved version, official source |
| Data/state | only some fixtures/accounts/orders fail | minimal failing state, persistence boundaries |
| Concurrency/timing | intermittent/order-sensitive | deterministic coordination, shared state |
| Product logic | harness/path proven, assertion consistently wrong | isolate algorithm/branch |
| Invariant/design | local fixes move failure elsewhere | identify violated cross-component rule |

Do not jump to product logic until cheaper external explanations are falsified.

## Recovery Protocol

### Stage 1 — Freeze mutation
No new production edits until the diagnosis changes. Preserve the failing state and collect exact evidence.

Record:
- command/action;
- exact error/output;
- workspace/commit/mutation generation;
- attempts already made and what differed;
- expected observation.

### Stage 2 — Reproduce minimally
Find the smallest reliable reproduction. If the failure is flaky, capture seeds/order/time/environment and work on determinism before another fix.

### Stage 3 — Build a hypothesis queue
Create 2-5 plausible causes ranked by:
- ability to explain all observed evidence;
- probability given recent changes;
- cost/safety of falsification.

Each hypothesis must predict an observation that would distinguish it.

Bad: "maybe cache."

Good: "CLI executes stale `dist/cli.js`; if true, source timestamp will be newer than dist and direct source invocation will show new behavior."

### Stage 4 — Walk the attribution ladder
Use the cheapest separating probes first:

1. **Harness** — does the test/probe reach the intended assertion/path with realistic inputs?
2. **Environment/artifact** — correct branch, cwd, env, version, build, cache, process?
3. **Execution path** — is edited code actually reached? which implementation is registered?
4. **Data/dependency** — does input/version/state differ from assumptions?
5. **Product logic** — with above proven, isolate the wrong branch/algorithm.
6. **Invariant/design** — if local logic is individually reasonable but system remains wrong, identify the violated system contract.

The ladder is guidance, not ritual. Skip a rung only when existing evidence already proves it.

### Stage 5 — Instrument or bisect when observation is weak
Use narrow temporary diagnostics, binary search/bisect, toggling one variable, or comparing known-good/bad states.

Change one diagnostic dimension at a time so the result is interpretable.

### Stage 6 — Falsify, do not accumulate guesses
After each probe:
- reject hypothesis;
- strengthen hypothesis;
- or revise the queue.

Do not keep contradicted explanations alive as "maybe still related."

### Stage 7 — Form the revised diagnosis
A valid diagnosis explains:
- why the observed failure occurred;
- why previous attempts did not fix it;
- what evidence distinguishes it from alternatives;
- what smallest repair should change the outcome.

### Stage 8 — Issue one bounded repair
Return to `fable-execute` or `fable-tdd` with one repair and one expected proof. If diagnosis reveals architecture uncertainty, route to plan/discover instead.

## Decision Rules
- Never repeat an unchanged failed command unless a named environmental/state variable changed or the rerun is explicitly measuring nondeterminism.
- Do not delete caches/build artifacts reflexively before recording evidence; destructive cleanup can erase the clue that proves staleness.
- If source changes have no runtime effect, prove the executed artifact/path before editing logic again.
- If CI-only failure exists, compare environment/version/parallelism first; do not assume CI is "random."
- If failure is data-specific, minimize the failing data/state before broad refactor.
- If a dependency/version hypothesis emerges, route external semantic verification to `fable-research`.
- If local patches shift failure between components, suspect a shared invariant/design and return to `fable-plan`.
- Similar failed fixes count as a failure streak; superficial syntax changes do not reset diagnostic responsibility.

## Invariants
- Recovery is diagnostic/read-only until a revised diagnosis exists.
- Every new probe is chosen to distinguish hypotheses.
- Contradicted hypotheses are removed.
- Diagnostic instrumentation is temporary and cleaned after repair.
- Final repair is bounded and tied to a predicted observable outcome.

## Failure Taxonomy of Recovery Itself
### Blind cleanup
Cache/build reset makes problem disappear but root cause is unknown. Record as unresolved unless causal evidence is obtained.

### Hypothesis sprawl
Long list of possibilities with no discriminating probes. Rank and test the cheapest separator.

### Mutation during diagnosis
Agent edits product while still uncertain, invalidating the failing state. Revert/restore diagnostic baseline where safe and restart evidence collection.

### Confirmation bias
Only probes supporting first theory are run. Add at least one falsifier for the leading hypothesis.

### Non-minimal reproduction
Huge suite/system creates too many confounders. Isolate smaller path before interpreting results.

## Anti-Patterns
- third/fourth patch with same causal theory;
- "clear cache and see" without recording before/after evidence;
- rerunning flaky command until green;
- blaming environment without comparing environments;
- adding broad logging everywhere;
- changing multiple diagnostic variables at once;
- preserving disproved assumptions;
- solving symptom while unable to explain previous failures.

## Recovery Packet

```text
Failure/reproduction:
Attempts already made:
Hypothesis queue:
Probe → observation → hypothesis effect:
Revised diagnosis:
Why prior attempts failed:
Bounded repair:
Expected proof after repair:
Residual uncertainty:
Next Skill:
```

## Completion Criteria
Recovery completes only when:
- a reliable enough reproduction exists or nondeterminism is explicitly characterized;
- leading alternative causes were falsified with evidence;
- diagnosis materially differs from the failed assumption/attempt;
- proposed repair is bounded and predicts a concrete changed observation;
- execution can resume without another blind retry.

## Progressive Resources
- Deep guide: `references/diagnostic-falsification-playbook.md`
- Existing ladder: `references/attribution-ladder.md`
- Example: `examples/recovering-stale-test-cache.md`
