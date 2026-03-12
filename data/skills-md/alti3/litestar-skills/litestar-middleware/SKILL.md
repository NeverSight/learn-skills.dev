---
name: litestar-middleware
description: Design and apply Litestar middleware for cross-cutting concerns such as CORS, CSRF, allowed-host checks, compression, rate limiting, logging, sessions, request enrichment, policy enforcement, and custom ASGI pipeline control. Use when behavior must wrap broad route sets consistently across the ASGI stack. Do not use for route-specific business rules, simple response mutation better handled by lifecycle hooks, or auth/guard policy work that belongs in security-focused skills.
---

# Middleware

## Execution Workflow

1. Confirm the requirement is really middleware-worthy: broad ASGI wrapping, not route business logic.
2. Prefer built-in config-based middleware first.
3. Choose the right layer and ordering deliberately.
4. Decide whether the concern belongs in middleware, lifecycle hooks, or route logic.
5. For custom middleware, choose the simplest correct implementation style.
6. Validate both success and exception-generated responses, plus exclusions and scope handling.

## Core Rules

- Keep middleware focused on one cross-cutting concern.
- Prefer built-in middleware/config objects before creating custom implementations.
- Treat middleware order as part of API behavior.
- Keep middleware scope-aware for `http`, `websocket`, and `lifespan` as needed.
- Use lifecycle hooks when the job is response-object mutation rather than ASGI message wrapping.
- Keep middleware non-blocking and ASGI-compliant.
- Keep `404` and `405` expectations explicit because those router-generated exceptions occur before the middleware stack.

## Decision Guide

- Use built-in config middleware for CORS, CSRF, compression, rate limiting, logging, sessions, and allowed hosts.
- Use a middleware factory for very small wrappers.
- Use `ASGIMiddleware` for configurable production custom middleware.
- Use `MiddlewareProtocol` for minimal low-level behavior.
- Use `AbstractMiddleware` only for compatibility or migration scenarios.
- Use `DefineMiddleware` when constructor-style args must be supplied to a middleware factory or class.
- Use `litestar-lifecycle-hooks` instead when the behavior belongs to `after_request`, `before_send`, or related hook stages.

## Reference Files

Read only the sections you need:

- For middleware fundamentals, ordering, exclusions, and built-in middleware selection, read [references/builtin-and-ordering.md](references/builtin-and-ordering.md).
- For custom middleware implementation styles, `ASGIMiddleware`, `MiddlewareProtocol`, `AbstractMiddleware`, and `DefineMiddleware`, read [references/custom-middleware-patterns.md](references/custom-middleware-patterns.md).

## Recommended Defaults

- Start with one middleware concern at a time.
- Keep built-in config values explicit and reviewed.
- Keep exclusions and `opt`-based skips narrow and tested.
- Make ordering assumptions visible in code comments only when they are truly non-obvious.
- Test middleware against both successful and failing downstream handlers.

## Anti-Patterns

- Putting route-specific business rules into middleware.
- Creating custom middleware when a built-in config or lifecycle hook already fits.
- Ignoring middleware order when several wrappers interact.
- Mutating request or response state at the wrong ASGI stage.
- Assuming router-generated `404` and `405` pass through middleware.
- Letting middleware silently depend on undocumented `opt` exclusions or path patterns.

## Validation Checklist

- Confirm middleware is attached at the intended layer only.
- Confirm order matches both layer precedence and list order.
- Confirm exclusions via path patterns, `exclude_opt_key`, or scopes behave as intended.
- Confirm behavior is correct for both success and exception-generated responses.
- Confirm `404` and `405` behavior is handled at the right boundary.
- Confirm custom middleware remains ASGI-compliant and non-blocking.
- Confirm built-in security and logging middleware settings align with deployment expectations.

## Cross-Skill Handoffs

- Use `litestar-lifecycle-hooks` for hook-stage logic rather than raw ASGI wrapping.
- Use `litestar-authentication`, `litestar-security`, `litestar-logging`, and `litestar-metrics` for domain-specific middleware outcomes.
- Use `litestar-debugging` when middleware interactions are the source of a runtime defect.
- Use `litestar-routing` when middleware behavior depends on layer placement or `opt` strategy.

## Litestar References

- https://docs.litestar.dev/latest/usage/middleware/index.html
- https://docs.litestar.dev/latest/usage/middleware/using-middleware.html
- https://docs.litestar.dev/latest/usage/middleware/builtin-middleware.html
- https://docs.litestar.dev/latest/usage/middleware/creating-middleware.html
