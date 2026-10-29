---
name: sap-cap
description: >
  Query @cap-js/mcp-server before writing CDS entities, types, aspects, services,
  or CAP service handlers. Triggers on schema and service files in db/ and srv/.
paths:
  - "**/db/**/*.cds"
  - "**/srv/**/*.cds"
  - "**/srv/**/*.js"
---

# CAP MCP-First Development

Before writing, modifying, debugging, or fixing CDS entities, service definitions,
or CAP service handlers, you MUST query the CAP MCP server and apply its guidance.

## Tools

Use `mcp__cap__*` tools — primarily `mcp__cap__search_docs` and `mcp__cap__search_model`.

## Workflow

1. **Query before coding** — call `mcp__cap__search_docs` for syntax, patterns, or conventions
2. **Trust MCP over training knowledge** — if guidance conflicts with what you know, follow MCP
3. **Prefer the simplest pattern** when MCP returns multiple valid approaches

## Scope

This skill covers:
- CDS entity definitions, types, aspects (`db/schema.cds`)
- Service definitions and projections (`srv/*.cds`)
- Service handlers, actions, functions, events (`srv/*.js`)
- CDS built-in types, key patterns, virtual fields

This skill does **not** cover CDS annotations (`@UI`, `@Common`, `@Capabilities`) or
Fiori Elements configuration — those belong to the `sap-fiori` skill.
