---
name: pgvector-setup
description: Set up pgvector for vector storage in PostgreSQL. Use when asked to "set up vector database", "configure pgvector", "create embedding tables", "set up semantic search", or when building RAG applications with PostgreSQL.
compatibility: PostgreSQL 13+ with pgvector extension, pgpm CLI
metadata:
  author: constructive-io
  version: "1.0.0"
---

# pgvector Setup

Set up PostgreSQL with pgvector for storing and querying vector embeddings. This is the foundation for building RAG (Retrieval-Augmented Generation) applications.

## When to Apply

Use this skill when:
- Setting up vector storage for embeddings
- Creating tables to store document embeddings
- Building semantic search functionality
- Implementing RAG pipelines with PostgreSQL
- Migrating from other vector databases to PostgreSQL

## Prerequisites

pgvector must be available in your PostgreSQL instance. Use one of these Docker images:

| Image | Description |
|-------|-------------|
| `pyramation/postgres:17` | PostgreSQL 17 with pgvector (recommended) |
| `ghcr.io/constructive-io/docker/postgres-plus:17` | PostgreSQL 17 with pgvector and additional extensions |

## Quick Start

### 1. Start PostgreSQL with pgvector

Ensure PostgreSQL is running with a pgvector-enabled image (see `pgpm-docker` skill) and PG env vars are loaded (see `pgpm-env` skill).

### 2. Create Schema and Tables

Create a pgpm module for your vector storage:

```bash
pgpm init my-vectors
cd my-vectors
pgpm add schemas/intelligence
pgpm add schemas/intelligence/tables/documents --requires schemas/intelligence
pgpm add schemas/intelligence/tables/chunks --requires schemas/intelligence/tables/documents
```

## Schema Design

### Documents Table

Store full documents with their embeddings:

```sql
-- deploy/schemas/intelligence/tables/documents.sql
-- Deploy: schemas/intelligence/tables/documents
-- requires: schemas/intelligence

CREATE TABLE intelligence.documents (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    embedding VECTOR(768),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Chunks Table

Store document chunks for granular retrieval:

```sql
-- deploy/schemas/intelligence/tables/chunks.sql
-- Deploy: schemas/intelligence/tables/chunks
-- requires: schemas/intelligence/tables/documents

CREATE TABLE intelligence.chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES intelligence.documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding VECTOR(768),
    chunk_index INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_chunks_document_id ON intelligence.chunks(document_id);
```

### Chat History Table (Optional)

Track conversation history for RAG sessions:

```sql
-- deploy/schemas/intelligence/tables/chat_history.sql
CREATE TABLE intelligence.chat_history (
    id SERIAL PRIMARY KEY,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_chat_history_session ON intelligence.chat_history(session_id);
```

## Vector Dimensions

Choose dimensions based on your embedding model:

| Model | Dimensions | Use Case |
|-------|------------|----------|
| `nomic-embed-text` | 768 | General purpose, good balance |
| `all-MiniLM-L6-v2` | 384 | Lightweight, fast |
| `text-embedding-ada-002` | 1536 | OpenAI, high quality |
| `text-embedding-3-small` | 1536 | OpenAI, newer model |

Declare the dimension in your VECTOR type:

```sql
embedding VECTOR(768)   -- For nomic-embed-text
embedding VECTOR(1536)  -- For OpenAI models
```

## Indexes for Performance

### IVFFlat Index (Recommended for Most Cases)

Good balance of speed and accuracy:

```sql
-- Create after inserting initial data
CREATE INDEX idx_chunks_embedding ON intelligence.chunks 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

The `lists` parameter should be approximately `sqrt(num_rows)`.

### HNSW Index (Better Recall)

Higher memory usage but better recall:

```sql
CREATE INDEX idx_chunks_embedding_hnsw ON intelligence.chunks 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

## Revert Scripts

Always include revert scripts for pgpm:

```sql
-- revert/schemas/intelligence/tables/documents.sql
DROP TABLE IF EXISTS intelligence.documents;

-- revert/schemas/intelligence/tables/chunks.sql
DROP TABLE IF EXISTS intelligence.chunks;
```

## Verify Scripts

Confirm deployment succeeded:

```sql
-- verify/schemas/intelligence/tables/documents.sql
DO $$
BEGIN
  PERFORM 1 FROM pg_tables 
  WHERE schemaname = 'intelligence' AND tablename = 'documents';
  IF NOT FOUND THEN
    RAISE EXCEPTION 'Table intelligence.documents does not exist';
  END IF;
END $$;
```

## Complete Module Structure

```text
my-vectors/
├── deploy/
│   └── schemas/
│       └── intelligence/
│           ├── schema.sql
│           └── tables/
│               ├── documents.sql
│               ├── chunks.sql
│               └── chat_history.sql
├── revert/
│   └── schemas/
│       └── intelligence/
│           ├── schema.sql
│           └── tables/
│               ├── documents.sql
│               ├── chunks.sql
│               └── chat_history.sql
├── verify/
│   └── schemas/
│       └── intelligence/
│           ├── schema.sql
│           └── tables/
│               ├── documents.sql
│               ├── chunks.sql
│               └── chat_history.sql
├── pgpm.plan
└── package.json
```

## Deploying

```bash
pgpm deploy --database myapp_dev --createdb --yes
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "type vector does not exist" | pgvector extension not installed; use a pgvector-enabled image |
| "dimension mismatch" | Embedding dimension doesn't match VECTOR(n) declaration |
| Slow queries | Add IVFFlat or HNSW index after initial data load |
| Out of memory | Reduce HNSW parameters or use IVFFlat instead |

## References

- Related skill: `pgvector-embeddings` for generating and storing embeddings
- Related skill: `pgvector-similarity-search` for querying vectors
- Related skill: `rag-pipeline` for complete RAG implementation
- [pgvector documentation](https://github.com/pgvector/pgvector)
