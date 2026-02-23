---
name: mcp-creator
description: >-
  Build production-ready MCP servers using FastMCP v3. Guides research,
  scaffolding, tool/resource/prompt implementation, testing, and deployment.
  Targets FastMCP 3.0.0rc2 with Providers, Transforms, middleware, OAuth,
  and composition. Use when creating MCP servers, integrating APIs via MCP,
  converting OpenAPI specs or FastAPI apps, or troubleshooting FastMCP issues.
  NOT for building REST APIs, CLI tools, or non-MCP integrations.
license: MIT
argument-hint: "<service or API to integrate>"
model: opus
metadata:
  author: wyattowalsh
  version: "2.0"
---

# MCP Creator — FastMCP v3

Build production-ready MCP servers with FastMCP v3 (3.0.0rc2). This skill guides through research, scaffolding, implementation, testing, and deployment. All output follows this repo's conventions: `mcp/<name>/` directory, `fastmcp.json` config, `uv` workspace member, imperative voice, kebab-case naming.

**Target:** FastMCP v3 rc2 — Provider/Transform architecture, 14 built-in middleware, OAuth 2.1, server composition, component versioning, structured output, background tasks, elicitation, sampling.

**Input:** `$ARGUMENTS` — the service, API, or capability to wrap as an MCP server.

---

## Dispatch

Route `$ARGUMENTS` to the appropriate mode:

| $ARGUMENTS pattern | Mode | Start at |
|---------------------|------|----------|
| Service/API name (e.g., "GitHub", "Stripe") | **New server** | Phase 1 |
| Path to existing server (e.g., `mcp/myserver/`) | **Extend** | Phase 3 |
| OpenAPI spec URL or file path | **Convert OpenAPI** | Phase 2 (scaffold) then load `references/server-composition.md` §6 |
| FastAPI app to convert | **Convert FastAPI** | Phase 2 (scaffold) then load `references/server-composition.md` §7 |
| Error message or "debug" + description | **Debug** | Load `references/common-errors.md`, match symptom |
| "learn" or conceptual question | **Learn** | Load relevant reference file, explain |
| Empty | **Gallery / help overview** | Show available modes and example invocations |

---

## Consult Live Documentation

Before implementation, fetch current FastMCP v3 docs. Bundled references capture rc2 — live docs may be newer.

1. **Context7** — `resolve-library-id` for "fastmcp", then `query-docs` for the topic.
2. **WebFetch** — `https://gofastmcp.com/llms-full.txt` — comprehensive LLM-optimized docs.
3. **WebSearch fallback** — `site:gofastmcp.com <topic>` for specific topics.

If live docs contradict bundled references, **live docs win**. Always fetch live docs first — API details shift between rc2 and stable.

---

## Phase 1: Research & Plan

**Goal:** Understand the target service and design the MCP server's tool/resource/prompt inventory.

**Load:** `references/tool-design.md` (naming, descriptions, parameter design, 8 tool patterns)

### 1.1 Understand the Target

- Read any documentation, SDK, or API reference for the target service.
- Identify the core operations users need (CRUD, search, status, config).
- Note authentication requirements (API keys, OAuth, tokens).
- Check for existing MCP servers for this service — avoid duplicating work.

### 1.2 Architecture Checklist

Answer before proceeding:

- [ ] Auth needed? (API key → env var, OAuth → HTTP transport, none → stdio)
- [ ] Transport? (stdio for local, Streamable HTTP for remote/multi-client)
- [ ] Background tasks? (long-running operations → `task=True`, requires `fastmcp[tasks]`)
- [ ] OpenAPI spec available? (→ `OpenAPIProvider` or `FastMCP.from_openapi()`)
- [ ] Multiple domains? (→ composed servers with `mount()` + namespaces)

### 1.3 Design Tool Inventory

Plan 5-15 tools per server. For each tool, define:

