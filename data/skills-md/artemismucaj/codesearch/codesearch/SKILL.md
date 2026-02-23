---
name: codesearch
description: Semantic code search using ML embeddings and AST analysis. Replaces built-in search tools for intent-based code exploration. Use when the user asks to find code by describing what it does, understand code relationships, or explore a codebase semantically.
metadata:
  author: ArtemisMucaj
  version: "0.6.0"
compatibility: Requires the codesearch binary installed and a repository indexed with `codesearch index`.
---

# Codesearch

Hybrid code search powered by ML embeddings, BM25-style keyword matching, and Reciprocal Rank Fusion. Finds code by meaning **and** by exact keyword — both in a single query, by default.

## When to Use This Skill

Invoke this skill **immediately** when:
- User asks to find code by **intent** (e.g., "where is authentication handled?")
- User asks to understand **what code does** (e.g., "how does the indexer work?")
- User asks to explore **functionality** (e.g., "find error handling logic")
- User asks about **implementation details** (e.g., "how are embeddings generated?")
- You need to discover code related to a **concept** rather than an exact string
- User asks about **blast radius** or **impact** of changing a function/symbol
- User asks **who calls** a function or **what does a function call** (symbol context)

## When to Use Built-in Tools Instead

Use Grep/Glob for:
- Exact text matching: `Grep "fn new_indexer"` (find exact function name)
- Specific imports: `Grep "use tokio"` (find import statements)
- File patterns: `Glob "**/*.rs"` (find files by extension)
- Variable references: `Grep "config_path"` (find exact variable name)

## Installation

If the `codesearch` binary is not found, install it automatically by running the install script bundled with this skill:

```shell
INSTALL_DIR="$HOME/.local/bin" sh .claude/skills/codesearch/install.sh
```

After installation, verify it works:

```shell
codesearch --version
```

> **Note:** The script downloads the latest release binary from GitHub for the current OS/architecture. It installs to `$INSTALL_DIR` (defaults to `$HOME/.local/bin` above). Ensure `$HOME/.local/bin` is in your `PATH`. If it's not already in your PATH, add this line to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):
> ```shell
> export PATH="$HOME/.local/bin:$PATH"
> ```
> Then reload your shell configuration: `source ~/.bashrc` (or `source ~/.zshrc`).

## Prerequisites

Before using codesearch, the target repository must be indexed:

```shell
# Index a repository (run once, supports incremental updates)
codesearch index /path/to/repo

# Index with a custom name
codesearch index /path/to/repo --name my-project

# Force full re-index (ignores cached file hashes)
codesearch index /path/to/repo --force
```

## Search

Use `codesearch search` to find code. By default it runs **hybrid search** (semantic vector similarity + BM25 keyword matching, fused via RRF) for best precision and recall.

```shell
# Hybrid search — default, no flag needed
codesearch search "user authentication flow"
codesearch search "error handling middleware"
codesearch search "database connection setup"
codesearch search "API request validation"

# Semantic-only search (disable keyword leg, pure vector similarity)
codesearch search "user authentication flow" --no-text-search

# Limit number of results (default: 10)
codesearch search "error handling" --num 5

# Filter by minimum relevance score
# Note: hybrid RRF scores are ~0.016–0.033; semantic cosine scores are 0.0–1.0
codesearch search "authentication" --min-score 0.02   # for hybrid results
codesearch search "authentication" --no-text-search --min-score 0.5  # for semantic-only

# Filter by programming language
codesearch search "struct definition" --language rust
codesearch search "class hierarchy" --language python --language typescript

# Filter by repository (when multiple repos are indexed)
codesearch search "config loading" --repository my-project
```

### Hybrid vs Semantic-only

| Mode | Flag | Best for |
|------|------|----------|
| Hybrid (default) | *(none)* | Most queries — combines meaning and keyword precision |
| Semantic-only | `--no-text-search` | Abstract intent queries where exact keywords unlikely to match |

### Supported Languages

Codesearch supports: **Rust**, **Python**, **JavaScript**, **TypeScript**, **Go**, **HCL**, **PHP**, **C++**

### What Gets Indexed

Codesearch uses Tree-sitter to extract and index these code constructs:
- Functions and methods
- Structs, classes, and enums
- Traits and implementations
- Modules, constants, and typedefs
- Import statements

## Call Graph Analysis

Once a repository is indexed, the call graph is available for two complementary commands.

### Impact Analysis — blast radius of a change

```shell
# Who breaks if `authenticate` changes? (default depth: 5 hops)
codesearch impact authenticate

# Limit to 2 hops
codesearch impact authenticate --depth 2

# Restrict to one repository; JSON output for scripts
codesearch impact authenticate --repository my-api --format json
```

### Symbol Context — 360-degree callers + callees

```shell
# Who calls `authenticate`, and what does it call?
codesearch context authenticate

# Limit results per direction
codesearch context authenticate --limit 10

# JSON output
codesearch context authenticate --format json
```

## Repository Management

```shell
# List all indexed repositories
codesearch list

# View indexing statistics
codesearch stats

# Delete a repository from the index
codesearch delete <id-or-path>
```

## Query Best Practices

**Do:**
```shell
codesearch search "How are file chunks created and stored?"
codesearch search "Vector embedding generation process"
codesearch search "Configuration loading and validation"
codesearch search "HTTP request routing logic"
```

**Don't:**
```shell
codesearch search "func"          # Too vague
codesearch search "error"         # Too generic
codesearch search "HandleRequest" # Use Grep for exact name matches
```

## Recommended Workflow

1. **Start with `codesearch search`** to find relevant code semantically
2. **Use `Read` tool** to examine the files and lines from search results
3. **Use `Grep`** only for exact string searches when you know the identifier name
4. **Use `codesearch search`** again with refined queries if initial results aren't specific enough

## Advanced Configuration

```shell
# Use a custom data directory for the index
codesearch --data-dir /custom/path search "query"

# Use a namespace to isolate projects
codesearch --namespace my-project search "query"

# Use in-memory storage (no persistence, useful for one-off searches)
codesearch --memory-storage search "query"

# Disable result reranking (faster but less accurate)
codesearch --no-rerank search "query"
```

## Keywords

semantic search, hybrid search, code search, natural language search, find code, explore codebase, code understanding, intent search, AST analysis, embeddings, code discovery, code exploration, BM25, keyword search, RRF, reciprocal rank fusion, call graph, impact analysis, blast radius, symbol context, callers, callees, dependency analysis
