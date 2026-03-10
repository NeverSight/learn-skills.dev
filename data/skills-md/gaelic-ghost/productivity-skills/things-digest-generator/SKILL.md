---
name: things-digest-generator
description: Generate a week-ahead Things planning digest with recent activity, upcoming deadlines, and concrete next actions. Use when users request Things check-ins, weekly planning summaries, or prioritized planning recommendations.
---

# Things Digest Generator

Build a repeatable Things planning digest from Things MCP data or equivalent JSON exports.

## Inputs

- Preferred data source: Things MCP reads
  - `things_read_areas`
  - `things_read_projects` with `status="open"`
  - `things_read_todos` with `status="open"`
  - `things_read_todos` with `status="completed"` and `completed_after=<today-7d>`
  - Optional `things_read_todo` for checklist or note signals
- JSON fallback for deterministic script usage:
  - `--areas`
  - `--projects`
  - `--open-todos`
  - optional `--recent-done`
  - optional `--detailed-todos`
- Optional overrides:
  - `--days-ahead`
  - `--due-soon-days`
  - `--top-projects`
  - `--top-areas`
  - `--max-suggestions`
  - `--open-count-cap`
  - `--output-style`
  - `--config`
  - `--today`

## Workflow

1. Resolve settings from CLI overrides, `config/customization.yaml`, `config/customization.template.yaml`, then script defaults.
2. Prefer live Things MCP reads; fall back to JSON inputs when MCP is unavailable or when deterministic script execution is required.
3. Build urgency buckets and activity scores from open and recently completed todos.
4. Rank top projects and areas, then generate bounded suggestions.
5. If there are no open todos and no recent completed todos, output exactly `No findings.`
6. Otherwise render the digest using the canonical section order in `references/output-format.md`.

## Output Contract

- Return markdown that begins at `# Things Planning Digest - YYYY-MM-DD`.
- Return these sections in order after the title:
  - `Executive Summary` only when `outputStyle=executive`
  - `Snapshot`
  - `Recently Active`
  - `Week/Weekend Ahead`
  - `Suggestions`
- Use exact task, project, and area names where available.
- If there are no open todos and no recent completed todos in scope, output exactly `No findings.`

## Guardrails

- Never modify Things data unless explicitly requested.
- If MCP is unavailable, report the missing permission and use JSON fallback when provided.
- If neither MCP nor JSON inputs are available, stop and report one deterministic `Input error:` message that names the missing file, unreadable path, invalid JSON, or unsupported JSON shape.

## References

- `references/output-format.md`
- `references/customization.md`
- `references/config-schema.md`
- `references/suggestion-rules.md`
- `references/automation-prompts.md`