| Field | Requirement |
|-------|-------------|
| Name | `snake_case`, `verb_noun` format, max 64 chars |
| Description | 3-5 sentences: WHAT, WHEN to use, WHEN NOT, WHAT it returns |
| Parameters | Each with type, description, constraints via `Annotated[type, Field(...)]` |
| Annotations | `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint` |
| Error cases | What `ToolError` messages to raise for expected failures |

### 1.4 Design Resources and Prompts

- **Resources** for static/slow-changing data (config, schemas, status). URI-addressed.
- **Prompts** for reusable message templates that guide LLM behavior.
- See `references/fastmcp-v3-api.md` §6-7 for URI patterns and prompt design.

### 1.5 Plan Architecture

Decide on composition strategy:

- **Single server** — Most cases. One `FastMCP` instance with all tools.
- **Composed servers** — Large APIs. Domain servers mounted via `mount()` with namespaces.
- **Provider-based** — Dynamic tool registration. `FileSystemProvider` or custom `Provider`.
- **OpenAPI conversion** — Auto-generate tools from OpenAPI spec. `OpenAPIProvider` or `FastMCP.from_openapi()`.

See `references/server-composition.md` for patterns.

### 1.6 Deliverable

Produce a tool/resource/prompt inventory table before proceeding:

```markdown
| Component | Type | Name | Description (brief) |
|-----------|------|------|---------------------|
| Tool | tool | search_issues | Search GitHub issues by query |
| Resource | resource | config://settings | Current server configuration |
| Prompt | prompt | summarize_pr | Summarize a pull request for review |
```

---

## Phase 2: Scaffold

**Goal:** Create the project directory, tests, and configure dependencies.

### 2.1 Create Project Structure

Run `wagents new mcp <name>` to scaffold:

```
mcp/<name>/
├── server.py          # FastMCP entry point
├── pyproject.toml     # uv project config
├── fastmcp.json       # FastMCP CLI config
└── tests/
    ├── conftest.py    # Client fixture, mock Context
    └── test_server.py # Automated test suite
```

Customize the scaffold:
- Set server name in `server.py`: `mcp = FastMCP("name")`.
- Set package name in `pyproject.toml`: `name = "mcp-<name>"`.
- Update description in `pyproject.toml`.
- Add service-specific dependencies to both `pyproject.toml` and `fastmcp.json`.

### 2.2 Add Test Configuration

Add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"

[dependency-groups]
dev = ["pytest>=8", "pytest-asyncio>=0.25"]
```

Create `tests/conftest.py` — see `references/testing.md` §4 for the complete template.

### 2.3 Configure and Verify

- Ensure root `pyproject.toml` has `[tool.uv.workspace] members = ["mcp/*"]`.
- Run `cd mcp/<name> && uv sync` to install dependencies.
- Verify: `uv run python -c "from server import mcp; print(mcp.name)"`.

Note: `wagents validate` validates skills/agents only, NOT MCP servers. Use the import check above for MCP server validation.

---

## Phase 3: Implement

**Goal:** Build all tools, resources, and prompts from the Phase 1 inventory.

**Load:** `references/fastmcp-v3-api.md` (full API surface), `references/tool-design.md` (patterns)

### 3.1 Server Setup

```python
from fastmcp import FastMCP, Context

mcp = FastMCP(
    "server-name",
    instructions="Description of what this server provides and when to use it.",
)
```

For shared resources (HTTP clients, DB connections), add a composable lifespan:

```python
from fastmcp.server.lifespan import lifespan

@lifespan
async def http_lifespan(server):
    import httpx
    async with httpx.AsyncClient() as client:
        yield {"http": client}

