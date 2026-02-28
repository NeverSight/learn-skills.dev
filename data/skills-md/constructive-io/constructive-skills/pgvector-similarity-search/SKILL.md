---
name: pgvector-similarity-search
description: Perform semantic similarity search with pgvector. Use when asked to "search similar documents", "find related content", "semantic search", "vector search", or when implementing the retrieval phase of RAG pipelines.
compatibility: PostgreSQL with pgvector, embeddings already stored in database
metadata:
  author: constructive-io
  version: "1.0.0"
---

# pgvector Similarity Search

Query vector embeddings using pgvector's similarity operators. This skill covers the retrieval phase of RAG pipelines.

## When to Apply

Use this skill when:
- Finding semantically similar documents or chunks
- Implementing the retrieval step of RAG
- Building semantic search features
- Querying embeddings stored in PostgreSQL

## Distance Operators

pgvector supports three distance metrics:

| Operator | Distance Type | Use Case |
|----------|---------------|----------|
| `<=>` | Cosine distance | Most common, normalized vectors |
| `<->` | Euclidean (L2) | When magnitude matters |
| `<#>` | Inner product | Dot product similarity |

**Cosine distance** is recommended for text embeddings as it measures angle between vectors, ignoring magnitude.

## Basic Similarity Search

### Direct Query

```sql
SELECT id, content, 1 - (embedding <=> $1::vector) AS similarity
FROM intelligence.chunks
WHERE embedding IS NOT NULL
ORDER BY embedding <=> $1::vector
LIMIT 5;
```

The `1 - distance` converts cosine distance to similarity (0 to 1 scale).

### With Threshold

Filter results below a similarity threshold:

```sql
SELECT id, content, 1 - (embedding <=> $1::vector) AS similarity
FROM intelligence.chunks
WHERE embedding IS NOT NULL
  AND 1 - (embedding <=> $1::vector) > 0.7
ORDER BY embedding <=> $1::vector
LIMIT 5;
```

## Similarity Search Function

Create a reusable PostgreSQL function:

```sql
-- deploy/schemas/intelligence/procedures/find_similar_chunks.sql
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

### Revert Script

```sql
-- revert/schemas/intelligence/procedures/find_similar_chunks.sql
DROP FUNCTION IF EXISTS intelligence.find_similar_chunks(VECTOR(768), INTEGER, FLOAT);
```

## TypeScript Implementation

```typescript
import { Pool } from 'pg';
import { OllamaClient } from './utils/ollama';

const formatVector = (embedding: number[]): string => `[${embedding.join(',')}]`;

export class SimilaritySearch {
  private pool: Pool;
  private ollama: OllamaClient;

  constructor(pool: Pool, ollamaBaseUrl?: string) {
    this.pool = pool;
    this.ollama = new OllamaClient(ollamaBaseUrl);
  }

  async findSimilar(
    query: string,
    limit: number = 5,
    threshold: number = 0.7
  ): Promise<Array<{ id: number; content: string; similarity: number }>> {
    // Generate embedding for the query
    const queryEmbedding = await this.ollama.generateEmbedding(query);

    // Search for similar chunks
    const result = await this.pool.query(
      `SELECT id, content, similarity
       FROM intelligence.find_similar_chunks($1::vector, $2, $3)
       ORDER BY similarity DESC`,
      [formatVector(queryEmbedding), limit, threshold]
    );

    return result.rows;
  }

  async getContext(query: string, limit: number = 5): Promise<string> {
    const chunks = await this.findSimilar(query, limit);
    return chunks.map(c => c.content).join('\n\n');
  }
}
```

## Aggregating Context

For RAG, combine retrieved chunks into a single context string:

```sql
SELECT string_agg(content, E'\n\n') as context
FROM intelligence.find_similar_chunks($1::vector, $2, $3);
```

In TypeScript:

```typescript
async function getRAGContext(query: string, pool: Pool, ollama: OllamaClient): Promise<string> {
  const queryEmbedding = await ollama.generateEmbedding(query);

  const result = await pool.query(
    `SELECT string_agg(content, E'\n\n') as context
     FROM intelligence.find_similar_chunks($1::vector, $2)`,
    [formatVector(queryEmbedding), 5]
  );

  return result.rows[0].context || '';
}
```

## Testing Similarity Search

```typescript
import { getConnections, PgTestClient } from 'pgsql-test';
import { OllamaClient } from '../src/utils/ollama';

