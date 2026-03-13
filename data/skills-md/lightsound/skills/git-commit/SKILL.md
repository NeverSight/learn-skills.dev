---
name: git-commit
description: "Analyze diffs, split into logical commits, and create Conventional Commit messages. Use when the user asks to commit, stage changes, or split work into multiple commits."
allowed-tools: Bash
disable-model-invocation: true
---

# Git Commit

Create well-scoped, reviewable commits with Conventional Commit messages.

## Conventional Commit Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

| Type       | Purpose                        |
| ---------- | ------------------------------ |
| `feat`     | New feature                    |
| `fix`      | Bug fix                        |
| `docs`     | Documentation only             |
| `style`    | Formatting/style (no logic)    |
| `refactor` | Code refactor (no feature/fix) |
| `perf`     | Performance improvement        |
| `test`     | Add/update tests               |
| `build`    | Build system/dependencies      |
| `ci`       | CI/config changes              |
| `chore`    | Maintenance/misc               |
| `revert`   | Revert commit                  |

Breaking changes: `feat!: summary` or `BREAKING CHANGE:` footer.

## Workflow

### 1. Inspect working tree

```bash
git status
git diff --stat
git diff
```

### 2. Decide commit boundaries

Split when changes contain unrelated concerns:

- feature vs refactor
- backend vs frontend
- formatting vs logic
- tests vs production code
- dependency bumps vs behavior changes

Default to **multiple small commits** when in doubt.

### 3. Stage only what belongs in the next commit

```bash
git add path/to/file
git add -p            # patch staging for mixed changes in one file
git restore --staged -p  # unstage a hunk
```

### 4. Sanity check staged changes

```bash
git diff --cached
```

Verify:

- No secrets or tokens
- No debug logging (`console.log`, `debugger`, etc.)
- No unrelated formatting churn

### 5. Describe the commit in 1-2 sentences

Answer: "What changed?" + "Why?"

**If you cannot describe it cleanly, the commit is too big or mixed — go back to step 2.**

### 6. Write the commit message

```bash
git commit -m "$(cat <<'EOF'
<type>[scope]: <description>

<body: what/why>

<footer>
EOF
)"
```

- Description: imperative mood, present tense, <72 chars
- Body: what and why, not implementation diary
- Footer: `Closes #123`, `Refs #456`, `BREAKING CHANGE:` if needed

### 7. Verify

Run the repo's fastest meaningful check (lint, typecheck, or unit tests) before moving on.

### 8. Repeat

Go back to step 3 for the next commit. Continue until the working tree is clean or all intended changes are committed.

## Deliverable

For each commit, provide:

- The commit message
- A one-line summary (what/why)

## Safety Protocol

- NEVER update git config
- NEVER force push to main/master
- NEVER skip hooks (--no-verify) unless user explicitly asks
- NEVER run destructive commands (--force, hard reset) without explicit request
- If commit fails due to hooks, fix the issue and create a NEW commit (don't amend)
