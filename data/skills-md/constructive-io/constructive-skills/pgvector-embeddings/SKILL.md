---
name: pgvector-embeddings
description: Generate and store vector embeddings with Ollama and pgvector. Use when asked to "generate embeddings", "embed documents", "store vectors", "create document embeddings", or when implementing the ingestion phase of RAG pipelines.
compatibility: Node.js 18+, PostgreSQL with pgvector, Ollama running locally or accessible via network
metadata:
  author: constructive-io
  version: "1.0.0"
---

# pgvector Embeddings

Generate vector embeddings using Ollama and store them in PostgreSQL with pgvector. This skill covers the ingestion phase of RAG pipelines.

## When to Apply

Use this skill when:
- Generating embeddings for documents or text
- Storing embeddings in PostgreSQL
- Building the ingestion pipeline for RAG
- Converting text to vectors for semantic search
- Chunking documents for better retrieval

## Embedding Models

### Recommended: nomic-embed-text

The `nomic-embed-text` model provides 768-dimensional embeddings with good quality and performance:

```bash
# Pull the model
ollama pull nomic-embed-text
```

| Model | Dimensions | Speed | Quality |
|-------|------------|-------|---------|
| `nomic-embed-text` | 768 | Fast | Good |
| `mxbai-embed-large` | 1024 | Medium | Better |
| `all-minilm` | 384 | Very Fast | Acceptable |

## OllamaClient Implementation

Create a TypeScript client for generating embeddings:

```typescript
// src/utils/ollama.ts
import fetch from 'cross-fetch';

interface OllamaEmbeddingResponse {
  embedding: number[];
}

export class OllamaClient {
  private baseUrl: string;

  constructor(baseUrl?: string) {
    this.baseUrl = baseUrl || process.env.OLLAMA_HOST || 'http://localhost:11434';
  }

  async generateEmbedding(text: string, model: string = 'nomic-embed-text'): Promise<number[]> {
    const response = await fetch(`${this.baseUrl}/api/embeddings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model,
        prompt: text,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate embedding: ${response.statusText}`);
    }

    const data: OllamaEmbeddingResponse = await response.json();
    return data.embedding;
  }
}
```

## Storing Embeddings

### Format Vector for PostgreSQL

pgvector expects vectors in bracket notation:

```typescript
const formatVector = (embedding: number[]): string => `[${embedding.join(',')}]`;
```

### Insert Document with Embedding

```typescript
import { Pool } from 'pg';
import { OllamaClient } from './utils/ollama';

const pool = new Pool();
const ollama = new OllamaClient();

async function addDocument(title: string, content: string, metadata: Record<string, unknown> = {}) {
  // Generate embedding for the full document
  const embedding = await ollama.generateEmbedding(content);

  // Insert with embedding
  const result = await pool.query(
    `INSERT INTO intelligence.documents (title, content, metadata, embedding)
     VALUES ($1, $2, $3, $4::vector)
     RETURNING id`,
    [title, content, metadata, formatVector(embedding)]
  );

  return result.rows[0].id;
}
```

## Document Chunking

### Why Chunk Documents?

Large documents should be split into smaller chunks for better retrieval:
- Embeddings capture meaning better for shorter text
- Retrieval returns more relevant context
- Reduces noise in LLM responses

### Chunking Function (SQL)

Create a PostgreSQL function for chunking:

```sql
-- deploy/schemas/intelligence/procedures/create_document_chunks.sql
CREATE FUNCTION intelligence.create_document_chunks(
    p_document_id INTEGER,
    p_chunk_size INTEGER DEFAULT 1000,
    p_chunk_overlap INTEGER DEFAULT 200
)
RETURNS VOID AS $$
DECLARE
    v_content TEXT;
    v_position INTEGER := 1;
    v_chunk_index INTEGER := 0;
    v_chunk TEXT;
    v_len INTEGER;
BEGIN
    SELECT content INTO v_content
    FROM intelligence.documents
    WHERE id = p_document_id;

    IF v_content IS NULL THEN
        RAISE NOTICE 'No content found for document_id %', p_document_id;
        RETURN;
    END IF;

    v_len := LENGTH(v_content);

    WHILE v_position <= v_len LOOP
        v_chunk := SUBSTRING(v_content FROM v_position FOR p_chunk_size);

        INSERT INTO intelligence.chunks (document_id, content, chunk_index)
        VALUES (p_document_id, v_chunk, v_chunk_index);

        v_position := v_position + (p_chunk_size - p_chunk_overlap);
        v_chunk_index := v_chunk_index + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

### Chunking Parameters

| Parameter | Recommended | Description |
|-----------|-------------|-------------|
| `chunk_size` | 500-1000 | Characters per chunk |
| `chunk_overlap` | 100-200 | Overlap between chunks |

Overlap ensures context isn't lost at chunk boundaries.

## Complete Ingestion Pipeline

```typescript
import { Pool } from 'pg';
import { OllamaClient } from './utils/ollama';

