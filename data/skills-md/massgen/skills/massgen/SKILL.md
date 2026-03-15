---
name: massgen
description: "Invoke MassGen's multi-agent system for general-purpose tasks, evaluation, planning, or spec writing. Use whenever you want multiple AI agents to tackle a problem, need outside perspective on your work, a thoroughly refined plan, or a well-specified set of requirements. Perfect for: writing, code generation, research, design, analysis, pre-PR review, complex project planning, feature specification, architecture decisions, or any task where multi-agent iteration produces better results than working alone."
---

# MassGen

Invoke MassGen for multi-agent iteration on any task — general-purpose work, evaluation, planning, or spec writing. Multiple AI agents independently work on the problem and converge on the strongest result through MassGen's checklist-gated voting system.

## When to Use

**General** (default) — get multi-agent results on any task:
- When you want multiple AI agents to independently tackle a problem
- When the task doesn't fit neatly into evaluate, plan, or spec
- Writing, research, code generation, design, analysis, or any open-ended task

**Evaluate** — get diverse, critical feedback on existing work:
- After iterating and stalling — need outside perspective
- Before submitting PRs or delivering artifacts
- When wanting diverse AI perspectives on implementation quality

**Plan** — create or refine a structured project plan:
- When starting a complex feature or project that needs task decomposition
- When an existing plan has gaps, is too vague, or needs restructuring
- When you need a valid task DAG with verification criteria

**Spec** — create or refine a requirements specification:
- When starting a feature that needs precise requirements before implementation
- When an existing spec has ambiguities, missing edge cases, or gaps
- When you need EARS-formatted requirements with acceptance criteria

## Mode Selection

| Mode | Purpose | Input | Output | Default Criteria Preset |
|------|---------|-------|--------|------------------------|
| general | Any task | Task description + context | Winner's deliverables in `result.md` + workspace files | Auto-generated |
| evaluate | Critique existing work | Artifacts to evaluate | `critique_packet.md` (with `approach_assessment`), `verdict.json`, `next_tasks.json` (with `fix_tasks`, `evolution_tasks`) | `"evaluation"` |
| plan | Create or refine a plan | Goal + constraints (+ existing plan) | `project_plan.json` (typed tasks, chunks, deps, prototypes) | `"planning"` |
| spec | Create or refine a spec | Problem + needs (+ existing spec) | `project_spec.json` (EARS requirements, chunks, rationale) | `"spec"` |

## FIRST: Check Config (do this before anything else)

Before reading any other section of this skill, run this check:

```bash
ls .massgen/config.yaml 2>/dev/null && echo "FOUND: project config"
ls ~/.config/massgen/config.yaml 2>/dev/null && echo "FOUND: global config"
```

- If the user gave a specific config path → use it with `--config <path>`.
- If `.massgen/config.yaml` exists → use it (no `--config` needed).
- If `~/.config/massgen/config.yaml` exists → use it.
- If **neither exists** → run the web quickstart **from the current working directory** (do NOT cd anywhere) and wait for it to finish:

```bash
uv run massgen --web-quickstart
```

Run this from cwd so the config is saved to `.massgen/config.yaml` in the
right project. Do NOT cd to another directory first. The quickstart opens a
browser where the user picks providers/models, enters API keys, and saves a
config. It exits automatically when done.

**STOP here until you have a config.** Do NOT proceed with the workflow below
until a config exists. Do NOT create config files yourself. Do NOT search
for configs in subdirectories, parent directories, or anywhere else.

---

## Scope

Before starting, determine what the MassGen invocation covers. Focused invocations
produce far better results than unscoped "do everything" runs.

- **General**: the task to accomplish, relevant context, quality expectations
- **Evaluate**: which files/artifacts to evaluate, what to ignore, evaluation focus
- **Plan**: the goal/objective, constraints, what context to include
- **Spec**: the problem to specify, user needs, system boundaries

If the user doesn't specify scope, ask them.

## Workflow

### Step 0: Create Working Directory

Create a timestamped subdirectory so parallel invocations don't conflict:

```bash
MODE="general"  # or "evaluate", "plan", or "spec"
WORK_DIR=".massgen/$MODE/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$WORK_DIR"
```

All artifacts (context, criteria, prompt, output, logs) go in this directory.

### Step 1: Clarify & Write Context File

Read `references/<mode>/workflow.md` (relative to this skill) for the context
file template specific to your mode.

