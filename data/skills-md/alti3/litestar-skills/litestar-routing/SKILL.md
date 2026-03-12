---
name: litestar-routing
description: Design and implement Litestar routing with app/router/controller composition, handler decorators, path and parameter modeling, route indexing/reverse lookups, ASGI mounting, and layered route metadata. Use when creating or refactoring endpoint topology and URL contracts. Do not use for purely internal service logic unrelated to HTTP route structure.
---

# Routing

Use this skill when API path design, handler registration, route composition, and parameter behavior are core to the task.

## Execution Workflow

1. Define endpoint contracts with semantic handler decorators and strict type annotations.
2. Choose composition model:
3. Register simple handlers directly on app.
4. Use routers for path grouping and nested route trees.
5. Use controllers for OOP-style endpoint grouping under a shared controller path.
6. Choose parameter sources and constraints (path/query/header/cookie/layered parameters).
7. Apply route metadata and indexing (`name`, `opt`) for discoverability and policy hooks.
8. Validate reverse-routing, unique path+method combinations, and layered precedence behavior.

## Implementation Rules

- Keep URL design stable, resource-oriented, and version-aware.
- Keep handlers thin; delegate business logic to services.
- Prefer semantic decorators (`@get`, `@post`, etc.) over `@route()` for clearer OpenAPI operations.
- Use explicit path converters and narrow parameter types.
- Treat dynamic registration as an exception path; avoid it for routine topology.
- Apply metadata and guards at the narrowest effective scope.
- Keep type annotations complete for all handler params and return values.

## Routing Topology: App, Router, Controller

### App-level registration

- `Litestar(route_handlers=[...])` is the root registration point.
- Registered components are appended to root path `/`.
- A handler can be attached to multiple paths by passing a list of paths to the decorator.

### Dynamic registration

- Use `app.register(handler)` when runtime registration is genuinely required.
- App instance is available from connection objects (`Request`, `WebSocket`, `ASGIConnection`), so dynamic registration can be called from handlers/middleware/dependencies.
- Dynamic registration should be used sparingly because it increases operational complexity.

### Routers

- `Router` can register controllers, handlers, and nested routers.
- Nested routers compose their paths; registering router A on router B appends A’s path under B’s path.

### Controllers

- Controllers are `Controller` subclasses with a class-level `path`.
- Controller path prefixes each route handler method path.
- If `path` is omitted, it defaults to `/`.
- Path + HTTP method combinations must remain unique per effective routing tree.

## Registering Components Multiple Times

- Controllers can be registered multiple times across different routers; each router creates its own controller instance.
- Standalone handlers can also be registered multiple times; Litestar copies handlers per registration context.
- Routers can be nested, but once a router is registered it cannot be re-registered.

## Route Handlers

### Core behaviors

- Handlers are built with Litestar decorators on functions or controller methods.
- Both sync and async callables are supported.
- For sync handlers:
- `sync_to_thread=True` runs in threadpool (safe for blocking code).
- `sync_to_thread=False` signals non-blocking sync behavior.
- Leaving sync behavior implicit can emit warnings.

### Declaring paths

- Path can be positional (`@get("/x")`) or keyword (`@get(path="/x")`).
- Path can be a list for multi-path registration and optional path-parameter patterns.

### Type annotation requirements

- All handler arguments and return values must be typed.
- Missing annotations raise `ImproperlyConfiguredException` during app startup.

### Reserved kwargs injection

Reserved names include:

- `cookies`, `headers`, `query`
- `request` (HTTP handlers)
- `socket` (WebSocket handlers)
- `scope`, `state`, `body` (body for HTTP handlers)

If collisions occur, use alternative parameter naming patterns.

### HTTP handlers

- `@route()` maps to `HTTPRouteHandler` but is generally discouraged for normal CRUD-style APIs.
- Prefer semantic decorators:
- `@get`, `@post`, `@put`, `@patch`, `@delete`, `@head`

### WebSocket handlers

- `@websocket()` supports low-level socket handling directly.
- For higher-level real-time patterns, use dedicated WebSocket architecture patterns (see cross-skill handoff).

### ASGI handlers

- `@asgi()` / `ASGIRouteHandler` supports custom ASGI apps.
- ASGI handler signature is constrained to `scope`, `receive`, `send`.
- ASGI handlers must be async.

## Mounting ASGI Apps

- Use `@asgi(..., is_mount=True)` to mount sub-app behavior on a path prefix.
- Mounted handlers receive all traffic under that prefix.
- With `copy_scope=True`, forwarded `scope["path"]` is rewritten relative to mount root.
- This is useful for integrating third-party ASGI apps.

