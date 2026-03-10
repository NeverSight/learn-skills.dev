---
name: postman
description: >
  Full API lifecycle management through Postman. Sync OpenAPI specs to collections,
  generate typed client code, run API tests, create mock servers, publish documentation,
  audit security against OWASP Top 10, and discover APIs across workspaces.
  Requires the Postman MCP Server. Use this skill when the user mentions Postman,
  API collections, syncing specs, generating SDKs, running API tests, creating mocks,
  API documentation, or API security audits. Triggers on tasks involving API development
  workflows, collection management, or any Postman-related operations.
metadata:
  author: postman-devrel
  version: "2.0.1"
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - mcp__postman__*
---

# Postman Agent Skill

Full API lifecycle management through the Postman MCP Server. Sync specs, generate code, run tests, create mocks, publish docs, and audit security.

**Version**: 2.0.1
**Requires**: Postman MCP Server

## Prerequisites

This skill requires the Postman MCP Server to be configured. The MCP server exposes 111+ tools for interacting with Postman workspaces, collections, specs, environments, mocks, monitors, and more.

**Setup check**: Call `getAuthenticatedUser` via MCP. If it succeeds, you're connected. If it fails, walk through Setup below.

## Important: MCP Tool Behavior

Before using the workflows below, be aware of these behaviors:

- **`getWorkspaces` returns ALL workspaces.** For large organizations this can be 300KB+. If you already have a workspace ID, use `getWorkspace(workspaceId)` directly instead.
- **`getCollection` default response is a lightweight map** with `itemRefs` (folder/request tree). This is efficient for discovery. Only use `model=full` when you need complete request/response bodies, and be aware it can exceed 300KB for large collections. Prefer targeted `getCollectionRequest` and `getCollectionResponse` calls for specific endpoints.
- **`getTaggedEntities` returns 404 for missing tags**, not an empty array. Handle this gracefully. Tag functionality may require an Enterprise plan.
- **`runCollection` returns aggregate results only** (total requests, passed, failed, duration). It does NOT return per-request detail or error messages. For debugging specific failures, examine individual requests with `getCollectionRequest` and `getCollectionResponse` after the run.
- **`searchPostmanElements` only searches the PUBLIC Postman network**, not private workspaces. Always search private workspace first with `getCollections`.

## Setup

If MCP tools are not available or `getAuthenticatedUser` fails:

1. Get a Postman API key:
   - Go to https://postman.postman.co/settings/me/api-keys
   - Click "Generate API Key", name it "Claude Code"
   - Copy the key (starts with PMAK-)

2. Set the environment variable:
   ```
   export POSTMAN_API_KEY=PMAK-your-key-here
   ```
   Add to `~/.zshrc` or `~/.bashrc` to persist.

3. Verify: Call `getAuthenticatedUser`. On success, call `getWorkspaces` to list workspaces, then `getCollections` with the workspace ID to count resources.

Present:
```
Connected as: <user name>

Your workspaces:
  - My Workspace (personal) - 12 collections, 3 specs
  - Team APIs (team) - 8 collections, 5 specs

You're all set.
```

## Routing

When the user's request involves Postman or APIs, match their intent to the correct workflow below. Always prefer these structured workflows over raw MCP tool calls.

| User Intent | Workflow |
|-------------|----------|
| Import a spec, push spec to Postman, create collection from spec, sync, push changes | **Sync Collections** |
| Generate client code, SDK, wrapper, typed client, consume an API | **Generate Client Code** |
| Find API, search endpoints, what's available, discover APIs | **Discover APIs** |
| Run tests, check if tests pass, validate API, test collection | **Run Collection Tests** |
| Create mock server, fake API, mock for frontend, mock URL | **Create Mock Servers** |
| Generate docs, improve documentation, publish docs, API docs | **API Documentation** |
| Security audit, vulnerabilities, OWASP, security check | **API Security Audit** |
| Is my API agent-ready?, scan my API, analyze spec for AI | Use the **postman-api-readiness** skill |

**Routing rules:**
1. Specific workflows take priority. If intent clearly maps to one, use it.
2. Ambiguous requests: ask the user what they need.
3. Multi-step requests chain workflows. "Import my spec and run tests" = Sync then Test.
4. Only use `mcp__postman__*` tools directly for single targeted updates or when the user explicitly asks.

