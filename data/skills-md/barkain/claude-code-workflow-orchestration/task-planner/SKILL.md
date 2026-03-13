---
name: task-planner
description: Analyze user request, explore codebase, decompose into subtasks, assign agents, and return complete execution plan with wave assignments.
context: fork
allowed-tools: Read, Grep, Glob, Bash, WebFetch, AskUserQuestion, Agent, TaskCreate, TaskUpdate, TaskList, TaskGet
---

> **DEPRECATED:** This skill is retained for backward compatibility only. The planning logic (complexity scoring, tier classification, agent assignment, wave scheduling, task creation) has been moved to native plan mode in `system-prompts/workflow_orchestrator.md` (see "Planning Instructions" section). The main agent now enters plan mode via `EnterPlanMode` instead of invoking this skill.

# Task Planner

Analyze the user's request and return a complete execution plan including agent assignments and wave scheduling.

---

## Process

1. **Read environment configuration** — Run `echo ${CLAUDE_MAX_CONCURRENT:-8}` via Bash to capture the max concurrent agents limit. This value will be included in the execution plan JSON.

2. **Parse intent** — What does the user actually want? What's the success criteria?

3. **Check for ambiguities** — If blocking, return questions. If minor, state assumptions and proceed.

4. **Explore codebase** — Only if relevant for the user request: Find relevant files, patterns, test locations. Sample, don't consume.

5. **Decompose** — Break into atomic subtasks with clear boundaries.

6. **Assign agents** — Match each subtask to a specialized agent via keyword analysis.

7. **Map dependencies** — What blocks what? What can parallelize?

8. **Assign waves** — Group independent tasks into parallel waves.

9. **File conflict check** — Cross-reference target files across tasks in the same wave (see below).

10. **Flag risks** — Complexity, missing tests, potential breaks.

11. **Populate Tasks** — Create task entries using TaskCreate with structured metadata for execution.

---

## Output

### If Clarification Needed

When blocking ambiguities exist that prevent planning, use the `AskUserQuestion` tool to get clarification from the user.

**Use AskUserQuestion with**:
- `question`: A clear, specific question about what's blocking
- Include default assumptions in the question text so the user can simply confirm or override

**Example**:
```
AskUserQuestion(
  question: "Should this API support pagination? (Default: Yes, using cursor-based pagination)"
)
```

**Format for multiple questions**: Ask the most critical blocking question first. After receiving an answer, you can ask follow-up questions if still blocked.

### If Ready — Complete Execution Plan

Output the following structured plan:

---

## EXECUTION PLAN

**Status**: Ready

**Goal**: `<one sentence>`

**Execution Mode**: `subagent` | `team`

**Max Concurrent**: `<value from CLAUDE_MAX_CONCURRENT env var, default 8>`

**Success Criteria**:
- `<verifiable outcome>`

**Assumptions**:
- `<assumption made, if any>`

**Relevant Context**:
- Files: `<paths>`
- Patterns to follow: `<patterns>`
- Tests: `<location>`

---

### Subtasks with Agent Assignments

| ID | Description | Agent | Depends On | Wave |
| --- | --- | --- | --- | --- |
| 1 | `<description>` | `<agent-name>` | none | 0 |
| 2 | `<description>` | `<agent-name>` | none | 0 |
| 3 | `<description>` | `<agent-name>` | 1, 2 | 1 |
| ... | | | | |

---

### Wave Breakdown

List EVERY task individually (no compression):

```markdown
### Wave 0 (N parallel tasks)
  1: <description> -> <agent-name>
  2: <description> -> <agent-name>

### Wave 1 (M tasks)
  3: <description> -> <agent-name>
```

**Prohibited patterns:**
- `+` notation: `task1 + task2`
- Range notation: `1-3`
- Wildcard: `root.1.*`
- Summaries: `4 test files`

---

### Task Creation with Tasks API

**Note:** Use TaskCreate for each subtask. Metadata is stored in structured fields, not encoded strings.

