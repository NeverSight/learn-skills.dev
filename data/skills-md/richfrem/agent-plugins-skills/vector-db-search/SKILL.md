---
name: vector-db-search
description: "Semantic search skill for retrieving code and documentation from the ChromaDB vector store. Use when you need concept-based search across the repository (Phase 2 of the 3-phase search protocol). V2 includes L4/L5 retrieval constraints."
allowed-tools: Bash, Read
dependencies: ["pip:chromadb", "pip:frontmatter", "pip:langchain", "pip:langchain_chroma", "pip:langchain_classic", "pip:langchain_community", "pip:langchain_core", "pip:langchain_huggingface", "pip:langchain_text_splitters", "skill:vector-db-init"]
---
# Vector DB Search

Semantic (meaning-based) search against the ChromaDB vector store.
Use for Phase 2 of the 3-phase search protocol -- after the RLM Summary Ledger (Phase 1)
returns insufficient results.

## Scripts

| Script | Role |
|:-------|:-----|
| `scripts/query.py` | Semantic search -- CLI entry point |
| `scripts/operations.py` | Core Parent-Child retrieval library |
| `scripts/vector_config.py` | Profile config helper (`vector_profiles.json`) |
| `scripts/vector_consistency_check.py` | Integrity validation |

**Write operations** (ingest, cleanup) are handled by dedicated agents: `vdb-ingest`, `vdb-cleanup`.

## When to Use

- Phase 1 (RLM Summary Ledger) returned no match or insufficient detail
- User asks "how does X work?" / "find code that does Y"
- You need specific snippets, not just file-level summaries

## Execution Protocol

### 1. Verify ChromaDB is running

```bash
curl -sf http://127.0.0.1:8110/api/v1/heartbeat
```

If connection refused: run `vector-db-launch` skill (`plugins/vector-db/skills/vector-db-launch/SKILL.md`).
For first-time setup: run `vector-db-init` skill (`plugins/vector-db/skills/vector-db-init/scripts/init.py`).

### 2. Select Profile and Search

Profiles are **project-defined** in `vector_profiles.json` (see `vector-db-init` skill). Any number can exist. Discover what's available:

```bash
cat .agent/learning/vector_profiles.json
```

Common default is `knowledge` -- your project may define more (e.g. separate profiles for code vs docs). When topic is ambiguous, search all profiles.

```bash
python3 ./scripts/query.py \
  "your natural language question" --profile knowledge --limit 5
```

Results include ranked parent chunks with RLM Super-RAG context pre-injected.


## Architectural Constraints (Electric Fence)

### NEVER -- direct database reads
Do **not** `cat`, `strings`, or `sqlite3` the `.vector_data/` directory.
Binary blobs will corrupt your context window and the retrieval pipeline.

### ALWAYS -- use the API
All access goes through `query.py`. No exceptions.

### Source Transparency Declaration (L5 Pattern)
When search returns empty results, explicitly state:
```
> Not Found in Vector Store
> Searched profile: [profile_name] for "[query]"
> Profile covers: [scope]
> Not searched: [out-of-scope areas]
```
