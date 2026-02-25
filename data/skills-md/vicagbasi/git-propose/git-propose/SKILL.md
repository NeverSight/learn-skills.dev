---
name: git-propose
description: Review full Git working tree changes and propose one or more safe, reviewable commit messages plus commit ordering. Use when the user asks for "git propose", asks how to split current changes into commits, or wants Conventional Commit messages from staged, unstaged, and untracked changes.
---

# Git Propose

Review all working directory changes and return commit proposal output in the exact structure below. Prefer best-effort recommendations over questions unless risk is material (secrets/data loss).

## Gather Git State

Run:

```bash
git rev-parse --is-inside-work-tree
git status --porcelain=v1
git ls-files --others --exclude-standard
git diff --staged --name-status
git diff --name-status
git diff --staged
git diff
git diff --staged --stat
git diff --stat
```

Treat staged content as intentional unless incomplete or unsafe without related unstaged changes.
Assess all change buckets before proposing commits:
- staged tracked changes
- unstaged tracked changes
- untracked files

## Preflight and Empty-State Rules

- Run `git rev-parse --is-inside-work-tree` first. If it fails, do not run remaining git-state commands.
- If not inside a git work tree, return the required output format with:
  - `Repo State Summary`: `Not a git repository`.
  - `Proposed Commit Plan`: `0 commits`.
  - `Build-Mode Notes`: assumption that no git state is available.
- If working tree is clean (no staged, unstaged, or untracked changes), return the required output format with:
  - `Repo State Summary`: `Clean working tree`.
  - `Proposed Commit Plan`: `0 commits`.
  - `Commit Proposals (Ready to Paste)`: `No commit proposed`.

## Required Output Format

Return exactly these section headings in this order:
- `## Repo State Summary`
- `## Red Flags / Safety Notes (if any)`
- `## Proposed Commit Plan`
- `## Commit Proposals (Ready to Paste)`
- `## Build-Mode Notes`

Required content inside those sections:
- Repo State Summary:
  - Staged: brief summary
  - Unstaged: brief summary
  - Untracked: brief summary and include when needed for commit intent
  - Mixed staged/unstaged in same files: yes/no and impact
- Red Flags / Safety Notes:
  - Call out secrets/credentials, generated artifacts, lockfile-only drift, huge formatting churn, risky partial staging
- Proposed Commit Plan:
  - Number of commits
  - Rationale for split/merge choice
  - Why ordering is reviewable
- Commit Proposals:
  - Intent / Scope (no file paths)
  - Suggested staging (by intent, no file paths)
  - Full commit message: title + blank line + body + optional footers
  - Files included (required): explicit file path list to stage for the commit (not part of commit message)
- Build-Mode Notes:
  - Explicit assumptions
  - Ask clarifying questions only for real risk

Use this exact Markdown skeleton:

```markdown
## Repo State Summary
- Staged: ...
- Unstaged: ...
- Untracked: ...
- Mixed staged/unstaged in same files: ...

## Red Flags / Safety Notes (if any)
- ...

## Proposed Commit Plan
- Number of commits: ...
- Rationale for split/merge choice: ...
- Why ordering is reviewable: ...

## Commit Proposals (Ready to Paste)
### Commit 1
- Intent / Scope: ...
- Suggested staging: ...
- Full commit message:
  - Subject: `type(scope): Subject`
  - Body:
    - `Body line 1`
    - `Body line 2`
 - Files included:
   - `path/to/file.ext`
   - `path/to/other.ext`

## Build-Mode Notes
- Explicit assumptions: ...
- Clarifying questions (only if real risk): ...
```

## Commit Strategy Rules

- Choose single commit for one cohesive concern.
- Split commits by concern when feature/refactor/fix/docs/tooling are mixed.
- Favor cohesion over raw size.
- Order by dependency and narrative:
  - enabling refactors first
  - functional changes next
  - tests with the behavior they verify
  - docs after behavior
- Keep each commit independently reviewable and preferably revertible.

## Commit Message Rules

- Use Conventional Commits: `type(scope): subject`.
- Allowed types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `perf`, `style`, `ci`.
- Write subject in imperative present tense, capitalized, no trailing period.
- Keep subject near 50 chars (can stretch when clarity requires).
- Insert one blank line between subject and body.
- Write body around 72-char wraps; explain why, approach, and tradeoffs.
- Avoid file paths and line references in commit body.
- File paths are allowed only in the per-commit `Files included` section.
- Add optional footers (`Fixes #123`, `BREAKING CHANGE: ...`) when relevant.

## Ambiguity Handling

- In build-like execution, continue with best-effort proposals and state assumptions.
- Ask a question only when proceeding may introduce material risk.
