---
name: virgil
description: >
  Parse, explore, and understand unfamiliar codebases using virgil-cli. Covers
  the full workflow: parsing source into Parquet, querying with built-in commands,
  navigating dependencies and callers, and running raw DuckDB SQL. Use when asked
  to analyze a codebase, understand architecture, find symbols, trace dependencies,
  onboard to a project, investigate bugs, or map the API surface of any
  TypeScript/JavaScript/C/C++/C#/Rust/Python/Go/Java/PHP codebase.
---

# Virgil — Codebase Exploration Skill

## Prerequisites

Check that virgil is available:

```bash
virgil --help
```

If not installed, build from source:

```bash
cargo install --git https://github.com/virgil-cli/virgil-cli
```

## Core Workflow

Every codebase exploration follows three phases:

### Phase 1 — Parse

```bash
virgil parse <PROJECT_DIR> --output <DATA_DIR>
```

This produces five Parquet files in `<DATA_DIR>`: `files.parquet`, `symbols.parquet`, `imports.parquet`, `comments.parquet`, `errors.parquet`.

Parse once, query many times. Re-parse only when source changes.

### Phase 2 — Orient

```bash
virgil overview --data-dir <DATA_DIR> --format json
```

Overview gives you: language breakdown, top symbols by usage, directory structure, hub files (most imported), dependency summary, and barrel file detection.

### Phase 3 — Drill Down

Use targeted commands to investigate specifics:

```bash
virgil search <QUERY> --data-dir <DATA_DIR> --format json
virgil outline <FILE> --data-dir <DATA_DIR> --format json
virgil deps <FILE> --data-dir <DATA_DIR> --format json
virgil callers <SYMBOL> --data-dir <DATA_DIR> --format json
```

## Output Format

- Use `--format json` when processing output programmatically (AI agent consumption)
- Use `--format table` when displaying results to the user
- Use `--format csv` for export to spreadsheets or pipelines

All query commands support `--format table|json|csv`. Default is `table`.

## Quick Command Reference

| Command | Purpose | Key Args |
|---------|---------|----------|
| `parse` | Parse source into Parquet files | `<DIR>`, `-o`, `-l` |
| `overview` | High-level codebase summary | `--depth` |
| `search` | Fuzzy symbol search | `<QUERY>`, `--kind`, `--exported` |
| `outline` | All symbols in one file | `<FILE>` |
| `files` | List parsed files | `--language`, `--directory`, `--sort` |
| `read` | Read source with line ranges | `<FILE>`, `--start-line`, `--end-line`, `--root` |
| `query` | Raw DuckDB SQL | `<SQL>` |
| `deps` | What a file imports | `<FILE>` |
| `dependents` | What imports a file | `<FILE>` |
| `callers` | Who imports a symbol | `<SYMBOL>`, `--limit` |
| `imports` | List imports with filters | `--module`, `--kind`, `--external`, `--internal` |
| `comments` | List comments with filters | `--file`, `--kind`, `--documented`, `--symbol` |
| `errors` | List parse errors | `--error-type`, `--language` |

Full flag-by-flag docs: see `references/command-reference.md`

## Path Conventions

- **All file paths in Parquet are relative** to the project root passed to `parse`.
- `--data-dir` points to the directory containing the Parquet files (default: `.`).
- `--root` (on `read` command) points to the project source root for resolving relative paths.
- When `parse` and query commands run from the project root with default `--output .`, no extra flags are needed.

## Parquet Table Schemas

Five tables are available for SQL queries via `virgil query`:

### files

| Column | Type | Description |
|--------|------|-------------|
| path | Utf8 | Relative path from project root |
| name | Utf8 | File name |
| extension | Utf8 | Extension without dot |
| language | Utf8 | Language identifier |
| size_bytes | UInt64 | File size in bytes |
| line_count | UInt64 | Number of lines |

### symbols

| Column | Type | Description |
|--------|------|-------------|
| name | Utf8 | Symbol name |
| kind | Utf8 | Symbol kind (see below) |
| file_path | Utf8 | Relative file path |
| start_line | UInt32 | 0-based start line |
| start_column | UInt32 | 0-based start column |
| end_line | UInt32 | 0-based end line |
| end_column | UInt32 | 0-based end column |
| is_exported | Boolean | Whether the symbol is exported |

