---
name: mcp-cli
description: Use MCP servers on-demand via the mcp CLI tool - discover tools, resources, and prompts without polluting context with pre-loaded MCP integrations
---

# MCP CLI: On-Demand MCP Server Usage

Use the `mcp` CLI tool to dynamically discover and invoke MCP server capabilities without pre-configuring them as permanent integrations.

## When to Use This Skill

Use this skill when you need to:
- Explore an MCP server's capabilities before deciding to use it
- Make one-off calls to an MCP server without permanent integration
- Access MCP functionality without polluting the context window
- Test or debug MCP servers
- Use MCP servers that aren't pre-configured

## Prerequisites

The `mcp` CLI must be installed at `~/.local/bin/mcp`. If not present:

```bash
# Clone and build
cd /tmp && git clone --depth 1 https://github.com/f/mcptools.git
cd mcptools && CGO_ENABLED=0 go build -o ~/.local/bin/mcp ./cmd/mcptools
```

Always ensure PATH includes the binary:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Discovery Workflow

### Step 1: Discover Available Tools

```bash
mcp tools <server-command>
```

**Examples:**
```bash
# Filesystem server
mcp tools npx -y @modelcontextprotocol/server-filesystem /path/to/allow

# Memory/knowledge graph server
mcp tools npx -y @modelcontextprotocol/server-memory

# GitHub server (requires token)
mcp tools docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server

# HTTP-based server
mcp tools https://example.com/mcp
```

### Step 2: Discover Resources (if supported)

```bash
mcp resources <server-command>
```

Resources are data sources the server exposes (files, database entries, etc.).

### Step 3: Discover Prompts (if supported)

```bash
mcp prompts <server-command>
```

Prompts are pre-defined prompt templates the server provides.

### Step 4: Get Detailed Info (JSON format)

```bash
# For full schema details including parameter types
mcp tools --format json <server-command>
mcp tools --format pretty <server-command>
```

## Making Tool Calls

### Basic Syntax

```bash
mcp call <tool_name> --params '<json>' <server-command>
```

### Examples

**Read a file:**
```bash
mcp call read_file --params '{"path": "/tmp/example.txt"}' \
  npx -y @modelcontextprotocol/server-filesystem /tmp
```

**Write a file:**
```bash
mcp call write_file --params '{"path": "/tmp/test.txt", "content": "Hello world"}' \
  npx -y @modelcontextprotocol/server-filesystem /tmp
```

**List directory:**
```bash
mcp call list_directory --params '{"path": "/tmp"}' \
  npx -y @modelcontextprotocol/server-filesystem /tmp
```

**Create entities (memory server):**
```bash
mcp call create_entities --params '{"entities": [{"name": "Project", "entityType": "Software", "observations": ["Uses TypeScript"]}]}' \
  npx -y @modelcontextprotocol/server-memory
```

**Search (memory server):**
```bash
mcp call search_nodes --params '{"query": "TypeScript"}' \
  npx -y @modelcontextprotocol/server-memory
```

### Complex Parameters

For nested objects and arrays, ensure valid JSON:

```bash
mcp call edit_file --params '{
  "path": "/tmp/file.txt",
  "edits": [
    {"oldText": "foo", "newText": "bar"},
    {"oldText": "baz", "newText": "qux"}
  ]
}' npx -y @modelcontextprotocol/server-filesystem /tmp
```

### Output Formats

```bash
# Table (default, human-readable)
mcp call <tool> --params '{}' <server>

# JSON (for parsing)
mcp call <tool> --params '{}' -f json <server>

# Pretty JSON (readable JSON)
mcp call <tool> --params '{}' -f pretty <server>
```

## Reading Resources

```bash
# List available resources
mcp resources <server-command>

# Read a specific resource
mcp read-resource <resource-uri> <server-command>

# Alternative syntax
mcp call resource:<resource-uri> <server-command>
```

## Using Prompts

```bash
# List available prompts
mcp prompts <server-command>

# Get a prompt (may require arguments)
mcp get-prompt <prompt-name> <server-command>

# With parameters
mcp get-prompt <prompt-name> --params '{"arg": "value"}' <server-command>
```

## Server Aliases (for repeated use)

If using a server frequently during a session:

```bash
# Create alias
mcp alias add fs npx -y @modelcontextprotocol/server-filesystem /home/user

# Use alias
mcp tools fs
mcp call read_file --params '{"path": "README.md"}' fs

# List aliases
mcp alias list

# Remove when done
mcp alias remove fs
```

Aliases are stored in `~/.mcpt/aliases.json`.

## Authentication

### HTTP Basic Auth
```bash
mcp tools --auth-user "username:password" https://api.example.com/mcp
```

