---
name: roamresearch
description: Roam Research operations via roam-cli. Use this skill for page/block retrieval, search, datalog queries, markdown save, journaling lookup, and low-level block or batch writes with environment-injected credentials.
compatibility: Requires roam-cli in PATH and ROAM_API_TOKEN/ROAM_API_GRAPH environment variables.
---

# RoamResearch Skill

Use this skill to perform Roam Research read/write/query workflows through `roam-cli`.

## Prerequisites

- `roam-cli` binary in PATH
- Environment variables: `ROAM_API_TOKEN`, `ROAM_API_GRAPH`
- Run `roam-cli status` to verify before any operations

If not set up, see `references/installation.md`.

## Command Mapping

| Command | Purpose |
|---|---|
| `get` | Read page by title or block by UID |
| `search` | Search blocks by terms |
| `q` | Run raw datalog query |
| `save` | Save GFM markdown as a page (`--title`) or under a parent block (`--parent`) |
| `journal` | Read daily journaling blocks |
| `block find` | Find block UID by text on a page/daily note |
| `block create-tree` | Create nested block tree from JSON |
| `block create/update/delete/move/get` | Low-level block operations |
| `batch run` | Batch actions (native + `create-with-children` DSL) |

## `block create-tree` Input Contract

- Requires `--parent <block-uid>`.
- JSON supports either a single object or an array of objects.
- Node shape is:
  - `text` (required): block text
  - `children` (optional): nested nodes
- CLI accepts both `text` and `string` in input JSON (`text` takes precedence when both are provided).

Example:

```json
{
  "text": "Current State - 2026-02-24",
  "children": [
    {"text": "Project A", "children": [{"text": "Task 1"}]}
  ]
}
```

## Recommended Workflow

1. Run `roam-cli status` first.
2. Prefer read commands first: `get`, `search`, `q`.
3. Prefer high-level writes: `save`, `journal`.
4. Use low-level APIs for deterministic control: `block`, `batch`.

## Save Markdown (GFM format)

`save` accepts **GFM (GitHub Flavored Markdown)** and auto-converts to Roam blocks. Key rules:

- Do NOT include `#` h1 — page title comes from `--title`
- Headings `##`–`###` become headed blocks (levels 4–6 capped to 3)
- Lists (`-`/`*`/`+`) become nested child blocks; ordered lists preserve the `1.` marker
- Tables MUST use standard GFM pipe+separator format (header row, `---` row, data rows)
- Code blocks, blockquotes passed through; horizontal rules discarded

Full conversion rules: see `references/gfm-format.md`

## Error Handling Rules

- Missing credentials: explicitly report missing `ROAM_API_TOKEN` / `ROAM_API_GRAPH`.
- API failures: include HTTP status code and response body.
- Not found: clearly include the identifier/uid that was requested.

## Output Rules

- Preserve JSON output when `--json` is requested.
- Keep default output concise and readable.
- Never invent Roam data; only report real command results.

## Detailed Examples

See `references/usage-examples.md` for full command examples.
