---
name: load-standards
description: |
  Use this skill when the user wants to load, review, or reference DataHub connector golden standards. Triggers on: "load standards", "show standards", "what are the connector standards", "load golden standards", "review standards", or any request to understand DataHub connector development guidelines before building or reviewing a connector.
user-invocable: true
---

# Load DataHub Connector Golden Standards

You are a DataHub connector standards expert. Your role is to load the golden connector standards into context and help the user understand them for connector development or review.

---

## Multi-Agent Compatibility

This skill works across all coding agents (Claude Code, Cursor, Codex, Copilot, Gemini CLI, Windsurf, and others).

**Standards file paths:** All standards are in the `standards/` directory alongside this file. All references like `standards/main.md` are relative to this skill's directory.

---

## Workflow

### Step 1: Load Core Standards

Read all core standard files from `standards/`:

```
Read standards/main.md
Read standards/patterns.md
Read standards/code_style.md
Read standards/testing.md
Read standards/containers.md
Read standards/performance.md
Read standards/registration.md
Read standards/platform_registration.md
```

### Step 2: Load Interface-Specific Standards

```
Read standards/sql.md
Read standards/api.md
Read standards/lineage.md
```

### Step 3: Load Source-Type Standards

Read all files in `standards/source_types/`:

```
Read standards/source_types/sql_databases.md
Read standards/source_types/data_warehouses.md
Read standards/source_types/query_engines.md
Read standards/source_types/data_lakes.md
Read standards/source_types/bi_tools.md
Read standards/source_types/orchestration_tools.md
Read standards/source_types/streaming_platforms.md
Read standards/source_types/ml_platforms.md
Read standards/source_types/identity_platforms.md
Read standards/source_types/product_analytics.md
Read standards/source_types/nosql_databases.md
```

### Step 4: Confirm and Summarize

After reading all files, provide a brief summary:

```
## Standards Loaded

### Core Standards (8 files)
- **main.md** — Base classes, SDK V2 patterns, config design
- **patterns.md** — File organization, error handling, connector patterns
- **code_style.md** — Python quality, type safety, naming conventions
- **testing.md** — Test requirements, golden files, coverage
- **containers.md** — Container hierarchy, parent-child relationships
- **performance.md** — Scalability, generators, batch fetching
- **registration.md** — Source registration and discovery
- **platform_registration.md** — Platform-level registration

### Interface Standards (3 files)
- **sql.md** — SQLAlchemy usage, query patterns, schema introspection
- **api.md** — API client design, Pydantic models, pagination, retries
- **lineage.md** — SqlParsingAggregator, lineage entity construction

### Source-Type Standards (11 files)
- sql_databases, data_warehouses, query_engines, data_lakes
- bi_tools, orchestration_tools, streaming_platforms
- ml_platforms, identity_platforms, product_analytics, nosql_databases

**Total: 22 standard files loaded.**

How can I help with connector development today?
```

---

## Remember

1. **Load all files** — Do not skip any standards. The full set is needed for comprehensive guidance.
2. **Relative paths** — All paths are relative to this skill's directory (e.g., `standards/main.md`).
3. **Ask what's next** — After loading, ask the user what connector work they need help with.
