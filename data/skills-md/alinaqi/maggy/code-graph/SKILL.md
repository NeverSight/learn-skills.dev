---
name: code-graph
description: AST-based code graph for fast symbol lookup, dependency analysis, and blast radius via codebase-memory-mcp MCP server
when-to-use: "Before reading files — query the graph first for symbol lookup, call tracing, and blast radius"
user-invocable: false
effort: medium
---

# Code Graph Skill


**Purpose:** Use the code graph (codebase-memory-mcp) for sub-millisecond
symbol lookup, function search, dependency analysis, and blast radius
detection. This replaces brute-force grep and file reading for code
navigation.

---

## Core Principle

**Graph first, file second.** Before reading files or grepping, query the
code graph. Only read full files when you need to modify them or need
context beyond what the graph provides.

**Consider graph when planning.** When planning any change — feature,
refactor, bug fix — start by querying the graph to understand scope,
dependencies, and blast radius. This applies to thinking and planning
phases, not just implementation. Grep is still the right tool for
searching string literals, log messages, config values, and content
that lives outside code structure.

```
┌────────────────────────────────────────────────────────────────┐
│  GRAPH FIRST, FILE SECOND                                      │
│  ─────────────────────────────────────────────────────────────│
│  The code graph indexes your entire codebase as a persistent   │
│  knowledge graph. Claude queries it via MCP for instant         │
│  symbol lookup, dependency chains, and blast radius — instead   │
│  of reading hundreds of files.                                 │
│                                                                │
│  14 MCP tools │ 64 languages │ sub-ms queries │ zero deps      │
│  ~99% fewer tokens for navigation vs brute-force file reads    │
├────────────────────────────────────────────────────────────────┤
│  AUTO-UPDATED                                                  │
│  ─────────────────────────────────────────────────────────────│
│  File watcher keeps graph in sync. Post-commit hook ensures    │
│  freshness. No manual rebuild needed.                          │
└────────────────────────────────────────────────────────────────┘
```

---

## When to Use Graph vs Direct Read

| Task | Use Graph Tool | Use Direct Read? |
|------|---------------|------------------|
| Find function/class definition | `search_graph` | No |
| Get function signature + docs | `get_code_snippet` | No |
| Find all callers of a function | `trace_call_path` | No |
| Trace dependency chain | `query_graph` | No |
| Determine blast radius of change | `detect_changes` | No |
| Understand project architecture | `get_architecture` | No |
| Search for code patterns | `search_code` | No |
| Read full implementation to modify | `search_graph` to locate, then Read file | Yes |
| Understand business logic context | `get_code_snippet` for overview, then Read | Yes |

**Rule:** If a graph tool can answer the question, use it. Only open files
when you need the full source to make edits.

---

## Available MCP Tools

### Indexing & Status

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `index_repository` | Build/rebuild graph for a project | First setup, or after major restructure |
| `index_status` | Check if graph is current | Before querying, if unsure of freshness |
| `list_projects` | List all indexed projects | Multi-project navigation |

### Querying & Navigation

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `search_graph` | Find symbols by name (fuzzy) | "Find auth-related functions" |
| `search_code` | Text search across indexed codebase | "Find TODO comments", pattern matching |
| `get_code_snippet` | Get source code for a specific symbol | Need signature, docstring, implementation |
| `get_graph_schema` | Understand graph structure and relationships | Exploring what data is available |
| `query_graph` | Run structured graph queries | Complex dependency/relationship queries |

### Analysis

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `trace_call_path` | Trace caller/callee chains | "Who calls sendEmail?", "What does init() trigger?" |
| `detect_changes` | Identify changed files and blast radius | Before/after code changes, PR review |
| `get_architecture` | High-level module/package structure | Onboarding, understanding project layout |

### Management

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `delete_project` | Remove a project from the graph | Cleanup, project restructure |
| `manage_adr` | Architecture decision records | Document architectural decisions |
| `ingest_traces` | Import runtime traces | Performance analysis, dead code detection |

---

## Workflow: Before Any Code Change

```
0. PLAN       → get_architecture + search_graph to understand scope before planning
1. LOCATE     → search_graph to find the symbol
2. UNDERSTAND → get_code_snippet for context
3. BLAST      → detect_changes to assess impact
4. TRACE      → trace_call_path to find all affected callers
5. CHANGE     → Read file, make edit
6. VERIFY     → detect_changes again to confirm scope
```

**Step 0 applies to planning, not just coding.** When the user asks you to
plan a feature, refactor, or fix — query the graph first to understand
what exists, what depends on what, and what the scope looks like. This
prevents plans based on wrong assumptions about the codebase.

**Never skip step 3.** Blast radius analysis prevents unexpected breakage
from changes to shared code.

---

## Graph Data & Freshness

The graph stays fresh automatically through 3 layers — no manual rebuild needed:

| Layer | Trigger | What Happens |
|-------|---------|-------------|
| **File watcher** | Every file save | codebase-memory-mcp detects changes and re-indexes affected files in real-time |
| **Auto-index** | Session start | `auto_index: true` ensures graph is current when Claude Code starts |
| **Post-commit hook** | Every `git commit` | Touches `.code-graph/.needs-update` marker — file watcher picks it up (~10ms, non-blocking) |

**You do NOT need to manually re-index** unless you do a major restructure
(rename entire directories, switch branches with massive diffs). In that
case: `index_repository` once, then the 3 layers keep it fresh.

- **Storage**: `.code-graph/` directory (auto-created, gitignored)
- **MCP config**: `.mcp.json` at project root (committed, shared with team)

---

## MCP Configuration

The code graph MCP server is configured in `.mcp.json` at project root:

```json
{
  "mcpServers": {
    "codebase-memory": {
      "command": "codebase-memory-mcp",
      "args": []
    }
  }
}
```

**Installation:** `~/.claude/install-graph-tools.sh`

---

## Decision Framework

```
Need to find a symbol/function?
  → search_graph (sub-ms, structured result)
  → NOT: grep -r "functionName" (slow, unstructured)

Need to understand dependencies?
  → query_graph or trace_call_path (complete, traversable)
  → NOT: manually reading import statements

Need to assess change impact?
  → detect_changes (comprehensive, instant)
  → NOT: searching for usages manually across files

Need to understand architecture?
  → get_architecture (high-level overview)
  → NOT: reading every directory listing

Need to read/modify code?
  → search_graph to locate, then Read the specific file
  → NOT: reading entire directories hoping to find it
```

---

## Anti-Patterns

| Anti-Pattern | Do This Instead |
|-------------|-----------------|
| Grepping for function names | `search_graph` with the function name |
| Reading entire files to find a signature | `get_code_snippet` for the specific symbol |
| Manually tracing import chains | `trace_call_path` or `query_graph` |
| Making changes without checking impact | `detect_changes` before every edit to shared code |
| Reading all files in a directory | `get_architecture` for structure, `search_graph` for specifics |
| Ignoring graph staleness warnings | Check `index_status`, re-index if needed |
| Re-indexing on every query | Trust the file watcher; only manual re-index after major restructure |
