---
name: mcp-cli
description: Call any MCP server tool as a CLI command with shell composition. Use when tool args come from files, pipes, or shell commands. Trigger on "mcp-call", "call mcp from cli", or when MCP tool content is in a file.
---

# MCP CLI

Call any configured MCP server tool from the command line with `--flag=value` style args and full shell composition support.

If `mcp-call` is not found, install it: `pipx install mcp-cli-skill` or `uvx mcp-cli-skill`

## Commands

```bash
mcp-call --servers                                    # list configured servers
mcp-call <server> --tools                             # list tools (human-readable)
mcp-call <server> --discover                          # list tools as JSON with schemas
mcp-call <server> <tool> --schema                     # show tool's input schema as JSON
mcp-call <server> <tool> --key=value ...              # call a tool
mcp-call <server> <tool> --json '{"key":"val"}'       # call with JSON args
echo '{}' | mcp-call <server> <tool>                  # call with stdin JSON
mcp-call --add <name> <cmd> [args] [--env K=V ...]    # add stdio server
mcp-call --add-http <name> <url>                      # add HTTP server
mcp-call --remove <name>                              # remove server
mcp-call --sync                                       # re-sync from Claude configs
```

## Server Management

Config stored at `~/.mcp-cli/servers.json`. On first run, seeds from `~/.claude/settings.json` and `~/.claude.json`. Supports both stdio and HTTP MCP servers.

```bash
mcp-call --add myredash uvx redash-mcp --env REDASH_URL=http://localhost --env REDASH_API_KEY=abc123
mcp-call --add github npx @modelcontextprotocol/server-github --env GITHUB_TOKEN=ghp_xxx
mcp-call --remove myredash
mcp-call --sync
```

## Examples

```bash
mcp-call redash redash_query --action=adhoc --query="$(cat /tmp/query.sql)" --data_source_id=1
mcp-call redash redash_query --action=list --page_size=5 | jq '.results[].name'
mcp-call slack slack_chat --action=post --channel=C123 --text="$(cat /tmp/msg.txt)"
mcp-call redash redash_query --action=run --id=42 | jq '.query_result.data.rows' > /tmp/result.json
```

## Multi-tool Workflow

When you need to chain multiple MCP tools together, generate a bash script and run it:

```bash
#!/bin/bash
# Fetch github issues, search code, post to slack

# 1. Fetch open bugs
mcp-call github list_issues \
  --owner=acme --repo=backend --state=open --labels=bug \
  | jq '.[] | {number, title}' > /tmp/bugs.json

# 2. Search for related code
for title in $(jq -r '.[].title' /tmp/bugs.json | head -5); do
  mcp-call github search_code --query="$title repo:acme/backend" | jq '.items[:2]'
done > /tmp/code_matches.txt

# 3. Post summary to slack
mcp-call slack send_message \
  --channel="#engineering" \
  --text="$(jq -r '.[] | "• #\(.number): \(.title)"' /tmp/bugs.json)"
```

This is better than making separate MCP tool calls because you get file I/O, pipes, loops, and variable expansion for free.

## When to Use

Prefer this over MCP tool calls when:
- Content comes from a file: `--arg="$(cat file)"`
- Output needs piping: `| jq`, `> file`, `| grep`
- Shell variable expansion needed: `--arg="$VAR"`
- Chaining multiple calls in one command

## Arg Types

Values auto-parse: `--id=42` → int, `--flag=true` → bool, `--name=hello` → string.
