---
name: litestar-middleware
description: "Auto-activate for ASGIMiddleware, DefineMiddleware, middleware=, CORSConfig, CSRFConfig, AllowedHostsConfig, CompressionConfig, request IDs, or ASGI scopes. Not for route logic."
---

# Litestar Middleware

Use this skill for built-in middleware config, custom ASGI middleware, request lifecycle hooks, and auth user loading.

## Code Style Rules

- Use built-in middleware configs before custom middleware.
- Keep middleware focused on cross-cutting request behavior.
- Filter by ASGI scope when middleware applies only to HTTP or WebSocket.
- Keep business policy in Guards and services.

## Quick Reference

- Middleware patterns: [middleware.md](references/middleware.md)
- Pair with [litestar-auth-guards](../litestar-auth-guards/SKILL.md) for permission checks.
- Pair with [litestar-deployment](../litestar-deployment/SKILL.md) for proxy and platform concerns.

<workflow>

## Workflow

1. Decide whether a built-in config solves the need.
2. Choose custom middleware only for cross-cutting behavior.
3. Set ordering deliberately.
4. Verify HTTP and WebSocket behavior separately when both apply.

</workflow>

<guardrails>

## Guardrails

- Do not put business workflows in middleware.
- Do not apply HTTP-only middleware to WebSocket scopes.
- Do not mutate request state without documenting the key.
- Do not duplicate Guard policy in middleware.

</guardrails>

<validation>

## Validation Checkpoint

- [ ] Middleware order is intentional.
- [ ] Scope filtering is correct.
- [ ] Built-in configs are used where available.
- [ ] Tests cover the request path affected by middleware.

</validation>

<example>

## Example

```python
from litestar.middleware import ASGIMiddleware

middleware = [RequestIDMiddleware()]
```

</example>

## References Index

- [middleware.md](references/middleware.md)

## Official References

- <https://docs.litestar.dev/> - Litestar documentation
- <https://docs.litestar.dev/latest/reference/> - Litestar API reference

## Shared Styleguide Baseline

- [General](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
