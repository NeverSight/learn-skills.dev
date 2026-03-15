---
name: mock-loom
description: >-
  Interact with mock-loom Rule-Based API Mocking Engine via MCP tools.
  Set up workspaces, integrations, packs, endpoint contracts and scenarios,
  data sources, send mock requests, and debug entity state with timeline/rollback.
  Use when working with mock-loom, API mocking, API simulation, mock server,
  route import from OpenAPI/Postman/cURL, entity rollback, traffic logs,
  or when the user asks to create, test, inspect, or manage mock endpoints.
allowed-tools:
  - mcp__mock-loom__*
---

# mock-loom MCP

MCP integration for the mock-loom Rule-Based API Mocking Engine.

## Setup

### Dummy Auth (development)

```bash
make run-dummy    # Start API on port 18081 (no credentials needed)
make build-mcp    # Build MCP binary
```

`.mcp.json` at project root configures Claude Code to spawn the MCP server with `MOCK_LOOM_AUTH_TOKEN=dummy-token`.

### OIDC (production)

```bash
make build-mcp                          # Build MCP binary
./apps/mcp/bin/mock-loom-mcp login      # Open browser → OIDC login
./apps/mcp/bin/mock-loom-mcp status     # Verify token is valid
./apps/mcp/bin/mock-loom-mcp logout     # Clear stored tokens
```

Remove `MOCK_LOOM_AUTH_TOKEN` from `.mcp.json` env so the MCP server reads OIDC tokens from `~/.mock-loom/tokens.json` instead. Tokens auto-refresh via refresh token.

## Quick Start Workflow

```
1. mock_loom_list_workspaces          → discover existing workspaces
2. mock_loom_setup_workspace          → create workspace (idempotent by slug)
3. mock_loom_setup_integration        → create integration in workspace
4. mock_loom_manage_pack              → create endpoint pack (route group)
5. mock_loom_import_routes            → import from OpenAPI/Postman/cURL
   OR mock_loom_configure_endpoint    → manually configure contract + scenarios
6. mock_loom_manage_data_source       → create data source + upload baseline JSON
7. mock_loom_send_mock_request        → test the mock endpoint
8. mock_loom_get_traffic              → verify scenario matching
9. mock_loom_debug_entities           → inspect entity mutations
```

## Tool Reference

### Workspace

| Tool | Purpose | Key Args |
|------|---------|----------|
| `mock_loom_list_workspaces` | List all workspaces | — |
| `mock_loom_setup_workspace` | Create/get workspace | `name`, `slug` |

### Integration & Packs

| Tool | Purpose | Key Args |
|------|---------|----------|
| `mock_loom_setup_integration` | Create/get integration | `workspace_id`, `name`, `slug`, `base_url?`, `auth_mode?` |
| `mock_loom_manage_pack` | Create/update pack | `integration_id`, `name`, `slug`, `base_path`, `pack_id?` |
| `mock_loom_import_routes` | Bulk import routes | `integration_id`, `pack_id`, `source_type` (OPENAPI/POSTMAN/CURL), `payload` |
| `mock_loom_list_routes` | List packs/routes | `integration_id`, `pack_id?` |
| `mock_loom_get_overview` | Full integration overview | `integration_id` |

### Endpoints

| Tool | Purpose | Key Args |
|------|---------|----------|
| `mock_loom_configure_endpoint` | Get/update contract + scenarios | `integration_id`, `pack_id`, `endpoint_id`, `contract?`, `scenarios?` |
| `mock_loom_get_traffic` | View traffic logs | `integration_id`, `pack_id`, `endpoint_id` |

### Data Sources & Debugging

| Tool | Purpose | Key Args |
|------|---------|----------|
| `mock_loom_manage_data_source` | CRUD + baseline + schema | `integration_id`, `action`, `source_id?`, `name?`, `slug?`, `kind?`, `baseline_json?` |
| `mock_loom_debug_entities` | List/create/timeline/rollback | `integration_id`, `source_id`, `action`, `entity_id?`, `target_event_id?`, `payload?` |

### Runtime

| Tool | Purpose | Key Args |
|------|---------|----------|
| `mock_loom_send_mock_request` | Execute mock request | `workspace_id`, `integration_id`, `method`, `path`, `headers?`, `query?`, `body?` |

