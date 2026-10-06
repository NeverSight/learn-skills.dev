---
name: plan-graph
description: Build and inspect dependency-aware DAGs from Cursor-style `.plan.md` files that use `name`, `overview`, `todos`, and `isProject`. Use when you need to turn plan files into launch lanes, validate plan structure, reuse or create saved graph state for an exact plan selection, or feed plan-derived work into `subagent-graph` and `helm`.
---

# Plan Graph

Turn plan markdown into a concrete graph instead of hand-waving over the document structure. This skill is for plan-driven orchestration, not for live steering once workers are already moving.

## Handoff Contract

For plan-backed orchestration, treat this as the canonical handoff bundle:

- the exact plan selection: explicit `--plan` paths, or `--plans-root` plus `--glob`
- any explicit `--depends source:target` edges
- the resolved `graph_id`
- `selection_hash`
- `snapshot_path` and `state_dir` when a snapshot exists on disk

Carry the same selection when auto-managed reuse is acceptable. Carry the explicit `graph_id` when downstream work must attach to one exact saved slot regardless of selection context.

## Canonical Inputs

Default search root:

- `./.codex/plans` in the current working directory
- override with `--plans-root`
- or set `CODEX_PLANS_ROOT` or `CODEX_HOME`

Expected frontmatter shape:

- `name`
- `overview`
- `todos`
- `isProject`

Expected todo shape:

- `id`
- `content`
- `status`

Expected todo statuses in the current local corpus:

- `pending`
- `in_progress`
- `completed`

The parser is intentionally tolerant of imperfect plans such as empty names, empty overviews, and `todos: []`. Treat those as warnings unless the calling task explicitly wants strict validation.

Recommended file shape below the frontmatter:

- repeat the plan name as the top-level heading
- add short markdown sections such as `Execution Notes`, `Constraints`, `References`, or `Operator Guidance`
- keep the body focused on narrative guidance that frontmatter cannot express cleanly
- write the body as something a subagent can read end-to-end to understand intent, boundaries, success criteria, and implementation guidance without relying only on the frontmatter

Do not duplicate the overview paragraph or the todo list in the markdown body unless a caller explicitly wants that redundancy. The frontmatter remains the machine-readable source of truth for graphing and status.

When creating new plan files, start from [`references/plan-template.plan.md`](references/plan-template.plan.md) and adapt it instead of inventing the body structure ad hoc.

## Durable State

Do not rely on implicit thread or agent metadata for cross-agent persistence.

- If you pass `--graph-id <id>` or set `GRAPH_ID`, the tool uses that explicit graph slot.
- If you omit `GRAPH_ID`, the tool reuses the latest slot for the same resolved plan selection and rewrites that snapshot from current plan files before reporting.
- A plan selection means both the resolved absolute plan paths and any explicit `--depends` edges.
- If no saved snapshot matches, it creates a managed graph slot automatically from that selection and writes a snapshot for later reuse.
- Persist shared state under `./.codex/plan-graphs/<resolved-graph-id>/` by default.
- Override the snapshot root with `--state-dir`, `CODEX_PLAN_GRAPHS_ROOT`, or `CODEX_HOME`.
- `--write-state` forces persistence for an explicit graph id.
- If you use an explicit `--graph-id` without `--write-state`, only treat `snapshot_path` as real when the command output actually includes it.

This survives across root agent work, spawned workers, explorers, and later resumptions far better than thread-local context.

## Workflow

1. Choose the plan set.
   - Use explicit `--plan` paths when the task already points at specific plans.
   - Otherwise search the default or overridden plans root with `--glob`.
   - If you need to author new plan files first, copy `references/plan-template.plan.md` and then fill in the frontmatter plus the detailed markdown body.
   - Or use `scripts/plan_graph.py generate --breadth N --depth M` to scaffold a plan set and persisted graph state automatically.
2. Validate the plan corpus first.
   - Run `scripts/plan_graph.py validate`.
- Validation covers both parse quality and graph integrity: duplicate plan names or slugs, duplicate todo ids, empty todo content, self-dependencies, dependency cycles, and orphaned plan nodes.
- In a multi-plan selection, every selected plan should participate in at least one dependency edge. If a plan is documentation-only or an umbrella wrapper, either link it explicitly or leave it out of the active graph selection.
- Because inter-plan edges connect the source plan's final todo to the target plan's first todo, wrapper or project-summary plans usually work best as downstream rollup nodes unless their todo sequence is intentionally written to gate all child work.
   - Use `--strict` only when malformed plans should fail the workflow.
3. Start with a quick summary when you need orientation.
   - Run `scripts/plan_graph.py summary`.
   - This gives the per-plan status plus handoff state without flooding the operator with the full DAG.
