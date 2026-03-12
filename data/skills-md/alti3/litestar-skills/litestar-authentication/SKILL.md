---
name: litestar-authentication
description: Implement Litestar authentication with custom authentication middleware, built-in security backends, JWT and session flows, route inclusion and exclusion rules, and typed auth context on `Request` / `ASGIConnection`. Use when establishing identity, issuing or validating credentials, or attaching authenticated user context in Litestar. Do not use for generic request parsing, broad security audits, or unrelated transport concerns.
---

# Authentication

## Execution Workflow

1. Choose the identity mechanism first: session, JWT header, JWT cookie, OAuth2 password bearer, or custom middleware based on client and trust boundaries.
2. Attach authentication once at app scope with `on_app_init` or middleware.
3. Configure exclusion rules explicitly for login, schema, health, and other public routes.
4. Use `request.user` and `request.auth` only after authentication has been established.
5. Apply guards separately for authorization checks.
6. Keep missing or invalid credential behavior consistent with the exception-handling strategy.

## Core Rules

- Keep authentication separate from request parsing and authorization.
- Let request parsing validate input fields before auth-specific business logic where possible.
- Prefer built-in security backends before custom middleware.
- Use custom middleware only when the identity source does not fit a built-in backend.
- Treat `request.user` and `request.auth` as authenticated context, not parsing shortcuts.
- Keep exclusion rules narrow and reviewable.
- Normalize identity failures to `401` behavior unless the project has a documented alternative.

## Decision Guide

- Use `SessionAuth` for browser-first applications with server-managed sessions.
- Use `JWTAuth` for token-in-header API clients.
- Use `JWTCookieAuth` for browser flows where token cookies are intentional.
- Use `OAuth2PasswordBearerAuth` when password-flow token issuance semantics are required.
- Use `AbstractAuthenticationMiddleware` when the credential source or validation logic is custom.
- Use `litestar-security` when the task includes authorization policy, secrets, and defense-in-depth concerns beyond identity wiring.

## Reference Files

Read only the sections you need:

- For custom middleware, built-in backends, request auth context, exclusion rules, and login patterns, read [references/auth-patterns.md](references/auth-patterns.md).

## Recommended Defaults

- Keep authentication middleware or backend registration at app scope.
- Exclude only explicitly public routes.
- Access authenticated context through typed `Request` or `ASGIConnection` after auth runs.
- Keep token issuance and logout flows explicit and testable.
- Hand off `401` / `403` response formatting to `litestar-exception-handling`.

## Anti-Patterns

- Parsing auth headers manually in every route handler.
- Mixing authorization policy into authentication middleware.
- Treating `request.user` as available on routes excluded from authentication.
- Using broad path exclusions that create accidental public surface area.
- Hardcoding secrets or sample tokens outside local examples.

## Validation Checklist

- Confirm protected endpoints reject missing or invalid credentials.
- Confirm public routes are public only when explicitly excluded.
- Confirm `request.user` and `request.auth` have the expected types on authenticated routes.
- Confirm login and logout flows produce the intended token or session behavior.
- Confirm identity failures line up with the exception-handling contract.
- Confirm tests cover both authenticated and unauthenticated paths.

## Cross-Skill Handoffs

- Use `litestar-requests` for header, cookie, and body parsing concerns that are not identity-specific.
- Use `litestar-security` for authorization, secret hygiene, and broader security posture.
- Use `litestar-exception-handling` to standardize `401` and `403` contracts.
- Use `litestar-testing` for auth boundary, exclusion-rule, and token-flow tests.

## Litestar References

- https://docs.litestar.dev/latest/usage/security/abstract-authentication-middleware.html
- https://docs.litestar.dev/latest/usage/security/security-backends.html
- https://docs.litestar.dev/latest/usage/security/jwt.html
- https://docs.litestar.dev/latest/usage/security/excluding-and-including-endpoints.html
