---
name: litestar-lifecycle-hooks
description: Apply Litestar request lifecycle hooks with `before_request`, `after_request`, and `after_response` for request enrichment, short-circuiting, response mutation, post-send side effects, and layered cross-cutting behavior around handler execution. Use when logic should run immediately before the handler, after the response object is resolved, or after the response has been sent. Do not use for startup/shutdown ownership, `before_send` / `after_exception` / `on_app_init`, decoupled event fanout, or raw ASGI wrapping that belongs in app setup, events, or middleware.
---

# Lifecycle Hooks

Use this skill when the requirement is specifically about the request-handler lifecycle for HTTP handlers, not application bootstrapping or whole-ASGI wrapping.

## Execution Workflow

1. Decide which stage matches the requirement: `before_request`, `after_request`, or `after_response` (the exact lifecycle stage needed for behavior injection).
2. Choose the layer intentionally: app, router, controller, or handler (the layer to place the hook in).
3. Keep hook behavior small, deterministic, and clearly cross-cutting.
4. Implement request-state handoff or response mutation explicitly.
5. Test normal flow, short-circuit flow, and layer-precedence behavior explicitly.

## Core Rules

- Match the hook to the lifecycle stage instead of forcing one hook to do everything.
- Keep hooks transport-focused and cross-cutting; push domain rules into services or handlers.
- Keep `before_request` return values deliberate because any non-`None` response-compatible value bypasses the route handler.
- Keep `after_request` focused on the resolved `Response`; it may return the same response or a replacement response.
- Keep `after_response` side effects safe to run after the response is already sent; it cannot change the response the client received.
- Treat hook placement as behavior: Litestar lifecycle hooks are layered, and the closest layer to the handler takes precedence.
- Use request state or other explicit request-scoped storage when `before_request` must pass data into the handler.

## Decision Guide

- Use `before_request` when you need request gating, request-state enrichment, or an early HTTP result before the handler runs.
- Use `after_request` when you need response-object mutation such as reshaping content, adding headers, or swapping the response type.
- Use `after_response` when you need metrics, counters, audit emission, or third-party notification after the response has already gone out.
- Use `litestar-middleware` instead when the concern needs raw ASGI `scope/receive/send`, broad wrapping across route groups, built-in middleware, or WebSocket/lifespan coverage.
- Use `litestar-app-setup` instead when the concern is `before_send`, `after_exception`, `on_app_init`, startup/shutdown hooks, or lifespan-managed resources.
- Use `litestar-events` instead when one action should fan out into decoupled in-process side effects rather than inline lifecycle interception.

## Reference Files

Read only the sections you need:

- For exact hook semantics, short-circuit behavior, handler-to-response boundaries, and layered precedence, read [references/request-response-hooks.md](references/request-response-hooks.md).
- For deciding between lifecycle hooks and middleware, including exception-path and ASGI-boundary differences, read [references/hook-vs-middleware.md](references/hook-vs-middleware.md).

## Hook Semantics

### `before_request`

- Runs immediately before the route handler function is called.
- Accepts a `Request` as its first parameter.
- Returns either `None` or any value Litestar can use as a response.
- Returning a value bypasses the route handler for that request.
- Best for request enrichment, conditional short-circuiting, and request-scoped flags stored on `request.state`.

### `after_request`

- Runs after the route handler has returned and Litestar has resolved a `Response`.
- Accepts a `Response` as its first parameter.
- Must return a `Response`.
- May mutate and return the same response or replace it with a different response object.
- Best for response normalization, response metadata, and response-type transformation after handler execution.

### `after_response`

- Runs after the response has been returned by the server.
- Accepts a `Request` as its first parameter.
- Returns `None`.
- Cannot affect the response that the client already received.
- Best for post-send metrics, counters, audit trails, and external notifications.

## Layering Model

- Lifecycle hooks participate in Litestar's layered architecture.
- You can define them on the application, router, controller, or handler layer.
- If the same lifecycle hook is defined on multiple layers, the layer closest to the handler takes precedence.
- Do not assume hook definitions compose across layers; precedence is override-oriented, not additive.

## Recommended Defaults

- Prefer one clear responsibility per hook.
- Store transient per-request data on `request.state` when `before_request` needs to communicate with the handler.
- Return `None` from `before_request` unless you intentionally want to short-circuit the handler.
- Mutate the existing response in `after_request` when that is sufficient; replace it only when the response contract truly changes.
- Keep `after_response` idempotent enough for retries in tests and safe enough that delayed failures do not corrupt request flow assumptions.
- Keep layer overrides narrow and documented by placement rather than comments whenever possible.

## Example Pattern

```python
from litestar import Litestar, Request, Response, get
from litestar.status_codes import HTTP_403_FORBIDDEN


async def before_request(request: Request) -> Response | None:
    tenant_id = request.headers.get("x-tenant-id")
    if tenant_id is None:
        return Response({"detail": "missing tenant"}, status_code=HTTP_403_FORBIDDEN)
    request.state.tenant_id = tenant_id
    return None


async def after_request(response: Response) -> Response:
    response.headers["x-service"] = "orders"
    return response


async def after_response(request: Request) -> None:
    request.app.state.setdefault("paths_seen", []).append(request.url.path)


@get("/orders")
async def list_orders(request: Request) -> dict[str, str]:
    return {"tenant_id": request.state.tenant_id}


app = Litestar(
    route_handlers=[list_orders],
    before_request=before_request,
    after_request=after_request,
    after_response=after_response,
)
```

## Anti-Patterns

- Hiding authoritative business rules in hooks instead of the handler or service layer.
- Returning ad hoc shapes from `before_request` without treating them as real response contracts.
- Doing heavy network or database work in `after_request` when the concern belongs in `after_response`, events, or a background mechanism.
- Expecting `after_response` mutations to show up in the current client response.
- Defining the same hook on multiple layers and expecting all of them to run.
- Using lifecycle hooks as a substitute for startup/shutdown resource management.
- Reaching for middleware when only request or response objects need light interception.

## Validation Checklist

- Confirm the chosen hook stage matches the intended timing.
- Confirm `before_request` short-circuit cases bypass the handler as intended.
- Confirm request-scoped data written by `before_request` is available where it is later consumed.
- Confirm `after_request` always returns a valid `Response`.
- Confirm `after_response` side effects tolerate the fact that the response is already gone to the client.
- Confirm layer placement is intentional and tested where app/router/controller/handler overrides exist.
- Confirm error-path behavior is tested if hooks must coexist with exception handlers or middleware.
- Confirm the logic still belongs in hooks rather than middleware, events, or app setup.

## Cross-Skill Handoffs

- Use `litestar-app-setup` for startup/shutdown hooks, lifespan, `before_send`, `after_exception`, and `on_app_init`.
- Use `litestar-middleware` when the concern must wrap the ASGI pipeline rather than request and response objects.
- Use `litestar-events` for decoupled in-process side effects instead of inline hook fanout.
- Use `litestar-testing` to verify short-circuit behavior, layer precedence, and post-send side effects.

## Litestar References

- https://docs.litestar.dev/latest/usage/lifecycle-hooks.html
- https://docs.litestar.dev/latest/usage/middleware/index.html
- https://docs.litestar.dev/latest/usage/middleware/using-middleware.html
