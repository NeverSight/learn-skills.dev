---
name: database-architect
description: >-
  Design schemas, plan migrations, and optimize queries. Six modes from modeling
  to evolution. Use for database architecture. NOT for DBA ops, backups, or
  deployment (devops-engineer).
argument-hint: "<mode> [target]"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0"
---

# Database Architect

Schema design, migration planning, query optimization, and zero-downtime schema evolution.

**Scope:** Database architecture decisions only. NOT for DBA operations, backup management, deployment strategies (use devops-engineer), or vector DB patterns (use data-wizard).

## Dispatch

| $ARGUMENTS | Mode |
|------------|------|
| `design <requirements>` | Design: generate schema DDL from requirements |
| `migrate <description>` | Migrate: migration SQL with rollback plan |
| `review <schema or migration path>` | Review: audit existing schema or migration files |
| `optimize <query or table>` | Optimize: index and query optimization |
| `evolve` | Evolve: codebase-wide schema evolution analysis |
| Empty | Show mode menu with examples |

## Canonical Vocabulary

| Term | Definition |
|------|------------|
| **schema** | Complete DDL definition: tables, columns, constraints, indexes |
| **migration** | A versioned, reversible schema change with up/down operations |
| **zero-downtime** | Schema change that requires no application downtime (expand-contract) |
| **expand-contract** | Two-phase migration: expand (add new), contract (remove old) |
| **normalization level** | 1NF through 5NF classification of table structure |
| **index coverage** | Percentage of query patterns served by existing indexes |
| **data loss risk** | Whether a migration operation can destroy existing data |
| **backwards compatible** | Migration that works with both old and new application code |
| **hot path** | Query pattern executed at high frequency requiring optimization |
| **covering index** | Index containing all columns needed to satisfy a query |
| **partial index** | Index with a WHERE clause filtering indexed rows |
| **cardinality** | Number of distinct values in a column relative to total rows |

## Mode 1: Design

Generate schema DDL from natural language requirements.

### Design Step 1: Gather Requirements

Parse requirements from `$ARGUMENTS`. Identify:
- Entities and their relationships (1:1, 1:N, M:N)
- Required constraints (unique, not null, check, foreign key)
- Expected query patterns and access paths
- Target database engine (default: PostgreSQL)

### Design Step 2: Analyze Schema

Run schema analyzer for structural validation:
```
uv run python skills/database-architect/scripts/schema-analyzer.py --ddl <path_or_stdin>
```
Use for iterating on the design. Parse JSON output for normalization level and structural issues.

### Design Step 3: Generate DDL

Produce complete DDL with:
- Table definitions with appropriate types and constraints
- Indexes for declared query patterns
- Foreign key relationships with appropriate ON DELETE/UPDATE actions
- Comments on non-obvious design decisions

Read `references/normalization-guide.md` for normalization/denormalization decision rules.
Read `references/db-idioms.md` for engine-specific type and syntax choices.

### Design Step 4: Present

Output the DDL with a summary table:

| Table | Columns | Indexes | Foreign Keys | Normalization |
|-------|---------|---------|--------------|---------------|

Include rationale for denormalization decisions (if any).

## Mode 2: Migrate

Generate migration SQL with rollback plan and zero-downtime strategy.

### Migrate Step 1: Understand the Change

Parse migration description from `$ARGUMENTS`. Classify each operation:
```
uv run python skills/database-architect/scripts/migration-validator.py --path <migration_dir>
```

Read `references/migration-patterns.md` for zero-downtime strategies per operation type.

### Migrate Step 2: Generate Migration

For each operation, produce:
- **Up migration**: forward SQL
- **Down migration**: rollback SQL
- **Zero-downtime strategy**: if the operation is not backwards-compatible
- **Data loss risk**: flag destructive operations explicitly

Use expand-contract pattern for:
- Column renames (add new, copy, drop old)
- Column type changes (add new, backfill, drop old)
- NOT NULL additions (add with default, backfill, add constraint)
- Table renames (create new, migrate references, drop old)

### Migrate Step 3: Validate

Run migration validator on generated SQL:
```
uv run python skills/database-architect/scripts/migration-validator.py --sql <path>
```

Flag any operations with `data_loss_risk: true` or `reversible: false`.

### Migrate Step 4: Present

Output migration with sections: Up, Down, Zero-Downtime Notes, Risk Assessment.

## Mode 3: Review

Audit existing schema or migration files for quality and safety.

### Review Step 1: Read Target

Read the schema or migration files at the path in `$ARGUMENTS`.

### Review Step 2: Analyze

