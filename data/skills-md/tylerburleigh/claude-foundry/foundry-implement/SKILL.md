---
name: foundry-implement
description: Task implementation skill for spec-driven workflows. Reads specifications, identifies next actionable tasks, and creates detailed execution plans. Use when ready to implement a task from an existing spec - bridges the gap between planning and coding.
---

# SDD-Implement: Concise Playbook

## Overview

- **Purpose:** Task execution workflow - select tasks, plan implementation, and track progress within an active spec.
- **Scope:** Single-task execution with user approval at key checkpoints.
- **Entry:** Invoked via skill system after spec has been identified.

### Flow

> `[x?]`=decision · `(GATE)`=user approval · `→`=sequence · `↻`=loop · `§`=section ref

```
- **Entry** → LoadConfig → `environment action="get-config"` → Merge config → ModeDispatch
  - [--parallel?] → §ParallelMode
  - [--delegate?] → §DelegatedMode
  - [--auto?] → Skip user gates
  - Task selection → [selection mode?]
    - [interactive?] → SelectTask
    - [recommend?] → `task action="prepare"` → ShowRecommendation
    - [browse?] → `task action="query"` → (GATE: task selection)
  - Type dispatch → [type?]
    - [verify?] → §VerifyWorkflow
    - [task?] → DeepDive
      - `task action="prepare"` → ExtractContext
      - DraftPlan → (GATE: approve plan)
        - [approved] → PreImpl
        - [changes] → ↻ back to DraftPlan
        - [defer] → **Exit**
      - PreImpl → LSP analysis → Explore subagent
      - `task action="update-status" status="in_progress"` → **Implement**
      - PostImpl → `task action="complete"` → Journal (auto)
      - [success?] → SurfaceNext → `task action="prepare"` → ShowNextTask → (GATE: continue?)
        - [yes] → ↻ back to SelectTask
        - [else] → **Exit**
      - [blocked?] → HandleBlocker → `task action="block"` → (GATE: alternatives)
        - [add-dep?] → `task action="add-dependency"`
        - [add-requirement?] → `task action="add-requirement"`
        - [resolve] → ↻ back to **Implement**
        - [skip] → SurfaceNext
```

§VerifyWorkflow → see references/verification.md

§ParallelMode flow:

```
- **Entry** → `task action="prepare-batch"` → IdentifyEligible
  - [conflicts?] → ExcludeConflicting
  - `task action="start-batch"` → SpawnSubagents
  - For each subagent → Task(general-purpose, run_in_background=true)
  - TaskOutput(block=true) → CollectResults
  - `task action="complete-batch"` → AggregateResults
  - [failures?] → HandlePartialFailure
  - [more batches?] → ↻ back to prepare-batch
  - [else] → **Exit**
```

> Flow notation: see [dev_docs/flow-notation.md](../../dev_docs/flow-notation.md)

---

## MCP Tooling

This skill interacts solely with the Foundry MCP server (`foundry-mcp`). Tools use the router+action pattern: `mcp__plugin_foundry_foundry-mcp__<router>` with `action="<action>"`.

| Router | Key Actions |
|--------|-------------|
| `task` | `prepare`, `query`, `info`, `start`, `complete`, `update-status`, `block`, `unblock`, `add-dependency`, `add-requirement`, `session`, `session-step`, `session-events`, `fix-verification-types`, `gate-waiver`, `prepare-batch`, `start-batch`, `complete-batch`, `reset-batch` |
| `research` | `node-status`, `node-execute`, `node-record`, `node-findings` |
| `journal` | `add`, `list` |
| `lifecycle` | `activate`, `move`, `complete` |
| `spec` | `find`, `list` |
| `journal` | `add`, `list` |
| `environment` | `get-config` |

**Critical Rules:**
- The agent never invokes the CLI directly
- Stay inside the repo root, avoid chained shell commands
- NEVER read raw spec JSON outside of MCP helpers

---

## Execution Modes

Four flags control execution behavior. Defaults loaded via `environment action="get-config"`, CLI flags override.

**Config Loading:** At entry, call the environment tool to read configuration from `foundry-mcp.toml`. Returns both `implement` (mode flags + model) and `git` (commit cadence, auto_push) sections. If the config file is missing or section not found, use defaults (all false for implement, model=small, auto_push=false).

