---
name: add-plan-todos
description: "Create and maintain granular todos in the active execution plan to reduce omissions, sequencing errors, and misunderstandings. Use when drafting a plan, updating scope, starting implementation, or recovering from uncertainty/blockers."
---

Add and refine todos in the current plan before and during implementation.

## Workflow

1. Read the user request and current plan state.
2. Add missing todos so every phase is represented:
   - context gathering
   - implementation
   - validation/testing
   - final reporting
3. Split broad work into atomic todos that describe one action each.
4. Add guardrail todos for risky steps (assumptions, dependencies, migrations, irreversible actions).
5. Add explicit verification todos with concrete checks or commands.
6. Reorder todos so dependencies come first and only one todo is `in_progress`.
7. Mark covered todos `completed` and keep remaining work `pending`.

## Quality Bar

- Make each todo specific, testable, and observable.
- Avoid combined todos like "implement and test" in one step.
- Prefer adding one extra todo over leaving ambiguity.
- Update the plan whenever scope, constraints, or findings change.
