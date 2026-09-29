---
name: yueban-git-commit
description: 'Perform a git commit following Conventional Commits, with commit message analysis, smart staging, and message generation. Use when the user asks to commit code, create a commit, or mentions "/commit". Supports: (1) auto-detecting type and scope from the diff, (2) generating a conventional commit message from the diff, (3) interactive commits (overriding type/scope/description), (4) smart staging by logical grouping, (5) pushing to the remote after commit, once confirmed (skip asking only if the user''s request already implied pushing).'
allowed-tools: Bash
---

# Git Commit with Conventional Commits

## Overview

Create standardized, semantic git commits based on Conventional Commits. Determine the appropriate type, scope, and message by analyzing the actual diff.

## Commit format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Commit language convention

1. Write `description` and `body` in English by default, unless the user explicitly asks for Chinese.
2. Keep `type`, `scope`, and convention keywords (e.g. `BREAKING CHANGE`, `Refs`, `Closes`) in their standard English form.
3. Leave proper nouns, code identifiers, paths, and commands as-is — do not force-translate them.

## Commit types

| Type       | Purpose                          |
| ---------- | --------------------------------- |
| `feat`     | New feature                       |
| `fix`      | Bug fix                           |
| `docs`     | Documentation only                |
| `style`    | Formatting/style change (no logic change) |
| `refactor` | Refactor (not a new feature, not a fix) |
| `perf`     | Performance improvement           |
| `test`     | Add/update tests                  |
| `build`    | Build system/dependency changes   |
| `ci`       | CI/config changes                 |
| `chore`    | Maintenance/misc changes          |
| `revert`   | Revert a commit                   |

## Breaking changes

```
# Add an exclamation mark after type/scope
feat!: remove deprecated endpoint

# Use a BREAKING CHANGE footer
feat: support config inheritance from other configs

BREAKING CHANGE: `extends` field behavior has changed
```

## Workflow

### 1. Analyze the diff

```bash
# If files are already staged, check the staged diff
git diff --staged

# If nothing is staged, check the working tree diff
git diff

# Also check status — a submodule with ANY changes (committed-but-unpushed
# inside it, or still-uncommitted working tree changes) shows up here as
# e.g. " M <submodule-path>", regardless of which case it is
git status --porcelain

# If this repo tracks submodules (.gitmodules exists) and status shows one as
# modified, check further — `+` here means the submodule already has commits
# ahead of the parent's recorded pointer, but a submodule can also have
# uncommitted working-tree changes with NO `+` shown (git submodule status
# only compares HEAD to the recorded SHA, it does not report dirty working trees)
if [ -f .gitmodules ]; then
  git submodule status
fi
```

If `git status --porcelain` lists a submodule path as modified, **stop here and resolve it via the "Handling submodules" section below before continuing to step 2** — don't rely on the `+` prefix alone to decide whether it's safe to proceed, since a submodule with uncommitted (not yet committed inside it) changes shows no `+` at all. Run `git -C <submodule-path> status --porcelain` to see whether the submodule's own working tree is dirty (case 1: needs a commit + push inside the submodule first) or clean (case 2: already committed, just confirm it's pushed before bumping the pointer).

### 2. Stage files (if needed)

When nothing is staged yet, or you want to reorganize the change groupings, first decide how many commits this should be — don't jump straight to staging everything as one group:

