---
name: litestar-templating
description: Configure Litestar templating with `TemplateConfig`, Jinja/Mako/MiniJinja engines, file-or-string `Template` responses, request and CSRF-aware context, template callables, and custom engine integration. Use when implementing or fixing server-rendered HTML in Litestar. Do not use for static asset serving or pure JSON API endpoints.
---

# Templating

## Execution Workflow

1. Choose the template engine that matches the project and ensure the corresponding Litestar extra is installed.
2. Configure `template_config` with the right `TemplateConfig` shape: `directory`, `directory=[...]`, or `instance=...`.
3. Return `Template` responses with explicit `template_name` or `template_str` and a stable, minimal context mapping.
4. Use built-in request, CSRF, and URL helpers for presentation concerns; keep domain logic out of templates.
5. Register engine-wide callables or environment customization centrally through `engine_callback`.
6. Verify missing-template behavior, route/static URL generation, CSRF rendering, and HTML output in tests.

## Core Rules

- Register one template engine at the app level via `template_config`.
- Use `directory` or `directory=[...]` for normal file-based templates.
- Use `instance=` only when you intentionally own engine creation or loader/environment wiring.
- Do not combine `instance` with `directory`.
- Prefer `template_name` for normal pages and reusable fragments; use `template_str` only for small inline templates.
- Keep context string-keyed, explicit, and view-shaped rather than dumping service or ORM objects into the template.
- Keep custom template callables side-effect free and presentation-focused.
- Use Litestar URL helpers instead of hardcoding route or static asset paths in markup.
- Treat CSRF helpers as transport concerns and wire them only when CSRF protection is enabled.

## Decision Guide

- Match the existing project engine unless there is a clear reason to migrate.
- Use Jinja when the project wants the default Litestar path and broad ecosystem support.
- Use Mako or MiniJinja when the project already standardizes on those template syntaxes.
- Use multiple template directories only when lookup truly spans shared and feature-local templates.
- Use `instance=` when you need a custom environment, loader, or preconfigured engine object.
- Use `engine_callback` when the engine needs custom callables, globals, or centralized one-time setup.
- Implement a custom engine only when Jinja, Mako, and MiniJinja do not fit the project.

## Reference Files

Read only the sections you need:

- For engine selection, install extras, `TemplateConfig`, directory vs. instance setup, and engine access, read [references/engine-selection-and-setup.md](references/engine-selection-and-setup.md).
- For `Template` responses, file vs. string rendering, context shaping, request access, and CSRF inputs, read [references/template-responses-and-context.md](references/template-responses-and-context.md).
- For built-in template callables, registering custom callables, and implementing a custom engine protocol, read [references/template-callables-and-custom-engines.md](references/template-callables-and-custom-engines.md).

## Recommended Defaults

- Keep templates in dedicated directories with engine-specific suffixes such as `.jinja2`, `.mako`, or `.minijinja`.
- Pass small view models or explicit dictionaries to templates instead of raw persistence models when possible.
- Use `url_for` and `url_for_static_asset` inside templates for links and asset references.
- Use `csrf_input` for HTML forms and `csrf_token` only when the token must be embedded another way.
- Keep partials, layouts, and page templates separate so fragment rendering stays predictable.
- Reach for `template_str` mainly for very small fragments, prototyping, or HTMX-style inline responses.

## Anti-Patterns

- Mixing `directory` and `instance` in the same `TemplateConfig`.
- Treating templates as a place for business rules, permission checks, or database lookups.
- Returning large full-page HTML from inline `template_str` snippets.
- Passing large opaque objects into context when the template needs only a few fields.
- Hardcoding URLs for routes or static files in templates.
- Registering template callables ad hoc inside handlers instead of once through engine configuration.
- Following older custom-engine examples without checking the current protocol surface in the reference docs.

## Validation Checklist

- Confirm the correct Litestar engine extra is installed.
- Confirm `template_config` exists and uses a valid `directory` or `instance` configuration.
- Confirm template names resolve from the intended directory set and fail clearly when missing.
- Confirm context keys and request-dependent template values render as expected.
- Confirm CSRF helpers appear only when CSRF protection is configured.
- Confirm route and static asset URLs reverse correctly through template helpers.
- Confirm inline string templates are limited to cases where file-based templates would add unnecessary overhead.
- Confirm tests cover both full-page and fragment responses where applicable.

## Cross-Skill Handoffs

- Use `litestar-htmx` for fragment-oriented update flows and progressive enhancement.
- Use `litestar-responses` when response container behavior, headers, cookies, or status codes are the main concern.
- Use `litestar-static-files` when asset mounting and static URL behavior are part of the task.
- Use `litestar-security` when CSRF configuration or broader web security policy is the real issue.
- Use `litestar-testing` for client assertions on rendered HTML, redirects, and form flows.

## Litestar References

- https://docs.litestar.dev/latest/usage/templating.html
- https://docs.litestar.dev/latest/reference/template.html
