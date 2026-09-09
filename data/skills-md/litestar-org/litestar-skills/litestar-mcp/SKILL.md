---
name: litestar-mcp
description: "Auto-activate for litestar_mcp, LitestarMCP, MCP, MCPConfig, mcp.app, mcp.run(), @mcp.tool/resource/prompt, MCPAuthConfig, MCPAuthBackend, mcp_tool=, mcp_resource=, Streamable HTTP, stdio, or OIDC MCP endpoints. Not for non-Litestar MCP servers or clients — use the official MCP Python SDK instead."
---

# litestar-mcp

`litestar-mcp` exposes explicitly marked Litestar route handlers as [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) tools, resources, and prompts over JSON-RPC 2.0.

Version `0.13.0` follows the stateless MCP specification (protocol `2026-07-28`). The transport is **POST-only and request-scoped**: the legacy `initialize` handshake, sessions and `Mcp-Session-Id`, `ping`, `GET` and `DELETE` transport handlers, replay, and `/.well-known/mcp-server.json` are removed. Each request supplies protocol version, method, and client capabilities; named calls also supply matching name or URI metadata. Call `server/discover` for capabilities. See [Stateless Protocol](references/stateless-protocol.md).

Mark routes by passing `mcp_tool="name"`, `mcp_resource="name"`, or `mcp_prompt="name"` directly to the Litestar route decorator — Litestar funnels unknown kwargs into `handler.opt`, so no `opt={...}` wrapper is needed. Use the decorator forms for structured metadata: `@mcp_tool` adds schemas, annotations, scopes, and task policy; `@mcp_prompt` adds title, arguments, and icons. Route description keys are `mcp_description`, `mcp_resource_description`, and `mcp_prompt_description`; `MCPOptKeys` can rename every key the plugin reads. There is no `opt={"mcp_tool_name": ...}` form or `mcp_exclude` key. To hide a route, leave it unmarked.

## Code Style Rules

- PEP 604 unions: `T | None`, never `Optional[T]`
- Consumer Litestar app modules MAY use `from __future__ import annotations`
- Async all I/O. Pure standalone `@mcp.tool` / `@mcp.resource` / `@mcp.prompt` functions may be sync; keep blocking I/O out of the event loop.

## Quick Reference

### Install

```bash
pip install litestar-mcp
```

Or install with bridge extras for the stdio-to-HTTP proxy:

```bash
pip install "litestar-mcp[bridge]"
```

### Basic Setup

```python
from litestar import Litestar, get, post
from litestar_mcp import LitestarMCP, MCPConfig


@get("/users", mcp_tool="list_users")
async def list_users() -> list[dict[str, str | int]]:
    """List all registered users."""
    return [{"id": 1, "name": "Alice"}]


@post("/analyze", mcp_tool="analyze_data")
async def analyze_data(data: dict[str, str]) -> dict[str, int]:
    """Analyze provided key-value dataset."""
    return {"count": len(data)}


@get("/config", mcp_resource="app_config")
async def get_app_config() -> dict[str, bool]:
    """Read the active application configuration."""
    return {"debug": False}


app = Litestar(
    route_handlers=[list_users, analyze_data, get_app_config],
    plugins=[LitestarMCP(MCPConfig(name="My API"))],
)
```

The default MCP surface is:

| Endpoint | Purpose |
| --- | --- |
| `POST /mcp` | The only transport route. JSON-RPC endpoint for `server/discover`, `tools/*`, `resources/*`, `prompts/*`, `completion/complete`, `subscriptions/listen`, and optional task methods |
| `GET /.well-known/agent-card.json` | Agent card metadata (enabled by `register_agent_card=True`) |
| `GET /.well-known/oauth-protected-resource` | RFC 9728 OAuth protected-resource metadata (enabled by `register_oauth_protected_resource=True`; populated from `auth`) |

