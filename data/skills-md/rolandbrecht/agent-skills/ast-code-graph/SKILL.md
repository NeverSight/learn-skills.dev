---
name: ast-code-graph
description: >
  ALWAYS invoke this skill BEFORE using grep for any structural code analysis.
  Trigger on ANY of these patterns:

  **Structural pattern search:** "useEffect without dependency array", "async functions without try-catch", "User.objects.get() without exception handling", "fetch() calls outside src/api/", "console.log inside class methods", "route handlers missing error handling"

  **Bulk code migration/transformation:** wrap all async handlers, replace all X() calls with Y(), add error handling to all route handlers, rewrite deprecated API patterns across hundreds of files

  **Dependency & impact analysis:** "what does analyzePayment depend on", "blast radius of changing X", "which modules depend on ./lib/database.js", "direct and transitive dependencies"

  **Safe renaming:** "rename fetchUserData to getUserData safely", rename across TypeScript/JavaScript codebase

  **Dead code & circular imports:** "exports never imported anywhere", "circular imports causing webpack bundle", unused exports, which npm dependencies are actually used in source

  **ast-grep rules:** write an ast-grep rule, sg pattern, ast-grep syntax

  Trigger keywords: try-catch, useEffect, async without, circular imports, safe rename, blast radius, bulk migration, never imported, unused exports, ast-grep, enforce pattern, structural search, depends on, which modules.

  Do NOT trigger for: grep-able string searches, file-name lookups, reading READMEs, writing regex, CSV/data scripts.
---

# AST & Code Graph Indexing

## Overview

Text-based search (`grep`, `ripgrep`) finds string matches. AST-based analysis understands **structure** — it knows the difference between a function definition, a function call, a comment, and a string literal.

