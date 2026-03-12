---
name: litestar-dto
description: Configure Litestar DTO behavior for inbound parsing and outbound serialization, including layer-scoped `dto`/`return_dto`, `DTOConfig` policies, `DTOData` update workflows, and custom `AbstractDTO` implementations. Use when API payload contracts differ from internal model structures. Do not use when internal models can be exposed safely without transformation.
---

# DTO

Use this skill when request and response payloads need explicit shape control, field-level policy, or DTO factory customization.

## Execution Workflow

1. Start with the handler contract: define inbound (`dto`) and outbound (`return_dto`) behavior explicitly.
2. Choose DTO factory type for your model ecosystem (for example, `DataclassDTO`, `SQLAlchemyDTO`, or plugin-provided DTOs).
3. Define policy with `DTOConfig` (exclude, rename, nesting depth, unknown-field handling, PATCH behavior).
4. Apply DTOs at the correct layer (handler, controller, router, or app) and rely on closest-layer precedence.
5. Use `DTOData[T]` in write/update handlers when you need controlled instantiation and patching semantics.
6. Validate wrappers and envelopes (`Response[T]`, pagination, generic wrappers) to ensure DTO transformation is still applied.
7. Implement a custom `AbstractDTO` only when factory DTOs cannot express required behavior.

## Implementation Rules

- Keep read and write DTOs separate when policies differ.
- Keep DTO configuration explicit and reviewable; avoid implicit field exposure.
- Treat nested serialization depth as an API and performance control, not a default.
- Reject unknown fields (`forbid_unknown_fields=True`) in stricter API surfaces.
- Use DTOs to enforce immutability and server-owned fields (`id`, audit fields).
- Keep handler logic focused on business behavior, not ad-hoc payload transformation.

## DTO Basics: Layering and Parameters

Litestar exposes two DTO parameters on each app layer:

- `dto`: inbound parsing for handler `data`; if `return_dto` is not set, this is also used for outbound serialization.
- `return_dto`: outbound serialization policy only.

DTOs can be declared on handler, controller, router, or application. The DTO closest to the handler in the ownership chain applies.

Common pattern:

- `dto=WriteDTO` to parse inbound payloads.
- `return_dto=ReadDTO` to serialize outbound payloads.
- `return_dto=None` on handlers where DTO serialization should be disabled (for example, `DELETE -> None`).

## `DTOConfig` Policy Guide

Use `DTOConfig` to define stable contract rules:

- `exclude={...}`: remove fields (supports nested paths, including list-item paths such as `"pets.0.id"`).
- `rename_fields={...}`: rename specific fields.
- `rename_strategy="camel"` (or callback): apply systematic renaming.
- `max_nested_depth`: control nested parsing/serialization depth (`1` default shown in docs).
- `forbid_unknown_fields=True`: reject extra payload fields instead of silently ignoring them.
- `partial=True`: PATCH-friendly DTO behavior.
- `leading_underscore_private=False` only when you intentionally want underscore-prefixed fields treated as public.
- `experimental_codegen_backend=False` to selectively disable codegen backend behavior.

Important behavior:

- Explicit `rename_fields` mappings are not further transformed by `rename_strategy`.

## Field Marking and Access Control

Use `dto_field(...)` metadata to mark model fields with DTO semantics:

- `"private"`: not parsed from inbound data and never serialized in outbound data.
- `"read-only"`: not parsed from inbound data.

Also note:

- Fields with leading underscores are implicitly private by default.

## `DTOData[T]`: Controlled Create and Update Flows

Use `DTOData[T]` for create/update handlers that need controlled model mutation:

- `data.create_instance(...)` creates model instances from validated input and can inject server-side values.
- Nested values can be supplied with double-underscore paths (for example, `address__id=...`) when excluded nested fields must still be set.
- `data.update_instance(existing)` supports partial updates cleanly for PATCH workflows when `partial=True`.

PATCH pattern:

- Exclude immutable/server-owned fields (for example, `id`) in DTO config.
- Use `DTOData.update_instance()` to apply only submitted fields.

## Wrapper and Envelope Handling

DTO factory types can transform data inside supported wrappers:

- Generic wrapper dataclasses (for example, `WithCount[T]`) when one type parameter maps to DTO-supported model data.
- Litestar pagination wrappers such as `ClassicPagination[T]` (DTO applies to `items`).
- `Response[T]` wrappers (DTO applies to `content`).

## Performance Notes

DTO codegen backend:

- Introduced in `2.2.0`, stabilized and enabled by default in `2.8.0`.
- Can be toggled per DTO with `DTOConfig(experimental_codegen_backend=...)`.

Use selective override only when debugging compatibility or behavior differences.

## AbstractDTO and Custom DTO Classes

Use built-in DTO factories first. Create custom DTO classes only when required behavior is not expressible via existing DTO factories + `DTOConfig`.

When implementing custom DTOs, you must implement `AbstractDTO` methods:

- `generate_field_definitions(model_type)`: yield `DTOFieldDefinition` objects for DTO-visible fields.
- `detect_nested_field(field_definition)`: return whether the field represents nested model data.

This is the minimal protocol Litestar requires for custom DTO implementations.

## Example Patterns

```python
from litestar import get, patch
from litestar.dto import DTOConfig, DTOData, DataclassDTO

class UserReadDTO(DataclassDTO[User]):
    config = DTOConfig(exclude={"password_hash"})

class UserPatchDTO(DataclassDTO[User]):
    # Patch DTO excludes immutable id and accepts partial payloads.
    config = DTOConfig(exclude={"id"}, partial=True)

@get("/users/{user_id:int}", return_dto=UserReadDTO)
async def get_user(user_id: int) -> User:
    return ...

@patch("/users/{user_id:int}", dto=UserPatchDTO, return_dto=UserReadDTO)
async def patch_user(user_id: int, data: DTOData[User]) -> User:
    user = ...
    return data.update_instance(user)
```

```python
from litestar.dto import DTOConfig
from litestar.plugins.sqlalchemy import SQLAlchemyDTO

class PublicUserDTO(SQLAlchemyDTO[User]):
    config = DTOConfig(exclude={"password_hash"})
```

## Validation Checklist

- Confirm `dto` and `return_dto` are intentionally selected (or explicitly disabled) per handler.
- Confirm layer precedence does not accidentally override handler-level DTO intent.
- Confirm exclude/rename/nesting config generates expected payload shape.
- Confirm unknown field behavior matches API strictness (`forbid_unknown_fields`).
- Confirm private/read-only/underscore fields are not writable by clients.
- Confirm PATCH handlers use `partial=True` + `DTOData.update_instance()` where appropriate.
- Confirm wrapper responses (`Response`, pagination, generic envelopes) still apply DTO transformations.
- Confirm OpenAPI output matches the DTO-shaped contract.

## Cross-Skill Handoffs

- Use `litestar-dataclasses`, `litestar-plugins`, or `litestar-custom-types` for model ecosystem specifics.
- Use `litestar-databases` when DTO behavior couples to SQLAlchemy or Piccolo persistence design.
- Use `litestar-openapi` to verify generated schema accuracy after DTO changes.
- Use `litestar-requests` and `litestar-responses` for transport-level behavior outside DTO transformation.

## Litestar References

- https://docs.litestar.dev/2/usage/dto/index.html
- https://docs.litestar.dev/2/usage/dto/0-basic-use.html
- https://docs.litestar.dev/2/usage/dto/1-abstract-dto.html
- https://docs.litestar.dev/2/usage/dto/2-creating-custom-dto-classes.html
