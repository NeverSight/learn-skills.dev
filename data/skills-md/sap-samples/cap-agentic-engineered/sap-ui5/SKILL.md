---
name: sap-ui5
description: >
  Query @ui5/mcp-server before writing SAPUI5 controllers, XML views, control
  APIs, or model bindings. Triggers on views and controller extensions in app/.
paths:
  - "**/app/**/*.xml"
  - "**/app/**/ext/**/*.js"
  - "**/app/**/ext/**/*.ts"
---

# UI5 MCP-First Development

Before writing, modifying, debugging, or fixing SAPUI5 controllers, XML views,
or control bindings, you MUST query the UI5 MCP server and apply its guidance.

## Tools

Use `mcp__ui5__*` tools — primarily `mcp__ui5__get_api_reference`, `mcp__ui5__get_guidelines`,
`mcp__ui5__run_ui5_linter`, and `mcp__ui5__get_project_info`.

## Workflow

1. **Query before coding** — call `mcp__ui5__get_api_reference` for control APIs, or `mcp__ui5__get_guidelines` for project-level patterns
2. **Trust MCP over training knowledge** — if guidance conflicts with what you know, follow MCP
3. **Run the linter after changes** — call `mcp__ui5__run_ui5_linter` to catch deprecated APIs
4. **Prefer the simplest pattern** when MCP returns multiple valid approaches

## Scope

This skill covers:
- XML views with `sap.m`, `sap.f`, `sap.uxap` namespaces
- Controller extensions (`app/**/ext/controller/*.js`)
- Model bindings, formatters, event handlers
- Control APIs and property configuration

## UI5 Code Standards

- XML views only — no JavaScript views
- `sap.ui.define` for all modules — no globals
- Async loading: `data-sap-ui-async="true"`
- i18n for all user-facing text
- No deprecated APIs (`jQuery.sap.*`, sync loading, `sap.ui.getCore()`)
- Fiori Elements controller extensions must be plain objects (not ES6 classes) — `this` refers to the `ExtensionAPI` instance
