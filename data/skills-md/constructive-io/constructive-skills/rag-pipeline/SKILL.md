---
name: rag-pipeline
description: Build complete RAG (Retrieval-Augmented Generation) pipelines with pgvector and Ollama. Use when asked to "build RAG", "implement RAG pipeline", "create AI search", "build document Q&A", or when combining vector search with LLM generation.
compatibility: Node.js 18+, PostgreSQL with pgvector, Ollama with embedding and chat models
metadata:
  author: constructive-io
  version: "1.0.0"
---

# RAG Pipeline

Build complete Retrieval-Augmented Generation pipelines combining pgvector for semantic search and Ollama for text generation.

## When to Apply

Use this skill when:
- Building document Q&A systems
- Implementing AI-powered search
- Creating chatbots with knowledge bases
- Combining vector search with LLM responses
- Building applications that need context-aware AI responses

## RAG Architecture

```
Document → Chunking → Embedding → pgvector Storage
                                        ↓
Query → Embedding → Similarity Search → Context Retrieval → LLM Response
```

### Components

1. **Ingestion**: Chunk documents, generate embeddings, store in pgvector
2. **Retrieval**: Embed query, find similar chunks, aggregate context
3. **Generation**: Pass context + query to LLM for response

## Complete RAGService Implementation

```typescript
// src/services/rag.service.ts
import { Pool } from 'pg';
import { OllamaClient } from '../utils/ollama';

interface Chunk {
  id: number;
  document_id: number;
  content: string;
  chunk_index: number;
}

const formatVector = (embedding: number[]): string => `[${embedding.join(',')}]`;

export class RAGService {
  private pool: Pool;
  private ollama: OllamaClient;

  constructor(pool: Pool, ollamaBaseUrl?: string) {
    this.pool = pool;
    this.ollama = new OllamaClient(ollamaBaseUrl);
  }

  // Ingestion: Add document with automatic chunking and embedding
  async addDocument(
    title: string,
    content: string,
    metadata: Record<string, unknown> = {}
  ): Promise<number> {
    // Generate embedding for full document
    const embedding = await this.ollama.generateEmbedding(content);

    // Insert document
    const result = await this.pool.query(
      `INSERT INTO intelligence.documents (title, content, metadata, embedding)
       VALUES ($1, $2, $3, $4::vector)
       RETURNING id`,
      [title, content, metadata, formatVector(embedding)]
    );

    const documentId = result.rows[0].id;

    // Create chunks
    await this.pool.query(
      'SELECT intelligence.create_document_chunks($1)',
      [documentId]
    );

    // Generate embeddings for each chunk
    const chunks = await this.pool.query<Chunk>(
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

  // Retrieval + Generation: Query with RAG
  async query(
    question: string,
    sessionId: string,
    contextLimit: number = 5
  ): Promise<string> {
    // Embed the question
    const questionEmbedding = await this.ollama.generateEmbedding(question);

    // Retrieve relevant context
    const result = await this.pool.query(
      `SELECT string_agg(content, E'\n\n') as context
       FROM intelligence.find_similar_chunks($1::vector, $2)`,
      [formatVector(questionEmbedding), contextLimit]
    );

    const context = result.rows[0].context;

    // Generate response with context
    const response = await this.ollama.generateResponse(question, context);

    // Store in chat history
    await this.pool.query(
      `INSERT INTO intelligence.chat_history (session_id, role, content)
       VALUES ($1, 'user', $2), ($1, 'assistant', $3)`,
      [sessionId, question, response]
    );

    return response;
  }

  // Streaming response variant
  async queryStreaming(
    question: string,
    sessionId: string,
    onChunk: (chunk: string) => void,
    contextLimit: number = 5
  ): Promise<void> {
    const questionEmbedding = await this.ollama.generateEmbedding(question);

    const result = await this.pool.query(
      `SELECT string_agg(content, E'\n\n') as context
       FROM intelligence.find_similar_chunks($1::vector, $2)`,
      [formatVector(questionEmbedding), contextLimit]
    );

    const context = result.rows[0].context;

    // Store user message
    await this.pool.query(
      'INSERT INTO intelligence.chat_history (session_id, role, content) VALUES ($1, $2, $3)',
      [sessionId, 'user', question]
    );

    let fullResponse = '';

    await this.ollama.generateStreamingResponse(
      question,
      (chunk) => {
        onChunk(chunk);
        fullResponse += chunk;
      },
      context
    );

    // Store assistant response
    await this.pool.query(
      'INSERT INTO intelligence.chat_history (session_id, role, content) VALUES ($1, $2, $3)',
      [sessionId, 'assistant', fullResponse]
    );
  }

  // Get conversation history
  async getChatHistory(
    sessionId: string,
    limit: number = 10
  ): Promise<Array<{ role: string; content: string }>> {
    const result = await this.pool.query(
      `SELECT role, content
       FROM intelligence.chat_history
       WHERE session_id = $1
       ORDER BY created_at DESC
       LIMIT $2`,
      [sessionId, limit]
    );

    return result.rows.reverse();
  }
}
```