Run schema analyzer:
```
uv run python skills/database-architect/scripts/schema-analyzer.py --ddl <path>
```

Check against:
- Normalization issues (references/normalization-guide.md)
- Missing indexes for common query patterns
- Constraint completeness (foreign keys, NOT NULL, defaults)
- Naming convention consistency
- Engine-specific anti-patterns (references/db-idioms.md)

For migration files, also run:
```
uv run python skills/database-architect/scripts/migration-validator.py --path <dir>
```

Check against:
- Reversibility of each operation
- Data loss risk
- Zero-downtime compatibility
- Migration ordering and dependencies

### Review Step 3: Present Findings

Group findings by severity:
- **Critical**: data loss risk, missing constraints on foreign keys, irreversible migrations without rollback
- **Warning**: missing indexes, denormalization without justification, suboptimal types
- **Info**: naming inconsistencies, missing comments, style suggestions

## Mode 4: Optimize

Index and query optimization recommendations.

### Optimize Step 1: Gather Context

Read the query or table definition from `$ARGUMENTS`. Identify:
- Current indexes on involved tables
- Query execution pattern (point lookup, range scan, join, aggregation)
- Data volume estimates if available

### Optimize Step 2: Analyze

Run index recommender:
```
uv run python skills/database-architect/scripts/index-recommender.py --schema <path> --queries <path_or_stdin>
```

Read `references/query-optimization.md` for optimization patterns.
Read `references/db-idioms.md` for engine-specific index capabilities.

### Optimize Step 3: Present Recommendations

For each recommendation:
- **Table**: affected table
- **Recommended index**: column list and type
- **Rationale**: which query pattern this serves
- **Trade-off**: write overhead and storage cost
- **Estimated impact**: qualitative (high/medium/low)

## Mode 5: Evolve

Codebase-wide schema evolution analysis.

### Evolve Step 1: Discover

Scan the codebase for:
- Schema definition files (SQL, ORM models, migration directories)
- Query patterns (raw SQL, ORM queries, query builders)
- Migration history and ordering

Use Grep and Glob to find schema-related files.

### Evolve Step 2: Analyze Evolution

Assess:
- Schema drift between ORM models and actual migrations
- Unused tables/columns (defined but never queried)
- Migration health (reversibility, ordering, gaps)
- Index coverage across query patterns
- Normalization consistency

### Evolve Step 3: Present Report

Output an evolution report with:
- Schema health score (tables, indexes, constraints coverage)
- Migration timeline summary
- Top recommendations ranked by impact
- Render dashboard for visual overview:
  Copy `templates/dashboard.html` to a temporary file, inject analysis JSON into the data script tag, open in browser.

## Reference Files

Load ONE reference at a time. Do not preload all references.

| File | Content | Read When |
|------|---------|-----------|
| `references/migration-patterns.md` | Zero-downtime strategies, expand-contract, operation safety | Migrate mode |
| `references/normalization-guide.md` | Normalization levels, denormalization decision rules | Design mode, Review mode |
| `references/db-idioms.md` | PostgreSQL, MySQL, SQLite, MongoDB type idioms and features | Design mode, Optimize mode |
| `references/query-optimization.md` | Index strategies, query rewriting, explain plan interpretation | Optimize mode |
| `references/zero-downtime-checklist.md` | Pre-migration checklist, deployment coordination | Migrate mode |

| Script | When to Run |
|--------|-------------|
| `scripts/schema-analyzer.py` | Design (validation), Review (analysis) |
| `scripts/migration-validator.py` | Migrate (validation), Review (migration audit) |
| `scripts/index-recommender.py` | Optimize (recommendations) |

| Template | When to Render |
|----------|----------------|
| `templates/dashboard.html` | Evolve mode — inject schema analysis JSON |

## Critical Rules

1. Every migration must have a rollback plan — no irreversible changes without explicit user acknowledgment
2. Never recommend dropping columns/tables without confirming data preservation strategy
3. Always flag data loss risk explicitly — silent destructive operations are unacceptable
4. Zero-downtime means schema-level compatibility, NOT deployment coordination (that is devops-engineer)
5. Default to PostgreSQL when no engine is specified — state the assumption
6. Every index recommendation must include write overhead trade-off
7. Do not generate ORM code — output raw DDL/SQL only
8. Normalization decisions must cite the specific normal form and violation
9. Run schema-analyzer.py or migration-validator.py before presenting results — do not rely on LLM analysis alone
10. Never copy honest-review's wave pipeline, confidence scoring, or team structure — this is a generator skill
11. Always present before executing — approval gate before any schema modification
12. Migration naming must follow `NNNN_description` convention (sequential, descriptive)
