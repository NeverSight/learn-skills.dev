---
name: agently-knowledge-base
description: Use when the user wants embeddings, vector indexing, retrieval, or retrieval-backed answers, including embedding-agent setup, Chroma-backed collections, collection add/query, and KB-to-answer flows.
---

# Agently Knowledge Base

Use this skill when embeddings and retrieval are the main capability surface.

## Native-First Rules

- prefer embedding-agent plus Chroma integration before custom vector plumbing
- separate indexing, retrieval, and answer generation concerns
- keep retrieval results explicit when they feed a later request

## Anti-Patterns

- do not hide KB retrieval inside unrelated prompt logic
- do not treat embeddings-only setup and KB-backed answer flow as unrelated stacks

## Read Next

- `references/overview.md`
