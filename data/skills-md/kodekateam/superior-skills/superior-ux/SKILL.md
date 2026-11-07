---
name: superior-ux
description: Design or review product experiences through user goals, journeys, information architecture, task flows, interaction models, feedback, recovery, and cross-screen continuity. Use when the primary question is how users understand and complete a goal across steps or surfaces. Do not use for visual styling, implementation-only logic, or unsupported user-research claims.
---

# Superior UX

Make the user's path to a meaningful outcome clear, coherent, and recoverable. Base decisions on product evidence and observable behavior; never invent research, personas, or confidence that the project does not support.

## Establish the experience contract

Before proposing a flow, identify:

- the primary user, job, context, and entry point;
- the successful outcome and how the user recognizes it;
- required decisions, information, permissions, and constraints;
- existing routes, screens, terminology, analytics, research, support evidence, and product rules;
- interruptions, failures, alternate paths, and return visits that materially affect completion.

Separate observed evidence from assumptions. Ask for direction when competing assumptions would change who the product serves, what consent means, or what outcome counts as success. Otherwise, use the smallest reversible assumption and state it.

Read [references/journeys-task-flows-and-information-architecture.md](references/journeys-task-flows-and-information-architecture.md) when work spans multiple steps, screens, roles, entry points, or navigation levels.

## Shape the journey

- Start from the user's goal, not the current screen arrangement or the organization's internal structure.
- Make entry, orientation, next action, progress, completion, and re-entry understandable.
- Distinguish required steps from optional enrichment. Add a step only when it protects comprehension, consent, correctness, or recovery.
- Keep choices comparable and vocabulary stable across surfaces.
- Reveal complexity when it becomes relevant instead of hiding essential consequences or showing every option at once.
- Preserve user control: provide a safe way to go back, cancel, defer, correct, or resume when the product contract allows it.

## Define interaction and recovery

For each consequential action, define what the user can observe before, during, and after it. Cover pending, success, partial success, validation failure, dependency failure, cancellation, and retry only where they can occur.

Read [references/interaction-feedback-and-recovery.md](references/interaction-feedback-and-recovery.md) when the flow contains forms, asynchronous work, destructive actions, external handoffs, interruption, or multi-step state.

Do not optimize completion by concealing cost, consent, security consequences, destructive effects, or meaningful alternatives. Preserve entered data after expected failures when safe, and return the user to a useful state rather than a dead end.

## Evaluate with evidence

Walk through representative scenarios from entry to outcome, including at least one material failure or interruption. Check whether users can answer:

1. Where am I and what can I do here?
2. What will happen if I continue?
3. What is happening now?
4. Did the action succeed, and what should I do next?
5. How do I recover or leave safely?

Read [references/ux-evaluation-and-evidence.md](references/ux-evaluation-and-evidence.md) for heuristic reviews, evidence quality, scenario selection, and usability validation. Describe findings as risks or observed problems at the confidence level the evidence supports; do not present an expert walkthrough as user research.

## Coordinate ownership

Load only the skills whose contracts materially change:

- `superior-ui` for visual hierarchy, component composition, and interface implementation;
- `superior-logic` for domain behavior, state transitions, APIs, and persistence;
- `superior-responsive` for viewport-driven reflow and adaptive navigation;
- `superior-accessibility` for keyboard, focus, semantics, assistive technology, and inclusive interaction;
- `superior-copy` for labels, instructions, errors, and product voice;
- `superior-testing` for dedicated journey, contract, or regression test design;
- `superior-docs` when the resulting experience contract must remain durable.

Do not edit implementation when the user asks only for a journey, flow, or review. When implementation is requested, use this skill to govern the experience contract and the owning implementation skills to change code.

## Deliver

Report the current and proposed journey, changed decisions or information structure, interaction and recovery contract, supporting evidence, unresolved assumptions, and validation performed. Prefer a compact flow or state table when sequence or branching would be harder to understand in prose.
