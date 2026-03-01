---
name: memory-lancedb-pro
description: "Comprehensive guide for maintaining, debugging, and upgrading the memory-lancedb-pro OpenClaw plugin — an enhanced LanceDB-backed long-term memory system with hybrid retrieval (Vector + BM25), cross-encoder reranking, multi-scope isolation, noise filtering, adaptive retrieval, and a management CLI. Use this skill when: (1) developing new features or fixing bugs in memory-lancedb-pro, (2) modifying the retrieval pipeline (vector search, BM25, RRF fusion, reranking, scoring stages), (3) adding or changing embedding providers, (4) updating scope/access control logic, (5) modifying agent tools or CLI commands, (6) troubleshooting memory quality issues (noise, duplicates, low recall), (7) working on the JSONL session distillation pipeline, (8) migrating data between memory backends, or (9) understanding the plugin's architecture to plan enhancements."
---

# memory-lancedb-pro Plugin Maintenance Guide

## Overview

**memory-lancedb-pro** is an enhanced long-term memory plugin for [OpenClaw](https://github.com/openclaw/openclaw). It replaces the built-in `memory-lancedb` plugin with advanced retrieval capabilities, multi-scope memory isolation, and a management CLI.

**Repository**: https://github.com/win4r/memory-lancedb-pro
**License**: MIT | **Language**: TypeScript (ESM) | **Runtime**: Node.js via OpenClaw Gateway

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   index.ts (Entry Point)                │
│  Plugin Registration · Config Parsing · Lifecycle Hooks │
└────────┬──────────┬──────────┬──────────┬───────────────┘
         │          │          │          │
    ┌────▼───┐ ┌────▼───┐ ┌───▼────┐ ┌──▼──────────┐
    │ store  │ │embedder│ │retriever│ │   scopes    │
    │ .ts    │ │ .ts    │ │ .ts    │ │    .ts      │
    └────────┘ └────────┘ └────────┘ └─────────────┘
         │                     │
    ┌────▼───┐           ┌─────▼──────────┐
    │migrate │           │noise-filter.ts │
    │ .ts    │           │adaptive-       │
    └────────┘           │retrieval.ts    │
                         └────────────────┘
    ┌─────────────┐   ┌──────────┐
    │  tools.ts   │   │  cli.ts  │
    │ (Agent API) │   │ (CLI)    │
    └─────────────┘   └──────────┘
```

## File Reference (Quick Navigation)

| File | Purpose | Key Exports |
|------|---------|-------------|
| `index.ts` | Plugin entry point. Registers with OpenClaw Plugin API, parses config, mounts lifecycle hooks | `memoryLanceDBProPlugin` (default), `shouldCapture`, `detectCategory` |
| `openclaw.plugin.json` | Plugin metadata + full JSON Schema config with `uiHints` | — |
| `package.json` | NPM package. Deps: `@lancedb/lancedb`, `openai`, `@sinclair/typebox` | — |
| `cli.ts` | CLI: `memory-pro list/search/stats/delete/delete-bulk/export/import/reembed/migrate` | `createMemoryCLI`, `registerMemoryCLI` |
| `src/store.ts` | LanceDB storage layer. Table creation, FTS indexing, CRUD, vector/BM25 search | `MemoryStore`, `MemoryEntry`, `loadLanceDB` |
| `src/embedder.ts` | Embedding abstraction. OpenAI-compatible API, task-aware, LRU cache | `Embedder`, `createEmbedder`, `getVectorDimensions` |
| `src/retriever.ts` | Hybrid retrieval engine. Full scoring pipeline | `MemoryRetriever`, `createRetriever`, `DEFAULT_RETRIEVAL_CONFIG` |
| `src/scopes.ts` | Multi-scope access control | `MemoryScopeManager`, `createScopeManager` |
| `src/tools.ts` | Agent tool definitions: `memory_recall/store/forget/update/stats/list` | `registerAllMemoryTools` |
| `src/noise-filter.ts` | Noise filter for low-quality content | `isNoise`, `filterNoise` |
| `src/adaptive-retrieval.ts` | Skip retrieval for greetings, commands, emoji | `shouldSkipRetrieval` |
| `src/migrate.ts` | Migration from legacy `memory-lancedb` | `MemoryMigrator`, `createMigrator` |
| `scripts/jsonl_distill.py` | JSONL session distillation script (Python) | — |

## Core Subsystem Reference

For detailed deep-dives into each subsystem, read the appropriate reference file:

- **Retrieval Pipeline** (scoring math, RRF fusion, reranking, all scoring stages): See [references/retrieval_pipeline.md](references/retrieval_pipeline.md)
- **Storage & Data Model** (LanceDB schema, FTS indexing, CRUD, vector dim): See [references/storage_and_schema.md](references/storage_and_schema.md)
- **Embedding System** (providers, task-aware API, caching, dimensions): See [references/embedding_system.md](references/embedding_system.md)
- **Plugin Lifecycle & Config** (hooks, registration, config parsing): See [references/plugin_lifecycle.md](references/plugin_lifecycle.md)
- **Scope System** (multi-scope isolation, agent access, patterns): See [references/scope_system.md](references/scope_system.md)
- **Tools & CLI** (agent tools, CLI commands, parameters): See [references/tools_and_cli.md](references/tools_and_cli.md)
- **Common Gotchas & Troubleshooting**: See [references/troubleshooting.md](references/troubleshooting.md)

## Development Workflows

### Adding a New Embedding Provider

1. Check if it's OpenAI-compatible (most are). If so, no code change needed — just config
2. If the model is not in `EMBEDDING_DIMENSIONS` map in `src/embedder.ts`, add it
3. If the provider needs special request fields beyond `task` and `normalized`, extend `buildPayload()` in `src/embedder.ts`
4. Test with `embedder.test()` method
5. Document the provider in README.md table

### Adding a New Rerank Provider

1. Add provider name to `RerankProvider` type in `src/retriever.ts`
2. Add case in `buildRerankRequest()` for request format (headers + body)
3. Add case in `parseRerankResponse()` for response parsing
4. Add to `rerankProvider` enum in `openclaw.plugin.json`
5. Test with actual API calls — reranker has 5s timeout protection

### Adding a New Scoring Stage

1. Create a `private apply<StageName>(results: RetrievalResult[]): RetrievalResult[]` method in `MemoryRetriever`
2. Add corresponding config fields to `RetrievalConfig` interface
3. Insert the stage in the pipeline sequence in both `hybridRetrieval()` and `vectorOnlyRetrieval()`
4. Add defaults to `DEFAULT_RETRIEVAL_CONFIG`
5. Add JSON Schema fields to `openclaw.plugin.json`
6. Pipeline order: Fusion → Rerank → Recency → Importance → LengthNorm → TimeDecay → HardMin → Noise → MMR

### Adding a New Agent Tool

1. Create `registerMemory<ToolName>Tool()` in `src/tools.ts`
2. Define parameters with `Type.Object()` from `@sinclair/typebox`
3. Use `stringEnum()` from `openclaw/plugin-sdk` for enum params
4. Always validate scope access via `context.scopeManager`
5. Register in `registerAllMemoryTools()` — decide if core (always) or management (optional)
6. Return `{ content: [{ type: "text", text }], details: {...} }`

### Adding a New CLI Command

1. Add command in `registerMemoryCLI()` in `cli.ts`
2. Pattern: `memory.command("name <args>").description("...").option("--flag", "...").action(async (args, opts) => { ... })`
3. Support `--json` flag for machine-readable output
4. Use `process.exit(1)` for error cases
5. CLI is registered via `api.registerCli()` in `index.ts`

### Modifying Auto-Capture Logic

1. `shouldCapture(text)` in `index.ts` controls what gets auto-captured
2. `MEMORY_TRIGGERS` regex array defines trigger patterns (supports EN/CJK)
3. `detectCategory(text)` classifies captures as preference/fact/decision/entity/other
4. Auto-capture runs in `agent_end` hook, limited to 3 per turn
5. Duplicate detection threshold: cosine similarity > 0.95

### Modifying Auto-Recall Logic

1. Auto-recall uses `before_agent_start` hook (OFF by default)
2. `shouldSkipRetrieval()` from `src/adaptive-retrieval.ts` gates retrieval
3. Injected as `<relevant-memories>` XML block with UNTRUSTED DATA warning
4. `sanitizeForContext()` strips HTML, newlines, limits to 300 chars per memory
5. Max 3 memories injected per turn

## Key Design Decisions

- **autoRecall defaults to OFF** — prevents model from echoing injected memory context
- **autoCapture defaults to ON** — transparent memory accumulation
- **sessionMemory defaults to OFF** — raw session summaries degrade retrieval quality; use JSONL distillation instead
- **LanceDB dynamic import** — loaded asynchronously to avoid blocking; cached in singleton promise
- **Startup checks are fire-and-forget** — gateway binds HTTP port immediately; embedding/retrieval tests run in background with 8s timeout
- **Daily JSONL backup** — 24h interval, keeps last 7 files, runs 1 min after start
- **BM25 score normalization** — raw BM25 scores are unbounded, normalized with sigmoid: `1 / (1 + exp(-score/5))`
- **Update = delete + re-add** — LanceDB doesn't support in-place updates
- **ID prefix matching** — 8+ hex char prefix resolves to full UUID for user convenience
- **CJK-aware thresholds** — shorter minimum lengths for Chinese/Japanese/Korean text (4–6 chars vs 10–15 for English)
- **Env var resolution** — `${VAR}` syntax resolved at config parse time; gateway service may not inherit shell env

## Testing

- Smoke test: `node test/cli-smoke.mjs`
- Manual verification: `openclaw plugins doctor`, `openclaw memory-pro stats`
- Embedding test: `embedder.test()` returns `{ success, dimensions, error? }`
- Retrieval test: `retriever.test()` returns `{ success, mode, hasFtsSupport, error? }`
