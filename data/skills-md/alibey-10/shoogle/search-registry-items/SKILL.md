---
name: search-registry-items
description: >
  Find shadcn registry items by keyword to install, compare registries, or verify before add.
  Use when the user wants a component but didn't give @registry/name or asks which registry has
  X — even without mentioning MCP. Keyword on names/descriptions only; not layouts, blocks, or
  semantic search (shoogle.dev/search). Skip known add targets.
compatibility: Requires the Shoogle MCP server (`user-shoogle`) with network access. Setup guide at https://shoogle.dev/mcp-install
allowed-tools: CallMcpTool
metadata:
  user-invocable: "false"
---

# Search Registry Items

Look up indexed shadcn registry catalog entries via **full-text search** on item `name` and `description`. Returns the registry namespace and `addCommandArgument` for `npx shadcn@latest add`.

Default tool call:

```json
CallMcpTool({ "server": "user-shoogle", "toolName": "search_registry_items", "arguments": { "query": "button" } })
```

## Workflow

Progress:

- [ ] Call `search_registry_items` on `user-shoogle` with a short keyword or name fragment (not a full sentence)
- [ ] Present matches as the output table below — never dump raw JSON
- [ ] If multiple registries share the same name, ask which registry to use
- [ ] Install with `npx shadcn@latest add {addCommandArgument}` (or the project's package runner)
- [ ] Paginate only when needed (`offset` += `limit` while `pagination.hasMore`)

Skip search when the user already gave the exact add target (e.g. `@cult-ui/gradient-button`) — go straight to `view` / `add`.

For install and composition rules after search, use the [shadcn skill](https://github.com/shadcn-ui/ui/blob/main/skills/shadcn/SKILL.md).

## Gotchas

- **One MCP tool only.** `user-shoogle` exposes `search_registry_items`. Block and semantic MCP tools (`search`, `search_vectors`) are not available — use [shoogle.dev/search](https://shoogle.dev/search) instead. Do not use `npx shadcn@latest search` for this workflow.
- **Full-text on `name` and `description`.** Matching uses full-text search across both fields — not item titles, and not semantic/vector search. A query like `carousel` can match items named `carousel` or whose description mentions carousels.
- **Keywords, not intent.** Multi-concept natural-language queries like "login page with dark mode" won't work well. For semantic block discovery, send the user to [shoogle.dev/search](https://shoogle.dev/search).
- **Query the item name, not the registry prefix.** Use `button`, not `@acme/button`. Filter by `registry` in results.
- **Short fragments beat sentences.** Prefer `button`, `hero`, `data-table`. Empty or whitespace queries return nothing.
- **No results?** Try shorter fragments or synonyms (`dialog` vs `modal`).
- **`addCommandArgument` is the install target.** Use it verbatim: `npx shadcn@latest add cult-ui/gradient-button`. Do not reconstruct from `@registry/name`.
- **Pagination cap is 100.** Default page size is 100; mention `pagination.total` when results span pages.

If MCP is unavailable, point to [shoogle.dev/mcp-install](https://shoogle.dev/mcp-install). For parameter or response details, read [references/TOOL-REFERENCE.md](references/TOOL-REFERENCE.md).

## Output format

Always respond with a markdown table:

| name | registry | add command | type | description |
| ---- | -------- | ----------- | ---- | ----------- |

- **add command**: `npx shadcn@latest add {addCommandArgument}` when present
- Use `—` for empty descriptions
- End with match count and page info when relevant

**Example** — user asks for button components across registries:

| name | registry | add command | type | description |
| ---- | -------- | ----------- | ---- | ----------- |
| button | shadcn | `npx shadcn@latest add shadcn/button` | registry:ui | A clickable button component |
| button | cult-ui | `npx shadcn@latest add cult-ui/button` | registry:ui | Animated button variants |

Found 2 matches (showing 1–2 of 2). Which registry should I add from?

## Out of scope

| Need | Use instead |
| ---- | ----------- |
| Registry item by name or description | `search_registry_items` (this skill) |
| Block keyword search | [shoogle.dev/search](https://shoogle.dev/search) |
| Semantic / layout discovery | [shoogle.dev/search](https://shoogle.dev/search) |
| Install a known item | shadcn CLI `add` / `view` |
| Browse one registry | `npx shadcn@latest search @registry -q "…"` |