**Primary tool:** [ast-grep](https://ast-grep.github.io/) (`sg` / `ast-grep`) — a fast, Rust-based CLI for structural code search, lint, and rewriting. It uses tree-sitter for parsing and supports 20+ languages out of the box.

**Core principle:** When the question is about *code structure*, use AST analysis. When the question is about *text content*, use grep.

## When to Use

Use this skill when the task involves:

| Task | Why AST beats grep |
|------|--------------------|
| **Refactoring / renaming** | Grep finds the string in comments and strings too; AST finds only the symbol |
| **Dead code detection** | Grep can't tell if an export is actually imported elsewhere |
| **Dependency tracing** | "What modules does X depend on?" requires understanding `import`/`require` |
| **Impact analysis** | "If I change function X, what breaks?" needs call-graph traversal |
| **Circular dependency detection** | Requires building and analyzing a full import graph |
| **Code migration** | Rewriting deprecated API patterns structurally across a codebase |
| **Custom linting** | Enforcing project-specific patterns that standard linters don't cover |

**Don't use this skill when:**

- Searching for a specific string, error message, or config value → use `grep`
- Finding files by name or extension → use `find`/`fd`
- The codebase is < 5 files and you can read them all → just read them

---

## Prerequisites

Before using this tool for searches, you **MUST check** if `ast-grep` is installed natively on the system:

```bash
which ast-grep || which sg
```

If it is installed, use the native binary directly for semantic searches. **Do not** attempt to run it via Docker containers or complex wrapper scripts unless absolutely necessary.

If it is not installed, you can install it using one of the following methods depending on the OS:

- Node.js: `npm install -g @ast-grep/cli`
- MacOS (Homebrew): `brew install ast-grep`
- Rust (Cargo): `cargo install ast-grep --locked`

### Script Dependencies

The bundled scripts for graph building and AST parsing require additional dependencies:

- **JS/TS Parsing (`scripts/parse-js.mjs`)**: Requires Node.js v14+, `acorn`, and `acorn-walk`. Before running, check if they are installed globally or in the `ast-code-graph` directory. If not, you can install them by running `npm install acorn acorn-walk` in the `ast-code-graph` directory or `npm install -g acorn acorn-walk` globally.
- **Python Graph Builder (`scripts/build-graph.py`)**: Requires Python 3.8+ (uses standard library only, no external dependencies).

---

## Phase 1: Search — Find Code by Structure

### ast-grep (recommended — all languages)

`ast-grep` uses **pattern syntax** that looks exactly like the code you're searching for, using `$METAVAR` wildcards to match any AST node.

**Basic pattern search:**

```bash
# Find all calls to console.log
ast-grep -p 'console.log($MSG)' -l js src/

# Find all require() calls
ast-grep -p 'require($MOD)' -l js src/

# Find all async functions
ast-grep -p 'async function $NAME($$$PARAMS) { $$$BODY }' -l js src/

# Find if-else without braces
ast-grep -p 'if ($COND) $STMT' -l js src/
```

**Key metavariable syntax:**

- `$NAME` — matches a **single** AST node (like regex `.`). Example: `foo($ARG)` matches `foo(a)` but NOT `foo(a, b)`.
- `$$$ARGS` — matches **zero or more** nodes (like regex `.*`). Example: `foo($$$ARGS)` matches `foo()`, `foo(a)`, and `foo(a, b)`. **This is the most common pitfall! Default to `$$$` when matching arguments or block bodies unless you strictly want one node.**
- `$_` — anonymous match (when you don't need to reference it later).

**TypeScript generic calls require a separate pattern:**

In TypeScript/TSX, a call like `useState<string>('')` has `<string>` as a separate `type_arguments` AST node. The pattern `useState($$$ARGS)` will NOT match it. You need two passes for full coverage:

```bash
# Non-generic calls (works for all languages)
ast-grep -p 'useState($$$ARGS)' src/

# Generic TypeScript calls like useState<T>()
ast-grep -p 'useState<$T>($$$ARGS)' -l tsx src/
ast-grep -p 'useState<$T>($$$ARGS)' -l ts src/
```

Use `$$$T` instead of `$T` if the type argument can be a union like `string | null`.

**Search with rewrite preview:**

```bash
# Preview replacing var with const
ast-grep -p 'var $NAME = $VALUE' -r 'const $NAME = $VALUE' -l js src/

# Apply interactively (prompts y/n per match)
ast-grep -p 'var $NAME = $VALUE' -r 'const $NAME = $VALUE' -l js --interactive src/
```

See [ast-grep-cheatsheet.md](ast-grep-cheatsheet.md) for the full pattern reference.

---

## Phase 2: Pipeline JSON Output to Scripts

Often, simply printing matches to the terminal isn't enough. For complex analysis, you should export the matches as JSON and process them with a script. This is highly recommended for building graphs, finding dead code, or generating reports.

**Generate and save JSON:**

```bash
# Export all function definitions to a file for secondary analysis
ast-grep -p 'function $NAME($$$PARAMS) { $$$BODY }' -l typescript --json src/ > functions.json
```

Then, write a quick Python or Node.js script to read `functions.json` and extract the specific node text, line numbers, or relationships you need!
*(e.g., parsing the JSON to find functions that have a specific naming convention or parsing out all `import` sources to build a dependency graph).*

---

## Phase 3: Complex Workflows (Step-by-Step)

Here are detailed methodologies for solving complex structural problems:

### Workflow A: Impact Analysis (What breaks if I change X?)

1. **Search**: Find the definition of the target symbol `X` using `ast-grep` and ensure you have its exact name and module path.
2. **Find Direct Callers**: Use `ast-grep` to find all import statements that import `X`, and all function calls to `X()`. Save these results to a JSON file.
3. **Analyze**: If the codebase is large, write a quick script to parse the JSON and list the files/functions that call `X`.
4. **Iterate (Transitive Callers)**: If necessary, repeat the process for the functions that call `X` to build a full call graph. (Alternatively, if this is a Python project, use the bundled `build-graph.py` script as shown in Phase 4).

### Workflow B: Safe Refactoring / Migration

1. **Search**: `ast-grep -p '<pattern>' src/` to find all matches of the old pattern.
2. **Review**: Add `--json` to inspect match details and ensure your pattern isn't capturing unintended code boundaries (e.g. ensure you used `$$$BODY` for blocks, not `$BODY`).
3. **Preview**: Add `-r '<rewrite>'` to see the replacement printed to stdout. Check a few edge cases.
4. **Apply**: Add `--interactive` to selectively apply changes, or remove `--interactive` if you're 100% confident (though you should usually trust but verify).
5. **Verify**: Re-run the search pattern `ast-grep -p '<pattern>'` and ensure it returns 0 matches.

**Renaming a symbol requires multiple passes** — function definitions, call sites, and import/export statements are structurally distinct AST node types, so a single pattern won't catch all of them:

```bash
# Pass 1: rename the definition
ast-grep -p 'function oldName($$$P) { $$$B }' -r 'function newName($$$P) { $$$B }' -l ts src/

# Pass 2: rename all call sites (also catches bare references like arr.map(oldName))
ast-grep -p 'oldName($$$ARGS)' -r 'newName($$$ARGS)' -l ts src/

# Pass 3: rename named imports
ast-grep -p 'import { oldName } from $MOD' -r 'import { newName } from $MOD' -l ts src/
```

Note: AST matching is exact on identifiers, so `oldNameHelper` will NOT be affected — unlike a naive `sed` replace.

---

## Phase 4: Bundled Graph Builders (Fallback)

While `ast-grep` + JSON pipelines are powerful, this skill includes bundled scripts for common graph building tasks when you need full AST traversal beyond simple pattern matching.

*Use these particularly when checking for dead code or circular dependencies.*

> **🤖 Note to AI Agent:** When calling these bundled scripts, you must construct an **absolute path** by replacing `<SKILL_DIR>` with the absolute directory path where this `SKILL.md` file is located. Do not execute these with relative paths from the user's project root, or they will fail.

**Python codebases:**

```bash
python3 <SKILL_DIR>/scripts/build-graph.py <directory> [flags]

# Common Flags:
# --callers <symbol>  (find direct and transitive callers)
# --unused            (find dead code / unreferenced symbols)
# --depends-on <mod>  (find reverse dependencies)
# --cycles            (detect circular imports)
```

**JavaScript/TypeScript codebases:**

```bash
# Export a quick symbol list with line numbers
node <SKILL_DIR>/scripts/parse-js.mjs <file> --symbols
```

---

## Quick Reference

| I want to... | ast-grep command |
|---------------|-----------------|
| Find all calls to `foo()` | `ast-grep -p 'foo($$$ARGS)' src/` |
| Find function definitions | `ast-grep -p 'function $NAME($$$P) { $$$B }' src/` |
| Find unused imports | `ast-grep scan --inline-rules '...' src/` |
| Rename `oldFn` → `newFn` | 3 passes: definition, call sites, imports (see Workflow B) |
| Convert `var` → `const` | `ast-grep -p 'var $N = $V' -r 'const $N = $V' --interactive src/` |
| JSON output for scripting | `ast-grep -p '<pattern>' --json src/ > out.json` |
| Check change impact | Build graph → find all transitive callers (reverse BFS) |

## Supporting Files

- **[ast-grep-cheatsheet.md](ast-grep-cheatsheet.md)** — Full ast-grep pattern and CLI reference
- **[graph-schema.md](graph-schema.md)** — Node and edge type definitions with ER diagram
- **[query-patterns.md](query-patterns.md)** — Detailed cookbook of query patterns with examples
- **[scripts/parse-js.mjs](scripts/parse-js.mjs)** — Cross-platform Node.js script for JS/TS AST parsing
- **[scripts/build-graph.py](scripts/build-graph.py)** — Python code graph builder
