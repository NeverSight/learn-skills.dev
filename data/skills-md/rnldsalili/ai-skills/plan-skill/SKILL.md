---
name: plan-skill
description: Create read-only, inspection-first execution plans and analysis without modifying files or running state-changing commands. Use when the user asks for a plan, a checklist, scoping guidance, a strategy, or wants a proposal before any implementation work.
---

# Plan Skill

## Core rules

- Stay read-only: do not create, modify, delete, rename, or move any files.
- Avoid state-changing tools and commands: do not use write/edit/apply_patch, do not run installs, tests, builds, migrations, or git actions that change state.
- Use only read-only inspection: prefer Read/Glob/Grep; use Bash only for safe listing or status (ls, git status, git diff, git log).
- Inspect current code patterns before drafting the plan; default to existing conventions.
- If up-to-date or niche info is needed, do lightweight web research (read-only) and summarize key points.
- If the user asks to implement changes, stop and request a switch to build mode before doing any edits.

## Workflow

1. Restate the goal and scope in one sentence.
2. Inspect the repo first with read-only tools; identify existing patterns and conventions.
3. Identify impacted areas and call out unknowns.
4. If needed, do quick online research and summarize relevant findings.
5. Draft a minimal, step-by-step plan in execution order.
6. Enumerate files to touch (paths only, no edits).
7. Provide commands to run later (do not execute).
8. Note risks and assumptions.
9. Ask a single blocking question only if required; otherwise state the chosen default.

## Output format

Observations (optional)
- [existing pattern or convention]

Plan
- [Step 1]
- [Step 2]

Files to touch
- path/to/file.ext

Commands to run later
- command --flags

Risks/assumptions
- [risk or assumption]

Open question (omit if none)
- [single blocking question]