## Contract JSON Shape

The contract defines expected request structure:

```json
{
  "headers": [
    {"name": "X-Api-Key", "required": true, "schema": {"type": "string"}}
  ],
  "queryParams": [
    {"name": "page", "required": false, "schema": {"type": "integer"}}
  ],
  "body": {
    "type": "object",
    "properties": {
      "name": {"type": "string"},
      "email": {"type": "string", "format": "email"}
    },
    "required": ["name"]
  }
}
```

## Scenario JSON Shape

Scenarios are priority-ordered condition→response rules:

```json
[
  {
    "name": "Get user by ID",
    "priority": 1,
    "conditionExpr": "request.params.path.id != ''",
    "response": {
      "statusCode": 200,
      "delayMs": 0,
      "headers": {"Content-Type": "application/json"},
      "body": {"id": "u-1", "name": "John"}
    }
  },
  {
    "name": "Fallback",
    "priority": 99,
    "conditionExpr": "true",
    "response": {
      "statusCode": 404,
      "delayMs": 0,
      "headers": {"Content-Type": "application/json"},
      "body": {"error": "not found"}
    }
  }
]
```

### String response body

`response.body` accepts a JSON object or a string. String bodies are sent as raw bytes — use `response.headers` to set Content-Type:

```json
{
  "name": "HTML response",
  "priority": 10,
  "conditionExpr": "request.body.accion == 'buscarAlumno'",
  "response": {
    "statusCode": 200,
    "delayMs": 0,
    "headers": {"Content-Type": "text/html; charset=utf-8"},
    "body": "<html><body><table><tr><td>26075524</td><td>JUAN PEREZ</td></tr></table></body></html>"
  }
}
```

- JSON object → serialized as JSON, auto Content-Type `application/json`
- String → raw bytes, default Content-Type `text/plain; charset=utf-8` (override via headers)
- null/omitted → no body

## Expression Language (expr-lang)

Scenarios use `expr-lang/expr` for conditions and mutations.

### Available Context Variables

**request** (top-level aliases + params):
- `request.method` — HTTP method
- `request.path` — Full request path
- `request.header.<name>` — Request headers (lowercase keys)
- `request.query.<name>` — Query parameters
- `request.body` — Parsed request body (see below)
- `request.params.path.<name>` — Path parameters (e.g. `{userId}` or `:userId`)
- `request.params.query.<name>` — Query parameters (alias)
- `request.params.headers.<name>` — Headers (alias)
- `request.params.body` — Body (alias)

**source** (data source entities):
- `source.<slug>` — Array of all entities for a data source
- `source.<slug>_by_id` — Map of entities indexed by ID

**auth** (authentication context):
- `auth.token` — Raw auth token
- `auth.email` — Authenticated email
- `auth.claims` — Token claims map
- `auth.headers` — Auth-related headers

### Request Body Parsing

Body parsing depends on `Content-Type`:

| Content-Type | `request.body` type | Example |
|---|---|---|
| `application/json` | Parsed JSON (object, array, etc.) | `request.body.name` |
| `application/x-www-form-urlencoded` | Map of field→string (first value per key) | `request.body.accion` |
| Other / missing | Raw string or JSON attempt | — |

Form-urlencoded example — request body `accion=buscar&txtRun=26075524`:
```
request.body.accion == "buscar" && request.body.txtRun == "26075524"
```

### Common Patterns
```
request.method == 'POST'
request.body.name != ''
request.params.path.id != ''
len(source.users) > 0
source.users_by_id[request.params.path.id] != nil
request.body.accion == "buscarAlumno"
```

## Known API Behaviors

- **Response keys**: Workspace/Integration/Pack creation returns **PascalCase** keys (`ID`, `Name`, `Slug`).
- **Member responses**: Use **snake_case** keys.
- **DELETE/PATCH**: Often return **204 No Content** (no body).
- **Data source PATCH**: Requires both `name` and `slug`.
- **PUT /schema**: Requires ALL fields, not just overrides.
- **Auth modes**: `NONE`, `BEARER`, `API_KEY`.
- **Data source kinds**: `JSON`, `CSV`.
- **Import types**: `OPENAPI`, `POSTMAN`, `CURL`.