4. Build the graph when structure matters.
   - Run `scripts/plan_graph.py dag` for a full text or JSON DAG.
   - Run a visual pass with `--format mermaid` whenever you need to confirm roots, parallel branches, blocked lanes, or whether the umbrella project plan is incorrectly acting like an execution node.
   - Mermaid output intentionally omits the plain-text handoff footer, so pair it with a text or JSON `dag`/`frontier` run when you also need the resolved graph id, blockers, or handoff state.
   - Add `--depends source:target` edges when plan-to-plan sequencing is known but not stored in frontmatter.
   - In text mode, this command prints `handoff state` lines for downstream handoff.
5. Surface launchable work.
   - Run `scripts/plan_graph.py frontier --lanes N --max-depth M`.
   - This gives the next executable lane per plan after accounting for completed todos and explicit upstream plan dependencies.
   - In text mode, this command also includes the same `handoff state` footer.
6. Visually check the graph before handing it off.
   - Render the graph with `scripts/plan_graph.py dag --format mermaid`.
   - Confirm the critical path, any parallel lanes, and every `blocked_by` relationship shown by the matching text `dag` or `frontier` run.
   - If the visual graph shows a documentation-only wrapper plan acting like a runnable lane, either remove it from the active selection or add explicit dependencies so it is no longer an orphaned node.
6. Inspect what already exists before minting new work.
   - Run `scripts/plan_graph.py plans` to see existing plan files.
   - Run `scripts/plan_graph.py graphs` to see saved graph snapshots.
   - Run `scripts/plan_graph.py delete-plan` to preview matched plan-file deletion, then rerun with `--yes` to actually delete them.
   - Use `--format json` when you need machine-readable `graph_id`, `selection_hash`, `snapshot_path`, `state_dir`, `plan_count`, `edge_count`, or `selected_plan_paths` for downstream operators.
7. Preserve exact targeting across subagents.
   - Rerun any `--plan` / `--glob` selection plus the same `--depends` edges to resolve the same auto-managed graph slot.
   - For strict targeting, pass an explicit `--graph-id` (or reuse the resolved one from prior output).
   - Prefer `--format json` or `graphs --format json` whenever you need the exact `graph_id`, `selection_hash`, `state_dir`, or `snapshot_path`.
8. Persist or reuse the shared snapshot when the graph will feed other skills.
   - In the common case, rerun the same plan selection and let the tool auto-reuse the saved slot.
   - Hand the resolved `GRAPH_ID` to `subagent-graph`, `dag`, or `helm` only when another tool or agent truly needs that exact slot.

## Commands

Use the bundled CLI instead of re-parsing plan files ad hoc:

```bash
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py generate --plans-root ./.codex/plans --graph-id example-graph --title-prefix "Example Plan" --slug-prefix example-plan --breadth 2 --depth 2 --todo-count 3
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py generate --plans-root ./.codex/plans --state-dir ./.codex/plan-graphs --title-prefix "Migration Plan" --slug-prefix migration-plan --breadth 3 --depth 2 --format json
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py plans --glob '*.plan.md'
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py graphs
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py delete-plan --plan "$PLAN_PATH"
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py delete-plan --plan "$PLAN_PATH" --yes
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py validate --glob '*.plan.md'
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py summary --plan "$PLAN_PATH"
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py summary --glob '*subagent*.plan.md' --format json
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py dag --plan "$PLAN_PATH" --format mermaid
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py dag --plans-root ./.codex/plans --glob '*subagent*.plan.md' --depends source:target --format mermaid
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py dag --plan "$PLAN_PATH"
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py frontier --glob '*subagent*.plan.md' --lanes 3 --max-depth 2 --format json
python /Users/zackjackson/.codex/skills/plan-graph/scripts/plan_graph.py frontier --glob '*subagent*.plan.md' --lanes 3 --max-depth 2 --graph-id subagents-v1 --write-state
```

## Boundaries

- Use `subagent-graph` after the plan graph is known and you need launch waves, ownership, and merge sequencing.
- Use `dag` when you only need the current frontier, blocked lanes, or plan progress. The `dag` skill is the frontier/status companion, not the full DAG renderer.
- Use `helm` when workers are already active and the problem is operational steering.
- `delete-plan` removes matched plan files only. It does not prune saved graph snapshots.
- `generate` is for scaffolding plan files and a matching saved graph slot. It is not a substitute for execution planning after real todo content is known.

Read `references/cursor-plan-format.md` when you need the exact frontmatter assumptions, the on-disk state layout, or the saved-slot matching rules.