---

## Workflow: Sync Collections

Keep Postman collections in sync with API code. Create new collections from OpenAPI specs, update existing ones, or push endpoint changes.

### Step 1: Understand What Changed

Detect or ask:
- Is there a local OpenAPI spec? Search for `**/openapi.{json,yaml,yml}`, `**/swagger.{json,yaml,yml}`
- Did the user add/remove/modify endpoints?
- Is there an existing Postman collection to update, or do they need a new one?

### Step 2: Resolve Workspace

If the user provides a workspace ID, call `getWorkspace(workspaceId)` directly. Otherwise, call `getCollections` with a workspace ID if known, or ask the user which workspace to use. Avoid calling `getWorkspaces` (no filter) on large org accounts as it returns all workspaces (300KB+).

### Step 3: Find or Create the Collection

**Updating an existing collection:**
1. Call `getCollections` with the `workspace` parameter
2. Match by name or ask which collection
3. Call `getCollection` to get current state

**Creating from a spec:**
1. Read the local OpenAPI spec
2. Call `createSpec` with `workspaceId`, `name`, `type` (one of `OPENAPI:2.0`, `OPENAPI:3.0`, `OPENAPI:3.1`, `ASYNCAPI:2.0`), and `files` (array of `{path, content}`)
3. Call `generateCollection` from the spec. **This is async (HTTP 202).** Poll `getGeneratedCollectionSpecs` or `getSpecCollections` until complete.
4. Call `createEnvironment` with variables from the spec:
   - `base_url` from `servers[0].url`
   - Auth variables from `securitySchemes` (mark as `secret`)
   - Common path parameters

### Step 4: Sync

**Spec to Collection (most common):**
1. Call `createSpec` or `updateSpecFile` with local spec content
2. Call `syncCollectionWithSpec` to update the collection. **Async (HTTP 202).** Poll `getCollectionUpdatesTasks` for completion.
3. Note: `syncCollectionWithSpec` only supports OpenAPI 3.0. For Swagger 2.0 or OpenAPI 3.1, use `updateSpecFile` and regenerate via `generateCollection`.
4. Report what changed

**Collection to Spec (reverse sync):**
1. Call `syncSpecWithCollection` to update the spec from collection changes
2. Write the updated spec back to the local file

**Manual updates (no spec):**
1. `createCollectionRequest` to add new endpoints
2. `updateCollectionRequest` to modify existing ones
3. `createCollectionFolder` to organize by resource
4. `createCollectionResponse` to add example responses

### Step 5: Confirm

```
Collection synced: "Pet Store API" (15 requests)
  Added:    POST /pets/{id}/vaccinations
  Updated:  GET /pets - added 'breed' filter parameter
  Removed:  (none)

  Environment: "Pet Store - Development" updated
  Spec Hub: petstore-v3.1.0 pushed
```

---

## Workflow: Generate Client Code

Generate typed client code from Postman collections. Reads private API definitions and writes production-ready code matching the project's conventions.

### Step 1: Find the API

1. If workspace ID is known, call `getWorkspace(workspaceId)` to get the full inventory (collections, specs, environments) in one call. Otherwise ask the user which workspace.
2. Call `getCollections` with `workspace` parameter. Use `name` filter if specified.
3. If no results in private workspace, fall back to `searchPostmanElements` (public network only)
4. Call `getCollection` for the lightweight map (default, no `model` param)
5. Call `getSpecDefinition` if a linked spec exists (richer type info)

### Step 2: Understand the API Shape

For each relevant endpoint:
1. Call `getCollectionFolder` for resource grouping
2. Call `getCollectionRequest` for method, URL, headers, auth, body schema, parameters
3. Call `getCollectionResponse` for status codes, response shapes, error formats
4. Call `getEnvironment` for base URLs and variables
5. Call `getCodeGenerationInstructions` for Postman-specific codegen guidance

### Step 3: Detect Project Language

If not specified, detect from the project:
- `package.json` or `tsconfig.json` -> TypeScript/JavaScript
- `requirements.txt` or `pyproject.toml` -> Python
- `go.mod` -> Go
- `Cargo.toml` -> Rust
- `pom.xml` or `build.gradle` -> Java
- `Gemfile` -> Ruby

