---
name: api-designer
description: >-
  Contract-first API design for REST, GraphQL, gRPC. Design, spec, review,
  version, compat, sdk. Use for API architecture and OpenAPI specs.
  NOT for MCP servers (mcp-creator) or frontend API calls.
argument-hint: "<mode> <input>"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0"
---

# API Designer

Contract-first API design across REST, GraphQL, and gRPC. Produces OpenAPI 3.1 specs, reviews existing APIs, analyzes backward compatibility, and scaffolds client code.

## Canonical Vocabulary

| Term | Definition |
|------|-----------|
| **spec** | An OpenAPI 3.1 document (YAML or JSON) describing an API's surface |
| **endpoint** | A path + method combination in a REST API; a query/mutation in GraphQL; an RPC in gRPC |
| **breaking change** | Any modification that causes existing clients to fail without code changes |
| **non-breaking change** | A backward-compatible modification (additive fields, new endpoints, optional params) |
| **resource** | A domain entity exposed through the API (noun-based URL segment in REST) |
| **contract** | The formal agreement between API producer and consumer defined by the spec |
| **protocol** | The API paradigm: REST, GraphQL, or gRPC |
| **surface** | The complete set of endpoints, types, and operations an API exposes |
| **versioning strategy** | How breaking changes are communicated: URL path, header, or query parameter |

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| `design <requirements>` | Design a new API from requirements |
| `spec <code or path>` | Generate OpenAPI 3.1 spec from existing code |
| `review <spec or path>` | Audit an existing API design |
| `version <spec or path>` | Versioning and deprecation strategy |
| `compat <old> <new>` | Backward compatibility diff analysis |
| `sdk <spec or path>` | Scaffold client code structure |
| Natural language about API design | Auto-detect mode from intent |
| Empty | Show mode menu with examples |

### Mode Menu (empty args)

| # | Mode | Example |
|---|------|---------|
| 1 | Design | `design "User management API with RBAC"` |
| 2 | Spec | `spec src/routes/` |
| 3 | Review | `review openapi.yaml` |
| 4 | Version | `version openapi.yaml` |
| 5 | Compat | `compat v1.yaml v2.yaml` |
| 6 | SDK | `sdk openapi.yaml` |

> Pick a number or describe what you need.

## Protocol Detection

Detect the API protocol from input before entering any mode. Classification determines which conventions and patterns apply.

**Detection signals:**

| Signal | REST | GraphQL | gRPC |
|--------|------|---------|------|
| File extension | `.yaml`, `.json` (OpenAPI) | `.graphql`, `.gql` | `.proto` |
| Keywords | endpoint, resource, CRUD, path | query, mutation, subscription, resolver | service, rpc, message, protobuf |
| URL patterns | `/api/v1/resources` | `/graphql` | gRPC service names |
| Code patterns | Express/FastAPI routes, controllers | Schema definitions, resolvers | Proto service definitions |

**Routing:**
- Clear signal for one protocol: proceed with that protocol's conventions
- Mixed signals or ambiguous: ask user — "Which protocol? [REST / GraphQL / gRPC]"
- No protocol context (pure requirements): default to REST, note assumption

Load `references/rest-conventions.md`, `references/graphql-patterns.md`, or `references/grpc-patterns.md` based on detected protocol.

## Mode A: Design

New API from requirements. Read `references/rest-conventions.md` (or protocol-specific reference).

### Design Steps

1. **Parse requirements** — Extract resources, relationships, operations, auth needs, constraints
2. **Resource modeling** — Define resources with attributes, relationships, cardinality
3. **Endpoint design** — Map CRUD + custom operations to endpoints following protocol conventions
4. **Request/response schemas** — Define payloads with types, validation rules, examples
5. **Auth strategy** — Recommend auth approach (API key, OAuth2, JWT) based on use case
6. **Error contract** — Define error response format with codes, messages, detail objects
7. **Pagination & filtering** — Apply cursor or offset pagination, filter query patterns
8. **Rate limiting** — Recommend limits based on endpoint sensitivity and expected load
9. **Generate spec** — Output complete OpenAPI 3.1 YAML
10. **Validate** — Run `scripts/api-spec-validator.py` on generated spec

## Mode B: Spec

Generate OpenAPI 3.1 from existing code.

### Spec Steps

1. **Scan codebase** — Read route definitions, controllers, handlers, decorators
2. **Extract endpoints** — Map code to path + method + parameters + response types
3. **Infer schemas** — Build request/response schemas from type annotations or runtime types
4. **Generate spec** — Output OpenAPI 3.1 YAML with all discovered endpoints
5. **Validate** — Run `scripts/api-spec-validator.py`
6. **Gap report** — List endpoints missing descriptions, examples, or error responses

## Mode C: Review

Audit existing API design. Read-only analysis.

### Review Steps

