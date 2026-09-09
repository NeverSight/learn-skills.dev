---
name: litestar-auth-guards
description: "Auto-activate for guards=, Guard, ASGIConnection, JWTAuth, JWTCookieAuth, SessionAuth, role or tenant checks, or WebSocket auth. Not for frontend route protection."
---

# Litestar Auth and Guards

Use this skill for authentication boundaries, authorization checks, guard composition, and user context.

## Code Style Rules

- Put auth and permission checks in Guards or middleware, not handler bodies.
- Prefer Controller-level guards when a whole domain shares a policy.
- Raise Litestar HTTP exceptions or domain exceptions consistently.
- Keep tenant isolation explicit in guard logic and service filters.
- Let authentication middleware populate `connection.user` and
  `connection.auth`; use guards for authorization.

## Quick Reference

- Guard patterns: [guards.md](references/guards.md)
- Middleware user loading: [litestar-middleware](../litestar-middleware/SKILL.md)
- Realtime auth: [litestar-realtime](../litestar-realtime/SKILL.md)

<workflow>

## Workflow

1. Determine where identity is loaded.
2. Add Guards at app, Controller, or route scope.
3. Keep permission checks reusable and testable.
4. Verify denial paths and authenticated success paths.

</workflow>

<guardrails>

## Guardrails

- Do not inline auth checks in handlers.
- Do not make Guards perform database work repeatedly when middleware can load the user once.
- Do not trust client-supplied tenant IDs without server-side scoping.
- Do not use HTTP-only assumptions for WebSocket auth.
- Do not claim WebSocket handshakes cannot carry headers. Non-browser clients
  can send them; the browser WebSocket API cannot set arbitrary headers.

</guardrails>

<validation>

## Validation Checkpoint

- [ ] Guard scope matches the policy scope.
- [ ] Denial paths return the expected status.
- [ ] Handlers contain no duplicated auth branching.
- [ ] Browser WebSocket routes use cookies, a short-lived query token, or a
  first-message protocol; non-browser header auth is documented separately.

</validation>

<example>

## Example

```python
from litestar.connection import ASGIConnection
from litestar.exceptions import PermissionDeniedException
from litestar.handlers import BaseRouteHandler


async def requires_active_user(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    if not connection.user or not connection.user.is_active:
        raise PermissionDeniedException("Authentication required")
```

</example>

## References Index

- [guards.md](references/guards.md)

## Official References

- <https://docs.litestar.dev/> - Litestar documentation
- <https://docs.litestar.dev/latest/reference/> - Litestar API reference
- <https://github.com/litestar-org/litestar/tree/v2.24.0> - Audited Litestar 2.24.0 source

## Shared Styleguide Baseline

- [General](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
