---
name: agentic-kit-rag
description: Configure agentic-kit for RAG (Retrieval-Augmented Generation) with pgvector and PGPM. Use when asked to "enable RAG for agentic-kit", "add database context to AI chat", "configure RAG environment", "set up local RAG database", or when building AI applications that need contextual responses from a knowledge base.
compatibility: Node.js 18+, PostgreSQL with pgvector, Ollama, PGPM CLI
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Agentic Kit RAG Integration

Configure the agentic-kit for Retrieval-Augmented Generation (RAG) using pgvector for semantic search and PGPM for database management. This skill enables AI chat applications to provide contextual responses based on a knowledge base stored in PostgreSQL.

## When to Apply

Use this skill when:
- Adding RAG capabilities to agentic-kit applications
- Configuring environment variables for RAG-enabled AI chat
- Setting up a local database for document storage and retrieval
- Building AI assistants that need access to a knowledge base
- Integrating pgvector with the sf-rag-utils app

## Architecture Overview

```
User Query → Agentic Kit → RAG Provider
                              ↓
                    [RAG_ENABLED=true?]
                         ↓         ↓
                       Yes         No
                         ↓         ↓
              Query Embedding   Direct Ollama
                         ↓
              pgvector Search
                         ↓
              Context Retrieval
                         ↓
              Ollama + Context → Response
```

## Environment Variables

Configure RAG behavior through environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `RAG_ENABLED` | `true` | Enable RAG context retrieval (set to `false` for direct Ollama) |
| `RAG_DATABASE_URL` | - | PostgreSQL connection string (required when RAG_ENABLED=true) |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `RAG_EMBEDDING_MODEL` | `nomic-embed-text` | Model for generating embeddings |
| `RAG_CHAT_MODEL` | `llama3.2` | Model for chat responses |
| `RAG_SIMILARITY_THRESHOLD` | `0.5` | Minimum similarity score for retrieval |
| `RAG_CONTEXT_LIMIT` | `5` | Maximum number of chunks to retrieve |
| `RAG_SCHEMA` | `intelligence` | PostgreSQL schema for RAG tables |

### Example .env File

```bash
# RAG Configuration
RAG_ENABLED=true
RAG_DATABASE_URL=postgres://postgres:postgres@localhost:5432/rag_dev

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
RAG_EMBEDDING_MODEL=nomic-embed-text
RAG_CHAT_MODEL=llama3.2

# Retrieval Settings
RAG_SIMILARITY_THRESHOLD=0.5
RAG_CONTEXT_LIMIT=5
RAG_SCHEMA=intelligence
```

### Disabling RAG (Direct Ollama Mode)

To use direct Ollama without RAG context:

```bash
RAG_ENABLED=false
OLLAMA_HOST=http://localhost:11434
RAG_CHAT_MODEL=llama3.2
```

## Quick Start

### 1. Set Up Local Database with PGPM

Ensure PostgreSQL is running with a pgvector-enabled image (see `pgpm-docker` skill) and PG env vars are loaded (see `pgpm-env` skill).

```bash
# Run the setup script
bash /mnt/skills/user/agentic-kit-rag/scripts/setup-rag-database.sh
```

### 2. Configure Environment

Create a `.env` file in your application:

```bash
RAG_ENABLED=true
RAG_DATABASE_URL=postgres://postgres:postgres@localhost:5432/rag_dev
OLLAMA_HOST=http://localhost:11434
```

### 3. Pull Required Ollama Models

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

## RAG Provider Implementation

Create a RAG-aware provider for agentic-kit:

