---
name: content
description: Review and improve product UX content including labels, instructions, errors, empty states, confirmations, terminology, and content timing. Use when a designer asks whether UI copy is clear, consistent, accessible, actionable, appropriately human, or aligned with the product's established language.
license: MIT
metadata:
  author: Tranz007
  version: "0.2.1"
---

# Content

Treat words as part of the interaction, not decoration added after the design.

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

## Start with context

Read the relevant user goal and flow plus terminology, accessibility expectations, and product constraints from the smallest relevant project context when present. Check design-system content patterns and localization constraints when available.

## Review the job the content must do

Check for:

- clear action and outcome;
- terminology consistency;
- information shown at the moment it is needed;
- unnecessary instructions the interface could make obvious instead;
- labels that describe destinations or actions accurately;
- error language that explains what happened and how to recover;
- confirmation language proportional to consequence;
- technical or organizational jargon exposed to users;
- blame, ambiguity, coercion, or false reassurance;
- strings likely to fail with translation, expansion, dynamic values, or assistive technology.

## Prefer established product language

Use terms already established by the product and design system unless there is a reason to challenge them. If terminology is inconsistent across authoritative sources, flag the conflict instead of choosing silently.

## Rewrite carefully

Preserve factual meaning, legal requirements, and uncertainty. Do not make a message friendlier by making it less precise.

For high-consequence actions, clarity wins over personality.

## Output

Lead with content problems that change comprehension or behavior. Provide revised strings when useful, and explain only the decisions that are not obvious.

## Examples

- "Review the copy in this recovery flow."
- "Are these error messages actually useful?"
- "Make these labels clearer and consistent with our product language."