**TaskCreate Parameters:**
- `subject`: Brief imperative title (e.g., "Create project structure")
- `description`: Detailed description including requirements and context
- `activeForm`: Present continuous form shown during execution (e.g., "Creating project structure")
- `metadata`: Object containing wave, phase, agent, parallel execution info, and output_file path

**Output File Assignment:** Each task gets `output_file: $CLAUDE_SCRATCHPAD_DIR/{sanitized_subject}.md` in metadata. Agents write full results there, return ONLY `DONE|{path}` (nothing else - this preserves main agent context). The scratchpad directory is automatically session-isolated.

**Agent Return Format (CRITICAL):**
- Agents MUST return exactly: `DONE|{output_file_path}`
- Example: `DONE|$CLAUDE_SCRATCHPAD_DIR/review_auth_module.md`
- PROHIBITED: summaries, findings, explanations, any other text
- All content goes in the output file, NOT the return value

**File Writing:**
- Agents HAVE Write tool access for /tmp/ paths
- Agents write directly to output_file - do NOT delegate file writing
- If Write is blocked, report error and stop (do not loop)

**File naming rules:**
- Use `$CLAUDE_SCRATCHPAD_DIR` for output files (automatically session-isolated)
- Sanitize subject: lowercase, replace spaces with underscores, remove special chars except hyphens
- Example: Task "Review code-cleanup-optimizer" → `$CLAUDE_SCRATCHPAD_DIR/review_code-cleanup-optimizer.md`

**Example TaskCreate calls:**

```
TaskCreate:
  subject: "Create project structure"
  description: "Set up initial project directory structure with src/, tests/, and config files"
  activeForm: "Creating project structure"
  metadata: {"wave": 0, "phase_id": "1", "agent": "general-purpose", "parallel": true, "output_file": "$CLAUDE_SCRATCHPAD_DIR/create_project_structure.md"}

TaskCreate:
  subject: "Create database config"
  description: "Create database configuration with connection pooling and environment-based settings"
  activeForm: "Creating database config"
  metadata: {"wave": 0, "phase_id": "2", "agent": "general-purpose", "parallel": true, "output_file": "$CLAUDE_SCRATCHPAD_DIR/create_database_config.md"}

TaskCreate:
  subject: "Verify implementations"
  description: "Run all tests and verify implementations meet requirements"
  activeForm: "Verifying implementations"
  metadata: {"wave": 1, "phase_id": "3", "agent": "task-completion-verifier", "parallel": false, "output_file": "$CLAUDE_SCRATCHPAD_DIR/verify_implementations.md"}
```

**After creating tasks, set up dependencies:**
```
TaskUpdate:
  taskId: "3"
  addBlockedBy: ["1", "2"]
```

---

### Risks

- `<what could go wrong and why>`

---

→ CONTINUE TO EXECUTION

---

## Available Specialized Agents

**IMPORTANT - Agent Name Prefix:**
- **Plugin mode:** Use `workflow-orchestrator:<agent-name>` (e.g., `workflow-orchestrator:task-completion-verifier`)
- **Native install:** Use just `<agent-name>` (e.g., `task-completion-verifier`)

To detect mode: Check if running as a plugin by looking for `workflow-orchestrator:` prefix in available agents list.

| Agent (base name) | Keywords | Capabilities |
| --- | --- | --- |
| **codebase-context-analyzer** | analyze, understand, explore, architecture, patterns, structure, dependencies | Read-only code exploration and architecture analysis |
| **tech-lead-architect** | design, approach, research, evaluate, best practices, architect, scalability, security | Solution design and architectural decisions |
| **task-completion-verifier** | verify, validate, test, check, review, quality, edge cases | Testing, QA, validation |
| **code-cleanup-optimizer** | refactor, cleanup, optimize, improve, technical debt, maintainability | Refactoring and code quality improvement |
| **code-reviewer** | review, code review, critique, feedback, assess quality, evaluate code | Code review and quality assessment |
| **devops-experience-architect** | setup, deploy, docker, CI/CD, infrastructure, pipeline, configuration | Infrastructure, deployment, containerization |
| **documentation-expert** | document, write docs, README, explain, create guide, documentation | Documentation creation and maintenance |
| **dependency-manager** | dependencies, packages, requirements, install, upgrade, manage packages | Dependency management (Python/UV focused) |
| **Explore** | review, summarize, scan, list, catalog | Built-in Haiku agent for breadth tasks (cheap, fast). **READ-ONLY: Cannot write files.** |

