---
name: mongodb-schema-design
description: MongoDB schema design patterns and anti-patterns. Use when designing data models, reviewing schemas, migrating from SQL, or troubleshooting performance issues caused by schema problems. Triggers on "design schema", "embed vs reference", "MongoDB data model", "schema review", "unbounded arrays", "one-to-many", "tree structure", "16MB limit", "schema validation", "JSON Schema", "time series", "schema migration", "polymorphic", "TTL", "data lifecycle", "archive", "index explosion", "unnecessary indexes", "approximation pattern", "document versioning".
license: Apache-2.0
metadata:
  author: mongodb
  version: "2.3.0"
---

# MongoDB Schema Design

Data modeling patterns and anti-patterns for MongoDB, maintained by MongoDB. Contains **33 rules across 5 categories**, prioritized by impact. Bad schema is the root cause of most MongoDB performance and cost issues—queries and indexes cannot fix a fundamentally wrong model.

## When to Apply

Reference these guidelines when:
- Designing a new MongoDB schema from scratch
- Migrating from SQL/relational databases to MongoDB
- Reviewing existing data models for performance issues
- Troubleshooting slow queries or growing document sizes
- Deciding between embedding and referencing
- Modeling relationships (one-to-one, one-to-many, many-to-many)
- Implementing tree/hierarchical structures
- Seeing Atlas Schema Suggestions or Performance Advisor warnings
- Hitting the 16MB document limit
- Adding schema validation to existing collections

## Rule Categories by Priority

| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Schema Anti-Patterns | CRITICAL | `antipattern-` | 7 |
| 2 | Schema Fundamentals | HIGH | `fundamental-` | 5 |
| 3 | Relationship Patterns | HIGH | `relationship-` | 6 |
| 4 | Design Patterns | MEDIUM | `pattern-` | 12 |
| 5 | Schema Validation | MEDIUM | `validation-` | 3 |

## Quick Reference

### 1. Schema Anti-Patterns (CRITICAL) - 7 rules

- `antipattern-unbounded-arrays` - Never allow arrays to grow without limit
- `antipattern-bloated-documents` - Keep documents under 16KB for working set
- `antipattern-massive-arrays` - Arrays over 1000 elements hurt performance
- `antipattern-unnecessary-collections` - Fewer collections, more embedding
- `antipattern-excessive-lookups` - Reduce $lookup by denormalizing
- `antipattern-schema-drift` - Enforce consistent structure across documents
- `antipattern-unnecessary-indexes` - Audit and remove unused or redundant indexes

### 2. Schema Fundamentals (HIGH) - 5 rules

- `fundamental-embed-vs-reference` - Decision framework for relationships
- `fundamental-data-together` - Data accessed together stored together
- `fundamental-document-model` - Embrace documents, avoid SQL patterns
- `fundamental-schema-validation` - Enforce structure with JSON Schema
- `fundamental-16mb-awareness` - Design around BSON document limit

### 3. Relationship Patterns (HIGH) - 6 rules

- `relationship-one-to-one` - Embed for simplicity, reference for independence
- `relationship-one-to-few` - Embed bounded arrays (addresses, phone numbers)
- `relationship-one-to-many` - Reference for large/unbounded relationships
- `relationship-one-to-squillions` - Reference massive child sets, store summaries
- `relationship-many-to-many` - Two-way referencing for bidirectional access
- `relationship-tree-structures` - Parent/child/materialized path patterns

### 4. Design Patterns (MEDIUM) - 12 rules

- `pattern-archive` - Move historical data to separate storage for performance
- `pattern-attribute` - Collapse many optional fields into key-value attributes
- `pattern-bucket` - Group time-series or IoT data into buckets
- `pattern-time-series-collections` - Use native time series collections when available
- `pattern-extended-reference` - Cache frequently-accessed related data
- `pattern-subset` - Store hot data in main doc, cold data elsewhere
- `pattern-computed` - Pre-calculate expensive aggregations
- `pattern-outlier` - Handle documents with exceptional array sizes
- `pattern-polymorphic` - Store heterogeneous documents with a type discriminator
- `pattern-schema-versioning` - Evolve schemas safely with version fields