Write `$WORK_DIR/context.md` using the template from the workflow file.

**Key principle for all modes**: provide factual context that orients the MassGen
agents. Do NOT bias them with your opinions about quality — let them discover
issues independently. That's the whole point of multi-agent evaluation.

- **General**: describe the task, relevant context, quality expectations
- **Evaluate**: describe what was built, scope, git info, verification evidence
- **Plan**: describe the goal, constraints, existing context, success criteria
- **Spec**: describe the problem, user needs, system boundaries, constraints

### Step 2: Generate Criteria

Each mode has a recommended criteria preset:

| Mode | Preset | How to Apply |
|------|--------|-------------|
| general | Auto-generated | Omit `--criteria-file` and `--criteria-preset` |
| evaluate | Custom or `"evaluation"` | `--criteria-file` with JSON, or `--criteria-preset evaluation` |
| plan | `"planning"` | `--criteria-preset planning` |
| spec | `"spec"` | `--criteria-preset spec` |

For general mode, criteria are auto-generated from the task content — omit
both flags unless you have specific quality axes to enforce.

**To use custom criteria**: read `references/criteria_guide.md` for the format
and writing guide, then write criteria JSON to `$WORK_DIR/criteria.json`.

If there's a specific focus area, weight your criteria toward that focus.
In Claude Code: use AskUserQuestion to ask the user for focus preference.
In Codex or non-interactive: default to general coverage.

```bash
cat > $WORK_DIR/criteria.json << 'EOF'
[
  {"text": "...", "category": "must"},
  {"text": "...", "category": "must"},
  {"text": "...", "category": "should"},
  {"text": "...", "category": "could"}
]
EOF
```

### Step 3: Construct the Prompt

1. Read the prompt template from `references/<mode>/prompt_template.md` (relative to this skill)
2. Read the context file you wrote in Step 1
3. Replace `{{CONTEXT_FILE_CONTENT}}` with the context file contents
4. Replace `{{CUSTOM_FOCUS}}` with the focus directive (or empty string if none)
5. Write the final prompt to `$WORK_DIR/prompt.md`

### Step 4: Run MassGen

Use the launcher script (`scripts/massgen_run.sh` relative to this skill)
to run MassGen, launch the web viewer, and wait for completion in a single
atomic command. This avoids the double-backgrounding issues that cause agents
to lose track of running processes.

**Run in the background** using your agent's native mechanism (e.g.,
`run_in_background` in Claude Code):

```bash
# SKILL_DIR is the directory containing this SKILL.md file
bash "$SKILL_DIR/scripts/massgen_run.sh" \
  --work-dir "$WORK_DIR" \
  --prompt-file "$WORK_DIR/prompt.md" \
  --criteria-file "$WORK_DIR/criteria.json" \
  --viewer
```

If using default criteria (no custom criteria file), omit `--criteria-file`.
For planning/spec modes, use `--criteria-preset planning` or `--criteria-preset spec` instead.
If you resolved a custom config in Step 2, add `--config <path>`.

The script handles everything atomically:
1. Launches MassGen in `--automation` mode
2. Waits for the log directory to appear (with 30s timeout)
3. Starts the web viewer at `http://localhost:8000`
4. Waits for MassGen to complete
5. Writes `$WORK_DIR/run_summary.json` with exit code, duration, log dir

**After the background task completes**, read the summary:

```bash
cat $WORK_DIR/run_summary.json
```

**Script options:**
- `--viewer` — launch web viewer (opens `http://localhost:8000`)
- `--viewer-port PORT` — use a different port
- `--config FILE` — custom MassGen config YAML
- `--output-file FILE` — override result path (default: `$WORK_DIR/result.md`)
- `--no-cwd-context` — disable read-only CWD access
- `--extra-args "..."` — pass additional massgen CLI flags

**Timing:** expect 15-45 minutes. Do not assume something is stuck — MassGen runs multiple agents through several rounds of iteration.

### Step 5: Parse the Output

The output depends on the mode. The winner's workspace path is shown in
`$WORK_DIR/result.md` (look for "Workspace cwd" or check `status.json` in
the log directory for `workspace_paths`).

**General mode**: the winner's answer is in `$WORK_DIR/result.md`. Any files
the agents created are in the winner's workspace (path shown in result.md).
Copy or reference the workspace files as needed.

