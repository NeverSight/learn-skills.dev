---
name: project-workspace-cleaner
description: Scan workspace repositories for cleanup opportunities using a read-only hygiene audit. Use when users ask to detect build/cache artifact buildup, stale large transient files, and prioritized cleanup chores by repository and directory.
---

# Project Workspace Cleaner

Run a read-only scan over repositories in a workspace root and rank cleanup chores by severity.

## Inputs

- Optional CLI overrides:
  - `--workspace`
  - `--min-mb`
  - `--stale-days`
  - `--max-findings`
  - `--config`
  - `--json`
- Config precedence:
  1. CLI flags
  2. `config/customization.yaml`
  3. `config/customization.template.yaml`
  4. script defaults

## Workflow

1. Resolve settings using the documented precedence.
2. Run `scripts/scan_workspace_cleanup.py`.
3. Record skipped paths when traversal or stat operations fail, then continue scanning remaining accessible paths.
4. Rank findings by severity, score, size, repo, and directory.
5. Return the ranked findings plus repo-level totals.
6. If there are no findings and no skipped paths, report the user-facing clean result.

## Output Contract

Each finding includes:

- `severity`
- `repo`
- `directory`
- `category`
- `size_human`
- `score`
- `why_flagged`
- `suggested_cleanup`

- Repo summary includes total flagged size and finding counts per severity.
- JSON output includes `partial_results` and `skipped_paths`.
- For user-facing clean runs, output exactly `No findings.`
- If any path is skipped, return a partial-results warning and list skipped paths instead of using the clean-run message.

## Guardrails

- Never run destructive commands.
- Never remove artifacts automatically.
- Never write into scanned repositories.
- Provide recommendations only.

## References

- `references/config-schema.md`
- `references/customization.md`
- `references/automation-prompts.md`
- `references/patterns.md`
