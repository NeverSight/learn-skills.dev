---
name: gps-mcp
description: >-
  Configure and use gps-mcp (Model Context Protocol) for Google Play Publisher
  operations. Use when wiring Cursor/Claude MCP, listing gps_ tools, or choosing
  read-only agent mode.
---

# `gps-mcp`

## Client config

```json
{
  "mcpServers": {
    "google-play-store": {
      "command": "gps-mcp",
      "args": ["--credentials", "/path/to/sa.json"]
    }
  }
}
```

Inspect-only:

```json
{
  "mcpServers": {
    "google-play-store": {
      "command": "gps-mcp",
      "args": ["--read-only", "--credentials", "/path/to/sa.json"]
    }
  }
}
```

Same credential env vars as CLI (`GOOGLE_APPLICATION_CREDENTIALS`, …).

## Tool surface

- Tools are named `gps_*` and match `gps call` / `gps ops`
- Discovery: `gps_search_capabilities`, `gps_list_capabilities`
- Always pass `packageName` unless the tool is meta (`gps_whoami`)

## Agent rules

1. Call `gps_whoami` first if auth is unclear.
2. Prefer read tools before writes.
3. For writes, confirm intent with the user when the action is destructive (refund, halt, delete listing, revoke).
4. Empty `gps_list_reviews` usually means no API-eligible reviews in the recent window — not an auth failure if other tools succeed.
5. Track/listing reads use ephemeral edits; they work under `--read-only`.
