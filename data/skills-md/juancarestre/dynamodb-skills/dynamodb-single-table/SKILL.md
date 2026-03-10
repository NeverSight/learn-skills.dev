---
name: dynamodb-single-table
description: "Orchestrator for the DynamoDB single-table design pipeline. Use when the user wants to design a DynamoDB table end-to-end or is unsure which step to start with. Routes to the appropriate specialized skill: dynamodb-access-patterns, dynamodb-table-design, or dynamodb-query-interfaces."
---

# DynamoDB Single-Table Design Pipeline

This skill orchestrates a 3-step pipeline for designing and implementing a DynamoDB single-table design. Use it when the user wants the full workflow or needs guidance on which step to take next.

## Pipeline Overview

```
  Step 1                    Step 2                    Step 3
  ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
  │ Access Patterns   │ ──>  │ Table Design      │ ──>  │ Query Interfaces  │
  │                   │      │                   │      │                   │
  │ Elicit entities   │      │ Design PK/SK/GSI  │      │ Generate method   │
  │ & access patterns │      │ Map AP -> Query   │      │ signatures & types│
  │ Output: .md file  │      │ Output: .md file  │      │ Output: .md file  │
  └──────────────────┘      └──────────────────┘      └──────────────────┘
  Skill:                    Skill:                    Skill:
  dynamodb-access-patterns  dynamodb-table-design     dynamodb-query-interfaces
```

## Step 0: Detect Pipeline State

Before routing, check if the user's project already has pipeline artifacts. Search for files matching these patterns:

- `**/access-patterns.md` or `**/access_patterns.md`
- `**/table-design.md` or `**/table_design.md`
- `**/query-interfaces.md` or `**/query_interfaces.md`

Also check common locations:
- `docs/dynamodb/`
- `docs/`
- Project root

**Based on what exists:**

| Files Found | State | Action |
|---|---|---|
| None | Fresh start | Route to `dynamodb-access-patterns` |
| Access patterns only | Step 1 complete | Route to `dynamodb-table-design` with the file path |
| Access patterns + table design | Steps 1-2 complete | Route to `dynamodb-query-interfaces` with the file path |
| All three files | Pipeline complete | Ask if they want to add entities, modify, or review |
| Table design only (no access patterns) | Partial/legacy | Warn that access patterns should be documented; offer to backfill or continue to Step 3 |

Tell the user what you found:
```
I found existing DynamoDB design artifacts in your project:

  [x] Access Patterns: docs/dynamodb/access-patterns.md
  [x] Table Design:    docs/dynamodb/table-design.md
  [ ] Query Interfaces: (not found)

You're ready for Step 3. Should I generate the query interfaces from
your table design?
```

## How to Route

| User wants to... | Route to |
|---|---|
| Start designing from scratch | `dynamodb-access-patterns` |
| Define entities and how they'll be queried | `dynamodb-access-patterns` |
| Has access patterns, needs key design | `dynamodb-table-design` |
| Has a table design, needs code interfaces | `dynamodb-query-interfaces` |
| Add a new entity to an existing table | Start with `dynamodb-access-patterns` for the new entity, then continue the pipeline |
| Understand single-table design concepts | Answer directly using the concepts below |

## Core Concepts (Quick Reference)

### What is Single-Table Design?

All entity types live in ONE DynamoDB table. You pre-join related data into **item collections** (items sharing a partition key) so they can be fetched in a single `Query` call. This eliminates the need for joins and reduces network round-trips.

### When to Use Single-Table Design

- You need sub-30ms response times at any scale
- You have well-defined access patterns that won't change frequently
- You need to fetch multiple entity types in a single request
- You're building OLTP workloads (not analytics)

### When NOT to Use Single-Table Design

- Your access patterns are still evolving rapidly (early-stage startup)
- You use GraphQL with per-type resolvers (the resolver model negates single-query benefits)
- You need flexible ad-hoc queries (consider a relational database instead)

### Key Principles

1. **Access patterns first.** Never design keys without knowing your queries.
2. **Pre-join into item collections.** Related data shares a partition key.
3. **One table, generic key names.** Use `pk`/`sk` (not `userId`/`orderId`).
4. **GSIs for alternate access patterns.** Reuse before creating new ones (max 20).
5. **Composite sort keys for multi-field sorting.** Encode hierarchy in the SK.
6. **No Scans.** Every query must use a partition key. If you need Scan, redesign.
7. **Transactions for multi-item writes.** Ensure consistency across item collections.

## Artifacts Produced

By the end of the pipeline, the user will have 3 files:

| File | Content | Produced by |
|---|---|---|
| `access-patterns.md` | Entities, attributes, all read/write/delete patterns | `dynamodb-access-patterns` |
| `table-design.md` | PK/SK design, GSIs, access pattern -> query mapping | `dynamodb-table-design` |
| `query-interfaces.md` | Entity types, key builders, repository method signatures | `dynamodb-query-interfaces` |

These files serve as the specification for the implementation phase.
