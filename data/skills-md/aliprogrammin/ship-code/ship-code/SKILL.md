---
name: ship-code
description: >
  Anti-slop agentic coding workflow for Claude Code. Use this skill whenever the user wants to set up
  an agentic coding workflow, enforce quality gates, prevent technical debt, write precise task specs,
  decompose complex features into atomic units, or run a spec→execute→verify loop. Trigger on phrases
  like "set up my project for Claude Code", "break this into tasks", "write a spec", "no slop", "quality
  gates", "pre-commit hooks", "agentic workflow", "ship-code workflow", or any request to build
  something non-trivial with Claude Code where quality and traceability matter.
---

# ship-code

A lightweight anti-slop workflow for Claude Code. No enterprise theater. Just the practices that
actually prevent garbage from entering your codebase.

**Core philosophy:** Slop is an engineering problem, not an LLM problem. If an agent produces bad
code, fix the environment — never patch the output.

---

## Installation

This is a Claude Code plugin. Install it by placing this folder at:
- **Project-level** (shared with team): `.claude/plugins/ship-code/`
- **Global** (all your projects): `~/.claude/plugins/ship-code/`

Commands will be available as `/ship-code:init`, `/ship-code:plan`, `/ship-code:ship`, etc.

## About `.ship/`

The `.ship/` folder is created **inside your project root** by `/ship-code:init`. It holds:
- Quality gate config
- Hard blocks definition
- Centralized issue log
- Task spec files

This is intentional — it's project-level config that should live alongside your code (and optionally be committed to git for team sharing).

---

| Command | What it does |
|---|---|
| `/ship-code:init` | Set up hooks, gates, config, and hard blocks for this project |
| `/ship-code:research <problem>` | Research a problem — best practices, libraries, codebase analysis, spec suggestion |
| `/ship-code:plan <description>` | Decompose a feature into atomic specs, then execute them |
| `/ship-code:ship` | Ship multiple features at once — agent interviews you, plans everything, executes with gates |
| `/ship-code:run <spec-file>` | Execute a single spec file |
| `/ship-code:verify` | Run all quality gates and report results |
| `/ship-code:quick <description>` | Ad-hoc task with no ceremony — gates still enforced |

---

## Context management rules (always active)

The main context is the orchestrator. It stays light. All heavy work happens in subagents.

| Command | Who does the work |
|---|---|
| `/ship-code:research` | Delegates entirely to `ship-researcher` subagent |
| `/ship-code:plan` | Delegates entirely to `ship-planner` subagent |
| `/ship-code:ship` | Interviews user in main context → delegates execution to `ship-shipper` subagent |
| `/ship-code:verify` | Delegates entirely to `ship-verifier` subagent |
| `/ship-code:run` | Delegates entirely to `ship-planner` subagent (single spec mode) |
| `/ship-code:quick` | Runs in main context — lightweight enough, no subagent needed |
| `/ship-code:init` | Runs in main context — one-time setup, no subagent needed |

**Rules for the main context:**
- Never read large files or grep the whole codebase in the main context
- Never run tests or linters directly in the main context
- Never accumulate tool call output in the main context — delegate instead
- Subagents return only a concise summary — the main context never sees raw tool output
- Subagents are fire-and-done: they complete their task, return a summary, and are gone

**Rules for subagents:**
- Each subagent gets exactly one job with a clear deliverable
- Subagents cannot spawn other subagents
- Subagents return summaries, never full transcripts
- Subagents write their artifacts to disk (`.ship/`) so nothing is lost when they exit

---

These govern every agent action in this workflow:

1. **Never fix bad output — reset and rerun.** If output is wrong, diagnose the root cause (bad spec,
   missing context, wrong scope), fix that, and rerun from scratch.

2. **One agent, one task, one prompt.** Each agent gets exactly one job. Focused agents are correct agents.

3. **Gates before handoff.** Tests + lint + types must pass 100% before any task is considered done,
   committed, or passed to another agent.

4. **Never mock what you can use for real.** Mocks hide real failures. Real integrations catch them.

5. **Precise specs, zero inference.** Agents must never guess intent. Specs include exact files, line
   ranges, inputs, outputs, and acceptance criteria.