| Flag | Effect |
|------|--------|
| `--auto` | Skip prompts between tasks (autonomous execution) |
| `--delegate` | Use subagent(s) for implementation |
| `--parallel` | Run subagents concurrently (implies `--delegate`) |
| `--model <small\|medium\|large>` | Model size for delegated tasks (default: small) |

Model sizes map to Claude tiers: small = haiku, medium = sonnet, large = opus.

**Resulting combinations:**

| Flags | Subagent | Concurrent | Prompts | Description |
|-------|----------|------------|---------|-------------|
| (none) | ❌ | ❌ | ✅ | Interactive, inline |
| `--auto` | ❌ | ❌ | ❌ | Autonomous, inline |
| `--delegate` | ✅ | ❌ | ✅ | Interactive, sequential subagent |
| `--auto --delegate` | ✅ | ❌ | ❌ | Autonomous, sequential subagent |
| `--delegate --parallel` | ✅ | ✅ | ✅ | Interactive, concurrent subagents |
| `--auto --delegate --parallel` | ✅ | ✅ | ❌ | Autonomous, concurrent subagents |

### Autonomous Behavior (`--auto`)

Executes tasks continuously without user prompts between each task. Session state persists across `/clear` boundaries.

**Key behaviors:**
- Auto-selects recommended tasks via `task action="prepare"`
- Skips plan approval gates (uses generated plan)
- Auto-continues after task completion
- Pauses on: context >= 85%, 3+ consecutive errors, blocked tasks, task limit

**Session tracking:** Uses canonical `task action="session"` with commands: `start`, `status`, `pause`, `resume`, `end`. Step orchestration via `task action="session-step"` with commands: `next`, `report`, `replay`, `heartbeat`.

> Full documentation: [references/autonomous-mode.md](./references/autonomous-mode.md)
> Session management: [references/session-management.md](./references/session-management.md)

### Parallel Behavior (`--delegate --parallel`)

Spawns multiple subagents to execute independent tasks concurrently. File-path conflicts are detected and excluded.

**Key behaviors:**
- Uses `task action="prepare-batch"` to identify eligible tasks
- Excludes tasks with conflicting `file_path` metadata
- Spawns `Task(general-purpose, run_in_background=true)` per task
- Collects results via `TaskOutput` and aggregates with `complete-batch`
- Handles partial failures (successful tasks complete, failed tasks remain in_progress)

**Batch actions:** `prepare-batch`, `start-batch`, `complete-batch`, `reset-batch`

**CRITICAL when using `--parallel`:** Read [references/parallel-mode.md](./references/parallel-mode.md) before proceeding. Contains required JSON formats for batch operations.

### Delegation Behavior (`--delegate`)

Uses subagent(s) for implementation. Fresh context per task while main agent handles orchestration.

**Key behaviors:**
- Spawns `Task(general-purpose, model={model})` for each task implementation
- Model defaults to `small` (haiku); override with `--model medium` (sonnet) or `--model large` (opus)
- Sequential by default; concurrent with `--parallel`
- Main agent handles task lifecycle (status updates, journaling)
- With `--auto`: skips user gates; without: preserves all gates

**Subagent receives:**
- Task details, file path, acceptance criteria
- Context from main agent (LSP findings, explore results, previous sibling)
- Verification scope guidance
- Constraint: subagent does NOT update spec status or write journals

**When to use:**
- Large file changes where you want oversight
- Complex tasks where fresh context helps
- Long sessions to preserve main agent context

> See also: [references/subagent-patterns.md](./references/subagent-patterns.md)

---

## CRITICAL: Global Requirements

### Config Loading (NEVER SKIP)

**At entry, IMMEDIATELY call the environment tool before any other action:**

```bash
mcp__plugin_foundry_foundry-mcp__environment action="get-config"
```

This returns:
- `implement` section: mode flags (`auto`, `delegate`, `parallel`) + `model`
- `git` section: `commit_cadence`, `auto_push`

**Merge with CLI flags:** CLI flags override config values. If config missing, use defaults (all flags false, model=small, auto_push=false).

