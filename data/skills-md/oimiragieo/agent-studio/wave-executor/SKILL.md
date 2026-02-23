---
verified: true
lastVerifiedAt: 2026-02-19T22:00:00.000Z
name: wave-executor
description: Fresh-process orchestration for EPIC-tier batch pipelines. Spawns a new Bun process per wave via the Claude Agent SDK, preventing GC-related crashes in long-running sessions.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Bash, Glob, Grep]
aliases: [batch-executor, ralph-loop]
agents:
  - router
  - master-orchestrator
  - planner
category: Planning & Architecture
tags:
  - wave
  - orchestration
  - batch
  - pipeline
  - epic
best_practices:
  - Use for EPIC-tier batch work (>10 artifacts, >5 waves)
  - Always provide a plan file with wave definitions
  - Prefer append-only writes to prevent regression
  - Monitor inventory file for progress between waves
error_handling: strict
streaming: supported
---

# Wave Executor

## Overview

Wave Executor runs EPIC-tier batch pipelines by spawning a **fresh Claude Code process per wave** via the Claude Agent SDK. Each wave gets a clean Bun runtime with zero accumulated `spawn()` or `abort_signal` state, preventing the JSC garbage collector use-after-free crash (oven-sh/bun, anthropics/claude-code#21875, #27003) that occurs when a single Bun process handles thousands of concurrent subagent spawns.

This is the framework's implementation of the Ralph Wiggum pattern: iteration over fresh processes with file-based coordination.

## When to Use

**Use this skill when:**

- EPIC-tier batch work: >10 artifacts, >5 waves
- Multi-wave skill updates, bundle generation, or mass refactoring
- Any pipeline expected to run >30 minutes with parallel subagents
- Work that previously crashed due to Bun segfaults

**Do NOT use for:**

- Simple 1-3 skill updates (use `skill-updater` directly)
- Single-skill work (use `Task()` subagent)
- Work that fits in one context window (just do it inline)

## How It Works

```
Router invokes wave-executor via Bash
  │
  └─ node .claude/tools/cli/wave-executor.mjs --plan <path>
       │  (runs on system Node.js — NOT Bun)
       │
       ├─ Reads plan.json with wave definitions
       ├─ Reads inventory.json for resume state
       │
       ├─ For each pending wave:
       │    ├─ SDK query() → NEW Bun process (fresh GC)
       │    ├─ Claude executes wave tasks
       │    ├─ Streams output to stdout
       │    ├─ Bun process exits → memory freed
       │    ├─ Updates inventory.json
       │    └─ Sleeps → next wave
       │
       └─ Returns JSON summary
```

Key invariant: no single Bun process accumulates more than ~100 spawns.

## Invocation

**Via Bash (agents):**

```bash
node .claude/tools/cli/wave-executor.mjs --plan <path> --json
```

**Via slash command (users):**

```
/wave-executor --plan .claude/context/plans/my-plan.json
```

**CLI flags:**

| Flag               | Default             | Description                     |
| ------------------ | ------------------- | ------------------------------- |
| `--plan <path>`    | required            | Path to wave plan JSON          |
| `--model <model>`  | `claude-sonnet-4-6` | Model for wave execution        |
| `--max-turns <n>`  | `50`                | Max conversation turns per wave |
| `--start-from <n>` | `1`                 | Resume from wave N              |
| `--dry-run`        | `false`             | Preview without executing       |
| `--json`           | `false`             | Machine-readable output         |

## Plan File Format

```json
{
  "name": "enterprise-bundle-generation",
  "waves": [
    {
      "id": 1,
      "skills": ["rust-expert", "python-backend-expert", "typescript-expert"],
      "domain": "language",
      "promptTemplate": "Update enterprise bundle files for skills: {skills}. Read each SKILL.md and .claude/rules/ file. Do 3-5 WebSearch queries for current {domain} tools and patterns. Generate domain-specific bundle files (append-only, never overwrite non-stubs). Validate JSON schemas and Node.js syntax. Commit results."
    },
    {
      "id": 2,
      "skills": ["nextjs-expert", "react-expert", "svelte-expert"],
      "domain": "web-framework"
    }
  ],
  "config": {
    "model": "claude-sonnet-4-6",
    "maxTurnsPerWave": 50,
    "sleepBetweenWaves": 3000,
    "inventoryPath": ".claude/context/runtime/wave-inventory.json"
  }
}
```

Each wave must have `id` (number) and `skills` (non-empty array). Optional: `domain`, `promptTemplate`.

## Inventory Tracking

The executor maintains an inventory file at the configured path (default `.claude/context/runtime/wave-inventory.json`). This enables:

- **Resume from crash:** `--start-from N` picks up where a failed run left off
- **Progress monitoring:** read the inventory file to see completed waves
- **Cost tracking:** each wave records its cost

## Integration with Router

The router should use this skill when the planner classifies work as EPIC-tier:

1. Planner creates a plan file with wave definitions
2. Router invokes: `Skill({ skill: 'wave-executor' })`
3. Agent runs: `node .claude/tools/cli/wave-executor.mjs --plan <path> --json`
4. Router reads JSON result for success/failure

The router's Bun process stays idle during execution (single Bash call) — no subagent spawning, no hook accumulation.

## Memory Protocol (MANDATORY)

**Before starting:**

- Read `.claude/context/memory/learnings.md` for prior wave execution learnings
- Check inventory file for resume state

**After completing:**

- Append wave execution summary to `.claude/context/memory/learnings.md`
- Record any errors to `.claude/context/memory/issues.md`
- Record architecture decisions to `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
