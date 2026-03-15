---
name: execute
description: Orchestrated task execution engine. Decomposes any goal into small atomic tasks, plans dependencies, selects the right agent/tool/MCP server for each, executes in optimally parallel batches, and tracks everything. Use when given a complex, multi-step goal that benefits from structured decomposition and full tool utilization.
disable-model-invocation: true
argument-hint: "<goal description>"
---

# Execute — Orchestrated Task Engine

Decompose a goal into atomic tasks, plan dependencies, select optimal tools, and execute with maximum parallelism.

## Protocol

Process every `/execute` invocation through these 6 phases in strict order. Never skip a phase. Gate each phase: do not advance until the current phase is complete.

### Phase 1: ANALYZE

Understand the goal before decomposing it.

1. Parse `$ARGUMENTS` as the goal statement
2. Identify the goal type (feature, bugfix, refactor, research, migration, infrastructure, other)
3. Explore the codebase to understand current state — use Glob, Grep, Read, or the Explore agent for broad searches
4. Check existing skills, memory files, and CLAUDE.md for relevant patterns
5. If the goal is ambiguous, use AskUserQuestion to clarify scope — do NOT guess

**Gate:** Proceed only when the goal, scope, and current state are clearly understood.

### Phase 2: DECOMPOSE

Break the goal into small, atomic tasks. Each task must be completable in a single focused action (< 30 minutes of work). If a task feels too large, split it further.

For each task, create it with `TaskCreate` using this specification:

```
Subject: <imperative verb phrase — "Add retry logic to Bedrock calls">
Description: |
  **Input:** <what this task needs — files, data, outputs from prior tasks>
  **Tool:** <specific agent, skill, MCP server, or direct tool — see references/agent-selection.md>
  **Steps:**
  1. <concrete step>
  2. <concrete step>
  3. <concrete step>
  **Success:** <how to verify completion — test passes, file exists, output matches>
  **Output:** <what this task produces — modified files, data, artifacts>
ActiveForm: <present continuous — "Adding retry logic to Bedrock calls">
```

**Decomposition rules:**
- One responsibility per task — if a task has "and" in it, split it
- Research tasks are separate from implementation tasks
- Test-writing is a separate task from code-writing
- File creation is separate from file modification
- Each task targets ≤ 3 files

**Gate:** All tasks created via TaskCreate. Minimum 3 tasks for any non-trivial goal.

### Phase 3: PLAN

Establish execution order by setting dependencies and identifying parallel batches.

1. For each task, set `addBlockedBy` via `TaskUpdate` to declare which tasks must complete first
2. Identify **batches** — groups of tasks with all dependencies satisfied:
   - **Batch 1:** Tasks with zero dependencies (launch all in parallel)
   - **Batch 2:** Tasks whose dependencies are all in Batch 1
   - **Batch N:** Tasks whose dependencies are all in Batches 1..N-1
3. Display the execution plan as a table:

```
Batch 1 (parallel): #1 Research API docs, #2 Read existing code
Batch 2 (parallel): #3 Implement service [blocked by #1, #2], #4 Write types [blocked by #1]
Batch 3 (sequential): #5 Write tests [blocked by #3], #6 Integration test [blocked by #3, #4]
Batch 4: #7 Review and polish [blocked by #5, #6]
```

**Gate:** All dependencies set. Execution plan displayed. No circular dependencies.

### Phase 4: EXECUTE

Process batches in order. Within each batch, maximize parallelism.

**For each batch:**

1. Call `TaskUpdate` to set all batch tasks to `in_progress`
2. Launch all tasks in the batch simultaneously:
   - **Agent tasks** → use `Task` tool with the appropriate `subagent_type` (see references/agent-selection.md)
   - **Direct tool tasks** → use Read, Write, Edit, Grep, Glob, Bash directly
   - **MCP tasks** → use the appropriate MCP server tool
   - **Web research** → use WebSearch, WebFetch
   - **Skill tasks** → invoke via Skill tool
3. Collect results from all tasks in the batch
4. Mark completed tasks via `TaskUpdate` with `status: completed`
5. If a task fails:
   - Log the failure in the task description via `TaskUpdate`
   - Assess: is this recoverable? Create a fix task if yes
   - Assess: are downstream tasks blocked? Flag them
   - Continue with non-blocked tasks — do NOT stop the entire pipeline
6. Proceed to next batch only when ALL tasks in current batch are resolved (completed or failed-and-handled)

**Execution rules:**
- Send a single message with multiple `Task` tool calls for parallel agent launches
- Use `run_in_background: true` for agent tasks that can run concurrently
- For direct edits (Write/Edit), execute sequentially if they touch the same file
- Always read a file before editing it
- After code changes, run relevant tests if a test suite exists

### Phase 5: VERIFY

After all batches complete, verify the overall goal.

1. Call `TaskList` to confirm all tasks are `completed`
2. For code changes: run the build or test command if applicable
3. For research: verify all questions in the original goal are answered
4. If verification fails: create remediation tasks and loop back to Phase 4
5. Run the `code-quality` agent on modified files if substantial code was written

**Gate:** All tasks completed. Build/tests pass (if applicable). Goal satisfied.

### Phase 6: REPORT

Summarize execution results.

```
## Execution Report

**Goal:** <original goal>
**Tasks:** <completed>/<total> completed
**Batches:** <N> batches, <M> parallel launches

### Completed
- #1 ✓ <subject> — <key output>
- #2 ✓ <subject> — <key output>

### Failed (if any)
- #X ✗ <subject> — <reason>

### Files Modified
- path/to/file.swift — <what changed>

### Next Steps (if any)
- <remaining work or follow-ups>
```

## Agent & Tool Selection

See [references/agent-selection.md](references/agent-selection.md) for the complete selection matrix.

**Quick reference:**
| Task Type | Tool/Agent |
|-----------|-----------|
| Find files by pattern | Glob (direct) |
| Search code content | Grep (direct) |
| Read specific files | Read (direct) |
| Broad codebase exploration | Explore agent |
| Architecture/design decisions | architecture-planner agent + deep-analysis skill |
| Write/modify code | Write/Edit (direct) or api-backend/frontend-specialist agent |
| Code review | code-quality agent |
| Write tests | test-automation agent |
| Database work | database-architect agent |
| Performance analysis | performance-optimizer agent |
| Security audit | security-scan command |
| Library documentation | library-docs skill (context7 MCP) |
| Complex reasoning | deep-analysis skill (sequential-thinking MCP) |
| Web research | WebSearch + WebFetch |
| GitHub operations | Bash (gh CLI) or GitHub MCP |
| Git operations | Bash (git CLI) |
| Build/run commands | Bash |
| Browser testing | Playwright MCP |

## Error Recovery

When a task fails:

1. **Transient failure** (network, timeout) → retry once
2. **Validation failure** (wrong format, missing input) → fix input, create fix task
3. **Dependency failure** (upstream task produced bad output) → fix upstream first
4. **Unrecoverable** (missing access, unsupported operation) → mark failed, skip dependents, notify user
5. **Ambiguity discovered** (unclear requirements mid-execution) → pause, AskUserQuestion, resume

Never silently skip a failed task. Always log what happened and why.