**Large-Scope Detection:** If task mentions "all files" / "entire repo" / "summarize each" -> consider parallel agents with a final aggregation phase. Each agent handles one bounded scope; aggregation phase collects summaries. **Important:** If tasks need to write output files, use `general-purpose` instead of Explore (Explore is read-only).

**When assigning agents in TaskCreate metadata and delegations, ALWAYS use the full prefixed name: `workflow-orchestrator:<agent-name>`**

---

## Agent Selection Algorithm

1. Extract keywords from subtask (case-insensitive)
2. Count matches per agent; select agent with >=2 matches (highest wins)
3. Ties: first in table order; <2 matches: general-purpose

---

## Execution Mode Selection (Dual-Mode: Subagent vs Team)

After decomposing subtasks and assigning agents, evaluate execution mode.

### Prerequisites

1. Check env via Bash: `echo ${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:-0}`
2. If not `1`, always use `"subagent"` mode (skip remaining checks)

### team_mode_score Calculation

| Factor | Points | Condition |
|--------|--------|-----------|
| Phase count | +2 | > 8 phases |
| Complexity tier | +2 | Tier 3 (score > 15) |
| Cross-phase data flow | +3 | Phase B reads files created by Phase A AND needs to make decisions based on content |
| Review-fix cycles | +3 | Plan includes review/verify then fix/refactor on same artifact |
| Iterative refinement | +2 | Plan includes success_criterion with retry loops |
| User keyword | +5 | User says "collaborate", "team", "work together" |
| Breadth task | -5 | Same operation across multiple items (e.g., "review all files") |
| Phase count <= 3 | -3 | Simple workflow |

### Decision

- `team_mode_score >= 5`: `execution_mode = "team"`
- `team_mode_score < 5`: `execution_mode = "subagent"`

### What execution_mode: "team" means

When `execution_mode` is set to `"team"`, the workflow orchestrator will:
- Create a native agent team via `TeamCreate`
- Execute ALL phases (across all waves) using `Agent(team_name=...)` instead of isolated `Agent(...)`
- This means ALL agents can communicate via `SendMessage` and coordinate through shared task list
- The plan structure (phases, waves, dependencies) stays the same -- only the execution mechanism changes

You do NOT need to create a single `phase_type: "team"` phase for complex workflows. The plan can have multiple individual phases across multiple waves. Setting `execution_mode: "team"` at the plan level is sufficient -- the orchestrator handles the rest.

Reserve `phase_type: "team"` for simple multi-perspective exploration tasks where the plan IS a single team phase (e.g., "explore from 3 angles").

### Execution Plan JSON Extension

When `execution_mode` is `"subagent"`, omit `team_config` -- execution proceeds exactly as today.

When `execution_mode` is `"team"`, include `team_config` in the execution plan output:

```json
{
  "execution_mode": "team",
  "team_config": {
    "team_name": "workflow-{timestamp}",
    "lead_mode": "delegate",
    "plan_approval": true,
    "max_teammates": 4,
    "teammate_roles": [
      {
        "role_name": "implementer",
        "agent_config": "code-cleanup-optimizer",
        "phase_ids": ["phase_0_0", "phase_0_1", "phase_1_0"]
      },
      {
        "role_name": "reviewer",
        "agent_config": "task-completion-verifier",
        "phase_ids": ["phase_2_0"]
      }
    ]
  }
}
```

### team_config Fields

