---
name: sharpen-assess
license: MIT
description: Assess change exposure, judgment difficulty, and verification separately before recommending model capability and reasoning effort. Use for consequential engineering decisions or execution budgeting; advise without changing the user's settings.
---

# Sharpen Assess

Estimate what a wrong change could affect and what reasoning the work requires. Change risk and execution budget are separate decisions: an inexpensive edit can carry substantial risk.

## Inputs

- Required: a bounded task and available evidence about the affected behavior.
- Optional: caller risk taxonomy, model preferences, supported provider settings, budget constraints, and available validation.
- Default: advisory, read-only, provider-neutral output. Existing user choices remain in force.

## Procedure

1. Bound the work being assessed. Inspect affected interfaces, data, users, ownership boundaries, reversibility, and existing verification. Mark unknown exposure rather than assuming it is small.
2. Assess change risk from consequences and recoverability, not file count or model size. Use the caller's defined taxonomy; otherwise use low, moderate, high, critical, or unknown with a concrete reason. Use unknown when the available evidence cannot support a level.
3. Assess judgment difficulty and verification separately from exposure: novelty, unresolved contracts, alternatives, and whether checks cover the relevant failure modes. Unknown exposure needs evidence; a stronger model does not resolve it. Choose the least expensive capability that can perform the actual reasoning with the available verification.
   - `fast` — local, mechanical, reversible work whose verification is both cheap and complete.
   - `standard` — ordinary repository-grounded reasoning, multi-step drafting, conventional coding, and routine technical documentation.
   - `frontier` — unresolved architectural tradeoffs, difficult cross-domain judgment, or a consequential premise that needs expert analysis. A security or billing label alone does not require this tier; account for task difficulty and verified constraints.
4. Choose the reasoning intent: how hard that class should deliberate.
   - `glance` — take the direct path; minimal deliberation.
   - `measured` — ordinary, everyday deliberation.
   - `thorough` — work the alternatives and re-check the assumptions.
   - `exhaustive` — exhaust the search and re-verify the result.
5. Respect explicit user model or effort choices. Report a relevant mismatch and compensating verification without silently replacing the choice.
6. Name evidence that would raise or lower either assessment and the validation required regardless of model strength.

## Rules

- **Default the intent to the tier, then deviate with a stated reason.** `fast` pairs with `glance`, `standard` with `measured`, `frontier` with `thorough`; `exhaustive` is held for the highest-stakes work rather than assigned by default.
- **The two dials move independently.** Use a higher intent for unresolved reasoning, not for the number of mechanical checks. A brief expert call may need `frontier` with `glance`; a small task with genuinely difficult alternatives may need more deliberation. State the reasoning that requires the deviation.
- **An intent names a position on a ladder, not a vendor setting.** `glance` is the floor, `measured` the everyday default, `thorough` above it, `exhaustive` the ceiling of whatever the executing model exposes; a model missing an interior position takes the nearest one it has. Resolving an intent to a concrete setting belongs to the executor, and only from a supplied or currently verified catalog. Never invent a model, price, effort level, or automatic mapping.
- **Deliberation is not capability.** Raising the intent to cover judgment the chosen class cannot reach uses the wrong dial, and more deliberation is not more correct.
- **Risk beats size.** One destructive statement can be `critical` risk. A mechanical rename with reliable references and complete checks can stay `fast` with `glance`, regardless of file count. Execute exhaustive mechanical checks when needed; their volume alone is not a reason to increase deliberation.
- **Establish the platform before claiming its semantics.** Familiar syntax does not identify the runtime, its version, or its defaults. Without that evidence, state the verification objective and the missing input instead of prescribing a platform-specific command.
- **An alternative meets the same evidence standard as the change it replaces.** An inverse command does not establish operational reversibility; qualify disruption, recovery, cost, and consumer compatibility until their prerequisites are verified, and do not infer a legal obligation from the presence of user data.
- **Destructive execution needs its own gate.** State the required authorization and verified recovery path separately from the risk level, model choice, and proposed checks. Do not treat a suggested rollback command as recovery evidence.

## Output and stopping

Honor the caller's schema, including its enums. Without one, give a concise decision first, then include only the material details below:

- `change_risk`: level, concrete exposure, reversibility, and important unknowns.
- `execution_advice`: recommended capability tier and reasoning intent, rationale, explicit user constraints, and any provider mapping limitation.
- `verification`: the checks needed to justify completion, independent of the chosen model.
- `reassessment_triggers`: per dial, the evidence that would raise it and the evidence that would lower it.

When information is insufficient, qualify the assessment and identify the missing input. Stop after giving the advice; do not execute the task, launch a model, change configuration, or claim verification that has not run.

## Examples

- Normal: a broad mechanical rename with reliable references and complete tests may need modest capability even though it touches many files. Explain the remaining compatibility exposure separately.
- Edge: a one-line destructive migration can be high risk. If the user fixes the model choice, preserve it, state the risk and missing recovery evidence, and recommend checks rather than changing the model.

## Completion check

Risk and execution advice are distinct, every concrete provider claim has evidence, the user's settings were preserved, and stronger reasoning was not treated as a substitute for validation.
