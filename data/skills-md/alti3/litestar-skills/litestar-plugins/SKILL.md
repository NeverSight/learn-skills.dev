---
name: litestar-plugins
description: Configure Litestar plugin architecture and ecosystem integrations, including custom Init/DI/serialization/route plugins, SQLAlchemy plugin stacks, Pydantic plugin surfaces, Piccolo DTO usage, and model-bound transport support for dataclasses, msgspec, attrs, and TypedDict. Use when selecting, wiring, or debugging plugin-driven behavior at application boundaries. Do not use for unrelated framework setup that does not involve Litestar plugin protocols, plugin registration, or plugin-backed transport/model integration.
---

# Plugins

Use this skill when a Litestar app needs plugin-driven behavior, or when the task touches one of the model ecosystems that Litestar integrates through plugins, DTO factories, or OpenAPI schema plugins.

## Current Docs Mapping

The links previously listed for this skill are partly stale in the latest Litestar docs. Use the current structure below:

- Core plugin architecture is documented at `usage/plugins/index.html`.
- SQLAlchemy plugin docs moved under `usage/databases/sqlalchemy/plugins/...`.
- Piccolo is documented in latest docs as `PiccoloDTO` usage under `usage/databases/piccolo.html`, not as a separate general plugin page.
- Pydantic and attrs support in latest docs is primarily reference-driven under `reference/plugins/...`.
- Dataclass and msgspec support in latest docs is documented as DTO factories under `reference/dto/...`, not as standalone plugin usage pages.
- Latest docs do not expose a dedicated TypedDict plugin page. Treat TypedDict as a typing/schema concern unless project-local code proves otherwise.

Do not blindly follow old `usage/plugins/*.html` URLs for every ecosystem. Several now return 404 in the latest docs.

## Execution Workflow

1. Start from the desired outcome: app initialization, dependency injection help, automatic DTO generation, ORM session management, or OpenAPI schema support.
2. Decide whether the problem needs a true Litestar plugin protocol implementation or only an ecosystem DTO/OpenAPI integration.
3. Register the minimum plugin set needed in `Litestar(..., plugins=[...])`, and keep ordering explicit.
4. Prefer explicit `dto` / `return_dto` declarations when the public contract matters more than boilerplate reduction.
5. Validate request parsing, response serialization, dependency injection, and generated OpenAPI together.
6. Add focused tests for the exact supported annotation shapes: single model, collection, wrapper, PATCH flow, and dependency injection edge cases.

## Core Plugin Protocols

### `InitPlugin`

Use for application composition and startup-time configuration.

- Implements `on_app_init(self, app_config: AppConfig) -> AppConfig`.
- Runs after application `on_app_init` hooks.
- Runs in the same order as the `plugins=[...]` list.
- Appropriate for injecting dependencies, registering route handlers, middleware, exception handlers, or app-wide config.

Use this when the plugin changes application structure.

### `SerializationPluginProtocol`

Use when Litestar should auto-create DTOs for supported handler annotations.

- Implement `supports_type(field_definition) -> bool`.
- Implement `create_dto_for_type(field_definition) -> type[AbstractDTO]`.
- Litestar uses the plugin only when an annotation is supported and the handler does not already define `dto` or `return_dto`.

Use this for reducing repeated DTO declarations, not for hiding contract decisions.

### `DIPlugin`

Use when Litestar needs help understanding constructor type information for dependency injection.

- Implement `has_typed_init(type_) -> bool`.
- Implement `get_typed_init(type_) -> tuple[Signature, dict[str, Any]]`.

Use this for model types whose constructor annotations are not directly recoverable by default inspection.

### `ReceiveRoutePlugin`

Use when a plugin must observe routes during registration.

- Implements `receive_route(route: BaseRoute) -> None`.
- Good for route validation, route metadata collection, or derived registration side effects.

Keep this observational. Do not bury broad app mutation here.

### `OpenAPISchemaPluginProtocol`

Use when a non-native model/type needs custom OpenAPI schema generation.

- Implement `is_plugin_supported_type(value) -> bool`.
- Implement `to_openapi_schema(field_definition, schema_creator) -> Schema`.

Use this for schema generation, not request parsing or DTO mutation.

## Selection Guide

Choose the smallest surface that solves the problem:

- Need to mutate `AppConfig` or install app-wide behavior: use an `InitPlugin`.
- Need automatic DTOs for specific model annotations: use a serialization plugin.
- Need constructor introspection for DI: use a `DIPlugin`.
- Need OpenAPI support for a model ecosystem: use a schema plugin.
- Need ORM request/session lifecycle: use the ORM ecosystem’s init/full plugin.
- Need only payload shaping for a model ecosystem: use explicit DTO classes instead of broad plugins.

## Ecosystem Guidance

### SQLAlchemy

Latest docs still show imports from `litestar.plugins.sqlalchemy`, but the class reference material is now largely hosted through Advanced Alchemy.

Primary choices:

