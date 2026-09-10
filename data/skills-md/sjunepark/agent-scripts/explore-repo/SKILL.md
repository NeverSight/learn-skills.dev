---
name: explore-repo
description: "Explore external GitHub or Git source from the centralized `~/.repos` cache for pinned refs, upstream comparison, or delegated repository inspection."
---

# Explore Repo

Inspect external source from a stable cache outside the current project.

## Workflow

1. Decide whether external source inspection is warranted.
- Prefer installed source or primary documentation when it answers the question directly.
- Inspect the external repo when behavior depends on implementation details, version-specific control flow, defaults, generated files, or undocumented edge cases.
- If the user names a repository, branch, tag, commit, or package version, treat that as the target source unless local evidence points to a more exact ref.

2. Use the central repo cache.
- Default cache root: `~/.repos`.
- Use a host-qualified path:

  ```text
  ~/.repos/github.com/<owner>/<repo>
  ~/.repos/<host>/<owner-or-group>/<repo>
  ```

- Strip a trailing `.git` from the directory name.
- Do not clone external repos into the current project, `.tmp/`, or a tracked worktree unless the user explicitly asks for that location.

3. Reuse or create the clone.
- If the cache path already exists, inspect it before updating:

  ```bash
  git -C ~/.repos/github.com/<owner>/<repo> status --short --branch
  git -C ~/.repos/github.com/<owner>/<repo> remote -v
  ```

- If the clone is dirty, do not reset, clean, pull, checkout, or overwrite it without explicit user approval. Report the dirty state and either inspect read-only or create a separate worktree under `~/.repos/.worktrees/`.
- If the clone is clean and current source is acceptable, update with:

  ```bash
  git -C ~/.repos/github.com/<owner>/<repo> fetch --prune --tags
  ```

- For a new clone, prefer a partial clone:

  ```bash
  mkdir -p ~/.repos/github.com/<owner>
  git clone --filter=blob:none <url> ~/.repos/github.com/<owner>/<repo>
  ```

- Add `--depth=1` only when history is not needed. Avoid shallow clones when comparing commits, inspecting history, or checking old tags.

4. Check out the needed ref.
- If a branch, tag, commit, release, or dependency version matters, fetch and check out that exact ref.
- Record the inspected ref for the final answer:

  ```bash
  git -C ~/.repos/github.com/<owner>/<repo> rev-parse --short HEAD
  git -C ~/.repos/github.com/<owner>/<repo> status --short --branch
  ```

5. Explore with focused reads.
- Use `rg`, `rg --files`, `git grep`, `git log`, and narrow file reads before opening broad source files.
- Delegate broad or independent exploration to subagents when available. Use a
  fast, low-reasoning configuration for routine source scans and a more capable
  configuration when the subagent must understand complex logic, architecture,
  cross-module behavior, or subtle implementation tradeoffs. Ask for concise
  findings, supporting paths, refs, and minimal quoted code.

6. Use worktrees for experiments.
- Keep cached clones read-only by default.
- If builds, edits, generated files, or risky checkouts are needed, create an isolated worktree:

  ```bash
  mkdir -p ~/.repos/.worktrees
  git -C ~/.repos/github.com/<owner>/<repo> worktree add --detach ~/.repos/.worktrees/<repo>-<task> <ref>
  ```

- Remove worktrees only when they were created for the current task and are no longer needed.

7. Report the result.
- Cite the cache path, remote URL, inspected ref, and relevant files or symbols.
- Separate direct source observations from inference.

## Guardrails

- Do not create or update project-local ignore rules just to hide external clones.
- Do not delete cached repos unless the user asks for cleanup.
- Do not wire cached external repos into the current project as dependencies.
- Do not paste large source files into the answer.

## Cleanup

Use `~/.repos` as an intentional cache, not disposable task output. When storage cleanup is requested, inspect size and age first, then propose or remove specific stale repos:

```bash
du -sh ~/.repos/* 2>/dev/null
find ~/.repos -mindepth 2 -maxdepth 4 -type d -name .git -prune -exec dirname {} \;
```