**Why mandatory:** Without this call, the skill may use incorrect defaults for autonomous mode, delegation, and commit behavior.

### Spec Reading Rules (NEVER VIOLATE)

The skill **only** interacts with specs via MCP tools:
- `mcp__plugin_foundry_foundry-mcp__task action="prepare"`
- `mcp__plugin_foundry_foundry-mcp__task action="info"`
- `mcp__plugin_foundry_foundry-mcp__spec action="find"`
- `mcp__plugin_foundry_foundry-mcp__task action="query"`

Direct JSON access (`Read()`, `cat`, `jq`, `grep`, etc.) is prohibited.

### User Interaction Requirements

**Gate key decisions with `AskUserQuestion` (MANDATORY):**
- Spec selection (when multiple available)
- Task selection (recommended vs alternatives)
- Plan approval (before implementation)
- Blocker handling (alternative tasks or resolve)
- Completion verification (for verify tasks)
- **Continuation after task completion** (when context < 85% and more tasks remain)

**Anti-Pattern:** Never use text-based numbered lists. Always use `AskUserQuestion` for structured choices.

### Anti-Recursion Rule (NEVER VIOLATE)

This skill must NEVER invoke itself or `Skill(foundry-implement)`. The only valid callers are:
- The skill system (entry point)
- Direct user invocation

If you find yourself about to call `Skill(foundry-implement)` from within this skill, **STOP** and proceed with the workflow instead. The skill handles the complete task lifecycle - there is no need to re-invoke it.

> For detailed context gathering patterns, see `references/context-gathering.md`
> For agent delegation patterns (when to use foundry-spec), see `references/agent-delegation.md`

---

## Task Workflow

Execute one task at a time with explicit user approval.

**Assumption:** The active spec has been identified (either via skill auto-discovery or passed during invocation).

### Select Task

- **Recommendation path**: `mcp__plugin_foundry_foundry-mcp__task action="prepare"` -> surface task id, file, complexity, blockers
- **Browsing path**: Use `mcp__plugin_foundry_foundry-mcp__task action="query"` -> present shortlist via `AskUserQuestion`

### Task Type Dispatch

After selecting a task, check its type to determine the workflow path.

**Check task type** from the `task action="prepare"` response or via `mcp__plugin_foundry_foundry-mcp__task action="info"`:

| Task Type | Workflow Path |
|-----------|---------------|
| `type: "verify"` | Go to **Verification Task Workflow** |
| `type: "research"` | Go to **Research Node Workflow** |
| `type: "task"` (default) | Continue to **Deep Dive & Plan Approval** |

**CRITICAL:** Verification and research tasks must NOT go through the implementation workflow. They require MCP tool invocation, not code changes.

### Deep Dive & Plan Approval (Implementation Tasks Only)

**Note:** This section is for `type: "task"` only. Verification tasks (`type: "verify"`) use the Verification Task Workflow.

Invoke `mcp__plugin_foundry_foundry-mcp__task action="prepare"` with the target `spec_id`. The response contains:
- `task_data`: title, metadata, instructions
- `dependencies`: blocking status (can_start, blocked_by list)
- `context`: previous sibling, parent task, phase, sibling files, journal, dependencies

Treat `context` as the authoritative source. Only fall back to `mcp__plugin_foundry_foundry-mcp__task action="info"` when the spec explicitly requires absent data.

> For context field details and JSON structure, see `references/context-structure.md`

**Draft execution plan:**
1. Confirm previous edits in `context.sibling_files`
2. Align deliverables with `context.parent_task`
3. Call out open risks via `context.phase`
4. Reference `context.previous_sibling.summary` for continuity

**Present plan via `AskUserQuestion`:**
- Options: "Approve & Start", "Request Changes", "More Details", "Defer"

### Subagent Guidance (Pre-Implementation Exploration)

Before implementing, use Claude Code's built-in subagents for efficient codebase exploration:

| Scenario | Subagent | Thoroughness |
|----------|----------|--------------|
| Find related files/patterns | Explore | medium |
| Understand unfamiliar code areas | Explore | very thorough |
| Complex multi-file investigation | general-purpose | N/A |

