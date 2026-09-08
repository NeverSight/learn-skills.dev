---
name: rm-challenge
license: MIT
description: Test the consequential assumptions of a proposed development or architecture approach before expensive work. Use when a plan depends on an uncertain mechanism or premise; ordinary diff review and general brainstorming do not require this step.
---

# Assumption challenge

Identify the strongest supported reason a plan could fail and the smallest useful test of it. A plan with no supported blocking objection is an acceptable result.

## Inputs

- Required: the proposed approach and its intended outcome.
- Optional: constraints, existing evidence, alternatives already considered, and experiment budget.
- Default: read-only analysis. Proposing an experiment does not authorize its external effects or expense.

## Procedure

1. State the assumption whose failure would materially undermine the outcome. Separate it from preferences about implementation style.
2. Inspect evidence for and against it, on whichever of these the plan actually exposes:
   - `unverified premise` — the plan states something as established that no available evidence establishes
   - `self-told story` — an explanation the plan gives for its own past or design is treated as ground truth
   - `analogy read as identity` — a mechanism is assumed to carry across domains whose structures differ
   - `borrowed result` — the argument leans on an outcome that has not been obtained yet
   - `principle stated, opposite built` — the plan names a constraint and then does the reverse of it
   - `closed-loop check` — the validation draws on the same source or assumption it is supposed to test, so nothing independent enters
   - `sample and multiplicity` — the planned sample cannot detect a real effect, or a threshold that any one of many uncorrected comparisons would cross
3. Choose the most consequential supported objection. Preserve any other independently blocking issue instead of disguising unrelated failures as one root cause. Do not manufacture an objection to fill the output.
4. If the evidence already settles the assumption, explain why; a decisive contract does not require a live experiment to reconfirm it. When the caller requests a test or evidence remains inconclusive, specify the smallest informative test: input, action, observation, and the result that would support or reject the assumption. State what a simulation or finite sample cannot establish, without inventing a probability or required trial count.
5. Execute only a permitted, useful check within the existing scope. Otherwise return the proposed test with its required inputs or authorization. Distinguish observed results from predictions.

## Rules

- **One root, and only the genuinely separate ones beside it.** Where several axes fire on the same underlying cause, report the objection that renders the rest irrelevant once it holds, together with its cheapest falsification. An issue that would block the outcome on its own is a second finding, not padding — the test is whether fixing the root also removes it.
- **Examine the plan; do not redesign it.** Producing a better approach is separate work. The result here is the objection and the observation that would settle it.
- **Check the inverted-principle axis explicitly.** It is the one most often missed, because the plan's own stated constraint reads as evidence that the constraint was honored.
- **Prefer a deterministic local counterexample.** Use the supplied interfaces or test doubles consistent with their contracts, and specify the action sequence, controlled condition, and observable assertion. Require external infrastructure only when local evidence cannot answer the requested question.
- **Separate what was observed from what explains it.** A result compatible with several mechanisms establishes none of them; name the additional observation or control that would distinguish them.
- **A remedy earns the same scrutiny, and absence is not yet an outcome.** State the guarantees a suggested fix needs and whether they are established. While earlier work may still complete or become visible, an observation of absence is provisional, so keep a remedy conditional until its coordination and recovery guarantees are verified.

## Output and stopping

Use the caller's schema. Otherwise provide the assumption, supported objection or "no supported blocking objection," evidence, proposed test, acceptance criterion, and result if executed. Note material uncertainty.

Stop after a useful test resolves the assumption or the next step needs unavailable evidence, budget, or authority. If no cheaper informative test exists, explain that limitation rather than proposing a ceremonial check. This procedure does not authorize implementing the plan, modifying provider settings, or running a deployment.

## Examples

- Normal: a plan assumes an index removes a query bottleneck. Propose inspecting the query plan against representative data before rewriting the service, with the relevant scan and latency observations named.
- Edge: a refactor's claimed risk is already covered by a passing contract test and unchanged call paths. Report that the objection is unsupported; do not invent a different defect merely to reject the plan.

## Completion check

The objection could affect the outcome, contrary evidence was considered, and the experiment has an observable decision criterion. Unrun experiments are not reported as passed.