### MCPConfig

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `base_path` | `str` | `"/mcp"` | URL prefix for the MCP transport endpoint |
| `include_in_schema` | `bool` | `False` | Include the MCP router and all `/.well-known/*` discovery routes in OpenAPI |
| `name` | `str \| None` | `None` | Server name; defaults to OpenAPI title |
| `instructions` | `str \| None` | `None` | Server instructions advertised to MCP clients |
| `guards` | `list[Any] \| None` | `None` | Litestar guards applied to the MCP router |
| `route_opt` | `dict[str, Any] \| None` | `None` | Route `opt` mapping applied to the mounted MCP router (e.g. for opt-based auth/permission policies) |
| `register_oauth_protected_resource` | `bool` | `True` | Whether to register RFC 9728 `/.well-known/oauth-protected-resource` route; disable when another plugin owns root discovery |
| `register_agent_card` | `bool` | `True` | Whether to register `/.well-known/agent-card.json` discovery route |
| `allowed_origins` | `list[str] \| None` | `None` | Restrict accepted `Origin` headers |
| `include_operations` | `list[str] \| None` | `None` | Only expose matching operation names |
| `exclude_operations` | `list[str] \| None` | `None` | Exclude matching operation names |
| `include_tags` | `list[str] \| None` | `None` | Only expose routes with matching OpenAPI tags |
| `exclude_tags` | `list[str] \| None` | `None` | Exclude routes with matching OpenAPI tags |
| `auth` | `MCPAuthConfig \| None` | `None` | OAuth protected-resource metadata |
| `tasks` | `bool \| MCPTaskConfig` | `False` | Enable MCP task support. Pass `MCPTaskConfig` to configure the backing `Store` and record TTLs |
| `opt_keys` | `MCPOptKeys` | `MCPOptKeys()` | Rename the `handler.opt` keys the plugin reads |
| `cache_ttl_ms` | `int` | `0` | Response cache lifetime in milliseconds; `0` disables caching |
| `cache_scope` | `Literal["private", "public"]` | `"private"` | Whether cached responses may be shared between callers |
| `subscription_max_streams` | `int` | `10000` | Max concurrent SSE streams |
| `subscription_keepalive_seconds` | `float` | `15.0` | Seconds between SSE keepalive pings |
| `subscription_channels` | `Any \| None` | `None` | Channels backend backing `subscriptions/listen` fan-out |
| `list_page_size` | `int` | `100` | Page size for `tools/list`, `resources/list`, `resources/templates/list`, `prompts/list` |
| `before_tool_call` | `BeforeToolCallHook \| None` | `None` | Observe each `tools/call` before dispatch |
| `after_tool_call` | `AfterToolCallHook \| None` | `None` | Observe each `tools/call` result, exception, and duration |
| `max_blob_bytes` | `int \| None` | `25 * 1024 * 1024` | Maximum raw byte length for base64-embedded blobs; `None` disables the cap |

> Filters (`include_tags` / `exclude_tags` / `include_operations` / `exclude_operations`) gate both list responses and direct invocation. A filtered tool/resource/template behaves like an unknown name or URI in `tools/call` / `resources/read`; still use `guards` / auth for real access control.

### Route Marking

```python
from litestar import get, post


@get("/products", mcp_resource="product_list")
async def list_products() -> list[dict[str, str]]:
    """List all available products in the catalog."""
    return [{"id": "sku-1", "name": "Widget"}]


@post("/cart/items", mcp_tool="add_to_cart")
async def add_to_cart(data: dict[str, int]) -> dict[str, str]:
    """Add a product item to the shopping cart."""
    return {"status": "added"}


@get(
    "/products/{product_id:int}",
    mcp_resource="product",
    mcp_resource_template="shop://products/{product_id}",
)
async def get_product(product_id: int) -> dict[str, int | str]:
    """Fetch details for a single product by identifier."""
    return {"id": product_id, "name": "Widget"}


@get("/products/{product_id:int}/blurb", mcp_prompt="product_blurb")
async def product_blurb(product_id: int) -> str:
    """Write a short marketing blurb for a product."""
    return f"Product {product_id} is top tier."
```

`mcp_resource_template` takes effect alongside `mcp_resource` — the resource supplies the name the template binds to. A handler can expose more than one MCP role (a tool and a resource) at once; the description-override keys (`mcp_description` vs `mcp_resource_description`) are kind-specific so each surface can carry its own prose.

Register prompts not bound to a route with the `@mcp_prompt` decorator plus `LitestarMCP(prompts=[...])`:

