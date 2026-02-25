---
name: install-mcpcat-python
description: Use when a user wants to add MCPCat analytics to their Python MCP server, install the mcpcat Python package, or integrate mcpcat.track() into an existing Python MCP server codebase.
---

# Integrate MCPCat into a Python MCP Server

MCPCat is a one-line SDK integration. It automatically tracks all tool calls, sessions, and user intent. You do NOT add tracking code inside tool functions — MCPCat hooks into the server at the protocol level.

## Step 1: Find the MCP server

Search all `.py` files for these import patterns (check in order):

1. `from mcp.server.fastmcp import FastMCP` or `from mcp.server import FastMCP` — **Official FastMCP**
2. `from fastmcp import FastMCP` — **Community FastMCP** (different package, needs `mcpcat[community]`)
3. `from mcp.server.lowlevel import Server` or `from mcp.server import Server` — **Low-level Server**

In the matched file, find the server variable assignment (e.g., `server = FastMCP(...)` or `app = Server(...)`). Store the variable name.

If `mcpcat.track` is already present in the file, tell the user MCPCat is already integrated and stop.

If multiple server instantiations exist, ask the user which one to instrument.

## Step 2: Get the project ID

If the user didn't provide a project ID (format: `proj_` followed by characters), ask them:

> What is your MCPCat project ID? (format: proj_xxxxx)
> Create a free account at https://mcpcat.io to get one.

## Step 3: Check peer dependency

Check the project's `pyproject.toml` or `requirements.txt` for the MCP SDK version:

- **Official MCP** (`from mcp.server...`): Requires `mcp >= 1.2.0`. If older, tell the user to upgrade.
- **Community FastMCP** (`from fastmcp import FastMCP`): Requires `fastmcp >= 2.7.0` and NOT `2.9.*`. If older or on 2.9.x, tell the user to upgrade/change version.

If the version can't be determined from project files, run `pip show mcp` or `pip show fastmcp` to check the installed version.

## Step 4: Install the package

First check if `mcpcat` (or `mcpcat[community]`) is already listed in the project's dependency files (`pyproject.toml` or `requirements.txt`). If it is already listed, skip this step.

If not listed, detect the package manager and install:

| Indicator | Command |
|-----------|---------|
| `uv.lock` or `[tool.uv]` in pyproject.toml | `uv add mcpcat` |
| `poetry.lock` | `poetry add mcpcat` |
| `Pipfile` | `pipenv install mcpcat` |
| `requirements.in` | Add `mcpcat` to `requirements.in`, then `pip-compile requirements.in` |
| Otherwise | Check the project's README and other `.md` files for dependency management instructions, then install accordingly |

**For community FastMCP** (import is `from fastmcp import FastMCP`), use `"mcpcat[community]"` instead of `mcpcat` in all install commands above.

`uv add`, `poetry add`, and `pipenv install` handle dependency files automatically — no extra step needed for those. For `pip-tools`, the dependency is tracked in `requirements.in`. For other package managers, ensure `mcpcat` is added to the appropriate dependency file after installation.

## Step 5: Add the integration code

Make two edits to the server file. Do NOT add tracking code inside tool functions — MCPCat does this automatically.

**1. Imports** — add at the top with other imports:

```python
import os
import mcpcat
from mcpcat import MCPCatOptions
```

Add `import os` only if not already present.

**2. Track call** — add AFTER the server variable is created, BEFORE `server.run()` or ASGI mounting:

```python
mcpcat.track(SERVER_VAR, "PROJECT_ID", MCPCatOptions(
    debug_mode=os.getenv("MCPCAT_DEBUG_MODE", "false").lower() in ("true", "1", "yes", "on")
))
```

Replace `SERVER_VAR` with the actual variable name (e.g., `server`, `app`, `mcp`) and `PROJECT_ID` with the user's project ID.

### Placement rules

- MUST be after the line that creates the server (e.g., `server = FastMCP(...)`)
- MUST be before `server.run()` or any ASGI app mounting
- Can go before or after `@server.tool()` definitions — both work. Before is canonical.
- If server is created inline (e.g., `export default FastMCP(...)`), refactor to assign to a variable first

### Why this MCPCatOptions pattern is required

The `MCPCAT_DEBUG_MODE` env var IS read at module load time, but `mcpcat.track()` calls `set_debug_mode(options.debug_mode)` which overrides it. Since `MCPCatOptions.debug_mode` defaults to `False`, calling `track()` without explicit options silently disables env-var-based debug mode. The pattern above preserves env var control. Debug logs are written to `~/mcpcat.log`.

### Complete example

A typical FastMCP server after integration:

```python
import os
import mcpcat
from mcpcat import MCPCatOptions
from mcp.server.fastmcp import FastMCP

server = FastMCP("weather-server", version="2.1.0")

mcpcat.track(server, "proj_abc123", MCPCatOptions(
    debug_mode=os.getenv("MCPCAT_DEBUG_MODE", "false").lower() in ("true", "1", "yes", "on")
))

@server.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: 72F, sunny"

if __name__ == "__main__":
    server.run()
```

Notice: zero tracking code inside `get_weather`. MCPCat automatically captures all tool calls at the protocol level.

## Step 6: Verify

1. Read the modified file and confirm the import and `track()` call are correctly placed.
2. Run `python -c "import mcpcat"` to verify the package is importable.
3. If the project uses a linter (ruff, mypy, pyright), run it if configured.
4. Tell the user:

> MCPCat is integrated. Your server will automatically report analytics when it runs.
> Enable debug logging: `MCPCAT_DEBUG_MODE=true python your_server.py` (logs to ~/mcpcat.log)
> View your dashboard at https://app.mcpcat.io

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Adding tracking code inside each tool function | MCPCat is automatic. Remove manual tracking. Only `mcpcat.track()` is needed. |
| Initializing MCPCat before server creation | `mcpcat.track(server, ...)` needs the server variable. Call it AFTER `server = FastMCP(...)`. |
| Using `pip install mcpcat` for community FastMCP | Use `pip install "mcpcat[community]"` when import is `from fastmcp import FastMCP`. |
| Using `MCPCatOptions()` without `debug_mode` | Defaults to `debug_mode=False`, overriding the env var. Pass it explicitly. |
| Using wrong env var name | The env var is `MCPCAT_DEBUG_MODE`, not `MCPCAT_DEBUG`. |
