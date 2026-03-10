---
name: troubleshoot-mcp-connection
description: >
  Diagnose and fix MCP server connection issues between Claude Code,
  Claude Desktop, and MCP servers. Covers Windows argument parsing,
  authentication failures, transport issues, and platform-specific
  debugging. Use when Claude Code or Claude Desktop fails to connect to
  an MCP server, when MCP tools don't appear in sessions, on "cannot
  attach the server" errors, when a working connection has stopped, or
  when setting up MCP on a new machine.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: mcp-integration
  complexity: intermediate
  language: multi
  tags: mcp, troubleshooting, debugging, connection, windows
---

# Troubleshoot MCP Connection

Diagnose and resolve MCP server connection failures.

## When to Use

- Claude Code or Claude Desktop fails to connect to an MCP server
- MCP tools don't appear in sessions
- "Cannot attach the server" errors
- Connection was working but stopped
- Setting up MCP on a new machine

## Inputs

- **Required**: Error message or symptom description
- **Required**: Which client (Claude Code, Claude Desktop, or both)
- **Required**: Which MCP server (mcptools, Hugging Face, custom)
- **Optional**: Recent changes to configuration or environment

## Procedure

### Step 1: Identify the Client and Configuration

**Claude Code** (WSL):

```bash
# View MCP configuration
claude mcp list
claude mcp get server-name

# Configuration stored in
cat ~/.claude.json | python3 -m json.tool
```

**Claude Desktop** (Windows):

```bash
# Configuration file location
cat "/mnt/c/Users/$USER/AppData/Roaming/Claude/claude_desktop_config.json"
```

**Expected:** Configuration file is located and readable, showing the MCP server entries with command, args, and env fields.

**On failure:** If the config file does not exist or is empty, the server was never configured. Follow the `configure-mcp-server` skill to set it up from scratch.

### Step 2: Test Server Independently

**R mcptools**:

```bash
# Test if R can start the server
"/mnt/c/Program Files/R/R-4.5.0/bin/Rscript.exe" -e "mcptools::mcp_server()"
```

If this fails:
- Check R path exists: `ls "/mnt/c/Program Files/R/"`
- Check mcptools is installed: `Rscript -e "library(mcptools)"`
- Check ellmer dependency: `Rscript -e "library(ellmer)"`

**Hugging Face MCP**:

```bash
# Test mcp-remote directly
mcp-remote https://huggingface.co/mcp

# Check if mcp-remote is installed
which mcp-remote
npm list -g mcp-remote
```

**Expected:** The server process starts and produces initialization output (JSON-RPC handshake or "listening" message) without errors.

**On failure:** If R mcptools fails, check that the R version path is correct and that mcptools is installed in the R library. If mcp-remote fails, reinstall globally with `npm install -g mcp-remote` and verify it is on the PATH.

### Step 3: Diagnose Common Error Patterns

**"Cannot attach the server" (Claude Desktop)**

Root cause: Windows command argument parsing.

Fix: Use environment variables instead of `--header` arguments:

```json
{
  "hf-mcp-server": {
    "command": "mcp-remote",
    "args": ["https://huggingface.co/mcp"],
    "env": { "HF_TOKEN": "your_token" }
  }
}
```

Also ensure `mcp-remote` is globally installed (`npm install -g mcp-remote`), not relying on `npx`.

**"Connection refused"**

- Server isn't running or port is wrong
- Firewall blocking the connection
- Wrong transport type (stdio vs HTTP)

**"Command not found"**

- Missing full path to executable
- PATH not configured in the execution context
- On Windows: use `C:\\PROGRA~1\\...` for paths with spaces

**MCP tools don't appear but no error**

- Server starts but tools aren't registered
- Check server stdout for initialization messages
- Verify the server uses the correct MCP protocol version

**Expected:** Error pattern matched to one of the documented categories (cannot attach, connection refused, command not found, or silent failure).

**On failure:** If the error does not match any known pattern, capture the full error output and check server-side logs. Search for the exact error message in the MCP server's GitHub issues.

