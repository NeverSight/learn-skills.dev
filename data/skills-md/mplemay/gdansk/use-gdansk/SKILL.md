---
name: use-gdansk
description: Comprehensive gdansk implementation and debugging guide for MCP app UIs. Use when adding or fixing Amber and FastMCP tool UIs, wiring `@amber.tool(..., page=...)` to React `views/apps/**/page.tsx` or `page.jsx` entries, enabling SSR, configuring metadata or `cache_html`, adding the PostCSS plugin, mounting under FastAPI, or diagnosing gdansk bundling and runtime errors.
---

# Use Gdansk

Use this workflow for all gdansk work. Follow the steps in order and use the linked references for exact templates and
edge cases.

## 1) Classify the request

Map the request to one primary workflow before coding:

1. Add a new tool UI:
   - Register or update a Python tool.
   - Map it to a React page with `@amber.tool(..., page=...)`.
2. Fix a broken gdansk UI:
   - Resolve page path validation errors.
   - Resolve missing bundle output or SSR runtime errors.
3. Add advanced integration:
   - Enable SSR globally or per tool.
   - Add metadata or disable cache.
   - Add PostCSS plugin handling.
   - Mount inside FastAPI.

If the user asks for multiple outcomes, implement one complete path first, then layer additional changes.

## 2) Validate project layout and dependencies first

Fail early on structure before writing feature code.

- Confirm the views root exists and contains `apps/`.
- Confirm each UI entry point is `views/apps/**/page.tsx` or `views/apps/**/page.jsx`.
- Confirm each page component has a default export.
- Confirm `views/package.json` has:
  - `"type": "module"`
  - `"@modelcontextprotocol/ext-apps"`
  - `"react"` and `"react-dom"`

Use [quickstart.md](references/quickstart.md) for the canonical baseline layout and minimum files.

## 3) Implement tool and page wiring with strict path rules

Always treat `page=` as a logical path under `views/apps/`, never an absolute filesystem path.

- Prefer directory shorthand (`page=Path("hello")`) when the page entry file is conventional.
- Use explicit file form only for disambiguation (`page=Path("hello/page.tsx")`).
- Never prefix the `page` argument with `apps/`.
- Never include `.` or `..` traversal segments.
- Keep the path relative.

Use [page-contract-and-tool-wiring.md](references/page-contract-and-tool-wiring.md) for accepted/rejected inputs and
`ui://` URI mapping behavior.

## 4) Apply optional integrations only when requested

Choose the smallest integration needed:

- SSR:
  - Global default: `Amber(..., ssr=True)`.
  - Per-tool override: `@amber.tool(..., ssr=True|False)`.
- HTML cache:
  - Default cached by fingerprint.
  - Disable via `Amber(..., cache_html=False)` when SSR output must be uncached per request.
- Metadata:
  - Set global metadata on `Amber`.
  - Override per tool with shallow top-level merge semantics.
- FastAPI:
  - Mount `mcp_app` and run its lifespan.
  - Use `streamable_http_path="/"` in `FastMCP` when mounted.
- PostCSS:
  - Add `PostCSS()` plugin.
  - Ensure `postcss-cli` is installed under `views/node_modules/.bin`.

Use [integration-options.md](references/integration-options.md) for exact implementation shapes.

## 5) Verify and diagnose before finishing

After implementation:

1. Start server in dev mode and confirm bundle output appears under `views/.gdansk/`.
2. Open or fetch the UI resource and confirm rendered HTML includes client script.
3. For SSR paths, confirm server bundle exists and hydration path is correct.
4. For CSS changes, confirm generated CSS is present and transformed.

If anything fails, match the exact error string and follow [troubleshooting.md](references/troubleshooting.md).

## Guardrails

- Do not invent alternative page conventions (for example `app.tsx`); gdansk expects `page.tsx` or `page.jsx`.
- Do not pass filesystem-absolute paths to `@amber.tool(page=...)`.
- Do not use `apps/...` as the decorator input prefix.
- Do not enable SSR without checking that the page has a default export and that dependencies are SSR-compatible.
- Do not add PostCSS plugin without installing CLI dependencies in the views package.

## Reference map

- Baseline templates and run commands: [quickstart.md](references/quickstart.md)
- Strict page contract and URI behavior: [page-contract-and-tool-wiring.md](references/page-contract-and-tool-wiring.md)
- SSR, metadata, FastAPI, PostCSS options: [integration-options.md](references/integration-options.md)
- Error-driven diagnosis: [troubleshooting.md](references/troubleshooting.md)
