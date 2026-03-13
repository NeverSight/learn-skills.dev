---
name: commit-changes
description: >
  Stage, commit, and amend changes with conventional commit messages.
  Covers reviewing changes, selective staging, writing descriptive
  commit messages using HEREDOC format, and verifying commit history. Use
  when saving a logical unit of work to version control, creating a commit
  with a conventional message, amending the most recent commit, or
  reviewing staged changes before committing.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: git
  complexity: basic
  language: multi
  tags: git, commit, staging, conventional-commits, version-control
---

# Commit Changes

Stage files selectively, write clear commit messages, and verify commit history.

## When to Use

- Saving a logical unit of work to version control
- Creating a commit with a descriptive, conventional message
- Amending the most recent commit (message or content)
- Reviewing what will be committed before committing

## Inputs

- **Required**: One or more changed files to commit
- **Optional**: Commit message (will be drafted if not provided)
- **Optional**: Whether to amend the previous commit
- **Optional**: Co-author attribution

## Procedure

### Step 1: Review Current Changes

Check working tree status and inspect diffs:

```bash
# See which files are modified, staged, or untracked
git status

# See unstaged changes
git diff

# See staged changes
git diff --staged
```

**Expected:** Clear picture of all modified, staged, and untracked files.

**On failure:** If `git status` fails, verify you are inside a git repository (`git rev-parse --is-inside-work-tree`).

### Step 2: Stage Files Selectively

Stage specific files rather than using `git add .` or `git add -A` to avoid accidentally including sensitive files or unrelated changes:

```bash
# Stage specific files by name
git add src/feature.R tests/test-feature.R

# Stage all changes in a specific directory
git add src/

# Stage parts of a file interactively (not supported in non-interactive contexts)
# git add -p filename
```

Review what is staged before committing:

```bash
git diff --staged
```

**Expected:** Only the intended files and changes are staged. No `.env`, credentials, or large binaries.

**On failure:** Unstage accidentally added files with `git reset HEAD <file>`. If sensitive data was staged, unstage immediately before committing.

### Step 3: Write a Commit Message

Use conventional commits format. Always pass the message via HEREDOC for proper formatting:

```bash
git commit -m "$(cat <<'EOF'
feat: add weighted mean calculation

Implements weighted_mean() with support for NA handling and
zero-weight filtering. Includes input validation for mismatched
vector lengths.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

Conventional commit types:

| Type | When to use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Adding or updating tests |
| `refactor` | Code change that neither fixes nor adds |
| `chore` | Build, CI, dependency updates |
| `style` | Formatting, whitespace (no logic change) |

**Expected:** Commit created with a descriptive message that explains *why*, not just *what*.

**On failure:** If a pre-commit hook fails, fix the issue, re-stage with `git add`, and create a **new** commit (do not use `--amend` since the failed commit was never created).

### Step 4: Amend the Last Commit (Optional)

Only amend if the commit has **not** been pushed to a shared remote:

```bash
# Amend message only
git commit --amend -m "$(cat <<'EOF'
fix: correct weighted mean edge case for empty vectors

EOF
)"

# Amend with additional staged changes
git add forgotten-file.R
git commit --amend --no-edit
```

**Expected:** The previous commit is updated in-place. `git log -1` shows the amended content.

**On failure:** If the commit was already pushed, do not amend. Create a new commit instead. Force-pushing amended commits to shared branches causes history divergence.

### Step 5: Verify the Commit

```bash
# View the last commit
git log -1 --stat

# View recent commit history
git log --oneline -5

# Verify the commit content
git show HEAD
```

**Expected:** The commit appears in history with the correct message, author, and file changes.

**On failure:** If the commit contains wrong files, use `git reset --soft HEAD~1` to undo the commit while keeping changes staged, then re-commit correctly.

## Validation

- [ ] Only intended files are included in the commit
- [ ] No sensitive data (tokens, passwords, `.env` files) committed
- [ ] Commit message follows conventional commits format
- [ ] Message body explains *why* the change was made
- [ ] `git log` shows the commit with correct metadata
- [ ] Pre-commit hooks (if any) passed

## Common Pitfalls

- **Committing too much at once**: Each commit should represent one logical change. Split unrelated changes into separate commits.
- **Using `git add .` blindly**: Always review `git status` first. Prefer staging specific files by name.
- **Amending pushed commits**: Never amend commits that have been pushed to a shared branch. This rewrites history and causes problems for collaborators.
- **Vague commit messages**: "fix bug" or "update" tells nothing. Describe what changed and why.
- **Forgetting `--no-edit` on content amends**: When adding forgotten files to the last commit, use `--no-edit` to keep the existing message.
- **Hook failure leading to `--amend`**: When a pre-commit hook fails, the commit was never created. Using `--amend` would modify the *previous* commit. Always create a new commit after fixing hook issues.

## Related Skills

- `manage-git-branches` - branch workflow before committing
- `create-pull-request` - next step after committing
- `resolve-git-conflicts` - handling conflicts during merge/rebase
- `configure-git-repository` - repository setup and conventions
