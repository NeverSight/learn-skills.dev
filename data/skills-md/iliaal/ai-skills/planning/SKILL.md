---
name: planning
description: >-
  Software implementation planning with file-based persistence (.plan/). Use when
  asked to plan, break down a feature, or starting complex tasks. Apply
  proactively before non-trivial coding.
---

# Planning

## Core Principle

```
Context window = RAM (volatile, limited)
Filesystem     = Disk (persistent, unlimited)
→ Anything important gets written to disk.
```

Planning tokens are cheaper than implementation tokens. Front-load thinking; scale effort to complexity.

## When to Plan

- **Full plan** (.plan/ directory): multi-file changes, new features, refactors, >5 tool calls
- **Flat list** (inline checklist): 3-5 file changes, clear scope, no research needed -- write a numbered task list in the conversation or a single progress.md, skip .plan/ scaffolding
- **Skip planning**: single-file edits, quick lookups, simple questions

## Planning Files

Scaffold the `.plan/` directory with pre-populated templates using [init-plan.sh](./scripts/init-plan.sh):

```bash
bash init-plan.sh "Feature Name"
```

This creates `.plan/` with `task_plan.md`, `findings.md`, and `progress.md` — each pre-populated with the correct structure. Also adds `.plan/` to `.gitignore`.

Planning files are ephemeral working state — do not commit them. If working on multiple features sequentially, old files are overwritten; the plan captures the current task only.

| File | Purpose | Update When |
|------|---------|-------------|
| `.plan/task_plan.md` | Phases, tasks, decisions, errors | After each phase |
| `.plan/findings.md` | Research, discoveries, code analysis | After any discovery |
| `.plan/progress.md` | Session log, test results, files changed | Throughout session |

## Plan Template

```markdown
# Plan: [Feature/Task Name]

## Approach
[1-3 sentences: what and why]

## Scope
- **In**: [what's included]
- **Out**: [what's explicitly excluded]

## Phase 1: [Name]
**Files**: [specific files, max 5-8 per phase]
**Tasks**:
- [ ] [Verb-first atomic task] — `path/to/file.ts`
- [ ] [Next task]
**Verify**: [specific test: "POST /api/users → 201", not "test feature"]
**Exit**: [clear done definition]

## Phase 2: [Name]
...

## Open Questions
- [Max 3, only truly blocking unknowns]
```

## Phase Sizing Rules

Every phase must be **context-safe**:
- Max 5-8 files touched
- Max 2 dependencies on other phases
- Fits in one 2-4 hour session (implementation + verification + fixes)
- If a phase violates these → split it

## Clarifying Questions

Scale to complexity:
- Small task: 0-1 questions, assume reasonable defaults
- Medium feature: 1-2 questions on critical unknowns
- Large project: 3-5 questions (auth, data model, integrations, scope)

Only ask if truly blocking. Make reasonable assumptions for everything else.

## Task Rules

- **Atomic**: one logical unit of work per task
- **Verb-first**: "Add...", "Create...", "Refactor...", "Verify..."
- **Concrete**: name specific files, endpoints, components
- **Ordered**: respect dependencies, sequential when needed
- **Verifiable**: include at least one validation task per phase

## Context Management Rules

| Situation | Action |
|-----------|--------|
| Starting new phase | Read .plan/task_plan.md (refresh goals in attention window) |
| After any discovery | Write to .plan/findings.md immediately |
| After completing phase | Update .plan/task_plan.md status, log to .plan/progress.md |
| After viewing image/PDF | Write findings NOW (multimodal content doesn't persist) |
| Resuming after gap | Read all planning files, run `git diff --stat` to reconcile actual vs planned state |
| Just wrote a file | Don't re-read it (still in context) |
| Error occurred | Log to .plan/task_plan.md, read relevant files for state |

## Error Protocol

```
ATTEMPT 1: Diagnose root cause → targeted fix
ATTEMPT 2: Different approach (different tool, library, method)
ATTEMPT 3: Question assumptions → search for solutions → update plan
AFTER 3 FAILURES: Escalate to user with what you tried
```

**Never repeat the exact same failing action.** Track attempts, mutate approach.

## Iterative Refinement

For complex projects, iterate on the plan before implementing:
1. Draft initial plan
2. Review for gaps, missing edge cases, architectural issues
3. Revise until suggestions become incremental
4. Only then start implementation

## 5-Question Context Check

If you can answer these, your planning is solid:

| Question | Source |
|----------|--------|
| Where am I? | Current phase in .plan/task_plan.md |
| Where am I going? | Remaining phases |
| What's the goal? | Approach section |
| What have I learned? | .plan/findings.md |
| What have I done? | .plan/progress.md |

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Start coding without a plan | Create .plan/task_plan.md first |
| State goals once and forget | Re-read plan before decisions |
| Hide errors and retry silently | Log errors, mutate approach |
| Keep everything in context | Write large content to files |
| Repeat failed actions | Track attempts in plan file |
| Create vague tasks ("improve X") | Concrete verb-first tasks with file paths |
| Plan phases with 12+ files | Split into 5-8 file chunks |
| Plan at 100% capacity | Budget for verification, fixes, and unknowns |

## Relationship to `workflows:plan`

This skill provides the **methodology** for planning (file persistence, phase sizing, context management). The `workflows:plan` command provides the **structured workflow** (research agents, issue templates, plan file creation).

Use this skill's principles during any planning activity. Use `workflows:plan` when creating a full feature plan with research and issue structure.

## Integration

- **This skill** applies as methodology during `workflows:plan` and `workflows:work`
- **Predecessor:** `brainstorming` — use first when requirements are ambiguous or multiple approaches exist
- **Prose quality:** `writing` — use to humanize plan language and remove AI slop from plan documents
- **End of chain:** `finishing-branch` (merge / PR / keep / discard)
- See `brainstorming` for the full workflow chain diagram
