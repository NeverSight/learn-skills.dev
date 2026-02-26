---
name: sdx-commit
description: Analyze current git changes, group them by logical/OpenSpec change, and make conventional commits for each group. Use when the user wants clean, structured commits instead of one mixed commit.
license: MIT
metadata:
  author: [md@rcbd.org]
  version: "1.0"
---

Analyze the current git diff, group files into logical changes, then produce concise conventional-commit messages and commit each group separately.

---

## Steps

1. **Check for changes**

   ```bash
   git status --porcelain
   ```

   If there are no changes, tell the user "Nothing to commit" and stop.

2. **Analyze changed files before staging**

   Collect changed paths (modified, staged, untracked) and inspect them:

   ```bash
   git status --porcelain
   git diff --name-only
   git diff --cached --name-only
   ```

   Build **file groups** before staging anything.

   **Grouping priority (in order):**
   - **OpenSpec change groups**: files under `openspec/changes/<change-name>/` and related code/docs that clearly implement that same change
   - **Shared infra/support groups**: cross-cutting files (build/config/tooling/logging helpers) that don’t belong cleanly to one change
   - **Skill/docs groups**: skill files, agent config, docs-only updates

   Prefer **one commit per change group**. If there is only one clear group, use one commit.

   **Important:** If a single file contains unrelated edits for multiple groups and cannot be split cleanly at file-level, ask the user before proceeding (or keep it in one group and explain the tradeoff).

3. **Draft a commit plan (group-by-group)**

   For each group:
   - list files in the group
   - summarize intent
   - draft a conventional commit message

   Use the commit message format below.

4. **Present the plan and ask for confirmation**

   Show:
   - proposed groups (with files)
   - proposed commit message for each group

   Ask for confirmation before staging/committing.

5. **Stage and commit each group individually**

   For each confirmed group, in order:

   a. Stage only that group’s files
   ```bash
   git add -- <file1> <file2> ...
   ```

   b. Review the staged summary
   ```bash
   git diff --cached --stat
   git diff --cached --name-only
   ```

   c. Commit using the group’s message
   ```bash
   git commit -m "<message>"
   ```

   For multi-line messages, use multiple `-m` flags.

   d. Continue to the next group (index should be clean after commit)

6. **Commit message format (reference for each group)**

   Use this format for each group commit:

   ```
   feat(<scope>): concise description of what changed
   ```

   Rules:
   - **scope** = the logical area affected. Use short names like: `connector`, `db`, `api`, `engine`, `frontend`, `docs`, `config`, `infra`.
   - If a change maps to a known openspec change (check `openspec/changes/*/`), use that change name as the scope. For example: `feat(mvp-full-sync): add Klaviyo connector`.
   - Each line should be ≤ 72 characters.
   - Use `feat` for new features, `fix` for bug fixes, `refactor` for restructuring, `docs` for documentation, `chore` for config/build changes.
   - If all changes are part of one logical unit, a single line is fine.
   - If changes span multiple areas, use multiple lines — first line is the primary change, subsequent lines are secondary.

   Example single-line:
   ```
   feat(connector): add Klaviyo connector with cursor pagination
   ```

   Example multi-line:
   ```
   feat(connector): add Klaviyo connector with cursor pagination

   feat(api): expose embedded PG URL via /api/config endpoint
   fix(db): clean up stale postmaster.pid on startup
   chore(docs): add project README
   ```

   This applies to **each group commit**.

7. **Confirm all commits**

   Show recent commits created in this run (usually the last N lines):

   ```bash
   git log --oneline -<N>
   ```

   Confirm each planned group was committed.

---

## Guidelines

- Be **concise**. Each line should tell the reader _what_ changed, not _how_.
- Prefer **action verbs**: add, fix, remove, update, refactor, extract.
- Don’t list every file in commit messages — summarize by intent.
- If there are 10+ files changed across 3+ areas, still aim for ≤ 5 commit message lines.
- When in doubt, fewer lines is better.
- Prefer multiple small commits over one mixed commit when changes map to different OpenSpec changes.
- Group by **change first**, then by layer (api/frontend/docs) within that change.