**Example invocation:**
```
Use the Explore agent (medium thoroughness) to find:
- Existing implementations of similar patterns
- Test files for the target module
- Related documentation that may need updates
```

**Benefits of subagent exploration:**
- Prevents context bloat in main conversation
- Small model size (haiku) is faster for search operations
- Returns focused results for detailed analysis
- Keeps main context available for implementation

> For more subagent patterns including autonomous mode usage, see `references/subagent-patterns.md`

### LSP Dependency Analysis

Before implementing, use LSP tools to verify dependencies and preview impact:

1. **Verify dependencies exist**: Use `goToDefinition` on symbols the task modifies
2. **Preview impact**: Use `findReferences` to identify all affected files and call sites
3. **Include in plan**: Surface LSP findings (usage count, affected files, test coverage) in plan approval
4. **Fallback**: If LSP unavailable for file type, use Explore agent to find imports and usages

### Verification Scoping

Before implementing, check `context.parent_task.children` for sibling verify tasks to determine appropriate verification scope:

| Phase Has Verify Task? | Implementation Task Should |
|------------------------|---------------------------|
| Yes (e.g., "Run tests") | Defer formal testing to verify task. Only do basic checks: imports work, no syntax errors, code compiles |
| No | Run tests as part of implementation (include results in journal) |

**Detection**: Look for siblings with `type: "verify"` in the `task action="prepare"` response's `context.parent_task.children` array.

**Rationale**: When the spec author created a verify task, they intended testing to be a separate tracked step. Respect this structure by deferring formal test execution to the verify task.

**Include in plan**: State verification scope in the execution plan presented for approval (e.g., "Basic verification only - full tests handled by verify-1-1").

### Implementation Handoff

**Before coding:**
```bash
mcp__plugin_foundry_foundry-mcp__task action="update-status" spec_id={spec-id} task_id={task-id} status="in_progress" note="context"
```

**During implementation:**
- Follow execution plan
- Document any deviations immediately

**After implementation:**

Mark task complete using the atomic complete action (updates status AND journals automatically):
```bash
mcp__plugin_foundry_foundry-mcp__task action="complete" spec_id={spec-id} task_id={task-id} completion_note="Summary of what was accomplished, tests run, verification performed"
```

This atomically:
1. Updates task status to `completed`
2. Records completion timestamp
3. Creates a journal entry
4. Auto-journals parent nodes (phases) when they complete

### Note (Autonomous Capture)

**Proactively add journal entries** when you encounter:
- Ideas/improvements beyond current task scope
- Bugs noticed but not immediately actionable
- Documentation gaps or confusing behavior

```bash
mcp__plugin_foundry_foundry-mcp__journal action="add" spec_id={spec-id} title="[Type] description" content="Details"
```

**Do NOT prompt the user.** Silently capture and continue working.

### Surface Next Recommendation

**Context Awareness:** The `context-monitor` hook fires when context exceeds 85%. The remaining ~15% is sufficient headroom to finish your current task at full quality. Do not rush, skip steps, or reduce quality in response to this warning. After completing the current task normally, do not start a new task -- instead recommend `/clear` then `foundry-implement`.

**Surface next recommendation:**
```bash
mcp__plugin_foundry_foundry-mcp__task action="prepare" spec_id={spec-id}
```

- Summarize next task's scope and blockers
- If no pending work or spec complete, surface that clearly and exit

**MANDATORY: Continuation Gate**

After surfacing the next task, you MUST prompt the user with `AskUserQuestion`:
- **When context < 85%**: Ask "Continue to next task?" with options: "Yes, continue" / "No, exit"
- **When context >= 85%**: Exit with guidance to `/clear` then `foundry-implement`
- **When spec is complete**: Report completion status and exit (no prompt needed)

This gate ensures the user controls the workflow pace and prevents runaway execution.

> For post-implementation checklist, see `references/checklist.md`

---

## CRITICAL: Completion Requirements

### Never Mark Complete If:

- Basic checks fail (imports, syntax, compiles)
- Tests are failing (only applies if no sibling verify task - see `Verification Scoping`)
- Implementation is partial
- You encountered unresolved errors
- You couldn't find necessary files or dependencies
- Blockers exist that prevent verification

