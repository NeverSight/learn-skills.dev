---
name: gsd-orchestration
description: |
  Spec-driven development orchestration with context engineering for solo developers.
  Prevents context rot through fresh subagent contexts and atomic task execution.
  Use when: starting projects, planning features, executing development phases,
  or when user says "gsd", "plan", "new project", "execute phase".
  Triggers: /gsd init, /gsd plan, /gsd execute, /gsd status, /gsd verify
allowed-tools: Read Write Edit Task Skill Bash(git *)
---

# GSD Orchestration

> "The complexity is in the system, not in your workflow." — TÂCHES

## Philosophy

GSD solves **context rot** — the quality degradation as Claude fills its context window.
Each task runs in fresh context. Plans are atomic. Verification is built-in.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `gsd init` | New project: questions → research → requirements → roadmap |
| `gsd discuss [N]` | Capture decisions for phase N (NO CODE) |
| `gsd plan [N]` | Create atomic task plans for phase N |
| `gsd execute [N]` | Run tasks with fresh context per task |
| `gsd verify [N]` | Verify deliverables work as expected |
| `gsd status` | Current position and next action |
| `gsd complete [N]` | Archive phase, update state |

### Parallel Execution Commands (NEW)

| Command | Purpose |
|---------|---------|
| `gsd execute-all` | Execute all phases sequentially (background optional) |
| `gsd execute-parallel [N]` | Execute phase N with parallel tasks where possible |
| `gsd execute-overnight` | Full autopilot mode for unattended execution |
| `gsd check-conflicts [N]` | Analyze PLANs for file conflicts before parallel execution |
| `gsd status --live` | Live monitoring of running background agents |

## Core Workflow
```
gsd init → gsd discuss 1 → gsd plan 1 → gsd execute 1 → gsd verify 1 → gsd complete 1
                ↓
         gsd discuss 2 → gsd plan 2 → ...
```

For detailed workflow instructions, see [references/WORKFLOW.md](references/WORKFLOW.md).

## Project Structure
```
.gsd/
├── PROJECT.md         # Vision, goals, tech stack (always loaded)
├── REQUIREMENTS.md    # Scoped v1/v2 requirements
├── ROADMAP.md         # All phases with status
├── STATE.md           # Current position, blockers, decisions
└── phases/
    └── phase-N/
        ├── CONTEXT.md       # Decisions from discuss
        ├── ARCHITECTURE.md  # AI agent architecture (if AI phase)
        ├── RESEARCH.md      # Domain research (optional)
        ├── PLAN-1.md        # Atomic task plan
        ├── PLAN-2.md        # Atomic task plan
        └── SUMMARY.md       # What was built
```

## Context Engineering Rules

**Critical**: These rules prevent context rot.

1. **Fresh context per task** - Clear mental state between tasks
2. **Load only relevant files** - Never load all .gsd/ files at once
3. **Maximum 3 tasks per plan** - Keeps execution focused
4. **Size limits**:
   - PROJECT.md: ~500 lines max
   - Each PLAN.md: ~200 lines max
   - RESEARCH.md: ~1000 lines max

For context engineering principles, see [references/CONTEXT-ENGINEERING.md](references/CONTEXT-ENGINEERING.md).

## Configuration

This skill is configured for:
- **Project types**: Mixed (all types - adaptive based on project)
- **Verification**: Automated tests + manual checks
- **Planning depth**: Adaptive (adjust based on complexity)
- **Git workflow**: Atomic commits per task with conventional format

---

## Command Implementations

### `gsd init`

**Context to load**: Nothing - fresh start

**Process**:
1. Ask 5 focused questions: project description, core problem, target user, tech stack, success criteria
2. Optional: Spawn research subagent for complex domains
3. Generate: PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md

**Output**: "Project initialized. Run `gsd discuss 1` to begin."

---

### `gsd discuss [N]`

**Context to load**: PROJECT.md, ROADMAP.md (phase N), STATE.md (decisions)

**CRITICAL RULE**: NO CODE. NO FILE CREATION. Only conversation.

**Process**:
1. Summarize phase goal
2. **Offer agent-architect** for complex phases (see ARCHITECT-INTEGRATION.md)
3. Identify gray areas (visual, API, data, CLI decisions)
4. Ask clarifying questions until clear
5. Generate `.gsd/phases/phase-N/CONTEXT.md`

**Output format**:
```
## Phase [N] Discussion Complete

### Decisions Made:
- [Decision 1 with reasoning]
- [Decision 2 with reasoning]

### Out of Scope:
- [Deferred item with reason]

### Edge Cases Identified:
- [Edge case 1 and how to handle]
- [Edge case 2 and how to handle]

Ready to plan? Run: `gsd plan [N]`
```

**CONTEXT.md template**:
```markdown
# Phase [N] Context

## Decisions
- **[Topic]**: [Decision] - [Reasoning]
- **[Topic]**: [Decision] - [Reasoning]

## Out of Scope
- [Item] - [Why deferred/rejected]

## Edge Cases
- [Case] → [How to handle]

## Open Questions
- [Question that needs answering during planning]
```