**Symbol kinds:** `function`, `class`, `method`, `variable`, `interface`, `type_alias`, `enum`, `arrow_function`, `struct`, `union`, `namespace`, `macro`, `property`, `typedef`, `trait`, `constant`, `module`

### imports

| Column | Type | Description |
|--------|------|-------------|
| source_file | Utf8 | File containing the import |
| module_specifier | Utf8 | Import path (e.g., `react`, `./utils`) |
| imported_name | Utf8 | Imported symbol name (`*` for namespace) |
| local_name | Utf8 | Local binding name |
| kind | Utf8 | Import kind (see below) |
| is_type_only | Boolean | Whether the import is type-only |
| line | UInt32 | Line number |
| is_external | Boolean | External library (true) vs user code (false) |

**Import kinds:** `static`, `dynamic`, `require`, `re_export`, `include`, `using`, `use`, `import`, `from`

### comments

| Column | Type | Description |
|--------|------|-------------|
| file_path | Utf8 | Relative file path |
| text | Utf8 | Raw comment text including delimiters |
| kind | Utf8 | Comment kind: `line`, `block`, `doc` |
| start_line | UInt32 | 0-based start line |
| start_column | UInt32 | 0-based start column |
| end_line | UInt32 | 0-based end line |
| end_column | UInt32 | 0-based end column |
| associated_symbol | Utf8 (nullable) | Name of documented symbol |
| associated_symbol_kind | Utf8 (nullable) | Kind of documented symbol |

### errors

| Column | Type | Description |
|--------|------|-------------|
| file_path | Utf8 | Path of file that failed |
| file_name | Utf8 | File name |
| extension | Utf8 | Extension without dot |
| language | Utf8 | Language identifier |
| error_type | Utf8 | Error type: `parser_creation`, `file_read`, `parse_failure` |
| error_message | Utf8 | Human-readable error description |
| size_bytes | UInt64 | File size in bytes |

## Supported Languages

| Language | Extensions | Export Detection |
|----------|------------|-----------------|
| TypeScript | `.ts` | ES `export` keyword |
| TSX | `.tsx` | ES `export` keyword |
| JavaScript | `.js` | ES `export` keyword |
| JSX | `.jsx` | ES `export` keyword |
| C | `.c`, `.h` | Not `static` = exported |
| C++ | `.cpp`, `.cc`, `.cxx`, `.hpp`, `.hxx`, `.hh` | Not `static` = exported |
| C# | `.cs` | `public`/`internal` modifier |
| Rust | `.rs` | `pub` visibility modifier |
| Python | `.py`, `.pyi` | No leading `_` = exported |
| Go | `.go` | Uppercase first letter |
| Java | `.java` | `public` modifier |
| PHP | `.php` | `public` visibility (default) |

## Strategic Playbooks

Six pre-built exploration strategies for common tasks:

1. **Understand codebase architecture** — overview, hub files, outline, SQL deep-dives
2. **Find where something is defined/used** — search, read, callers, dependents
3. **Onboard to new codebase** — parse, overview, files by dependents, outline, read, imports
4. **Investigate a bug** — search, read, deps, callers, read callers, comments
5. **Understand dependencies** — deps, dependents, imports filters, overview, SQL
6. **Map the API surface** — overview, search exported, filter by kind, SQL

Each playbook is a numbered step-by-step command sequence.
Full playbooks: see `references/strategies.md`

## Raw SQL

For questions that built-in commands can't answer, use raw DuckDB SQL:

```bash
virgil query "SELECT kind, COUNT(*) as cnt FROM symbols GROUP BY kind ORDER BY cnt DESC" --data-dir <DATA_DIR> --format json
```

Available tables: `files`, `symbols`, `imports`, `comments`, `errors`.

Reusable query recipes by category (files, symbols, dependencies, comments, cross-table): see `references/sql-recipes.md`

## Reference

- Full command flags: `references/command-reference.md`
- Strategic playbooks: `references/strategies.md`
- SQL query recipes: `references/sql-recipes.md`
