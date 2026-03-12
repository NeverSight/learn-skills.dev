---
name: memory-management
description: "Tiered memory system for cognitive continuity across agent sessions. Manages hot cache (session context loaded at boot) and deep storage (loaded on demand). Use when: (1) starting a session and loading context, (2) deciding what to remember vs forget, (3) promoting/demoting knowledge between tiers, (4) user says 'remember this' or asks about project history."
allowed-tools: Read, Write
---
# Memory Management

Tiered memory system that makes an AI agent a continuous collaborator across sessions.

## Architecture

The memory system has six tiers, configurable per project:

```
Tier 1: HOT CACHE (always loaded at boot -- ~200 lines target)
+-- <primer_file>             Role, identity, constraints
+-- <boot_digest_file>        Tactical status, active tasks
+-- <boot_contract_file>      Immutable constraints
+-- <snapshot_file>           Cognitive Hologram (1 sentence per file)

Tier 2: RLM SUMMARY LEDGER (fast keyword lookup -- loaded on demand)
+-- <summary_cache_file>      Pre-generated text summaries: docs, protocols, research
                              Plugin: rlm-factory | Skill: rlm-search | Profile: project
+-- <tool_cache_file>         Pre-generated text summaries: plugins, skills, scripts
                              Plugin: rlm-factory | Skill: rlm-search | Profile: tools

Tier 3: VECTOR STORE (semantic embedding search -- loaded on demand)
+-- <vector_db_backend>       ChromaDB via vector-db plugin / vector-db-agent skill
                              Profile: knowledge | Port: configured in vector_profiles.json

Tier 4: DEEP STORAGE (filesystem -- authoritative source, loaded on demand)
+-- <domain_data_dir>/        Research topics: {topic}/analysis.md
+-- <design_docs_dir>/        ADRs, RFCs
+-- <governance_dir>/         Protocols, playbooks

Tier 5: VAULT (Obsidian -- linked knowledge graph, loaded on demand)
+-- <vault_dir>/              Plugin: obsidian-integration
                              Skills: obsidian-vault-crud, obsidian-canvas-architect,
                                      obsidian-graph-traversal, obsidian-bases-manager
                              Env: VAULT_PATH or OBSIDIAN_VAULT_PATH

Tier 6: SOUL (external persistence -- optional, synced at session seal)
+-- <traces_file>             Plugin: project-specific (e.g. huggingface-utils)
                              e.g. lineage/, data/, soul_traces.jsonl on HF Hub
```

Projects define their own file paths for each slot. Tiers may be omitted or added based on project complexity.

## Lookup Flow (3-Phase Search Protocol)

When searching for information, ALWAYS escalate in order. Never skip ahead.

```
Query arrives ->
1. HOT CACHE                     Instant. Boot files cover ~90% of context needs.
2. DEEP STORAGE (topic/decision) Load specific domain dir or design doc by subject.
3. RLM SUMMARY LEDGER (Phase 1)  Keyword search via rlm-factory:rlm-search skill.
4. VECTOR STORE (Phase 2)        Semantic search via vector-db:vector-db-search skill.
5. GREP / EXACT SEARCH (Phase 3) rg/grep scoped to paths from Steps 3 or 4.
6. Ask user                      Unknown? Learn it and persist it.
```

### Phase 1 -- RLM Summary Scan (Table of Contents)

RLM is **amortized prework**: each file read ONCE, summarized ONCE, cached as plain text JSON.
Searching summaries is O(1) keyword lookup -- no embeddings, no inference.

Trigger the `rlm-factory:rlm-search` skill, providing the profile and search term.

**Use Phase 1 when:** You need to understand what a file does, find which file owns a feature,
or navigate the codebase without reading individual files.

**Escalate to Phase 2 when:** The summary is insufficient or no match found.

### Phase 2 -- Vector Store Semantic Search (Back-of-Book Index)

Embedding-based nearest-neighbor search across all indexed chunks. Returns ranked
parent chunks with RLM Super-RAG context pre-injected.

Trigger the `vector-db:vector-db-search` skill, providing the query, profile, and limit.

**Use Phase 2 when:** You need specific code snippets, patterns, or implementations.

**Escalate to Phase 3 when:** You have a file path (from Phase 1 or 2) and need an exact line.

### Phase 3 -- Grep / Exact Search (Ctrl+F)

Precise keyword or regex match. Always scope to paths discovered in earlier phases.

```bash
# Scoped to a specific path (use paths from Phase 1/2)
grep_search "VectorDBOperations" ../../skills/

# Ripgrep for regex
rg "def query" ../../ --type py
```

**Anti-patterns:** Never run a full-repo grep without scoping. Never skip Phase 1.

## Dependencies

### `rlm-factory` -- RLM Summary Ledger (Tier 2)

| Component | Value |
|:----------|:------|
| **Plugin** | `plugins/rlm-factory/` |
| **Skill (write)** | `skills/rlm-curator/` -- distill, inject, audit, cleanup |
| **Skill (read)** | `skills/rlm-search/` -- query the ledger |
| **Skill (Phase 1 search)** | `rlm-factory:rlm-search` |
| **Skill (write/inject)** | `rlm-factory:rlm-curator` |
| **Skill (audit coverage)** | `rlm-factory:rlm-curator` |
| **Skill (shared config)** | `rlm-factory:rlm-curator` |
| **Cache files** | `.agent/learning/rlm_summary_cache.json` (docs), `.agent/learning/rlm_tool_cache.json` (tools) |

