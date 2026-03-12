---
name: litestar-databases
description: Build Litestar database architecture with SQLAlchemy and Piccolo ORM, including model/repository patterns, SQLAlchemy plugin selection, session lifecycle, transaction boundaries, and DTO/serialization controls. Use when implementing persistence layers, transaction handling, or ORM integration. Do not use for non-persistent in-memory workflows.
---

# Databases

Use this skill when persistence architecture and ORM integration are core to the task, especially SQLAlchemy plugin wiring or Piccolo DTO-based API flows.

## Execution Workflow

1. Choose ORM path (`SQLAlchemy` or `Piccolo`) based on ecosystem and project constraints.
2. For SQLAlchemy, choose plugin strategy first (`SQLAlchemyPlugin` vs `SQLAlchemyInitPlugin` + optional `SQLAlchemySerializationPlugin`).
3. Configure engine + session factory centrally at app initialization (async or sync).
4. Define model/repository/service boundaries and keep transaction ownership explicit.
5. Integrate dependency injection so handlers receive a scoped session/unit-of-work.
6. Define DTO and serialization boundaries at API edges (never leak raw ORM internals unintentionally).
7. Validate lifecycle behavior: startup initialization, request cleanup/rollback, and lazy-loading behavior in hot paths.

## Implementation Rules

- Keep transactions explicit and short-lived; commit where business operations complete, rollback on failure paths.
- Keep repositories/services free of HTTP transport concerns.
- Keep session ownership deterministic; handlers should not guess who closes/rolls back a session.
- Prefer async SQLAlchemy for IO-heavy API workloads unless sync architecture is a deliberate requirement.
- Avoid returning ORM entities blindly when relationships/lazy attributes can trigger unexpected DB access.
- Use DTO shaping for both inbound and outbound payloads to protect private/internal fields.

## SQLAlchemy: Decision Guide

- Use `SQLAlchemyPlugin` for most applications that need both app/session tooling and SQLAlchemy model serialization support.
- Use `SQLAlchemyInitPlugin` only when you need engine/session injection and lifecycle management but do not want automatic SQLAlchemy DTO serialization.
- Add `SQLAlchemySerializationPlugin` when you want automatic SQLAlchemy DTO generation for handler `data` and return annotations.
- Use separate init + serialization plugins when you need explicit composition control; otherwise prefer the combined `SQLAlchemyPlugin`.

## SQLAlchemy: Models and Repository Patterns

Litestar SQLAlchemy support includes built-in repository utilities and base model patterns:

- Repository classes:
- `SQLAlchemyAsyncRepository` for async session workflows.
- Generic repository support for CRUD plus filtering, sorting, pagination, and bulk operations.
- Base model options include UUID and BigInt primary-key variants with optional audit columns:
- `UUIDBase`, `UUIDAuditBase`
- `BigIntBase`, `BigIntAuditBase`

Implementation expectations:

- Choose one base strategy early (UUID vs BigInt) and keep it consistent.
- Keep query logic in repositories/services, not route handlers.
- Use repository filtering/pagination primitives in list endpoints rather than ad-hoc SQL in handlers.
- Treat relationship loading strategy as part of API design to avoid N+1 regressions.

## SQLAlchemy: Plugin Configuration Patterns

### Pattern 1: Combined plugin (recommended)

```python
from litestar import Litestar
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyPlugin

config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///app.sqlite",
    create_all=True,
    metadata=Base.metadata,
)
sqlalchemy = SQLAlchemyPlugin(config=config)
app = Litestar(route_handlers=[...], plugins=[sqlalchemy])
```

### Pattern 2: Split init + serialization plugins

```python
from litestar import Litestar
from litestar.plugins.sqlalchemy import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
    SQLAlchemySerializationPlugin,
)

config = SQLAlchemyAsyncConfig(connection_string="sqlite+aiosqlite:///app.sqlite")
app = Litestar(
    route_handlers=[...],
    plugins=[SQLAlchemyInitPlugin(config=config), SQLAlchemySerializationPlugin()],
)
```

### Pattern 3: Sync configuration

```python
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin, SQLAlchemySyncConfig

config = SQLAlchemySyncConfig(connection_string="sqlite:///app.sqlite")
plugin = SQLAlchemyPlugin(config=config)
```

## SQLAlchemy: Dependency Injection and Lifecycle

`SQLAlchemyInitPlugin` provides:

- Engine and session availability via dependency injection.
- Engine and session factory stored on app state.
- A `before_send` handler for request-lifecycle cleanup behavior.
- Signature namespace support for SQLAlchemy-annotated handler dependencies.

Design guidance:

- Inject session dependencies into handlers/services instead of constructing sessions ad hoc.
- Keep one clear per-request unit-of-work path.
- Validate rollback and cleanup behavior during exception paths.

## SQLAlchemy: Serialization and DTO Boundaries

`SQLAlchemySerializationPlugin` automatically creates SQLAlchemy DTO types for handler `data` and return annotations that use SQLAlchemy models (including collections), unless an explicit DTO is already provided.

Practical guidance:

- Use automatic serialization for straightforward CRUD APIs.
- Use explicit DTO classes when fields, nesting, or security requirements need tighter control.
- Mark model fields (for example via DTO field controls) to prevent exposing private data.
- Verify generated OpenAPI schemas and serialized payloads after model changes.

## Piccolo ORM Guidance

Litestar supports Piccolo-centric API flows via `PiccoloDTO`.

Core pattern:

- Define Piccolo `Table` models.
- Use `PiccoloDTO[Model]` for request/response shaping.
- Use custom DTO subclasses with `DTOConfig` for partial updates and field exclusions.

Example:

```python
from litestar.contrib.piccolo import PiccoloDTO
from litestar.dto import DTOConfig

class PatchDTO(PiccoloDTO[Task]):
    config = DTOConfig(exclude={"id"}, partial=True)
```

Piccolo implementation guidance:

- Keep table definitions and DB config centralized.
- Use DTO-level controls for patch semantics and hidden/internal columns.
- Keep query and persistence logic out of transport handlers where possible.

## Validation Checklist

- Confirm selected plugin strategy matches requirements (combined vs split plugins).
- Confirm async/sync config matches deployed runtime and DB driver.
- Confirm migrations/model metadata align with runtime models.
- Confirm session injection works and per-request cleanup runs reliably.
- Confirm rollback behavior on exceptions is tested.
- Confirm DTO boundaries prevent internal/private field leakage.
- Confirm N+1 and lazy-loading pitfalls are addressed in hot paths.
- Confirm list endpoints enforce deterministic filtering/sorting/pagination.

## Cross-Skill Handoffs

- Use `litestar-dependency-injection` for session provisioning patterns.
- Use `litestar-dto` and `litestar-responses` for safe transport shaping.
- Use `litestar-testing` for transactional test isolation.
- Use `litestar-openapi` to verify schema output after DTO/plugin changes.

## Litestar References

- https://docs.litestar.dev/2/usage/databases/sqlalchemy/models_and_repository.html
- https://docs.litestar.dev/2/usage/databases/sqlalchemy/plugins/index.html
- https://docs.litestar.dev/2/usage/databases/sqlalchemy/plugins/sqlalchemy_plugin.html
- https://docs.litestar.dev/2/usage/databases/sqlalchemy/plugins/sqlalchemy_init_plugin.html
- https://docs.litestar.dev/2/usage/databases/sqlalchemy/plugins/sqlalchemy_serialization_plugin.html
- https://docs.litestar.dev/2/usage/databases/piccolo.html