## Route Indexing and Reverse Routing

- Set explicit unique `name` on handlers for stable lookup.
- Name uniqueness is required; duplicates raise `ImproperlyConfiguredException`.
- `route_reverse(name, **params)` can build a path.
- `request.url_for(name, **params)` builds absolute URLs.
- Avoid reverse lookups on handlers with multiple ambiguous matching paths; result selection can be unpredictable.

## Arbitrary Route Metadata with `opt`

- All route decorators accept `opt={...}` metadata.
- Arbitrary kwargs on route decorators are merged into `opt`.
- `opt` is available to guards, request route handler context, and ASGI scope.
- `opt` is layered (app/router/controller/handler) and merged by precedence.
- Closest layer to the handler wins on key conflicts.

## Signature Namespace Resolution

- Litestar builds runtime signature models for handlers/dependencies.
- If types are only imported under `TYPE_CHECKING`, resolve them via:
- `signature_types=[...]` on app/router/controller/handler layer as needed.
- `signature_namespace={...}` when alias names differ from runtime type `__name__`.

Default signature namespace includes:

- `Headers`, `ImmutableState`, `Receive`, `Request`, `Scope`, `Send`, `State`, `WebSocket`, `WebSocketScope`

## Parameters: Path, Query, Header, Cookie, Layered

### Path parameters

- Declared in route path as `{name:type}`, for example `{user_id:int}`.
- Supported path converter types include:
- `date`, `datetime`, `decimal`, `float`, `int`, `path`, `str`, `time`.
- Path-converter type and function annotation do not have to match 1:1 if coercion is valid.
- Path params can exist in path without being declared in the function signature; they still validate and document.

### `Parameter()` helper

- Use `Parameter(...)` with `Annotated[...]` for extra validation and OpenAPI metadata.
- Supports constraints and docs attributes (for example `gt`, `lt`, titles/descriptions/examples).

### Query parameters

- Any non-path function kwarg is treated as query param by default.
- Query parameters are required by default.
- Defaults produce optional-like behavior at runtime for omitted values.
- Optional annotations (`str | None` / `Optional[str]`) express nullable query params.
- Query values are coercible into richer types (for example datetime, numbers, lists).

### Alternative names and constraints

- Remap URL query names via `Parameter(query="externalName")`.
- Apply validation constraints via `Parameter(...)`, for example numeric bounds.

### Enum query parameter docs

- Enum docstrings feed schema descriptions by default.
- Use `schema_component_key` when same enum needs different parameter descriptions across endpoints.

### Header and cookie parameters

- Must be declared with `Parameter(header="...")` or `Parameter(cookie="...")`.
- Behavior otherwise follows query-parameter parsing/validation model.

### Layered parameters

- Parameters can be declared at app/router/controller/handler levels.
- Layered declarations participate in validation and OpenAPI generation.
- Handler-local declarations can further narrow constraints from outer layers.
- Path parameters cannot be declared in non-handler layers.

## Validation Checklist

- Confirm `route_handlers` topology resolves to intended final paths.
- Confirm unique path+method operations and unique handler names.
- Confirm controller and router path composition behaves as intended.
- Confirm sync handlers have explicit `sync_to_thread` decisions.
- Confirm type annotations exist for all handler args and return values.
- Confirm reserved kwargs and injected dependencies do not collide unexpectedly.
- Confirm query/header/cookie/path parameters validate and coerce as expected.
- Confirm layered parameters enforce outer constraints and handler overrides correctly.
- Confirm reverse routing (`route_reverse` / `url_for`) is deterministic for indexed handlers.
- Confirm `opt` metadata merge behavior is correct across layers.
- Confirm mounted ASGI apps receive expected rewritten path semantics.
- Confirm OpenAPI output matches effective paths, params, and operation decomposition.

## Cross-Skill Handoffs

- Use `litestar-requests` and `litestar-responses` for transport contract depth.
- Use `litestar-authentication` and `litestar-dependency-injection` for route-scoped security/services.
- Use `litestar-websockets` for higher-level websocket session architecture.
- Use `litestar-openapi` to verify operation IDs, parameter schemas, and route docs fidelity.

## Litestar References

- https://docs.litestar.dev/latest/usage/routing/index.html
- https://docs.litestar.dev/latest/usage/routing/overview.html
- https://docs.litestar.dev/latest/usage/routing/handlers.html
- https://docs.litestar.dev/latest/usage/routing/parameters.html