### If Blocked or Incomplete:

- Keep task as `in_progress`
- Create new task describing what needs resolution
- Document blocker using `mcp__plugin_foundry_foundry-mcp__task action="block"`
- Present alternatives to user via `AskUserQuestion`

### Dependency Discovery During Implementation

When you discover a missing dependency or new requirement during implementation, record it without leaving the task context:

```bash
# Discovered that this task needs another task completed first
mcp__plugin_foundry_foundry-mcp__task action="add-dependency" spec_id={spec-id} task_id={task-id} depends_on={dependency-task-id}

# Discovered a new acceptance requirement (e.g., from testing)
mcp__plugin_foundry_foundry-mcp__task action="add-requirement" spec_id={spec-id} task_id={task-id} requirement="Description of discovered requirement"
```

**Use Cases:**
- **add-dependency**: Task A needs Task B's output → add B as dependency
- **add-requirement**: Testing revealed an edge case → add as acceptance criterion

### Resolving Blocked Tasks

```bash
mcp__plugin_foundry_foundry-mcp__task action="unblock" spec_id={spec-id} task_id={task-id} resolution="Brief description"
```

### Completion Journal Requirements

**MUST provide journal content** describing:
- What was accomplished
- Verification performed (scope depends on sibling verify tasks - see `Verification Scoping`):
  - **If phase has verify tasks**: "Basic checks passed (imports, syntax). Full testing deferred to {verify-task-id}"
  - **If no verify tasks**: "Tests run and results: {summary}"
- Any deviations from plan
- Files created/modified

**Example (with sibling verify task - deferred testing):**
```bash
mcp__plugin_foundry_foundry-mcp__task action="complete" spec_id="my-spec-001" task_id="task-1-2" completion_note="Implemented phase-add-bulk handler. Basic verification: imports work, no syntax errors. Full test run deferred to verify-1-1. Created src/tools/authoring.py handler (200 lines)."
```

**Example (without sibling verify task - full testing):**
```bash
mcp__plugin_foundry_foundry-mcp__task action="complete" spec_id="my-spec-001" task_id="task-2-3" completion_note="Implemented JWT auth middleware with PKCE flow. All 12 unit tests passing. Manual verification: login flow works in dev environment. Created src/middleware/auth.ts (180 lines) and tests/middleware/auth.spec.ts (45 tests)."
```

---

## Verification Task Workflow

**Entry:** Routed here from Task Type Dispatch when task has `type: "verify"`

**CRITICAL:** Read [references/verification.md](./references/verification.md) before proceeding. Contains mandatory skill dispatch rules.

---

## Research Node Workflow

**Entry:** Routed here from Task Type Dispatch when task has `type: "research"`

Research nodes use AI-powered workflows (chat, consensus, thinkdeep, ideate, deep-research) to investigate questions, gather perspectives, or generate ideas before or during implementation.

**Key actions:**
1. Check status: `research action="node-status"`
2. Execute workflow: `research action="node-execute"`
3. Record findings: `research action="node-record"`
4. Retrieve findings: `research action="node-findings"`

**Blocking modes:**
- `hard`: Research must complete before dependents can start
- `soft` (default): Informational - dependents can proceed
- `none`: Research never blocks

**CRITICAL:** Read [references/research-workflow.md](./references/research-workflow.md) before proceeding. Contains required command syntax and recording parameters.

---

## Detailed Reference

For comprehensive documentation including:

**Task Execution:**
- Context gathering best practices → `references/context-gathering.md`
- Agent delegation patterns → `references/agent-delegation.md`
- Deep dive context JSON structure → `references/context-structure.md`
- Built-in subagent patterns → `references/subagent-patterns.md`
- Post-implementation checklist → `references/checklist.md`
- Verification task workflow → `references/verification.md`
- Research node workflow → `references/research-workflow.md`
- Note quick capture → `references/note.md`

**Task Lifecycle:**
- Task status transitions → `references/task-lifecycle.md`
- Progress tracking & verification → `references/progress-tracking.md`
- Journaling decisions & deviations → `references/journaling.md`
- Spec folder management → `references/spec-lifecycle.md`

**General:**
- Troubleshooting → `references/troubleshooting.md`