### Bearer Token
```bash
mcp tools --auth-header "Bearer your-token-here" https://api.example.com/mcp
```

### Environment Variables (for Docker-based servers)
```bash
mcp tools docker run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN="$GITHUB_TOKEN" \
  ghcr.io/github/github-mcp-server
```

## Transport Types

### Stdio (default for npx/node commands)
```bash
mcp tools npx -y @modelcontextprotocol/server-filesystem /tmp
```

### HTTP (auto-detected for http/https URLs)
```bash
mcp tools https://example.com/mcp
```

### SSE (Server-Sent Events)
```bash
mcp tools http://localhost:3001/sse
# Or explicitly:
mcp tools --transport sse http://localhost:3001
```

## Common MCP Servers

### Filesystem
```bash
# Allow access to specific directory
mcp tools npx -y @modelcontextprotocol/server-filesystem /path/to/allow
```

### Memory (Knowledge Graph)
```bash
mcp tools npx -y @modelcontextprotocol/server-memory
```

### GitHub
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="your-token"
mcp tools docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server
```

### Brave Search
```bash
export BRAVE_API_KEY="your-key"
mcp tools npx -y @anthropic/mcp-server-brave-search
```

### Puppeteer (Browser Automation)
```bash
mcp tools npx -y @anthropic/mcp-server-puppeteer
```

## Best Practices

### 1. Always Discover First
Before calling tools, run `mcp tools` to understand what's available and the exact parameter schema.

### 2. Use JSON Format for Parsing
When you need to process results programmatically:
```bash
mcp call <tool> --params '{}' -f json <server> | jq '.field'
```

### 3. Validate Parameters
The table output shows parameter signatures. Match them exactly:
- `param:str` = string
- `param:num` = number
- `param:bool` = boolean
- `param:str[]` = array of strings
- `[param:str]` = optional parameter

### 4. Handle Errors Gracefully
Tool calls may fail. Check exit codes and stderr:
```bash
if ! result=$(mcp call tool --params '{}' server 2>&1); then
  echo "Error: $result"
fi
```

### 5. Use Aliases for Multi-Step Operations
If making several calls to the same server:
```bash
mcp alias add tmp-server npx -y @modelcontextprotocol/server-filesystem /tmp
mcp call list_directory --params '{"path": "/tmp"}' tmp-server
mcp call read_file --params '{"path": "/tmp/file.txt"}' tmp-server
mcp alias remove tmp-server
```

### 6. Restrict Capabilities with Guard
For safety, limit what tools are accessible:
```bash
# Only allow read operations
mcp guard --allow 'tools:read_*,list_*' --deny 'tools:write_*,delete_*' \
  npx -y @modelcontextprotocol/server-filesystem /home
```

## Debugging

### View Server Logs
```bash
mcp tools --server-logs <server-command>
```

### Check Alias Configuration
```bash
cat ~/.mcpt/aliases.json
```

### Verbose Output
Use `--format pretty` for detailed JSON output to debug parameter issues.

## Quick Reference

| Action | Command |
|--------|---------|
| List tools | `mcp tools <server>` |
| List resources | `mcp resources <server>` |
| List prompts | `mcp prompts <server>` |
| Call tool | `mcp call <tool> --params '<json>' <server>` |
| Read resource | `mcp read-resource <uri> <server>` |
| Get prompt | `mcp get-prompt <name> <server>` |
| Add alias | `mcp alias add <name> <server-command>` |
| Remove alias | `mcp alias remove <name>` |
| JSON output | Add `-f json` or `-f pretty` |

## Example: Complete Workflow

```bash
# 1. Discover what's available
mcp tools npx -y @modelcontextprotocol/server-filesystem /home/user/project

# 2. Check for resources
mcp resources npx -y @modelcontextprotocol/server-filesystem /home/user/project

# 3. Create alias for convenience
mcp alias add proj npx -y @modelcontextprotocol/server-filesystem /home/user/project

# 4. Explore directory structure
mcp call directory_tree --params '{"path": "/home/user/project"}' proj

# 5. Read specific files
mcp call read_file --params '{"path": "/home/user/project/README.md"}' proj

# 6. Search for patterns
mcp call search_files --params '{"path": "/home/user/project", "pattern": "**/*.ts"}' proj

# 7. Clean up alias
mcp alias remove proj
```

## Troubleshooting

### "command not found: mcp"
Ensure PATH is set: `export PATH="$HOME/.local/bin:$PATH"`

### JSON parse errors
- Escape special characters properly
- Avoid shell expansion issues by using single quotes around JSON
- For complex JSON, write to a temp file and use `--params "$(cat params.json)"`

### Server timeout
Some servers take time to start. The mcp CLI waits for initialization automatically.

### Permission denied
For filesystem server, ensure the allowed directory path is correct and accessible.
