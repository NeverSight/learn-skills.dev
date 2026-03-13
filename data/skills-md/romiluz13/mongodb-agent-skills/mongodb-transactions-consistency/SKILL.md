---
name: mongodb-transactions-consistency
description: MongoDB transaction correctness, consistency, and retry safety. Use when implementing multi-document writes, debugging transaction failures, choosing readConcern/writeConcern, handling TransientTransactionError or UnknownTransactionCommitResult, or deciding when transactions are required. Triggers on "transaction", "withTransaction", "session", "read concern", "write concern", "causal consistency", "snapshot", "retry commit", "ACID", "TransientTransactionError", and "UnknownTransactionCommitResult".
license: Apache-2.0
metadata:
  author: mongodb
  version: "1.2.0"
---

# MongoDB Transactions and Consistency

Transaction and consistency guidance for MongoDB, maintained by MongoDB. Contains **20 rules across 5 categories**, prioritized by correctness risk. This skill is intentionally non-overlapping with schema and query/index skills: it focuses on **atomicity, isolation, durability, retries, and consistency semantics**.

## When to Apply

Reference these guidelines when:
- Implementing multi-document writes that must succeed or fail together
- Choosing read concern / write concern for correctness guarantees
- Handling transaction retry errors in application code
- Diagnosing commit uncertainty and rollback risk
- Running transactions on replica sets or sharded clusters
- Designing idempotent business workflows with retries
- Reviewing whether a workload actually needs a transaction

## Non-Overlap Boundaries

- **Schema shape decisions** remain in `mongodb-schema-design`.
- **Index/query performance tuning** remains in `mongodb-query-and-index-optimize`.
- **Vector/hybrid search patterns** remain in `mongodb-ai`.
- This skill covers **correctness semantics and transaction-safe execution patterns**.

## Rule Categories by Priority

| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Transaction Fundamentals | CRITICAL | `fundamental-` | 5 |
| 2 | Consistency Semantics | HIGH | `consistency-` | 4 |
| 3 | Retry and Error Handling | CRITICAL | `retry-` | 4 |
| 4 | Operational Constraints | HIGH | `ops-` | 4 |
| 5 | Implementation Patterns | MEDIUM | `pattern-` | 3 |

## Quick Reference

### 1. Transaction Fundamentals (CRITICAL) - 5 rules

- `fundamental-use-transactions-when-required` - Use transactions for multi-document atomicity, not single-document writes
- `fundamental-propagate-session` - Pass the same session to every operation in a transaction
- `fundamental-one-transaction-per-session` - Run only one active transaction per session
- `fundamental-primary-read-preference` - Use primary read preference inside transactions
- `fundamental-commit-write-concern` - Set commit durability explicitly where business-critical

### 2. Consistency Semantics (HIGH) - 4 rules

- `consistency-read-concern-levels` - Choose local, majority, or snapshot intentionally
- `consistency-snapshot-majority-coupling` - Understand snapshot visibility requirements
- `consistency-causal-majority-pairing` - Pair majority read+write for causal guarantees
- `consistency-rollback-risk` - Avoid weak concern combinations for critical workflows

### 3. Retry and Error Handling (CRITICAL) - 4 rules

- `retry-transient-transaction-error` - Retry full transaction on transient transaction errors
- `retry-unknown-commit-result` - Retry commit safely when commit result is unknown
- `retry-transaction-too-large-cache` - Handle TransactionTooLargeForCache as a redesign signal
- `retry-upsert-duplicate-key-81` - Know retry behavior changes around duplicate-key upserts (7.0.22+, 8.0.11+, 8.1+)

### 4. Operational Constraints (HIGH) - 4 rules

- `ops-transaction-runtime-limit` - Keep transactions short and below lifetime limits
- `ops-lock-timeout-tuning` - Tune lock wait timeout for transactional lock acquisition
- `ops-restricted-operations` - Avoid unsupported operations inside transactions
- `ops-sharded-caveats` - Apply sharded-cluster transaction caveats explicitly

### 5. Implementation Patterns (MEDIUM) - 3 rules

- `pattern-withtransaction-vs-core-api` - Choose callback API vs core API intentionally
- `pattern-idempotent-transaction-body` - Make transaction bodies idempotent under retries
- `pattern-observability` - Instrument transaction outcomes and retry paths

## Key Principle

> **"Transactions are a correctness tool, not a default coding pattern."**

Single-document writes are already atomic in MongoDB. Use transactions when business invariants span documents, collections, or shards.

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/fundamental-use-transactions-when-required.md
rules/retry-unknown-commit-result.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect and correct code examples
- When NOT to use the pattern
- Verification checks and diagnostics

---

## How These Rules Work

### Recommendations with Verification

Every rule in this skill provides:
1. **A recommendation** for correctness-safe behavior
2. **A verification checklist** for deployment reality
3. **Commands to verify** before implementation
4. **MCP-friendly checks** when connected

### Why Verification Matters

I can reason about transaction semantics, but cannot infer your SLA, failure budget, or deployment topology without evidence. Always validate with your workload and cluster shape.

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

### Action Policy

**I will NEVER execute write operations without your explicit approval.**

| Operation Type | MCP Tools | Action |
|---------------|-----------|--------|
| **Read (Safe)** | `find`, `aggregate`, `explain`, `serverStatus`, `currentOp` | I may run automatically to verify |
| **Write (Requires Approval)** | `update`, `insert`, `delete`, `commitTransaction` | I will show the command and wait for your "yes" |
| **Destructive (Requires Approval)** | `drop`, `dropDatabase` | I will warn you and require explicit confirmation |

---

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
