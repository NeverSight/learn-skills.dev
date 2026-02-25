---
name: datafusion
description: 'DataFusion integration: logical/physical plans, execution context, table providers, schema memoization, and SQL handler routing. Keywords: DataFusion, Arrow, logical plan, physical plan, table provider, schema registry.'
---

Use this skill for work involving DataFusion, Arrow schemas, SQL planning/execution, and table providers.

Implementation guidance:
1) Use existing schema registry helpers for Arrow schema construction; memoize schemas where supported.
2) Implement or extend TableProvider with correct schema, statistics, and scan behavior.
3) Keep SQL handling in kalamdb-core/sql/executor and route through handler modules.
4) Use DataFusion’s logical plan for validation; avoid manual SQL parsing unless required.
5) Keep table/provider creation cheap; cache shared providers if appropriate.
6) Ensure column types map correctly to Arrow types and are consistent across writes and reads.

Best practices:
- Respect DataFusion’s async execution model; avoid blocking IO in scan/exec paths.
- Prefer predicate pushdown where the provider supports it.
- Align system tables with kalamdb-commons models and constants.

Pitfalls:
- Mismatched schema ordering or nullability between writer and provider.
- Unbounded in-memory collection during scans.
- Creating new providers per request when a shared instance is intended.
