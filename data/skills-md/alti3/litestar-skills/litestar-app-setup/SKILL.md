---
name: litestar-app-setup
description: Build and configure Litestar application entrypoints, app-level configuration, startup/shutdown lifecycle, lifespan context managers, application state, hooks, and layered parameter precedence. Use when creating a new Litestar service, restructuring app initialization, or setting app-level defaults. Do not use for isolated handler logic that belongs in routing, requests, responses, DTO-focused skills, or the in-process event bus handled by `litestar-events`.
---

# App Setup

Use this skill when defining or refactoring the application root object and its global behavior.

## Execution Workflow

1. Define an importable application entrypoint (`app.py`, `application.py`, `main.py`, or factory) for runtime and CLI discovery.
2. Construct `Litestar(...)` with explicit `route_handlers=[...]` (controllers, routers, or handlers); this list is required.
3. Configure app-level concerns intentionally (dependencies, middleware, exception handlers, DTO defaults, request/response classes).
4. Choose lifecycle model:
5. Use `on_startup` / `on_shutdown` for straightforward init/teardown hooks.
6. Use `lifespan=[...]` async context managers for resource lifecycles that require context ownership.
7. Add application hooks (`after_exception`, `before_send`, `on_app_init`) only for cross-cutting concerns.
8. Use application state sparingly, initialize it explicitly, and inject it intentionally where needed.
9. Validate layered overrides to ensure the closest layer to the handler wins as expected.

## Implementation Rules

- Keep the app module focused on composition, not business logic.
- Prefer explicit `route_handlers=[...]` registration and avoid dynamic side effects during import.
- Keep lifecycle ownership deterministic; avoid mixing competing init/teardown patterns without clear intent.
- Keep state minimal and stable; avoid mutable global state unless no cleaner scope exists.
- Use application hooks for instrumentation and cross-cutting behavior, not domain logic.
- Keep `debug=True` local-only and tie runtime behavior to environment settings.

## Application Object Fundamentals

- The root of a Litestar service is a `Litestar` instance.
- The only required constructor argument is `route_handlers`, containing controllers/routers/handlers.
- The application object is the root layer (base path `/`) and owns app-wide defaults.

```python
from litestar import Litestar, get

@get("/")
async def hello() -> dict[str, str]:
    return {"hello": "world"}

app = Litestar(route_handlers=[hello])
```

## Startup and Shutdown Hooks

Use `on_startup=[...]` and `on_shutdown=[...]` for ordered initialization and teardown:

- Hooks can be sync or async callables.
- Startup hooks run on ASGI startup event.
- Shutdown hooks run on ASGI shutdown event.
- A common pattern is creating resources in startup and disposing them in shutdown.

```python
from typing import cast

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from litestar import Litestar

DB_URI = "postgresql+asyncpg://postgres:mysecretpassword@pg.db:5432/db"

def get_db_connection(app: Litestar) -> AsyncEngine:
    if not getattr(app.state, "engine", None):
        app.state.engine = create_async_engine(DB_URI)
    return cast("AsyncEngine", app.state.engine)

async def close_db_connection(app: Litestar) -> None:
    if getattr(app.state, "engine", None):
        await cast("AsyncEngine", app.state.engine).dispose()

app = Litestar(on_startup=[get_db_connection], on_shutdown=[close_db_connection], route_handlers=[...])
```

Boundary note:

- These hooks manage app lifecycle resources.
- They are not Litestar's event bus. Use `litestar-events` when emitting decoupled in-process side effects with `app.emit(...)` and listeners.

## Lifespan Context Managers

Use `lifespan=[async_context_manager, ...]` when resources need a continuous owned context:

```python
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine

from litestar import Litestar

@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    engine = getattr(app.state, "engine", None)
    if engine is None:
        engine = create_async_engine("postgresql+asyncpg://postgres:mysecretpassword@pg.db:5432/db")
        app.state.engine = engine
    try:
        yield
    finally:
        await engine.dispose()

app = Litestar(route_handlers=[...], lifespan=[db_connection])
```

Shutdown ordering rule:

- If multiple lifespan context managers and shutdown hooks are registered, context managers unwind in reverse order before shutdown hooks execute in their declared order.

## Application State

Use state for app-scoped shared context, not as a default data transport mechanism.

Key behaviors:

- App instance is available in ASGI scope as `scope["litestar_app"]`.
- You can access app from scope using `Litestar.from_scope(scope)`.
- `request.app.state` and `socket.app.state` expose state from connection objects.
- `state` is also injectable into handlers and dependencies by using a `state` kwarg.

Initialization options:

- `State({...})` from dict.
- `State(existing_state_or_immutable_state)`.
- `State([(key, value), ...])`.
- `State(..., deep_copy=True)` to protect against external mutation.

Immutability option:

- Use `ImmutableState` typing to enforce no mutation (attribute assignment raises `AttributeError`).

```python
from litestar import Litestar, get
from litestar.datastructures import State

@get("/")
def handler(state: State) -> dict[str, int]:
    return {"count": state.count}

app = Litestar(route_handlers=[handler], state=State({"count": 100}, deep_copy=True))
```

## Application Hooks

### `after_exception`

- Called after an exception with `(exception, scope)`.
- Intended for side effects such as metrics/logging.
- Not an exception handler replacement.

### `before_send`

- Called on each ASGI message with `(message, scope)`.
- Gate logic by `message["type"]` (for example `http.response.start`) when mutating headers or metadata.

```python
from litestar import Litestar, get
from litestar.datastructures import MutableScopeHeaders

@get("/test")
def handler() -> dict[str, str]:
    return {"key": "value"}

async def before_send_hook_handler(message: dict, scope: dict) -> None:
    if message["type"] == "http.response.start":
        headers = MutableScopeHeaders.from_message(message=message)
        headers["My-Header"] = Litestar.from_scope(scope).state.message

def on_startup(app: Litestar) -> None:
    app.state.message = "value injected during send"

app = Litestar(route_handlers=[handler], on_startup=[on_startup], before_send=[before_send_hook_handler])
```

### `on_app_init`

- Intercepts `Litestar` constructor arguments before app instantiation.
- Each hook receives and must return `AppConfig`.
- Useful for reusable configuration packages and third-party app configuration systems.
- `on_app_init` handlers must be synchronous (cannot be coroutine functions) because they run inside `__init__`.

## Layered Architecture and Precedence

Litestar layers:

1. Application
2. Router
3. Controller
4. Handler

Precedence rule:

- For layered parameters, the value set on the layer closest to the handler wins.

Layered parameters documented on the Applications page:

- `after_request`
- `after_response`
- `before_request`
- `cache_control`
- `dependencies`
- `dto`
- `etag`
- `exception_handlers`
- `guards`
- `include_in_schema`
- `middleware`
- `opt`
- `request_class`
- `response_class`
- `response_cookies`
- `response_headers`
- `return_dto`
- `security`
- `tags`
- `type_decoders`
- `type_encoders`
- `websocket_class`

## Validation Checklist

- Confirm CLI autodiscovery works (`litestar run` resolves the correct app).
- Confirm `route_handlers` registration is explicit and import-side-effect free.
- Confirm startup/shutdown hooks run in expected order and release external resources.
- Confirm lifespan context managers dispose resources and unwind correctly.
- Confirm mixed lifespan + shutdown sequences match reverse-context + declared-hook ordering.
- Confirm state initialization uses the intended source and optional `deep_copy` behavior.
- Confirm `state` injection in handlers/dependencies uses the expected state class.
- Confirm `after_exception` is used for side effects only, not exception handling.
- Confirm `before_send` logic is message-type aware and does not mutate unintended messages.
- Confirm `on_app_init` hooks are synchronous and return `AppConfig`.
- Confirm layered overrides behave as expected (closest layer wins) for app/router/controller/handler.

## Cross-Skill Handoffs

- Use `litestar-routing` for endpoint grouping and path design.
- Use `litestar-events` for in-process event-bus listeners and `app.emit(...)`, not startup/shutdown ownership.
- Use `litestar-lifecycle-hooks` for request/response interception and cross-cutting instrumentation.
- Use `litestar-dependency-injection` for dependency scoping across layers.
- Use `litestar-logging`, `litestar-middleware`, and `litestar-openapi` for domain-specific configuration depth.

## Litestar References

- https://docs.litestar.dev/latest/usage/applications.html
- https://docs.litestar.dev/latest/usage/routing/index.html
- https://docs.litestar.dev/latest/usage/events.html
- https://docs.litestar.dev/latest/usage/lifecycle-hooks.html
