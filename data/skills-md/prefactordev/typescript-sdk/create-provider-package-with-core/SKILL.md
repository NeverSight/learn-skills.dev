---
name: create-provider-package-with-core
description: Use when building a custom provider integration on top of @prefactor/core so your app can instrument agent, llm, and tool workflows without relying on a prebuilt adapter package.
---

# Create Provider Package With Core

Build your own provider adapter package on top of `@prefactor/core`.

Core principle: `@prefactor/core` handles tracing infrastructure, while your adapter maps provider-specific APIs.

## Trigger Phrases

Apply this skill when the request includes patterns like:

- "add a new provider package"
- "instrument provider X using @prefactor/core"
- "my framework does not have a Prefactor adapter"
- "build a custom SDK integration with Prefactor"

## Workflow

1. Define adapter boundaries.
2. Create a small adapter package in your project.
3. Implement instrumentation with core primitives.
4. Validate trace behavior in your app.
5. Harden for production usage.

## 1) Define adapter boundaries

- Keep your adapter thin: request/response mapping, middleware hooks, payload adaptation.
- Reuse `@prefactor/core` for lifecycle, context, serialization, and transport behavior.
- Use provider-prefixed span types (`<provider>:agent`, `<provider>:llm`, `<provider>:tool`).

## 2) Create a small adapter package

In your app or workspace, create a dedicated module/package (for example `prefactor-provider-<provider>`):

- `src/index.ts` public entrypoint
- `src/<provider>-middleware.ts` provider integration wrapper
- `tests/` covering tracing behavior
- `package.json` with dependency on `@prefactor/core`

Use this package surface:

- ESM imports/exports; explicit `.js` on relative imports.
- Export only stable adapter entrypoints from `src/index.ts`.

## 3) Implement instrumentation with core primitives

- Depend on `@prefactor/core` for tracing, context propagation, config, transport helpers.
- Wrap provider execution paths in context (`SpanContext.runAsync(...)`) so parent/child spans remain intact.
- Capture inputs/outputs and usage metadata when available; apply truncation/redaction safeguards.
- On errors, record span failure data and rethrow the original error.
- For streaming providers, finish spans on completion, cancellation, and stream errors.

## 4) Validate trace behavior in your app

Validate in integration tests or a local smoke script:

- parent/child span relationships
- success + error span completion
- streaming completion/cancel/error terminal paths
- payload capture and limits
- provider-prefixed span types

Confirm telemetry is emitted through your configured Prefactor transport.

## 5) Harden for production usage

Before rollout, verify:

- instrumentation never crashes user requests
- spans finish exactly once
- secrets are redacted and payloads are bounded
- errors preserve original stack/type when rethrown

## Quick Reference

| Decision | Put it where |
| --- | --- |
| Reusable tracing/context helpers | `@prefactor/core` |
| Provider request/response mapping | your adapter package |
| Span lifecycle logic | `@prefactor/core` + thin wrapper calls |
| Provider-only middleware/wrappers | your adapter package |

## References

- Use `references/provider-package-checklist.md` for an implementation checklist.

## Common Mistakes

- Re-implementing tracing lifecycle per provider instead of reusing core.
- Using generic span names instead of provider-prefixed types.
- Capturing raw payloads without truncation/redaction.
- Swallowing provider errors after instrumentation.
