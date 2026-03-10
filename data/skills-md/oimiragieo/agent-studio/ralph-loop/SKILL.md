---
name: ralph-loop
description: Autonomous iteration loop with dual-mode support. Standalone mode uses Stop hooks (RALPH_ACTIVE=1). Multi-agent mode uses router-managed iteration. Never traps the host/router session.
version: 2.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
agents: [developer, qa, devops, master-orchestrator]
category: 'Orchestration'
tags: [ralph, autonomous, loop, iteration, stop-hook, verification, audit]
best_practices:
  - Always define clear completion criteria before starting
  - Set max iterations to prevent runaway loops
  - Use verification commands as completion gates
  - Check guardrails.md before each iteration
error_handling: graceful
streaming: supported
verified: true
lastVerifiedAt: 2026-02-28T00:00:00.000Z
skills:
  - task-management-protocol
  - ripgrep
  - code-semantic-search
  - token-saver-context-compression
  - verification-before-completion
  - memory-search
---

# Ralph Loop

Autonomous iteration loop for Claude Code with dual-mode support. Named after the Ralph Wiggum technique popularized in the Claude Code community (Dec 2025 - Feb 2026).

## Purpose

Enable Claude Code to work autonomously on well-defined tasks until genuine completion, without manual re-prompting. The skill provides:

1. **Dual-mode architecture** — Standalone mode (Stop hook) or multi-agent mode (router-managed iteration)
2. **RALPH_ACTIVE env var guard** — Stop hook only activates when `RALPH_ACTIVE=1` is set, preventing host/router trapping
3. **State persistence** — JSON state file tracks iteration count, timestamps, findings
4. **Circuit breaker** — Detects repeated failures and exits gracefully
5. **Verification-first exit** — Completion signal only accepted when validation commands pass
6. **Guardrails** — Accumulated lessons from past failures prevent repeated mistakes

## When to Use

- Well-defined tasks with clear, testable success criteria
- Iterative work (get tests passing, fix lint errors, audit codebase)
- Overnight or background autonomous runs
- Multi-phase audits with structured findings logs

## When NOT to Use

- Subjective goals ("make the code better")
- One-off fixes that don't need iteration
- Tasks requiring human judgment at each step
- Exploratory research without clear deliverables

## Architecture — Two Modes

### Mode 1: Standalone (Stop Hook)

For single-session use. The Stop hook keeps the session alive until completion. Requires `RALPH_ACTIVE=1` env var (set by the launcher scripts).

```
User runs ralph-audit.sh/bat (sets RALPH_ACTIVE=1)
    |
    v
Claude works on task (reads PROMPT.md)
    |
    v
Claude attempts to exit
    |
    v
Stop hook intercepts (ralph-stop-hook.cjs)
    |
    +-- RALPH_ACTIVE != '1'? --> YES --> exit(0) immediately (no-op)
    |
    +-- Completion signal found? --> YES --> Clear state, exit(0)
    |
    +-- Max iterations reached? --> YES --> Clear state, exit(0)
    |
    +-- NO --> Increment iteration, save state, re-inject prompt, block exit
```

### Mode 2: Router-Managed (Multi-Agent) -- Primary mode for agent-studio

This is the primary mode within agent-studio. The router manages iteration by spawning and re-spawning QA agents via `Task()`. No Stop hook is involved -- the router itself controls the loop lifecycle. The state file at `.claude/context/runtime/ralph-state.json` within agent-studio tracks iteration progress.

```
Router receives /ralph-loop command
    |
    v
Router spawns QA agent with audit prompt via Task()
    |
    v
QA agent completes, reports findings via TaskUpdate()
    |
    v
Router checks audit state file (.claude/context/runtime/ralph-state.json)
    |
    +-- RALPH_AUDIT_COMPLETE_NO_FINDINGS? --> Done
    |
    +-- RALPH_ITERATION_COMPLETE? --> Spawn another QA agent
    |
    +-- Max iterations? --> Report and stop
```

**Why two modes:** Stop hooks fire on the host session, not on subagents. In multi-agent setups (like agent-studio), the Stop hook would trap the router. The `RALPH_ACTIVE` guard ensures the hook is a no-op unless explicitly activated by a standalone launcher. In agent-studio, Mode 2 is used exclusively -- the router orchestrates iteration without any Stop hook registration.

## Components

### Skill Bundle (included in this skill directory)

