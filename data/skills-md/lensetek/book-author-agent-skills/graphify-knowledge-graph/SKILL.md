---
name: graphify-knowledge-graph
description: Use to index and query project knowledge graphs (Obsidian Zettelkasten, CPMK prerequisite trees, paper collections, and codebase ASTs) with strict multi-project data isolation.
metadata:
  short-description: Project-isolated Graphify Knowledge Graph harness for structural memory and traversal
---

# Graphify Knowledge Graph Harness

Use this skill when you need to index, traverse, or query structural relationships in an academic book project (e.g. Obsidian Vaults, CPMK prerequisite networks, literature sets, or codebase ASTs) without wasting model context tokens.

## Agent Contract

Input:

- `project_dir`: Absolute path to the current book project directory (defaults to cwd).
- `action`: `index`, `query`, or `clean`.
- `query_type`: `summary`, `search`, `neighbors`, or `shortest_path`.
- `target`: Keyword or node ID for targeted queries.

Output:

- `status`: `success` or `error`.
- `isolation_status`: `100% project-bound` (stored under `.graphify/`).
- `graph_artifacts`: `graph.json`, `graph.html`, and `GRAPH_REPORT.md`.
- `query_results`: Matching nodes, neighbors, or shortest paths.

## Multi-Project Data Isolation Rules

1. **Project-Bound Storage**: Graphify outputs MUST be created inside `<project_dir>/.graphify/`. Never mix graphs from different book projects into a shared global folder.
2. **Auto .gitignore Injection**: Ensure `.graphify/` is added to the project's `.gitignore` file automatically.
3. **Local AST Parsing**: Indexing runs 100% locally via deterministic AST parsing. No credentials, private text, or API keys are ever sent to external cloud servers.

## Helper Script Invocation

Execute the standalone Python harness script via CLI:

```bash
# Index current project
python .codex/skills/scripts/graphify_harness.py index --project-dir "/path/to/project"

# Query central concepts or keywords
python .codex/skills/scripts/graphify_harness.py query --project-dir "/path/to/project" --query-type search --target "CPMK-1"

# Query node neighbors for cross-referencing
python .codex/skills/scripts/graphify_harness.py query --project-dir "/path/to/project" --query-type neighbors --target "section:bab1.md#Pendahuluan"

# Clean project graph cache
python .codex/skills/scripts/graphify_harness.py clean --project-dir "/path/to/project"
```

## Collaborating Specialist Agents

- `book-author-orchestrator`: Runs preflight graph indexing on new book projects.
- `academic-source-analyzer` & `research-synthesis-to-reference-book`: Queries graph clusters to group papers/notes into thematic chapters.
- `rps-to-buku-ajar`: Traverses CPMK prerequisite chains via `shortest_path`.
- `academic-chapter-writer`: Queries `neighbors` for automated cross-referencing between chapters.
- `citation-integrity-reviewer`: Verifies claim provenance from draft text back to evidence snippet nodes.
