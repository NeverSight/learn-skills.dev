---
name: system-fit
description: Decide whether a UX need should reuse, compose, extend, or create a design-system component or pattern. Use when a designer asks whether something needs a new component, how a design fits the current system, or what design-system contribution a feature should make.
license: MIT
metadata:
  author: Tranz007
  version: "0.2.1"
---

# System Fit

Prevent accidental design-system sprawl without forcing every problem into an existing component.

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

## Inspect the real system

Use `.ux/DESIGN-SYSTEM.md` when available and inspect authoritative sources such as Storybook, component packages, token definitions, design documentation, implementation examples, and contribution rules. Load other project context only when it can change the system-fit decision.

Do not assume Figma, Storybook, or code is the source of truth. Use the project's documented hierarchy or flag the ambiguity.

## Classify the fit

Prefer this order:

1. **Reuse** — an existing component or pattern already solves the need.
2. **Compose** — existing primitives solve it when combined in an established way.
3. **Extend** — an existing component needs a legitimate new state, behavior, variant, or documentation update.
4. **Create** — the need is meaningfully distinct and reusable enough to justify a new system asset.
5. **Feature-local** — the solution is too specific to become a shared system component.

Do not create a new component merely because the exact visual arrangement is new.

## Check the gap

If the existing system almost fits, identify the precise missing behavior: state, accessibility behavior, data scale, responsive behavior, content rule, interaction, or API.

Consider whether the gap is documentation rather than implementation.

## Output

Lead with the classification and recommendation. Name the existing assets involved, the gap, and any design-system contribution that should accompany the feature.

If the system source cannot be verified, make the recommendation conditional rather than pretending certainty.

## Contrast example

Bad:
> Create a new `SearchableStationPicker` component because the design system does not have that exact component today.

Good:
> **Compose.** The existing Autocomplete handles station search and the existing selection/chip pattern handles chosen values. The gap is not a new component; it is documented behavior for no-results, async loading, and keyboard selection. Add those states to the existing pattern before proposing a new system component.

Why: the good response identifies the actual missing behavior and prefers composition over component proliferation.

## Examples

- "Does this need a new component?"
- "Can we build this from what the design system already has?"
- "Should this state go back into Storybook?"
