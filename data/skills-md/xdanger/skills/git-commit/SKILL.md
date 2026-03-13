---
name: git-commit
description: Create atomic git commits with Conventional Commits and Gitmoji. Use when the user asks to commit changes, create a commit, or says "/commit". Review staged and unstaged diffs, split changes into logical groups, and write focused commit messages that follow repository-local conventions.
---

# Git Commit

Follow repo-local commit instructions first. If none exist, use:

```text
<Gitmoji> <type>(<scope>)[!]: <subject>

[optional body]

[optional footer(s)]
```

## Workflow

### 1. Inspect the worktree

Check both staged and unstaged changes before committing:

```bash
git status --porcelain
git diff --staged --stat
git diff --stat
git diff --staged -- <file>
git diff -- <file>
```

### 2. Plan atomic commit groups

Prefer the fewest commits that still keep concerns isolated.

- One logical change per commit
- Keep tests with the code they validate
- Keep lockfiles with the dependency change that produced them
- Separate behavioral changes from formatting, renames, docs, and other mechanical edits
- If one file mixes concerns, use `git add -p`

Quick check:

1. Can this commit be described without "and"?
2. Would reverting it undo only one intent?
3. Would `git bisect` or `git cherry-pick` still be clear?

### 3. Stage one group at a time

```bash
git add path/to/file1 path/to/file2
git add -p path/to/file
```

Avoid broad staging unless the entire worktree is one logical change. Never stage secrets.

### 4. Write the commit message

Choose the closest matching type and Gitmoji. Common pairs:

- `✨ feat` for user-facing additions
- `🐛 fix` for bug fixes
- `♻️ refactor` for internal restructuring without behavior change
- `✅ test` for test-only work
- `📝 docs` for documentation
- `🔧 chore` for maintenance, config, or repo upkeep

Message checklist:

- imperative, lowercase subject
- no trailing period
- keep the subject short, ideally within 50 characters
- add scope when it helps
- use `!` and a `BREAKING CHANGE:` footer for breaking changes
- add body bullets only when they improve reviewability
- add issue refs or `Co-Authored-By:` footers when applicable

Example:

```text
✨ feat(auth): add OAuth2 login flow

- :sparkles: implement `GoogleAuthProvider` with PKCE
- :lock: add CSRF token validation

Closes #42
```

### 5. Commit in a useful order

When multiple commits are needed, prefer:

1. preparatory refactors
2. infrastructure or config
3. feature or fix
4. docs or formatting

Each commit should leave the tree in a coherent state.

## Git Safety

- do not change git config
- do not use destructive commands unless explicitly requested
- do not bypass hooks unless explicitly requested
- if hooks fail, fix the issue and create a new commit instead of amending by default