| Field | Description |
|-------|-------------|
| `team_name` | Unique team identifier: `workflow-{YYYYMMDD_HHMMSS}`. Used with `TeamCreate(team_name=...)` and `Agent(team_name=...)`. |
| `lead_mode` | Always `"delegate"` (coordination-only, aligns with delegation enforcement) |
| `plan_approval` | `true` to require lead approval of teammate plans before implementation (see Plan Approval Cycle below) |
| `max_teammates` | Max concurrent teammates (default 4, conservative to manage lead context) |
| `teammate_roles[]` | Array of role definitions mapping agents to phases |
| `teammate_roles[].role_name` | Descriptive role (e.g., "implementer", "reviewer", "architect") |
| `teammate_roles[].agent_config` | Agent name for system prompt (e.g., "code-cleanup-optimizer") |
| `teammate_roles[].phase_ids` | Array of phase IDs this teammate handles |

**Bootstrapping:** The main agent creates the team via `TeamCreate(team_name=...)`, then spawns each teammate via `Agent(team_name=..., subagent_type=..., prompt=...)`. The `team_name` parameter on Agent is what makes it a teammate (shared context, SendMessage) vs an isolated subagent.

### Plan Approval Cycle

Plan approval is activated via the **spawn prompt** (natural language instruction), not an Agent tool parameter. When `plan_approval: true` in team_config, the task-planner should include the plan-before-implementing instruction in the teammate prompt template.

When spawning teammates, add this instruction to each teammate's prompt:
> "Before implementing, first explore the codebase and create a detailed plan. Submit your plan for approval before making any changes."

This activates native plan mode behavior. The full approval cycle:

1. Teammate explores in read-only mode and designs their implementation approach
2. Teammate calls `ExitPlanMode`, which sends a `plan_approval_request` message to the lead
3. Lead receives a JSON message with `type: "plan_approval_request"` containing a `requestId` and the proposed plan
4. Lead reviews the plan
5. Lead responds via `SendMessage` with `type: "plan_approval_response"`:
   - **Approve:** `SendMessage(type: "plan_approval_response", request_id: "<requestId>", recipient: "<teammate>", approve: true)` -- teammate exits plan mode and proceeds to implementation
   - **Reject:** `SendMessage(type: "plan_approval_response", request_id: "<requestId>", recipient: "<teammate>", approve: false, content: "<feedback>")` -- teammate revises their plan based on feedback and re-submits via `ExitPlanMode`
6. The cycle repeats until the plan is approved

When `plan_approval` is `false` or omitted, do NOT include the plan instruction in the spawn prompt -- teammates proceed directly to implementation.

### Execution Mode in Execution Plan Output

Add to the plan header:

```
**Execution Mode**: `subagent` | `team`
**Team Mode Score**: `<score>` (breakdown: <factors>)
```

When team mode is selected, also output:

```
**Team Config**:
- Team name: `<name>`
- Max teammates: `<count>`
- Roles: `<role1> (<agent>), <role2> (<agent>)`
```

---

## Handling Explicit Team Requests

When the user explicitly requests team/collaboration (e.g., "use a team", "have agents collaborate", "devil's advocate review"):

### Role-to-Agent Mapping

| User Role | Agent |
|-----------|-------|
| architect, designer | tech-lead-architect |
| critic, devil's advocate, challenger | task-completion-verifier |
| researcher, analyst, explorer | codebase-context-analyzer |
| reviewer, code reviewer | code-reviewer |
| other / unspecified | general-purpose (with `custom_prompt` describing the role) |

### Synthesis Phase

Always include a **synthesis/aggregation phase** in the final wave (Wave N) that collects outputs from all team-member phases and produces a unified result. Assign this to `general-purpose` or `tech-lead-architect` depending on context. The synthesis phase is a **regular subagent phase** (not a team phase).

### Team Phase Creation (execution_mode: "team")

When `execution_mode` is `"team"`, create a **SINGLE phase per team wave** with `phase_type: "team"` in metadata. Do NOT create one task per teammate -- the entire team is ONE task.

The phase metadata includes:
- `phase_type: "team"` -- marks this as a native team phase
- `agent: "native-team"` -- signals team execution (not a regular agent)
- `teammates` array -- each entry has `name`, `role`, `agent`, and optional `custom_prompt`
- `output_files` array -- one output file per teammate

**Note:** The PreToolUse hook automatically creates `.claude/state/team_mode_active` on the first team tool use (e.g., `TeamCreate`) when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set. No manual state file creation is needed.

