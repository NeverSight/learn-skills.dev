---
name: groove-work-plan
description: "Research codebase, write concrete implementation plan. Use after brainstorming."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-work-plan

## Outcome

The codebase is researched for relevant patterns and constraints. A concrete implementation plan is written with ordered steps, file paths, and function names. Plan is captured as a task or doc.

## Acceptance Criteria

- Plan references actual code patterns found in the codebase (not assumptions)
- Steps are ordered and specific enough to execute without ambiguity
- File paths and function names are named where known
- Edge cases are identified and handling is specified
- Stage task created in backend: `YYYY-MM-DD, Plan`

## Constraints

- Read `tasks:` from `.groove/index.md` to determine backend
- Use Explore agent for codebase research before writing the plan
- Use template at `skills/groove-work-plan/templates/plan-doc.md` for doc output
- Warn if no prior brainstorm exists — ask user to confirm scope before proceeding
- Do not write code during plan — plan only
- Create stage task via `/groove-utilities-task-create` if `tasks != none` (title `YYYY-MM-DD, Plan`)
