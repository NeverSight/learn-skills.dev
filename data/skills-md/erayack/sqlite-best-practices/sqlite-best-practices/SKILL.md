---
name: sqlite-best-practices
description: SQLite performance optimization, configuration, and best practices. Use this skill when writing, reviewing, or optimizing SQLite queries, schema designs, or database configurations.
license: MIT
metadata:
  author: Eray Acikgoz
  version: "1.0.0"
  date: February 2026
  abstract: Comprehensive SQLite performance optimization guide. Contains rules across key categories like Configuration (Pragmas), Query Performance, and Schema Design. Each rule includes detailed explanations, incorrect vs. correct SQL examples, and performance impacts.
---

# SQLite Best Practices

Comprehensive performance optimization guide for SQLite. Contains rules across multiple categories, prioritized by impact to guide automated query optimization, schema design, and runtime configuration.

## When to Apply

Reference these guidelines when:
- Configuring SQLite for production (WAL mode, timeouts)
- Designing schemas (Strict tables, data types)
- Optimizing queries and indexes
- Working with JSON or Full Text Search in SQLite
- Managing concurrency and transactions
- Designing backup and replication strategies

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Configuration & Pragmas | CRITICAL | `config-` |
| 2 | Query Performance | CRITICAL | `query-` |
| 3 | Operations & Distributed | HIGH | `ops-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Data Access Patterns | MEDIUM | `data-` |
| 6 | JSON & Advanced | LOW | `json-` / `fts-` / `advanced-` |

## How to Use

Read individual rule files for detailed explanations and SQL examples:

```
references/config-wal-mode.md
references/query-indexes.md
references/ops-continuous-wal.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect SQL/Config example with explanation
- Correct SQL/Config example with explanation
- Performance metrics or impacts

## References

- https://www.sqlite.org/docs.html (Official Documentation)
- https://www.sqlite.org/syntaxdiagrams.html (Railroad Diagrams - Highly recommended for syntax)
- https://www.sqlite.org/pragma.html (Pragma Cheatsheet)
- https://www.sqlite.org/wal.html (Write-Ahead Logging)