**Evaluate mode**: three files — `verdict.json`, `next_tasks.json`, `critique_packet.md`.
Read `verdict.json` first to determine iterate vs converged.
See `references/evaluate/workflow.md` for full output structure.

**Plan mode**: `project_plan.json` — structured task list with chunks,
dependencies, and verification. May include auxiliary files in `research/`,
`framework/`, `risks/` subdirectories.
See `references/plan/workflow.md` for full output structure.

**Spec mode**: `project_spec.json` — EARS requirements with chunks,
rationale, and verification. May include auxiliary files in `research/`,
`design/`, `decisions/` subdirectories.
See `references/spec/workflow.md` for full output structure.

### Step 6: Ground in Your Native Task System

**This is the most critical step for evaluate, plan, and spec modes.** MassGen
produced a structured result — now you must internalize it by entering your
native task/plan mode and enumerating every task or requirement as a tracked
item. Without this, the plan is just text that fades from context as you work.

For **general mode**, grounding is optional — it applies when the output
contains a structured task list or action items, but many general tasks
produce artifacts (code, documents, designs) rather than task lists.

**Why this matters**: agents that skip this step tend to execute the first
few tasks, then drift — forgetting verification steps, skipping later
tasks, or losing track of dependencies. Grounding forces you to commit
to the full scope before executing anything.

**For all modes:**

1. **Enter your task planning mode** (e.g., TodoWrite in Claude Code,
   task tracking in Codex, or whatever native tracking your environment
   provides)
2. **Create one tracked task per item** from the MassGen output:
   - **Evaluate**: each task from `next_tasks.json` becomes a tracked task,
     preserving `implementation_guidance`, `depends_on`, and `verification`
   - **Plan**: each task from `project_plan.json` becomes a tracked task,
     preserving chunk ordering, dependencies, and verification criteria
   - **Spec**: each requirement from `project_spec.json` becomes a tracked
     task (implement + verify), preserving priority, dependencies, and
     acceptance criteria
3. **Preserve the dependency order** — don't flatten the DAG. Tasks in
   chunk C01 must complete before C02 tasks begin
4. **Include verification as explicit tasks** — don't just track "implement
   X", also track "verify X meets [criteria]". Verification that isn't
   tracked doesn't happen
5. **Mark each task's status** as you work: pending → in_progress → completed

**Then execute in order**, updating status as you go. When you complete a
task, check it off and move to the next one. This creates an execution
trace that keeps you honest about what's done and what remains.

### Step 7: Execute and Iterate

**General**: read `result.md` for the winning answer. Copy deliverable
files from the winner's workspace if applicable.

**Evaluate**: read `verdict.json` — if `"iterate"`, check
`approach_assessment.ceiling_status` in `next_tasks.json` first:
- `ceiling_not_reached` → execute `fix_tasks`, then `evolution_tasks` as stretch
- `ceiling_approaching` → execute `fix_tasks`, then `evolution_tasks`
- `ceiling_reached` → consider re-invoking plan mode with evaluation findings
  (see Plan-Evaluate Loop below)
If `"converged"`, proceed to delivery.

**Plan / Spec**: store the result as a living document (see below),
then execute the grounded tasks chunk by chunk. At tasks marked with
`eval_checkpoint`, invoke evaluate mode to assess approach viability
before continuing (see Plan-Evaluate Loop below).

## Living Document Protocol (Plan & Spec Modes)

This is the most important section for plan/spec modes — it defines how
the output is used after MassGen produces it.

### Store

Adopt the MassGen output into `.massgen/plans/` using the existing
`PlanStorage` infrastructure:

```
.massgen/plans/plan_<timestamp>/
├── workspace/          # Mutable working copy
│   ├── plan.json       # (renamed from project_plan.json) or spec.json
│   └── research/       # Auxiliary files from MassGen output
├── frozen/             # Immutable snapshot (identical to workspace/ at creation)
│   ├── plan.json       # or spec.json
│   └── research/
└── plan_metadata.json  # artifact_type, status, chunk_order, context_paths
```

Copy `project_plan.json` → `workspace/plan.json` (or `project_spec.json` →
`workspace/spec.json`). Copy any auxiliary directories. Create `frozen/` as
an identical snapshot.

### Read on Restart

**FIRST ACTION** in every new session: read `workspace/plan.json` (or
`workspace/spec.json`). This is the source of truth for what's done and
what's next.

### Update Continuously

