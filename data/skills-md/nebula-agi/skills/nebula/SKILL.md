---
name: nebula
description: "Integrate Nebula persistent memory into applications using the official Python or JavaScript/TypeScript SDKs, REST API, or MCP server. Use when: (1) building apps that store and search memories (chatbots, RAG, knowledge bases), (2) setting up MCP integration for AI assistants (Claude Code, Cursor, VS Code, Claude Desktop, Windsurf), (3) working with Nebula collections, conversations, document uploads, semantic search, or metadata filtering, (4) code imports nebula or @nebula-ai/sdk, (5) user mentions Nebula memory API or trynebula.ai."
---

# Nebula Integration

Nebula is a persistent semantic memory platform for AI applications. It provides SDKs for Python and JavaScript/TypeScript, a REST API, and an MCP server for AI assistants.

## Quick Start

### Python

```python
pip install nebula-client
```

```python
from nebula import Nebula

nebula = Nebula(api_key="your-api-key")
# Or set NEBULA_API_KEY env var and call Nebula()

# Create a collection
collection = nebula.create_collection(name="notes", description="My notes")

# Store a memory
memory_id = nebula.store_memory({
    "collection_id": collection.id,
    "content": "Machine learning is transforming healthcare",
    "metadata": {"topic": "AI"}
})

# Search
results = nebula.search(query="healthcare AI", collection_ids=[collection.id])
for r in results:
    print(f"{r.score:.2f}: {r.content}")
```

### JavaScript / TypeScript

```bash
npm install @nebula-ai/sdk
```

```typescript
import { Nebula } from '@nebula-ai/sdk';

const nebula = new Nebula({ apiKey: 'your-api-key' });
// Or set NEBULA_API_KEY env var and call new Nebula()

const collection = await nebula.createCollection({
  name: 'notes', description: 'My notes'
});

const memoryId = await nebula.storeMemory({
  collection_id: collection.id,
  content: 'Machine learning is transforming healthcare',
  metadata: { topic: 'AI' }
});

const results = await nebula.search({
  query: 'healthcare AI',
  collection_ids: [collection.id]
});
```

## Core Concepts

- **Collections**: Organizational containers for memories (like projects/workspaces). Always specify `collection_id` when storing.
- **Memories**: Universal information containers. Three types:
  - **Document**: Entire documents, auto-chunked. Upload text, pre-chunked text, or files (PDF, DOCX, images, audio).
  - **Conversation**: Multi-turn chat. Use `memory_id` to append messages to the same conversation.
  - **Simple**: Single pieces of information.
- **Chunks**: Individual pieces within a memory (messages in conversations, sections in documents). Each has a unique ID for granular operations.
- **Search**: Hybrid semantic + full-text search with metadata filtering. Scores range 0-1.
- **Authority**: Score (0-1) to prioritize content in search results. Default 0.5.

## Authentication

- **API Key**: Get from [trynebula.ai](https://trynebula.ai) -> Settings -> API Keys
- **Environment variable**: `NEBULA_API_KEY` (auto-read by both SDKs)
- **Explicit**: Pass `api_key` (Python) or `apiKey` (JS) to constructor
- **Base URL**: `https://api.trynebula.ai` (default, configurable via `base_url`/`baseUrl`)

## Conversation Pattern

Conversations use `memory_id` to append messages to the same container:

```python
# Python
conv_id = nebula.store_memory({
    "collection_id": "support",
    "content": "Hello!", "role": "assistant"
})
nebula.store_memory({
    "memory_id": conv_id,
    "collection_id": "support",
    "content": "I need help", "role": "user"
})

# Retrieve full conversation
messages = nebula.get_conversation_messages(conv_id)
```

```typescript
// JavaScript
const convId = await nebula.storeMemory({
  collection_id: 'support', content: 'Hello!', role: 'assistant'
});
await nebula.storeMemory({
  memory_id: convId, collection_id: 'support',
  content: 'I need help', role: 'user'
});
const messages = await nebula.getConversationMessages(convId);
```

## Search with Filters

```python
results = nebula.search(
    query="bug reports",
    collection_ids=["issues"],
    filters={
        "severity": {"$in": ["critical", "high"]},
        "status": {"$ne": "closed"}
    },
    effort="medium"
)
```

Operators: `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`, `$like`, `$ilike`, `$overlap`, `$contains`, `$and`, `$or`. Prefix metadata fields with `metadata.` in REST API.

For full filter reference, see [references/search-and-filtering.md](references/search-and-filtering.md).

## Reference Files

Load these as needed for detailed API information:

- **[references/python-sdk.md](references/python-sdk.md)**: Full Python SDK reference (sync + async clients, all methods, error handling)
- **[references/javascript-sdk.md](references/javascript-sdk.md)**: Full JavaScript/TypeScript SDK reference (all methods, Memory helpers, error handling)
- **[references/search-and-filtering.md](references/search-and-filtering.md)**: Search configuration, hybrid weights, effort levels, metadata filter operators, authority scores
- **[references/mcp-setup.md](references/mcp-setup.md)**: MCP server setup for Cursor, VS Code, Windsurf, Claude Desktop, Claude Code
- **[references/rest-api.md](references/rest-api.md)**: Direct HTTP/cURL API reference for all endpoints