**Native team bootstrapping:** The main agent executes `TeamCreate(team_name=...)` to create the team, then spawns each teammate via `Agent(team_name=..., subagent_type=..., prompt=...)`. The `team_name` parameter on Agent is what makes it a teammate (shared context, `SendMessage` for inter-agent communication) vs an isolated subagent (no `team_name` = no communication).

**Example TaskCreate for a team phase:**

```
TaskCreate:
  subject: "Agent Team: Multi-perspective exploration"
  description: "Spawn native Agent Team with 3 teammates exploring TODO CLI design. Bootstrap via TeamCreate then Agent(team_name=...) for each teammate."
  activeForm: "Running Agent Team exploration"
  metadata: {
    wave: 0,
    phase_id: "phase_0_team",
    phase_type: "team",
    agent: "native-team",
    team_name: "workflow-20250211_143022",
    teammates: [
      { name: "ux-researcher", role: "UX & developer experience", agent: "general-purpose" },
      { name: "architect", role: "System design & trade-offs", agent: "tech-lead-architect" },
      { name: "devils-advocate", role: "Critical analysis & failure modes", agent: "task-completion-verifier" }
    ],
    output_files: [
      "$CLAUDE_SCRATCHPAD_DIR/ux_research.md",
      "$CLAUDE_SCRATCHPAD_DIR/architecture.md",
      "$CLAUDE_SCRATCHPAD_DIR/devils_advocate.md"
    ]
  }
```

**Example TaskCreate for the synthesis phase (next wave):**

```
TaskCreate:
  subject: "Synthesize team exploration results"
  description: "Read outputs from all teammates and produce unified recommendations"
  activeForm: "Synthesizing team results"
  metadata: {
    wave: 1,
    phase_id: "phase_1_synthesis",
    agent: "general-purpose",
    parallel: false,
    output_file: "$CLAUDE_SCRATCHPAD_DIR/synthesis.md"
  }
```

Then set up dependencies:
```
TaskUpdate:
  taskId: "<synthesis_task_id>"
  addBlockedBy: ["<team_phase_task_id>"]
```

### Subagent Fallback (execution_mode: "subagent")

