---
name: vectorize
description: Vector database for embeddings and semantic search at the edge. Load when building RAG pipelines, implementing semantic search, storing embeddings from Workers AI, finding similar documents, building recommendation systems, or querying vectors by similarity.
---

# Cloudflare Vectorize

Store and query high-dimensional vector embeddings at the edge for RAG (Retrieval Augmented Generation), semantic search, and similarity matching.

## FIRST: Create Index

```bash
# Create with preset (auto-configures dimensions and metric)
wrangler vectorize create my-index --preset @cf/baai/bge-base-en-v1.5

# Or create with explicit dimensions
wrangler vectorize create my-index --dimensions 768 --metric cosine

# List indexes
wrangler vectorize list
```

Add to `wrangler.jsonc`:

```jsonc
{
  "vectorize": [
    { "binding": "SEARCH_INDEX", "index_name": "my-index" }
  ]
}
```

## When to Use

| Use Case | Description |
|----------|-------------|
| RAG Pipelines | Store document embeddings for context retrieval with LLMs |
| Semantic Search | Find similar content by meaning, not keywords |
| Recommendation Systems | Match users/items based on embedding similarity |
| Duplicate Detection | Find near-duplicate content using vector distance |
| Content Classification | Group similar items by vector clustering |

## Quick Reference

| Operation | API |
|-----------|-----|
| Insert vectors | `await env.INDEX.insert([{ id, values, metadata }])` |
| Query similar vectors | `await env.INDEX.query(vector, { topK: 5 })` |
| Upsert (insert or update) | `await env.INDEX.upsert([{ id, values, metadata }])` |
| Delete by IDs | `await env.INDEX.deleteByIds(["id1", "id2"])` |
| Get by IDs | `await env.INDEX.getByIds(["id1", "id2"])` |

## Basic RAG Example

```typescript
interface Env {
  SEARCH_INDEX: Vectorize;
  AI: Ai;
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url);

    // Index documents with embeddings
    if (url.pathname === "/index" && req.method === "POST") {
      const { text, id } = await req.json<{ text: string; id: string }>();
      
      // Generate embedding using Workers AI
      const { data } = await env.AI.run("@cf/baai/bge-base-en-v1.5", {
        text: [text],
      });
      
      const embedding = data[0];
      
      // Insert into Vectorize
      await env.SEARCH_INDEX.insert([{
        id,
        values: embedding,
        metadata: { text }
      }]);
      
      return Response.json({ success: true, id });
    }

    // Search similar documents
    if (url.pathname === "/search" && req.method === "POST") {
      const { query } = await req.json<{ query: string }>();
      
      // Generate query embedding
      const { data } = await env.AI.run("@cf/baai/bge-base-en-v1.5", {
        text: [query],
      });
      
      const queryEmbedding = data[0];
      
      // Find similar vectors
      const results = await env.SEARCH_INDEX.query(queryEmbedding, {
        topK: 5,
        returnMetadata: true
      });
      
      return Response.json({
        matches: results.matches.map(match => ({
          id: match.id,
          score: match.score,
          text: match.metadata?.text
        }))
      });
    }

    return new Response("Not found", { status: 404 });
  }
};
```

## Configuration

### wrangler.jsonc

```jsonc
{
  "name": "vectorize-demo",
  "main": "src/index.ts",
  "compatibility_date": "2026-01-01",
  "compatibility_flags": ["nodejs_compat"],
  
  // AI binding for generating embeddings
  "ai": { "binding": "AI" },
  
  // Vectorize binding
  "vectorize": [
    {
      "binding": "SEARCH_INDEX",
      "index_name": "my-index"
    }
  ]
}
```

### Type Definitions

```typescript
interface Env {
  SEARCH_INDEX: Vectorize;
  AI: Ai;
}

// Vector insert/upsert format
interface VectorRecord {
  id: string;
  values: number[];
  metadata?: Record<string, any>;
}

// Query result format
interface VectorQueryResult {
  matches: Array<{
    id: string;
    score: number;
    values?: number[];
    metadata?: Record<string, any>;
  }>;
  count: number;
}
```

## Index Creation

### Using Presets

Presets automatically configure dimensions and distance metrics to match Workers AI embedding models:

