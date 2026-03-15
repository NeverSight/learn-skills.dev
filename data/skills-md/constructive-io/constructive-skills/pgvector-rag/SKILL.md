---
name: pgvector-rag
description: pgvector setup, embeddings, similarity search, RAG pipelines, Ollama integration, and agentic-kit RAG. Use when asked to "set up vector database", "generate embeddings", "semantic search", "build RAG", "use Ollama", "run local LLM", "configure RAG", "create AI search", "embed documents", or when building any RAG or vector search application with PostgreSQL.
compatibility: Node.js 18+, PostgreSQL with pgvector, Ollama, pgpm CLI
metadata:
  author: constructive-io
  version: "2.0.0"
---

# pgvector & RAG

Complete toolkit for building vector search and RAG (Retrieval-Augmented Generation) applications with PostgreSQL. Covers pgvector schema setup, embedding generation with Ollama, similarity search, full RAG pipelines, and agentic-kit integration.

## When to Apply

Use this skill when:
- **Setting up pgvector:** Creating tables, indexes, vector storage schema
- **Generating embeddings:** Using Ollama to embed documents and chunks
- **Similarity search:** Querying vectors with cosine/L2/inner product distance
- **Building RAG:** Combining retrieval with LLM generation
- **Ollama integration:** Local LLM inference, model management, streaming
- **Agentic-kit RAG:** Wiring RAG into agentic-kit chat applications

## Architecture

```
Document → Chunking → Embedding → pgvector Storage
                                        ↓
Query → Embedding → Similarity Search → Context Retrieval → LLM Response
```

## Quick Start

```bash
# 1. Start PostgreSQL with pgvector
pgpm docker start
eval "$(pgpm env)"

# 2. Pull Ollama models
ollama pull nomic-embed-text
ollama pull llama3.2

# 3. Create vector storage module
pgpm init my-vectors
cd my-vectors
pgpm add schemas/intelligence
pgpm add schemas/intelligence/tables/documents --requires schemas/intelligence
pgpm add schemas/intelligence/tables/chunks --requires schemas/intelligence/tables/documents
```

## Schema Design

### Documents Table

```sql
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

```sql
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

### Similarity Search Function

```sql
CREATE FUNCTION intelligence.find_similar_chunks(
    p_embedding VECTOR(768),
    p_limit INTEGER DEFAULT 5,
    p_similarity_threshold FLOAT DEFAULT 0.7
)
RETURNS TABLE (
    id INTEGER,
    content TEXT,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.content,
        1 - (c.embedding <=> p_embedding) AS similarity
    FROM intelligence.chunks c
    WHERE c.embedding IS NOT NULL
      AND 1 - (c.embedding <=> p_embedding) > p_similarity_threshold
    ORDER BY c.embedding <=> p_embedding
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;
```

## Embedding Models

| Model | Dimensions | Speed | Quality |
|-------|------------|-------|---------|
| `nomic-embed-text` | 768 | Fast | Good |
| `mxbai-embed-large` | 1024 | Medium | Better |
| `all-minilm` | 384 | Very Fast | Acceptable |

## Distance Operators

| Operator | Type | Use Case |
|----------|------|----------|
| `<=>` | Cosine | Most common, normalized vectors |
| `<->` | Euclidean (L2) | When magnitude matters |
| `<#>` | Inner product | Dot product similarity |

## TypeScript: OllamaClient

```typescript
import fetch from 'cross-fetch';

export class OllamaClient {
  private baseUrl: string;

  constructor(baseUrl?: string) {
    this.baseUrl = baseUrl || process.env.OLLAMA_HOST || 'http://localhost:11434';
  }

  async generateEmbedding(text: string, model = 'nomic-embed-text'): Promise<number[]> {
    const response = await fetch(`${this.baseUrl}/api/embeddings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model, prompt: text }),
    });
    if (!response.ok) throw new Error(`Embedding failed: ${response.statusText}`);
    const data = await response.json();
    return data.embedding;
  }

  async generateResponse(prompt: string, context?: string, model = 'mistral'): Promise<string> {
    const fullPrompt = context
      ? `Context: ${context}\n\nQuestion: ${prompt}\n\nAnswer:`
      : prompt;
    const response = await fetch(`${this.baseUrl}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model, prompt: fullPrompt, stream: false }),
    });
    if (!response.ok) throw new Error(`Generation failed: ${response.statusText}`);
    const data = await response.json();
    return data.response;
  }
}
```

## Vector Format

pgvector expects bracket notation:

```typescript
const formatVector = (embedding: number[]): string => `[${embedding.join(',')}]`;
```

## RAG Query Pattern

```typescript
// 1. Embed the question
const queryEmbedding = await ollama.generateEmbedding(question);

// 2. Retrieve context
const result = await pool.query(
  `SELECT string_agg(content, E'\n\n') as context
   FROM intelligence.find_similar_chunks($1::vector, $2)`,
  [formatVector(queryEmbedding), 5]
);

// 3. Generate response with context
const response = await ollama.generateResponse(question, result.rows[0].context);
```

## Indexes for Performance

```sql
-- IVFFlat (good balance, add after initial data load)
CREATE INDEX idx_chunks_embedding ON intelligence.chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- HNSW (better recall, more memory)
CREATE INDEX idx_chunks_embedding_hnsw ON intelligence.chunks
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `RAG_DATABASE_URL` | - | PostgreSQL connection string |
| `RAG_EMBEDDING_MODEL` | `nomic-embed-text` | Embedding model |
| `RAG_CHAT_MODEL` | `llama3.2` | Chat model |
| `RAG_SIMILARITY_THRESHOLD` | `0.5` | Minimum similarity score |
| `RAG_CONTEXT_LIMIT` | `5` | Max chunks to retrieve |

## Troubleshooting Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| "type vector does not exist" | pgvector extension not installed; use pgvector-enabled Docker image |
| "Connection refused" to Ollama | Start Ollama: `ollama serve` |
| "Model not found" | Pull model: `ollama pull <model>` |
| Dimension mismatch | Ensure VECTOR(n) matches model output dimensions |
| No results returned | Lower similarity threshold |
| Slow queries | Add IVFFlat or HNSW index |

## Reference Guide

Consult these reference files for detailed documentation on specific topics:

| Reference | Topic | Consult When |
|-----------|-------|--------------|
| [references/setup.md](references/setup.md) | pgvector schema setup | Creating tables, indexes, vector dimensions, pgpm module structure |
| [references/embeddings.md](references/embeddings.md) | Generating and storing embeddings | OllamaClient, document chunking, ingestion pipeline, batch processing |
| [references/similarity-search.md](references/similarity-search.md) | Similarity search queries | Distance operators, thresholds, metadata filtering, performance tuning |
| [references/rag-pipeline.md](references/rag-pipeline.md) | Complete RAG pipeline | RAGService implementation, streaming, chat history, prompt engineering |
| [references/ollama.md](references/ollama.md) | Ollama integration | Installation, API endpoints, model selection, chat API, CI/CD setup |
| [references/agentic-kit.md](references/agentic-kit.md) | Agentic-kit RAG | RAGProvider, createRAGKit, useAgent hook, environment config, database schema |

## Cross-References

Related skills (separate from this skill):
- `graphile-pgvector` — Integrate pgvector with PostGraphile v5 GraphQL
- `pgpm` (`references/docker.md`) — PostgreSQL container management for pgvector
- `github-workflows-ollama` — GitHub Actions for Ollama and pgvector testing
