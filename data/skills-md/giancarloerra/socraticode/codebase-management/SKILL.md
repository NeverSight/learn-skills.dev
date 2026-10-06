---
name: codebase-management
description: >-
  Set up, index, and manage SocratiCode codebase indexing. Use when the user wants to
  index a project, check infrastructure health, start/stop file watching, configure
  context artifacts, troubleshoot indexing issues, manage the code graph, or any
  SocratiCode administrative task. Activates when the user mentions indexing, setting up
  search, SocratiCode infrastructure, or managing the codebase index.
---

# SocratiCode Management

Set up, index, and manage SocratiCode codebase indexing, file watching, code graphs, and context artifacts.

## First-Time Setup

1. **Check infrastructure**: `codebase_health` — verifies Docker, Qdrant, Ollama/embedding provider, and embedding model
2. **Start indexing**: `codebase_index` — runs in background, returns immediately
3. **Poll progress**: `codebase_status` — call every ~60 seconds until 100% complete
   - This also keeps the MCP connection alive (some hosts disconnect idle connections)
4. **Done**: Graph auto-builds after indexing. In the default watcher mode, the file watcher auto-starts. Ready to search.

On first use, SocratiCode automatically pulls Docker images, starts containers, and downloads the embedding model (~5 min one-time setup).

## Incremental Updates & File Watching

The file watcher keeps the index automatically updated in the default `SOCRATICODE_WATCHER=auto` mode.

- **`codebase_watch { action: "start" }`** — start the watcher (runs catch-up update first)
- **`codebase_watch { action: "stop" }`** — stop the watcher
- **`codebase_watch { action: "status" }`** — list watched projects (including cross-process)
- **`codebase_update`** — manual incremental update (only changed files, synchronous). Usually not needed if watcher is active.

For a deliberate code-index snapshot, configure every MCP process that uses the checkout with `SOCRATICODE_WATCHER=off` and `SOCRATICODE_AUTO_RESUME=off`. Search and graph tools keep reading the existing index and graph; run `codebase_update` and `codebase_graph_build` only when a refresh is wanted. Use watcher mode `manual` instead when explicit `codebase_watch { action: "start" }` should remain available. Never try to restart a watcher whose status says disabled.

With `SOCRATICODE_WATCHER=git`, active indexed checkouts refresh on checked-out ref/HEAD changes, checked every 10 seconds and on search/status/graph requests. No native file watcher starts. Pending or failed refreshes are not current results. Git triggers the update, but the working tree is indexed, including uncommitted edits. Use `codebase_update` for file saves that do not change ref/HEAD. Selecting Git mode does not create a first index. `SOCRATICODE_AUTO_RESUME=off` suppresses startup catch-up, not later Git-triggered updates. A Git diagnostic must not be bypassed by starting a watcher.

## Managing Indexes

- **`codebase_stop`** — gracefully pause in-progress indexing. Current batch finishes and checkpoints. All progress preserved. Resume with `codebase_index`.
- **`codebase_remove`** — delete entire index (destructive). Safely stops watcher, cancels indexing, waits for graph builds.
- **`codebase_prune`** — inventory stored identities; delete one by exact identity, fresh confirmation token and shared-store acknowledgement. Path absence is advisory, never a candidate set.
- **`codebase_list_projects`** — list all indexed projects with metadata, graph info, and artifact status.

## Managing the Code Graph

The dependency graph is auto-built after indexing. In watcher modes `manual` and `off`, graph queries read an existing graph but will ask for an explicit build instead of creating a missing graph as a side effect.

- **`codebase_graph_build`** — manually rebuild (background, async). Poll with `codebase_graph_status`.
- **`codebase_graph_remove`** — delete graph (auto-rebuilds on next `codebase_index`)
- **`codebase_graph_status`** — check build progress or graph readiness

## Context Artifacts Setup

To index non-code knowledge, create `.socraticodecontextartifacts.json` in the project root:

```json
{
  "artifacts": [
    {
      "name": "database-schema",
      "path": "./docs/schema.sql",
      "description": "PostgreSQL schema — all tables, indexes, constraints, foreign keys."
    }
  ]
}
```

Supported types: SQL schemas, OpenAPI/Protobuf API specs, Terraform/CloudFormation configs, Kubernetes manifests, architecture docs, environment configs — any text-based file or directory.

- **`codebase_context_index`** — manually index/re-index all artifacts (usually auto-triggered)
- **`codebase_context_remove`** — remove all indexed artifacts (blocked during indexing)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Docker not available | Install Docker Desktop from https://docker.com, ensure it's running |
| Slow indexing on macOS/Windows | Docker can't use GPU. Install native Ollama from https://ollama.com/download for Metal/CUDA acceleration. Or use cloud embeddings. |
| Want cloud embeddings instead | Set `EMBEDDING_PROVIDER=openai` + `OPENAI_API_KEY`, or `EMBEDDING_PROVIDER=google` + `GOOGLE_API_KEY` |
| Search returns no results | Check `codebase_status` — project may not be indexed. Run `codebase_index`. |
| Stale results | Check `codebase_status`. Run `codebase_update`; start the watcher only when status does not say it is disabled. |
| Indexing was interrupted | Run `codebase_index` again — it resumes from the last checkpoint automatically. |
| Another process is indexing | `codebase_status` detects cross-process indexing. Wait for it, or use `codebase_stop`. |

## Key Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `QDRANT_MODE` | `managed` | `managed` (Docker) or `external` (remote/cloud Qdrant) |
| `QDRANT_URL` | — | Full URL for remote Qdrant (e.g. `https://xyz.cloud.qdrant.io:6333`) |
| `QDRANT_API_KEY` | — | API key for remote Qdrant |
| `EMBEDDING_PROVIDER` | `ollama` | `ollama`, `openai`, or `google` |
| `OPENAI_API_KEY` | — | Required when `EMBEDDING_PROVIDER=openai` |
| `GOOGLE_API_KEY` | — | Required when `EMBEDDING_PROVIDER=google` |
| `OLLAMA_MODE` | `auto` | `auto` (detect native, fallback Docker), `docker`, `external` |
| `EMBEDDING_MODEL` | `nomic-embed-text` | Model name (provider-specific) |
| `SEARCH_DEFAULT_LIMIT` | `10` | Default result limit for codebase_search (1-50) |
| `SEARCH_MIN_SCORE` | `0.10` | Default minimum RRF score threshold (0-1) |
| `MAX_FILE_SIZE_MB` | `5` | Maximum file size for indexing in MB; must be a complete finite number |
| `EXTRA_EXTENSIONS` | — | Additional file extensions to index (e.g. `.tpl,.blade,.hbs`) |
| `SOCRATICODE_WATCHER` | `auto` | `auto`, `manual` (explicit start only), `off` (no watcher), or `git` (ref/HEAD-triggered refresh, no native watcher) |
| `SOCRATICODE_AUTO_RESUME` | — | `all` resumes all stored projects; `off` disables startup catch-up and interrupted-index recovery |

For full parameter details on every tool, see [references/tool-reference.md](references/tool-reference.md).
