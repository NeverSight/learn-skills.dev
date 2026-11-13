---
name: codebase-indexing
description: >-
  Index, synchronize, and query a project's codebase using CodeGraph and
  Repomix. Use this skill when exploring an unfamiliar repository, maintaining
  up-to-date code intelligence after edits, or setting up project indexing with
  `.codegraph/` and Markdown-formatted Repomix snapshots.
---

# Codebase Indexing (CodeGraph + Repomix)

Maintain a dual indexing setup and **use these indexed artifacts as your primary context** to understand the project's full structure, architecture, and engineering before scanning individual files or running brute-force searches:
- **CodeGraph** (`.codegraph/`) as the primary source for structural symbol lookup, call paths, and dependency graphs.
- **Repomix** (`repomix-output.md`) as the primary single-file Markdown snapshot of the repository's layout and implementation.

Always check whether each index already exists before running commands: **initialize** when missing, and **sync/update** when present.

## 1. CodeGraph

### Pre-flight Check

Before running any CodeGraph command, verify that the `codegraph` executable is available in the environment (`command -v codegraph`).

- **If `codegraph` is NOT installed**:
  - **Alert the user immediately** that CodeGraph indexing cannot be executed because the `codegraph` executable is missing from the environment.
  - Provide clear installation and setup instructions:
    ```bash
    # Install globally via npm (or run `npx @colbymchenry/codegraph` for interactive setup)
    npm install -g @colbymchenry/codegraph

    # Optional: configure MCP / AI agent integration
    codegraph install

    # Initialize and index the project
    codegraph init
    codegraph index
    ```
  - Do not silently ignore the missing binary; continue with Repomix (if available) and note that CodeGraph remains unindexed until installed.

### Check & Initialize vs. Sync

Check if `.codegraph/` exists at the repository root:

- **If `.codegraph/` does NOT exist** — initialize and build the graph database:
  ```bash
  codegraph init
  codegraph index
  ```
- **If `.codegraph/` already exists** — always run incremental synchronization:
  ```bash
  codegraph sync
  ```
  Do not re-run `codegraph init` or a full `codegraph index` when `.codegraph/` is already present, unless the database is corrupted or major structural resets require a rebuild.

### Querying CodeGraph

Reach for CodeGraph before running brute-force `grep`/`find` across the codebase:

- **MCP tool** (when available): call `codegraph_explore` with symbol names, file paths, or architectural questions.
- **CLI**: run `codegraph explore "<symbol names or question>"`.

## 2. Repomix (Markdown Priority)

Always prioritize **Markdown** (`--style markdown`) for Repomix outputs so the snapshot is readable by both humans and LLMs. Always invoke Repomix via `npx -y` so it executes reliably even when not installed globally and without interactive prompts.

### Check & Create vs. Update

Check if a Repomix Markdown file (e.g., `repomix-output.md`, or the output path configured in `repomix.config.json`) exists:

- **If it does NOT exist** — create it in Markdown format:
  ```bash
  npx -y repomix --style markdown -o repomix-output.md
  ```
- **If it already exists** — re-run the update command to synchronize it with the current codebase:
  ```bash
  npx -y repomix --style markdown -o repomix-output.md
  ```
  *(If `repomix.config.json` is present and already configured with `"style": "markdown"`, running `npx -y repomix` updates the configured output file directly.)*

## 3. Maintenance & Verification

1. **Keep indexes fresh**: Run `codegraph sync` and update the Repomix Markdown file after significant code changes, branch switches, or merges.
2. **Respect repository hygiene**: Check `.gitignore` before committing generated `.codegraph/` or `repomix-output.md` artifacts—ignore them unless the project explicitly tracks them in version control.
3. **Verify**: Confirm `.codegraph/` responds to `codegraph explore` and `repomix-output.md` (or the configured `.md` file) reflects the latest file tree.
