---
name: ralph-iteration
description: Run one Ralph-style planning or build iteration from project-supplied prompts, plans, specs, and backpressure files. Use when the user asks to Ralph, run a Ralph loop, bootstrap Ralph files, create/update an implementation plan, or execute the next item from an existing Ralph plan.
---

# Ralph Loop

## Quick Start

Ralph is a dumb outer loop:

```text
load prompt + requirements + plan + backpressure
choose one task
implement or plan
run backpressure until the work is proven or blocked
update IMPLEMENTATION_PLAN.md
commit when building if the active workflow allows it
exit so the next loop starts fresh
```

Backpressure is not optional. Without proving checks, Ralph is just an agent following a todo list.

## Inputs

Ralph needs four things:

- a prompt;
- requirements;
- `IMPLEMENTATION_PLAN.md`;
- this skill's `AGENTS.md` as Ralph loop backpressure.

Use the files the current project points you at. If any input is missing, stop.

Use `templates/` only when the user asks to set up Ralph files.

## Required Input

There are two Ralph modes:

- `plan`: create or refresh `IMPLEMENTATION_PLAN.md`.
- `build`: execute the next item from `IMPLEMENTATION_PLAN.md`.

Use the requested mode when the user names `plan` or `build`. Otherwise default to `build` when `IMPLEMENTATION_PLAN.md` exists, and `plan` when it does not or is stale.

For `plan`, a project goal and requirements are required.

For `build`, an `IMPLEMENTATION_PLAN.md` is required.

If required input is missing, do not improvise a substitute. Report the missing file or decision and stop.

## Doctrine

- Ralph's useful state lives on disk, not chat.
- Ralph loop backpressure lives in this skill's `AGENTS.md`: prove or block, update `IMPLEMENTATION_PLAN.md`, and exit after one iteration.
- `IMPLEMENTATION_PLAN.md` is disposable. Regenerate it when stale or wrong.
- The main agent is the scheduler. Use parallel subagents for reads/searches when available.
- Search before building. Do not assume missing functionality is missing.
- See this skill's `AGENTS.md` for the generic backpressure rule.
- Let Ralph Ralph. Avoid over-prescribing implementation details in the plan.
- Keep `AGENTS.md` operational only. Progress belongs in `IMPLEMENTATION_PLAN.md`.

See `REFERENCE.md` for the upstream playbook shape and `templates/` for bootstrap files.

## Plan Mode

Use this when no plan exists or the plan is stale.

1. Study the requirements, existing source, and `IMPLEMENTATION_PLAN.md` if present.
2. Compare requirements against the code.
3. Create or update `IMPLEMENTATION_PLAN.md` as the prioritized list of remaining work.
4. Do not implement.
5. Do not commit unless the workflow explicitly asks for planning commits.

## Build Mode

Use this when `IMPLEMENTATION_PLAN.md` exists.

1. Study the prompt, requirements, backpressure, and `IMPLEMENTATION_PLAN.md`.
2. Choose the most important remaining task.
3. Search the codebase first.
4. Implement the task completely.
5. Apply Ralph loop backpressure, then run the project checks that prove the changed surface.
6. Update `IMPLEMENTATION_PLAN.md` with discoveries, completed work, and unresolved bugs.
7. When checks pass, commit the increment if the workflow allows commits.
8. Stop after one task so the next loop starts with fresh context.

## Output

Report one state:

- `planned`: `IMPLEMENTATION_PLAN.md` was created or updated.
- `task-done`: one build task was implemented, checked, and the plan was updated.
- `blocked`: required input is missing, checks cannot pass, or the next task needs human judgment.
- `done`: the implementation plan has no remaining work.

## Hard Stops

- Do not implement in plan mode.
- Do not build without an `IMPLEMENTATION_PLAN.md`.
- Do not claim progress without backpressure passing or a recorded blocker.
- Do not treat unrelated failing checks as invisible; fix or record them in the plan.
- Do not bloat `AGENTS.md` with status or progress.
- Use the active project's git policy. Upstream Ralph commonly commits and may push/tag through the loop script; adapters may narrow that.