mcp = FastMCP("server-name", lifespan=http_lifespan)
# Access in tools: ctx.lifespan_context["http"]
```

Combine lifespans with `|`: `mcp = FastMCP("name", lifespan=db_lifespan | cache_lifespan)`

### 3.2 Implement Tools

For each tool in the inventory, follow this pattern:

```python
from typing import Annotated
from pydantic import Field
from fastmcp import Context
from fastmcp.exceptions import ToolError

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "openWorldHint": True,
    },
)
async def search_items(
    query: Annotated[str, Field(description="Search term to find items.", min_length=1)],
    limit: Annotated[int, Field(description="Max results to return.", ge=1, le=100)] = 10,
    ctx: Context | None = None,
) -> dict:
    """Search for items matching a query.

    Use this tool when you need to find items by keyword. Returns a list of
    matching items with their IDs and titles. Use the limit parameter to
    control result count. Does not search archived items.

    Returns a dictionary with 'items' list and 'total' count.
    """
    if ctx:
        await ctx.info(f"Searching for: {query}")
    try:
        results = await do_search(query, limit)
        return {"items": results, "total": len(results)}
    except ServiceError as e:
        raise ToolError(f"Search failed: {e}")
```

**Key rules for every tool:**
- `Annotated[type, Field(description=...)]` on EVERY parameter.
- Verbose docstring: WHAT, WHEN to use, WHEN NOT, WHAT it returns.
- `ToolError` for expected failures (always visible to client).
- `annotations` dict on every tool — at minimum `readOnlyHint`.
- `ctx: Context | None = None` for testability without MCP runtime.

See `references/tool-design.md` §9 for 8 complete tool patterns (sync, async+Context, stateful, external API, data processing, dependency-injected, sampling, elicitation).

### 3.3 Implement Resources

```python
import json

@mcp.resource("config://settings", mime_type="application/json")
async def get_settings() -> str:
    """Current server configuration."""
    return json.dumps(settings)

@mcp.resource("users://{user_id}/profile")
async def get_user_profile(user_id: str) -> str:
    """User profile by ID."""
    return json.dumps(await fetch_profile(user_id))
```

See `references/fastmcp-v3-api.md` §6 for URI templates, query params, wildcards, and class-based resources.

### 3.4 Implement Prompts

```python
from fastmcp.prompts import Message

@mcp.prompt
def summarize_pr(pr_number: int, detail_level: str = "brief") -> list[Message]:
    """Generate a prompt to summarize a pull request."""
    return [Message(
        role="user",
        content=f"Summarize PR #{pr_number} at {detail_level} detail level.",
    )]
```

### 3.5 Composition (if applicable)

For large servers, split into domain modules and compose. See `references/server-composition.md`.

```python
from fastmcp import FastMCP
from .issues import issues_server
from .repos import repos_server

mcp = FastMCP("github")
mcp.mount(issues_server, namespace="issues")
mcp.mount(repos_server, namespace="repos")
```

### 3.6 Auth (if applicable)

Load `references/auth-and-security.md` when implementing authentication.

- **stdio transport:** No MCP-level auth. Use env vars for backend API keys.
- **HTTP transport:** OAuth 2.1 via `JWTVerifier`, `GitHubProvider`, or `RemoteAuthProvider`.
- **Per-tool auth:** `@mcp.tool(auth=require_scopes("admin"))`.
- **Dual-mode pattern:** `common.py` with shared tools, separate auth/no-auth entry points.

---

## Phase 4: Test

**Goal:** Verify all components work correctly with deterministic tests.

**Load:** `references/testing.md` (patterns, 18-item checklist)

### 4.1 Write Tests

Use the in-memory `Client` — no network, no subprocess:

```python
import pytest
from fastmcp import Client
from server import mcp

@pytest.fixture
async def client():
    async with Client(mcp) as c:
        yield c

async def test_search_items(client):
    result = await client.call_tool("search_items", {"query": "test"})
    assert result.data is not None
    assert not result.is_error

async def test_list_tools(client):
    tools = await client.list_tools()
    names = [t.name for t in tools]
    assert "search_items" in names
