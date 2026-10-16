---
name: project-mgr
description: Manage project status with the local-first project-mgr CLI. Use when an AI agent needs to add an append-only project update, set project descriptions/notes, list or fuzzy-search projects, start the local Web Dashboard, import status records, query current or historical project state, or export a status ledger.
---

# project-mgr

## CLI selection

Prefer an installed `pmgr`: locate it with `command -v pmgr` and check the installed package metadata/documentation for the required version and capabilities. This source revision supports `-h` / `--help`, `help [command]`, and `-v` / `-V` / `--version` / `version` without opening the database. Older installed releases may not support these flags; inspect their package metadata instead. In a source checkout, use `pnpm pmgr` only when the local dependencies are already installed and the package manager is available without downloading it.

Do not automatically install or upgrade dependencies, or fall back to `npx` / `npm exec`. If no usable CLI is available, report the missing executable, dependency, or capability and the setup needed. Perform installation or upgrades only when the user authorizes that setup.

Completion links and version-2 exports require project-mgr 0.3.0 or later. This skill is updated through Git and has no independent release version.

## Database safety

- Read `PMGR_DB_PATH` before operating. If unset, the CLI uses `~/.local/share/project-mgr/project-mgr.sqlite`.
- For exploratory or test work, set `PMGR_DB_PATH` to a dedicated absolute SQLite path for every command. Do not use `:memory:` when more than one CLI invocation must share data.
- The database file and its parent directory must be accessible with the permissions SQLite needs for journal files and writes. Even query commands open the ledger and may initialize or migrate it; do not assume they are filesystem-read-only.
- On a permission or read-only database error, report the command, resolved database path, and error without exposing credentials. Use the environment's approved permission mechanism when available; otherwise report the blocked operation. Do not reinstall the CLI, change permissions, or silently switch to another database to work around the error. Change the ledger location only when the user requests it.
- Query before writing. `add` appends a snapshot; it does not edit the previous one. Read back the affected state after writing and report success only when verified. If a write's outcome is uncertain, query before retrying to avoid duplicates.
- Set `--source agent` for agent-authored updates. Use `--external-ref` only when a stable idempotency key is available.
- Explicitly pass `--status` on every `add`, and include `status` in every agent-authored import entry. The CLI defaults to `completed`; do not rely on that default. Choose the status from the evidence and inspect the current snapshot when unclear. Completing one activity does not necessarily complete the project; use `active` when project work continues. If the status remains uncertain, clarify before writing.
- If the project is not yet in the ledger database, initialize its metadata with `set-project`. Backfill only milestones supported by verifiable Git commits, dated documents, or historical records, and include the evidence reference in `--progress`. Use historical `--at` timestamps only when supported by that evidence; a commit timestamp proves a commit, not a deployment. There is no required number of entries. Never invent milestones or dates; when evidence is unavailable, skip backfill and append only the current known status.

## Metadata vs. status entries

- **Project notes (`--notes`)**: Reserved for persistent, medium-to-long-term project context (e.g., architectural constraints, permanent tech stack choices, long-term goals, or critical environment caveats).
  - Manage notes via `set-project --project <name> --notes "..."`.
  - **Do NOT** put transient progress, session logs, or one-off status messages into `--notes`.
  - Avoid passing `--notes` during routine `add` commands to prevent accidentally overwriting long-term project notes.
- **Project description (`--description`)**: A high-level, stable summary of the project's purpose.
- **Status snapshots (`add`)**: Use `--summary` (concise milestone headline), `--progress` (detailed work accomplished), `--next` (immediate next steps), `--blocker` (current obstacles), and `--decision` for transactional, append-only updates.

## Operations

Prefer `--json` for data that must be interpreted or reported programmatically.

```bash
# Set, update, or clear project metadata (description, notes, display name).
pmgr set-project --project my-project --description "Project summary" --notes "Internal notes" --json
pmgr set-project --project my-project --clear-description --clear-notes --json

# List all projects or fuzzy search across project names, descriptions, notes, status summaries, and tags.
pmgr projects --json
pmgr list --query "keyword" --json

# Start the local Web Dashboard & REST API server.
pmgr serve --port 3000 --no-open --json

# Record a completed milestone while the project remains active.
pmgr add --project my-project --status active --summary "Implemented the CLI" \
  --progress "Tests pass" --next "Publish the package" --source agent --json

# Query current state, history, or state at a time.
pmgr current --project my-project --json
pmgr history --project my-project --limit 20 --json
pmgr history --limit 20 --json
pmgr at --project my-project --at 2026-08-03T12:00:00+08:00 --json

# Import validated JSON/JSONL, or export portable records.
pmgr import statuses.jsonl --json
pmgr export --project my-project --format jsonl > statuses.jsonl
```

Use `PMGR_DB_PATH=/absolute/path/test.sqlite pmgr ...` to isolate a manual test database. Import validates and writes the entire batch within one transaction; export output can be imported directly.

## Complete predecessor activities

Before recording follow-up work, inspect `history --project <name> --json`, including the original `status`, `effectiveStatus`, and `completedBy` evidence. Do not interpret a missing completion link as unfinished work. Inspect older pages with `--offset` when needed.

When this update resolves all commitments of earlier entries (including blockers and next steps), pass repeatable `--completes <id-or-uid>` to `add`. One follow-up may complete several entries. For partial progress, describe the remaining work and do not link. A commit/deployment is sufficient only when it resolves all the targeted entry's commitments.

Use `complete --entry <id-or-uid> --by <id-or-uid> --source agent` for an existing follow-up. Use `revoke-completion --entry <id-or-uid> --by <id-or-uid> --reason "..." --source agent` to correct a mistaken link. Links require the same project and strictly increasing occurrence times. Query the affected history afterward to verify effective completion. Do not bulk-close old entries without evidence.

Export produces version-2 bundles (one bundle per line for JSONL), preserving entry/event identities and audit history; legacy imports remain supported. `at` has no completion annotations. Project current state still comes from the latest snapshot.
