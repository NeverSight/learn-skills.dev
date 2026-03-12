---
name: obsidian-graph-traversal
description: "Semantic link traversal for Obsidian Vaults. Builds an in-memory graph index from wikilinks and provides instant forward-link, backlink, and multi-degree connection queries. Use when exploring note relationships or finding orphaned notes."
allowed-tools: Bash, Read
---
# Obsidian Graph Traversal

**Status:** Active
**Author:** Richard Fremmerlid
**Domain:** Obsidian Integration
**Depends On:** `obsidian-markdown-mastery` (WP05, `obsidian-parser`)

## Purpose

This skill transforms static vault notes into a queryable semantic graph. It answers
questions like "What connects to Note X?" and "What are the 2nd-degree connections
of Concept A?" — instantly, without rescanning the vault.

**Performance Target**: < 2 seconds for deep queries across 1000+ notes.

## Available Commands

### Build the Graph Index
```bash
python ./scripts/graph_ops.py build --vault-root <path>
```

### Get Forward Links (outbound)
```bash
python ./scripts/graph_ops.py forward --note "Note Name"
```

### Get Backlinks (inbound)
```bash
python ./scripts/graph_ops.py backlinks --note "Note Name"
```

### Get N-Degree Connections
```bash
python ./scripts/graph_ops.py connections --note "Note Name" --depth 2
```

### Find Orphaned Notes
```bash
python ./scripts/graph_ops.py orphans --vault-root <path>
```

## Architecture

### In-Memory Graph Index
- On `build`, every `.md` file in the vault is parsed using the `obsidian-parser`
- Wikilinks are extracted; embeds (`![[...]]`) are filtered out
- A bidirectional adjacency map is built: `{source: [targets], ...}` and `{target: [sources], ...}`
- The index is cached as `.graph-index.json` at the vault root
- Invalidation uses file `mtime` — if a file changed since last build, only that file is re-indexed

### The Primary Agent as Librarian
The graph index enables the agent to:
- **Detect blind spots**: Orphaned notes indicate areas where agents act without historical context
- **Resolve conflicts**: If two agents update the same note, the graph shows the impact radius
- **Enforce schema**: Frontmatter metadata (status, trust_score) tracked across linked notes