```typescript
// src/lib/ai/rag-provider.ts
import { Pool } from 'pg';
import type { AgentProvider, GenerateInput, StreamCallbacks, Message } from '@sf-ai/agentic-kit';

interface RAGConfig {
  databaseUrl: string;
  ollamaHost?: string;
  embeddingModel?: string;
  chatModel?: string;
  similarityThreshold?: number;
  contextLimit?: number;
  schema?: string;
}

const formatVector = (embedding: number[]): string => `[${embedding.join(',')}]`;

export class RAGProvider implements AgentProvider {
  readonly name = 'rag';
  private pool: Pool;
  private ollamaHost: string;
  private embeddingModel: string;
  private chatModel: string;
  private similarityThreshold: number;
  private contextLimit: number;
  private schema: string;

  constructor(config: RAGConfig) {
    this.pool = new Pool({ connectionString: config.databaseUrl });
    this.ollamaHost = config.ollamaHost || 'http://localhost:11434';
    this.embeddingModel = config.embeddingModel || 'nomic-embed-text';
    this.chatModel = config.chatModel || 'llama3.2';
    this.similarityThreshold = config.similarityThreshold || 0.5;
    this.contextLimit = config.contextLimit || 5;
    this.schema = config.schema || 'intelligence';
  }

  private async generateEmbedding(text: string): Promise<number[]> {
    const response = await fetch(`${this.ollamaHost}/api/embeddings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: this.embeddingModel, prompt: text }),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate embedding: ${response.statusText}`);
    }

    const data = await response.json();
    return data.embedding;
  }

  private async retrieveContext(query: string): Promise<string> {
    const embedding = await this.generateEmbedding(query);

    const result = await this.pool.query(
      `SELECT string_agg(content, E'\n\n') as context
       FROM ${this.schema}.find_similar_chunks($1::vector, $2, $3)`,
      [formatVector(embedding), this.contextLimit, this.similarityThreshold]
    );

    return result.rows[0]?.context || '';
  }

  async generate(input: GenerateInput): Promise<string> {
    const context = await this.retrieveContext(input.prompt);

    const response = await fetch(`${this.ollamaHost}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: input.model || this.chatModel,
        messages: this.buildMessages(input.messages || [], input.prompt, context),
        stream: false,
      }),
    });

    if (!response.ok) {
      throw new Error(`Chat failed: ${response.statusText}`);
    }

    const data = await response.json();
    return data.message.content;
  }

  async generateStream(input: GenerateInput, callbacks: StreamCallbacks): Promise<void> {
    callbacks.onStateChange?.('thinking');

    const context = await this.retrieveContext(input.prompt);

    const response = await fetch(`${this.ollamaHost}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: input.model || this.chatModel,
        messages: this.buildMessages(input.messages || [], input.prompt, context),
        stream: true,
      }),
    });

    if (!response.ok) {
      const error = new Error(`Chat stream failed: ${response.statusText}`);
      callbacks.onStateChange?.('error');
      callbacks.onError?.(error);
      throw error;
    }

    await this.processStream(response, callbacks);
  }

  private buildMessages(
    messages: Message[],
    prompt: string,
    context: string
  ): Array<{ role: string; content: string }> {
    const systemMessage = messages.find(m => m.role === 'system');
    const conversationMessages = messages.filter(m => m.role !== 'system');

    const systemContent = systemMessage?.content || 'You are a helpful assistant.';
    const contextualSystem = context
      ? `${systemContent}\n\nUse the following context to answer questions. If the context doesn't contain relevant information, say so.\n\nContext:\n${context}`
      : systemContent;

    return [
      { role: 'system', content: contextualSystem },
      ...conversationMessages.map(m => ({ role: m.role, content: m.content })),
      { role: 'user', content: prompt },
    ];
  }

  private async processStream(response: Response, callbacks: StreamCallbacks): Promise<void> {
    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('Failed to get response reader');
    }

    callbacks.onStateChange?.('streaming');

    const decoder = new TextDecoder();
    let fullResponse = '';
    let done = false;

    while (!done) {
      const result = await reader.read();
      done = result.done;
      if (done) break;

      const chunk = decoder.decode(result.value);
      const lines = chunk.split('\n').filter(Boolean);

      for (const line of lines) {
        try {
          const data = JSON.parse(line);
          if (data.message?.content) {
            fullResponse += data.message.content;
            callbacks.onToken?.(data.message.content);
          }
        } catch {
          // Skip malformed JSON lines
        }
      }
    }

    callbacks.onStateChange?.('complete');
    callbacks.onComplete?.(fullResponse);
  }

  async isAvailable(): Promise<boolean> {
    try {
      const [ollamaCheck, dbCheck] = await Promise.all([
        fetch(`${this.ollamaHost}/api/tags`).then(r => r.ok),
        this.pool.query('SELECT 1').then(() => true).catch(() => false),
      ]);
      return ollamaCheck && dbCheck;
    } catch {
      return false;
    }
  }

  async close(): Promise<void> {
    await this.pool.end();
  }
}
```

## Creating RAG-Enabled Kit

```typescript
// src/lib/ai/create-rag-kit.ts
import { AgentKit, OllamaProvider } from '@sf-ai/agentic-kit';
import { RAGProvider } from './rag-provider';

interface RAGKitConfig {
  ragEnabled?: boolean;
  databaseUrl?: string;
  ollamaHost?: string;
  embeddingModel?: string;
  chatModel?: string;
  similarityThreshold?: number;
  contextLimit?: number;
  schema?: string;
}

