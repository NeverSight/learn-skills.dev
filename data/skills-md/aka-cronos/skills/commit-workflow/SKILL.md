---
name: commit-workflow
description: >-
  Commit: use when a commit needs making, a commit message
  needs drafting, or another skill needs a commit made.
metadata:
  author: aka-cronos
---

# Commit Workflow

Every commit is **atomic**: one logical concern, one message.

## Source of truth

Commit policy — types, subject format, body rules, footers — lives in
[references/commit-best-practices.md](references/commit-best-practices.md). Read it before
drafting any message. If the project ships `.agents/rules/commit-best-practices.md` (or the
Cursor adapter `.cursor/rules/commit-best-practices.mdc`), that file overrides these defaults.

## Workflow

### Step 1: Inspect staged state

Run `git status --short`, `git diff --cached --name-only`, and `git diff --cached --stat`.

If nothing is staged, report it and stop.

**Done when:** you have the full list of staged files and the diffstat.

### Step 2: Group by concern

Assign every staged file to a concern group. Common groups:

- docs (`docs/**`, `README*`)
- tooling/config (`.cursor/**`, `.agents/**`, `.github/**`, config files)
- app code (`apps/**`, `src/**`, `app/**`, `components/**`)
- packages (`packages/**`)
- backend/data (`**/convex/**`, `db/**`, migrations)
- tests (`**/*.test.*`, `tests/**`)

Files that fit none of these get a group by best judgment — read the diff when the path alone
is ambiguous.

**Done when:** every staged file belongs to exactly one group, with none left unassigned.

### Step 3: Split by concern

One atomic commit per group. With more than one group, set the boundaries and the commit
order. With a single group, one commit.

**Done when:** every group has a place in the commit order, none merged.

### Step 4: Draft the message(s)

Subject: `type(scope): short summary`. Body when the *why* is not obvious from the diff:
**bullets**, formatted per the commit policy.

Ask a concise clarifying question when type, scope, or a split boundary is genuinely
ambiguous.

**Done when:** each commit candidate has a message that satisfies the policy file.

### Step 5: Run quality checks

Detect the package manager from the `packageManager` field in `package.json`, falling back to
the lockfile (`pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lock*` → bun,
`package-lock.json` → npm). Then run only the scripts that exist in `package.json`:
`lint`, `typecheck`, `format`, `test`, `build`.

Report each script as passed, failed, or absent. On any failure, ask whether to proceed.

**Done when:** each of the five scripts is reported as passed, failed, or absent.

### Step 6: Commit and verify

For each group in order: leave only that group's files staged, `git commit`, then verify with
`git log -1 --oneline` and `git show --stat HEAD`.

**Done when:** every group has a verified commit.

## Guardrails

- Keep secrets out of commits — `.env*`, credential files, token files.
- Treat destructive git commands and `--amend` as opt-in: run them only when asked.

## Examples

[examples.md](examples.md) walks a mixed-concern split and a single-concern commit end to end.
Read it when a split boundary or a draft message is hard to pin down.