1. **Parse spec** — Load and validate the OpenAPI document
2. **Run validator** — `scripts/api-spec-validator.py` for structural issues
3. **Run endpoint matrix** — `scripts/api-endpoint-matrix.py` for surface overview
4. **Convention check** — Verify naming, HTTP method usage, status codes against `references/rest-conventions.md`
5. **Security audit** — Check auth coverage, HTTPS enforcement, sensitive data exposure
6. **Consistency check** — Verify naming patterns, response envelope consistency, error format uniformity
7. **Report** — Present findings by severity (critical, warning, info) with specific fix recommendations

## Mode D: Version

Versioning and deprecation strategy.

### Version Steps

1. **Analyze current state** — Parse spec, identify version indicators
2. **Recommend strategy** — Compare URL path vs header vs query param versioning (load `references/versioning-strategies.md`)
3. **Deprecation plan** — Timeline, sunset headers, migration guides for deprecated endpoints
4. **Version matrix** — Table showing which endpoints exist in which versions
5. **Migration guide template** — Skeleton for consumer migration documentation

## Mode E: Compat

Backward compatibility diff between two spec versions.

### Compat Steps

1. **Load both specs** — Parse old and new OpenAPI documents
2. **Run compat checker** — `scripts/compat-checker.py <old> <new>`
3. **Classify changes** — Breaking vs non-breaking with change type and location
4. **Impact assessment** — Which consumers are affected, estimated migration effort
5. **Remediation** — For each breaking change, suggest backward-compatible alternatives

## Mode F: SDK

Scaffold client code structure from a spec. NOT a publishable SDK package — a structural starting point.

### SDK Steps

1. **Parse spec** — Extract endpoints, schemas, auth requirements
2. **Group by resource** — Organize endpoints into logical client modules
3. **Generate client skeleton** — Method stubs with typed parameters and return types
4. **Auth integration** — Wire auth mechanism into client constructor
5. **Error handling** — Map API error codes to client exceptions
6. **Usage examples** — One example per resource showing common operations

## Scripts

| Script | Purpose | Run When |
|--------|---------|----------|
| `scripts/api-spec-validator.py` | Validate OpenAPI 3.x for completeness and best practices | Design, Spec, Review |
| `scripts/api-endpoint-matrix.py` | Extract endpoint inventory from spec | Review, Version, SDK |
| `scripts/compat-checker.py` | Compare two specs for breaking changes | Compat |

### Script Invocation

```bash
uv run python skills/api-designer/scripts/api-spec-validator.py <spec-path>
uv run python skills/api-designer/scripts/api-endpoint-matrix.py <spec-path>
uv run python skills/api-designer/scripts/compat-checker.py <old-spec> <new-spec>
```

All scripts output JSON to stdout, warnings to stderr.

## Reference File Index

| File | Content | Read When |
|------|---------|-----------|
| `references/rest-conventions.md` | REST best practices, HTTP methods, status codes, naming, pagination, rate limiting | Design, Spec, Review (REST) |
| `references/graphql-patterns.md` | GraphQL schema design, query patterns, error handling, subscriptions | Design, Spec, Review (GraphQL) |
| `references/grpc-patterns.md` | gRPC service patterns, proto design, streaming, error codes | Design, Spec, Review (gRPC) |
| `references/versioning-strategies.md` | URL vs header vs query versioning, deprecation, backward compat checklist | Version, Compat |
| `data/http-conventions.json` | HTTP method semantics reference data | Scripts |
| `data/status-codes.json` | HTTP status code guide reference data | Scripts |

Do not load all references at once. Load only what the detected protocol and active mode require.

## Critical Rules

1. Always detect protocol before entering any mode — never assume REST without evidence
2. If protocol is ambiguous, ask the user — do not guess
3. Generated specs must pass `api-spec-validator.py` before presenting to user
4. Every endpoint must have at least one error response defined (4xx or 5xx)
5. Never design APIs without pagination for list endpoints returning collections
6. Breaking changes in compat mode must include remediation suggestions
7. SDK mode produces structural scaffolds only — never claim the output is production-ready
8. Use the canonical vocabulary consistently — "spec" not "swagger", "endpoint" not "route"
9. All specs target OpenAPI 3.1 — do not generate Swagger 2.0 or OpenAPI 3.0
10. NOT for MCP servers (use mcp-creator) or frontend API client code

## Scope Boundaries

**IS for:**
- Designing new REST, GraphQL, or gRPC APIs from requirements
- Generating OpenAPI specs from existing code
- Reviewing and auditing API designs
- Versioning strategy and deprecation planning
- Breaking change analysis between spec versions
- Scaffolding client code structure

**NOT for:**
- MCP server APIs (use `/mcp-creator`)
- Frontend API client implementations
- API gateway configuration
- Runtime API testing or load testing
- Database schema design (use `/database-architect`)
