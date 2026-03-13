---
name: cp
description: Commit and push in one step. Use when user says "/cp", "commit and push", "커밋하고 푸시", "커밋 푸시", or wants to stage, commit, and push changes in a single action. Optionally accepts a commit message as argument.
user-invocable: true
---

# Commit & Push Skill

Streamlined git workflow: stage, commit, and push in one command.

## Usage

### Basic

```bash
/cp                        # Auto-generate commit message
/cp "fix: resolve bug"     # Use provided message
```

### Korean Triggers

- "커밋하고 푸시"
- "커밋 푸시"
- "변경사항 올려줘"

## Workflow

### 1. Analyze Changes

```bash
git status                 # See all changes
git diff --staged          # Staged changes
git diff                   # Unstaged changes
git log -3 --oneline       # Recent commits for context
```

### 2. Generate Commit Message

If no message provided, analyze changes and generate following Conventional Commits:

| Prefix | Use Case |
|--------|----------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation |
| `refactor:` | Code restructuring |
| `style:` | Formatting (no logic change) |
| `test:` | Adding tests |
| `chore:` | Maintenance tasks |

### 3. Stage Files

Prefer specific files over `git add -A`:

```bash
git add src/component.tsx src/utils.ts
```

**Never stage:**
- `.env` files
- Credentials or secrets
- Large binary files (unless intentional)

### 4. Commit

Use HEREDOC for proper formatting:

```bash
git commit -m "$(cat <<'EOF'
type: concise description

Optional body with more details.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### 5. Push

```bash
git push origin <current-branch>
```

If upstream not set:

```bash
git push -u origin <current-branch>
```

## Safety Checks

Before committing:

1. **No secrets**: Scan for API keys, passwords, tokens
2. **Correct branch**: Verify not pushing to protected branch accidentally
3. **Clean diff**: Review what's being committed

## Error Handling

| Error | Solution |
|-------|----------|
| "Nothing to commit" | No changes detected, inform user |
| "Push rejected" | Run `git pull` first, then retry |
| "Pre-commit hook failed" | Fix issues, stage again, create NEW commit |
