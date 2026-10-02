---
name: diagnosing-bugs
description: Reproduce, isolate, and fix difficult bugs or performance regressions.
---

# Diagnosing Bugs

Diagnose hard bugs by combining reproduction, code inspection, provisional hypotheses, and targeted probes. Choose the next step by the evidence missing; the sections below are tools for the investigation, not gates that must be completed in order.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Build a feedback loop

Start from the user's exact symptom, expected behavior, entry point, environment, inputs, and action sequence. Trace the relevant code and use provisional hypotheses to identify the conditions a reproduction must preserve. Keep those hypotheses distinct from established causes.

Prefer an existing check that can fail on the reported bug and pass after the fix. Build or adapt a feedback loop when it will distinguish causes or verify the outcome; do not require a runnable reproduction before inspecting code or forming a testable explanation.

### Choose a useful check

Choose the cheapest check that reaches the reported failure. These are alternatives, not a sequence to exhaust:

1. **Failing test** at whatever seam reaches the bug: unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) that drives the UI and asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** For input-dependent failures, use bounded input generation and retain the seed and failing inputs.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **Human-assisted reproduction.** If the agent cannot exercise the path, give the user precise actions and ask for the relevant observations. Use `scripts/hitl-loop.template.sh` when a repeatable terminal-guided loop helps.

Record the command or manual actions, relevant conditions, and observed result. Distinguish a check that has reproduced the symptom from one that is only expected to catch it.

### Tighten the loop

Improve the loop when doing so will make the next experiment more useful:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

Speed, determinism, and unattended execution help iteration, but none is a prerequisite for useful evidence. Stop optimizing the harness when the next diagnostic check would teach more.

### Non-deterministic bugs

Use bounded runs and record attempts, failures, and conditions. Control scheduling, seeds, concurrency, or workload when the suspected mechanism justifies it and the experiment preserves the reported failure. Choose further runs or instrumentation by the uncertainty they can resolve, not a required reproduction rate. A run without failures does not by itself prove a flaky bug is gone.

### When reproduction is unavailable

State what was tried and the evidence gap. Continue relevant code inspection, trace analysis, and safe probes that can narrow the cause. Ask for a specific environment, redacted artifact, or permission for production instrumentation only when that missing input blocks further progress; continue independent investigation while waiting.

Keep the leading cause provisional until the evidence establishes the mechanism. If an authorized fix is supported by code or captured evidence despite unavailable reproduction, explain that basis and the verification still missing. Do not claim the original bug was reproduced or proven fixed without observing it.

## Reproduce and reduce the scenario

When execution is available, establish that the check reaches the user's failure mode, rather than a nearby error or merely successful execution. Capture the exact symptom and relevant conditions for comparison after the fix. Repeat only when needed to distinguish a stable result from noise.

Reduce inputs, callers, configuration, data, or steps when doing so helps isolate the mechanism or makes verification practical. Change one suspected factor at a time and check whether the same failure remains.

Stop reducing when the scenario is small enough to test the leading explanation or a different probe would be more informative. Complete minimization is not required before testing a hypothesis or applying a supported fix. Retain the original scenario for final verification; a reduced path may bypass the reported defect.

## Test hypotheses

Form and revise hypotheses throughout the investigation. Use one leading explanation when the evidence is specific; compare alternatives when several mechanisms fit the observations. Do not invent candidates to fill a quota.

For each hypothesis worth testing, identify its supporting evidence and a prediction that would distinguish it from the alternatives or disprove it. Choose the cheapest decisive check, then update the explanation from the result.

For example: if a stale cache causes the wrong value, bypassing that cache under the same inputs should restore the expected value. Check whether the result supports that mechanism rather than assuming any improvement confirms it.

Share the leading explanation, material uncertainty, and next check when they help the user follow or correct the investigation. Continue without waiting unless a decision or missing evidence actually blocks the next step.

## Instrument

Each probe must resolve a specific uncertainty or test a prediction. Change one variable at a time when comparing outcomes so the result remains attributable.

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

For performance regressions, establish a baseline under the reported workload with a timing harness, profiler, or query plan. Use profiling, bisection, or a focused experiment according to the suspected cause. Compare the same workload after the fix; do not claim a measured improvement when baseline or after-change measurements are unavailable.

## Fix and verify

Write the regression test before the fix when it can exercise the real bug through a practical seam.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

If no practical regression-test seam exists, explain the limitation and use the closest meaningful check through the real behavior, such as the original browser flow, replay, or command. Do not create substantial test infrastructure or a misleading test merely to satisfy this workflow.

When that test is practical:

1. Turn the supported failure scenario into a focused regression test at that seam.
2. Run it before fixing the code and confirm it fails for the intended reason. If it does not, investigate the mismatch rather than treating it as proof of the reported bug.
3. Apply the fix supported by the established mechanism.
4. Run the check again and confirm the intended behavior passes. If it still fails, return to the investigation.

Preserve the relevant starting state, configuration, and real decision path in the regression. Setup must not repair a prerequisite that the reported workflow lacks. A check that expects graceful rejection does not prove the required operation succeeds.

Change expectations only when an authorized requirement changed or evidence establishes that the test was wrong against the requirement. Interface or setup changes must retain the protected failure case. Do not accept new output, replace a failing collaborator with a successful stub, or skip the regression merely to get green.

Continue authorized fixes and necessary restructuring. If a valid failure depends on an unresolved decision, unavailable prerequisite, or material scope expansion, preserve the failing test and report the blocker and remaining work. A reproduction-only request can finish with a red test; an implementation request remains incomplete. Distinguish behavioral failure from a check that could not reach the behavior, and confirm the reported command actually ran the regression.

Whether or not a durable test was added, verify the fix through the original entry point, environment, inputs, and sequence when accessible. A reduced reproduction or lower-level test supports that verification but does not replace it. For intermittent failures, report the before/after observations and remaining uncertainty. If either failing-before evidence or original-scenario verification is unavailable, state that gap explicitly.

After confirming the fix, consider whether the bug exposed a stable invariant that can be enforced at the seam that owns it. Prefer an existing structural mechanism—such as a type or schema constraint, boundary validation, lint rule, or canonical entry point—when it prevents the demonstrated bug class. Keep the regression test as behavioral proof. Do not add machinery for an isolated failure with no credible recurrence, and do not expand the authorized scope to enforce the invariant.

## Cleanup and report

Before finishing:

- Record the original-scenario result, regression check, and any verification gap. Reuse results from the final implementation; rerun only after a relevant change or when uncertainty warrants it.
- Remove temporary debug instrumentation and throwaway artifacts created for the investigation, or keep useful artifacts in an agreed debug location.
- Report the supported cause, fix, verification evidence, and remaining uncertainty. Include the cause in a commit or PR description when that publication was requested.