When `execution_mode` is `"subagent"` (either because `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is not `1`, or because `team_mode_score < 5`), decompose into **individual parallel phases** as normal. The role-to-agent mapping still applies -- each teammate becomes a separate TaskCreate in the same wave, executed as standard parallel subagents. The synthesis phase remains as a separate task in the next wave.

---

**Explore Agent Constraint (CRITICAL):**
- Explore is READ-ONLY — it CANNOT write files (no Write, Edit, NotebookEdit tools)
- NEVER assign Explore if task has `output_file` in metadata
- NEVER assign Explore if description contains: "write", "create", "save", "generate", "produce", "output"
- For parallel breadth tasks that need output files: use `general-purpose` instead of Explore

---

## Complexity Scoring & Tier Classification

**Score formula:** `action_verbs*2 + connectors*2 + domain + scope + risk` (range 0-35)

| Score | Tier | Min Depth |
| --- | --- | --- |
| < 5 | 1 | 1 |
| 5-15 | 2 | 2 |
| > 15 | 3 | 3 |

**Rule:** Depth < tier minimum → MUST decompose further.

---

## Atomicity Validation

**Step 1:** Depth >= tier minimum? If NO → DECOMPOSE (skip Step 2)

**Step 2:** Atomic if ALL true: single operation, ≤3 files modified, ≤5 files/10K lines input, single deliverable, implementation-ready, single responsibility

**Split rules:**
- Unbounded input → split by module/directory
- Multiple operations → one subtask each
- CRUD → separate create/read/update/delete

---

### Success Criteria & Iteration

- `requirements[]` - What it must do
- `success_criterion` - Verifiable command (optional); if present, agent loops until pass or max 5 attempts

---

### Implementation Task Decomposition

When decomposing implementation tasks (create, build, implement):

**ALWAYS decompose by function/component**, not by file:

| Task | Decomposition | Parallel? |
|------|---------------|-----------|
| "Create calculator with add, subtract, multiply, divide" | 4 tasks (one per operation) | Yes |
| "Build user auth with login, logout, register" | 3 tasks (one per feature) | Yes |
| "Implement CRUD operations" | 4 tasks (create, read, update, delete) | Yes |

**Example - Calculator module:**

WRONG (single task):
```
Wave 1: Create calculator module [1 task]
```

CORRECT (parallel tasks):
```
Wave 1 (Parallel):
- Implement add() function
- Implement subtract() function
- Implement multiply() function
- Implement divide() function
```

**Detection patterns:**
- "with [list]" -> decompose each item
- "basic operations" -> decompose: add, subtract, multiply, divide
- "CRUD" -> decompose: create, read, update, delete
- "auth" -> decompose: login, logout, register, etc.

**Minimum decomposition:** If a task mentions multiple operations/functions, create one subtask per operation.

---

## Agent-Based Decomposition (NOT Item-Based)

**WRONG:** 16 files → 16 tasks (1 task per file)
**RIGHT:** 16 files, 8 agents → 8 tasks (2 files per task)

When decomposing breadth tasks (same operation × multiple items):

1. **Identify total items** (files, modules, components, etc.)
2. **Use agent count** from `CLAUDE_MAX_CONCURRENT` (default 8, or user-specified)
3. **Create ONE task per agent**, NOT one task per item
4. **Each task description includes its assigned items**

**Example:**
- Input: "Review 16 agent files"
- Agent count: 8
- Output: 8 tasks (NOT 16)
  - Task 1: "Review code-cleanup-optimizer.md, code-reviewer.md" → general-purpose
  - Task 2: "Review codebase-context-analyzer.md, dependency-manager.md" → general-purpose
  - Task 3: "Review devops-experience-architect.md, documentation-expert.md" → general-purpose
  - Task 4: "Review task-completion-verifier.md, tech-lead-architect.md" → general-purpose
  - ... (4 more tasks with 2 files each)

**Compatibility with Atomic Task Criteria:**
This does NOT violate atomic task rules. "Atomic" means "single coherent unit of work", not "1 item per task".

A task that reviews 2-3 files and writes 1 report is still atomic:
- ✅ <30 minutes
- ✅ Modifies ≤3 files (1 report)
- ✅ Single deliverable (1 report)
- ✅ Single responsibility (review assigned files)

The difference is GROUPING strategy, not atomicity definition.

**Why this matters:**
- Reduces task overhead (8 TaskCreate calls vs 16)
- Matches actual parallelism limit (can only run 8 concurrent anyway)
- Simpler execution (1 wave of 8, not 2 waves of 8)
- Less context pollution in main agent

---

## Wave Optimization Rules

**Principle:** More tasks, fewer waves. Parallel by default. Bounded input (≤5 files/10K lines per task).

**Target:** 4+ tasks per wave, <6 total waves. A 10-task workflow → 2-3 waves.

---

### File Conflict Check (Same-Wave Tasks)

Before finalizing wave assignments, cross-reference target files across tasks in the same wave:
- If two tasks in the same wave modify the same file → move one to the next wave (make sequential)
- If two tasks read the same file but only one writes → OK (parallel safe)
- If uncertain about file overlap → default to sequential (conservative)

This is especially critical in team mode where teammates execute concurrently with shared filesystem access.

---

## Constraints

- Never implement anything
- Explore enough to plan, no more
- Trivial requests still get structure (one subtask)
- No tool execution beyond Read, Grep, Glob, Bash (for exploration), AskUserQuestion, TaskCreate, TaskUpdate, TaskList, TaskGet
- MUST create all tasks using TaskCreate before returning
- Use TaskUpdate to set up dependencies between tasks (addBlockedBy, addBlocks)

---

## Initialization

1. Read `CLAUDE_MAX_CONCURRENT` via Bash (default 8)
2. Parse request → explore codebase → check ambiguities → decompose → assign agents → map dependencies → assign waves
3. Create tasks via TaskCreate, set dependencies via TaskUpdate
4. Output plan with `max_concurrent` value (main agent cannot read env vars)