| File                    | Relative Path                          | Purpose                                         |
| ----------------------- | -------------------------------------- | ----------------------------------------------- |
| Main script             | `scripts/main.cjs`                     | CLI for status/reset/config of ralph loop state |
| Pre-execute hook        | `hooks/pre-execute.cjs`                | Input validation before skill execution         |
| Post-execute hook       | `hooks/post-execute.cjs`               | Output validation after skill execution         |
| Input schema            | `schemas/input.schema.json`            | Input validation schema                         |
| Output schema           | `schemas/output.schema.json`           | Output contract schema                          |
| Implementation template | `templates/implementation-template.md` | PROMPT.md and launcher templates                |
| Skill rule              | `rules/ralph-loop.md`                  | Skill-specific rules                            |

### Project-Level Files (set up per-project by the user)

These files are NOT part of the skill bundle. They live in the hosting project's `.claude/` directory and must be created/configured by the user or via the implementation template.

| File            | Project Path                               | Purpose                                                    |
| --------------- | ------------------------------------------ | ---------------------------------------------------------- |
| Stop hook       | `.claude/hooks/ralph-stop-hook.cjs`        | Loop controller (stdin -> transcript check -> re-inject)   |
| Prompt          | `.claude/ralph/PROMPT.md`                  | Audit/task instructions re-injected each iteration         |
| State           | `.claude/context/runtime/ralph-state.json` | Iteration count, timestamps, findings count (auto-created) |
| Guardrails      | `.claude/ralph/guardrails.md`              | Learned lessons from past failures                         |
| Launcher (bash) | `.claude/ralph/ralph-audit.sh`             | Unix/macOS launcher script (sets RALPH_ACTIVE=1)           |
| Launcher (bat)  | `.claude/ralph/ralph-audit.bat`            | Windows launcher script (sets RALPH_ACTIVE=1)              |
| Settings        | `.claude/settings.json`                    | Stop hook registration (Mode 1 only)                       |

## Usage

### Standalone Mode (Stop Hook)

```bash
# From your project's workspace root — sets RALPH_ACTIVE=1 automatically
.claude/ralph/ralph-audit.sh      # Unix/macOS
.claude\ralph\ralph-audit.bat     # Windows
```

### Manual Standalone Start

```bash
# Must set RALPH_ACTIVE=1 yourself for the Stop hook to activate
export RALPH_ACTIVE=1
claude --print-output-format text < .claude/ralph/PROMPT.md
```

### Multi-Agent Mode (Router-Managed)

Use the `/ralph-loop` command within agent-studio, or have the router spawn QA agents with the audit prompt. The router manages iteration; no Stop hook is involved.

### Custom Prompt

Create a custom `PROMPT.md` with:

1. **Mission** — What the agent must accomplish
2. **Scope** — Specific areas to audit/fix
3. **Validation commands** — Commands that must pass
4. **Completion condition** — The exact completion signal string

### Completion Signals

| Signal                                        | Meaning                                  |
| --------------------------------------------- | ---------------------------------------- |
| `RALPH_AUDIT_COMPLETE_NO_FINDINGS`            | All validations pass, zero open findings |
| `RALPH_ITERATION_COMPLETE: N findings remain` | Progress made, N findings still open     |

## Stop Hook Protocol

The stop hook (`ralph-stop-hook.cjs`) follows this protocol:

0. **GUARD 0: Check `RALPH_ACTIVE` env var** — if not `'1'`, exit 0 immediately (no stdin read, no file checks, no-op). This is the critical protection that prevents the hook from trapping the host/router session.
1. Read stdin (Claude Code transcript JSON)
2. Check `stop_hook_active` guard (prevent infinite re-triggering)
3. Check if `ralph-state.json` exists (no state = no active loop)
4. Check transcript for `RALPH_AUDIT_COMPLETE_NO_FINDINGS`
   - Found → clear state file, exit 0 (allow exit)
5. Load state from `ralph-state.json`, increment iteration
6. Check for progress signal (`RALPH_ITERATION_COMPLETE`)
7. Check circuit breaker (findings count stuck for N iterations)
8. Check max iterations (default: 25)
   - Reached → clear state, exit 0 (force stop)
9. Save updated state
10. Read `PROMPT.md` and write to stdout as JSON `{ decision: 'block', reason: <prompt> }`
11. Exit 0 (with block decision in stdout)

