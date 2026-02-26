---
name: spec-kit-parallel-orchestrator
description: Parallel orchestration skill for Spec Kit workflows. When users mention spec kit, enter /speckit.* or /prompts:speckit.* commands, request spec kit workflow prompt, or need multi-agent collaboration, this skill must be triggered. It validates stages and dependencies first, then splits tasks into 3-6 parallel subtasks, aggregates results, and recursively proceeds to the next round.
---

# Spec Kit Parallel Orchestrator

## Overview

Transforms spec kit workflows from "single-threaded execution" to "3-6 Sub Agent parallel + stage aggregation". Prioritizes parallel execution for independent nodes, strictly serial execution for strong dependency chains.

## Trigger Conditions (Must Match)

Invoke this skill when any condition is met:

1. User explicitly enters `/speckit.` prefixed commands, e.g., `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`
2. Codex CLI compatible form `/prompts:speckit.` also matches
3. User mentions "spec kit workflow / spec-driven" and requests breakdown, planning, implementation
4. User requests "parallel task splitting" or "multi-agent concurrent + stage aggregation"

## State Machine

```
pending → in_progress → verifying → passing
               ↓              ↓
           blocked  ←  failed
```

| Status | Trigger |
|--------|---------|
| `pending` | Initial state |
| `in_progress` | `harness-start.sh` selects task |
| `verifying` | `harness-end.sh` begins verification |
| `passing` | All gates passed |
| `failed` | E2E test failed |
| `blocked` | Dependency incomplete or environment check failed |

## Harness Artifacts

```
specs/harness/
├── feature_list.json     # Feature definitions + status
├── progress.log.md       # Session history
├── session_state.json    # Current context
└── init.sh               # Environment check
```

## Stage Alignment (github/spec-kit)

1. Stage order: `constitution -> specify -> clarify -> plan -> tasks -> implement`
2. `/speckit.tasks` parallel semantics: only parallelizable tasks run concurrently
3. `/speckit.implement` must respect task dependencies

## Execution Rules

1. Validate stage and dependency analysis first
2. Split into **3-6** subtasks (3 for medium, 4-6 for complex)
3. Each subtask specifies: goal, input, output, boundary, file scope
4. Only parallelizable nodes execute concurrently
5. No write conflicts between subtasks
6. Aggregate results, then proceed to next round

## Gate Enforcement

| Gate | Verification |
|------|--------------|
| Working Tree Clean | `git status` |
| New Commit Exists | Compare commits |
| E2E Passed | Custom command |

## Output Template

Each round outputs:
1. Parallel task list (3-6)
2. Completion status and outputs
3. Conflicts/blockers
4. Aggregation conclusion
5. Next round plan

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `harness-lib.sh` | Common functions |
| `harness-init.sh` | Initialize |
| `harness-start.sh` | Start session |
| `harness-end.sh` | End session |
| `harness-pick-next.sh` | Select task |
| `harness-commit.sh` | Commit progress |
| `harness-verify-e2e.sh` | E2E verify |
| `harness-status.sh` | Status view |

## References

- `references/examples.md` - Prompt templates
- `references/best-practices.md` - Best practices
- [Anthropic: Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
