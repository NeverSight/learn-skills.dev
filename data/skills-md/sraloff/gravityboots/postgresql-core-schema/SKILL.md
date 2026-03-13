---
name: postgresql-core-schema
description: PostgreSQL-specific schema design, types, and DDL patterns.
---

# PostgreSQL Core & Schema

## When to use this skill
- Creating or modifying PostgreSQL tables (DDL).
- Working with JSONB, Arrays, or specialized Postgres types.
- Creating triggers or functions (PL/pgSQL).

## 1. Data Types
- **Timestamps**: Always use `timestamptz` (Timestamp with Time Zone), rarely `timestamp` (without TZ).
- **Text**: Use `text` instead of `varchar(n)` unless a strict limit is architecturally required.
- **JSON**: Use `jsonb` (binary) for storage and indexing, not `json`.
- **Primary Keys**: `bigint GENERATED ALWAYS AS IDENTITY` or `uuid` (v4/v7).

## 2. Constraints & Integrity
- **Check Constraints**: Use `CHECK` constraints generously (e.g., `CHECK (price > 0)`).
- **Foreign Keys**: Index all FK columns manually (Postgres does not auto-index them).
- **Exclusion Constraints**: Use where `UNIQUE` is not enough (e.g., non-overlapping time ranges).

## 3. Advanced Features
- **Triggers**: Use for audit logs or complex data consistency that cannot be enforced by constraints.
- **Partitions**: Consider declarative partitioning for massive time-series tables.
- **Enumerations**: Use Native Enums for strict, infrequently changing sets; otherwise use a reference table.
