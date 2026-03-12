---
name: addon-docling-legal-chunk-embed
description: Use when you need legal PDF to markdown extraction plus clause chunking and embedding prep; pair with addon-rag-ingestion-pipeline and architect-python-uv-batch.
---

# Add-on: Docling Legal Chunk + Embed

Use this skill when a project needs legal-focused document ingestion from PDF into markdown/chunks suitable for retrieval and downstream clause reasoning.

## Compatibility

- Works with `architect-python-uv-batch`.
- Works with `architect-python-uv-fastapi-sqlalchemy` (worker or async job path).
- Commonly paired with `addon-rag-ingestion-pipeline`.

## Inputs

Collect:
- `LEGAL_SOURCE_DIR`: default `data/inbox/legal`.
- `CLAUSE_MAX_CHARS`: default `1400`.
- `CLAUSE_OVERLAP_CHARS`: default `120`.
- `EMBED_PROVIDER`: `sentence-transformers` | `openai`.
- `OUTPUT_MODE`: `markdown+json` (default) | `json-only`.

## Integration Workflow

1. Add dependencies:
```bash
uv add docling orjson
```
- For local embeddings:
```bash
uv add sentence-transformers
```
- For OpenAI embeddings:
```bash
uv add openai
```

2. Add modules:
```text
src/{{MODULE_NAME}}/rag/legal/docling_extract.py
src/{{MODULE_NAME}}/rag/legal/clause_chunk.py
src/{{MODULE_NAME}}/rag/legal/embed_index.py
src/{{MODULE_NAME}}/rag/legal/types.py
```

3. Add CLI commands:
```bash
uv run {{PROJECT_NAME}} legal-extract --source data/inbox/legal --out data/processed/legal
uv run {{PROJECT_NAME}} legal-index --source data/processed/legal --out data/index/legal-index.json
```

4. Enforce clause-aware chunking:
- Prefer section/heading boundaries first (`Article`, `Section`, numbered clauses).
- Fallback to paragraph-level splitting.
- Keep stable clause ids and citation metadata (`source_path`, `page`, `section`, `clause_id`).

## Required Templates

### `src/{{MODULE_NAME}}/rag/legal/types.py`
```python
from pydantic import BaseModel


class LegalClause(BaseModel):
    clause_id: str
    source_path: str
    section: str | None = None
    page: int | None = None
    content: str
    metadata: dict[str, str] = {}
```

### `src/{{MODULE_NAME}}/rag/legal/clause_chunk.py`
```python
import re


SECTION_RE = re.compile(r"^(article|section|clause)\s+[\w.-]+", re.IGNORECASE)


def split_legal_clauses(markdown_text: str, max_chars: int = 1400) -> list[str]:
    blocks = [b.strip() for b in markdown_text.split("\n\n") if b.strip()]
    clauses: list[str] = []
    buf = ""
    for block in blocks:
        is_boundary = bool(SECTION_RE.match(block))
        if is_boundary and buf:
            clauses.append(buf.strip())
            buf = block
            continue
        if len(buf) + len(block) + 2 > max_chars and buf:
            clauses.append(buf.strip())
            buf = block
        else:
            buf = f"{buf}\n\n{block}".strip() if buf else block
    if buf:
        clauses.append(buf.strip())
    return clauses
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Preserve legal ordering and section labels; do not reorder clauses.
- Keep extracted markdown for auditability before embedding.
- Include deterministic clause ids to support re-ingestion idempotency.
- Never drop citation metadata needed for legal review.
- Keep PII handling configurable; redact only when explicitly required.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
uv run {{PROJECT_NAME}} legal-extract --source data/inbox/legal --out data/processed/legal
uv run {{PROJECT_NAME}} legal-index --source data/processed/legal --out data/index/legal-index.json
uv run pytest -q
```
Fallback (`offline-smoke`):
```bash
test -f src/{{MODULE_NAME}}/rag/legal/docling_extract.py
test -f src/{{MODULE_NAME}}/rag/legal/clause_chunk.py
test -f src/{{MODULE_NAME}}/rag/legal/embed_index.py
```

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
