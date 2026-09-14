---
name: code-review-graph
description: Build a persistent knowledge graph of your codebase so Claude reads only what matters — up to 49x fewer tokens on coding tasks.
triggers:
  - build the code review graph
  - set up code-review-graph for this project
  - review changes since last commit with graph
  - analyze blast radius of my changes
  - reduce tokens when reviewing code
  - incremental graph update for codebase
  - find what files are affected by this change
  - install code review graph mcp
---

# code-review-graph

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`code-review-graph` builds a persistent structural map of a codebase using Tree-sitter, stores it in a local SQLite graph, and exposes it to Claude via MCP. Instead of re-reading entire projects on every task, Claude queries the graph and reads only the files in the blast radius of a change — averaging 6.8× fewer tokens on code reviews and up to 49× on daily coding tasks in large monorepos.

---

## Installation

### Claude Code Plugin (recommended)

```bash
claude plugin marketplace add tirth8205/code-review-graph
claude plugin install code-review-graph@code-review-graph
```

Restart Claude Code after installation.

### pip

```bash
pip install code-review-graph
code-review-graph install   # registers the MCP server with Claude Code
```

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

### Optional: semantic search support

```bash
pip install code-review-graph[embeddings]
```

Enables vector embeddings via `sentence-transformers` for `semantic_search_nodes_tool`.

---

## Initial Setup

After installation, open your project in Claude Code and run:

```
Build the code review graph for this project
```

Or use the slash command:

```
/code-review-graph:build-graph
```

The first build parses the full codebase (~10 seconds for 500 files). After that, the graph updates incrementally on every file save and git commit (under 2 seconds for a 2,900-file project).

---

## CLI Reference

```bash
# Register MCP server with Claude Code
code-review-graph install

# Parse entire codebase into the graph (first run)
code-review-graph build

# Re-parse only changed files (subsequent runs)
code-review-graph update

# Show graph statistics: node count, edge count, language breakdown
code-review-graph status

# Auto-update the graph as you save files (continuous watch mode)
code-review-graph watch

# Generate an interactive D3.js HTML visualisation of the graph
code-review-graph visualize

# Start the MCP server manually (Claude Code does this automatically)
code-review-graph serve
```

---

## Slash Commands in Claude Code

| Command | What it does |
|---|---|
| `/code-review-graph:build-graph` | Build or rebuild the code graph from scratch |
| `/code-review-graph:review-delta` | Review changes since the last commit |
| `/code-review-graph:review-pr` | Full PR review with blast-radius analysis |

---

## MCP Tools (used automatically by Claude)

Once the graph is built, Claude calls these tools without manual prompting:

| Tool | Purpose |
|---|---|
| `build_or_update_graph_tool` | Build or incrementally update the graph |
| `get_impact_radius_tool` | Find all files/functions affected by a change |
| `get_review_context_tool` | Return a token-optimised structural summary for review |
| `query_graph_tool` | Query callers, callees, tests, imports, inheritance |
| `semantic_search_nodes_tool` | Search code entities by name or meaning |
| `embed_graph_tool` | Compute vector embeddings for semantic search |
| `list_graph_stats_tool` | Graph size and health statistics |
| `get_docs_section_tool` | Retrieve documentation sections |
| `find_large_functions_tool` | Find functions/classes over a line-count threshold |

---

## Configuration: Ignoring Paths

Create `.code-review-graphignore` in the repository root:

```
generated/**
*.generated.ts
vendor/**
node_modules/**
dist/**
__pycache__/**
*.pyc
migrations/**
```

The graph will skip these paths during build and update.

---

## Python API

The graph can be queried programmatically for custom tooling or scripts.

### Build and update the graph

```python
from code_review_graph import GraphBuilder

builder = GraphBuilder(repo_path="/path/to/your/project")

# Full build (first time)
stats = builder.build()
print(f"Nodes: {stats['nodes']}, Edges: {stats['edges']}")

# Incremental update (subsequent runs — only parses changed files)
update_stats = builder.update()
print(f"Re-parsed: {update_stats['files_updated']} files")
```

### Query the graph

```python
from code_review_graph import GraphQuery

query = GraphQuery(repo_path="/path/to/your/project")

# Find all callers of a function
callers = query.get_callers("authenticate_user")
print(callers)
# ['api/views.py::login_view', 'tests/test_auth.py::test_login']

# Find all callees (functions called by a function)
callees = query.get_callees("process_payment")
print(callees)

# Find tests that cover a file
tests = query.get_tests_for("payments/processor.py")
print(tests)

# Get inheritance chain for a class
parents = query.get_inheritance("AdminUser")
print(parents)
# ['BaseUser', 'PermissionMixin']
```

### Blast-radius analysis

```python
from code_review_graph import ImpactAnalyzer

analyzer = ImpactAnalyzer(repo_path="/path/to/your/project")

# What is affected if this file changes?
impact = analyzer.get_impact_radius("auth/models.py")
print(impact)
# {
#   "direct_callers": ["api/views.py", "middleware/auth.py"],
#   "transitive_dependents": ["api/tests/test_views.py", "integration/test_flow.py"],
#   "test_files": ["tests/test_auth.py"],
#   "blast_radius_size": 7
# }

# Multiple changed files (e.g., from a git diff)
changed_files = ["auth/models.py", "payments/processor.py"]
combined_impact = analyzer.get_impact_radius(changed_files)
```

