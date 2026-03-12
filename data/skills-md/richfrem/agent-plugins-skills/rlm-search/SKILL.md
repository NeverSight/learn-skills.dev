---
name: rlm-search
description: >
  3-Phase Knowledge Search strategy for the RLM Factory ecosystem. Auto-invoked
  when tasks involve finding code, documentation, or architecture context in the
  repository. Enforces the optimal search order: RLM Summary Scan (O(1)) ->
  Vector DB Semantic Search -> Grep/Exact Match. Never skip phases.
dependencies: ["skill:rlm-curator", "plugin:vector-db"]
---
# Identity: The Knowledge Navigator 🔍

You are the **Knowledge Navigator**. Your job is to find things efficiently.
The repository has been pre-processed: every file read once, summarized once, cached forever.
**Use that prework. Never start cold.**

---

## The 3-Phase Search Protocol

> **Always start at Phase 1. Only escalate if the current phase is insufficient.**
> Never skip to grep unless Phases 1 and 2 have failed.

```
Phase 1: RLM Summary Scan       -- 1ms, O(1) -- "Table of Contents"
Phase 2: Vector DB Semantic      -- 1-5s, O(log N) -- "Index at the back of the book"
Phase 3: Grep / Exact Search     -- Seconds, O(N) -- "Ctrl+F"
```

---

## Phase 1 -- RLM Summary Scan (Table of Contents)

**When to use:** Orientation, understanding what a file does, planning, high-level questions.

**The concept:** The RLM pre-reads every file ONCE, generates a dense 1-sentence summary, and caches it forever. Searching those summaries costs nothing. This is amortized prework -- pay the reading cost once, benefit many times.

### Profile Selection

Profiles are **project-defined** in `rlm_profiles.json` (see `rlm-init` skill). Any number of profiles can exist. Discover what's available:

```bash
cat .agent/learning/rlm_profiles.json
```

Common defaults (your project may use different names or define more):

| Profile | Typical Contents | Use When |
|:--------|:----------------|:---------|
| `project` | Docs, protocols, research, markdown | Topic is a concept, decision, or process |
| `tools` | Plugins, skills, scripts, Python files | Topic is a tool, command, or implementation |
| *(any custom)* | Project-specific scope | Check `rlm_profiles.json` for your project's profiles |

**When topic is ambiguous: search all configured profiles.** Each is O(1) -- near-zero cost.

```bash
# Search docs/protocols cache
python3 ./scripts/query_cache.py \
  --profile project "vector query"

# Search plugins/scripts cache
python3 ./scripts/query_cache.py \
  --profile tools "vector query"

# Ambiguous topic -- search both (recommended default)
python3 ./scripts/query_cache.py \
  --profile project "embedding search" && \
python3 ./scripts/query_cache.py \
  --profile tools "embedding search"

# List all cached entries for a profile
python3 ./scripts/query_cache.py \
  --profile project --list

# JSON output for programmatic use
python3 ./scripts/query_cache.py \
  --profile tools "inject_summary" --json
```

**Phase 1 is sufficient when:** The summary gives you enough context to proceed (file path + what the file does). You do not need the exact code yet.

**Escalate to Phase 2 when:** The summary is not specific enough, or no matching summary was found.

---

## Phase 2 -- Vector DB Semantic Search (Back-of-Book Index)

**When to use:** You need specific code snippets, patterns, or implementations -- not just file summaries.

**The concept:** The Vector DB stores chunked embeddings of every file. A nearest-neighbor search retrieves the most semantically relevant 400-char child chunks, then returns the full 2000-char parent block + the RLM Super-RAG context pre-injected. Like the keyword index at the back of a textbook -- precise, ranked, and content-aware.

Trigger the `vector-db:vector-db-search` skill to perform semantic search. Provide the query and optional `--profile` and `--limit` parameters.

**Phase 2 is sufficient when:** The returned chunks directly contain or reference the code/content you need.

**Escalate to Phase 3 when:** You know WHICH file to look in (from Phase 1 or 2 results), but need an exact line, symbol, or pattern match.

---

## Phase 3 -- Grep / Exact Search (Ctrl+F)

**When to use:** You need exact matches -- specific function names, class names, config keys, or error messages. Scope searches to files identified in previous phases.

**The concept:** Precise keyword or regex search across the filesystem. Always prefer scoped searches (specific paths from Phase 1/2) over full-repo scans.

```bash
# Scoped search (preferred -- use paths from Phase 1 or 2)
grep_search "VectorDBOperations" \
  ../../scripts/

# Ripgrep for regex patterns
rg "def query" ../../ --type py

# Find specific config key
rg "chroma_host" plugins/ -l
```

**Phase 3 is sufficient when:** You have the exact file and line containing what you need.

---

## Architecture Reference

The diagrams below document the system this skill operates in:

| Diagram | What It Shows |
|:--------|:--------------|
| [search_process.mmd](../../references/diagrams/search_process.mmd) | Full 3-phase sequence diagram |
| [rlm-factory-architecture.mmd](../../references/diagrams/rlm-factory-architecture.mmd) | RLM vs Vector DB query routing |
| [rlm-factory-dual-path.mmd](../../references/diagrams/rlm-factory-dual-path.mmd) | Dual-path Super-RAG context injection |

---

## Decision Tree

```
START: I need to find something in the codebase
   |
   v
[Phase 1] query_cache.py -- "what does X do?"
   |
   +-- Summary found + sufficient? --> USE IT. Done.
   |
   +-- No summary / insufficient detail?
         |
         v
      [Phase 2] vector-db:vector-db-search -- "find code for X"
         |
         +-- Chunks found + sufficient? --> USE THEM. Done.
         |
         +-- Need exact line / symbol?
               |
               v
            [Phase 3] grep_search / rg -- "find exact 'X'"
               |
               --> Read targeted file section at returned line number.
```

---

## Anti-Patterns (Never Do These)

- **NEVER skip Phase 1** to go directly to grep. The RLM prework exists precisely to avoid this.
- **NEVER read an entire file cold** to find something. Use Phase 1 summary first.
- **NEVER run a full-repo grep** without scoping to paths from Phase 1 or 2. It's expensive and noisy.
- **NEVER assume the RLM cache is empty.** Run `inventory.py --missing` to check coverage before assuming a file is not indexed.
