---
name: docs
version: 0.0.2
category: productivity
description: "Code documentation agent — write/update docs with /docs write, check status with /docs check. Minimal code blocks, reference pointer based."
argument-hint: "<write|check> [topic] [code-path]"
---

## Input

```text
$ARGUMENTS
```

## Instructions

### Document Root

Documents managed by this skill are stored under `docs/generated/`.
They are organized by category subdirectories: `docs/generated/<category>/<slug>.md`

Documents outside `docs/generated/` are considered manually written and must never be modified.

### Tool Usage Rules

Always use the tools below for document search and management. Do not open files one by one — search smartly using patterns.

| Purpose | Tool | Usage |
|---------|------|-------|
| Find document files | **Glob** | `docs/generated/**/*.md` pattern to get full document list |
| Search frontmatter | **Grep** | Filter by `title:`, `category:` patterns |
| Read existing docs | **Read** | Read frontmatter + body (only necessary documents) |
| Verify code references | **Glob** | Check if file paths in `code_refs` exist |
| Create documents | **Write** | Create new document files |
| Update documents | **Edit** | Update specific parts of existing documents |
| Scan INDEX | **Read** | Read `docs/generated/INDEX.md` for category structure and document list |

### Subcommand Routing

The first word of `$ARGUMENTS` determines the subcommand.

| First word | Action |
|------------|--------|
| `write` | Read and execute `references/write-procedure.md` |
| `check` | Read and execute `references/check-procedure.md` |
| (none / help) | Print usage below and stop |

**When run without a subcommand:**

```
## docs

Code documentation agent — systematically records development knowledge.

### Commands

| Command | Description |
|---------|-------------|
| write <topic> [code-path] | Write or update a document on the topic |
| check | Check all document status (stale, broken refs, orphan docs) |

### Features

- Uses `[symbol](file-path)` reference pointers instead of code blocks
- Organized by category folders under `docs/generated/`
- INDEX.md based document indexing
```

### Argument Parsing

Parse the remaining arguments after removing the subcommand keyword (`write` / `check`).

**`write` arguments:**
- First argument: **topic** (required) — title/topic of the document
- Second argument: **code-path** (optional) — path to related code (file or directory)

Examples:
- `/docs write "auth flow design"` → topic only
- `/docs write "auth flow" src/auth/` → topic + code-path

**`check` arguments:** None.

### Document Writing Principles

1. **Minimize code blocks**: Do not include code snippets directly in documents. Instead, use markdown links in the form `[symbol](project-root-relative/file-path)` as references.
2. **Focus on design intent**: Record "why it was done this way" rather than "what was done".
3. **Protect manual documents**: Never modify documents outside `docs/generated/`.
