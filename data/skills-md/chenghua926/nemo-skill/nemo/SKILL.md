---
name: nemo
description: Search engine for MCP tools and agent skills. Search 790+ MCP server tools and 760+ agent skills in one place, call remote MCP tools, and get full skill instructions via simple HTTP API.
---

# Nemo

Nemo indexes MCP tools and agent skills into a single searchable catalog. Use it to discover tools on demand via HTTP.

**Base URL:** `https://nemo.25chenghua.workers.dev`

## Search

Find MCP tools and agent skills by keyword.

```bash
curl "https://nemo.25chenghua.workers.dev/api/search?q=QUERY"
```

| Param | Default | Description |
|-------|---------|-------------|
| `q` | required | Search query |
| `limit` | 5 | Max results (1-20) |
| `detail` | compact | `compact` or `full` (includes descriptions, schemas) |
| `source` | all | `all`, `mcp`, or `skills` |

Each result has a `type` field: `"mcp_tool"` or `"skill"`.

## Get Skill Instructions

Load full SKILL.md content for a skill found via search.

```bash
curl "https://nemo.25chenghua.workers.dev/api/skill/SKILL_NAME"
```

Add `?repo=owner/repo` if multiple skills share the same name.

Returns the complete instructions, install command, and metadata.

## Call a Remote MCP Tool

Proxy a tool call to any indexed MCP server.

```bash
curl -X POST "https://nemo.25chenghua.workers.dev/api/call" \
  -H "Content-Type: application/json" \
  -d '{"endpoint": "SERVER_URL", "tool": "TOOL_NAME", "args": {}}'
```

Use the `serverEndpoint` and `toolName` from search results.

## Workflow

1. Search: `curl ".../api/search?q=file+conversion"`
2. If result is `type: "skill"` → get instructions: `curl ".../api/skill/SKILL_NAME"` → follow them
3. If result is `type: "mcp_tool"` → call it: `POST .../api/call` with `endpoint`, `tool`, `args`
