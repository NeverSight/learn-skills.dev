---
name: repo-updater
description: 'Repo Updater - Multi-repo synchronization with AI-assisted review orchestration. Parallel sync, agent-sweep for dirty repos, ntm integration, git plumbing. 17K LOC Bash CLI. Use when syncing multiple GitHub repositories, running agent-sweep on uncommitted changes, or orchestrating AI-assisted code review across repos.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
---

# Repo Updater

Bash CLI for synchronizing dozens or hundreds of GitHub repositories with AI-assisted code review and agent-sweep for uncommitted changes.

## Critical Concepts

| Concept           | Rule                                                                                 |
| ----------------- | ------------------------------------------------------------------------------------ |
| Git plumbing only | Never parse human-readable output; use `rev-list`, `status --porcelain`, `rev-parse` |
| Stream separation | Human-readable → stderr; data → stdout (`--json 2>/dev/null \| jq`)                  |
| No global `cd`    | All git operations use `git -C`                                                      |

## Essential Commands

| Command                    | Purpose                                            |
| -------------------------- | -------------------------------------------------- |
| `ru sync`                  | Sync all configured repos (add `-j8` for parallel) |
| `ru sync --dry-run`        | Preview what would happen                          |
| `ru sync --resume`         | Resume interrupted sync                            |
| `ru status`                | Read-only check of all repos                       |
| `ru add owner/repo`        | Add repo to sync list                              |
| `ru remove owner/repo`     | Remove from list                                   |
| `ru list`                  | Show configured repos                              |
| `ru prune`                 | Detect orphaned repos                              |
| `ru doctor`                | System health check                                |
| `ru review --plan`         | Discover issues/PRs for AI review                  |
| `ru review --apply --push` | Apply reviewed changes                             |
| `ru agent-sweep`           | Process repos with uncommitted changes             |
| `ru agent-sweep -j4`       | Parallel agent processing                          |

## AI Review Priority Scoring

| Factor     | Points | Logic                                   |
| ---------- | ------ | --------------------------------------- |
| Type       | 0-20   | PRs: +20, Issues: +10, Draft PRs: -15   |
| Labels     | 0-50   | security/critical: +50, bug/urgent: +30 |
| Age (bugs) | 0-50   | >60 days: +50, >30 days: +30            |
| Recency    | 0-15   | Updated <3 days: +15, <7 days: +10      |
| Staleness  | -20    | Recently reviewed: -20                  |

Levels: CRITICAL (≥150), HIGH (≥100), NORMAL (≥50), LOW (<50)

## Agent Sweep Phases

| Phase       | Default Timeout | Action                                                   |
| ----------- | --------------- | -------------------------------------------------------- |
| 1: Planning | 300s            | Analyze uncommitted changes, generate commit plan        |
| 2: Commit   | 600s            | Validate plan, stage files, create commit, quality gates |
| 3: Release  | 300s (opt-in)   | Determine version bump, create tag/release               |

Execution modes: `agent` (full workflow), `plan` (phase 1 only), `apply` (phase 2+3)

## Update Strategies

| Strategy  | Behavior                                       |
| --------- | ---------------------------------------------- |
| `ff-only` | Fast-forward only; fails if diverged (default) |
| `rebase`  | Rebase local commits on top of remote          |
| `merge`   | Create merge commit if needed                  |

## Exit Codes

| Code | Meaning                            |
| ---- | ---------------------------------- |
| 0    | All repos processed successfully   |
| 1    | Some repos failed                  |
| 2    | Conflicts or quality gate failures |
| 3    | System/dependency error            |
| 4    | Invalid arguments                  |
| 5    | Interrupted (use `--resume`)       |

## Environment Variables

| Variable             | Default          | Description                          |
| -------------------- | ---------------- | ------------------------------------ |
| `RU_PROJECTS_DIR`    | `/data/projects` | Base directory for repos             |
| `RU_LAYOUT`          | `flat`           | Path layout (flat, owner-repo, full) |
| `RU_PARALLEL`        | `1`              | Parallel workers                     |
| `RU_TIMEOUT`         | `30`             | Network timeout (seconds)            |
| `RU_UPDATE_STRATEGY` | `ff-only`        | Pull strategy                        |
| `GH_TOKEN`           | (from gh CLI)    | GitHub token                         |

## Common Mistakes

| Mistake                                                           | Correct Pattern                                                            |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Parsing human-readable git output (e.g., `git status` text)       | Use git plumbing: `rev-list`, `status --porcelain`, `rev-parse`            |
| Using `cd` to change into repo directories                        | Use `git -C <path>` for all git operations                                 |
| Mixing data and human-readable output on the same stream          | Data goes to stdout, human-readable to stderr (`--json 2>/dev/null \| jq`) |
| Running sync without `--dry-run` first on unfamiliar repos        | Always preview with `ru sync --dry-run` before executing                   |
| Using `service_role` key or bypassing auth in agent-sweep scripts | Follow security guardrails; agent-sweep has preflight checks for a reason  |

## Delegation

- **Discover which repos have uncommitted changes or are out of sync**: Use `Explore` agent to run `ru status` and analyze the output
- **Process dirty repos with agent-sweep across multiple repositories**: Use `Task` agent to run `ru agent-sweep -j4` and handle quality gate failures
- **Plan a multi-repo sync strategy with review prioritization**: Use `Plan` agent to design sync order, parallelism settings, and review budget allocation

## References

- [Commands](references/commands.md) — sync, status, repo management, diagnostics, output modes, jq examples
- [Review System](references/review-system.md) — two-phase workflow, session drivers, cost budgets, priority scoring
- [Agent Sweep](references/agent-sweep.md) — three-phase workflow, preflight checks, security guardrails, execution modes
- [Configuration](references/configuration.md) — XDG directory structure, repo list format, layout modes, per-repo config
- [Troubleshooting](references/troubleshooting.md) — common issues, debug mode, preflight failure debugging, integration points