---

### `gsd plan [N]`

**Context to load**:
- PROJECT.md (tech stack section)
- ROADMAP.md (phase N only)
- CONTEXT.md (if exists)
- **ARCHITECTURE.md (if exists from agent-architect)** ← Architectural decisions
- Previous phase SUMMARY.md (if exists)

**Process**:
1. **Research** (optional): Spawn researcher subagent for complex/unfamiliar domains

2. **Plan**: Break into 2-3 atomic tasks
   - **If ARCHITECTURE.md present** (agent-architect was used):
     - Use agent definitions (identity + task dispatch templates) → Task for implementing agents
     - Use tool specifications (built-in + custom MCP + external MCP) → Task for tools + MCP setup
     - Use orchestration pattern + guiding skill → Task for orchestration + interaction loop
     - Reference architecture decisions in all plans
     - Instruct prompts to be stored as markdown files in `prompts/` directory
   - **Standard phases**: Break phase into logical atomic tasks

3. **Validate**: Check plan completeness

**Generate**: Task plans using XML format.

For XML task templates, see [references/XML-TEMPLATES.md](references/XML-TEMPLATES.md).

**Output**: `.gsd/phases/phase-N/PLAN-1.md`, `PLAN-2.md`, etc.

**Planning depth** (adaptive based on configuration):
- **Quick**: Minimal specs, basic acceptance criteria
- **Standard**: Clear descriptions, testable criteria
- **Comprehensive**: Detailed specs, edge cases, examples
- **Adaptive**: Adjust based on task complexity

Each PLAN.md should be **executable** - another Claude instance can implement it without additional context.

---

### `gsd execute [N]`

**For EACH task in phase**:

**Context to load (fresh per task)**:
- PROJECT.md (tech stack only - ~50 lines)
- Current PLAN-X.md (full)
- Relevant source files only

**Process**:
1. Announce: "Starting Task [X]: [Name]"
2. Execute according to plan
3. Self-verify against acceptance criteria
4. Commit (if git workflow enabled):
   ```bash
   git add -A && git commit -m "type(phase-N): description

   - Detail 1
   - Detail 2

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```
5. Announce: "Task [X] complete - [summary]"
6. **Clear context**
7. Next task

**Commit types**: feat, fix, docs, refactor, test, chore

**Between tasks output**:
```
---
✓ Task 1 complete: [one-line summary]

Clearing context for Task 2...
Loading: PROJECT.md (tech), PLAN-2.md, [relevant files]

Starting Task 2: [Name]
---
```

**Important**: The "clearing context" announcement is a mental cue to actually reset context. Don't carry forward details from previous tasks.

---

### `gsd verify [N]`

**Context to load**:
- ROADMAP.md (phase N goals)
- All PLAN-X.md files for phase
- STATE.md

**Process**:
1. Extract testable deliverables from plans
2. For each deliverable:
   - **Automated**: Run test commands (based on configuration)
   - **Manual**: Provide verification instructions
3. Document results
4. If all pass → suggest `gsd complete [N]`
5. If any fail → identify failing task, suggest fix

**Verification based on configuration**:
- **Automated tests**: pytest, jest, npm test, go test, etc.
- **Manual checks**: curl commands, UI walkthrough, CLI usage

**Output**:
```
## Verification Results: Phase [N]

### Automated Tests
[✓ / ✗] Unit tests pass
[✓ / ✗] Integration tests pass
[✓ / ✗] Type checking clean
[✓ / ✗] Linter clean

### Manual Checks
- [ ] Check 1: [specific instruction]
- [ ] Check 2: [specific instruction]

### Overall Status
[PASS / FAIL with summary]

[If PASS]
All verification passed. Run `gsd complete [N]` to finalize.

[If FAIL]
Issues found:
- Task [X]: [specific failure]
Suggested action: Fix and re-verify
```

---

### `gsd status`

**Context to load**: STATE.md only

**Output**:
```
# GSD Status

**Project**: [Name]
**Phase**: [N] - [Phase Name]
**Status**: [Not Started / Planning / Executing / Verifying]

## Progress
[■■■□□□□□□□] 30% (3/10 phases)

## Completed Phases
- Phase 1: [Name] ✓
- Phase 2: [Name] ✓

## Current Phase Tasks
- [x] Task 1: [brief description]
- [ ] Task 2: [brief description] ← YOU ARE HERE
- [ ] Task 3: [brief description]

## Next Action
`gsd execute 3` (continue with task 2)

## Recent Decisions
- [Most recent decision from STATE.md]

## Blockers
[None / list of blockers]
```

---

### `gsd complete [N]`

**Process**:
1. Generate SUMMARY.md (deliverables, files, decisions, metrics)
2. Update STATE.md (mark complete, advance to N+1)
3. Update ROADMAP.md (mark requirements done)
4. Optional: Git tag if milestone complete

