---
name: update-docs
description: Analyse code changes since the last docs update and refresh the project's documentation files. Use when code has changed and documentation needs to be updated, after implementing new features, or before a milestone commit.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Update Docs Workflow

Use this workflow whenever code has changed and the project documentation needs to be brought up to date. The agent uses `git` to detect what changed since the last documentation commit, analyses the diff, and updates only the affected docs.

This workflow is **project-agnostic**: it auto-detects the project root and documentation location.

---

## Step 1 — Orient: detect the project

// turbo
Run the following to establish the project root and basic structure:

```bash
# Project root and current branch
git rev-parse --show-toplevel && git branch --show-current

# Last 5 commits (so we can pick the baseline)
git log --oneline -5
```

Then find where the documentation lives:

```bash
# Look for common doc directory patterns
find "$(git rev-parse --show-toplevel)" -maxdepth 3 -type d \
  \( -name "docs" -o -name "doc" -o -name "wiki" -o -name "pages" \) \
  ! -path "*/.git/*" ! -path "*/node_modules/*" ! -path "*/.venv/*"

# Also check for top-level markdown files
find "$(git rev-parse --show-toplevel)" -maxdepth 1 -name "*.md" -type f
```

From the results, identify:

- **`$ROOT`**: the git root directory
- **`$DOCS_DIR`**: where the documentation files are (e.g. `docs/src/`, `docs/`, `wiki/`)

If `$DOCS_DIR` cannot be determined automatically, ask the user: **"Where are your documentation files? (e.g. `docs/`, `docs/src/`, or `README.md` only)"**

---

## Step 2 — Find the baseline commit

// turbo
Find the most recent commit that touched the documentation directory:

```bash
git log --oneline --all -- "$DOCS_DIR" | head -5
```

Note the first hash — call it `<baseline>`. This is the last point in time when docs were current.

If no doc commits exist, use the initial commit as baseline:

```bash
git log --oneline --all | tail -1
```

---

## Step 3 — Get the code diff since the baseline

// turbo
First, a compact summary of what changed in source code (not docs):

```bash
git diff <baseline> HEAD --stat -- . \
  ':!'"$DOCS_DIR" ':!*.md' ':!*.rst' ':!*.txt' ':!*.json'
```

If the diff is manageable, get the full diff:

```bash
git diff <baseline> HEAD -- . \
  ':!'"$DOCS_DIR" ':!*.md' ':!*.rst' ':!*.txt' ':!*.json'
```

> **Tip**: If the diff exceeds ~400 lines, analyse it **file by file** using:
>
> ```bash
> git diff <baseline> HEAD -- path/to/file.py
> ```
>
> Focus on: new/deleted classes or functions, changed method signatures, new modules, changed configuration keys, new data files.

---

## Step 4 — Discover existing documentation structure

Read the documentation files discovered in Step 1. Understand:

- What topics each file covers
- What module/component/concept each file documents
- The writing style (language, heading level, use of code blocks, tables)

Maintain the same style and language as the existing docs when making edits.

---

## Step 5 — Map changes to affected docs

For each changed file or module, determine which documentation file(s) need updating.

**General mapping heuristics** (adapt to the specific project structure):

| Type of code change                            | What to update                                                                              |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------- |
| New class or module added                      | Add it to whichever architecture/overview doc covers that layer; update dependency diagrams |
| Class or function deleted                      | Remove or strike from all docs that mention it                                              |
| Method signature / parameter changed           | Update code examples, parameter tables                                                      |
| New config key or environment variable         | Update configuration docs                                                                   |
| New external dependency added                  | Update setup/installation docs                                                              |
| Data schema changed (DB, JSON, Pydantic, etc.) | Update data model docs                                                                      |
| New CLI command or flag                        | Update CLI reference / usage docs                                                           |
| Behaviour change (algorithm, business logic)   | Update design/architecture docs                                                             |
| New test coverage (major new tests)            | No doc update usually needed unless testing guide exists                                    |

---

## Step 6 — Make surgical edits to affected docs

Update **only** the sections that are out of date. Do not rewrite sections that are still accurate.

Edit rules:

- **Add** new items (classes, methods, parameters, config keys) that appeared in the diff
- **Remove or revise** descriptions of things that were renamed, deleted, or refactored
- **Update** flow diagrams, step-by-step pipelines, and tables to reflect new reality
- **Preserve** all sections not touched by the diff — no gratuitous rewrites
- Match the writing style of the existing doc exactly (language, formatting, code fence style)

---

## Step 7 — Summarise changes and optionally commit

After all edits, display a brief summary:

- Which doc files were modified
- What was added / removed / updated in each

Then ask the user: **"文档已更新。是否要将这些改动提交到 Git？(Y/n)"**

If yes, suggest a commit message in the format:

```
docs: update <DOCS_DIR> to reflect changes since <baseline-short-hash>
```

Then run (replace `<DOCS_DIR>` and `<message>` accordingly):

```bash
git add <DOCS_DIR> && git commit -m "<message>"
```

If no, remind the user that all files are already saved and can be committed later with:

```bash
git add <DOCS_DIR> && git commit -m "docs: ..."
```
