---
name: systematic-debugging
description: Use when investigating or fixing a bug, regression, failing or flaky test, build or deployment failure, performance problem, or incorrect output; also when asked why a failure occurred. Not for feature design, failure-free code explanation, or applying an already-verified correction without new uncertainty.
---

# Systematic Debugging

Find the cause before choosing a permanent fix. A fix should explain the evidence, not merely make one symptom disappear. Scale the investigation to the uncertainty: an obvious defect may need only a small reproduction and one check, not a full ceremony.

## Scope and Safety

- A request to explain a failure authorizes investigation, not edits, restarts, or deployment. Skip this workflow for failure-free code explanation or an already-verified correction unless new evidence contradicts it.
- Protect user work and diagnostic evidence. Do not reset state, delete artifacts, retry non-idempotent operations, or probe shared/production systems without authorization for that scope. Redact secrets and personal data; log only what distinguishes the hypotheses.
- During an incident, an authorized reversible mitigation can precede diagnosis. Preserve available evidence and check rollback/schema compatibility and persisted writes first. Report service restoration separately from root cause and permanent repair; do not block containment on a local reproduction.

## Investigate

1. **Observe and preserve the failure.** Read the relevant error and surrounding context, not just its final line. Record expected versus actual behavior, exact command or steps, inputs, version, and relevant environment. Establish the expectation from requirements, a contract, or a working case—not the suspect implementation. Reproduce safely before repair when possible. For intermittent or production-only failures, retain traces and conditions, bound observation by time or attempts, and say when reproduction is unavailable; absence on one run is not resolution.
2. **Locate the first divergence.** Check relevant recent code, configuration, dependency, schema, and environment changes; timing alone does not prove causation. Follow the failing data/control path and compare a like-for-like working case. Across components, inspect inputs and outputs at the boundaries using a shared request/job identifier. When invalid data appears deep in execution, read [root-cause-tracing](references/root-cause-tracing.md). For test pollution, preserve order and runner lifecycle rather than assuming an isolated test reproduces it; that guide explains the limits of [find-polluter.sh](scripts/find-polluter.sh).
3. **Test a falsifiable hypothesis.** State “I think X causes Y because Z; probe P should show Q, and result R would contradict it.” Choose the smallest safe probe that distinguishes plausible causes. Change one relevant variable at a time, keep useful output and exit status, and separate temporary experiments from a proposed repair. If the result contradicts the hypothesis, revise it; do not stack speculative patches.
4. **Repair the demonstrated cause.** Keep the correction scoped and preserve valid behavior. Do not swallow errors, weaken assertions, raise timeouts, or add broad fallbacks just to hide the failure. For timing races, read [condition-based-waiting](references/condition-based-waiting.md) before replacing a delay. For invalid input or a dangerous operation, read [defense-in-depth](references/defense-in-depth.md) to choose distinct safeguards—not validation at every internal layer. If fixes keep failing or exposing unrelated coupling, pause and reconsider the causal model or design with the user rather than forcing another patch.
5. **Verify the same behavior.** Prefer the project's existing test setup; add a regression check there when practical. With no test framework, use exact manual steps or a disposable check rather than scaffolding one unasked. Show that the check catches the original failure, then repeat it after the fix and exercise relevant adjacent valid/error paths. For intermittent failures, report the observed attempts and conditions without claiming elimination. Use applicable existing checks; do not repair unrelated baseline failures in passing. A green suite alone does not verify the original symptom.

Stop when the evidence supports the cause and the scoped correction has been checked, or when a named evidence/authorization gap prevents progress. Do not reread evidence or repeat checks whose possible outcomes cannot change the decision.

## Incorrect Output and Performance

No exception is required. For wrong reports or decisions, inspect recorded inputs, intermediate transformations, and outputs against an independently established expectation. Compare like cases and change one causal rule at a time; aggregate improvement must not hide a broken important case.

For performance, measure a baseline before changing code: same workload, environment, concurrency, and relevant cache state. Locate where time or resources are spent, then repeat that measurement after the change with correctness checks. A metric that does not improve is evidence to revisit the hypothesis or implementation, not by itself a reason to delete the concept. Name confounders and measurement limits.

## Handoff

Keep it proportionate: **symptom → evidence and cause (or current hypothesis) → correction or mitigation → checks and results → remaining limits**. Distinguish observed facts from inference, implemented from verified, and restored service from a permanent fix. If blocked, name the next evidence or permission needed, not a guessed cause.

Maintainers revising this skill can use [evaluation scenarios](references/evaluation-scenarios.md) to check metadata selection and application separately. They are not part of ordinary debugging. The optional dependency-free [waiting example](scripts/condition-based-waiting-example.ts) is linked from the timing guide; prefer existing project waiters over copying it.