As tasks complete (plan) or requirements are implemented (spec), update
the workspace copy. Mark status, add notes, record discoveries.
The workspace copy is a living document.

### Check Drift

Periodically compare `workspace/` against `frozen/`. The existing
`PlanSession.compute_plan_diff()` returns a `divergence_score`
(0.0 = no drift, 1.0 = complete rewrite). High drift means re-evaluate
whether the plan/spec is still valid.

### Refine When Stuck

If the plan/spec proves wrong or incomplete, re-invoke this skill with
the workspace copy as "What Already Exists" to get multi-agent refinement.
This creates a new plan directory with a fresh `frozen/` snapshot.

### Don't Drift Silently

If you deviate from the plan/spec, update the workspace copy first.
An outdated plan is worse than no plan.

## Mode Overviews

### General

Run any task through MassGen's multi-agent system. Agents independently
produce solutions and converge through checklist-gated voting. Use this
for tasks that don't fit neatly into evaluate, plan, or spec — writing,
code generation, research, analysis, design, or anything where multiple
perspectives improve the result.

See `references/general/workflow.md` for the context template and
output handling.

### Evaluate

Critique existing work artifacts. Evaluator agents inspect your code,
documents, or deliverables and produce a structured critique with
machine-readable verdict, per-criterion scores, and actionable
improvement tasks. The checklist-gated voting system ensures agents
converge on the strongest critique.

See `references/evaluate/workflow.md` for the full context template,
output structure, and examples.

### Plan

Create or refine a structured project plan. Planning agents decompose
the goal into a task DAG with chunks, dependencies, verification
criteria, and technology choices. Each round of MassGen iteration
improves task quality — descriptions get more actionable, verification
gets more specific, sequencing gets tighter.

See `references/plan/workflow.md` for the full context template,
output format, and lifecycle.

### Spec

Create or refine a requirements specification. Spec agents produce
EARS-formatted requirements with acceptance criteria, rationale,
and verification. Iteration focuses on precision — each round
eliminates ambiguities, fills gaps, and strengthens edge case coverage.

See `references/spec/workflow.md` for the full context template,
output format, and lifecycle.

## Plan-Evaluate Loop

For complex or creative projects, plan and evaluate modes work together
in a feedback loop:

```
Plan → Execute → Evaluate → (fix OR re-plan) → Execute → Evaluate → ...
```

### When to Use the Loop

- The task has exploratory components (visual design, creative writing, UX)
- The project is complex enough that the initial plan is partly speculative
- Quality expectations are high and "correct but adequate" isn't enough
- Prior iterations show diminishing returns

### Loop Protocol

1. **Plan**: invoke plan mode. Agents classify tasks as `deterministic` or
   `exploratory` and create prototypes to validate assumptions
2. **Execute**: implement the plan chunk by chunk
3. **Evaluate**: at `eval_checkpoint` tasks (or after any exploratory chunk),
   invoke evaluate mode
4. **Decide**: read `approach_assessment` in the evaluation output:
   - `ceiling_not_reached` → execute fix_tasks, continue
   - `ceiling_approaching` → execute fix_tasks + evolution_tasks, continue
   - `ceiling_reached` → re-invoke plan mode with evaluation discoveries
5. **Evolve**: if re-planning, pass `approach_assessment` and `breakthroughs`
   as context. The new plan amplifies what worked and avoids approaches that
   hit their ceiling
6. **Repeat** until evaluation returns "converged"

### What Makes This Different from Just Re-Running Eval

- Eval assesses whether the APPROACH has room to grow, not just whether
  the OUTPUT has defects
- When the approach is limited, the loop goes back to PLANNING, not just
  more implementation
- Breakthroughs discovered during execution feed FORWARD into new plans,
  not just into preserve lists
- The plan evolves based on evidence from execution, not speculation

### Loop Termination

- Max 3 plan mutations per chunk — if still not converging, escalate to user
- If evaluation returns "converged" with `ceiling_not_reached`, the loop
  is complete
- If the user provides explicit direction, follow it regardless of ceiling status

## Condensed Examples

### General: Multi-Agent Task Execution