6. **Pit of success.** The easiest path the agent can take should always be the correct one.

7. **Traceability always.** Every change is attributable to a specific agent, task, and timestamp. Commit messages encode this. The hook logs it.

8. **Isolated work trees.** Each agent works in its own declared scope. In multi-agent flows, use git worktrees to give each agent a fully isolated filesystem — no shared state, no stepping on each other.

9. **Escalate, don't improvise.** If an agent hits something outside its scope or fails gates twice, it stops and surfaces to the human. It never silently works around a blocker.

10. **Read before you write.** Before implementing, agents scan existing code for patterns, conventions, and style. New code must match what's already there. This is the recursive quality loop — good code trains better code.

---

## `/ship-code:init`

Sets up the project for anti-slop agentic development.

### What it does

1. Creates `.ship/config.json` with project quality gate settings
2. Installs pre-commit hook that runs gates before every commit
3. Creates `.ship/issues.md` as the single source of truth for agent learnings/blockers
4. Creates `.ship/HARD_BLOCKS.md` defining what agents can never do
5. Detects stack (Node/Python/etc) and configures appropriate linting + type-checking

### Hard blocks (default)

Written to `.ship/HARD_BLOCKS.md` and enforced via hook:

- **NEVER** `git push` — human reviews and pushes manually
- **NEVER** modify files outside declared scope
- **NEVER** delete tests to make gates pass
- **NEVER** use `any` type or disable linting rules to make gates pass
- **NEVER** commit with failing tests

### Config written to `.ship/config.json`

```json
{
  "gates": {
    "tests": true,
    "lint": true,
    "types": true,
    "no_push": true
  },
  "stack": "auto-detected",
  "issue_log": ".ship/issues.md",
  "task_dir": ".ship/tasks/"
}
```

### Hook installed to `.git/hooks/pre-commit`

Runs: lint → types → tests. Blocks commit if any fail. Logs failures to `.ship/issues.md` with timestamp and task ID.

### Traceability in commits

Every commit message follows this format:
```
feat(ship-<task-id>): <title>

agent: claude-code
task: <spec-file-path>
timestamp: <ISO timestamp>
scope: <files modified>
```

This makes every change fully attributable — who (agent), what (task), when (timestamp), where (files).

### Work tree isolation (multi-agent)

For multi-agent flows, each agent gets its own git worktree:
```bash
git worktree add .ship/worktrees/<task-id> HEAD
```
Agent works in its worktree. Changes are merged back only after gates pass. Agents never share a working directory.

---

## `/ship-code:plan <description>`

The main workflow. Takes a plain-English description, produces atomic specs, executes them, commits each one.

### Phase 1 — Decompose

Agent analyzes the request and breaks it into atomic units following "one agent, one task, one prompt":

- Each unit = one clear outcome
- No task touches more than ~3 files
- Dependencies between tasks are explicit
- Scope is locked: files the task can and cannot touch

Output: `.ship/tasks/<slug>/` directory with one spec file per unit.

### Spec file format

```xml
<task>
  <id>001</id>
  <title>Short title</title>
  <goal>What this task achieves in one sentence</goal>
  <scope>
    <can-modify>src/auth/login.ts, src/auth/types.ts</can-modify>
    <cannot-modify>src/db/*, any test files not for this task</cannot-modify>
  </scope>
  <context>
    Relevant snippets, line numbers, existing patterns to follow
  </context>
  <steps>
    Precise numbered steps. No room for inference.
  </steps>
  <acceptance>
    Exact conditions that must be true when done.
    These become the verify checklist.
  </acceptance>
  <gates>lint, types, tests</gates>
</task>
```

### Phase 2 — Execute

For each spec file (sequentially by default, parallel if no dependencies):

1. **Read before writing** — agent scans existing code in the target files for patterns, naming conventions, error handling style, and type patterns. New code must match. This is the recursive quality loop: good existing code produces better new code.
2. Agent reads spec, declares scope out loud
3. Implements changes
4. Runs gates automatically
5. If gates pass → atomic commit with full traceability: `feat(ship-<id>): <title>`
6. If gates fail → diagnose root cause, log to `.ship/issues.md`, fix spec or context, rerun. **Never patch output.**
7. If gates fail twice on the same spec → **stop, escalate to human.** Log the blocker. Do not attempt a third run with the same spec.

