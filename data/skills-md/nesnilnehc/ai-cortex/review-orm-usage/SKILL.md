---
name: review-orm-usage
description: Review ORM usage patterns for N+1 queries, connection management, migration safety, transaction handling, and query efficiency. Library-level atomic skill; output is a findings list.
tags: [eng-standards, optimization]
version: 1.0.0
license: MIT
related_skills: [review-diff, review-codebase, review-code, review-sql, review-performance]
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review orm, orm review]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review ORM Usage

## Purpose

Review **ORM usage patterns** at the **library level** only. Do not define scope (diff vs codebase) or perform security/architecture analysis; those are handled by scope and cognitive skills. Emit a **findings list** in the standard format for aggregation. Focus on N+1 query detection, connection management, migration safety, transaction handling, query efficiency, and model design across ORM libraries (Prisma, Entity Framework, SQLAlchemy, Sequelize, TypeORM, Hibernate, Django ORM, ActiveRecord, etc.).

---

## Core Objective

**Primary Goal**: Produce an ORM usage findings list covering N+1 queries, connection management, migration safety, transaction handling, query efficiency, and model design for the given code scope.

**Success Criteria** (ALL must be met):

1. ✅ **ORM library-only scope**: Only ORM usage patterns are reviewed; no scope selection, security, or architecture analysis performed
2. ✅ **All six ORM dimensions covered**: N+1, connections, migrations, transactions, query efficiency, and model design are assessed where relevant
3. ✅ **Findings format compliant**: Each finding includes Location, Category (`library-orm`), Severity, Title, Description, and optional Suggestion
4. ✅ **File/model references**: All findings reference specific file:line or model/entity name
5. ✅ **ORM-agnostic**: Findings apply across ORM libraries; specific library is referenced only for context

**Acceptance Test**: Does the output contain an ORM-focused findings list with file/model references covering all relevant library dimensions without performing security, architecture, or scope analysis?

---

## Scope Boundaries

**This skill handles**:

- N+1 query detection (eager vs lazy loading, include/join patterns, batch loading, data loader patterns)
- Connection management (pool configuration, connection leaks, timeout handling, connection reuse)
- Migration safety (backwards-compatible migrations, zero-downtime deployment, data vs schema migration, rollback strategy)
- Transaction handling (transaction scope, isolation levels, nested transactions, deadlock prevention)
- Query efficiency (unnecessary SELECT *, missing indexes hinted by query patterns, raw query fallback, query complexity)
- Model design (proper relations, cascade behavior, soft delete patterns, audit columns, index declarations)

**This skill does NOT handle**:

- Scope selection — scope is provided by the caller
- Security analysis (SQL injection, sensitive data exposure) — use `review-security`
- Architecture analysis (module boundaries, coupling) — use `review-architecture`
- Raw SQL quality (syntax, portability, parameterization) — use `review-sql`
- General performance analysis (algorithmic complexity, I/O cost) — use `review-performance`
- Full orchestrated review — use `review-code`

**Handoff point**: When all ORM findings are emitted, hand off to `review-code` for aggregation. For SQL injection risks (unsanitized raw queries), note them and suggest `review-security`. For complex raw SQL quality, note and suggest `review-sql`.

---

## Use Cases

- **Orchestrated review**: Used as the library step when [review-code](../review-code/SKILL.md) runs scope → language → framework → library → cognitive for projects using an ORM.
- **ORM-only review**: When the user wants only ORM usage patterns checked across their data layer.
- **Pre-PR ORM checklist**: Ensure N+1 queries, transaction handling, and migration safety are correct before merge.
- **Migration review**: Focused check on migration files for backwards-compatibility and rollback safety.

**When to use**: When the code under review uses an ORM library and the task includes library-level quality. Scope is determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: ORM usage patterns in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection, security review, or architecture review; do not review non-ORM files for ORM rules unless in scope.

### Review checklist (ORM library only)

1. **N+1 query detection**: Identify lazy-loading patterns that trigger N+1 queries; check for eager loading (include/join), batch loading, or data loader patterns; flag loops that issue individual queries per iteration.
2. **Connection management**: Verify pool configuration (min/max, idle timeout); detect potential connection leaks (unreturned connections, missing dispose/close); check timeout and retry settings; confirm connection reuse in request-scoped contexts.
3. **Migration safety**: Assess backwards-compatibility (additive-only vs destructive changes); check for zero-downtime deployment readiness (no table locks on large tables, no NOT NULL without default); verify data migration is separated from schema migration; confirm rollback strategy exists.
4. **Transaction handling**: Evaluate transaction scope (too broad or too narrow); check isolation levels for correctness; detect nested transaction misuse (savepoints vs flat); flag potential deadlock patterns (inconsistent lock ordering, long-held locks).
5. **Query efficiency**: Flag unnecessary `SELECT *` or over-fetching columns; identify query patterns that hint at missing indexes (unindexed WHERE/ORDER BY columns); evaluate raw query fallback appropriateness; assess query complexity (deep joins, subqueries in loops).
6. **Model design**: Verify proper relation declarations (one-to-many, many-to-many, polymorphic); check cascade behavior (unintended cascade delete); review soft delete implementation; confirm audit columns (createdAt, updatedAt) where expected; check index declarations on frequently queried fields.

