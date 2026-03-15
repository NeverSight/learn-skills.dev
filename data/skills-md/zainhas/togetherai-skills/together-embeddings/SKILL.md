---
name: together-embeddings
description: Generate text embeddings and rerank documents via Together AI. Embedding models include BGE, GTE, E5, UAE families. Reranking via MixedBread reranker. Use when users need text embeddings, vector search, semantic similarity, document reranking, RAG pipeline components, or retrieval-augmented generation.
---

# Together Embeddings & Reranking

## Overview

Generate vector embeddings for text and rerank documents by relevance.

- Embeddings endpoint: `/v1/embeddings`
- Rerank endpoint: `/v1/rerank`

## Installation

```shell
# Python (recommended)
uv init  # optional, if starting a new project
uv add together
```

```shell
# or with pip
pip install together
```

```shell
# TypeScript / JavaScript
npm install together-ai
```

Set your API key:

```shell
export TOGETHER_API_KEY=<your-api-key>
```

## Embeddings

### Generate Embeddings

```python
from together import Together
client = Together()

response = client.embeddings.create(
    model="BAAI/bge-base-en-v1.5",
    input="What is the meaning of life?",
)
print(response.data[0].embedding[:5])  # First 5 dimensions
```

```typescript
import Together from "together-ai";
const together = new Together();

const response = await together.embeddings.create({
  model: "BAAI/bge-base-en-v1.5",
  input: "What is the meaning of life?",
});
console.log(response.data[0].embedding.slice(0, 5));
```

```shell
curl -X POST "https://api.together.xyz/v1/embeddings" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"BAAI/bge-base-en-v1.5","input":"What is the meaning of life?"}'
```

### Batch Embeddings

```python
texts = ["First document", "Second document", "Third document"]
response = client.embeddings.create(
    model="BAAI/bge-base-en-v1.5",
    input=texts,
)
for i, item in enumerate(response.data):
    print(f"Text {i}: {len(item.embedding)} dimensions")
```

```typescript
import Together from "together-ai";
const together = new Together();

const response = await together.embeddings.create({
  model: "BAAI/bge-base-en-v1.5",
  input: [
    "First document",
    "Second document",
    "Third document",
  ],
});
for (const item of response.data) {
  console.log(`Index ${item.index}: ${item.embedding.length} dimensions`);
}
```

```shell
curl -X POST "https://api.together.xyz/v1/embeddings" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "BAAI/bge-base-en-v1.5",
    "input": [
      "First document",
      "Second document",
      "Third document"
    ]
  }'
```

### Embedding Models

| Model | API String | Dimensions | Max Input |
|-------|-----------|------------|-----------|
| BGE Base EN v1.5 | `BAAI/bge-base-en-v1.5` | 768 | 512 tokens |
| Multilingual E5 Large | `intfloat/multilingual-e5-large-instruct` | 1024 | 514 tokens (recommended) |

## Reranking

Rerank a set of documents by relevance to a query:

```python
response = client.rerank.create(
    model="mixedbread-ai/Mxbai-Rerank-Large-V2",
    query="What is the capital of France?",
    documents=[
        "Paris is the capital of France.",
        "Berlin is the capital of Germany.",
        "London is the capital of England.",
        "The Eiffel Tower is in Paris.",
    ],
)
for result in response.results:
    print(f"Index: {result.index}, Score: {result.relevance_score:.4f}")
```

```typescript
import Together from "together-ai";
const together = new Together();

const documents = [
  "Paris is the capital of France.",
  "Berlin is the capital of Germany.",
  "London is the capital of England.",
  "The Eiffel Tower is in Paris.",
];

const response = await together.rerank.create({
  model: "mixedbread-ai/Mxbai-Rerank-Large-V2",
  query: "What is the capital of France?",
  documents,
  top_n: 2,
});

for (const result of response.results) {
  console.log(`Index: ${result.index}, Score: ${result.relevance_score}`);
}
```

```shell
curl -X POST "https://api.together.xyz/v1/rerank" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mixedbread-ai/Mxbai-Rerank-Large-V2",
    "query": "What is the capital of France?",
    "documents": ["Paris is the capital of France.", "Berlin is the capital of Germany."]
  }'
```

### Rerank Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Rerank model (required) |
| `query` | string | Search query (required) |
| `documents` | string[] or object[] | Documents to rerank (required). Pass objects with named fields for structured documents. |
| `top_n` | int | Return top N results |
| `return_documents` | bool | Include document text in response |
| `rank_fields` | string[] | Fields to use for ranking when documents are JSON objects (e.g., `["title", "text"]`) |

## RAG Pipeline Pattern

```python
# 1. Generate query embedding
query_embedding = client.embeddings.create(
    model="BAAI/bge-base-en-v1.5",
    input="How does photosynthesis work?",
).data[0].embedding

# 2. Retrieve candidates from vector DB (your code)
candidates = vector_db.search(query_embedding, top_k=20)

# 3. Rerank for precision
reranked = client.rerank.create(
    model="mixedbread-ai/Mxbai-Rerank-Large-V2",
    query="How does photosynthesis work?",
    documents=[c.text for c in candidates],
    top_n=5,
)

# 4. Use top results as context for LLM
context = "\n".join([candidates[r.index].text for r in reranked.results])
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": f"Answer based on this context:\n{context}"},
        {"role": "user", "content": "How does photosynthesis work?"},
    ],
)
```

## Resources

- **Model details**: See [references/models.md](references/models.md)
- **Runnable script**: See [scripts/embed_and_rerank.py](scripts/embed_and_rerank.py) — embed, compute similarity, and rerank pipeline (v2 SDK)
- **Runnable script (TypeScript)**: See [scripts/embed_and_rerank.ts](scripts/embed_and_rerank.ts) — minimal OpenAPI `x-codeSamples` extraction for embeddings + rerank (TypeScript SDK)
- **Official docs**: [Embeddings Overview](https://docs.together.ai/docs/embeddings-overview)
- **Official docs**: [Rerank Overview](https://docs.together.ai/docs/rerank-overview)
- **API reference**: [Embeddings API](https://docs.together.ai/reference/embeddings)
- **API reference**: [Rerank API](https://docs.together.ai/reference/rerank)
