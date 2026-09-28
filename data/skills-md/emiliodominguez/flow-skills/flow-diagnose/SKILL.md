---
name: flow-diagnose
description: "Root-cause investigation for hard failures. Use when a bug, regression or crash in the product has no obvious cause, or a first fix did not hold. Hands off to `flow-work` or `flow-triage`."
metadata:
  stage: operate
---

# Diagnose

Reduce uncertainty before changing behavior. A matching prediction supports a hypothesis;
confirmation needs evidence that rules out plausible alternatives.

## Process

1. Establish symptom, expected behavior, environment, revision and impact. Reproduce with a
   small input when possible. For intermittent failures, record frequency, logs, traces and
   conditions instead of waiting for an on-demand repro. Name the check that will prove the
   eventual fix (a failing regression test or a controlled signal), even before the cause is known.
2. State a falsifiable hypothesis per plausible cause, with predictions and evidence for and
   against. Keep observations separate from explanations. Inspect actual data/control flow
   and changes near onset.
3. Pick the experiment that discriminates among causes. A stale read alone cannot separate
   cache invalidation from replica lag. Use a controlled intervention, boundary trace or
   counterexample, accounting for confounders and observer effects.
4. Instrument the smallest useful boundaries: structured logs, no sensitive payloads, only the
   inputs, correlation and timing the question needs. For performance, profile the workload.
5. Update each hypothesis: refuted, supported, confirmed or unresolved, in a compact evidence
   table. Parallel read-only investigation is fine for independent questions when authorized;
   agents must not race to patch competing theories.
6. Once the cause is supported, make the smallest in-scope correction. Add a regression test
   that fails on the defect and passes on the fix where practical; otherwise keep a
   reproducible trace or controlled acceptance check and state its limits.
7. Check the fix, affected behavior and required repository gates. Remove temporary
   instrumentation unless intentionally kept. Report root-cause confidence and residual risk.

## Stop conditions

Honor any investigation budget. If experiments stop yielding information, access is missing,
or evidence cannot separate causes, report the smallest missing observation instead of guessing
or repeating a patch. Urgent containment belongs in `flow-triage` under the user's operational
authorization.

## Red flags

- "I know what this is": write the competing hypothesis down and test it anyway.
- "Let me try one more change": no new patch without a new observation.
- "It went away": an unexplained disappearance is not a fix.
- "Three fixes failed": the model of the system is wrong; revisit assumptions, not the patch.

## Anti-patterns

- Treating correlation or one matching prediction as causation.
- Blocking on deterministic reproduction before collecting better telemetry.
- Stacking speculative fixes so nobody knows which cause mattered.
- Accepting a test/import failure as the regression signal without inspecting it.

## Done when

- Cause and correction have discriminating evidence, or the investigation ends with a precise
  unresolved hypothesis and the next observation needed.
- The final artifact and relevant checks support the claimed outcome.
- Temporary instrumentation and uncertainty are accounted for.

Use `flow-work` for implementation or `flow-triage` when production impact needs containment.