```bash
# BGE Base English (768 dimensions, cosine)
wrangler vectorize create docs-index --preset @cf/baai/bge-base-en-v1.5

# BGE Large English (1024 dimensions, cosine)
wrangler vectorize create docs-index --preset @cf/baai/bge-large-en-v1.5

# BGE Small English (384 dimensions, cosine)
wrangler vectorize create docs-index --preset @cf/baai/bge-small-en-v1.5
```

### Manual Configuration

For custom embeddings or external models:

```bash
# Create with specific dimensions and metric
wrangler vectorize create custom-index \
  --dimensions 1536 \
  --metric cosine

# Available metrics: cosine, euclidean, dot-product
```

**Distance Metrics:**

| Metric | Use Case | Range |
|--------|----------|-------|
| `cosine` | Most common for text embeddings | -1 to 1 (1 = identical) |
| `euclidean` | Absolute distance in space | 0 to ∞ (0 = identical) |
| `dot-product` | When embeddings are normalized | -∞ to ∞ (higher = more similar) |

## Insert and Query Operations

### Insert Vectors

```typescript
// Insert single vector
await env.SEARCH_INDEX.insert([{
  id: "doc-1",
  values: [0.1, 0.2, 0.3, ...], // Must match index dimensions
  metadata: {
    title: "Getting Started",
    category: "docs",
    created: new Date().toISOString()
  }
}]);

// Batch insert (more efficient)
const vectors = documents.map(doc => ({
  id: doc.id,
  values: doc.embedding,
  metadata: { title: doc.title, url: doc.url }
}));

await env.SEARCH_INDEX.insert(vectors);
```

### Upsert Vectors

Use `upsert` to insert new vectors or update existing ones:

```typescript
await env.SEARCH_INDEX.upsert([{
  id: "doc-1",
  values: updatedEmbedding,
  metadata: { title: "Updated Title" }
}]);
```

### Query for Similar Vectors

```typescript
// Basic query
const results = await env.SEARCH_INDEX.query(queryEmbedding, {
  topK: 10,
  returnMetadata: true,
  returnValues: false // Set true to get vector values back
});

// Process results
for (const match of results.matches) {
  console.log(`ID: ${match.id}`);
  console.log(`Score: ${match.score}`);
  console.log(`Metadata:`, match.metadata);
}

// Filter by metadata (optional)
const filtered = await env.SEARCH_INDEX.query(queryEmbedding, {
  topK: 10,
  returnMetadata: true,
  filter: { category: "docs" } // Namespace filtering
});
```

### Delete Vectors

```typescript
// Delete by IDs
await env.SEARCH_INDEX.deleteByIds(["doc-1", "doc-2"]);

// Delete all with specific namespace (if using namespace metadata)
const allDocs = await env.SEARCH_INDEX.query(zeroVector, { topK: 10000 });
const idsToDelete = allDocs.matches
  .filter(m => m.metadata?.namespace === "old")
  .map(m => m.id);
await env.SEARCH_INDEX.deleteByIds(idsToDelete);
```

### Retrieve by IDs

```typescript
// Get specific vectors
const vectors = await env.SEARCH_INDEX.getByIds(["doc-1", "doc-2"]);

for (const vector of vectors) {
  console.log(vector.id, vector.metadata);
}
```

## Integration with Workers AI

### Complete RAG Pipeline

```typescript
interface Env {
  SEARCH_INDEX: Vectorize;
  AI: Ai;
}

const EMBEDDING_MODEL = "@cf/baai/bge-base-en-v1.5";
const CHAT_MODEL = "@cf/meta/llama-3.1-8b-instruct";

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const { question } = await req.json<{ question: string }>();

    // 1. Generate embedding for user question
    const { data: embeddings } = await env.AI.run(EMBEDDING_MODEL, {
      text: [question],
    });
    
    const queryEmbedding = embeddings[0];

    // 2. Search for relevant context
    const results = await env.SEARCH_INDEX.query(queryEmbedding, {
      topK: 3,
      returnMetadata: true
    });

    // 3. Build context from results
    const context = results.matches
      .map(match => match.metadata?.text)
      .join("\n\n");

    // 4. Generate answer with RAG
    const response = await env.AI.run(CHAT_MODEL, {
      messages: [
        {
          role: "system",
          content: `Answer the question using only the following context:\n\n${context}`
        },
        {
          role: "user",
          content: question
        }
      ]
    });

    return Response.json({
      answer: response.response,
      sources: results.matches.map(m => ({
        id: m.id,
        score: m.score,
        metadata: m.metadata
      }))
    });
  }
};
```

