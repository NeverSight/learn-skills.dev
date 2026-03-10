---
name: swain-do
description: Bootstrap, install, and operate an external task-management CLI as the source of truth for agent execution tracking (instead of built-in todos). Provides the abstraction layer between swain-design intent (implementation plans and tasks) and concrete CLI commands. MUST be invoked when any implementation-tier artifact (SPEC, STORY, BUG) comes up for implementation — create a tracked plan before writing code. Optional but recommended for complex SPIKEs. For coordination-tier artifacts (EPIC, VISION, JOURNEY), swain-design must decompose into implementable children first — this skill tracks the children, not the container. Also use for standalone tasks that require backend portability, persistent progress across agent runtimes, or external supervision. Use this skill whenever the user asks to track tasks, create an implementation plan, check what to work on next, see task status, manage dependencies between work items, or close/abandon tasks — even if they don't mention "execution tracking" explicitly.
license: UNLICENSED
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  short-description: Bootstrap and operate external task tracking
  version: 2.3.0
  author: cristos
---

# Execution Tracking

Abstraction layer for agent execution tracking. Other skills (e.g., swain-design) express intent using abstract terms; this skill translates that intent into concrete CLI commands.

**Before first use:** Read [references/bd-cheatsheet.md](references/bd-cheatsheet.md) for complete command syntax, flags, ID formats, and anti-patterns.

## Artifact handoff protocol

This skill receives handoffs from swain-design based on a four-tier tracking model:

| Tier | Artifacts | This skill's role |
|------|-----------|-------------------|
| **Implementation** | SPEC, STORY, BUG | Create a tracked implementation plan and task breakdown before any code is written |
| **Coordination** | EPIC, VISION, JOURNEY | Do not track directly — swain-design decomposes these into children first, then hands off the children |
| **Research** | SPIKE | Create a tracked plan when the research is complex enough to benefit from task breakdown |
| **Reference** | ADR, PERSONA, RUNBOOK | No tracking expected |

If invoked directly on a coordination-tier artifact (EPIC, VISION, JOURNEY) without prior decomposition, defer to swain-design to create child SPECs or STORYs first, then create plans for those children.

## Term mapping

Other skills use these abstract terms. This skill maps them to the current backend (`bd`):

| Abstract term | Meaning | bd command |
|---------------|---------|------------|
| **implementation plan** | Top-level container grouping all tasks for a spec artifact | `bd create "Title" -t epic --external-ref <SPEC-ID> --json` |
| **task** | An individual unit of work within a plan | `bd create "Title" -t task --parent <epic-id> --json` |
| **origin ref** | Immutable link from a plan to the spec that seeded it | `--external-ref <ID>` flag on epic creation |
| **spec tag** | Mutable label linking a task to every spec it affects | `--labels spec:<ID>` on create, `--add-label spec:<ID>` on update |
| **dependency** | Ordering constraint between tasks | `bd dep add <child> <parent>` (child depends on parent) |
| **ready work** | Unblocked tasks available for pickup | `bd ready --json` (NOT `bd list --ready`) |
| **claim** | Atomically take ownership of a task | `bd update <id> --claim --json` |
| **complete** | Mark a task as done | `bd close <id> --reason "..."` |
| **abandon** | Close a task that will not be completed | `bd close <id> --reason "Abandoned: <why>" --json` |
| **escalate** | Abandon + invoke swain-design to update upstream artifacts | Abandon, then invoke swain-design skill |

## Configuration

The skill stores persistent project-level configuration in `.agents/execution-tracking.vars.json`. This file is created on first run and checked on every subsequent invocation.

### First-run setup

If `.agents/execution-tracking.vars.json` does not exist, create it by asking the user the questions below (use sensible defaults if the user says "just use defaults"):

| Key | Type | Default | Question |
|-----|------|---------|----------|
| `use_dolt` | boolean | `false` | "Should bd use Dolt for remote sync? (Requires a running Dolt server)" |
| `auto_prime` | boolean | `true` | "Run `bd prime` automatically on bootstrap to load workflow context?" |
| `fallback_format` | `"jsonl"` \| `"markdown"` | `"jsonl"` | "If bd is unavailable, use JSONL or Markdown for the fallback ledger?" |

Write the file as pretty-printed JSON:

```json
{
  "use_dolt": false,
  "auto_prime": true,
  "fallback_format": "jsonl"
}
```

On subsequent runs, read the file and apply its values — don't re-ask.

### Applying config