### Phase 3 — Human verify

After all tasks complete, agent presents:
- What was built (summary per task)
- Git log of atomic commits
- Gate results
- Open items logged to `.ship/issues.md`

Human reviews. If something is wrong → `/ship-code:plan` again with a corrected description, or `/ship-code:run` to re-execute a single spec.

---

## `/ship-code:run <spec-file>`

Execute a single spec in isolation. Useful for re-running a failed task or executing a manually written spec.

1. Reads the spec file
2. Declares scope (files it will and won't touch)
3. Implements
4. Runs gates
5. Commits if green, logs and halts if red

---

## `/ship-code:verify`

Run all quality gates and report status. Does not commit anything.

Reports:
- ✅ / ❌ Lint
- ✅ / ❌ Type check  
- ✅ / ❌ Tests (with count)
- ✅ / ❌ No forbidden patterns (mocks audit, `any` usage, disabled rules)
- Summary of `.ship/issues.md` open items

If anything fails: identifies root cause category (bad spec, missing context, scope violation, environment issue) and suggests the fix.

---

## `/ship-code:quick <description>`

For small ad-hoc tasks that don't need decomposition. Same guarantees, less ceremony.

1. Agent writes a single inline spec (not saved to disk)
2. Implements in one shot
3. Runs gates
4. Commits if green

Use for: bug fixes, renaming, config tweaks, one-liner additions.
Do not use for: anything touching more than 3 files or with unclear scope.

---

## Anti-slop diagnostics

When output is wrong, use this decision tree before retrying:

| Symptom | Root cause | Fix |
|---|---|---|
| Agent went off-scope | Scope wasn't explicit in spec | Add `<can-modify>` / `<cannot-modify>` to spec |
| Agent made wrong assumptions | Spec left room for inference | Add context snippets, line numbers, examples |
| Gates pass but feature is wrong | Acceptance criteria too vague | Rewrite `<acceptance>` with exact conditions |
| Agent wrote excessive mocks | No-mock policy not in scope | Add explicit note in spec: "no mocks — use real X" |
| Same mistake on retry | Bad spec, not bad agent | Rewrite the spec, don't retry with same spec |
| Unrelated files modified | Scope not enforced | Use hard blocks + scope declaration |

**Rule:** If you retry more than once with the same spec, the spec is the problem.

---

## File structure after `/ship-code:init`

```
.ship/
├── config.json          # Gate settings, stack config
├── HARD_BLOCKS.md        # What agents can never do
├── issues.md            # Centralized agent learnings & blockers
└── tasks/
    └── <task-slug>/
        ├── 001-spec.xml
        ├── 002-spec.xml
        └── summary.md   # Written after execution
.git/hooks/
└── pre-commit           # Gate enforcer
```

---

## Multi-agent notes

When chaining agents (e.g. planner → executor → reviewer):

- Each agent gets its own isolated worktree — no shared filesystem state
- Gates must pass at every handoff — never pass failing work downstream
- Each agent's scope is locked before it starts
- Reviewer agent reads spec + diff only — it does not re-read the whole codebase
- Garbage in = garbage out. If upstream output is bad, fix upstream, don't compensate downstream

### Chain of command — when to escalate

Agents must stop and surface to the human (never silently work around) when:

| Situation | Agent action |
|---|---|
| Task requires files outside declared scope | Stop. Log to `issues.md`. Ask human to update spec scope. |
| Gates fail twice on the same spec | Stop. Log root cause. Human must rewrite the spec. |
| Dependency between tasks is broken | Stop. Log blocker. Human decides how to reorder or fix. |
| Unexpected codebase state changes the plan | Stop. Surface finding. Human decides whether to proceed. |
| Hard block would be violated to complete the task | Stop. Never violate. Escalate. |

Escalation is not failure — it's the system working correctly. Silent workarounds are slop.
