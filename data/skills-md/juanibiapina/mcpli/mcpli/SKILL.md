---
name: mcpli
description: CLI tool for interacting with MCP (Model Context Protocol) servers. Use when invoking MCP tools, managing MCP servers, or working with MCP-based APIs. Triggers on "MCP server", "mcpli", "invoke MCP tool", or any MCP server interaction.
---

# mcpli

CLI that turns MCP servers into native commands with tab completion.

## Core Commands

### Add a server

```bash
mcpli add <name> <url> [--header "key: value"]...
```

Headers support environment variable expansion with `${VAR_NAME}`:

```bash
mcpli add myserver https://example.com/mcp/ \
  --header 'Authorization: Bearer ${API_TOKEN}'
```

### List servers and tools

```bash
mcpli list              # List all configured servers
mcpli list <server>     # List tools for a server
```

### Discover tools

```bash
mcpli <server> --help           # See all tools on a server
mcpli <server> <tool> --help    # See tool description and usage
```

### Invoke a tool

```bash
mcpli <server> <tool> [json-arguments]
```

Examples:

```bash
mcpli myserver get_status                           # No arguments
mcpli myserver search '{"query": "hello"}'          # With JSON arguments
mcpli myserver create_item '{"name": "test", "count": 5}'
```

### Manage servers

```bash
mcpli update <server>   # Refresh cached tool definitions
mcpli remove <server>   # Remove a configured server
```

## Workflow

1. Add server with `mcpli add` (fetches and caches tools)
2. Discover tools with `mcpli <server> --help`
3. Check tool parameters with `mcpli <server> <tool> --help`
4. Invoke tools with `mcpli <server> <tool> '{...}'`

## Notes

- Tool definitions are cached locally after `add`; use `update` to refresh
- Config stored at `~/.config/mcpli/config.json`
- Arguments must be valid JSON (use single quotes around JSON to avoid shell escaping issues)
