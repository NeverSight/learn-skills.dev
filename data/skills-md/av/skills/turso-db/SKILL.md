---
name: turso-db
description: Install, configure, and work with Turso DB — an in-process SQLite-compatible relational database engine written in Rust. Use when the user needs to (1) install Turso DB, (2) create or query databases with the tursodb CLI shell, (3) use Turso from JavaScript/Node.js via @tursodatabase/database, (4) work with vector search or embeddings in Turso, (5) set up full-text search with FTS indexes, (6) configure transactions including MVCC concurrent transactions, (7) enable encryption at rest, or (8) use Change Data Capture (CDC) for audit logging.
---

# Turso DB

Turso is an in-process relational database engine aiming for full SQLite compatibility. Unlike client-server databases, it runs in your application's memory space with sub-microsecond read/write latencies.

## Installation

```bash
# Via installer script
curl --proto '=https' --tlsv1.2 -LsSf \
  https://github.com/tursodatabase/turso/releases/latest/download/turso_cli-installer.sh | sh

# Via Homebrew
brew install turso
```

## Quick Start

```console
$ tursodb                        # transient in-memory database
$ tursodb mydata.db              # persistent database file
```

```sql
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
INSERT INTO users VALUES (1, 'Alice', 'alice@example.com');
SELECT * FROM users;
```

## Core SQL

Standard SQLite-compatible SQL. See [references/sql-reference.md](references/sql-reference.md) for full statement syntax (CREATE/ALTER/DROP TABLE, INSERT, SELECT, UPDATE, DELETE, transactions).

Key differences from SQLite:
- No multi-process/multi-threading access
- No savepoints, triggers, or vacuum
- Views experimental (behind `--experimental-views` flag)
- UTF-8 only

## JavaScript API

Install and use from Node.js:

```bash
npm i @tursodatabase/database        # native
npm i @tursodatabase/database --cpu wasm32  # WASM
```

```javascript
import { connect } from '@tursodatabase/database';
const db = await connect('turso.db');
const row = db.prepare('SELECT 1').get();
```

See [references/javascript-api.md](references/javascript-api.md) for details.

## Vector Search

Store embeddings and perform similarity search using built-in vector functions.

```sql
CREATE TABLE docs (id INTEGER PRIMARY KEY, content TEXT, embedding BLOB);
INSERT INTO docs VALUES (1, 'ML basics', vector32('[0.2, 0.5, 0.1]'));

SELECT content, vector_distance_cos(embedding, vector32('[0.3, 0.4, 0.2]')) AS dist
FROM docs ORDER BY dist LIMIT 5;
```

Supports: `vector32`, `vector64`, `vector32_sparse`, `vector8`, `vector1bit`.
Distance functions: `vector_distance_cos`, `vector_distance_l2`, `vector_distance_dot`, `vector_distance_jaccard`.

See [references/vector-search.md](references/vector-search.md) for all vector types, functions, and examples.

## Full-Text Search (Experimental)

Tantivy-powered FTS with BM25 scoring. Requires `fts` feature at compile time.

```sql
CREATE INDEX fts_idx ON articles USING fts (title, body)
WITH (weights = 'title=2.0,body=1.0');

SELECT title, fts_score(title, body, 'database') as score
FROM articles
WHERE fts_match(title, body, 'database')
ORDER BY score DESC LIMIT 10;
```

See [references/full-text-search.md](references/full-text-search.md) for tokenizers, query syntax, and highlighting.

## Advanced Features

See [references/advanced-features.md](references/advanced-features.md) for:

- **Journal modes**: WAL (default) and experimental MVCC (`PRAGMA journal_mode = experimental_mvcc`)
- **Encryption**: AES-GCM / AEGIS cipher support with `--experimental-encryption` flag
- **CDC**: Real-time change tracking via `PRAGMA unstable_capture_data_changes_conn('full')`
- **Index methods**: Custom data access methods (experimental, `--experimental-index-method`)
- **C API**: SQLite C API subset with Turso extensions