```python
from litestar import Litestar
from litestar_mcp import LitestarMCP, mcp_prompt


@mcp_prompt("summarize", description="Summarize a document for the user.")
def summarize(text: str) -> str:
    """Produce a summarization prompt for the supplied text."""
    return f"Summarize the following:\n\n{text}"


app = Litestar(plugins=[LitestarMCP(prompts=[summarize])])
```

Use structured metadata when the agent needs sharper tool selection:

```python
from litestar import post
from litestar_mcp import mcp_tool


@post("/reports")
@mcp_tool(
    name="generate_report",
    description="Generate a report for an existing account.",
    agent_instructions="Ensure account ID exists before calling.",
    when_to_use="Use after the user has confirmed the account and date range.",
    returns="A report id and queued status.",
    scopes=["reports:write"],
    task_support="optional",
)
async def generate_report(data: dict[str, str]) -> dict[str, str]:
    """Create a new reporting job."""
    return {"report_id": "rep-123", "status": "queued"}
```

### Accessing Request Context

Retrieve active MCP scope and metadata inside tool, resource, or prompt handlers with `get_mcp_request_context()`:

```python
from litestar import post
from litestar_mcp import MCPRequestContext, get_mcp_request_context


@post("/agent-session", mcp_tool="record_session")
async def record_session(note: str) -> dict[str, str]:
    """Record a note attached to the calling MCP client."""
    ctx: MCPRequestContext = get_mcp_request_context()
    return {
        "client_id": ctx.client_id,
        "owner_id": ctx.owner_id or "anonymous",
        "note": note,
    }
```

### Standalone MCP App

Use `MCP(...)` when the application is primarily an MCP server. Use `LitestarMCP(...)` when adding MCP to an existing Litestar app.

```python
from litestar_mcp import MCP

mcp = MCP("inventory-mcp", instructions="Expose inventory tools.")


@mcp.tool(name="lookup_product", description="Look up a product by SKU.")
def lookup_product(sku: str) -> dict[str, str]:
    """Return product status for the requested SKU."""
    return {"sku": sku, "status": "active"}


@mcp.resource(uri="inventory://status", name="inventory_status")
def inventory_status() -> dict[str, str]:
    """Return inventory service health."""
    return {"status": "healthy"}


@mcp.prompt(name="summarize_product")
def summarize_product(sku: str) -> str:
    """Create a prompt summarizing a product."""
    return f"Summarize product {sku}."


app = mcp.app


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

`mcp.app` lazily builds the underlying `Litestar` instance; access it after registering standalone decorators. `@mcp.tool`, `@mcp.resource`, and `@mcp.prompt` accept normal Litestar route-handler kwargs such as `dependencies`, `guards`, `tags`, DTO options, hooks, and `sync_to_thread`. The `name` kwarg names the MCP primitive; use `route_name` when the Litestar route handler itself needs a name.

`MCP(...)` also accepts `config=`, existing `plugins=`, existing `route_handlers=`, and standard `Litestar(...)` app kwargs.

`mcp.run(transport="sse", port=8000)` starts the HTTP/SSE transport through the Litestar CLI, so expose `app = mcp.app` at module scope or set `LITESTAR_APP` for worker/reload discovery. `mcp.run(transport="stdio")` reads line-delimited JSON-RPC from stdin, writes responses to stdout, manually drives ASGI lifespan, and dispatches through the same JSON-RPC router with a synthetic request context.

#### Direct stdio identity

Stdio has no HTTP headers or authentication middleware. Resolve credentials in the host process and inject the resulting identity with `MCPStdioContext`:

```python
from litestar_mcp import MCP, MCPStdioContext

mcp = MCP("inventory-mcp")
stdio_context = MCPStdioContext(
    client_id="desktop-agent",
    owner_id="alice",
    auth={"sub": "alice", "role": "operator"},
    session={"tenant": "acme"},
    state={"deployment": "production"},
)
mcp.run(transport="stdio", stdio_context=stdio_context)
```

The synthetic Litestar request exposes `user`, `auth`, `session`, and `state` to handlers, guards, resources, and dependency providers. Mapping values are copied per dispatch, so handler mutations do not alter the supplied context or leak into later calls. Task ownership resolves in this order: explicit `owner_id`, `auth["sub"]`, `user.id`, `user.sub`, then `"stdio"`.

#### Stdio-to-Streamable-HTTP bridge

Use the bridge when a local MCP client speaks stdio but the real server is an already-running Streamable HTTP endpoint:

```bash
pip install "litestar-mcp[bridge]"
litestar mcp bridge \
  --endpoint https://api.example.com/mcp \
  --bearer-env MCP_ACCESS_TOKEN