**Output**: "Phase [N] complete ✓. Run `gsd discuss [N+1]` for next phase."

---

## Parallel Execution Commands

GSD supports parallel execution using the **Fan-Out / Fan-In** pattern with automatic dependency detection.

**Critical Claude Code Constraints** (enforced by the platform):
- **No MCP tools in background agents** - Use built-in tools only (Read, Write, Edit, Bash, Glob, Grep)
- **No nested subagents** - Orchestrator spawns all agents, agents cannot delegate
- **Max ~10 concurrent agents** - Batch execution for larger phases

For complete documentation, see [references/PARALLEL-EXECUTION.md](references/PARALLEL-EXECUTION.md).
For detailed command reference, see [references/COMMANDS-REFERENCE.md](references/COMMANDS-REFERENCE.md).

### Quick Command Summary

| Command | Syntax | Purpose |
|---------|--------|---------|
| `execute-all` | `gsd execute-all [--from N] [--to M] [--background]` | Run all phases sequentially |
| `execute-parallel` | `gsd execute-parallel [N] [--max-agents N]` | Fan-Out/Fan-In parallel execution |
| `execute-overnight` | `gsd execute-overnight [--from N] [--parallel]` | Full autopilot for unattended execution |
| `check-conflicts` | `gsd check-conflicts [N] [--fix]` | Detect file conflicts before parallel |
| `status --live` | `gsd status --live [--interval N]` | Real-time monitoring of background agents |

### Overnight Execution Workflow

```bash
# Day: Plan all phases
gsd discuss 1 && gsd plan 1
gsd discuss 2 && gsd plan 2
# ... repeat for all phases

# Before sleep: Check conflicts and start
gsd check-conflicts 2 --fix
gsd execute-overnight --from 2 --parallel

# Next morning: Check results
gsd status
```

---

## Additional Commands

### `gsd add-phase`
Append a new phase to the roadmap interactively.

### `gsd pause`
Save current state for resuming later. Updates STATE.md with pause timestamp and context.

### `gsd resume`
Restore from paused state. Shows what was in progress and suggests next action.

### `gsd quick [description]`
Execute a quick ad-hoc task without full planning workflow. Useful for small fixes.

---

## Subagent Architecture

When spawning subagents, use minimal focused context:

| Subagent | Purpose | Context |
|----------|---------|---------|
| Researcher | Investigate domain | Query + PROJECT.md tech stack |
| Planner | Create task plans | Phase goal + CONTEXT.md |
| Checker | Validate plans | Plan + requirements |
| Executor | Implement tasks | Single PLAN.md + relevant files |

**Rule**: The orchestrator (main GSD) never does heavy lifting. It spawns, waits, integrates.

---

## Best Practices

1. **Fresh context per task** - Never accumulate across tasks
2. **No code during discuss** - Discuss is for requirements only
3. **Atomic means atomic** - If >15 min, split it
4. **Verify everything** - Even if it "looks right"
5. **Document decisions** - Future Claude instances need this
6. **Commit per task** - Git bisect finds exact failures
7. **Keep PROJECT.md lean** - Details go in REQUIREMENTS or phase docs
8. **One phase at a time** - Complete current before planning next
9. **Prompts as markdown files** - For agent projects, store prompts in `prompts/*.md`

For complete command reference, see [references/COMMANDS-REFERENCE.md](references/COMMANDS-REFERENCE.md).

---

## When to Use GSD

**Use GSD when**:
- Projects taking > 2 hours
- Multiple interconnected features
- Need to maintain context across sessions
- Want systematic verification
- Working on production code

**Skip GSD when**:
- Quick scripts (< 1 hour)
- Exploratory prototyping
- Single-file changes
- Emergency hotfixes
- You already have detailed specs

---

## Integrations

### agent-architect Integration

During `gsd discuss [N]`, GSD offers professional architectural design via **agent-architect** for complex phases. Creates `ARCHITECTURE.md` with 5-phase design process covering strategy, components, tools, orchestration, and production readiness.

See: [references/ARCHITECT-INTEGRATION.md](references/ARCHITECT-INTEGRATION.md)

### Domain Skill Integration

GSD auto-detects domain-specific needs (ML/DL, etc.) from PROJECT.md and offers specialized expertise during discuss/plan/execute phases.

See: [references/DOMAIN-INTEGRATION.md](references/DOMAIN-INTEGRATION.md)

---

## File Size Management

To keep context loading efficient:

| File | Target Lines | Max Lines |
|------|--------------|-----------|
| PROJECT.md | 200-300 | 500 |
| REQUIREMENTS.md | 500-800 | 1000 |
| ROADMAP.md | 300-400 | 500 |
| STATE.md | 100-150 | 200 |
| PLAN-X.md | 100-150 | 200 |
| CONTEXT.md | 150-200 | 300 |

If files exceed max, refactor or split into reference documents.