- `SQLAlchemyPlugin(config=...)`: full integration; combines init behavior and serialization support.
- `SQLAlchemyInitPlugin(config=...)`: session/engine lifecycle and DI only.
- `SQLAlchemySerializationPlugin()`: auto-generates `SQLAlchemyDTO[...]` for supported annotations when no explicit DTO is declared.
- `SQLAlchemyDTO[Model]`: explicit DTO when you need contract control.

`SQLAlchemyInitPlugin` behavior in latest docs:

- Makes engine and session injectable.
- Stores engine and session factory in application state.
- Configures a `before_send` handler.
- Adds relevant names to the signature namespace.

Configuration rules:

- Use `SQLAlchemyAsyncConfig` for async engines/sessions.
- Use `SQLAlchemySyncConfig` for sync engines/sessions.
- Sync handlers using SQLAlchemy sessions should generally set `sync_to_thread=True`.
- Customize dependency names with `engine_dependency_key` and `session_dependency_key` if defaults conflict.
- Customize cleanup and transaction behavior with `before_send_handler`.
- Use the autocommit handlers only when request-scoped commit-on-success / rollback-on-error matches the app’s transaction model.
- Use `engine_config` and `session_config` for lower-level SQLAlchemy tuning instead of ad hoc patching.

Serialization rules:

- `SQLAlchemySerializationPlugin` is functionally equivalent to explicit `SQLAlchemyDTO[...]` declarations for supported annotations.
- Explicit DTOs still win when you need `DTOConfig`, separate read/write policies, field exclusions, or PATCH semantics.
- Mark fields and DTO config deliberately. The serialization plugin is not a substitute for contract review.

### Piccolo

Latest docs focus on `litestar.contrib.piccolo.PiccoloDTO` rather than a dedicated plugin page.

Use Piccolo support like this:

- `dto=PiccoloDTO[Table]`
- `return_dto=PiccoloDTO[Table]`
- PATCH via a subclass with `DTOConfig(exclude={"id"}, partial=True)` and `DTOData[Table].update_instance(...)`

Guidance:

- Treat Piccolo as a DTO integration first, not a general-purpose plugin stack.
- Manage table creation, connection lifecycle, and broader persistence architecture through normal startup/database patterns.
- If the task is mainly persistence design, hand off to `litestar-databases`.

### Pydantic

Latest docs expose a broader plugin surface here than for most other model ecosystems.

Available pieces:

- `PydanticPlugin`: broad app integration for Pydantic.
- `PydanticInitPlugin`: init-focused integration.
- `PydanticDIPlugin`: DI constructor/signature support.
- `PydanticDTO[T]`: explicit DTO support for Pydantic models.
- `PydanticSchemaPlugin`: OpenAPI schema generation.

Important `PydanticPlugin` / `PydanticInitPlugin` options:

- `exclude`
- `include`
- `exclude_defaults`
- `exclude_none`
- `exclude_unset`
- `prefer_alias`
- `validate_strict`
- `round_trip`

Use them carefully:

- `prefer_alias=True` when wire format should follow model aliases.
- `validate_strict=True` when Pydantic v2 coercion should be tightened.
- `round_trip=True` when dump behavior must preserve data for model re-validation or exact round-tripping.

Decision rules:

- Use `PydanticPlugin` when Pydantic behavior should be configured app-wide.
- Use `PydanticInitPlugin` when you want the init/serialization behavior without relying on the broader combined surface.
- Use `PydanticDIPlugin` when dependency constructors are Pydantic models or otherwise need plugin-assisted typed-init extraction.
- Use `PydanticDTO` when API contract control matters more than global plugin defaults.
- Use `PydanticSchemaPlugin(prefer_alias=...)` when schema generation must reflect alias choices.

Do not assume that installing `PydanticPlugin` removes the need for explicit DTOs. Public API contracts still need deliberate read/write shaping.

### Dataclasses

Latest docs document dataclass support as `DataclassDTO`, not as a standalone plugin usage page.

Use:

- `litestar.dto.dataclass_dto.DataclassDTO`

What it provides:

- DTO field-definition generation for dataclass models.
- Nested-field detection for dataclass graphs.

Guidance:

- Prefer `DataclassDTO` for transport contracts.
- Do not invent a custom plugin just to support ordinary dataclass request/response models.
- If you need app-wide bootstrapping behavior around dataclass usage, that is a separate `InitPlugin` concern.

### msgspec

Latest docs document msgspec support as `MsgspecDTO`, not as a standalone plugin usage page.

Use:

- `litestar.dto.msgspec_dto.MsgspecDTO`

What it provides:

- DTO field-definition generation for `msgspec.Struct` models.
- Nested-field detection for msgspec models.

Guidance:

- Prefer explicit `MsgspecDTO` declarations when msgspec models are the transport boundary.
- Validate wrapper responses and OpenAPI output carefully. High-performance transport types can hide contract drift if not tested.

### attrs

Latest docs document attrs support as an OpenAPI schema plugin:

- `litestar.plugins.attrs.AttrsSchemaPlugin`
- `litestar.plugins.attrs.is_attrs_class()`

