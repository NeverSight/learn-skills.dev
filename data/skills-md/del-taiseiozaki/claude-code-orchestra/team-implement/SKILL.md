---
name: team-implement
description: |
  Parallel implementation using Agent Teams. Spawns teammates per module/layer,
  each owning separate files to avoid conflicts. Uses shared task list with
  dependencies for autonomous coordination. Run after /startproject plan approval.
metadata:
  short-description: Parallel implementation with Agent Teams
---

# Team Implement

**Parallel implementation using Agent Teams. Executes based on the plan approved in `/startproject`.**

## Prerequisites

- `/startproject` is complete and the plan has been approved by the user
- Architecture is documented in `.claude/docs/DESIGN.md`
- Task list has been created

## Workflow

```
Step 1: Analyze Plan & Design Team
  Analyze task dependencies from the plan and determine team composition
    ↓
Step 2: Spawn Agent Team
  Launch Teammates per module/layer
    ↓
Step 3: Monitor & Coordinate
  Lead monitors, integrates, and manages quality
    ↓
Step 4: Integration & Verification
  After all tasks complete, run integration tests
```

---

## Step 1: Analyze Plan & Design Team

**Identify parallelizable workstreams from the task list.**

### Team Design Principles

1. **File ownership separation**: Each Teammate owns a different set of files
2. **Respect dependencies**: Dependent tasks go to the same Teammate or execute in dependency order
3. **Appropriate granularity**: Target 5-6 tasks per Teammate

### Common Team Patterns

**Pattern A: Module-Based (Recommended)**
```
Teammate 1: Module A (models, core logic)
Teammate 2: Module B (API, endpoints)
Teammate 3: Tests (unit + integration)
```

**Pattern B: Layer-Based**
```
Teammate 1: Data layer (models, DB)
Teammate 2: Business logic (services)
Teammate 3: Interface layer (API/CLI)
```

**Pattern C: Feature-Based**
```
Teammate 1: Feature X (all layers)
Teammate 2: Feature Y (all layers)
Teammate 3: Shared infrastructure
```

### Anti-patterns

- Two Teammates editing the same file → overwrite risk
- Too many tasks per Teammate → risk of prolonged idle time
- Overly complex dependencies → coordination costs outweigh benefits

---

## Step 2: Spawn Agent Team

**Launch the team based on the plan.**

```
Create an agent team for implementing: {feature}

Each teammate receives:
- Project Brief from CLAUDE.md
- Architecture from .claude/docs/DESIGN.md
- Library constraints from .claude/docs/libraries/
- Their specific task assignments

Spawn teammates:

1. **Implementer-{module}** for each module/workstream
   Prompt: "You are implementing {module} for project: {feature}.

   Read these files for context:
   - CLAUDE.md (project context)
   - .claude/docs/DESIGN.md (architecture)
   - .claude/docs/libraries/ (library constraints)

   Your assigned tasks:
   {task list for this teammate}

   Your file ownership:
   {list of files this teammate owns}

   Rules:
   - ONLY edit files in your ownership set
   - Follow existing codebase patterns
   - Write type hints on all functions
   - Run ruff check after each file change
   - Communicate with other teammates if you need interface changes

   When done with each task, mark it completed in the task list.

   IMPORTANT — Work Log:
   When ALL your assigned tasks are complete, write a work log file to:
     .claude/logs/agent-teams/{team-name}/{your-teammate-name}.md

   Use this format:
   # Work Log: {your-teammate-name}
   ## Summary
   (1-2 sentence summary of what you accomplished)
   ## Tasks Completed
   - [x] {task}: {brief description of what was done}
   ## Files Modified
   - `{file path}`: {what was changed and why}
   ## Key Decisions
   - {decision made during implementation and rationale}
   ## Communication with Teammates
   - → {recipient}: {summary of message sent}
   - ← {sender}: {summary of message received}
   ## Issues Encountered
   - {issue}: {how it was resolved}
   (If none, write 'None')
   "

2. **Tester** (optional but recommended)
   Prompt: "You are the Tester for project: {feature}.

   Read:
   - CLAUDE.md, .claude/docs/DESIGN.md
   - Existing test patterns in tests/

   Your tasks:
   - Write tests for each module as implementers complete them
   - Follow TDD where possible (write test stubs first)
   - Run uv run pytest after each test file
   - Report failing tests to the relevant implementer

   Test coverage target: 80%+

   IMPORTANT — Work Log:
   When ALL your assigned tasks are complete, write a work log file to:
     .claude/logs/agent-teams/{team-name}/{your-teammate-name}.md

   Use this format:
   # Work Log: {your-teammate-name}
   ## Summary
   (1-2 sentence summary of what you accomplished)
   ## Tasks Completed
   - [x] {task}: {brief description of what was done}
   ## Files Modified
   - `{file path}`: {what was changed and why}
   ## Key Decisions
   - {decision made during implementation and rationale}
   ## Communication with Teammates
   - → {recipient}: {summary of message sent}
   - ← {sender}: {summary of message received}
   ## Issues Encountered
   - {issue}: {how it was resolved}
   (If none, write 'None')
   "

Use delegate mode (Shift+Tab) to prevent Lead from implementing directly.
Wait for all teammates to complete their tasks.
```

---

## Step 3: Monitor & Coordinate

**Lead focuses on monitoring and integration, not implementing.**

### Monitoring Checklist

- [ ] Check task list progress (Ctrl+T)
- [ ] Review each Teammate's output (Shift+Up/Down)
- [ ] Verify no file conflicts
- [ ] Check if any Teammate is stuck

### Intervention Triggers

| Situation | Response |
|-----------|----------|
| Teammate not making progress for a long time | Send a message to check, re-instruct if needed |
| File conflict detected | Reassign file ownership |
| Tests keep failing | Send message to the relevant Implementer |
| Unexpected technical issue | Consult Codex (via subagent) |

### Quality Gates (via Hooks)

`TeammateIdle` hook and `TaskCompleted` hook automatically run quality checks:

- Lint check (ruff)
- Test execution (pytest)
- Type check (ty)

---

## Step 4: Integration & Verification

**After all tasks are complete, run integration verification.**

```bash
# All quality checks
uv run ruff check .
uv run ruff format --check .
uv run ty check src/
uv run pytest -v

# Or via poe
poe all
```

### Integration Report

```markdown
## Implementation Complete: {feature}

### Completed Tasks
- [x] {task 1}
- [x] {task 2}
...

### Quality Checks
- ruff: PASS / FAIL
- ty: PASS / FAIL
- pytest: PASS ({N} tests passed)
- coverage: {N}%

### Next Steps
Run `/team-review` for parallel review
```

### Cleanup

```
Clean up the team
```

---

## Tips

- **Delegate mode**: Use Shift+Tab to prevent Lead from implementing directly
- **Task granularity**: 5-6 tasks per Teammate is optimal
- **File conflict prevention**: Module-level ownership separation is the most important factor
- **Separate Tester**: Having a dedicated Tester separate from Implementers enables a TDD-like workflow
- **Cost awareness**: Each Teammate is an independent Claude instance (high token consumption)
