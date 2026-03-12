---
name: litestar-htmx
description: Build HTMX-driven Litestar flows with `HTMXPlugin`, `HTMXRequest`, `request.htmx`, `HTMXTemplate`, and HTMX response classes such as `HXLocation`, `PushUrl`, `ReplaceUrl`, `Reswap`, `Retarget`, `TriggerEvent`, `ClientRedirect`, `ClientRefresh`, and `HXStopPolling`. Use when implementing server-rendered partial updates, progressive enhancement, polling, redirects, or history-aware HTML interactions. Do not use for SPA-only JSON APIs that do not exchange HTML or HTMX headers.
---

# HTMX

## Execution Workflow

1. Decide whether HTMX should be enabled globally with `HTMXPlugin` or locally with `request_class=HTMXRequest`.
2. Shape handlers around one contract: full page for normal requests, fragment or HTMX-aware response for HTMX requests.
3. Read request context from `request.htmx` instead of hand-parsing HTMX headers.
4. Choose the right response primitive: `HTMXTemplate` for rendered fragments or the dedicated HTMX response classes for redirect, refresh, swap, retarget, event, history, or polling behavior.
5. Keep templates small and swap-oriented so each endpoint returns only the markup or signal the target element needs.
6. Verify both non-HTMX and HTMX behaviors in tests, including headers, redirect semantics, and fragment shape.

## Core Rules

- Use `HTMXPlugin()` when most of the app should speak HTMX-aware requests.
- Use `request_class=HTMXRequest` locally when only one app layer or route needs HTMX support.
- Prefer `request.htmx` and `HTMXDetails` properties over manual header inspection.
- Keep full-page and fragment rendering intentional; do not accidentally return layout HTML into a fragment swap target.
- Annotate `HTMXTemplate` handlers as returning `Template`, matching the Litestar docs.
- If you trigger an HTMX event from `HTMXTemplate`, provide `after=` and keep it to `receive`, `settle`, or `swap`.
- Use the dedicated HTMX response classes instead of hand-setting `HX-*` headers.
- Treat HTMX handlers as first-class HTTP endpoints with clear success, validation, and fallback behavior.

## Decision Guide

- Use `HTMXPlugin()` when HTMX is the dominant interaction model.
- Use `HTMXConfig(set_request_class_globally=False)` when you want the plugin installed without forcing `HTMXRequest` at app scope.
- Use `request.htmx` truthiness to branch between full-page and fragment responses.
- Use `HTMXTemplate` when the response is HTML and may also need `push_url`, `re_swap`, `re_target`, or event triggering.
- Use `ClientRedirect` when the browser should redirect with a full reload.
- Use `HXLocation` when the client should navigate without a full page reload and may need target, swap, select, headers, or values.
- Use `PushUrl` or `ReplaceUrl` when you want to return content and also mutate browser history or the location bar.
- Use `Reswap`, `Retarget`, or `TriggerEvent` when the content stays inline but the HTMX client behavior must change.
- Use `ClientRefresh` when the whole page must refresh.
- Use `HXStopPolling` for polling endpoints that should explicitly stop the HTMX client.

## Reference Files

Read only the sections you need:

- For global vs local setup, `HTMXPlugin`, `HTMXConfig`, `HTMXRequest`, and `request.htmx` usage, read [references/setup-and-request-patterns.md](references/setup-and-request-patterns.md).
- For `HTMXTemplate`, full-page vs fragment rendering, and the dedicated HTMX response classes, read [references/template-and-response-patterns.md](references/template-and-response-patterns.md).
- For HTMX details properties, history-aware flows, polling, and testing patterns, read [references/details-polling-and-testing.md](references/details-polling-and-testing.md).

## Recommended Defaults

- Keep template rendering centralized through normal `template_config`; layer HTMX on top of existing server-rendered HTML rather than inventing a separate rendering stack.
- Use `HTMXPlugin()` when most handlers will need `request.htmx`.
- Branch once near the handler boundary between full-page and fragment rendering.
- Return the smallest useful HTML fragment for the current swap target.
- Prefer `HTMXTemplate` and the built-in HTMX response classes over manual header management.
- Keep route URLs stable so `push_url`, `replace_url`, and `HXLocation` remain predictable in tests and browser history.

## Anti-Patterns

- Parsing raw `HX-*` headers directly when `request.htmx` already provides the values.
- Returning a full layout to an element that expects only a fragment.
- Annotating handlers as `HTMXTemplate` instead of `Template`.
- Mixing JSON API behavior and fragment HTML behavior without an explicit branching contract.
- Hand-crafting HTMX response headers when a Litestar response class already models the behavior.
- Using HTMX response primitives without covering the non-HTMX fallback path when the route can also be opened directly.
- Treating polling, redirects, or event triggers as frontend-only concerns and leaving the server contract implicit.

## Validation Checklist

- Confirm HTMX enablement is global or local by intent.
- Confirm non-HTMX requests still receive a valid page or fallback response.
- Confirm HTMX requests return fragment-sized HTML or the intended HTMX response class.
- Confirm `request.htmx` fields used by the handler actually match the client-side HTMX attributes in play.
- Confirm `HTMXTemplate` event triggering includes `after=` when required.
- Confirm redirect, push, replace, retarget, swap, refresh, and polling behavior use the correct response primitive.
- Confirm templates do not depend on layout-only context when rendered as fragments.
- Confirm tests cover both body content and HTMX behavior.

## Cross-Skill Handoffs

- Use `litestar-templating` for engine setup, template directories, shared layouts, and template helper concerns.
- Use `litestar-responses` when the main issue is generic response metadata rather than HTMX-specific headers and flow control.
- Use `litestar-routing` when controller/router-level `request_class` placement or route structure is the real problem.
- Use `litestar-testing` to assert fragment HTML, redirects, polling stop behavior, and HTMX header-driven contracts.

## Litestar References

- https://docs.litestar.dev/2/usage/htmx.html
- https://docs.litestar.dev/2/reference/plugins/htmx.html
