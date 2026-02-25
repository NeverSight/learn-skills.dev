---
name: beads-viewer
description: 'Beads Viewer - Graph-aware triage engine for Beads projects. Computes PageRank, betweenness, critical path, and cycles. Use when triaging beads tasks, analyzing dependency graphs, finding bottlenecks, detecting circular dependencies, planning parallel execution tracks, or generating sprint burndown data.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
---

# Beads Viewer

## Overview

Beads Viewer (BV) is a graph-aware triage engine for Beads projects (`.beads/beads.jsonl`). It computes 9 graph metrics, generates execution plans, and provides deterministic recommendations.

**When to use:** Triaging beads tasks, analyzing dependency graphs, finding bottlenecks, detecting circular dependencies, planning parallel execution tracks, generating sprint burndown data, comparing historical project states.

**When NOT to use:** Parsing raw `beads.jsonl` directly (BV pre-computes graph metrics), simple bead CRUD operations (use `bd` CLI instead), projects without `.beads/beads.jsonl`.

| Capability   | Raw beads.jsonl                | BV Robot Mode                                     |
| ------------ | ------------------------------ | ------------------------------------------------- |
| Query        | "List all issues"              | "List the top 5 bottlenecks blocking the release" |
| Context Cost | High (linear with issue count) | Low (fixed summary struct)                        |
| Graph Logic  | Agent must compute             | Pre-computed (PageRank, betweenness, cycles)      |
| Safety       | Agent might miss cycles        | Cycles explicitly flagged                         |

## Quick Reference

| Command                            | Purpose                             | Key Points                                    |
| ---------------------------------- | ----------------------------------- | --------------------------------------------- |
| `bv --robot-triage`                | Full triage with recommendations    | Start here; includes quick_wins and blockers  |
| `bv --robot-next`                  | Single top pick with claim command  | Minimal context cost                          |
| `bv --robot-plan`                  | Parallel execution tracks           | Faster than `--robot-insights`                |
| `bv --robot-insights`              | Full graph metrics (all 9)          | Check `status` field; expensive               |
| `bv --robot-priority`              | Priority misalignment detection     | Flags misprioritzed items                     |
| `bv --robot-alerts`                | Stale issues, blocking cascades     | Proactive health checks                       |
| `bv --robot-suggest`               | Hygiene: duplicates, missing deps   | Includes cycle break suggestions              |
| `bv --robot-graph`                 | Dependency graph export             | JSON, DOT, or Mermaid format                  |
| `bv --recipe <name> --robot-<cmd>` | Pre-filter before any robot command | Recipes: actionable, high-impact, bottlenecks |
| `bv --robot-triage --label <name>` | Scope to label subgraph             | Reduces noise for focused analysis            |

**CRITICAL:** Never run bare `bv` from an agent session. It launches an interactive TUI that blocks the session. Always use `--robot-*` flags.

## The 9 Graph Metrics

| Metric            | What It Measures                | Key Insight                   |
| ----------------- | ------------------------------- | ----------------------------- |
| **PageRank**      | Recursive dependency importance | Foundational blockers         |
| **Betweenness**   | Shortest-path traffic           | Bottlenecks and bridges       |
| **HITS**          | Hub/Authority duality           | Epics vs utilities            |
| **Critical Path** | Longest dependency chain        | Keystones with zero slack     |
| **Eigenvector**   | Influence via neighbors         | Strategic dependencies        |
| **Degree**        | Direct connection counts        | Immediate blockers/blocked    |
| **Density**       | Edge-to-node ratio              | Project coupling health       |
| **Cycles**        | Circular dependencies           | Structural errors (must fix!) |
| **Topo Sort**     | Valid execution order           | Work queue foundation         |

Metrics compute in two phases: Phase 1 (degree, topo sort, density) is instant; Phase 2 (PageRank, betweenness, HITS, eigenvector, cycles) has a 500ms timeout. Always check the `status` field in output.

## Built-in Recipes

| Recipe        | Purpose                            |
| ------------- | ---------------------------------- |
| `default`     | All open issues sorted by priority |
| `actionable`  | Ready to work (no blockers)        |
| `high-impact` | Top PageRank scores                |
| `blocked`     | Waiting on dependencies            |
| `stale`       | Open but untouched for 30+ days    |
| `triage`      | Sorted by computed triage score    |
| `quick-wins`  | Easy P2/P3 items with no blockers  |
| `bottlenecks` | High betweenness nodes             |

## Robot Output Structure

All robot JSON output includes these standard fields:

| Field                    | Purpose                                                         |
| ------------------------ | --------------------------------------------------------------- |
| `data_hash`              | Fingerprint of beads.jsonl for verifying consistency            |
| `status`                 | Per-metric state: `computed`, `approx`, `timeout`, or `skipped` |
| `as_of` / `as_of_commit` | Present when using `--as-of` for time travel queries            |

Key output sections by command:

- **--robot-triage**: `quick_ref`, `recommendations`, `quick_wins`, `blockers_to_clear`, `project_health`, `commands`
- **--robot-insights**: `bottlenecks`, `keystones`, `influencers`, `hubs`, `authorities`, `cycles`, `clusterDensity`
- **--robot-plan**: `plan.tracks` (parallel work streams), `plan.summary.highest_impact`

## Common Mistakes

| Mistake                                                    | Correct Pattern                                                                                                        |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Running bare `bv` from an agent session                    | Always use `--robot-*` flags; bare `bv` launches an interactive TUI that blocks the agent                              |
| Ignoring the `status` field in robot output                | Always check per-metric status; large graphs may have `approx` or `skipped` metrics due to 500ms timeout               |
| Using `--robot-insights` when only the next task is needed | Use `--robot-next` for a single top pick or `--robot-triage` for quick recommendations; insights is expensive          |
| Not checking for cycles before starting implementation     | Run `bv --robot-insights` and check `.cycles` first; circular dependencies are structural errors that must be resolved |
| Parsing stderr as JSON data                                | Only stdout contains JSON; diagnostics and warnings go to stderr                                                       |
| Stale metrics after bead changes                           | Check `data_hash` field; results are cached by beads.jsonl fingerprint                                                 |
| Wrong recommendations for current work                     | Use `--recipe actionable` to filter to only unblocked, ready-to-work items                                             |

## Delegation

- **Analyze project dependency health and bottlenecks**: Use `Task` agent to run BV robot commands and summarize graph metrics
- **Plan sprint work from triage output**: Use `Plan` agent to interpret triage recommendations and build execution tracks
- **Search for related beads context**: Use `Explore` agent to investigate bead descriptions and find implementation patterns

## References

- [Robot commands, output structures, and jq patterns](references/robot-commands.md)
- [Graph metrics, two-phase analysis, and metric recipes](references/graph-metrics.md)
- [Agent workflows, TUI views, integrations, and time travel](references/workflows.md)