### `vector-db` -- Vector Store (Tier 3)

| Component | Value |
|:----------|:------|
| **Plugin** | `plugins/vector-db/` |
| **Skill** | `skills/vector-db-agent/` -- ingest, query, operations |
| **Skill (Phase 2 search)** | `vector-db:vector-db-search` |
| **Skill (ingest files)** | `vector-db:vector-db-ingest` |
| **Skill (operations)** | `vector-db:vector-db-search` |
| **Skill (config)** | `vector-db:vector-db-search` |
| **Backend** | ChromaDB (`chromadb.HttpClient` with `PersistentClient` fallback) |

### `obsidian-integration` -- Linked Vault (Tier 5)

| Component | Value |
|:----------|:------|
| **Plugin** | `plugins/obsidian-integration/` |
| **Skill: vault setup** | `skills/obsidian-init/` -- prerequisites, `.obsidian/` config, exclusion filters |
| **Skill: read/write notes** | `obsidian-integration:obsidian-vault-crud` -- atomic create/read/update/append |
| **Skill: CRUD operations** | `obsidian-integration:obsidian-vault-crud` |
| **Skill: parse markdown** | `obsidian-integration:obsidian-vault-crud` -- shared markdown parser |
| **Requires** | `pip:ruamel.yaml` (lossless YAML frontmatter), Obsidian Desktop |
| **Env** | `VAULT_PATH` -- absolute path to the vault root |

## Promotion / Demotion Rules

### Promote to Hot Cache when:
- Knowledge is referenced in 3+ consecutive sessions
- It's critical for active work (current spec, active protocol)
- It's a constraint or identity anchor

### Demote to Deep Storage when:
- Spec/feature is completed and merged
- Governing document is superseded by newer version
- Topic research is concluded
- Technical decision is ratified (move from draft to archive)

### What Goes Where

| Type | Hot Cache | On-Demand Tier |
|------|-----------|----------------|
| Active tasks | Boot digest | -- |
| Identity/role | Primer file | -- |
| Constraints | Boot contract | -- |
| Session state | Snapshot file | Tier 6 Soul (traces) |
| Research topics | Summary in snapshot | Tier 4: `domain_data_dir/{name}/` |
| Design decisions | Referenced by ID | Tier 4: `design_docs_dir/{id}_{name}.md` |
| Governing docs | Referenced by ID | Tier 4: `governance_dir/{id}_{name}.md` |
| Plugins/scripts/tools | -- | Tier 2: RLM Summary Ledger (tool cache) |
| Docs/protocols/research | -- | Tier 2: RLM Summary Ledger (summary cache) |
| System docs | -- | Tier 2 RLM + Tier 3 Vector Store |
| Linked notes, canvases | -- | Tier 5: Vault (Obsidian) |
| External persistence | -- | Tier 6: Soul (HuggingFace or equivalent) |

## Session Memory Workflow

### At Session Start (Boot)
1. Load hot cache files in order (primer -> contract -> digest -> snapshot)
2. Integrity check validates snapshot is current
3. If snapshot stale -> flag for refresh at session end

### During Session
- **New learning** -> Write to `<domain_data_dir>/{topic}/`
- **New decision** -> Create design document draft
- **New tool** -> Register in tool inventory
- **Correction** -> Update relevant file + note in disputes log if contradicting

### At Session End (Seal)
1. Update snapshot file with new content learned this session
2. Seal validates no drift since last audit
3. Persist traces to external storage (if configured)

## Conventions
- **Hot cache target**: ~200 lines total across all boot files
- **Snapshot**: 1 sentence per file, machine-readable
- **Topic folders**: `lowercase-hyphens/`
- **Document numbering**: 3-digit, sequential
- **Always capture** corrections and contradictions in a disputes log

## Configuration

Projects configure the memory system by setting file paths in their project-specific plugin:

| Variable | Purpose |
|:---------|:--------|
| `MEMORY_PRIMER_FILE` | Path to cognitive primer / role definition |
| `MEMORY_BOOT_DIGEST` | Path to tactical boot digest |
| `MEMORY_BOOT_CONTRACT` | Path to immutable constraints |
| `MEMORY_SNAPSHOT_FILE` | Path to learning snapshot (hologram) |
| `MEMORY_DOMAIN_DIR` | Directory for domain research |
| `MEMORY_DESIGN_DIR` | Directory for design docs (e.g. ADRs) |
| `MEMORY_GOVERNANCE_DIR` | Directory for governing docs (e.g. Protocols) |

## Architecture Diagrams

| Diagram | What It Shows |
|:--------|:--------------|
| [memory_architecture.mmd](references/diagrams/architecture/memory_architecture.mmd) | Full 4-tier memory system with exact plugin/skill/script names per tier |
| [memory_lookup_flow.mmd](references/diagrams/architecture/memory_lookup_flow.mmd) | 3-phase search sequence: Hot Cache -> RLM Ledger -> Vector Store -> Grep |
| [memory_session_lifecycle.mmd](references/diagrams/architecture/memory_session_lifecycle.mmd) | Session Boot -> Active -> Seal lifecycle with all event types |