- Read the full unstaged diff (`git diff`) and list every changed file with a one-line summary of what changed in it.
- Group files by *why* they changed, not by directory or file type: two files touched for the same reason (implementing one feature, fixing one bug, one refactor) are one group, even if they live in unrelated directories. Two files that happen to sit next to each other but serve unrelated changes (e.g. an unrelated typo fix picked up along the way) are separate groups.
- A file that mixes multiple unrelated hunks needs a **partial stage** (`git add -p path/to/file`, or `git diff` + `Edit` + manual `git apply --cached` for precise hunk selection) — don't force a mixed file into a single group just because splitting it is more work.
- If every changed file genuinely serves one purpose, one group (and one commit) is correct — don't manufacture multiple commits from a single logical change just to seem thorough.
- When the grouping is ambiguous (e.g. it's unclear whether two changes are "the same reason" or coincidentally adjacent), ask the user rather than guessing — a wrong split/merge is harder to undo than a short question.

```bash
# Stage specific files
git add path/to/file1 path/to/file2

# Stage by pattern
git add *.test.*
git add src/components/*

# Stage part of a file (interactively pick hunks) — for files that mix
# multiple logical groups
git add -p path/to/mixed-file

# Stage all tracked/untracked changes at once — only once you've confirmed
# every changed file genuinely belongs to the same logical group
git add -A
```

For a multi-group diff, repeat step 2 → step 3 → step 4 once per group (stage that group only, commit it, then move to the next group) rather than staging everything up front.

**Never commit sensitive information** (e.g. `.env`, `credentials.json`, private keys).

### 3. Generate the commit message

Analyze the diff and determine:

- **Type**: What category of change is this?
- **Scope**: Which module/area is affected?
- **Description**: A one-line description of the change (present tense, imperative mood, < 72 chars)

### 4. Perform the commit

```bash
# Confirm the staging area isn't empty before committing
if git diff --cached --quiet; then
  echo "Nothing staged — run git add first"
  exit 1
fi

# Single-line commit message
git commit -m "<type>[scope]: <description>"

# Multi-line commit message (with body/footer)
git commit -m "$(cat <<'EOF'
<type>[scope]: <description>

<optional body>

<optional footer>
EOF
)"
```

### 5. Push to the remote

Pushing is a side-effecting action visible to others — confirm with the user before doing it, the same way `yueban-git-safe-sync`/`yueban-git-feature-branch-flow` require confirmation before their own push steps. Skip asking only when the user's own request already implied it (e.g. "commit and push this", "commit, then push to origin"). After the commit succeeds (and, unless already implied, after the user confirms), push:

```bash
git push
# If there's no upstream, use: git push -u origin HEAD
```

## Handling submodules

If the repository tracks git submodules (see `.gitmodules`), they can show up in the parent repo's `git status`/`git diff` in two different ways — always tell them apart before staging:

1. **The submodule itself has uncommitted changes (dirty submodule)** — `git status` in the parent reports it as "modified content" or "untracked content" (or just `M <path>` in `--porcelain` output). Check with `git -C <submodule-path> status --porcelain`: any output means the submodule's own working tree has changes that were never committed inside the submodule. Note that `git submodule status` will **not** show a `+` prefix for this case — `+` only appears once the submodule has already committed ahead of the parent's recorded pointer, not while it's merely dirty.
   - Do not `git add <submodule-path>` directly in the parent repo — this silently rewinds the pointer to the submodule's previous commit, making the change appear to disappear while it actually still sits, uncommitted, inside the submodule.
   - `cd` into the submodule first and commit (and push) there, following the same Conventional Commits workflow, within the submodule's own history/conventions.
   - Only after the submodule's commit has been pushed to its own remote should you go back to the parent repo and stage the pointer change.

2. **Only the pointer moved (submodule HEAD changed, working tree clean)** — `git -C <submodule-path> status --porcelain` is empty, but `git submodule status` shows a `+` prefix: someone already committed and pushed inside the submodule (or it was updated via `git submodule update --remote`), and the parent repo just needs to record the new commit SHA.
   - Confirm the submodule's new commit has actually been pushed to its own remote (`git -C <submodule-path> status` shows "up to date"/no unpushed commits) — never point the pointer at a SHA that doesn't exist on the submodule's remote, or others will fail to fetch it after cloning.
   - Use `git diff --submodule=log -- <submodule-path>` (or a plain `git diff` if `diff.submodule=log` isn't configured) to see which commits are involved, and mention them in the commit body if the range is non-trivial.
   - Stage and commit the pointer bump as its own logical change, separate from unrelated file changes: `git add <submodule-path>`.
   - Use a message like `chore: bump <name> submodule` for a single submodule, or `chore: bump <name1>/<name2> submodules` when bumping several at once; add a short parenthetical reason if useful. If the pointer bump is incidental to a larger docs/feature change, it's fine to fold it into that commit's message instead of forcing a separate commit — follow whatever pattern the repo's history already uses.

When a submodule is in the "dirty" state from case 1, avoid `git add -A`/`git add .` — that would stage the pointer while the underlying commit doesn't exist anywhere durable. Stage the submodule path explicitly instead.

## Best practices

- Each commit should contain exactly one logical change
- Write in English by default: `add log aggregation script`, not a mixed-language description
- Use present tense, imperative mood: `fix parsing crash`, not `fixed parsing crash`
- Link issues: `Closes #123`, `Refs #456`
- Keep the description under 72 characters

## Git safety protocol

- Never modify git global/local config
- Never run destructive commands (e.g. `--force`, hard reset) without explicit request
- Never skip hooks (`--no-verify`) unless the user asks for it
- Never force-push to the repo's base/protected branch (whatever this repo's default branch actually is — check `git symbolic-ref refs/remotes/origin/HEAD` — not just the literal names `master`/`develop`)
- If a commit fails due to hooks, fix the issue first and create a new commit (don't amend)