## OllamaClient with Generation

```typescript
// src/utils/ollama.ts
import fetch from 'cross-fetch';

interface OllamaResponse {
  model: string;
  created_at: string;
  response: string;
  done: boolean;
}

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
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model, prompt: text }),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate embedding: ${response.statusText}`);
    }

    const data: OllamaEmbeddingResponse = await response.json();
    return data.embedding;
  }

  async generateResponse(prompt: string, context?: string): Promise<string> {
    const fullPrompt = context
      ? `Context: ${context}\n\nQuestion: ${prompt}\n\nAnswer:`
      : prompt;

    const response = await fetch(`${this.baseUrl}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'mistral',
        prompt: fullPrompt,
        stream: false,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate response: ${response.statusText}`);
    }

    const data: OllamaResponse = await response.json();
    return data.response;
  }

  async generateStreamingResponse(
    prompt: string,
    onChunk: (chunk: string) => void,
    context?: string
  ): Promise<void> {
    const fullPrompt = context
      ? `Context: ${context}\n\nQuestion: ${prompt}\n\nAnswer:`
      : prompt;

    const response = await fetch(`${this.baseUrl}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'mistral',
        prompt: fullPrompt,
        stream: true,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate streaming response: ${response.statusText}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('Failed to get response reader');
    }

    const decoder = new TextDecoder();
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n').filter(Boolean);

      for (const line of lines) {
        try {
          const data: OllamaResponse = JSON.parse(line);
          if (data.response) {
            onChunk(data.response);
          }
        } catch (error) {
          // Skip malformed JSON lines
        }
      }
    }
  }
}
```

## Usage Example

```typescript
import { Pool } from 'pg';
import { RAGService } from './services/rag.service';

const pool = new Pool();
const rag = new RAGService(pool);

// Add documents to knowledge base
await rag.addDocument(
  'Company Policies',
  'Our company offers 20 days of PTO per year. Remote work is allowed...',
  { category: 'hr', version: '2024' }
);

// Query with RAG
const answer = await rag.query(
  'How many PTO days do employees get?',
  'session-123'
);

console.log(answer);
// "Based on the company policies, employees receive 20 days of PTO per year."
```

## Testing RAG Pipeline

```typescript
// __tests__/rag.test.ts
process.env.LOG_SCOPE = 'rag';
jest.setTimeout(300000); // 5 minutes for LLM operations

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

describe('RAG Pipeline', () => {
  it('should generate response using retrieved context', async () => {
    // 1. Ingest document
    const document = `
      Hyperweb brings TypeScript fully on-chain with its custom Virtual Machine.
      It enables developers to write smart contracts in JavaScript.
      Hyperweb powers apps across ecosystems like Osmosis and dYdX.
    `.trim();

    const docEmbedding = await ollama.generateEmbedding(document);

    const docResult = await pg.client.query(
      `INSERT INTO intelligence.documents (title, content, embedding)
       VALUES ($1, $2, $3::vector)
       RETURNING id`,
      ['Hyperweb Overview', document, formatVector(docEmbedding)]
    );
    const docId = docResult.rows[0].id;

    // 2. Create and embed chunks
    await pg.client.query(
      'SELECT intelligence.create_document_chunks($1, $2, $3)',
      [docId, 300, 100]
    );

    const chunks = await pg.client.query(
      'SELECT id, content FROM intelligence.chunks WHERE document_id = $1',
      [docId]
    );

    for (const chunk of chunks.rows) {
      const embedding = await ollama.generateEmbedding(chunk.content);
      await pg.client.query(
        'UPDATE intelligence.chunks SET embedding = $1::vector WHERE id = $2',
        [formatVector(embedding), chunk.id]
      );
    }

    // 3. Query with RAG
    const query = 'What programming language does Hyperweb use?';
    const queryEmbedding = await ollama.generateEmbedding(query);

    const contextResult = await pg.client.query(
      `SELECT string_agg(content, E'\n\n') as context
       FROM intelligence.find_similar_chunks($1::vector, 3, 0.3)`,
      [formatVector(queryEmbedding)]
    );

    const context = contextResult.rows[0].context;

    // 4. Generate response
    const ollamaHost = process.env.OLLAMA_HOST || 'http://localhost:11434';
    const response = await fetch(`${ollamaHost}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'mistral',
        prompt: `Context:\n${context}\n\nQuestion: ${query}\n\nAnswer:`,
        stream: false,
      }),
    }).then(res => res.json());

    expect(response.response).toBeTruthy();
    expect(response.response.toLowerCase()).toMatch(/typescript|javascript/);
  });
});
```

## Performance Logging

Track performance across the pipeline:

```typescript
const measureTime = async <T>(
  service: 'ollama' | 'postgres',
  action: string,
  fn: () => Promise<T>
): Promise<T> => {
  const start = performance.now();
  const result = await fn();
  const duration = performance.now() - start;
  console.log(`[${service.toUpperCase()}] ${action}: ${duration.toFixed(2)}ms`);
  return result;
};