```

The bridge forwards newline-delimited JSON-RPC. It forwards independent request-scoped POST streams in parallel, multiplexes subscription responses, maps cancellation to stream closure, and lazily maps annotated tool parameters to MCP headers. Stdout contains JSON-RPC only; transport diagnostics go to stderr.

Use `--header "Name: value"` for static headers. Use exactly one of `--bearer-env` or `--bearer-cmd` for a token resolved per request; the bridge retries once with a fresh token after `401`. Match identity-proxy schemes with `--header-name` and `--token-prefix`.

For programmatic embedding, import `run_stdio_streamable_http_bridge` from `litestar_mcp.bridge`. It accepts injectable AnyIO stdin/stdout streams and a sync or async token provider, then returns process-style status `0` for clean EOF and `1` after emitting a bridge JSON-RPC error.

The default stdin frame limit is 16 MiB. Set `--max-message-size`; use `-1` to disable that limit. This is separate from `MCPConfig.max_blob_bytes`, which limits decoded binary payloads produced by the server.

### Binary Resources And Tool Results

Return `MCPResourceLink` from a tool when a stable resource URI can be fetched later. Return `MCPBlobResource` only when the binary must be embedded immediately. Use `MCPToolResult` when one result needs mixed content blocks, `structuredContent`, `isError`, or `_meta`. Use `MCPInputRequiredResult` when multi-round-trip client inputs are requested.

```python
from litestar import Response, get
from litestar_mcp import MCPResourceLink


@get("/reports/latest-link", mcp_tool="generate_report")
async def generate_report() -> MCPResourceLink:
    """Provide a linked resource pointing to the generated report."""
    return MCPResourceLink(
        name="report.pdf",
        uri="litestar://latest_report",
        mime_type="application/pdf",
        size=4,
    )


@get(
    "/reports/latest",
    mcp_resource="latest_report",
    mcp_resource_mime_type="application/pdf",
)
async def latest_report() -> Response[bytes]:
    """Stream binary content for the latest report."""
    return Response(content=b"%PDF", media_type="application/pdf")