```

### 4.2 Test Categories

Cover all 8 categories from `references/testing.md`:

1. **Discovery** — `list_tools()`, `list_resources()`, `list_prompts()` return expected names.
2. **Happy path** — Each tool with valid input returns expected output.
3. **Error handling** — Invalid input produces `ToolError`, not crashes.
4. **Edge cases** — Empty strings, boundary values, Unicode, large inputs.
5. **Resources** — `read_resource(uri)` returns correct content and MIME type.
6. **Prompts** — `get_prompt(name, args)` returns expected messages.
7. **Integration** — Tool chains, lifespan setup/teardown.
8. **Concurrent** — Multiple simultaneous calls don't interfere.

### 4.3 Interactive Testing

```bash
# MCP Inspector (browser-based)
fastmcp dev inspector mcp/<name>/server.py

# CLI testing
fastmcp list mcp/<name>/server.py
fastmcp call mcp/<name>/server.py search_items '{"query": "test"}'
```

### 4.4 Run Tests

```bash
cd mcp/<name> && uv run pytest -v
```

---

## Phase 5: Deploy & Configure

**Goal:** Make the server available to MCP clients.

**Load:** `references/deployment.md` (transports, client configs, Docker)

### 5.1 Select Transport

| Scenario | Transport | Command |
|----------|-----------|---------|
| Local / Claude Desktop | stdio | `fastmcp run server.py` |
| Remote / multi-client | Streamable HTTP | `fastmcp run server.py --transport http --port 8000` |
| Development | Inspector | `fastmcp dev inspector server.py` |

### 5.2 Generate Client Config

Add to client config (Claude Desktop, Claude Code, Cursor):

```json
{
  "mcpServers": {
    "server-name": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp/<name>", "fastmcp", "run", "server.py"]
    }
  }
}
```

See `references/deployment.md` §7 for complete configs per client.

### 5.3 Validate

MCP server validation (wagents validate does NOT check MCP servers):

```bash
# Import check
uv run python -c "from server import mcp; print(mcp.name)"

# List registered components
fastmcp list mcp/<name>/server.py