```bash
WORK_DIR=".massgen/general/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$WORK_DIR"

cat > $WORK_DIR/context.md << 'EOF'
## Task
Build a responsive landing page for a developer tool that converts
CSV files to JSON. Single page with hero, features, and CTA sections.

## Context
- Target audience: developers and data engineers
- Tech stack: HTML, CSS, vanilla JS (no frameworks)
- Must work on mobile and desktop

## Quality Expectations
- Visually polished, not template-looking
- Fast load time, no external dependencies
EOF

# Build prompt from references/general/prompt_template.md, then run
# No --criteria-file — criteria auto-generated from task
bash "$SKILL_DIR/scripts/massgen_run.sh" \
  --work-dir "$WORK_DIR" \
  --prompt-file "$WORK_DIR/prompt.md" \
  --viewer
```

### Evaluate: Pre-PR Review

```bash
WORK_DIR=".massgen/evaluate/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$WORK_DIR"

# Write context (scope: specific deliverables, no quality opinions)
cat > $WORK_DIR/context.md << 'EOF'
## Deliverables in Scope
- `src/api/handler.ts` — API request handler
- `src/hooks/useAuth.ts` — authentication hook

## Out of Scope
- Test files, CI config

## Original Task
Add JWT authentication to the API layer

## What Was Done
Implemented JWT validation in handler and auth hook for React components.

## Verification Evidence
pytest: 24 passed, 0 failed
EOF

# Write criteria (or omit --eval-criteria to use default preset)
cat > $WORK_DIR/criteria.json << 'EOF'
[
  {"text": "Auth security: JWT validation covers expiration, signature, and audience checks.", "category": "must"},
  {"text": "Error handling: invalid/expired tokens produce clear error responses.", "category": "must"},
  {"text": "Code quality: clean separation between auth logic and business logic.", "category": "should"}
]
EOF

# Build prompt from template, then run
bash "$SKILL_DIR/scripts/massgen_run.sh" \
  --work-dir "$WORK_DIR" \
  --prompt-file "$WORK_DIR/prompt.md" \
  --criteria-file "$WORK_DIR/criteria.json" \
  --viewer
```

### Plan: New Feature Planning

```bash
WORK_DIR=".massgen/plan/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$WORK_DIR"

cat > $WORK_DIR/context.md << 'EOF'
## Goal
Add real-time collaboration to the document editor — multiple users
editing the same document simultaneously with cursor presence.

## Constraints
- Must work with existing PostgreSQL database
- Timeline: 2 weeks
- Team: 2 engineers

## Existing Context
Express.js backend, React frontend, WebSocket already used for notifications.

## Success Criteria
Two users can edit the same document with <500ms sync latency and no data loss.
EOF

# Build prompt from references/plan/prompt_template.md, then run
bash "$SKILL_DIR/scripts/massgen_run.sh" \
  --work-dir "$WORK_DIR" \
  --prompt-file "$WORK_DIR/prompt.md" \
  --criteria-preset planning \
  --viewer
```

### Spec: Feature Specification

```bash
WORK_DIR=".massgen/spec/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$WORK_DIR"

cat > $WORK_DIR/context.md << 'EOF'
## Problem Statement
Users cannot recover deleted items — deletion is permanent and irreversible.

## User Needs / Personas
- End users: accidentally delete items, need easy recovery
- Admins: need to purge items for compliance after retention period

## Constraints
- PostgreSQL database, soft-delete pattern preferred
- 30-day retention before permanent purge
- Must not break existing API consumers
EOF

# Build prompt from references/spec/prompt_template.md, then run
bash "$SKILL_DIR/scripts/massgen_run.sh" \
  --work-dir "$WORK_DIR" \
  --prompt-file "$WORK_DIR/prompt.md" \
  --criteria-preset spec \
  --viewer
```

## Reference Files

- `references/general/workflow.md` — general mode context template and output handling
- `references/general/prompt_template.md` — general prompt template with placeholders
- `references/criteria_guide.md` — how to write quality criteria (format, tiers, examples)
- `references/evaluate/workflow.md` — evaluate mode context template, output structure, examples
- `references/evaluate/prompt_template.md` — evaluation prompt template with placeholders
- `references/plan/workflow.md` — plan mode context template, output format, lifecycle
- `references/plan/prompt_template.md` — planning prompt template with placeholders
- `references/spec/workflow.md` — spec mode context template, output format, lifecycle
- `references/spec/prompt_template.md` — spec prompt template with placeholders
- `massgen/subagent_types/round_evaluator/SUBAGENT.md` — source methodology for evaluation
- `massgen/skills/massgen-develops-massgen/SKILL.md` — reference pattern for `--automation`