Guidance:

- Treat attrs support as primarily a schema-generation concern in latest Litestar docs.
- Do not assume there is a full attrs serialization plugin or attrs DTO factory in the same style as Pydantic or SQLAlchemy.
- If attrs classes are transport models in your app, verify the exact request/response and schema behavior locally before standardizing on them.

### TypedDict

Latest docs do not expose a dedicated TypedDict plugin page.

Treat TypedDict support conservatively:

- Use TypedDict for static contract expression when plain annotations are sufficient.
- Verify generated OpenAPI and runtime behavior for the exact annotation shapes in play.
- If read/write transformation is required, prefer explicit DTOs or concrete transport models over assuming a TypedDict-specific plugin exists.

## Implementation Rules

- Prefer the smallest plugin surface that solves the problem.
- Keep plugin order deterministic and documented.
- Prefer explicit DTOs when the API contract differs from the domain model.
- Do not mix multiple model/serialization ecosystems in one API boundary without a clear reason.
- Keep plugin behavior version-aware; latest docs differ materially from older link layouts.
- Avoid global plugin installation when handler-level DTO declarations are enough.
- Keep `InitPlugin` logic composition-focused; do not bury business logic in `on_app_init()`.
- Keep `ReceiveRoutePlugin` side effects predictable and registration-time only.
- Keep DI plugins narrowly scoped to constructor inspection gaps.

## Custom Plugin Authoring Pattern

Use a custom plugin only when built-in surfaces are insufficient.

```python
from litestar import Litestar, get
from litestar.config.app import AppConfig
from litestar.di import Provide
from litestar.plugins import InitPlugin


@get("/health")
def healthcheck(version: str) -> dict[str, str]:
    return {"status": "ok", "version": version}


def provide_version() -> str:
    return "1.0.0"


class VersionPlugin(InitPlugin):
    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.dependencies["version"] = Provide(provide_version, sync_to_thread=False)
        app_config.route_handlers.append(healthcheck)
        return app_config


app = Litestar(route_handlers=[], plugins=[VersionPlugin()])
```

Authoring rules:

- Implement only the protocol you need.
- Make ordering requirements explicit if the plugin must run before or after other plugins.
- Keep mutations localized and reviewable.
- Do not rely on import-time side effects.
- If the plugin generates DTOs, document when explicit `dto` / `return_dto` should override it.

## Validation Checklist

- Confirm the selected surface is correct: plugin protocol vs DTO vs OpenAPI helper.
- Confirm plugin registration order is intentional and stable.
- Confirm app `on_app_init` hooks and plugin `on_app_init()` interactions are understood.
- Confirm explicit `dto` / `return_dto` declarations override plugin-generated DTO behavior where intended.
- Confirm request parsing and response serialization match the chosen model ecosystem.
- Confirm OpenAPI output is correct for Pydantic, attrs, dataclass, msgspec, and TypedDict annotations actually used.
- Confirm SQLAlchemy sync handlers are thread-safe and use `sync_to_thread=True` when needed.
- Confirm SQLAlchemy `before_send_handler` semantics match transaction boundaries.
- Confirm SQLAlchemy dependency key overrides do not break injection names.
- Confirm Piccolo and PATCH flows use `partial=True` plus `DTOData.update_instance()` when required.
- Confirm mixed serializer ecosystems are not competing at the same API boundary.
- Confirm stale docs links are not being copied into implementation decisions without checking current docs.

## Cross-Skill Handoffs

- Use `litestar-dto` for DTO shaping, `DTOConfig`, wrapper handling, and custom DTO factories.
- Use `litestar-databases` for overall SQLAlchemy or Piccolo persistence architecture.
- Use `litestar-dependency-injection` when the main challenge is dependency design rather than plugin wiring.
- Use `litestar-openapi` when schema generation and plugin-backed OpenAPI output are the main concern.
- Use `advanced-alchemy-litestar` when SQLAlchemy work is really about the Advanced Alchemy integration surface.

## Litestar References

Current primary references:

- https://docs.litestar.dev/latest/usage/plugins/index.html
- https://docs.litestar.dev/latest/reference/plugins/index.html
- https://docs.litestar.dev/latest/usage/databases/sqlalchemy/plugins/index.html
- https://docs.litestar.dev/latest/usage/databases/sqlalchemy/plugins/sqlalchemy_plugin.html
- https://docs.litestar.dev/latest/usage/databases/sqlalchemy/plugins/sqlalchemy_init_plugin.html
- https://docs.litestar.dev/latest/usage/databases/sqlalchemy/plugins/sqlalchemy_serialization_plugin.html
- https://docs.litestar.dev/latest/usage/databases/piccolo.html
- https://docs.litestar.dev/latest/reference/plugins/pydantic.html
- https://docs.litestar.dev/latest/reference/plugins/attrs.html
- https://docs.litestar.dev/latest/reference/dto/dataclass_dto.html
- https://docs.litestar.dev/latest/reference/dto/msgspec_dto.html