```

This produces a `resource_link` block from `tools/call`; `resources/read` returns the response bytes as a base64 `blob`. `MCPBlobResource(uri=..., data=..., mime_type=...)` produces an embedded `resource` block directly in a tool result. The plugin enforces `max_blob_bytes` before base64 encoding for helper objects, explicit resource blocks, and `resources/read`. An oversized tool payload becomes a tool result with `isError: true`; an oversized resource becomes a `Resource read failed` JSON-RPC error.

Set resource MIME metadata with `mcp_resource_mime_type=` on a Litestar route, `mime_type=` on `@mcp_resource`, or `mime_type=` on `@mcp.resource`. The handler response `Content-Type` wins during `resources/read`; configured metadata is the fallback and the value advertised by resource listings. The default is `application/json`.

Textual MIME types return `text`: `text/*`, JSON, XML, JavaScript, and YAML types are textual. Other MIME types return base64 `blob`; invalid UTF-8 under an otherwise textual MIME type also falls back to `blob`.

### Multi-Round-Trip Inputs

Return `MCPInputRequiredResult` when a tool or task requires additional information from the client before proceeding:

```python
from litestar import post
from litestar_mcp import MCPInputRequiredResult, MCPRequestContext, get_mcp_request_context


@post("/deploy", mcp_tool="deploy_service")
async def deploy_service(environment: str) -> MCPInputRequiredResult | dict[str, str]:
    """Deploy service with confirmation on production."""
    ctx: MCPRequestContext = get_mcp_request_context()
    if environment == "production":
        if not ctx.input_responses or "confirm" not in ctx.input_responses:
            return MCPInputRequiredResult(
                input_requests={
                    "confirm": {
                        "type": "boolean",
                        "description": "Confirm production deployment",
                    }
                },
                request_state="awaiting_confirmation",
            )
    return {"status": "deployed", "environment": environment}
```

### CLI Commands

The `litestar-mcp` CLI extension provides commands under the `mcp` group:

```bash
# List all registered tools in the application
litestar mcp list-tools

# List all registered resources in the application
litestar mcp list-resources

# Run a specific tool or resource handler locally
litestar mcp run list_users

# Run the Stdio-to-Streamable-HTTP bridge
litestar mcp bridge --endpoint http://127.0.0.1:8000/mcp
```

### Hiding Routes

Discovery is opt-in: a handler that carries no `mcp_*` marker never appears in MCP. There is no per-route exclude flag — `opt={"mcp_exclude": True}` is ignored.

```python
from litestar import get


@get("/internal/metrics")
async def metrics() -> dict[str, int]:
    """Internal metrics handler omitted from MCP."""
    return {"active_connections": 42}
```

To drop marked routes in bulk, use `MCPConfig` filters (`exclude_tags` / `exclude_operations`, or `include_tags` / `include_operations` allowlists). Filtered tools/resources/templates are absent from list responses and fail direct calls as unknown; enforce real access control with `guards` or auth.

### JSON-RPC Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "add_to_cart",
    "arguments": { "product_id": 42, "quantity": 3 }
  }
}
```

### Pagination, Signatures, And Errors

`tools/list`, `resources/list`, `resources/templates/list`, and `prompts/list` use opaque cursor pagination. Clients pass `params.cursor` from `nextCursor` until the response omits it; clients do not send `limit`. Set server page size with `MCPConfig(list_page_size=...)`; invalid cursors return `INVALID_PARAMS` (`-32602`).

Tool arguments are validated against Litestar's `handler.parsed_fn_signature` before dispatch.

Tool execution errors stay inside the tool result with `isError: true`; protocol errors such as unknown tool names use JSON-RPC errors. Resource and prompt handler failures use primitive-level JSON-RPC codes and preserve the handler HTTP status in `error.data.statusCode` when a handler response produced one.

### Tool-Call Callbacks

Use `MCPConfig.before_tool_call` and `MCPConfig.after_tool_call` for audit, metrics, or tracing that must fire around `tools/call` regardless of route ownership. Both callbacks receive the MCP tool name, a shallow copy of submitted arguments, and the synthesized `Request`. `after_tool_call` also receives keyword-only `result`, `exception`, and `duration`; it fires for successes, guard failures, handled error responses, and unhandled exceptions. Callback exceptions are logged and swallowed.

### Dependency Providers And Dishka

Litestar `Provide(...)` factory parameters that are user inputs, such as pagination or filter values, remain in tool schemas and forward during `tools/call`. When `dishka.integrations.litestar.setup_dishka()` is attached, provider-factory parameters whose annotated type is resolvable from `app.state.dishka_container` are treated as DI inputs instead of MCP arguments. Dishka remains optional.

### Built-in OpenAPI Resource

`LitestarMCP` exposes the app OpenAPI schema as:

- URI: `litestar://openapi`
- MIME type: `application/json`
- Method: `resources/read`

This resource is always present in `resources/list`; `MCPConfig.include_in_schema` does not remove it.

`include_in_schema=False` is the default. It hides the plugin-owned `/mcp` path and both `/.well-known/*` discovery paths from generated OpenAPI, while ordinary application routes—including routes marked for MCP—keep their own OpenAPI visibility.

Set `include_in_schema=True` to include all plugin-owned paths in OpenAPI:

- `/mcp`
- `/.well-known/oauth-protected-resource`
- `/.well-known/agent-card.json`

### Auth

Authentication is a Litestar middleware concern. Apps with existing auth middleware get `request.user` / `request.auth` before tool handlers run.

The supported auth paths are:

- Bring your own Litestar auth middleware; MCP routes inherit it.
- Use `MCPAuthBackend` with `OIDCProviderConfig`.
- Build a validator with `create_oidc_validator()` and pass shared JWKS behavior through `JWKSCache` when your app manages discovery/cache lifetimes.

For OIDC-backed MCP endpoints, pair `MCPAuthConfig` metadata with token validation:

```python
from litestar import Litestar
from litestar.middleware import DefineMiddleware
from litestar_mcp import LitestarMCP, MCPAuthBackend, MCPConfig, OIDCProviderConfig
from litestar_mcp.auth import MCPAuthConfig

app = Litestar(
    route_handlers=[],
    plugins=[
        LitestarMCP(
            MCPConfig(
                auth=MCPAuthConfig(
                    issuer="https://company.okta.com",
                    audience="api://mcp-tools",
                )
            )
        )
    ],
    middleware=[
        DefineMiddleware(
            MCPAuthBackend,
            providers=[
                OIDCProviderConfig(
                    issuer="https://company.okta.com",
                    audience="api://mcp-tools",
                )
            ],
            user_resolver=lambda claims, app: claims.get("sub"),
        )
    ],
)
```

For an identity proxy that supplies a raw token in a custom header, configure the backend explicitly:

```python
from litestar.middleware import DefineMiddleware
from litestar_mcp import MCPAuthBackend, OIDCProviderConfig

DefineMiddleware(
    MCPAuthBackend,
    providers=[
        OIDCProviderConfig(
            issuer="https://cloud.google.com/iap",
            audience="/projects/123/global/backendServices/456",
        )
    ],
    header_name="X-Goog-IAP-JWT-Assertion",
    token_prefix="",
)
```

`header_name` is case-insensitive when read. `token_prefix=""` validates the entire non-empty header value; a non-empty prefix must match exactly and is stripped before validation. Match the bridge’s `--header-name` and `--token-prefix` when connecting through the same proxy.

<workflow>

## Workflow

### Step 1: Install

```bash
pip install litestar-mcp
```

### Step 2: Decide What to Expose

List only the routes that should be callable by AI clients. Mark those routes with `mcp_tool=`, `mcp_resource=`, or `mcp_prompt=` (add `mcp_resource_template=` next to `mcp_resource=` for templated resources). Unmarked routes are never exposed.

### Step 3: Add the Plugin

Wire `LitestarMCP(MCPConfig(name=...))` into `Litestar(plugins=[...])`, or use standalone `MCP(...)` when the app exists only to serve MCP primitives. Use `include_tags` or `include_operations` when you need a second allowlist.

### Step 4: Add Auth

For public endpoints, configure bearer-token validation and `MCPAuthConfig` metadata. For internal deployments, use `guards=[...]`, `route_opt={...}`, or existing app auth middleware.

### Step 5: Verify

`POST /mcp` each JSON-RPC request directly — `server/discover` for capabilities, then `tools/list`, `resources/list`, `tools/call`, and `resources/read`. Confirm only marked routes appear, call one representative tool, and read one representative resource. Verify both `text` and `blob` resource paths when exposing binary data. For standalone stdio apps, send one line-delimited JSON-RPC request through stdin and confirm the response is written to stdout. For bridge deployments, verify stdout purity, concurrent request streams, and auth refresh paths.

</workflow>

<guardrails>

## Guardrails

- **Mark routes explicitly** - unmarked routes should not appear in MCP clients.
- **Default to allowlists** - `include_tags` / `include_operations` keep the tool set small and gate direct invocation; pair them with `guards` / auth for authorization.
- **Never expose admin or destructive routes by default** - require a human-confirmation workflow or multi-round-trip verification (`MCPInputRequiredResult`) before any irreversible operation.
- **Prefer resources for read-only reference data** - agents may read resources speculatively.
- **Keep DTOs precise** - loose `dict[str, Any]` request schemas produce weak tool contracts.
- **Use `MCPAuthConfig` plus token validation for public MCP** - metadata alone does not authenticate requests.
- **Set `allowed_origins` for browser-accessible MCP clients** - leave it `None` only for trusted server-to-server deployments.
- **Prefer `MCPResourceLink` over inline blobs** - linked resources avoid base64 expansion and let the application enforce authorization when the client reads the resource.
- **Keep `max_blob_bytes` bounded** - base64 embedding increases memory and wire size; disable the cap only behind a stricter application-owned limit.
- **Resolve stdio credentials out of band** - inject the verified principal with `MCPStdioContext`; JSON-RPC messages are not an authentication channel.
- **Treat `MCP` and `LitestarMCP` as public entry points** - avoid private router/service imports.
- **Keep observability callbacks side-effect safe** - `before_tool_call` / `after_tool_call` failures are swallowed, so callbacks must not enforce authorization or business invariants.

</guardrails>

<validation>

### Validation Checkpoint

Before delivering an MCP integration, verify:

- [ ] Existing Litestar apps include `LitestarMCP` in `app.plugins`; standalone apps expose `app = mcp.app`
- [ ] Exposed routes/functions use `mcp_tool=`, `mcp_resource=`, `mcp_prompt=`, `@mcp.tool`, `@mcp.resource`, or `@mcp.prompt`
- [ ] Admin / internal routes are left unmarked, or kept outside `include_*` / inside `exclude_*` — with `guards` or auth enforcing access
- [ ] Auth is configured for the deployment boundary (`MCPAuthBackend`, `MCPAuthConfig`, or custom middleware)
- [ ] `POST /mcp` `tools/list` returns only intended tools
- [ ] `POST /mcp` `resources/list` includes only intended resources plus `litestar://openapi`
- [ ] Filtered tools/resources/templates fail direct invocation as unknown
- [ ] Provider-declared user inputs appear in tool `inputSchema`; Dishka-resolved service parameters do not
- [ ] `before_tool_call` / `after_tool_call` callbacks are covered when configured, including failure paths
- [ ] Standalone `MCP` SSE or stdio transport is smoke-tested for the chosen deployment mode
- [ ] Direct stdio handlers and guards receive the intended `MCPStdioContext`; task ownership resolves to the intended principal
- [ ] Stdio bridge stdout contains JSON-RPC only; static/dynamic auth, concurrent request-scoped streams, and frame limits match the deployment
- [ ] Binary resource listings advertise the correct MIME type; reads return `text` or base64 `blob` as intended
- [ ] `max_blob_bytes` accepts the largest intended payload and rejects oversized tool results and resource reads
- [ ] OpenAPI contains ordinary application routes and hides plugin-owned paths by default; `include_in_schema=True` exposes all three plugin-owned paths when requested
- [ ] Exposed handlers performing I/O are `async def`; sync standalone functions are pure/non-blocking and return JSON-serializable types
- [ ] Tool argument DTOs are specific enough for generated schemas

</validation>

<example>

## Example

**Task:** Expose product listing as a resource and add-to-cart as a tool. Hide internal metrics.

```python
from litestar import Litestar, get, post
from litestar_mcp import LitestarMCP, MCPConfig


@get("/products", mcp_resource="product_list", tags=["public"])
async def list_products() -> list[dict[str, str]]:
    """List public catalog products."""
    return [{"id": "prod-1", "name": "Widget"}]


@post("/cart/items", mcp_tool="add_to_cart", tags=["public"])
async def add_to_cart(data: dict[str, int]) -> dict[str, str]:
    """Add product to user shopping cart."""
    return {"status": "success"}


@get("/internal/metrics")
async def metrics() -> dict[str, int]:
    """Internal metrics endpoint."""
    return {"cpu_percent": 12}


app = Litestar(
    route_handlers=[list_products, add_to_cart, metrics],
    plugins=[
        LitestarMCP(
            MCPConfig(
                name="E-Commerce API",
                include_tags=["public"],
            )
        )
    ],
)
```

</example>

## References Index

- **[Stateless Protocol](references/stateless-protocol.md)** — the POST-only transport, `server/discover`, `subscriptions/listen`, the tasks extension, MRTR results, response caching, and client migration.

## Cross-References

- Use this skill for route marking, transport and stdio behavior, binary content, MCP auth metadata, and verification requests.
- Use [litestar-auth-guards](../litestar-auth-guards/SKILL.md) when auth logic lives in normal Litestar guards or middleware.

## Official References

- <https://github.com/cofin/litestar-mcp/tree/v0.13.0> — audited v0.13.0 source and tests
- <https://cofin.github.io/litestar-mcp/>
- <https://github.com/cofin/litestar-mcp>
- <https://modelcontextprotocol.io/>
- <https://spec.modelcontextprotocol.io/>

## Shared Styleguide Baseline

- [General Principles](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