### Step 3b: Check for Variable Mismatches

Compare collection variables with environment variables. Common issue: collection uses `{{baseUrl}}` but environment defines `base_url` (or vice versa). Flag any naming mismatches to the user before generating code, as these cause silent failures at runtime.

### Step 4: Generate Code

Generate a typed client with:
- Method per endpoint with proper parameters
- Request/response types from collection schemas
- Authentication handling from collection auth config
- Error handling based on documented error responses
- Environment-based configuration (base URL from env vars)
- Pagination support if the API uses it

**Code conventions:**
- Match the project's existing style (imports, formatting, naming)
- Include JSDoc/docstrings from collection descriptions
- Use the project's HTTP library if one exists (axios, fetch, requests, etc.)
- Write to a sensible path (e.g., `src/clients/<api-name>.ts`)

### Step 5: Present

```
Generated: src/clients/users-api.ts

  Endpoints covered:
    GET    /users         -> getUsers(filters)
    POST   /users         -> createUser(data)
    GET    /users/{id}    -> getUser(id)
    PUT    /users/{id}    -> updateUser(id, data)
    DELETE /users/{id}    -> deleteUser(id)

  Types generated: User, CreateUserRequest, UpdateUserRequest, UserListResponse, ApiError
  Auth: Bearer token (from USERS_API_TOKEN env var)
  Base URL: from USERS_API_BASE_URL env var
```

---

## Workflow: Discover APIs

Answer natural language questions about available APIs across Postman workspaces. Find endpoints, check response shapes, understand what's available.

### Step 1: Search

1. If workspace ID is known, call `getWorkspace(workspaceId)` directly. Otherwise ask the user.
2. Call `getCollections` with `workspace` parameter. Use `name` filter to narrow.
3. If sparse, broaden:
   - `searchPostmanElements` as fallback (public network only, not private workspaces)
   - Note: `getTaggedEntities` and `getCollectionTags` may return 404/403 on non-Enterprise plans. Do not rely on these for discovery.

### Step 2: Drill Into Results

For each relevant hit:
1. `getCollection` for overview (default returns lightweight map with `itemRefs`, not full payloads)
2. Scan endpoint names from the map to identify relevant folders/requests
3. `getCollectionRequest` for specific relevant endpoints (targeted, not bulk)
4. `getCollectionResponse` for specific response data
5. `getSpecDefinition` if linked spec exists

### Step 3: Present

**Found:**
```
Yes, you can get a user's email via the API.

  Endpoint: GET /users/{id}
  Collection: "User Management API"
  Auth: Bearer token required

  Response includes:
    { "id": "usr_123", "email": "jane@example.com", "name": "Jane Smith" }

  Want me to generate a client for this API?
```

**Not found:** Show closest matches and explain why they don't match.

**Multiple results:** List collections with endpoint counts, ask which to explore.

---

## Workflow: Run Collection Tests

Execute Postman collection tests, analyze results, diagnose failures, and suggest fixes.

### Step 1: Find the Collection

1. If workspace ID is known, call `getWorkspace(workspaceId)` directly. Otherwise ask the user.
2. Call `getCollections` with `workspace` parameter. Use `name` filter if specified.

### Step 2: Run Tests

