---
name: moorcheh
description: Use this skill to interact with Moorcheh, the Universal Memory Layer for Agentic AI. Provides semantic search with ITS (Information-Theoretic Scoring), namespace management, text and vector data operations, and AI-powered answer generation (RAG). Use when building applications that need semantic search, knowledge bases, document Q&A, AI memory systems, or retrieval-augmented generation.
---

# Moorcheh — Universal Memory Layer Operations

This skill provides comprehensive access to the Moorcheh platform including namespace management, data operations, semantic search with ITS scoring, and AI-powered answer generation.

## Moorcheh Account

If the user does not have an account yet, direct them to the console to register and create a free account.

Create a Moorcheh account at [console.moorcheh.ai](https://console.moorcheh.ai).

## Environment Variables

```bash
export MOORCHEH_API_KEY="your-api-key-here"
```

For full environment setup, see [Environment Requirements](references/environment_requirements.md).

## Script Index

### Namespace Management

- [Create Namespace](references/create_namespace.md): Use to **create a new text or vector namespace** for organizing data. Text namespaces handle automatic embedding; vector namespaces require pre-computed embeddings.
- [List Namespaces](references/list_namespaces.md): Use to **discover what namespaces exist** in the account. This should be the first step before any operation.
- [Delete Namespace](references/delete_namespace.md): Use to **permanently remove a namespace** and all its data. This action is irreversible.

### Data Operations

- [Upload Text Data](references/upload_text.md): Use to **upload text documents with metadata** to a text namespace. Documents are automatically embedded and indexed for semantic search.
- [Upload Vectors](references/upload_vectors.md): Use to **upload pre-computed vector embeddings** to a vector namespace. Best when you have your own embedding pipeline.
- [Delete Data](references/delete_data.md): Use to **remove specific documents or vectors** from a namespace.
- [Create Example Data](references/example_data.md): Use to **create sample data for demos and testing** when no data is available.

### Search & AI

- [Semantic Search](references/search.md): **Primary search operation.** Performs semantic search across one or more namespaces using ITS scoring. Supports text queries, metadata filters, keyword filters, and relevance thresholds.
- [Generate AI Answer](references/generate_answer.md): Use to **generate AI-powered answers from your data (RAG)**. Searches relevant context and synthesizes a natural-language answer. Supports chat history, custom prompts, and structured output.

## Recommendations

- Always run **List Namespaces** first to discover available data before searching or uploading.
- For text data, prefer **text namespaces** — Moorcheh handles embedding automatically.
- Use **ITS scoring thresholds** (0.0–1.0) to control result quality. Higher = stricter matching.
- The **Generate Answer** endpoint is the primary RAG capability — use it for Q&A over documents.

## Output Formats

- Search results include `id`, `score`, `label` (relevance category), `text`, and `metadata`.
- AI answers include `answer`, `model`, `contextCount`, and optional `structuredData`.

## Error Handling

- `401 Unauthorized`: Verify `MOORCHEH_API_KEY` is set and valid
- `404 Namespace not found`: Create the namespace first or check spelling (case-sensitive)
- `400 Vector dimension mismatch`: Ensure vectors match the namespace's configured dimension
- `429 Too Many Requests`: Implement exponential backoff
