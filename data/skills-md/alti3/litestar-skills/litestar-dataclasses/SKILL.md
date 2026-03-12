---
name: litestar-dataclasses
description: Use Python dataclasses as Litestar transport models with explicit typing, defaults, and DTO interplay. Use when modeling request/response contracts with lightweight typed objects. Do not use when plugin-backed model systems (Pydantic/msgspec/attrs/ORM) are a better fit for the task.
---

# Dataclasses

## Execution Workflow

1. Define dataclasses for transport boundaries with explicit field types.
2. Use defaults and optionality intentionally to avoid ambiguous schemas.
3. Combine with DTO configuration when write/read shapes diverge.
4. Keep domain entities and transport dataclasses separate when needed.

## Implementation Rules

- Favor immutable or clearly controlled mutation patterns.
- Avoid embedding persistence/session behavior in dataclasses.
- Keep field names/schema stable for clients.
- Validate nested dataclass behavior in serialization paths.

## Example Pattern

```python
from dataclasses import dataclass
from litestar import post

@dataclass
class CreateUser:
    name: str
    email: str

@post("/users")
async def create_user(data: CreateUser) -> dict[str, str]:
    return {"email": data.email}
```

## Validation Checklist

- Confirm request binding maps correctly into dataclass fields.
- Confirm response serialization matches expected JSON schema.
- Confirm DTO include/exclude behavior remains predictable.

## Cross-Skill Handoffs

- Use `litestar-dto` for advanced shaping and nested field policy.
- Use `litestar-plugins` when switching to different model ecosystems.

## Litestar References

- https://docs.litestar.dev/latest/usage/dto/index.html
