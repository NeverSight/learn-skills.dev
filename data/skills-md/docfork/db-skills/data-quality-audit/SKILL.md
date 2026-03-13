---
name: data-quality-audit
description: Audits database data quality (nulls, duplicates, orphans, invalid ranges) and produces a short findings report with remediation queries. Use when debugging data issues, validating migrations, or verifying analytics correctness.
---

# Data Quality Audit

## Quick Start

Goal: find correctness issues quickly and return a small, actionable report.

## When to use this skill

- bug reports that smell like data drift (missing rows, double counts, weird nulls)
- after migrations/backfills to prove invariants still hold
- when analytics numbers disagree between systems

## Before you run checks

- database engine
- target tables + expected primary keys
- expected invariants (unique, not null, fk relationships, allowed ranges)
- performance constraints (large tables, peak hours)

## Workflow (default)

1. pick 1–3 core tables for the issue
2. run cheap checks first (nulls, duplicates on keys)
3. run relationship checks (orphans)
4. run domain checks (ranges, enums)
5. write a short findings report + safe remediation plan

## Core checks (portable sql)

### null checks

```sql
SELECT COUNT(*) AS null_count
FROM your_table
WHERE important_col IS NULL;
```

### duplicates on a candidate key

```sql
SELECT key_col, COUNT(*) AS c
FROM your_table
GROUP BY key_col
HAVING COUNT(*) > 1
ORDER BY c DESC
LIMIT 50;
```

### orphan rows (broken references)

```sql
SELECT COUNT(*) AS orphan_count
FROM child c
LEFT JOIN parent p ON p.id = c.parent_id
WHERE c.parent_id IS NOT NULL
  AND p.id IS NULL;
```

### invalid ranges

```sql
SELECT COUNT(*) AS bad_count
FROM your_table
WHERE amount < 0;
```

### time sanity (example)

```sql
SELECT COUNT(*) AS bad_count
FROM your_table
WHERE created_at > NOW();
```

## Performance-safe tips

- always start with `count(*)` + targeted where clauses
- add `limit` when inspecting example rows
- scope by time window if tables are huge (last 7/30 days)
- prefer indexed predicates (id ranges, created_at) for sampling

## Remediation patterns

### fix duplicates

- decide on a canonical row rule (latest by updated_at, highest priority status, etc.)
- write a deterministic dedupe query
- add a unique constraint or unique index after cleanup

### fix orphans

- pick policy: delete orphans, reattach to parent, or set fk to null
- add fk constraint after data is corrected

### fix nulls

- backfill from source columns or defaults
- add not null only after verification

## Output format (copy/paste)

```markdown
## data quality audit

### scope

- tables:
- time window:

### findings

- [severity] issue: evidence

### likely impact

- user impact:
- analytics impact:

### remediation

- step 1:
- step 2:

### verification

- query checks:
```
