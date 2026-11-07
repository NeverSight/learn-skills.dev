---
name: read-codebase-context
description: Use when preparing to change or plan code in an unfamiliar repository, or when asked to explain code, trace a flow, find callers, dependencies, or tests, identify affected files, or assess change impact.
---

# Read Codebase Context

Choose tools by purpose; current source and tests establish facts.

## Refresh an impact map

When the active change's `tasks.md` (or a legacy plan) has an `## Impact map`, first check that it has
`Verified at: <full commit SHA>`. Verify that commit exists and is an ancestor
of `HEAD` with `git cat-file -e <sha>^{commit}` and
`git merge-base --is-ancestor <sha> HEAD`. If the SHA is missing, unavailable,
or not an ancestor (for example, after a rebase), discard the map for
navigation and trace existing source below. When no commit existed at map
creation, re-trace existing source; if the planned source does not exist yet,
use the source-less map rule in step 5 instead of tracing a nonexistent flow.

For a valid SHA, run `git status --short` and
`git diff --name-only <verified-sha>` to find committed, staged, and unstaged
tracked changes since the map; add untracked paths from `git status --short`.
Re-trace changed and newly touched paths, then always run Confirm for every
entry-point and implementation symbol in the map across the current repository
using FFF multi-pattern grep or `rg`. Read current source for every file to
edit and every newly found caller. The map guides navigation, not evidence.

## Delegate the trace

After Locate, immediately use one host spawn tool for an Expand-through-Read
question; size is irrelevant. OpenCode: call `task` with
`subagent_type: "explore"`. Assign no edits. Include goal, scope, repo path, no
further delegation, and impact-map fields with `path:line` evidence. Omit this
conversation; disable inherited history when supported (`fork_turns: "none"` in
Codex). Treat its result as navigation: verify current source. On spawn failure,
unverifiable claims, or no tool, search directly.

No-edit is a prompt, not a permission limit; verify no trace edits.

## Trace and record the impact

1. Check `docs/llm/AGENTS.md` and `docs/llm/INDEX.md` independently. If both
   exist, read both and open the relevant linked page. If only `INDEX.md`
   exists, read it, open a relevant linked page, and report the missing
   `AGENTS.md`. If only `AGENTS.md` exists, read it, report the missing index
   and no verified wiki page coverage. If neither exists, report no verified
   wiki coverage and continue. If an existing index has no relevant linked
   page, report no verified coverage for this task and continue.
2. Search in this order: **Locate → Expand → Confirm → Read**. Each tool is
   optional; use the fallback when it is unavailable, fails, or returns
   irrelevant results. Do not retry a failed tool repeatedly.

   | Stage | Need | Tool |
   |---|---|---|
   | Locate | Concept or behavior | OpenEZ `code_query` with `path: <repo root>` |
   | Locate | Approximate filename | FFF fuzzy file find (`find_files`); fallback `rg --files` |
   | Locate | Identifier or literal | FFF grep (`grep`); fallback scoped `rg` |
   | Locate | Regex | `rg` |
   | Expand | Callers and callees | OpenEZ `code_context` at 1–2 hops |
   | Confirm | Dynamic or registration references | FFF multi-pattern grep (`multi_grep`), fallback `rg`; search symbol, string, route, config key, camelCase/snake_case variants |
   | Read | Large-file structure | OpenEZ `code_outline`, then read needed current-source ranges; fallback `rg` and direct reads |

   FFF grep is literal; regex uses `rg`. Pass `maxResults` to FFF and
   `maxTokens` (about 1,500–3,000) to OpenEZ only when supported by the schema.
   Search/index results are navigation; read current source for evidence.

3. Query OpenEZ directly with the repo path; never require `list_workspaces`
   first. On unavailable, error, not indexed, or irrelevant results, fall back
   once to FFF/`rg` and direct reads. Mention `setup-openez` only when direct
   search cannot establish a needed relationship; never recommend it by repo
   size or install/configure tools silently.
4. OpenEZ lines and callers are hints. For `git status --short` paths, get
   positions from FFF/`rg` plus a direct read, or call OpenEZ
   `index_workspace` (`mode: "incremental"`) for the already-registered
   current workspace and re-query; `setup-openez` owns new registration.
   `memory_recall` (1–3 keywords, `maxTokens` if supported) may locate decisions
   or handoffs; read the file before relying on it. Memory may hold a decision's
   title and path, never the only record.
5. Read any existing entry point, implementation, direct callers, and
   downstream callees until the source establishes persistence and external
   boundaries. Inspect state changes, storage/external adapters, jobs, events,
   email/notifications, authorization, error paths, and relevant tests. Record
   an impact map:

   If the planned entry point or flow does not exist yet, do not invent current
   callers or trace nonexistent symbols. Keep the same fields and write
   `Entry: no existing source; planned entry: <design file + symbol>` and
   `Flow: no existing flow; planned flow: <design flow>`. Use planned files,
   effects, and checks only when the written design specifies them. Before
   joint approval, label those planned values `pending approval`; planning and
   estimation may use them, but implementation still requires approval. Write
   `not specified in design` for unknown planned behavior; do not present a
   planned map as a source trace.

   ```text
   Entry: <file + symbol>
   Flow: <caller → implementation → dependency>
   State changes: <persistence or "none found">
   External effects: <storage/job/event/email/notification or "none found">
   Change candidates: <files likely to modify>
   Verification: <tests/checks to run>
   Verified at: <output of `git rev-parse HEAD`, or "no commit exists">
   ```

   When refreshing a map from an active `tasks.md`, write it back to that file
   with `Verified at` updated to the current baseline. If new evidence changes
   approved behavior or scope, return to its approval gate instead of silently
   changing it.

6. Never fabricate a file impact list from index results or memory alone.

The local `.openez/` directory is derived index data. Keep it out of source
documentation and version control unless the target repository explicitly
chooses otherwise.
