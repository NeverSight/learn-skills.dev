---
name: feature-implementation-planner
description: Plan new product or engineering features into implementation-ready work for coding agents. Use when the user asks to scope a new feature, break work into phases or tickets, evaluate tradeoffs, define acceptance criteria, sequence delivery, or prepare an execution plan that agents can implement safely.
---

## Planning Workflow

Follow this sequence unless the user asks for a shorter output:

1. Define feature worktree + branch plan using `Feature Worktree Policy`.
2. Clarify objective and constraints.
3. Discover relevant system context from repository docs and code.
4. Select planning mode using `Practical Default Mode Selection`.
5. Define scope boundaries (in-scope, out-of-scope, assumptions).
6. Generate one primary implementation approach and optional alternatives.
7. Convert the selected approach into an agent-executable plan with right-sized tasks.
8. Present plan status as `Awaiting Confirmation`, including the task list and commit strategy.
9. Wait for explicit user confirmation before execution (worktree creation, code edits, tests, or commits).

## Feature Worktree Policy

- Treat the current checked-out branch as the source branch unless the user specifies another source.
- For new feature implementation work, create a dedicated worktree and feature branch before code changes.
- Preferred commands:
  - `git worktree add -b feature/<concise-feature-name> ../<repo>-<concise-feature-name> <source-branch>`
  - `cd ../<repo>-<concise-feature-name>`
- Use a short, informative kebab-case branch suffix (for example: `feature/profile-groups-redesign`).
- Include a one-line worktree summary near the top of the plan:
  - `Worktree Plan: create ../<repo>-<name> on feature/<name> from <current-branch>`
- If only planning is requested and no implementation follows in the same session, still include the branch name to be used at execution time.
- If worktree creation requires a path outside the current project directory, explicitly call out that user confirmation is required before execution.

## Parallel Feature Streams

- Worktree isolation is the default for every feature. When the user is running multiple features at the same time, recommend `worktree-parallel` to orchestrate separate worktrees cleanly.
- Add a one-line parallelization note in the plan when applicable:
  - `Parallel Plan: use worktree-parallel to create isolated worktrees per feature branch`
- Keep one feature branch per worktree to reduce cross-feature conflicts and simplify review/rollback.

## Plan Confirmation Gate

- After presenting a plan, explicitly ask for confirmation before execution (for example: `Confirm this plan for execution?`).
- Do not start implementation actions until the user gives clear approval (for example: `approved`, `proceed`, `yes, implement`).
- If the user requests changes, revise the plan and re-confirm.
- Confirmation must include the commit strategy choice (task-level commits recommended).

## Task Chunking Policy

- Break the feature into clear, relevant tasks that are independently reviewable and testable.
- Target meaningful chunks (typically 2-5 tasks per phase), not micro-steps and not broad "do everything" buckets.
- Each task should include objective, file/module targets, acceptance criteria, and validation commands.
- Prefer coherent vertical slices when possible so each task has visible user or system value.

## Implementation Commit Policy

- Recommend one commit per completed task to preserve traceability between plan and code history.
- Include a suggested commit message for every planned task.
- Tiny inseparable follow-up fixes MAY be folded into the same task commit.
- Do not create commits until the user confirms both execution and the commit strategy.
- During implementation, report task completion alongside the corresponding commit SHA.

## Practical Default Mode Selection

Choose planning mode using these defaults:

- Use `architecture-first` for auth, data model, routing, or infrastructure-impacting features.
- Use `implementation-tickets-first` for contained UI flows, isolated endpoints, and incremental enhancements.
- Use `hybrid` by default when uncertain: produce a short architecture section (maximum one page), then move to ticket-first execution steps.

Mode behavior:

- `architecture-first`: expand `Proposed Design` with boundaries, contracts, and data flow before ticket breakdown.
- `implementation-tickets-first`: keep `Proposed Design` concise and prioritize detailed, implementation-ready tickets.
- `hybrid`: keep architecture concise, then provide full ticketized phases.

## Context Discovery Rules

- Start from `docs/INDEX.md`, then open only docs relevant to the feature.
- Read `AGENTS.md` and task-specific prompt files before proposing implementation steps.
- Use `rg` to find existing modules, routes, APIs, schemas, and tests that match the feature.
- Prefer incremental changes that align with current architecture and conventions.

## Output Contract

Produce plans in a concrete format with explicit file targets:

1. `Feature Summary`
2. `Goals and Non-Goals`
3. `Current State`
4. `Proposed Design`
5. `Implementation Phases`
6. `Testing Strategy`
7. `Rollout and Safety`
8. `Risks and Mitigations`
9. `Open Questions`
10. `Execution Readiness`

For `Implementation Phases`, include:

- Phase name and objective
- Expected files/modules to change
- Ordered, right-sized tasks with acceptance criteria
- Dependencies/blockers
- Definition of done
- Suggested commit message per task

Also include a one-line `Planning Mode` declaration near the top of every plan.
Also include `Plan Status: Awaiting Confirmation` near the top of every plan.

## Quality Bar

- Prefer small, reversible steps over broad rewrites.
- Keep tasks right-sized: avoid overly granular noise and overly broad bundles.
- Call out assumptions explicitly when information is missing.
- Separate mandatory work from optional follow-ups.
- Include validation commands (lint, typecheck, unit/e2e) for each meaningful phase.
- Keep plans actionable enough that another agent can implement without reinterpretation.
- Never start execution until explicit user confirmation is received.

## References

- For a reusable plan skeleton, use `references/plan-template.md`.
- For discovery and risk checks, use `references/planning-checklist.md`.
