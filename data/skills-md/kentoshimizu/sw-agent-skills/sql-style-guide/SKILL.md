---
name: sql-style-guide
description: "Style, review, and refactoring standards for SQL schema, migration, and query artifacts. Trigger when `.sql` schema/query/migration artifacts are created, changed, or reviewed and SQL-specific quality rules (naming, migration safety, query clarity, and performance intent) must be enforced. Do not use for ORM-only code changes with no SQL artifacts, or for non-SQL data modeling documents. Use together with language-specific style guides only when both SQL and application code are modified."
---

# Sql Style Guide

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

Apply this checklist when writing or reviewing SQL.

## Trigger Reference

- Use `references/trigger-matrix.md` as the canonical trigger and co-activation matrix.
- Resolve skill activation from changed files with `python3 scripts/resolve_style_guides.py <changed-path>...` when automation is available.
- Validate trigger matrix consistency with `python3 scripts/validate_trigger_matrix_sync.py`.

## Schema and naming conventions
## Quality Gate Reference

- Use `references/quality-gate-command-matrix.md` for CI check-only vs local autofix command mapping.

1. Use consistent naming (`snake_case`) for tables, columns, indexes, and constraints.
2. Define clear primary keys and explicit foreign key constraints.
3. Use explicit column types; avoid ambiguous generic types where precision matters.
4. Replace unexplained literal values with named domain enums/tables when recurring.

## Query structure and readability

1. Use explicit column lists; avoid `SELECT *` in application-facing queries.
2. Use CTEs for complex logic to improve readability and reviewability.
3. Keep joins explicit with clear predicates and aliases.
4. Comment only non-obvious business rules embedded in SQL.

## Safety and correctness

1. Use parameterized statements; never concatenate untrusted input into SQL strings.
2. Scope `UPDATE`/`DELETE` with explicit predicates and safeguard large mutations.
3. Use transactions intentionally and document isolation-level-sensitive flows.
4. Handle nullability and default behavior explicitly.

## Migration discipline

1. Keep migrations atomic, reversible where possible, and deterministic.
2. Separate schema changes from data backfills when risk is high.
3. Backfill in batches for large tables to reduce lock contention.
4. Validate migration order and dependency assumptions in CI.

## Performance and scalability

1. Validate query plans (`EXPLAIN`/`EXPLAIN ANALYZE`) for critical queries.
2. Add/adjust indexes based on observed access patterns, not guesswork.
3. Avoid N+1 query patterns at application boundaries.
4. Use pagination/limits for large result sets.

## Security and compliance

1. Enforce least privilege per DB role.
2. Avoid exposing sensitive columns unless explicitly required.
3. Redact secrets/PII in logs and query traces.
4. Keep audit fields (`created_at`, `updated_at`, actor IDs) where required.

## Testing and verification

1. Add migration tests and rollback checks when rollback is supported.
2. Add query-level tests for business-critical logic.
3. Cover edge cases: null values, empty sets, timezone boundaries, duplicate keys.
4. Document manual verification steps for high-risk production migrations.

## Observability and operations

1. Capture slow query metrics and alert thresholds.
2. Log query failures with stable error categorization.
3. Monitor lock wait times, deadlocks, and replication lag where applicable.
4. Ensure runbooks exist for migration rollback or remediation.

## CI required quality gates (check-only)

1. Run SQL lint checks (`sqlfluff lint`, or project equivalent check-only command).
2. Run migration validation in CI/staging.
3. Verify critical query plans before merge.
4. Reject changes with unsafe mutation patterns or unbounded scans.

## Optional autofix commands (local)

1. Run `sqlfluff fix` (or project equivalent) and then re-run lint checks.
