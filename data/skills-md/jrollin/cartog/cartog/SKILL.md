---
name: cartog
description: >-
  Code graph navigation and impact analysis. Use when the user asks
  "where is X defined?", "what calls X?", "who imports X?", "what depends on X?",
  "what breaks if I change X?", "help me refactor X", "show me the call graph",
  "find all usages of X", "show file structure", or needs to navigate code,
  locate definitions, trace dependencies, assess blast radius of changes,
  support refactoring (rename, extract, move), or explore an unfamiliar codebase.
  Supports Python, TypeScript/JavaScript, Rust, Go, Ruby.
---

# cartog — Code Graph Navigation Skill

## When to Use

Use cartog **before** reaching for grep, cat, or file reads when you need to:
- Discover symbols by partial name → `cartog search <query>`
- Understand the structure of a file → `cartog outline <file>`
- Find who references a symbol → `cartog refs <name>` (or `--kind calls` for just callers)
- See what a function calls → `cartog callees <name>`
- Assess refactoring impact → `cartog impact <name> --depth 3`
- Understand class hierarchies → `cartog hierarchy <class>`
- See file dependencies → `cartog deps <file>`

## Why cartog Over grep/glob

cartog pre-computes a code graph (symbols + edges) with tree-sitter and stores it in SQLite. Compared to grep/glob:
- **Fewer tool calls**: 1 command vs 3-6 grep/read cycles
- **Transitive analysis**: `impact --depth 3` traces callers-of-callers — grep can't do this
- **Structured results**: symbols with types, signatures, and line ranges — not raw text matches

## Workflow Rules

1. **Before you grep or read a file to understand structure**, query cartog first.
2. **Start with `cartog search <query>`** to locate any symbol before calling `refs`, `callees`, or `impact`:
   - If the output contains **exactly one result**, use that symbol name and file — proceed.
   - If multiple results share the same name but different files, add `--file <path>` to pick the right one — proceed.
   - If multiple results have different names, add `--kind <kind>` to filter, then re-evaluate.
   - Never pass an ambiguous name to `refs`/`callees`/`impact` — the result will be wrong.
3. **Use `cartog outline <file>`** instead of `cat <file>` when you need structure, not content.
4. **Before refactoring**, run `cartog impact <symbol>` to see the blast radius.
5. **Only fall back to grep/read** when cartog doesn't have what you need (e.g., reading actual implementation logic, string literals, config values).
6. **After making code changes**, run `cartog index .` to update the graph.

## Setup

Before first use, ensure cartog is installed and indexed:

```bash
# Install if missing
command -v cartog || bash scripts/install.sh

# Index (incremental — safe to re-run)
cartog index .
```

## Commands Reference

### Index (build/rebuild)
```bash
cartog index .                    # Index current directory
cartog index src/                 # Index specific directory
```

### Search (find symbols by partial name)
```bash
cartog search parse                          # prefix + substring match
cartog search parse --kind function          # filter by symbol kind
cartog search config --file src/db.rs        # filter to one file
cartog search parse --limit 10              # cap results
```
Returns symbols ranked: exact match → prefix → substring. Case-insensitive. Max 100 results.

Valid `--kind` values: `function`, `class`, `method`, `variable`, `import`.

### Outline (file structure)
```bash
cartog outline src/auth/tokens.py
```
Output shows symbols with types, signatures, and line ranges — no need to read the file.

### Refs (who references this?)
```bash
cartog refs validate_token               # all reference types
cartog refs validate_token --kind calls  # only call sites
```
Available `--kind` values: `calls`, `imports`, `inherits`, `references`, `raises`.

### Callees (what does this call?)
```bash
cartog callees authenticate
```

### Impact (transitive blast radius)
```bash
cartog impact SessionManager --depth 3
```
Shows everything that transitively depends on a symbol up to N hops.

### Hierarchy (inheritance tree)
```bash
cartog hierarchy BaseService
```

### Deps (file imports)
```bash
cartog deps src/routes/auth.py
```

### Stats (index summary)
```bash
cartog stats
```

## JSON Output

All commands support `--json` for structured output:
```bash
cartog --json refs validate_token
cartog --json outline src/auth/tokens.py
```

## Refactoring Workflow

Before changing any symbol (rename, extract, move, delete):

1. **Identify** — `cartog search <name>` to confirm the exact symbol name and file
2. **Map references** — `cartog refs <name>` to find every usage
3. **Assess blast radius** — `cartog impact <name> --depth 3` for transitive dependents
4. **Check hierarchy** — `cartog hierarchy <name>` if it's a class (subclasses need updating too)
5. **Plan change order** — update leaf dependents first, work inward toward the source
6. **Apply changes** — modify files
7. **Re-index** — `cartog index .` to update the graph
8. **Verify** — re-run `cartog refs <name>` to confirm no stale references remain

## Decision Heuristics

| I need to... | Use |
|-------------|-----|
| Discover symbols matching a partial name | `cartog search <query>` |
| Find where a symbol is defined | `cartog search <query>` then `cartog outline <file>` |
| Know what's in a file | `cartog outline <file>` |
| Find usages of a function | `cartog refs <name>` (use `--kind calls` for just callers) |
| Understand what a function does at a high level | `cartog callees <name>` |
| Check if a change is safe | `cartog impact <name>` |
| Understand class hierarchy | `cartog hierarchy <class>` |
| See file dependencies | `cartog deps <file>` |
| Read actual implementation logic | `cat <file>` (cartog can't help here) |
| Search for string literals / config | `grep` (cartog indexes structure, not content) |

## Limitations

- Structural/heuristic resolution, not full semantic. ~90% accuracy for cross-file references.
- Currently supports: Python, TypeScript/JavaScript, Rust, Go, Ruby. Java planned.
- Does not index string literals, comments (except docstrings), or config values.
- Method resolution is name-based — `foo.bar()` resolves `bar`, not `Foo.bar` specifically.
