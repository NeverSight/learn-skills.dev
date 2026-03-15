---
name: rpi-implement-plan
description: Implement approved technical plans phase-by-phase, including code changes, verification, and progress updates directly in the plan file. Use this whenever the user asks to execute a plan, implement from a plan document, continue plan-based work, resume from checked/unchecked tasks, or "do phase 1/2/3" from an implementation plan in `rpi/plans/`, even if they do not explicitly name this skill.
---

# RPI Implement Plan

Use this skill to execute an approved implementation plan from `rpi/plans/` with disciplined progress tracking and validation.

## Initial Behavior

- If the user provides a plan path, begin immediately.
- If no plan path is provided, ask for one.

Use this prompt when no path is provided:

```text
I'm ready to implement the plan. Please share the plan file path (typically under `rpi/plans/`) and I’ll execute it phase-by-phase, run verification checks, and update progress checkboxes in the plan as work completes.
```

## Getting Started

When a plan path is provided:

1. Read the plan completely.
2. Check for existing `- [x]` items to detect prior progress.
3. Read all files referenced by the plan, fully.
4. Create a task list that mirrors phases and key checklist items.
5. Start implementation when requirements are clear.

## Implementation Philosophy

- Follow the plan's intent while adapting to current code reality.
- Complete each phase fully before moving to the next.
- Verify changes in context, not in isolation.
- Update plan checkboxes as items are completed.

If the codebase conflicts with the plan, pause and surface the mismatch clearly:

```text
Issue in Phase [N]:
Expected: [what the plan says]
Found: [actual situation]
Why this matters: [explanation]

How should I proceed?
```

## Working Process

### 1) Implement phase-by-phase

- Finish one phase before starting the next.
- Make all required code/file changes for that phase.
- Run the phase's automated checks before proceeding.
- Mark completed checklist items in the plan file like so: `- [x] `.

### 2) Verify after each phase

- Run success criteria checks from the plan (tests, lint, typecheck, build, or equivalent).
- If necessary to confirm changes were made correctly, you can write and run temporary scripts to verify the behavior; clean them up afterwards.
- Fix issues before advancing.
- Record progress in your task list and in the plan checkboxes.

### 3) Handle blockers pragmatically

- Re-read relevant code and requirements before escalating.
- Account for plan drift when code has changed since planning.
- Ask for guidance only after presenting a concrete mismatch and options.

## Resuming Existing Work

If the plan already has checked items:

- Treat checked work as completed by default.
- Resume from the first meaningful unchecked item.
- Re-verify prior work only if current behavior suggests a regression or inconsistency.

## Output Expectations

When reporting progress to the user:

- Summarize what was implemented in the current phase.
- List verification commands run and outcomes.
- Call out any deviations from plan and why.
- Link the updated plan path so progress is auditable.

## Quality Bar

- Prioritize working software over mechanical checkbox completion.
- Keep momentum while maintaining correctness.
- Do not skip verification gates defined by the plan.
- Keep plan checkboxes truthful and up to date.
