---
name: litestar-contrib
description: Integrate Litestar contrib modules (for example HTMX, Jinja, Mako, JWT, OpenTelemetry, Pydantic, SQLAlchemy, Piccolo) with explicit scope and compatibility checks. Use when adding optional Litestar contrib features to an app. Do not use for core framework features that do not require contrib integrations.
---

# Contrib

## Execution Workflow

1. Identify the exact contrib module required for the user task.
2. Install and configure only that module (avoid broad optional dependency sprawl).
3. Verify compatibility with existing middleware, DTO, auth, and plugin stack.
4. Add focused regression tests at integration boundaries.

## Implementation Rules

- Keep contrib usage isolated behind clear adapters.
- Validate defaults before adding custom hooks/configuration.
- Treat each contrib add-on as an explicit architecture decision.
- Document operational implications (extra services, env vars, runtime dependencies).

## Example Pattern

```python
# Pattern: wire one contrib integration at app creation.
from litestar import Litestar

app = Litestar(
    route_handlers=[...],
    plugins=[...],  # add only the contrib plugin you need
)
```

## Validation Checklist

- Confirm contrib integration loads correctly at app startup.
- Confirm failure behavior is explicit when optional dependencies are missing.
- Confirm integration does not silently alter unrelated routes.

## Cross-Skill Handoffs

- Use `litestar-plugins` for plugin-system-focused integrations.
- Use `litestar-metrics`, `litestar-authentication`, `litestar-databases`, or `litestar-templating` for topic depth after contrib setup.

## Litestar References

- https://docs.litestar.dev/latest/usage/contrib.html
- https://docs.litestar.dev/latest/reference/contrib/index.html
