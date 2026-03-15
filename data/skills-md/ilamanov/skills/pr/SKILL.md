---
name: pr
description: Commit changes and create or update a pull request following project standards. Use when the user wants to commit work, create a PR, update an existing PR, or use the /pr command.
argument-hint: [description]
allowed-tools: Bash(git:*), Bash(gh:*)
---

# PR Workflow

## Context

- User's notes: $ARGUMENTS
- Current branch: !`git branch --show-current`
- Git status: !`git status --short`
- Existing PR: !`gh pr view --json number,title,url 2>/dev/null || echo "No PR exists"`
- Recent commits: !`git log main..HEAD --oneline 2>/dev/null || git log -3 --oneline`

## Step 0: Handle merged PR branches

If **not** on `main` and a PR already exists for the current branch, check if it has been merged:

```bash
gh pr view --json state --jq '.state'
```

If the state is `MERGED`:

1. Stash any uncommitted changes: `git stash --include-untracked` (skip if working tree is clean)
2. Switch to main: `git checkout main`
3. Pull latest: `git pull`
4. Create a new branch with a descriptive name based on the user's notes or the staged changes
5. Pop the stash if one was created: `git stash pop`
6. Continue to Step 1 on the new branch

## Step 1: Prepare the branch

1. If on main, create a new branch with a descriptive name
2. Commit all changes (except API keys or explicitly private content)
3. Push changes to the remote

## Step 2: Create or update the PR

**If no PR exists:** Create a new PR following the standards below.

**If a PR already exists:**

1. Read the existing PR:

   ```bash
   gh pr view --json title,body,labels,number
   gh pr diff --stat
   ```

   Read specific files directly rather than dumping the full diff.

2. Review whether the PR content accurately reflects the current diff:
   - Does the title follow semantic format?
   - Does the description accurately describe all commits?
   - Is the test plan still accurate?
   - Are the release notes complete?

3. Update if needed:

   ```bash
   gh pr edit <number> --title "new title" --body "new body"
   ```

4. Push any new commits (regular push, not force push)

## Step 3: Link related issues

Search for related issues and link them using `Closes #123` or `Relates to #123`.

## Handling problems

Committing automatically runs the linter. Fix any lint/type errors unless they require meaningful code changes—in that case, notify the user:

> I can't create/update this PR because [reason]. Would you like me to [suggestion]?

Never force commit or force push.

---

# PR Standards

## Title format

Use semantic PR titles (Conventional Commits):

```
<type>(<scope>): <description>
```

### Types

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `refactor` - Code change that neither fixes a bug nor adds a feature
- `perf` - Performance improvement
- `test` - Adding or fixing tests
- `chore` - Maintenance tasks

### Scope (optional)

A noun describing the affected area: `fix(editor):`, `feat(sync):`, `docs(examples):`

### Examples

- `feat(editor): add snap threshold configuration option`
- `fix(arrows): correct binding behavior with rotated shapes`
- `docs: update sync documentation`

## Body template

```md
<description paragraph>

### Change type

- [x] `bugfix` | `improvement` | `feature` | `api` | `other`

### Test plan

1. Step to test...

- [ ] Unit tests
- [ ] End to end tests

### Release notes

- Brief description of changes for users
```

### Description paragraph

Start with: "In order to X, this PR does Y."

- Keep it specific—avoid vague phrases like "improve user experience"
- Link related issues in the first paragraph
- Don't expect readers to also read the linked issue

### Change type

- Tick exactly one type with `[x]`
- Delete unticked items

### Test plan

- List manual testing steps if applicable
- Remove the numbered list if changes cannot be manually tested
- Tick checkboxes for included test types

### Release notes

- Write brief notes describing user-facing changes
- Use imperative mood: "Add...", "Fix...", "Remove..."
- Omit entirely for internal work with no user-facing impact

## API changes section

Include when changes affect `api-report.md`:

```md
### API changes

- Added `Editor.newMethod()` for X
- Breaking! Removed `Editor.oldMethod()`
```

## Important

- Never include AI attribution ("Generated with Claude Code", "Co-Authored-By: Claude", etc.) in commits, PR titles, or descriptions
- Never use title case for descriptions—use sentence case
- Never put yourself as co-author of any commits
