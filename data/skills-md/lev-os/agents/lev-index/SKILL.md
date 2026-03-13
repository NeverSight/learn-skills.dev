---
name: lev-index
description: |
  [WHAT] Vector index management for semantic search using LEANN (97% storage reduction)
  [HOW] Build indexes from directories, add content incrementally, search semantically via gRPC service on port 50052
  [WHEN] Use when building/updating indexes, checking index health, or directly querying a specific index
  [WHY] Enables semantic search across code and docs with efficient graph-based storage

  Triggers: "build index", "search index", "index status", "add to index", "update index", "semantic search"
skill_type: tool
category: process-get-index

lifecycle_integration:
  stage: captured
  input_artifact: content to index (code/docs/custom)
  output_artifact: searchable LEANN index
---

# lev-index - Vector Index Management

## Overview

`lev index` manages LEANN-powered vector indexes for semantic search. LEANN achieves 97% storage reduction through graph-based selective recomputation while maintaining high search quality.

## When to Use

Use `lev index` when:
- **Building indexes** - Creating searchable indexes from code or docs
- **Updating indexes** - Adding new content to existing indexes
- **Checking status** - Verifying index health and coverage
- **Direct semantic search** - Querying a specific index

Use `lev get` instead when:
- **Cross-index search** - Searching across multiple indexes with fusion
- **Auto-routed queries** - Let the system pick relevant indexes

## MCP Commands

The index service exposes 4 MCP tools:

| Tool | Purpose |
|------|---------|
| `index:search` | Semantic search over indexed content |
| `index:add` | Add text content to the index |
| `index:build` | Build index from a directory |
| `index:status` | Get index status and health |

## Basic Usage

### Build an Index
```bash
# Build index from directory
lev index build ~/Documents/codebase my-index

# Build with specific embedding model
lev index build ~/lev/docs documentation --model sentence-transformers
```

### Search an Index
```bash
# Basic semantic search
lev index search "authentication patterns" --index my-index

# With result limit
lev index search "error handling" --index codebase --top-k 10
```

### Add Content
```bash
# Add a file to existing index
lev index add "path/to/file.md" --index documentation

# Add text content directly
lev index add --text "Important context about auth" --index notes
```

### Check Status
```bash
# Get index health and stats
lev index status --index my-index

# List all indexes
lev index status --all
```

## Index Locations

| Index | Content | Path |
|-------|---------|------|
| codebase | Source code | `~/.config/lev/indexes/ck/codebase.index` |
| documentation | Docs, ADRs | `~/.config/lev/indexes/leann/documentation.leann` |
| ideas | Ideas collection | `~/.config/lev/indexes/leann/ideas.leann` |
| _global | Everything | `~/.config/lev/indexes/leann/_global.leann` |

## JavaScript SDK

```javascript
import { VectorIndexClient } from '@lev/index';

const client = new VectorIndexClient('localhost:50052');
await client.connect();

// Build an index
await client.build('~/Documents/codebase', 'my-index');

// Search
const results = await client.search('authentication patterns', {
  indexName: 'my-index',
  topK: 5
});

// Add content
await client.add('New content to index', {
  indexName: 'my-index',
  metadata: { source: 'manual', date: new Date() }
});

client.close();
```

## Service Architecture

```
core/index/
├── python/
│   └── server.py          # gRPC server (port :50052)
├── src/
│   └── commands/          # MCP commands
│       ├── search.js
│       ├── add.js
│       ├── build.js
│       └── status.js
└── vendor/
    └── leann/             # LEANN library
```

## Port Allocation

| Service | Port |
|---------|------|
| Memory (Graphiti) | 50051 |
| **Index (LEANN)** | **50052** |

## Index Maintenance

### When to Rebuild
- After major codebase changes
- When search quality degrades
- After adding significant new content

### Incremental Updates
```bash
# Add new files without full rebuild
lev index add new-file.md --index documentation
```

### Full Rebuild
```bash
# Clear and rebuild from scratch
lev index build ~/lev/docs documentation --clear
```

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `LEV_INDEX_PATH` | `~/.config/lev/indexes` | Base directory for index storage |

## Troubleshooting

### Index Not Found
```bash
# Check available indexes
lev index status --all

# Rebuild if missing
lev index build <path> <name>
```

### Stale Results
```bash
# Check index freshness
lev index status --index <name>

# Update with new content
lev index add <new-files> --index <name>
```

### Service Not Running
```bash
# Start the gRPC server
cd core/index/python && python server.py --port 50052
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `lev index build <path> <name>` | Create index from directory |
| `lev index search "query" --index X` | Semantic search |
| `lev index add <file> --index X` | Add content to index |
| `lev index status --index X` | Check index health |
| `lev index status --all` | List all indexes |

## Relates

### Master Router
- **Lev Master Router** (`lev/SKILL.md`) - Routes all lev-* skills
  Parent skill that dispatches to this skill based on keywords/context

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for lev-index, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