### Batch Document Indexing

```typescript
async function indexDocuments(
  documents: Array<{ id: string; text: string }>,
  env: Env
) {
  // Generate embeddings in batches
  const BATCH_SIZE = 50;
  
  for (let i = 0; i < documents.length; i += BATCH_SIZE) {
    const batch = documents.slice(i, i + BATCH_SIZE);
    
    // Generate embeddings for batch
    const { data: embeddings } = await env.AI.run(
      "@cf/baai/bge-base-en-v1.5",
      { text: batch.map(d => d.text) }
    );
    
    // Insert vectors
    const vectors = batch.map((doc, idx) => ({
      id: doc.id,
      values: embeddings[idx],
      metadata: { text: doc.text }
    }));
    
    await env.SEARCH_INDEX.insert(vectors);
  }
}
```

## Detailed References

- **[references/indexing.md](references/indexing.md)** - Index creation, presets, dimensions, metrics, management
- **[references/querying.md](references/querying.md)** - Query patterns, filtering, scoring, optimization
- **[references/limits.md](references/limits.md)** - Limits, quotas, performance characteristics, troubleshooting
- **[references/testing.md](references/testing.md)** - Mocking strategies, remote bindings (no local simulation)

## Best Practices

1. **Use presets for Workers AI models**: Automatically matches dimensions and metric
2. **Batch operations**: Insert/upsert multiple vectors at once for better performance
3. **Include useful metadata**: Store references to original documents for retrieval
4. **Choose appropriate topK**: Balance relevance vs response size (typically 3-10)
5. **Normalize embeddings for cosine**: Most text embedding models already do this
6. **Use upsert for updates**: Safer than delete + insert pattern
7. **Leverage metadata for filtering**: Add namespace or category fields for scoped searches
8. **Monitor index size**: Plan for growth, understand limits
9. **Test similarity thresholds**: Score interpretation varies by metric and model
10. **Cache frequent queries**: Reduce latency for common searches with KV or memory

## Common Patterns

### Hybrid Search (Keyword + Semantic)

```typescript
// Combine keyword filtering with vector search
const results = await env.SEARCH_INDEX.query(queryEmbedding, {
  topK: 20,
  returnMetadata: true
});

// Re-rank with keyword matching
const reranked = results.matches
  .filter(match => {
    const text = match.metadata?.text?.toLowerCase() || "";
    return keywords.some(kw => text.includes(kw.toLowerCase()));
  })
  .slice(0, 5);
```

### Chunking Long Documents

```typescript
function chunkDocument(text: string, chunkSize: number = 500): string[] {
  const words = text.split(/\s+/);
  const chunks: string[] = [];
  
  for (let i = 0; i < words.length; i += chunkSize) {
    chunks.push(words.slice(i, i + chunkSize).join(" "));
  }
  
  return chunks;
}

// Index each chunk separately
const chunks = chunkDocument(document.text);
const vectors = await Promise.all(
  chunks.map(async (chunk, idx) => {
    const { data } = await env.AI.run(EMBEDDING_MODEL, { text: [chunk] });
    return {
      id: `${document.id}-chunk-${idx}`,
      values: data[0],
      metadata: { 
        docId: document.id,
        chunkIndex: idx,
        text: chunk 
      }
    };
  })
);

await env.SEARCH_INDEX.insert(vectors);
```

### Multi-tenancy with Namespaces

```typescript
// Use metadata for tenant isolation
await env.SEARCH_INDEX.insert([{
  id: `tenant-${tenantId}-doc-${docId}`,
  values: embedding,
  metadata: {
    tenantId,
    text: content
  }
}]);

// Query with tenant filtering
const results = await env.SEARCH_INDEX.query(queryEmbedding, {
  topK: 10,
  returnMetadata: true
});

// Filter results by tenant
const tenantResults = results.matches.filter(
  m => m.metadata?.tenantId === currentTenantId
);
```
