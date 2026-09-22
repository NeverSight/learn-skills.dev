---
name: codebase-memory-mcp-intelligence
description: High-performance code intelligence MCP server that indexes codebases into knowledge graphs for structural queries, call traces, and architecture analysis
triggers:
  - index this codebase
  - show me the architecture
  - find all callers of this function
  - trace the call graph
  - search for functions matching
  - analyze code impact
  - show HTTP routes
  - detect dead code
---

# codebase-memory-mcp Intelligence

> Skill by [ara.so](https://ara.so) — MCP Skills collection.

## Overview

codebase-memory-mcp is a high-performance code intelligence MCP server that indexes codebases into persistent knowledge graphs. It parses 155 languages using tree-sitter ASTs, resolves call graphs, detects HTTP routes, and enables sub-millisecond structural queries. The Linux kernel (28M LOC) indexes in 3 minutes; average repos in milliseconds.

Key capabilities:
- **Graph-based code intelligence**: Functions, classes, calls, imports, inheritance as queryable nodes/edges
- **Structural search**: Find symbols by pattern, trace call chains, detect dead code
- **Architecture analysis**: Community detection, hotspots, layering, cross-service HTTP linking
- **Semantic search**: Vector search with bundled embeddings (no API key required)
- **155 languages**: Tree-sitter grammars compiled into a single static binary
- **14 MCP tools**: All accessible via natural language in any compatible agent

## Installation

### Quick Install (macOS/Linux)

```bash
# Standard version
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash

# With graph visualization UI
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash -s -- --ui
```

### Windows (PowerShell)

```powershell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.ps1 -OutFile install.ps1
.\install.ps1
```

### Manual Installation

Download from [releases](https://github.com/DeusData/codebase-memory-mcp/releases/latest):

```bash
# Extract and run installer
tar xzf codebase-memory-mcp-*.tar.gz
./install.sh
```

The installer auto-detects Claude Code, Cursor, Codex CLI, Gemini CLI, Zed, OpenCode, Aider, VS Code, and other agents, configuring MCP entries automatically.

### Verify Installation

```bash
codebase-memory-mcp --version
```

Restart your coding agent after installation.

## Core Usage Patterns

### Indexing a Codebase

**Via agent (recommended):**
```
User: Index this project
```

The MCP server will call `index_repository` with the current working directory.

**Via CLI:**
```bash
codebase-memory-mcp index /path/to/repo
```

**Enable auto-indexing:**
```bash
codebase-memory-mcp config set auto_index true
codebase-memory-mcp config set auto_index_limit 50000
```

Auto-index runs on MCP session start for new projects and registers existing projects with the background file watcher.

### Architecture Overview

Get a complete architectural summary in one call:

```
User: Show me the architecture of this codebase
```

This invokes `get_architecture` which returns:
- Languages and package structure
- Entry points (main functions, HTTP handlers)
- HTTP/gRPC/GraphQL routes
- Hotspot functions (high in/out degree)
- Module boundaries via Louvain clustering
- Layering analysis (presentation/business/data)

**Example response structure:**
```json
{
  "languages": ["TypeScript", "Python", "Go"],
  "packages": ["src/api", "src/services", "src/models"],
  "entry_points": [
    {"name": "main", "file": "src/index.ts", "type": "Function"}
  ],
  "routes": [
    {"path": "/api/users", "method": "GET", "handler": "getUsers", "file": "src/api/users.ts"}
  ],
  "hotspots": [
    {"name": "processRequest", "in_degree": 15, "out_degree": 8, "file": "src/services/request.ts"}
  ],
  "boundaries": [
    {"module": "Community_0", "members": ["src/api/*"], "internal_edges": 45, "external_edges": 12}
  ]
}
```

### Searching the Graph

**Find symbols by name pattern:**
```
User: Find all functions with "Handler" in the name
```

Uses `search_graph`:
```json
{
  "name_pattern": ".*Handler.*",
  "labels": ["Function"]
}
```

**Find high-degree nodes:**
```
User: Show me the most called functions
```

```json
{
  "labels": ["Function"],
  "min_in_degree": 5,
  "limit": 20
}
```

**Scope to specific files:**
```
User: Find all classes in the auth module
```

```json
{
  "labels": ["Class"],
  "file_pattern": ".*/auth/.*"
}
```

### Call Tracing

**Find all callers:**
```
User: What calls the authenticate function?
```

Uses `get_callers`:
```json
{
  "symbol_name": "authenticate",
  "max_depth": 3
}
```

**Trace call chain:**
```
User: Trace the execution path from main to database functions
```

Uses `trace_symbol`:
```json
{
  "symbol_name": "main",
  "direction": "outgoing",
  "max_depth": 5,
  "edge_types": ["CALLS"]
}
```

### Semantic Search

**Find related code by concept:**
```
User: Find authentication-related functions
```

Uses `semantic_query`:
```json
{
  "query": "authentication jwt token validation",
  "limit": 10
}
```

Semantic search uses bundled Nomic embeddings (no API key required) with 11-signal scoring:
- TF-IDF relevance
- AST structural similarity
- API signature matching
- Data flow patterns
- MinHash near-clone detection

### Cypher-Like Queries

**Advanced graph queries:**
```
User: Run a Cypher query to find all functions that call database operations
```

Uses `cypher_query`:
```cypher
MATCH (f:Function)-[:CALLS]->(db:Function)
WHERE db.name CONTAINS 'query' OR db.name CONTAINS 'exec'
RETURN f.name, f.file, COUNT(db) as db_calls
ORDER BY db_calls DESC
LIMIT 20
```

**Find inheritance hierarchies:**
```cypher
MATCH (c:Class)-[:INHERITS*1..3]->(base:Class)
WHERE base.name = 'BaseModel'
RETURN c.name, c.file
```

**HTTP route to implementation:**
```cypher
MATCH (r:Route)-[:HANDLED_BY]->(h:Function)-[:CALLS]->(s:Function)
WHERE r.path CONTAINS '/api/users'
RETURN r.path, h.name, COLLECT(s.name) as services
```

### Dead Code Detection

```
User: Find unused functions
```

Uses `find_dead_code`:
```json
{
  "entry_points": ["main", "handler"],
  "min_depth": 2
}
```

Returns functions with zero incoming `CALLS` edges, excluding recognized entry points (main, init, handlers, tests).

### Change Impact Analysis

**Detect impact of uncommitted changes:**
```
User: What's affected by my recent changes?
```

Uses `detect_changes`:
```json
{
  "include_tests": true
}
```

Returns:
- Changed symbols with confidence scores
- Affected downstream symbols (via call graph)
- Risk classification (CRITICAL/HIGH/MEDIUM/LOW)
- Test coverage mapping

**Example response:**
```json
{
  "changed_symbols": [
    {
      "name": "authenticate",
      "type": "Function",
      "file": "src/auth.ts",
      "confidence": 0.95,
      "change_type": "modified"
    }
  ],
  "affected_symbols": [
    {
      "name": "loginHandler",
      "type": "Function",
      "file": "src/handlers/login.ts",
      "distance": 1,
      "risk": "HIGH"
    }
  ]
}
```

### Architecture Decision Records (ADR)

**Create ADR:**
```
User: Document our decision to use Redis for session storage
```

Uses `manage_adr`:
```json
{
  "action": "create",
  "title": "Use Redis for Session Storage",
  "status": "accepted",
  "context": "Need fast, distributed session management",
  "decision": "Adopt Redis with session TTL and clustering",
  "consequences": "Requires Redis infrastructure; enables horizontal scaling"
}
```

**List ADRs:**
```
User: Show all architecture decisions
```

```json
{
  "action": "list"
}
```

**Update ADR:**
```json
{
  "action": "update",
  "id": "ADR-001",
  "status": "superseded"
}
```

### Cross-Service Analysis

**Find HTTP call sites:**
```
User: Show all external API calls
```

Uses `search_graph` with HTTP edge filters:
```json
{
  "edge_types": ["HTTP_CALLS"],
  "labels": ["Function"]
}
```

**Trace cross-service dependencies:**
```cypher
MATCH (f:Function)-[:HTTP_CALLS]->(r:Route)
RETURN f.name, f.file, r.path, r.method
```

## Configuration

### View Current Config

```bash
codebase-memory-mcp config list
```

### Key Settings

```bash
# Auto-index on session start
codebase-memory-mcp config set auto_index true

# File limit for auto-indexing
codebase-memory-mcp config set auto_index_limit 50000

# Enable background file watcher
codebase-memory-mcp config set watch true

# Embedding model (default: nomic-embed-code)
codebase-memory-mcp config set embedding_model nomic-embed-code

# Graph visualization port
codebase-memory-mcp config set ui_port 9749
```

### Ignore Patterns

Create `.cbmignore` in your repo root (gitignore syntax):

```
node_modules/
*.test.ts
dist/
build/
*.min.js
vendor/
```

Default ignores: `node_modules`, `.git`, `dist`, `build`, `vendor`, `.venv`, `__pycache__`

## Advanced Features

### Graph Visualization UI

Launch with UI enabled:

```bash
codebase-memory-mcp --ui=true --port=9749
```

Open `http://localhost:9749` for 3D interactive graph exploration.

Features:
- Force-directed layout with community coloring
- Filter by label, file, package
- Click nodes to see properties and edges
- Multi-galaxy layout for cross-repo graphs

### Team-Shared Graph Artifact

Commit compressed graph to avoid reindexing:

```bash
# After indexing, compress the graph
codebase-memory-mcp export --output=.codebase-memory/graph.db.zst

# Commit to repo
git add .codebase-memory/graph.db.zst
git commit -m "Add codebase graph snapshot"
```

Teammates run:
```bash
codebase-memory-mcp import --input=.codebase-memory/graph.db.zst
```

### CLI Mode

Use without MCP for scripting:

```bash
# Search
codebase-memory-mcp cli search_graph '{"name_pattern": ".*Service$", "labels": ["Class"]}'

# Cypher query
codebase-memory-mcp cli cypher_query 'MATCH (f:Function) WHERE f.name = "main" RETURN f'

# Get architecture
codebase-memory-mcp cli get_architecture '{}'

# Semantic search
codebase-memory-mcp cli semantic_query '{"query": "database connection pooling", "limit": 5}'
```

### Language-Specific Features

**Go:**
- Package resolution via `go.mod`
- Interface implementation detection
- Struct method resolution

**TypeScript/JavaScript:**
- JSX component tracing
- Type inference from JSDoc
- Import alias resolution
- Decorator detection

**Python:**
- Class hierarchy via `INHERITS`
- Decorator-based route detection (Flask, FastAPI)
- Import resolution via `pyproject.toml`, `setup.py`

**C/C++:**
- Header/implementation linking
- Preprocessor-aware parsing
- Template instantiation tracking

### Infrastructure-as-Code

**Kubernetes manifests:**
```
User: Show all Kubernetes resources
```

```json
{
  "labels": ["Resource"],
  "properties": {"kind": "Deployment"}
}
```

**Kustomize overlays:**
```cypher
MATCH (overlay:Module)-[:IMPORTS]->(base:Resource)
WHERE overlay.type = 'kustomize'
RETURN overlay.name, COLLECT(base.name) as resources
```

**Dockerfile analysis:**
```
User: Find all services using Node 18
```

```json
{
  "labels": ["Dockerfile"],
  "code_pattern": "FROM node:18"
}
```

## Troubleshooting

### Indexing Issues

**Large repos timing out:**
```bash
# Increase memory limit (default: 8GB)
codebase-memory-mcp config set max_memory_gb 16

# Skip large files
codebase-memory-mcp config set max_file_size_mb 5
```

**Missing symbols:**
- Check `.cbmignore` — ensure source files aren't excluded
- Verify language support: `codebase-memory-mcp --languages`
- Re-index: `codebase-memory-mcp index --force /path/to/repo`

**Slow queries:**
```bash
# Rebuild indexes
codebase-memory-mcp cli vacuum

# Check database size
ls -lh ~/.cache/codebase-memory-mcp/graph.db
```

### MCP Connection Issues

**Agent can't find server:**
1. Verify installation: `which codebase-memory-mcp`
2. Check agent config: `codebase-memory-mcp config verify`
3. Restart agent completely
4. Check logs: `~/.cache/codebase-memory-mcp/logs/`

**Tools not appearing:**
```bash
# Reinstall agent configs
codebase-memory-mcp install --force

# Verify MCP registration
codebase-memory-mcp config show-mcp-config
```

### Performance

**High memory usage during indexing:**
- Normal for large repos (Linux kernel uses ~6GB peak)
- Memory released after indexing completes
- Use `--max-memory-gb` flag to cap usage

**Slow semantic search:**
```bash
# Rebuild embeddings index
codebase-memory-mcp cli rebuild_embeddings

# Reduce result limit
codebase-memory-mcp config set semantic_limit 10
```

### File Watcher

**Changes not detected:**
```bash
# Check watcher status
codebase-memory-mcp status

# Restart watcher
codebase-memory-mcp watch restart

# Increase file watch limit (Linux)
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## Common Workflows

### Onboarding to New Codebase

```
1. "Index this project"
2. "Show me the architecture"
3. "What are the entry points?"
4. "Find the main HTTP routes"
5. "Show me the most important functions" (hotspots)
```

### Refactoring

```
1. "Find all callers of [function]"
2. "What's affected by my changes?" (after editing)
3. "Show me the call chain from [entry] to [target]"
4. "Find dead code"
```

### Debugging

```
1. "Trace execution from [function]"
2. "What calls this endpoint?" (for HTTP routes)
3. "Find similar functions to [name]"
4. "Show data flow through [function]"
```

### Cross-Service Analysis

```
1. "Find all external API calls"
2. "Show services that depend on [service]"
3. "Map HTTP routes to implementations"
4. "Find pub-sub channels across repos"
```

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `index_repository` | Index codebase into knowledge graph |
| `search_graph` | Structural search by pattern, label, degree |
| `search_code` | Graph-augmented grep |
| `semantic_query` | Vector search with bundled embeddings |
| `get_architecture` | Full architectural summary |
| `get_callers` | Find all callers of a symbol |
| `trace_symbol` | Trace call chains (in/out) |
| `cypher_query` | Advanced graph queries |
| `find_dead_code` | Detect unused functions |
| `detect_changes` | Git diff impact analysis |
| `manage_adr` | Architecture Decision Records |
| `get_context` | Context for specific symbols |
| `list_routes` | All HTTP/gRPC/GraphQL routes |
| `analyze_dependencies` | Cross-service dependency graph |

## Updates

```bash
# Check for updates
codebase-memory-mcp update

# Auto-update check on startup (default: enabled)
codebase-memory-mcp config set check_updates true
```

The server notifies on first tool call if a new release is available.

## Uninstall

```bash
# Remove all agent configs and binary
codebase-memory-mcp uninstall

# Keep database (default)
# Or remove database too:
rm -rf ~/.cache/codebase-memory-mcp/
```
