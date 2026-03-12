---
name: litestar-openapi
description: Configure Litestar OpenAPI schema generation and documentation UX with `OpenAPIConfig`, route-level schema metadata, schema generation controls, operation customization, UI render plugins, and documentation endpoint strategy. Use when API contract and docs quality must be implemented or corrected, especially for request, auth, and metrics surfaces. Do not use for runtime business logic changes unrelated to schema or documentation.
---

# OpenAPI

## Execution Workflow

1. Decide whether OpenAPI should be enabled, restricted, or disabled for the app.
2. Set app-level `OpenAPIConfig` for title, version, docs endpoints, servers, tags, and render plugins.
3. Add route-level metadata deliberately: `summary`, `description`, `response_description`, `tags`, `security`, `operation_id`, `raises`, and `include_in_schema`.
4. Use schema-generation customization only when default model generation is insufficient.
5. Choose UI render plugins and endpoint paths intentionally for each environment.
6. Validate that generated docs match real request, auth, and metrics behavior.

## Core Rules

- Keep documentation truthful to runtime behavior.
- Centralize OpenAPI config at app construction.
- Use route-level metadata only where it improves clarity or correctness.
- Disable schema generation with `openapi_config=None` only when docs must not be exposed.
- Keep request, response, security, and metrics documentation aligned with the skills that own those runtime behaviors.
- Prefer current render-plugin configuration over legacy controller-style customization paths.
- Treat OpenAPI changes as API changes that require review.

## Decision Guide

- Use app-level `OpenAPIConfig` for global schema and docs endpoint strategy.
- Use route-level metadata when one operation differs from the app default.
- Use `operation_class` or schema customization only when built-in generation is insufficient.
- Use `include_in_schema=False` for internal or operational routes that should stay out of public docs.
- Use UI plugins when interactive docs are required; choose the plugin based on audience and deployment constraints.
- Use one of the bundled render plugins rather than hand-building docs pages unless the UI must be bespoke.

## Reference Files

Read only the sections you need:

- For schema generation, enabling/disabling docs, route-level metadata, and operation customization, read [references/schema-and-operations.md](references/schema-and-operations.md).
- For UI render plugins, docs endpoints, path customization, and offline/CDN considerations, read [references/ui-plugins-and-endpoints.md](references/ui-plugins-and-endpoints.md).

## Recommended Defaults

- Keep app title, version, and server metadata explicit.
- Use route-level descriptions and summaries sparingly but intentionally.
- Document security requirements where auth actually applies.
- Keep internal or noisy operational endpoints out of the public schema when appropriate.
- Prefer a single clear docs UI per environment unless multiple UIs solve a real need.

## Anti-Patterns

- Documenting contracts that runtime behavior does not actually support.
- Leaving stale examples, tags, or security docs after runtime changes.
- Overusing route-level overrides until the schema becomes inconsistent.
- Exposing internal routes in the schema without intent.
- Treating UI plugin choice as purely cosmetic when endpoint paths and asset loading matter operationally.
- Customizing schema generation before understanding the default output.

## Validation Checklist

- Confirm schema generation is enabled or disabled intentionally.
- Confirm public routes appear in the schema and internal-only routes are omitted where intended.
- Confirm request, response, auth, and metrics surfaces are documented consistently with runtime behavior.
- Confirm operation IDs, tags, and summaries are stable and useful.
- Confirm documented exceptions and security requirements match the real route behavior.
- Confirm chosen UI plugin paths and asset sources are correct for the deployment environment.
- Confirm generated JSON and YAML schema endpoints behave as expected.

## Cross-Skill Handoffs

- Use `litestar-requests`, `litestar-responses`, and `litestar-dto` when schema mismatches originate in transport modeling.
- Use `litestar-authentication` and `litestar-security` when security scheme docs must match auth backends and guard behavior.
- Use `litestar-metrics` when operational endpoints or metrics docs should be included or excluded intentionally.
- Use `litestar-testing` when schema and docs stability need regression coverage.

## Litestar References

- https://docs.litestar.dev/latest/usage/openapi/index.html
- https://docs.litestar.dev/latest/usage/openapi/schema_generation.html
- https://docs.litestar.dev/latest/usage/openapi/ui_plugins.html