let pg: PgTestClient;
let teardown: () => Promise<void>;
let ollama: OllamaClient;

const formatVector = (embedding: number[]): string => `[${embedding.join(',')}]`;

beforeAll(async () => {
  ({ pg, teardown } = await getConnections());
  ollama = new OllamaClient();
});

afterAll(() => teardown());

test('should find semantically similar chunks', async () => {
  // Seed document about machine learning
  const mlContent = 'Machine learning enables systems to learn from data.';
  const mlEmbedding = await ollama.generateEmbedding(mlContent);

  await pg.client.query(
    `INSERT INTO intelligence.documents (title, content, embedding)
     VALUES ($1, $2, $3::vector)
     RETURNING id`,
    ['ML Basics', mlContent, formatVector(mlEmbedding)]
  );

  // Create chunk with embedding
  const docResult = await pg.client.query('SELECT id FROM intelligence.documents LIMIT 1');
  const docId = docResult.rows[0].id;

  await pg.client.query(
    `INSERT INTO intelligence.chunks (document_id, content, embedding, chunk_index)
     VALUES ($1, $2, $3::vector, 0)`,
    [docId, mlContent, formatVector(mlEmbedding)]
  );

  // Query for similar content
  const query = 'How do systems learn from data?';
  const queryEmbedding = await ollama.generateEmbedding(query);

  const results = await pg.client.query(
    `SELECT content, similarity
     FROM intelligence.find_similar_chunks($1::vector, 5, 0.3)
     ORDER BY similarity DESC`,
    [formatVector(queryEmbedding)]
  );

  expect(results.rows.length).toBeGreaterThan(0);
  expect(results.rows[0].similarity).toBeGreaterThan(0.3);
  expect(results.rows[0].content).toContain('Machine learning');
});
```

## Performance Optimization

### Add Indexes

For large datasets, add an index after initial data load:

```sql
-- IVFFlat index (good balance)
CREATE INDEX idx_chunks_embedding ON intelligence.chunks 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- HNSW index (better recall, more memory)
CREATE INDEX idx_chunks_embedding_hnsw ON intelligence.chunks 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

### Set Search Parameters

For IVFFlat, increase probes for better recall:

```sql
SET ivfflat.probes = 10;
```

For HNSW, adjust ef_search:

```sql
SET hnsw.ef_search = 100;
```

## Filtering with Metadata

Combine vector search with metadata filters:

```sql
SELECT c.id, c.content, 1 - (c.embedding <=> $1::vector) AS similarity
FROM intelligence.chunks c
JOIN intelligence.documents d ON c.document_id = d.id
WHERE c.embedding IS NOT NULL
  AND d.metadata->>'category' = 'technical'
  AND 1 - (c.embedding <=> $1::vector) > 0.7
ORDER BY c.embedding <=> $1::vector
LIMIT 5;
```

## Similarity Thresholds

Recommended thresholds by use case:

| Use Case | Threshold | Notes |
|----------|-----------|-------|
| Strict matching | 0.8+ | High precision, may miss relevant results |
| General search | 0.6-0.7 | Good balance |
| Exploratory | 0.4-0.5 | High recall, more noise |
| RAG context | 0.5-0.7 | Depends on document quality |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No results returned | Lower the similarity threshold |
| Irrelevant results | Raise the threshold or improve embeddings |
| Slow queries | Add IVFFlat or HNSW index |
| "Operator does not exist" | Ensure pgvector extension is installed |
| Dimension mismatch | Query vector must match stored vector dimensions |

## References

- Related skill: `pgvector-setup` for database schema setup
- Related skill: `pgvector-embeddings` for generating embeddings
- Related skill: `rag-pipeline` for complete RAG implementation
- [pgvector documentation](https://github.com/pgvector/pgvector)
