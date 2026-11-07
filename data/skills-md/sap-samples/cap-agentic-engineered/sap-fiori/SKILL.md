---
name: sap-fiori
description: >
  Query @sap-ux/fiori-mcp-server before writing CDS annotations, Fiori Elements
  config, or manifest.json. Triggers on annotation files in app/ and manifests.
paths:
  - "**/app/**/*.cds"
  - "**/app/**/manifest.json"
---

# Fiori MCP-First Development

Before writing, modifying, debugging, or fixing CDS annotations, Fiori Elements
page configuration, or manifest.json, you MUST query the Fiori MCP server and apply its guidance.

## Tools

Use `mcp__fiori__*` tools — primarily `mcp__fiori__search_docs`, `mcp__fiori__list_functionality`,
`mcp__fiori__get_functionality_details`, and `mcp__fiori__execute_functionality`.

## Workflow

1. **Query before coding** — call `mcp__fiori__search_docs` for annotation patterns, floorplan config, or manifest structure
2. **Trust MCP over training knowledge** — if guidance conflicts with what you know, follow MCP
3. **Use Fiori MCP tooling for modifications** — before manually editing manifest.json or annotations, check if `mcp__fiori__list_functionality` provides an automated function
4. **Prefer the simplest pattern** when MCP returns multiple valid approaches

## Scope

This skill covers:
- CDS annotations: `@UI`, `@Common`, `@Capabilities`, `@Communication`
- Fiori Elements floorplans: List Report, Object Page, Analytical List Page
- `manifest.json` configuration: routing, data sources, control configuration
- Custom actions in manifest (`controlConfiguration.actions`)

## Fiori Elements App Rules

When creating or modifying SAP Fiori Elements applications:

- The application typically starts with a **List Report** page showing the base entity in a table. Row details are shown in an **ObjectPage** based on the same entity.
- An ObjectPage can contain table sections based on to-many associations. Row details in a table section can open another ObjectPage based on the association's target entity.
- The data model must have one main entity with navigation properties to related entities.
- Each property must have a proper datatype.
- For all entities, provide primary keys of type **UUID**.
- When creating sample data in CSV files, all primary keys and foreign keys **MUST** be in UUID format (e.g., `550e8400-e29b-41d4-a716-446655440001`).
- When modifying the application (e.g., adding columns), do **not** use screen personalization — modify the project code. Always check whether `mcp__fiori__list_functionality` provides a suitable function first.
- When previewing, use the most specific `npm run watch-*` script for the app in `package.json`.