export function createRAGKit(config: RAGKitConfig = {}): AgentKit {
  const ragEnabled = config.ragEnabled ?? process.env.RAG_ENABLED !== 'false';
  const databaseUrl = config.databaseUrl || process.env.RAG_DATABASE_URL;
  const ollamaHost = config.ollamaHost || process.env.OLLAMA_HOST || 'http://localhost:11434';

  const kit = new AgentKit();

  if (ragEnabled && databaseUrl) {
    kit.addProvider(new RAGProvider({
      databaseUrl,
      ollamaHost,
      embeddingModel: config.embeddingModel || process.env.RAG_EMBEDDING_MODEL,
      chatModel: config.chatModel || process.env.RAG_CHAT_MODEL,
      similarityThreshold: config.similarityThreshold || parseFloat(process.env.RAG_SIMILARITY_THRESHOLD || '0.5'),
      contextLimit: config.contextLimit || parseInt(process.env.RAG_CONTEXT_LIMIT || '5', 10),
      schema: config.schema || process.env.RAG_SCHEMA,
    }));
  } else {
    kit.addProvider(new OllamaProvider({
      baseUrl: ollamaHost,
      defaultModel: config.chatModel || process.env.RAG_CHAT_MODEL || 'llama3.2',
    }));
  }

  return kit;
}
```

## Updating useAgent Hook

Modify the useAgent hook to support RAG:

```typescript
// src/lib/ai/use-agent.ts
'use client';

import { useCallback, useRef, useState } from 'react';
import type { AgentState, Message, StreamCallbacks } from '@sf-ai/agentic-kit';
import { createRAGKit } from './create-rag-kit';

export interface UseAgentOptions {
  baseUrl?: string;
  model?: string;
  systemPrompt?: string;
  ragEnabled?: boolean;
  databaseUrl?: string;
}

export function useAgent(options: UseAgentOptions = {}) {
  const { baseUrl, model, systemPrompt, ragEnabled, databaseUrl } = options;

  const kitRef = useRef(createRAGKit({
    ragEnabled,
    databaseUrl,
    ollamaHost: baseUrl,
    chatModel: model,
  }));

  // ... rest of the hook implementation
}
```

## Database Schema

The RAG database requires the following schema (created by the setup script):

```sql
-- Schema
CREATE SCHEMA IF NOT EXISTS intelligence;

-- Documents table
CREATE TABLE intelligence.documents (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    embedding VECTOR(768),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Chunks table
CREATE TABLE intelligence.chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES intelligence.documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding VECTOR(768),
    chunk_index INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_chunks_document_id ON intelligence.chunks(document_id);
CREATE INDEX idx_chunks_embedding ON intelligence.chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Similarity search function
CREATE FUNCTION intelligence.find_similar_chunks(
    p_embedding VECTOR(768),
    p_limit INTEGER DEFAULT 5,
    p_similarity_threshold FLOAT DEFAULT 0.5
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

## Adding Documents to the Knowledge Base

```typescript
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.RAG_DATABASE_URL });

async function addDocument(title: string, content: string, metadata = {}) {
  const ollamaHost = process.env.OLLAMA_HOST || 'http://localhost:11434';
  const embeddingModel = process.env.RAG_EMBEDDING_MODEL || 'nomic-embed-text';

  // Generate embedding
  const response = await fetch(`${ollamaHost}/api/embeddings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: embeddingModel, prompt: content }),
  });
  const { embedding } = await response.json();

  // Insert document
  const result = await pool.query(
    `INSERT INTO intelligence.documents (title, content, metadata, embedding)
     VALUES ($1, $2, $3, $4::vector)
     RETURNING id`,
    [title, content, metadata, `[${embedding.join(',')}]`]
  );

  const documentId = result.rows[0].id;

  // Create chunks
  await pool.query('SELECT intelligence.create_document_chunks($1)', [documentId]);

  // Generate embeddings for chunks
  const chunks = await pool.query(
    'SELECT id, content FROM intelligence.chunks WHERE document_id = $1',
    [documentId]
  );

  for (const chunk of chunks.rows) {
    const chunkResponse = await fetch(`${ollamaHost}/api/embeddings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: embeddingModel, prompt: chunk.content }),
    });
    const { embedding: chunkEmbedding } = await chunkResponse.json();

    await pool.query(
      'UPDATE intelligence.chunks SET embedding = $1::vector WHERE id = $2',
      [`[${chunkEmbedding.join(',')}]`, chunk.id]
    );
  }

  return documentId;
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "RAG_DATABASE_URL not set" | Set the environment variable or pass databaseUrl to createRAGKit |
| "Connection refused" to database | Ensure PostgreSQL is running (see `pgpm-docker` skill) |
| "Connection refused" to Ollama | Ensure Ollama is running: `ollama serve` |
| "type vector does not exist" | Run the setup script to install pgvector extension |
| No context retrieved | Lower RAG_SIMILARITY_THRESHOLD or add more documents |
| Slow responses | Reduce RAG_CONTEXT_LIMIT or optimize database indexes |

## References

- Related skill: `pgvector-setup` for database schema details
- Related skill: `pgvector-embeddings` for embedding generation
- Related skill: `pgvector-similarity-search` for retrieval queries
- Related skill: `rag-pipeline` for complete RAG implementation
- Related skill: `ollama-integration` for Ollama client details
- Related skill: `pgpm-docker` for PostgreSQL container management
