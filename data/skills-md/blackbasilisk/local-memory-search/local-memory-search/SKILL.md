---
name: local-memory-search
description: Local, offline semantic search over OpenClaw memory files (MEMORY.md and memory/*.md) using Python embeddings + FAISS (no online LLM/API). Use when Dave asks for "memory search" without cloud billing, wants semantic recall across notes, or wants to share a reusable local-memory semantic search skill.
---

# Local Memory Search (offline)

This skill adds a **local semantic search** workflow for OpenClaw memory files:

- `MEMORY.md`
- `memory/*.md`

It builds a local vector index (FAISS) using a small sentence-transformers embedding model.

## Requirements

- Python 3.10+ in PATH (`python --version`)

## Choose your backend (user choice)

### A) Light (recommended): `lsa` (TF‑IDF + SVD)

- No neural model
- No HuggingFace downloads
- Good “semantic-ish” matching (better than plain keyword search)

```powershell
cd $env:USERPROFILE\.openclaw\workspace\skills\local-memory-search
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -r .\scripts\requirements-lsa.txt
```

### B) Heavy (best semantic): `sentence-transformers` (Torch)

- True neural embeddings
- Bigger install (torch) + model download

```powershell
cd $env:USERPROFILE\.openclaw\workspace\skills\local-memory-search
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -r .\scripts\requirements-sentence-transformers.txt
```

## Build / refresh the index

Default (light LSA backend):

```powershell
.\.venv\Scripts\python.exe .\scripts\index_memory.py --workspace "$env:USERPROFILE\.openclaw\workspace" --backend lsa
```

Heavy backend example:

```powershell
.\.venv\Scripts\python.exe .\scripts\index_memory.py --workspace "$env:USERPROFILE\.openclaw\workspace" --backend sentence-transformers --model "sentence-transformers/all-MiniLM-L6-v2"
```

## Default workflow: jump + quote (recommended)

This matches the recommended operational pattern:

1) semantic jump to the best chunk
2) open the source file
3) print exact lines (with a little context)

```powershell
# Minimal output (default): prints just the best-matching lines
.\.venv\Scripts\python.exe .\scripts\jump_memory.py --query "o365 timezone config" --top 1

# If you want provenance:
.\.venv\Scripts\python.exe .\scripts\jump_memory.py --query "o365 timezone config" --top 1 --show-source --show-line-numbers --context 2

Tip: for cleaner quotes, re-index with default overlap 0 (the default).
```

## Search (semantic only)

```powershell
.\.venv\Scripts\python.exe .\scripts\search_memory.py --query "o365 timezone config" --top 5
```

If your index was built with a different backend/model, `search_memory.py` will automatically use the index metadata. You can override:

```powershell
.\.venv\Scripts\python.exe .\scripts\search_memory.py --backend fastembed --model "BAAI/bge-small-en-v1.5" --query "..."
```

## Notes

- Index is stored under: `~/.openclaw/credentials/local-memory-search/`
- Re-run indexing after you edit memory files.
- This is a local alternative to OpenClaw's built-in `memory_search` tool.
