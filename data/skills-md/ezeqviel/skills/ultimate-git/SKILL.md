---
name: ultimate-git
description: 'GitHub & Git operations specialist with opinionated workflows. Use when the user asks to create, review, or merge PRs, manage branches, create releases or tags, work with issues, configure GitHub Actions, manage repo settings, scaffold new repositories, or perform any gh CLI operation. Triggers on requests involving pull requests, branch strategy, releases, GitHub workflows, repo configuration, or conventional commits.'
---

# Ultimate Git

Opinionated Git & GitHub workflow skill built on the `gh` CLI. Provides branch strategy, PR conventions, repo scaffolding, and CI setup.

## Operating Rules

1. **Confirm repo context** before any operation: `gh repo view --json nameWithOwner -q .nameWithOwner`
2. **JSON output**: Use `--json` fields for programmatic output
3. **Heredoc for bodies**: Always use heredoc for PR/issue bodies to preserve formatting
4. **Non-destructive**: Never force-push to main/develop. Confirm before any destructive operation
5. **Pull before branching**: Never create a branch without pulling latest from parent first
6. **Conventional Commits**: All commits and PR titles follow the spec. See [references/conventional-commits.md](references/conventional-commits.md) for the full type table and examples

## Branch Strategy

```
main         ← releases + tags (protected, PR only)
  develop    ← stable dev (protected, PR only)
    feat/*   ← features (from develop, PR to develop)
    fix/*    ← bugfixes (from develop, PR to develop)
    hotfix/* ← urgent (from main, PR to main + develop)
```

## Workflows

### New Feature

```bash
git checkout develop && git pull origin develop
git checkout -b feat/feature-name
# ... work + commit using Conventional Commits ...
git push -u origin feat/feature-name
gh pr create --base develop --title "feat(scope): description" --body "$(cat <<'EOF'
## What changed
- Bullet list of concrete changes

## Why
- Business/technical reason

## Impact
- What works differently now
EOF
)"
```

#### Merging a PR (MANDATORY — use AskUserQuestion)

Before merging, check the target branch and review commit history with `git log --oneline BASE..HEAD`. Then use `AskUserQuestion` to let the user choose the merge strategy.

Recommendation logic (first option = recommended):

- **PR to main** (release/hotfix): always recommend `--merge` (preserves full history of what went into the release)
- **PR to develop with clean commits** (each commit is a logical unit with a good message): recommend `--merge`
- **PR to develop with messy commits** (WIP, fix typo, wip again, etc.): recommend `--squash`

```
header: "Merge strategy"
question: "How to merge PR #NUM? (X commits: [summarize commit quality])"
options:
- { label: "[Recommended]", description: "..." }
- { label: "[Other option]", description: "..." }
```

Then run: `gh pr merge PR_NUM --[strategy] --delete-branch`

### Release

```bash
git checkout main && git pull origin main
git merge develop
git push origin main
gh release create vX.Y.Z --target main --generate-notes --title "vX.Y.Z"
```

### Hotfix

```bash
git checkout main && git pull origin main
git checkout -b hotfix/fix-name
# ... fix + commit ...
git push -u origin hotfix/fix-name
gh pr create --base main --title "fix: hotfix description" --body "$(cat <<'EOF'
## What changed
- Description of the fix

## Why
- Urgency / impact of the bug

## Impact
- What this resolves
EOF
)"
# After merge to main, also merge main back to develop
```

## Repo Init Workflow

1. **Ask**: Language? Test command? Install command?
2. **Init**: `git init && git checkout -b main && git checkout -b develop`
3. **Generate**: `.gitignore` (language-appropriate) + `.github/workflows/ci.yml` (see [references/ci-templates.md](references/ci-templates.md))
4. **Commit**: `git add -A && git commit -m "chore: initial project scaffold"`
5. **Remote**: `gh repo create NAME --source=. --push --public`
6. **Default branch**: `gh api repos/{owner}/{repo} --method PATCH -f default_branch=develop`
7. **Protection**: Apply rules for main and develop (see [references/branch-protection.md](references/branch-protection.md))

## Error Resolution

| Error                   | First Action                                                 |
| ----------------------- | ------------------------------------------------------------ |
| `403 Forbidden`         | Check token scopes: `gh auth status`                         |
| `Merge conflicts`       | Resolve locally: `git pull origin BASE && git merge --no-ff` |
| `Status checks failing` | `gh pr checks PR_NUM` — wait or investigate CI               |
| `Branch protected`      | Create PR instead of direct push                             |
| `Not found`             | Verify repo: `gh repo view` and branch exists                |

Diagnose systematically: auth → repo context → branch state → permissions.
