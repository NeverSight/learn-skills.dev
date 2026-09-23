---
name: critique
description: Review and compare UX designs, flows, prototypes, specifications, or implementations against user goals, evidence, interaction behavior, accessibility, design-system fit, content, and engineering intent. Use when a designer asks for critique, comparison, tough feedback, review before approval, or wants to check whether implementation preserved the intended experience.
license: MIT
metadata:
  author: Tranz007
  version: "0.2.1"
---

# Critique

Review the work against its context and intent rather than personal taste.

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

## Establish the basis

Inspect the artifact plus the smallest relevant `.ux/` context, evidence, design-system patterns, accessibility rules, known constraints, and prior decisions. If reviewing implementation, inspect the actual code/diff as well as the intended UX source.

If the goal is unclear, state any cautious inference before critiquing against it, or ask only if the critique would otherwise be misleading.

## Review through relevant lenses

Use only lenses that matter to this work:

- user goal and task clarity;
- evidence and unsupported assumptions;
- information hierarchy and cognitive effort;
- interaction behavior, branches, interruption, and recovery;
- state completeness;
- content and terminology;
- accessibility and inclusive use;
- consistency and design-system fit;
- engineering or service dependencies;
- trust, privacy, or consequence where relevant.

## Compare when needed

When reviewing multiple options, derive the important decision criteria from the actual problem and evaluate each option against the same criteria. Do not turn the comparison into a beauty contest. "Neither" is a valid recommendation.

## Review implementation drift

When the artifact is code or a PR, look for UX behavior that changed or disappeared: states, recovery, persistence, content, design-system usage, focus/keyboard behavior, or acceptance intent.

A diff does not prove runtime behavior. Say what still needs to be verified rather than presenting inference as fact.

## Prioritize findings

Lead with issues likely to cause failure, exclusion, loss, misunderstanding, or significant implementation drift. Put polish later.

Point to the behavior or element, explain why it matters, and recommend a direction. Avoid vague comments such as "improve hierarchy" without saying what is wrong.

When the work is strong, spend fewer words validating it. Do not manufacture issues.

## Guardrails

Do not claim accessibility compliance from visual or code inspection alone. Do not invent research findings. Do not prefer novelty over an established system pattern without evidence.

## Contrast example

Bad:
> Improve the visual hierarchy, make the CTA more prominent, simplify the form, and consider accessibility.

Good:
> The primary action appears available before the required travel date is valid. That creates a false affordance: the user can try to continue before the form is ready. Keep the action unavailable until the date is valid, or surface validation early enough that the required fix is obvious before submit.

Why: the good critique identifies a specific behavior, explains the consequence, and gives a direction instead of offering generic design advice.

## Examples

- "Review this before I show engineering."
- "Give me a tough critique."
- "Compare these two approaches against the user problem."
- "Review this PR against the intended experience."
