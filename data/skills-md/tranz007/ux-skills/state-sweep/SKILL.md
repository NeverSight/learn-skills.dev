---
name: state-sweep
description: Find missing interface and service states such as loading, empty, partial, permission, timeout, stale data, validation, failure, interruption, and recovery. Use when a designer asks what states or edge cases are missing from a screen, component, journey, or feature.
license: MIT
metadata:
  author: Tranz007
  version: "0.2.1"
---

# State Sweep

Find behavior the happy-path design is hiding.

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

## Read the flow and system

Inspect the current design or implementation, the smallest relevant project context, relevant API or data behavior when available, design-system states, accessibility rules, and existing product patterns.

## Sweep by transition, not checklist

For each meaningful user action or system transition, ask what the user sees and can do:

- before data is available;
- while work is happening;
- when nothing exists;
- when only part succeeds;
- when input is invalid;
- when permission or eligibility blocks progress;
- when data changes or becomes stale;
- when the network, service, or dependency fails;
- when a session or operation times out;
- when the user interrupts, leaves, retries, or resumes;
- after success, including confirmation and persistence.

Also check focus, announcements, keyboard behavior, and recovery where dynamic state changes affect accessibility.

## Avoid state inflation

Do not create a separate visual state when the existing system behavior already handles the condition adequately. Reuse documented component states when possible.

## Output

Produce a concise state map. For each missing state, include the trigger, expected user-visible behavior, recovery path, and whether the design system already supports it.

Prioritize states whose absence can strand a user, lose work, create incorrect confidence, or produce inconsistent implementation.

## Contrast example

Bad:
> Consider loading, empty, error, success, offline, permission, timeout, disabled, hover, focus, validation, and edge-case states.

Good:
> After the user submits payment, the request can remain pending while the service responds. The current design leaves Submit available during that transition, so a second submission is possible. Add a pending state that prevents duplicate submission, preserves the entered data, communicates progress, and defines what happens if the request times out.

Why: the good response starts from a real transition and consequence instead of generating a generic state inventory.

## Examples

- "What states am I missing?"
- "State-sweep this checkout flow."
- "Engineering asked what happens when the API times out."