### Step 4: Check Network and Authentication

```bash
# Test Hugging Face API connectivity
curl -I "https://huggingface.co/mcp"

# Verify token validity
curl -H "Authorization: Bearer $HF_TOKEN" https://huggingface.co/api/whoami
```

**Expected:** HTTP endpoint returns 200 status and the whoami call returns your Hugging Face username, confirming network connectivity and valid authentication.

**On failure:** If curl returns a connection error, check DNS resolution and proxy settings. If the token is rejected (401), regenerate the token at huggingface.co/settings/tokens and update the configuration.

### Step 5: Verify JSON Configuration Syntax

```bash
# Validate JSON (common issue: trailing commas, missing quotes)
python3 -m json.tool /path/to/config.json
```

**Expected:** JSON parses without errors, confirming the configuration file has valid syntax.

**On failure:** The most common JSON issues are trailing commas after the last entry in an object or array, missing quotes around string values, and mismatched braces. Fix the syntax error reported by the parser and re-validate.

### Step 6: Platform-Specific Debugging

**Windows (Claude Desktop)**:
- Argument parsing differs from Unix
- Spaces in paths break command execution
- Use 8.3 short paths: `C:\PROGRA~1\R\R-45~1.0\bin\x64\Rscript.exe`
- Environment variables work more reliably than command-line headers

**WSL (Claude Code)**:
- Unix-style quoting works correctly
- Can use full paths with spaces (quoted)
- npm/npx via NVM: ensure NVM is loaded in the execution context

**Expected:** Platform-specific issue identified (e.g., Windows argument parsing, WSL path resolution, or NVM context loading).

**On failure:** If the issue is Windows-specific, switch from command-line arguments to environment variables for authentication. If WSL-specific, verify that the Windows executable path is accessible from WSL using the full `/mnt/c/...` path.

### Step 7: Reset and Reconfigure

If all else fails:

```bash
# Remove and re-add the server (Claude Code)
claude mcp remove server-name
claude mcp add server-name stdio "/full/path/to/executable" -- args

# Restart Claude Desktop after config changes
# (close and reopen the application)
```

**Expected:** After removing and re-adding the server, `claude mcp list` shows the server with the correct configuration and a fresh connection attempt succeeds.

**On failure:** If re-adding fails, check that the executable path is correct and the command works when run directly in the terminal. For Claude Desktop, ensure the application is fully closed (check system tray) before restarting.

### Step 8: Check Logs

**Claude Code**: Look for MCP errors in the terminal output when starting a session.

**Claude Desktop**: Check application logs (location varies by OS).

**Server-side**: Add logging to the MCP server to capture incoming requests and errors.

**Expected:** Log entries reveal the specific point of failure (server startup, handshake, authentication, or tool registration).

**On failure:** If no logs are available, add `stderr` capture to the server command (e.g., redirect to a log file) and reproduce the failure. For Claude Desktop, check `%APPDATA%\Claude\logs\` for application-level logs.

## Validation

- [ ] Server starts independently without errors
- [ ] Configuration JSON is valid
- [ ] Client connects successfully
- [ ] MCP tools appear in the session
- [ ] Tools execute correctly when called
- [ ] Connection persists across multiple requests

## Common Pitfalls

- **Editing the wrong config file**: Claude Code (`~/.claude.json`) vs Claude Desktop (`%APPDATA%\Claude\claude_desktop_config.json`)
- **Not restarting after config changes**: Claude Desktop requires restart; Claude Code picks up changes on new session
- **npx in restricted environments**: npx downloads packages at runtime. If network or permissions are restricted, install globally.
- **Token expiration**: Hugging Face tokens can expire. Regenerate if auth failures appear suddenly.
- **Version mismatches**: MCP protocol versions must be compatible between client and server

## Related Skills

- `configure-mcp-server` - initial MCP setup
- `build-custom-mcp-server` - custom server debugging context
- `setup-wsl-dev-environment` - WSL prerequisite setup