### 5. Schema Validation (MEDIUM) - 3 rules

- `validation-json-schema` - Validate data types and structure at database level
- `validation-action-levels` - Choose warn vs error mode for validation
- `validation-rollout-strategy` - Introduce validation safely in production

## Key Principle

> **"Data that is accessed together should be stored together."**

This is MongoDB's core philosophy. Embedding related data eliminates joins, reduces round trips, and enables atomic updates. Reference only when you must.

## Decision Framework

| Relationship | Cardinality | Access Pattern | Recommendation |
|-------------|-------------|----------------|----------------|
| One-to-One | 1:1 | Always together | Embed |
| One-to-Few | 1:N (N < 100) | Usually together | Embed array |
| One-to-Many | 1:N (N > 100) | Often separate | Reference |
| Many-to-Many | M:N | Varies | Two-way reference |

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/antipattern-unbounded-arrays.md
rules/relationship-one-to-many.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- "When NOT to use" exceptions
- Performance impact and metrics
- Verification diagnostics

---

## How These Rules Work

### Recommendations with Verification

Every rule in this skill provides:
1. **A recommendation** based on best practices
2. **A verification checklist** of things that should be confirmed
3. **Commands to verify** so you can check before implementing
4. **MCP integration** for automatic verification when connected

### Why Verification Matters

I analyze code patterns, but I can't see your actual data without a database connection.
This means I might suggest:
- Fixing an "unbounded array" that's actually small and bounded
- Restructuring a schema that works well for your access patterns
- Adding validation when documents already conform to the schema

**Always verify before implementing.** Each rule includes verification commands.

### MongoDB MCP Integration

For automatic verification, connect the [MongoDB MCP Server](https://github.com/mongodb-js/mongodb-mcp-server):

**Option 1: Connection String**
```json
{
  "mcpServers": {
    "mongodb": {
      "command": "npx",
      "args": ["-y", "mongodb-mcp-server", "--readOnly"],
      "env": {
        "MDB_MCP_CONNECTION_STRING": "mongodb+srv://user:pass@cluster.mongodb.net/mydb"
      }
    }
  }
}
```

**Option 2: Local MongoDB**
```json
{
  "mcpServers": {
    "mongodb": {
      "command": "npx",
      "args": ["-y", "mongodb-mcp-server", "--readOnly"],
      "env": {
        "MDB_MCP_CONNECTION_STRING": "mongodb://localhost:27017/mydb"
      }
    }
  }
}
```

**⚠️ Security**: Use `--readOnly` for safety. Remove only if you need write operations.

When connected, I can automatically:
- Infer schema via `mcp__mongodb__collection-schema`
- Measure document/array sizes via `mcp__mongodb__aggregate`
- Check collection statistics via `mcp__mongodb__db-stats`

### ⚠️ Action Policy

**I will NEVER execute write operations without your explicit approval.**

| Operation Type | MCP Tools | Action |
|---------------|-----------|--------|
| **Read (Safe)** | `find`, `aggregate`, `collection-schema`, `db-stats`, `count` | I may run automatically to verify |
| **Write (Requires Approval)** | `update-many`, `insert-many`, `create-collection` | I will show the command and wait for your "yes" |
| **Destructive (Requires Approval)** | `delete-many`, `drop-collection`, `drop-database` | I will warn you and require explicit confirmation |

When I recommend schema changes or data modifications:
1. I'll explain **what** I want to do and **why**
2. I'll show you the **exact command**
3. I'll **wait for your approval** before executing
4. If you say "go ahead" or "yes", only then will I run it

**Your database, your decision.** I'm here to advise, not to act unilaterally.

### Working Together

If you're not sure about a recommendation:
1. Run the verification commands I provide
2. Share the output with me
3. I'll adjust my recommendation based on your actual data

We're a team—let's get this right together.

---

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