Call `runCollection` with the collection UID in `OWNER_ID-UUID` format (from `getCollection` response's `uid` field).

If environment variables are needed:
1. Call `getEnvironments` to list available environments
2. Ask which to use or detect from naming convention
3. Pass the environment ID to `runCollection`

### Step 3: Parse Results

**Note:** `runCollection` returns aggregate results only (total requests, passed/failed counts, duration). It does NOT include per-request detail. Present what's available:

```
Test Results: Pet Store API
  Requests:  15 executed
  Failed:    3
  Assertions: 24 total, 21 passed
  Duration:  12.4s
```

If tests failed and per-request detail is needed, examine the collection's test scripts and request definitions with `getCollectionRequest` to help diagnose. The user may also need to check the Postman app or a monitor run for detailed failure logs.

### Step 4: Diagnose Failures

For each failure:
1. `getCollectionRequest` for full request definition
2. `getCollectionResponse` for expected responses
3. Check if API source code is in the current project
4. Explain expected vs actual
5. If code is local, find the handler and suggest the fix

### Step 5: Fix and Re-run

After fixing: offer to re-run and show before/after comparison.

### Step 6: Update Collection (if needed)

If the tests themselves need updating:
- `updateCollectionRequest` to fix request bodies, headers, or test scripts
- `updateCollectionResponse` to update expected responses

---

## Workflow: Create Mock Servers

Spin up a Postman mock server from a collection or spec. Get a working mock URL for frontend development, integration testing, or demos.

### Step 1: Find the Source

If workspace ID is known, call `getWorkspace(workspaceId)` directly. Otherwise ask the user.

**From existing collection:** `getCollections` with workspace ID -> select target collection

**From local spec:** Import first:
1. `createSpec` with workspace, name, type, files
2. `generateCollection`. **Async (HTTP 202).** Poll `getGeneratedCollectionSpecs` or `getSpecCollections` for completion.

### Step 2: Check for Examples

Mock servers serve example responses. Call `getCollection` and check if requests have saved responses.

If missing, generate realistic examples:
1. `getCollectionRequest` for each request's schema
2. Generate realistic example response from the schema
3. `createCollectionResponse` to save the example

### Step 3: Check for Existing Mocks

Call `getMocks` to check if one already exists for this collection. If found, present its URL. Only create new if none exists or explicitly requested.

### Step 4: Create Mock Server

Call `createMock` with:
- Workspace ID
- Collection UID in `ownerId-collectionId` format (from `getCollection` response's `uid` field)
- Environment ID (if applicable)
- Name: `<api-name> Mock`
- Private: false (or true if preferred)

### Step 5: Present

```
Mock server created: "Pet Store API Mock"
  URL: https://<mock-id>.mock.pstmn.io
  Status: Active

  Try it:
    curl https://<mock-id>.mock.pstmn.io/pets
    curl https://<mock-id>.mock.pstmn.io/pets/1
    curl -X POST https://<mock-id>.mock.pstmn.io/pets -d '{"name":"Buddy"}'

  The mock serves example responses from your collection.
  Update examples in Postman to change mock behavior.
```

### Step 6: Integration

```
Quick integration:
  # Add to your project .env
  API_BASE_URL=https://<mock-id>.mock.pstmn.io

  # Or in your frontend config
  const API_URL = process.env.API_BASE_URL || 'https://<mock-id>.mock.pstmn.io';
```

### Step 7: Publish (optional)

If the user wants public access:
- `publishMock` for unauthenticated access (demos, hackathons, public docs)
- `unpublishMock` to make private again

---

## Workflow: API Documentation

Analyze, improve, and publish API documentation from OpenAPI specs and Postman collections.

### Step 1: Find the Source

Check for API definitions in order:

**Local specs:** Search for `**/openapi.{json,yaml,yml}`, `**/swagger.{json,yaml,yml}`

**Postman specs:** `getAllSpecs` with workspace ID, then `getSpecDefinition` for full spec

**Postman collections:** `getCollections` then `getCollection` for full detail

### Step 2: Analyze Completeness

```
Documentation Coverage: 60%
  Endpoints with descriptions:     8/15
  Parameters with descriptions:    22/45
  Endpoints with examples:         3/15
  Error responses documented:      2/15
  Authentication documented:       Yes
  Rate limits documented:          No
```

### Step 3: Generate or Improve

**Sparse spec:** Generate documentation for each endpoint (summaries, parameter tables, request/response schemas, examples, error docs, auth requirements).

**Partial spec:** Fill gaps (add missing descriptions inferred from naming/schemas, generate realistic examples, add error responses, document auth and rate limits).

### Step 4: Apply Changes

Ask the user which output:
1. **Update the spec file** - Write improved docs back into OpenAPI spec
2. **Update in Postman** - `updateCollectionRequest` to add descriptions and examples
3. **Publish public docs** - `publishDocumentation` with collection ID, returns public URL. `unpublishDocumentation` to take down.
4. **Generate markdown** - Create `docs/api-reference.md` for the project

### Step 5: Sync

If both spec and collection exist, keep in sync:
- `syncCollectionWithSpec` to update collection from spec (async, OpenAPI 3.0 only)
- `syncSpecWithCollection` to update spec from collection changes

---

## Workflow: API Security Audit

Audit APIs for security issues against OWASP API Security Top 10. Works with local OpenAPI specs and Postman collections.

### Step 1: Find the Source

**Local spec:** Search for OpenAPI/Swagger files in the project

**Postman spec:** `getAllSpecs` then `getSpecDefinition`

**Postman collection:** `getCollections` then `getCollection` including auth config. Also `getEnvironment` to check for exposed secrets.

### Step 2: Run Security Checks

**Authentication and Authorization:**
- Security schemes defined (OAuth2, API Key, Bearer, etc.)
- Security applied globally or per-endpoint
- No accidentally unprotected endpoints
- OAuth2 scopes defined and appropriate
- Admin endpoints have elevated auth

**Transport Security:**
- All server URLs use HTTPS
- No mixed HTTP/HTTPS

**Sensitive Data Exposure:**
- No API keys, tokens, or passwords in example values
- No secrets in query parameters (should be headers/body)
- Password fields marked as `format: password`
- PII fields identified
- Postman environment variables checked for leaked secrets (via `getEnvironment`)

**Input Validation:**
- All parameters have defined types
- String parameters have `maxLength`
- Numeric parameters have `minimum`/`maximum`
- Array parameters have `maxItems`
- Enum values used where applicable
- Request body has required field validation

**Rate Limiting:**
- Rate limits documented
- Rate limit headers defined (X-RateLimit-Limit, X-RateLimit-Remaining)
- 429 response defined

**Error Handling:**
- Error responses don't leak stack traces
- Error schemas don't expose internal field names
- 401 and 403 responses properly defined

**OWASP API Top 10:**
- API1: Broken Object Level Authorization
- API2: Broken Authentication
- API3: Broken Object Property Level Authorization
- API4: Unrestricted Resource Consumption
- API5: Broken Function Level Authorization
- API6: Unrestricted Access to Sensitive Business Flows
- API7: Server Side Request Forgery
- API8: Security Misconfiguration
- API9: Improper Inventory Management
- API10: Unsafe Consumption of APIs

### Step 3: Present Results

```
API Security Audit: pet-store-api.yaml

  CRITICAL (2):
    SEC-001: 3 endpoints have no security scheme applied
      - GET /admin/users
      - DELETE /admin/users/{id}
      - PUT /admin/config
    SEC-002: Server URL uses HTTP (http://api.example.com)

  HIGH (3):
    SEC-003: No rate limiting documentation or 429 response
    SEC-004: API key sent as query parameter (use header instead)
    SEC-005: No maxLength on 8 string inputs (injection risk)

  MEDIUM (2):
    SEC-006: Password field visible in GET /users/{id} response
    SEC-007: Environment variable 'db_password' not marked secret

  Score: 48/100 - Significant Issues
```

### Step 4: Fix

For each finding:
1. Explain the security risk in plain terms
2. Show the exact spec change needed
3. Apply the fix with user approval

For Postman-specific issues:
- `putEnvironment` to mark secrets properly
- `updateCollectionRequest` to fix auth configuration
- `updateCollectionResponse` to remove sensitive data from examples

### Step 5: Re-audit

After fixes, re-run to show improvement.

---

## Error Handling

These patterns apply across all workflows:

| Error | Response |
|-------|----------|
| MCP tools not available | "The Postman MCP Server isn't configured. Set your POSTMAN_API_KEY environment variable and restart your editor." |
| 401 Unauthorized | "Your Postman API key was rejected. Generate a new one at https://postman.postman.co/settings/me/api-keys" |
| Network timeout | Retry once. Check https://status.postman.com for outages. |
| Async operation stuck | If polling shows no progress after 30 seconds, inform user and suggest checking Postman app directly. |
| Collection not found | "No collection matching that name. Try discovering APIs across your workspace." |
| Empty collection | "This collection has no requests. Add endpoints in Postman or sync from a local spec." |
| Invalid spec | Report specific parse errors with line numbers. Offer to fix common YAML/JSON syntax issues. |
| Plan limitations | "Some features may require a paid Postman plan. Core operations work on all plans." |

## MCP Tool Reference

See `references/mcp-tools.md` for the complete tool catalog and `references/mcp-limitations.md` for known limitations and workarounds.
