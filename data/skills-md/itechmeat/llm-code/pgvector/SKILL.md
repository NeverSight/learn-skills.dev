---
name: pgvector
description: "pgvector Postgres extension. Covers vector types, distance operators, indexing (HNSW/IVFFlat), and client library usage. Use when storing vectors in PostgreSQL, running nearest-neighbor searches, or configuring HNSW/IVFFlat indexes. Keywords: pgvector, PostgreSQL, vector search, HNSW, IVFFlat."
metadata:
  version: "0.8.2"
  release_date: "2026-02-25"
---

# pgvector

PostgreSQL extension for storing vectors and running exact/approximate nearest-neighbor search in SQL.

## Quick Navigation

- Installation: `references/installation.md`
- Core concepts and SQL recipes: `references/core.md`
- Indexing (HNSW / IVFFlat) and tuning: `references/indexing.md`
- Filtering, iterative scans, and performance: `references/performance-and-filtering.md`
- Types and functions reference (vector/halfvec/bit/sparsevec): `references/types-and-functions.md`
- Troubleshooting: `references/troubleshooting.md`
- Client libraries (priority):
  - Python: `references/python.md`
  - Go: `references/go.md`
  - Node (JS/TS): `references/node.md`
  - Java: `references/java.md`
  - Swift: `references/swift.md`

## When to Use

- You need vector similarity search inside Postgres (keep vectors with relational data).
- You want SQL-native ANN indexes (HNSW or IVFFlat) with tunable recall/speed.
- You want consistent patterns to store/query embeddings across multiple application languages.

## Quick Start (already installed)

Prerequisite: pgvector is installed on the Postgres server. See: `references/installation.md`.

Enable per database and run a first query:

```sql
CREATE EXTENSION vector;

CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');

SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;
```

### Choosing distance operators

- L2 (Euclidean): use `<->`
- Inner product: use `<#>` (note: returns negative inner product)
- Cosine distance: use `<=>`
- L1: use `<+>`
- Binary vectors: Hamming `<~>` / Jaccard `<%>`

### Indexing rules of thumb

- Exact search: no pgvector index; may use parallel scan on large tables.
- ANN search:
  - Prefer HNSW for better speed/recall, higher build time/memory.
  - Use IVFFlat when you need faster builds/lower memory.
- Create one index per distance function/operator class you plan to use.

## Critical Prohibitions / Gotchas

- Approximate indexes can change results (recall vs speed).
- Index usage typically requires `ORDER BY <distance-op> ... LIMIT ...`.
- `<#>` returns negative inner product; multiply by `-1` to get the actual value.
- `NULL` vectors are not indexed; for cosine distance, zero vectors are not indexed.

## Links

- Docs / repo: https://github.com/pgvector/pgvector
- Client libs:
  - Python: https://github.com/pgvector/pgvector-python
  - Go: https://github.com/pgvector/pgvector-go
  - Node: https://github.com/pgvector/pgvector-node
  - Java: https://github.com/pgvector/pgvector-java
  - Swift: https://github.com/pgvector/pgvector-swift
- Releases/tags: https://github.com/pgvector/pgvector/tags