### Tone and references

- **Professional and technical**: Reference specific locations (file:line or model/entity name). Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) containing ORM code (models, migrations, repositories, queries). Provided by the user or scope skill.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **library-orm**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform scope selection, security, or architecture review. Stay within ORM library usage patterns.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** review non-ORM code for ORM-specific rules unless explicitly in scope.
- **Do not** duplicate raw SQL analysis that belongs to `review-sql`; flag ORM-generated query issues only.

### Skill Boundaries

**Do NOT do these** (other skills handle them):

- Do NOT select or define the code scope — scope is determined by the caller or `review-code`
- Do NOT perform security analysis (SQL injection, data exposure) — use `review-security`
- Do NOT perform architecture analysis (module boundaries, coupling) — use `review-architecture`
- Do NOT perform raw SQL syntax or portability review — use `review-sql`
- Do NOT perform general algorithmic performance analysis — use `review-performance`

**When to stop and hand off**:

- When all ORM findings are emitted, hand off to `review-code` for aggregation
- When SQL injection risks are found (e.g. unsanitized interpolation in raw queries), note them and suggest `review-security`
- When raw SQL quality issues are found (syntax, portability), note them and suggest `review-sql`
- When the user needs a full review (scope + language + cognitive), redirect to `review-code`

---

## Self-Check

### Core Success Criteria

- [ ] **ORM library-only scope**: Only ORM usage patterns are reviewed; no scope selection, security, or architecture analysis performed
- [ ] **All six ORM dimensions covered**: N+1, connections, migrations, transactions, query efficiency, and model design are assessed where relevant
- [ ] **Findings format compliant**: Each finding includes Location, Category (`library-orm`), Severity, Title, Description, and optional Suggestion
- [ ] **File/model references**: All findings reference specific file:line or model/entity name
- [ ] **ORM-agnostic**: Findings apply across ORM libraries; specific library is referenced only for context

### Process Quality Checks

- [ ] Was only the ORM library dimension reviewed (no scope/security/architecture)?
- [ ] Are N+1, connections, migrations, transactions, query efficiency, and model design covered where relevant?
- [ ] Is each finding emitted with Location, Category=library-orm, Severity, Title, Description, and optional Suggestion?
- [ ] Are issues referenced with file:line or model/entity name?

### Acceptance Test

Does the output contain an ORM-focused findings list with file/model references covering all relevant library dimensions without performing security, architecture, or scope analysis?

---

## Examples

### Example 1: N+1 query in a loop

- **Input**: Controller or service that fetches a list of orders, then iterates to access `order.customer` without eager loading.
- **Expected**: Emit a finding (major) for N+1 query pattern; suggest eager loading via include/join (e.g. Prisma `include`, EF `Include`, SQLAlchemy `joinedload`, Hibernate `@EntityGraph`). Category = library-orm.

### Example 2: Destructive migration without rollback

- **Input**: Migration that drops a column or renames a table without a corresponding down/rollback migration and without a data preservation step.
- **Expected**: Emit a finding (critical) for destructive migration without rollback strategy; suggest additive migration pattern (add new column → backfill → switch reads → drop old). Category = library-orm.

### Edge case: Raw query fallback in ORM context

- **Input**: Repository method using raw SQL (`prisma.$queryRaw`, `DbContext.Database.ExecuteSqlRaw`, `session.execute(text(...))`) for a query that could be expressed with the ORM query builder.
- **Expected**: Emit a finding (suggestion) noting that the raw query bypasses ORM type safety and migration tracking; suggest using the ORM query builder if the query is expressible. If the raw query is justified (performance, unsupported feature), accept it but flag the lack of parameterization if present and suggest `review-security` for injection risk. Category = library-orm.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` or model/entity name (optional line or range). |
| **Category** | `library-orm`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `src/services/OrderService.ts:42`
- **Category**: library-orm
- **Severity**: major
- **Title**: N+1 query on Order.customer relation
- **Description**: Each order triggers a separate query to fetch the customer. With 100 orders this produces 101 queries instead of 2.
- **Suggestion**: Use eager loading (e.g. Prisma `include: { customer: true }`, EF `.Include(o => o.Customer)`) or batch the customer lookup.
```