### Semantic search

```python
from code_review_graph import SemanticSearch

# Requires: pip install code-review-graph[embeddings]
search = SemanticSearch(repo_path="/path/to/your/project")

# Embed the graph (one-time, cached)
search.embed()

# Search for code entities by concept
results = search.search("rate limiting middleware", top_k=5)
for r in results:
    print(r["node"], r["file"], r["score"])
```

### Find large functions

```python
from code_review_graph import GraphQuery

query = GraphQuery(repo_path="/path/to/your/project")

# Find functions/classes over 50 lines (good for refactoring targets)
large = query.find_large_functions(threshold=50)
for item in large:
    print(f"{item['name']} in {item['file']}: {item['lines']} lines")
```

---

## Common Patterns

### Pattern: Review only what changed in the current branch

```bash
# In Claude Code, after making changes:
/code-review-graph:review-delta
```

Claude will:
1. Call `build_or_update_graph_tool` to sync the graph with your edits
2. Call `get_impact_radius_tool` on changed files
3. Call `get_review_context_tool` to get a compact structural summary
4. Review only the relevant ~15 files instead of the full codebase

### Pattern: Continuous watch during development

```bash
# Terminal 1: keep the graph fresh as you code
code-review-graph watch

# Terminal 2: your normal development workflow
```

Any file save triggers an incremental re-parse of only that file and its dependents.

### Pattern: Pre-commit hook

```bash
# .git/hooks/pre-commit
#!/bin/sh
code-review-graph update
```

Makes the graph always current before Claude sees a commit.

### Pattern: Visualise the dependency graph

```bash
code-review-graph visualize
# Opens an interactive D3.js force-directed graph in your browser
# Toggle edge types: calls, imports, inheritance, test coverage
# Search nodes by name
```

### Pattern: Check graph health

```bash
code-review-graph status
# Example output:
# Graph: .code-review-graph/graph.db
# Nodes: 4,821 (functions: 2,103 | classes: 487 | files: 312)
# Edges: 11,204 (calls: 7,891 | imports: 2,108 | inherits: 205 | tests: 1,000)
# Languages: Python (180), TypeScript (98), JavaScript (34)
# Last updated: 2026-03-26 01:22:11 (3 files changed)
```

---

## Supported Languages

Python, TypeScript, JavaScript, Vue, Go, Rust, Java, C#, Ruby, Kotlin, Swift, PHP, Solidity, C/C++

Each language has full Tree-sitter grammar support for: functions, classes, imports, call sites, inheritance chains, and test detection.

---

## Adding a New Language

Edit `code_review_graph/parser.py`:

```python
# 1. Add file extension mapping
EXTENSION_TO_LANGUAGE = {
    # ... existing entries ...
    ".ex": "elixir",
    ".exs": "elixir",
}

# 2. Add AST node type mappings for the new language
_CLASS_TYPES["elixir"] = {"defmodule"}
_FUNCTION_TYPES["elixir"] = {"def", "defp"}
_IMPORT_TYPES["elixir"] = {"alias", "import", "use", "require"}
_CALL_TYPES["elixir"] = {"call"}
```

Then add a test fixture in `tests/fixtures/elixir/` and open a PR.

---

## Where the Graph Is Stored

The graph is stored locally in `.code-review-graph/graph.db` (SQLite). There is no external database, no cloud dependency, and no data leaves your machine. Add it to `.gitignore` if you don't want it committed:

```bash
echo ".code-review-graph/" >> .gitignore
```

Or commit it to share the pre-built graph with your team (saves the ~10-second initial build for each developer).

---

## Troubleshooting

### Graph is stale / not reflecting recent changes

```bash
code-review-graph update    # incremental re-parse of changed files
# or, if something seems wrong:
code-review-graph build     # full rebuild from scratch
```

### MCP server not connecting to Claude Code

```bash
# Re-register the MCP server
code-review-graph install

# Verify it's registered
claude mcp list
```

Then restart Claude Code.

### `uv` not found

```bash
# Install uv (required by the MCP server runner)
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
```

### Semantic search not working

```bash
# Install the embeddings extra
pip install "code-review-graph[embeddings]"

# Compute embeddings (required once after install)
code-review-graph embed    # or call embed_graph_tool via Claude
```

### A language isn't being parsed

Check that the file extension is in `EXTENSION_TO_LANGUAGE` and the corresponding Tree-sitter grammar is installed. Run `code-review-graph status` to see which languages were detected in your project.

### Build is slow on first run

Expected — Tree-sitter parses every file. A 500-file project takes ~10 seconds. All subsequent `update` calls complete in under 2 seconds because only changed files are re-parsed (detected via SHA-256 hash comparison).

---

## How the Token Reduction Works

On every review or coding task:

1. **Graph query**: Claude calls `get_impact_radius_tool` with the changed files
2. **Blast-radius tracing**: the graph follows call edges, import edges, and test edges to find every affected node
3. **Compact summary**: `get_review_context_tool` returns a 156–207 token structural summary (callers, dependents, test coverage gaps, dependency chains)
4. **Targeted reading**: Claude reads only the ~15 files in the blast radius, not the full codebase

In the Next.js monorepo (27,732 files): without the graph Claude reads ~739K tokens; with the graph it reads ~15K tokens — a 49× reduction.
