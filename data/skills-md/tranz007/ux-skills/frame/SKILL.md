---
name: frame
description: Turn a feature request, stakeholder request, idea, complaint, or vague design assignment into a clear UX problem frame with user outcome, evidence, constraints, assumptions, unknowns, and success signals. Use before solutioning when the real problem or reason for the work is unclear.
license: MIT
metadata:
  author: Tranz007
  version: "0.2.1"
---

# Frame

Clarify what problem is worth solving before polishing a solution.

## Always

- **Context** — inspect what is already known before asking the user to repeat it. Use `.ux/INTENT.md` when product purpose or outcome can change the answer, and load only the additional project context the task needs.
- **User** — ground the work in the people affected, their goal, task, context, and available evidence. Do not invent user needs, behaviors, or personas.
- **Evidence** — keep known, inferred, assumed, unknown, and conflicted information distinct when the difference matters.
- **System** — prefer established product language, components, patterns, and rules before inventing new ones.
- **Clear** — lead with the useful point, use the minimum structure needed, and remove generic AI filler.
- **Trust** — never invent evidence, requirements, rationale, implementation status, or compliance.
- **Outcome** — for substantial multi-step work, keep intent active, use a small `.ux/STATE.md` only when continuity needs it, prioritize the highest-impact unresolved gap before polishing, and verify the actual experience against intent before declaring completion.

Do not recite these rules to the user unless one of them materially affects the answer.

Do not introduce research questions, personas, or discovery work when the user and task are already clear or the missing information would not materially change the work.

## Start with what exists

Read the smallest relevant `.ux/` context, requirements, research, analytics, support evidence, prior decisions, and the current request. Do not assume the request is the problem.

## Reframe

Identify:

- the triggering request or symptom;
- the user or actor affected;
- the outcome they are trying to achieve;
- evidence that the problem exists;
- constraints that are real versus merely inherited;
- assumptions being treated as requirements;
- important unknowns;
- what would change if the problem were actually improved.

When evidence is absent, say so. Do not manufacture a user need from a stakeholder preference.

## Challenge premature solution language

Translate "build X" into the underlying outcome when possible. Preserve the requested solution as an option, not as an unquestioned requirement.

If the request already has strong evidence and framing, do not force a workshop around it.

## Output

Produce a compact working frame the designer can act on. Prefer a few direct sections such as Problem, Evidence, Assumptions, Unknowns, Constraints, and Success. Include a recommended next move only when it is useful.

## Contrast example

Bad:
> Problem: Users need a saved-traveler feature so they can book faster.

Good:
> Request: Add saved travelers.
>
> Problem: Repeat bookers may be re-entering the same traveler information. We do not yet know how often that happens, whether it causes meaningful abandonment, or whether users want that information stored.
>
> Next move: Check booking analytics/support evidence before treating saved travelers as the solution.

Why: the good frame separates the requested feature from the underlying outcome and keeps missing evidence visible.

## Examples

- "We need an AI recommendation feature. Help me frame it."
- "The business wants saved travelers. What problem are we actually solving?"
- "Turn this ticket into a UX problem statement."
