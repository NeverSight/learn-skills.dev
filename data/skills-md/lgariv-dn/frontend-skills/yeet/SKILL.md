---
name: "yeet"
description: "Use only when the user explicitly asks to stage, commit, push, and open a GitHub pull request in one flow using the GitHub CLI (`gh`)."
---

## Prerequisites

- Require GitHub CLI `gh`. Check `gh --version`. If missing, ask the user to install `gh` and stop.
- Require authenticated `gh` session. Run `gh auth status`. If not authenticated, ask the user to run `gh auth login` (and re-run `gh auth status`) before continuing.

## Naming conventions

- Branch: `{github username without '-dn' suffix}/ar-{jira ticket number}/{description}` when starting from default branch (v26.1/v26.2 etc. usually based on `v{year}.{quarter}`).
- Commit: See **Commit Message Style** below.
- PR title: `AR-{jira ticket number}: {description}` summarizing the full diff.

## Commit Message Style

### Format
```
[type]: Subject line (capitalize first word)

- Bullet point without ending period
- Another bullet explaining a specific change
```

### Types
Use square brackets: `[feat]`, `[fix]`, `[refactor]`, `[chore]`, `[test]`

### Subject Line Rules
- **Always capitalize** the first word after the colon
- **Never include ticket references** in commit messages (save for PR description)

### When to Use Body vs Longer Subject

**Simple changes** (single focus, straightforward logic):
→ Use a slightly longer, descriptive subject. No body needed.
```
[fix]: Skip tasks fetch for standalone task instances in expanded row
[chore]: Code quality improvements & rule compliance (memo, casts, etc.)
```

**Complex changes** (significant logic, multiple decisions, refactoring):
→ Use terse subject + bullet body. Complexity is about significance of change, NOT file count.
```
[refactor]: Address PR review comments from Amram

- Replace IIFE pattern with inline computed values for filteredChildWorkflowLogs
- Extract clearSelections() helper to eliminate 5 duplicate occurrences
- Extract buildTaskInstanceViewerData utility to separate file, reducing ~80 lines
- Remove duplicate imports in workflow-instance-api-context.tsx
```

### Bullet Style
- Start with action verb (Add, Remove, Update, Fix, Replace, Extract) or past tense (Added, Removed...)
- **Never end bullets with a period**
- Each bullet should describe one specific change

### Co-authored-by
**Only add** `Co-authored-by: Cursor <cursoragent@cursor.com>` when the AI wrote most of the code. If user drove the implementation and AI only assisted minimally, omit it.

## Workflow

- If on default branch (v26.1/v26.2 etc. usually based on `v{current year}.{current quarter}`), create a branch: `git checkout -b "{github username without '-dn' suffix}/ar-{jira ticket number}/{description}"`
- Otherwise stay on the current branch.
- Confirm status, then stage everything: `git status -sb` then `git add -A`.
- Commit following the **Commit Message Style** section above. Use HEREDOC for multi-line commits:
  ```bash
  git commit -m "$(cat <<'EOF'
  [type]: Subject line
  
  - First bullet point
  - Second bullet point
  EOF
  )"
  ```
- Run checks if not already. If checks fail due to missing deps/tools, install dependencies and rerun once.
- Push with tracking: `git push -u origin $(git branch --show-current)`
- If git push fails due to workflow auth errors, pull from master and retry the push.
- Open a PR and edit title/body to reflect the description and the deltas: `GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --draft --fill --head $(git branch --show-current)`
- Write the PR description to a temp file with real newlines (e.g. pr-body.md ... EOF) and run pr-body.md to avoid \\n-escaped markdown.
- PR description (markdown) must be detailed prose covering the issue, the cause and effect on users, the root cause, the fix, and any tests or checks used to validate. Base it on [pr-desc command](.cursor/commands/pr-desc.md)