const formatVector = (embedding: number[]): string => `[${embedding.join(',')}]`;

export class DocumentIngester {
  private pool: Pool;
  private ollama: OllamaClient;

  constructor(pool: Pool, ollamaBaseUrl?: string) {
    this.pool = pool;
    this.ollama = new OllamaClient(ollamaBaseUrl);
  }

  async ingestDocument(
    title: string,
    content: string,
    metadata: Record<string, unknown> = {},
    chunkSize: number = 1000,
    chunkOverlap: number = 200
  ): Promise<number> {
    // 1. Generate embedding for full document
    const docEmbedding = await this.ollama.generateEmbedding(content);

    // 2. Insert document
    const docResult = await this.pool.query(
      `INSERT INTO intelligence.documents (title, content, metadata, embedding)
       VALUES ($1, $2, $3, $4::vector)
       RETURNING id`,
      [title, content, metadata, formatVector(docEmbedding)]
    );
    const documentId = docResult.rows[0].id;

    // 3. Create chunks
    await this.pool.query(
      'SELECT intelligence.create_document_chunks($1, $2, $3)',
      [documentId, chunkSize, chunkOverlap]
    );

    // 4. Generate embeddings for each chunk
    const chunks = await this.pool.query(
      'SELECT id, content FROM intelligence.chunks WHERE document_id = $1 ORDER BY chunk_index',
      [documentId]
    );

    for (const chunk of chunks.rows) {
      const chunkEmbedding = await this.ollama.generateEmbedding(chunk.content);
      await this.pool.query(
        'UPDATE intelligence.chunks SET embedding = $1::vector WHERE id = $2',
        [formatVector(chunkEmbedding), chunk.id]
      );
    }

    return documentId;
  }
}
```

## Testing Embeddings

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

test('should generate and store embedding', async () => {
  const text = 'Machine learning is a subset of artificial intelligence.';
  const embedding = await ollama.generateEmbedding(text);

  expect(embedding).toHaveLength(768); // nomic-embed-text dimensions

  const result = await pg.client.query(
    `INSERT INTO intelligence.documents (title, content, embedding)
     VALUES ($1, $2, $3::vector)
     RETURNING id`,
    ['ML Basics', text, formatVector(embedding)]
  );

  expect(result.rows[0].id).toBeDefined();
});
```

## Design Considerations

### Embeddings at Application Layer

Generate embeddings in your application, not in database triggers:

**Why not triggers?**
- HTTP calls in triggers can cause transaction timeouts
- Failed embedding calls would rollback the entire transaction
- Harder to retry or handle rate limits

**Recommended approach:**
- Generate embeddings in application code
- Use job queues for async processing if needed
- Handle failures gracefully with retries

### Batch Processing

For large document sets, process in batches:

```typescript
async function batchIngest(documents: Array<{title: string, content: string}>) {
  for (const doc of documents) {
    try {
      await ingester.ingestDocument(doc.title, doc.content);
      console.log(`Ingested: ${doc.title}`);
    } catch (error) {
      console.error(`Failed to ingest ${doc.title}:`, error);
      // Continue with next document
    }
  }
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection refused" to Ollama | Ensure Ollama is running: `ollama serve` |
| "Model not found" | Pull the model: `ollama pull nomic-embed-text` |
| Dimension mismatch | Ensure VECTOR(n) matches model output dimensions |
| Slow embedding generation | Consider batching or using a faster model |
| Memory issues | Process documents in smaller batches |

## References

- Related skill: `pgvector-setup` for database schema setup
- Related skill: `pgvector-similarity-search` for querying embeddings
- Related skill: `ollama-integration` for Ollama client details
- Related skill: `rag-pipeline` for complete RAG implementation
