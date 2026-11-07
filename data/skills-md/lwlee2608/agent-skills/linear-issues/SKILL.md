---
name: linear-issues
description: Use when reading, searching, creating, updating, or commenting on Linear issues. Routes every Linear operation through the installed Linear MCP server and keeps ticket comments to a few sentences.
user-invocable: true
argument-hint: "[<issue ID or request>]"
---

# Work with Linear

Do all Linear work through the installed Linear MCP server.

## Rules

1. **Use the Linear MCP tools** (`mcp__linear__*`: `list_issues`, `get_issue`, `create_issue`, `update_issue`, `list_comments`, `create_comment`, …). Read the actual schemas before calling — Linear renames tools without notice.

2. **Never fall back to the GraphQL API or web UI.** If no Linear MCP server is connected, stop and tell the user to add `https://mcp.linear.app/mcp` (HTTP transport) to their agent. In Claude Code:
   ```bash
   claude mcp add --transport http linear https://mcp.linear.app/mcp
   ```

3. **Resolve names to IDs before writing.** Team, state, label, and assignee fields take UUIDs; a display name fails or silently no-ops. Call the matching `list_*` tool first.

4. **Keep comments short.** 1–3 sentences. Outcome first, link the PR instead of pasting the diff, no preamble, no recap of the ticket, no sign-off, no emoji.
   ```
   Root cause: config loader reads `retry_count` but the YAML key is `retryCount`, so it binds 0. Fixed in #482.
   ```

5. **Don't hand-move a PR-linked issue to Done.** A linked PR (branch name, or `Fixes ENG-482` in the title/body) moves the issue to Done on merge. Set it by hand only when no PR is linked, or the user asks.

6. **Confirm before writes the user did not ask for.** Issues, status changes, and comments are visible to the whole team. If they asked for the write, just do it.

## Verification

1. Re-read the object after a write; report the identifier and URL (`ENG-482 — https://linear.app/…`).
2. If a comment runs past ~3 sentences, cut it.
