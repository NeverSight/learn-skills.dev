---
name: powerbi-modeling
description: Power BI semantic models - DAX measures, star schemas, relationships, RLS, and performance tuning via MCP. Use when creating data models, writing DAX, or configuring table relationships in Power BI.
---

# Power BI Modeling

Use this skill when the work is inside a Power BI semantic model rather than a generic SQL schema or spreadsheet.

## Activation Conditions

- Designing or cleaning up a star schema
- Creating or reviewing DAX measures
- Configuring relationships and cross-filter direction
- Implementing row-level security
- Auditing model health and performance

## Practical Workflow

1. Inspect the current model before changing anything.
2. Classify tables as dimension, fact, bridge, or helper tables.
3. Prefer explicit measures over implicit aggregation.
4. Keep relationships simple and single-direction unless the use case is proven.
5. Hide technical fields from report authors.

## MCP Reality

Power BI model tooling is host-specific. If your client exposes a Power BI modeling MCP server, inspect the available operations first and map them to the model areas you need: connections, tables, columns, measures, relationships, DAX queries, and security roles.

For Microsoft documentation, the Microsoft Learn MCP server is a good companion. Prefer:

- `microsoft_docs_search_by_product` with `power-bi`
- `microsoft_docs_fetch` for the final page

## References & Resources

### Documentation
- [STAR-SCHEMA](./references/STAR-SCHEMA.md) - Dimension and fact modeling guidance
- [RELATIONSHIPS](./references/RELATIONSHIPS.md) - Relationship patterns and cross-filter tradeoffs
- [MEASURES-DAX](./references/MEASURES-DAX.md) - DAX naming and measure design
- [PERFORMANCE](./references/PERFORMANCE.md) - High-impact optimization ideas
- [RLS](./references/RLS.md) - Row-level security patterns

### Scripts
- [Power BI Model Audit](./scripts/powerbi-model-audit.py) - Local audit helper for naming, documentation, and modeling smells

### Examples
- [Model Examples](./examples/model-examples.md) - Example modeling patterns and DAX structure

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [microsoft-development](../microsoft-development/SKILL.md) | Official Microsoft docs for Power BI capabilities and limits |
| [sql-development](../sql-development/SKILL.md) | Shape the upstream warehouse or SQL source feeding the model |
| [excel-sheet](../excel-sheet/SKILL.md) | Excel as a data source or export target |
