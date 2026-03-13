---
name: addon-rag-pdf-pipeline
description: Use when you only need a legacy PDF-only RAG pipeline; prefer addon-rag-ingestion-pipeline for new builds.
---

# Add-on: PDF RAG Pipeline (Legacy Narrow Variant)

Use this skill for PDF-only RAG. For mixed formats (Markdown, text, HTML, CSV), prefer `addon-rag-ingestion-pipeline`.

## Compatibility

- Best with `architect-python-uv-batch` or `architect-python-uv-fastapi-sqlalchemy`.
- Can also support Next.js by keeping ingestion/indexing in a Python worker service.

## Inputs

Collect:
- `DOC_SOURCE`: local folder, object storage, or uploaded files.
- `EMBED_PROVIDER`: `openai` or `sentence-transformers`.
- `VECTOR_STORE`: `pgvector`, `chroma`, or existing store.
- `CHUNK_SIZE`: default `1000`.
- `CHUNK_OVERLAP`: default `150`.

## Integration Workflow

1. Add dependencies (Python worker path):
```bash
uv add pypdf langchain-text-splitters
```
- If `EMBED_PROVIDER=openai`: `uv add openai`
- If `EMBED_PROVIDER=sentence-transformers`: `uv add sentence-transformers`
- If `VECTOR_STORE=chroma`: `uv add chromadb`

2. Add modules:
```text
src/{{MODULE_NAME}}/rag/
  loaders/pdf_loader.py
  chunking.py
  embeddings.py
  indexer.py
  retriever.py
```

3. Standardize record model:
- `document_id`
- `chunk_id`
- `content`
- `embedding`
- `metadata` (filename, page, section, checksum, ingested_at)

4. Implement ingestion command:
```bash
uv run {{PROJECT_NAME}} rag-ingest --source ./data/inbox
```

5. Implement retrieval contract:
- Input: `query`, optional filters, `top_k`.
- Output: ranked chunks with score + citation metadata.

## Required Behaviors

- Deduplicate ingestion using content hash/checksum.
- Preserve citations (`filename`, `page_number`) for each chunk.
- Normalize unicode and whitespace before chunking.
- Keep embedding and retrieval concerns isolated from API/UI.

## Minimal Defaults

### `chunking.py`
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Never interpolate user query into raw SQL for vector search.
- Don’t block API request path with large ingestion jobs; run asynchronously.
- Track embedding model/version in metadata for reindex decisions.
- Keep chunking deterministic to avoid retrieval drift.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
uv run {{PROJECT_NAME}} rag-ingest --source ./data/inbox
uv run {{PROJECT_NAME}} rag-query --q "test query" --top-k 5
uv run pytest -q
```

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
