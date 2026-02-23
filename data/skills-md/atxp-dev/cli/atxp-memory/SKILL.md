---
name: atxp-memory
description: Agent memory management — cloud backup, restore, and local vector search of .md memory files
compatibility: Requires Node.js >=18 and npx
tags: [memory, search, backup, identity, agent-files, sync, vector-search, zvec]
metadata:
  homepage: https://docs.atxp.ai
  source: https://github.com/atxp-dev/cli
  npm: https://www.npmjs.com/package/atxp
  requires:
    binaries: [node, npx]
    node: ">=18"
    env:
      - name: ATXP_CONNECTION
        description: Auth token (created by npx atxp@latest login or agent register). Required for push/pull/status cloud operations. Not required for local index/search.
        required: false
    optionalDependencies:
      - name: "@zvec/zvec"
        description: Embedded vector database for local memory search (required for index/search subcommands)
---

# ATXP Memory — Agent Memory Management

Manage your agent's `.md` memory files: back up and restore to/from ATXP cloud servers, and **search your local memories** using zvec vector similarity search.

## Capabilities

| Capability | Description |
|------------|-------------|
| **Cloud Backup** | Push/pull `.md` files to ATXP servers for disaster recovery |
| **Local Search** | Index `.md` files into a local zvec vector database, then search by natural language query |
| **Status** | View cloud backup info and local index statistics |

## Security Model

- **Only `.md` files** are collected and transmitted (push/pull). No credentials, JSON configs, binaries, or other file types are ever sent.
- Files are sent to ATXP servers over **HTTPS**, associated with the authenticated agent's identity.
- `push` **replaces** the server snapshot entirely (latest snapshot only, no history).
- `pull` is **non-destructive** — it writes server files to the local directory but does not delete local files absent from the server.
- **Local search index** is stored in a `.atxp-memory-index/` subdirectory inside `--path`. It never leaves the local machine.
- **index** and **search** do not require authentication or network access.
- **Filesystem access**: reads from `--path` directory (push/index), writes to `--path` directory (pull) and `--path/.atxp-memory-index/` (index). No other directories are touched.
- **No modification** of OpenClaw config or auth files.

## When to Use

| Situation | Command |
|-----------|---------|
| After meaningful changes to SOUL.md, MEMORY.md, or at end of session | `push` |
| Bootstrapping a fresh workspace or recovering from environment loss | `pull` |
| After updating memory files and before starting a task that requires recall | `index` |
| Looking for relevant context in past memories | `search` |
| Verify backup exists before risky operations | `status` |

## Commands Reference

| Command | Description |
|---------|-------------|
| `npx atxp@latest memory push --path <dir>` | Recursively collect all `*.md` files from `<dir>` and upload to server |
| `npx atxp@latest memory pull --path <dir>` | Download backup from server and write files to `<dir>` |
| `npx atxp@latest memory index --path <dir>` | Chunk `.md` files by heading and build a local zvec search index |
| `npx atxp@latest memory search <query> --path <dir>` | Search indexed memories by similarity |
| `npx atxp@latest memory status [--path <dir>]` | Show cloud backup info and/or local index stats |

### Options

| Option | Required | Description |
|--------|----------|-------------|
| `--path <dir>` | Yes (push/pull/index/search) | Directory to operate on |
| `--topk <n>` | No (search only) | Number of results to return (default: 10) |

## How Local Search Works

1. **Indexing** (`memory index`):
   - Scans all `.md` files recursively from `--path`
   - Splits each file into chunks at heading boundaries (h1/h2/h3)
   - Converts each chunk into a 256-dimensional feature vector using locality-sensitive hashing (unigrams + bigrams)
   - Stores vectors and metadata in a local zvec database (HNSW index) at `<path>/.atxp-memory-index/`

2. **Searching** (`memory search`):
   - Converts the query text into the same vector representation
   - Performs approximate nearest neighbor search via zvec's HNSW index
   - Returns the top-k most similar chunks with file paths, headings, line numbers, and similarity scores

The search is purely local — no network requests, no API keys, no cost. Re-index after modifying memory files.

## Path Conventions

Typical OpenClaw workspace paths:

```
~/.openclaw/workspace-<id>/
~/.openclaw/workspace-<id>/SOUL.md
~/.openclaw/workspace-<id>/MEMORY.md
~/.openclaw/workspace-<id>/memory/
~/.openclaw/workspace-<id>/AGENTS.md
~/.openclaw/workspace-<id>/USER.md
```

## Backward Compatibility

The `backup` command is still accepted as an alias for `memory`:

```bash
npx atxp@latest backup push --path <dir>   # works, same as memory push
npx atxp@latest backup pull --path <dir>   # works, same as memory pull
npx atxp@latest backup status              # works, same as memory status
```

## Limitations

- **`.md` files only** — all other file types are ignored during push/index and not present in pull.
- **Latest snapshot only** — each push overwrites the previous backup. There is no version history.
- **Requires ATXP auth for cloud operations** — run `npx atxp@latest login` or `npx atxp@latest agent register` first.
- **`--path` is required** — there is no auto-detection of workspace location.
- **Local search requires @zvec/zvec** — install with `npm install @zvec/zvec` before using index/search.
- **Feature-hash embeddings** — local search uses statistical text hashing, not neural embeddings. It works well for keyword and phrase matching but is not a full semantic search. For best results, use specific terms from your memory files.