# Interactive inspection
fastmcp dev inspector mcp/<name>/server.py
```

### 5.4 Quality Checklist

Before declaring the server complete:

- [ ] Every tool has `Annotated` + `Field(description=...)` on all parameters
- [ ] Every tool has a verbose docstring (WHAT, WHEN, WHEN NOT, RETURNS)
- [ ] Every tool has `annotations` (at minimum `readOnlyHint`)
- [ ] Every tool uses `ToolError` for expected failures
- [ ] No `print()` or `stdout` writes in any tool
- [ ] Resources have correct URI schemes and MIME types
- [ ] Tests pass: `uv run pytest -v`
- [ ] MCP Inspector shows all components correctly
- [ ] `fastmcp.json` lists all required dependencies
- [ ] `pyproject.toml` has correct metadata and dependencies
- [ ] No deprecated constructor kwargs (removed in rc1)
- [ ] Custom routes have manual auth if sensitive
- [ ] `mask_error_details=True` set for production deployment

---

## Reference File Index

Load these files on demand during the relevant phase. Do NOT load all at once.

| File | Content | Load during |
|------|---------|-------------|
| `references/fastmcp-v3-api.md` | Complete v3 API surface: constructor, decorators, Context, return types, resources, prompts, providers, transforms, 14 middleware, background tasks, visibility, v2→v3 changes | Phase 3 |
| `references/tool-design.md` | LLM-optimized naming, descriptions, parameters, annotations, error handling, 8 tool patterns, structured output, response patterns, anti-patterns | Phase 1, 3 |
| `references/server-composition.md` | mount(), import_server(), proxy, FileSystemProvider, OpenAPI (OpenAPIProvider + from_openapi), FastAPI conversion, custom providers, transforms, gateway pattern, DRY registration | Phase 1, 3 |
| `references/testing.md` | In-memory Client, pytest setup, conftest.py template, 8 test categories, MCP Inspector, CLI testing, 18-item checklist | Phase 4 |
| `references/auth-and-security.md` | OAuth 2.1, JWTVerifier, per-component auth, custom auth checks, session-based visibility, custom route auth bypass, SSRF prevention, dual-mode pattern, 15 security rules | Phase 3 |
| `references/deployment.md` | Transports, FastMCP CLI, ASGI, custom routes, client configs, fastmcp.json schema, Docker, background task workers, production checklist | Phase 5 |
| `references/resources-and-prompts.md` | Resources (static, dynamic, binary), prompts (single/multi-message), resource vs tool guidance, testing patterns | Phase 3 |
| `references/common-errors.md` | 34 errors: symptom → cause → v3-updated fix, quick-fix lookup table | Debug mode |
| `references/quick-reference.md` | Minimal examples: server, tool, resource, prompt, lifespan, test, run | Quick start |

---

## Critical Rules

These are non-negotiable. Violating any of these produces broken MCP servers.

1. **No stdout.** Never use `print()` or write to stdout in tools/resources/prompts. Stdout is the MCP transport. Use `ctx.info()`, `ctx.warning()`, `ctx.error()` for logging.

2. **ToolError for expected failures.** Always `raise ToolError("message")` for user-facing errors. Standard exceptions are masked by `mask_error_details` in production.

3. **Verbose descriptions.** Every tool needs a 3-5 sentence docstring. Every parameter needs `Field(description=...)`. LLMs cannot use tools they don't understand.

4. **Annotations on every tool.** Set `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`. Clients use these for confirmation flows and retry logic.

5. **No `*args` or `**kwargs`.** MCP requires a fixed JSON schema for tool inputs. Dynamic signatures break schema generation.

6. **Async state access.** In v3, `ctx.get_state()` and `ctx.set_state()` are async — always `await` them.

7. **URI schemes required.** Every resource URI must have a scheme (`data://`, `config://`, `users://`). Bare paths fail.

8. **Test deterministically.** Use in-memory `Client(mcp)`, not manual prompting. Tests must be repeatable and automated.

9. **Module-level `mcp` variable.** The `FastMCP` instance must be importable at module level. `fastmcp run` imports `server:mcp` by default.

10. **Secrets in env vars only.** Never hardcode API keys. Never accept tokens as tool parameters. Load from environment, validate on startup.

---

## Quick Reference

Load `references/quick-reference.md` for the complete quick reference with minimal examples for server, tool, resource, prompt, lifespan, test, and run commands.

---

## Canonical Vocabulary

Use these terms consistently. Do not invent synonyms.

| Canonical term | Meaning | NOT |
|----------------|---------|-----|
| **tool** | A callable MCP function exposed to clients | "endpoint", "action", "command" |
| **resource** | URI-addressed read-only data exposed to clients | "asset", "file", "data source" |
| **prompt** | Reusable message template guiding LLM behavior | "instruction", "system message" |
| **provider** | Dynamic component source (e.g., `FileSystemProvider`, `OpenAPIProvider`) | "plugin", "adapter" |
| **transform** | Middleware that modifies components at mount time | "filter", "interceptor" |
| **middleware** | Request/response processing hook in the server pipeline | "handler", "decorator" |
| **lifespan** | Async context manager for shared server resources | "startup hook", "init" |
| **mount** | Attach a child server with a namespace prefix | "register", "include" |
| **namespace** | Prefix added to component names during mount | "scope", "prefix" |
| **Context** | Runtime object passed to tools for logging, state, sampling | "request", "session" |
| **ToolError** | Exception class for user-visible error messages | "raise Exception" |
| **annotation** | Tool metadata hints (`readOnlyHint`, `destructiveHint`, etc.) | "tag", "label" |
| **transport** | Communication layer: stdio or Streamable HTTP | "protocol", "channel" |
