---
name: addon-rag-ingestion-pipeline
description: Use when adding multi-format RAG ingest, chunk, embed, and retrieval pipelines; pair with architect-python-uv-batch or architect-python-uv-fastapi-sqlalchemy.
---

# Add-on: Multi-Format RAG Ingestion Pipeline

Use this skill when an existing project needs RAG ingestion/retrieval across multiple document formats.

## Compatibility

- Works with `architect-python-uv-batch`.
- Works with `architect-python-uv-fastapi-sqlalchemy`.
- Can back a Next.js app via a Python worker service.

## Inputs

Collect:
- `SOURCE_FORMATS`: one or more of `pdf`, `markdown`, `txt`, `html`, `csv`.
- `EMBED_PROVIDER`: `openai` or `sentence-transformers`.
- `VECTOR_STORE`: `pgvector`, `chroma`, or existing vector layer.
- `CHUNK_SIZE`: default `1000`.
- `CHUNK_OVERLAP`: default `150`.
- `TOP_K`: default `5`.

## Integration Workflow

1. Add dependencies (Python worker path):
```bash
uv add pypdf markdown-it-py beautifulsoup4 pandas langchain-text-splitters
```
- If `EMBED_PROVIDER=openai`: `uv add openai`
- If `EMBED_PROVIDER=sentence-transformers`: `uv add sentence-transformers`
- If `VECTOR_STORE=chroma`: `uv add chromadb`

2. Add modules:
```text
src/{{MODULE_NAME}}/rag/
  loaders/pdf_loader.py
  loaders/markdown_loader.py
  loaders/text_loader.py
  loaders/html_loader.py
  loaders/csv_loader.py
  normalize.py
  chunking.py
  embeddings.py
  indexer.py
  retriever.py
```

3. Use a normalized document contract:
- `document_id`
- `source_path`
- `source_type`
- `content`
- `metadata` (filename/page/section/checksum/ingested_at/model_version)

4. Implement ingestion entrypoint:
```bash
uv run {{PROJECT_NAME}} rag-ingest --source ./data/inbox --formats pdf,markdown,txt
```

5. Implement retrieval entrypoint:
```bash
uv run {{PROJECT_NAME}} rag-query --q "question" --top-k 5
```
- Ensure both commands are wired in the project CLI/script entrypoint.
- `rag-query` depends on an existing index from `rag-ingest`; do not run these validation commands in parallel.

## Loader Notes

- PDF: extract per page and keep `page_number` in metadata.
- Markdown: keep heading hierarchy and section anchors in metadata.
- Text: detect encoding fallback (`utf-8`, then `latin-1`).
- HTML: strip script/style tags and preserve title/headings where possible.
- CSV: convert rows into stable textual records with row identifiers.

## Minimal Defaults

### `normalize.py`
```python
import re
import unicodedata


def normalize_text(raw: str) -> str:
    text = unicodedata.normalize("NFKC", raw)
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
```

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


- Deduplicate ingestion by checksum to keep re-runs idempotent.
- Store embedding model/version so re-indexing can be reasoned about.
- Never interpolate user queries into raw SQL vector search.
- Keep ingestion async/offline for large corpora; do not block request-response paths.
- Preserve citation metadata for retrieval (`source_path`, section, page, row id).

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
uv run {{PROJECT_NAME}} rag-ingest --source ./data/inbox --formats pdf,markdown
uv run {{PROJECT_NAME}} rag-query --q "smoke test" --top-k 5
uv run pytest -q
```

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