- **`use_dolt`**: When `false`, skip all `bd dolt *` commands (start, stop, push, pull). When `true`, run `bd dolt start` during bootstrap and `bd dolt push` at session end.
- **`auto_prime`**: When `true`, run `bd prime` at bootstrap step 7. When `false`, skip it.
- **`fallback_format`**: Controls the format used by the [Fallback](#fallback) section.

## Bootstrap workflow

1. **Load config:** Read `.agents/execution-tracking.vars.json`. If missing, run [first-run setup](#first-run-setup) above.
2. **Check availability:** `command -v bd`
3. **If missing, install:**
   - macOS: `brew install beads`
   - Linux: `cargo install beads`
   - If install fails, go to [Fallback](#fallback).
4. **Check for existing database:** look for `.beads/` directory.
5. **If no `.beads/`, initialize:** `bd init`.
6. **Validate:** `bd doctor --json`. If errors, try `bd doctor --fix`.
7. **If `use_dolt` is `true`:** start the Dolt server with `bd dolt start`.
8. **If `git status` shows modified `.beads/dolt-*.pid` or `.beads/dolt-server.activity`:** these are ephemeral runtime files that were tracked by mistake. See `.beads/README.md` § "Remediation: Untrack Ephemeral Runtime Files" for the fix.
9. **If `auto_prime` is `true`:** `bd prime` for dynamic workflow context.

## Statuses

bd accepts exactly four status values: `open`, `in_progress`, `blocked`, `closed`. It rejects aliases like `todo` or `done`. See the cheatsheet for the full status table and valid values.

To express abandonment, use `bd close <id> --reason "Abandoned: ..."` — see [Escalation](#escalation).

## Operating rules

1. **Always use `--json`** on create/update/close — bd's human-readable output varies between versions, but JSON is stable and machine-parseable. Capture issue IDs from the JSON response so subsequent commands can reference them reliably.
2. **Always include `--description`** when creating issues — a title alone loses the "why" behind a task. Future agents (or your future self) picking up this work need enough context to act without re-researching.
3. Create/update tasks at the start of work, after each major milestone, and before final response — this keeps the external tracker useful as a live dashboard rather than a post-hoc record.
4. Keep task titles short and action-oriented — they appear in `bd ready` output, tree views, and notifications where space is limited.
5. Store handoff notes in task notes (`--notes` or `--append-notes`) rather than ephemeral chat context — chat history is lost between sessions, but task notes persist and are visible to any agent or observer.
6. Include references to related artifact IDs in labels (e.g., `spec:SPEC-003`) — this makes it possible to query all work touching a given spec with `bd list -l spec:SPEC-003`.
7. **Never use `bd edit`** — it opens `$EDITOR` (vim/nano) which blocks agents. Use `bd update` with inline flags instead.
8. **Prefix abandonment reasons with `Abandoned:`** when closing incomplete tasks — this convention makes abandoned work queryable (`bd search "Abandoned:"`) so nothing silently disappears.

## Spec lineage tagging

When creating tasks that implement a spec artifact:

```bash
# Create epic with immutable origin ref
bd create "Implement auth" -t epic --external-ref SPEC-003 --json

# Create child tasks with spec label
bd create "Add JWT middleware" -t task \
  --parent <epic-id> --labels spec:SPEC-003 --json

# Add cross-spec impact later
bd update <task-id> --add-label spec:SPEC-007

# Query all work for a spec
bd list -l spec:SPEC-003

# Bidirectional link between tasks in different plans
bd dep relate <task-a> <task-b>
```

## Escalation

When work cannot proceed as designed, use this protocol to abandon tasks and flow control back to swain-design for upstream changes before re-planning.

### Triage table

| Scope | Situation | Action |
|-------|-----------|--------|
| Single task | Alternative approach exists | Abandon task, create replacement under same plan |
| Single task | Spec assumption is wrong | Abandon task, invoke swain-design to update SPEC, create replacement task |
| Multiple tasks | Direction change needed | Abandon affected tasks, create ADR + update SPEC via swain-design, seed new tasks |
| Entire plan | Fundamental rethink required | Abandon all tasks, abandon SPEC (and possibly EPIC) via swain-design, create new SPEC if needed |

### Abandoning tasks

```bash
# Single task
bd close <id> --reason "Abandoned: <why>" --json

# Batch — close all open tasks under an epic
for id in $(bd list --parent <epic-id> --status=open --json | jq -r '.[].id'); do
  bd close "$id" --reason "Abandoned: <why>" --json
done

# Preserve in-progress notes before closing
bd update <id> --append-notes "Abandoning: <context about partial work>"
bd close <id> --reason "Abandoned: <why>" --json
```

### Escalation workflow

1. **Record the blocker.** Append notes to the plan epic explaining why work cannot proceed:
   ```bash
   bd update <epic-id> --append-notes "Blocked: <description of blocker>"
   ```

2. **Invoke swain-design.** Choose the appropriate scope:
   - **Spec tweak** — update the SPEC's assumptions or requirements, then return here.
   - **Design pivot** — create an ADR documenting the decision change, update affected SPECs, then return here.
   - **Full abandon** — transition the SPEC (and possibly EPIC) to Abandoned phase via swain-design.

3. **Seed replacement plan** from the updated spec. Create a new implementation plan linked to the same (or new) SPEC via origin ref:
   ```bash
   bd create "Implement <updated approach>" -t epic --external-ref <SPEC-ID> --json
   ```

4. **Link lineage.** Preserve traceability between abandoned and replacement work:
   - Use the same `spec:<SPEC-ID>` labels on new tasks.
   - Reference abandoned task IDs in the new epic's description or notes:
     ```bash
     bd update <new-epic-id> --append-notes "Replaces abandoned tasks: <old-id-1>, <old-id-2>"
     ```

### Cross-spec escalation

When abandoned tasks carry multiple `spec:` labels, each referenced spec may need upstream changes. Check every spec label on the abandoned tasks and invoke swain-design for each affected spec before re-planning.

```bash
# List spec labels on an abandoned task
bd show <id> --json | jq -r '.labels[]' | grep '^spec:'
```

## "What's next?" flow

When asked what to work on next, show ready work from the execution backend:

```bash
# Check for bd availability and initialization
command -v bd && [ -d .beads ]

# Show unblocked tasks (blocker-aware)
bd ready --json

# If there are in-progress tasks, show those too
bd list --status=in_progress --json
```

If bd is initialized and has tasks, present the results. If bd is not initialized or has no tasks, report that and defer to the swain-design skill's `specgraph.sh next` for artifact-level guidance.

When invoked from the swain-design skill's combined "what's next?" flow, this skill provides the **task layer** — concrete claimable work items — complementing the spec layer's artifact-level readiness view.

## Artifact/bd reconciliation

When specwatch detects mismatches between artifact status and bd item state (via `specwatch.sh bd-sync` or `specwatch.sh scan`), this skill is responsible for cleanup. The specwatch log (`.agents/specwatch.log`) contains `BD_SYNC` and `BD_ORPHAN` entries identifying the mismatches.

### Mismatch types and resolution

| Log entry | Meaning | Resolution |
|-----------|---------|------------|
| `BD_SYNC` artifact Implemented, bd open | Spec is done but tasks linger | Close open bd items: `bd close <id> --reason "Reconciled: artifact already Implemented" --json` |
| `BD_SYNC` artifact Abandoned, bd open | Spec was killed but tasks linger | Abandon open bd items: `bd close <id> --reason "Abandoned: parent artifact Abandoned" --json` |
| `BD_SYNC` all bd closed, artifact active | All work done but spec not transitioned | Invoke swain-design to transition the artifact forward (e.g., Approved → Implemented) |
| `BD_ORPHAN` bd refs non-existent artifact | bd items reference an artifact ID not found in docs/ | Investigate: artifact may have been renamed/deleted. Close or re-tag the bd items |

### Reconciliation workflow

1. **Read the log:** `grep '^BD_SYNC\|^BD_ORPHAN' .agents/specwatch.log`
2. **For each mismatch**, apply the resolution from the table above.
3. **Re-run sync check:** `specwatch.sh bd-sync` to confirm all mismatches resolved.

### Automated invocation

Specwatch runs `bd-sync` as part of `specwatch.sh scan` and during watch-mode event processing (when bd is available). When mismatches are found, the output directs the user to invoke swain-do for reconciliation.

## Observer pattern expectations

1. Maintain compact current-status view: `bd status` and `bd list --pretty`.
2. Ensure blockers are explicit: `bd blocked` shows issues with unsatisfied deps.
3. Use consistent labels so supervisors can filter by stream, owner, or phase.

## Plan ingestion (superpowers integration)

When a superpowers plan file exists (produced by the `writing-plans` skill), use the ingestion script instead of manually decomposing tasks. The script parses the plan's `### Task N:` blocks and registers them in bd with full spec lineage.

**Script location:** `scripts/ingest-plan.py` (relative to this skill)

### When to use

- A superpowers plan file exists at `docs/plans/YYYY-MM-DD-<name>.md`
- The plan follows the `writing-plans` format (header + `### Task N:` blocks)
- You have an origin-ref artifact ID to link the plan to

### Usage

```bash
# Parse and register in bd
python3 scripts/ingest-plan.py <plan-file> <origin-ref>

# Parse only (preview without creating bd tasks)
python3 scripts/ingest-plan.py <plan-file> <origin-ref> --dry-run

# With additional labels
python3 scripts/ingest-plan.py <plan-file> <origin-ref> --labels epic:EPIC-009
```

### What it does

1. Parses the plan header (title, goal, architecture, tech stack)
2. Splits on `### Task N:` boundaries
3. Creates a bd epic with `--external-ref <origin-ref>`
4. Creates child tasks with `--labels spec:<origin-ref>` and full task body as description
5. Wires sequential dependencies (Task N+1 depends on Task N)

### When NOT to use

- The plan file doesn't follow superpowers format — fall back to manual task breakdown
- You need non-sequential dependencies — use the script, then adjust deps manually with `bd dep add`
- The plan is very short (1-2 tasks) — manual creation is faster

## Fallback

If `bd` cannot be installed or is unavailable:

1. Log the failure reason.
2. Fall back to a neutral text task ledger (JSONL or Markdown checklist) in the working directory.
3. Use the same status model (`open`, `in_progress`, `blocked`, `closed`) and keep updates externally visible.