// Usage
const embedding = await measureTime('ollama', 'generateEmbedding', () =>
  ollama.generateEmbedding(text)
);
```

## Best Practices

### Chunking Strategy

| Document Type | Chunk Size | Overlap |
|---------------|------------|---------|
| Technical docs | 500-800 | 100-150 |
| Conversational | 300-500 | 50-100 |
| Legal/formal | 800-1200 | 200-300 |

### Context Window Management

Limit context to avoid exceeding LLM context window:

```typescript
const MAX_CONTEXT_CHARS = 4000;

async function getContext(query: string, limit: number = 5): Promise<string> {
  const chunks = await findSimilarChunks(query, limit);
  let context = '';

  for (const chunk of chunks) {
    if (context.length + chunk.content.length > MAX_CONTEXT_CHARS) break;
    context += chunk.content + '\n\n';
  }

  return context.trim();
}
```

### Prompt Engineering

Structure prompts for better responses:

```typescript
const buildPrompt = (context: string, question: string): string => `
You are a helpful assistant. Answer the question based only on the provided context.
If the context doesn't contain enough information, say so.

Context:
${context}

Question: ${question}

Answer:`.trim();
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Irrelevant responses | Lower similarity threshold, improve chunking |
| Hallucinations | Add "only use provided context" to prompt |
| Slow responses | Use streaming, optimize chunk count |
| Context too long | Reduce chunk count or size |
| Missing information | Increase similarity threshold, add more documents |

## References

- Related skill: `pgvector-setup` for database schema
- Related skill: `pgvector-embeddings` for embedding generation
- Related skill: `pgvector-similarity-search` for retrieval
- Related skill: `ollama-integration` for Ollama client details
- Related skill: `github-workflows-ollama` for CI/CD setup