### Exit Codes

| Code | Meaning                                         |
| ---- | ----------------------------------------------- |
| 0    | Allow exit (complete, max iterations, or error) |
| 2    | Block exit, stdout fed back as next prompt      |

## Configuration

### Environment Variables

| Variable                          | Default                            | Description                                                                                        |
| --------------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------- |
| `RALPH_ACTIVE`                    | (unset)                            | Must be `1` to activate the Stop hook. Set by launcher scripts. Without this, the hook is a no-op. |
| `RALPH_MAX_ITERATIONS`            | 25                                 | Maximum loop iterations                                                                            |
| `RALPH_COMPLETION_SIGNAL`         | `RALPH_AUDIT_COMPLETE_NO_FINDINGS` | String that signals completion                                                                     |
| `RALPH_CIRCUIT_BREAKER_THRESHOLD` | 3                                  | Consecutive iterations with unchanged findings count before circuit breaker trips                  |

### State File Schema

```json
{
  "iteration": 3,
  "startedAt": "2026-02-28T10:00:00Z",
  "lastRunAt": "2026-02-28T10:15:00Z",
  "lastFindingsCount": 5
}
```

## Writing Effective Prompts

### Structure

```markdown
# Mission

One-line directive.

## Before Doing Anything

Step 1: Read previous findings (if exists)
Step 2: Load context/skills

## Scope

Numbered list of areas to audit/fix.

## Validation Commands

Commands that must pass for completion.

## Findings Log

Where to write findings (path + format).

## Completion Condition

Exact signal strings and when to use each.
```

### Best Practices

1. **Binary criteria** — "All tests pass" not "code is good"
2. **Validation commands** — Include runnable commands (pnpm test, pnpm lint)
3. **Findings format** — Structured findings with severity, file, status
4. **Idempotent** — Prompt must work correctly on any iteration (read state first)
5. **Context management** — Include token-saver invocation for long sessions

## Guardrails Pattern

The `guardrails.md` file accumulates "Signs" — lessons learned from failures:

```markdown
### Sign: [Name]

- **Trigger**: When this applies
- **Instruction**: What to do
- **Added after**: What failure taught this
```

Agents should read guardrails.md at the start of each iteration and add new Signs when they encounter novel failure modes.

## Enforcement Hooks

Input validated against `schemas/input.schema.json` before execution.
Output contract defined in `schemas/output.schema.json`.

## Anti-Patterns

| Anti-Pattern                         | Why It Fails                                    | Correct Approach                                |
| ------------------------------------ | ----------------------------------------------- | ----------------------------------------------- |
| No max iterations                    | Infinite loop burns tokens                      | Always set `maxIterations` (default 25)         |
| Vague completion criteria            | Agent claims "done" prematurely                 | Use binary pass/fail validation commands        |
| No state persistence                 | Progress lost on context reset                  | Write findings to file, read at iteration start |
| Stop hook without RALPH_ACTIVE guard | Traps host/router session in multi-agent setups | Check `RALPH_ACTIVE=1` before any other logic   |
| Running standalone mode from router  | Router gets trapped by Stop hook                | Use router-managed iteration (Mode 2) instead   |
| No guardrails                        | Same mistakes repeated each iteration           | Maintain guardrails.md with learned Signs       |

## Iron Laws

1. **NO LOOP WITHOUT VERIFICATION** — Completion signal must be backed by passing validation commands
2. **NO LOOP WITHOUT MAX ITERATIONS** — Every loop must have a safety cap
3. **NO LOOP WITHOUT STATE FILE** — Progress must be persisted to survive context resets
4. **NO LOOP WITHOUT GUARDRAILS** — Failures must be recorded to prevent repetition
5. **RALPH_ACTIVE GUARD FIRST** — Stop hook must check `RALPH_ACTIVE=1` env var before reading stdin, checking files, or any other logic. This is the primary protection against trapping the host/router.

## Memory Protocol (MANDATORY)

**Before starting:**

Read `.claude/context/memory/learnings.md` using the `Read` tool.

Check for:

- Previously run ralph loops and their outcomes
- Known audit patterns and failure modes
- User preferences for iteration limits

**After completing:**

- Loop completed successfully → Append summary to `learnings.md`
- New guardrail discovered → Add Sign to `.claude/ralph/guardrails.md`
- Architecture decision → Append to `decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
