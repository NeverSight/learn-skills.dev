---
name: fix-review
description: Automatically address CodeRabbit review comments on the current PR. Fetches inline comments from coderabbitai[bot], classifies them by severity (bug/style/suggestion), applies fixes for actionable issues, verifies locally, and pushes. Use when CodeRabbit posts review comments.
---

# Fix CodeRabbit Review Comments

This skill automatically addresses CodeRabbit review comments by fetching inline comments, classifying their severity, applying targeted fixes, and pushing the result.

## Usage

```
/fix-review           # Auto-fix actionable CodeRabbit comments
/fix-review --dry-run # Show what would be fixed without applying
/fix-review --all     # Also attempt to fix suggestions (not just bugs/style)
```

## Workflow

### Step 1: Fetch PR and Review Data

Get the current PR details:

```bash
gh pr view --json number,url,headRefName
```

If no PR exists, report "No PR found for the current branch." and stop.

Get the repo identifier:

```bash
gh repo view --json nameWithOwner -q '.nameWithOwner'
```

### Step 2: Fetch CodeRabbit Reviews and Comments

Fetch all reviews from CodeRabbit:

```bash
gh api "repos/<owner>/<repo>/pulls/<pr_number>/reviews" \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]")]'
```

Fetch inline comments:

```bash
gh api "repos/<owner>/<repo>/pulls/<pr_number>/comments" \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | {id, path, line, original_line, diff_hunk, body, created_at}]'
```

If no CodeRabbit reviews or comments exist, report "No CodeRabbit review comments found on this PR." and stop.

### Step 3: Classify Comments

For each inline comment, classify it into one of three categories based on the comment body.

**Priority rule**: If a comment contains a ````suggestion` code block, it is always auto-fixable regardless of category — apply the suggestion directly. Classification then only affects reporting priority.

**Bug/Security** (auto-fix):
- CodeRabbit header markers: `⚠️ Potential issue`, `🐛 Bug`, `🔒 Security`
- Keywords in body (case-insensitive): `bug`, `error`, `security`, `vulnerability`, `incorrect`, `wrong`, `crash`, `leak`, `null`, `undefined`, `race condition`, `injection`, `xss`, `overflow`, `missing check`, `unhandled`, `exception`, `type error`, `not defined`
- Pattern: comment describes *what is broken*, not what could be improved
- Edge case: if body contains both a bug keyword AND `consider`/`might want to`, classify as Bug (err on side of safety)

**Style** (auto-fix):
- CodeRabbit header markers: `🧹 Nitpick`, `📝 Style`
- Keywords in body: `style`, `format`, `naming`, `convention`, `readability`, `import`, `unused`, `lint`, `whitespace`, `indentation`, `nit:`, `nit `, `typo`, `spelling`, `consistent`, `redundant`
- Delegation: if the issue is about Python formatting/linting (import order, unused imports, line length), delegate to `ruff check --fix` and `ruff format` rather than manual editing
- Edge case: `nit:` prefix always means Style regardless of other keywords

**Suggestion** (report only, unless `--all` flag):
- CodeRabbit header markers: `🛠️ Refactor suggestion`, `💡 Suggestion`, `📖 Note`
- Keywords in body: `consider`, `might want to`, `could be`, `alternative`, `refactor`, `performance`, `optimization`, `simplify`, `extract`, `pattern`, `architecture`
- Default: any comment that does not match Bug/Security or Style patterns falls here
- Edge case: `suggest` alone is NOT a Style keyword — it goes to Suggestion unless a `suggestion` code block is present (which makes it auto-fixable)

### Step 4: Apply Fixes

For each actionable comment (Bug/Security and Style categories):

1. Read the file at the specified path
2. Navigate to the specified line number
3. Analyze the comment body for:
   - **Code suggestion blocks** (````suggestion` markers in the comment): Apply the suggested code directly
   - **Descriptive feedback**: Understand the issue and implement an appropriate fix
4. Apply the fix to the file

For Style issues that ruff can handle:

```bash
ruff check --fix synapse/ tests/
ruff format synapse/ tests/
```

If `--dry-run` flag is provided: show each comment with its classification and proposed fix, but do NOT modify files, commit, or push.

### Step 5: Local Verification

After applying all fixes:

```bash
ruff check synapse/ tests/
```

```bash
ruff format synapse/ tests/ --check
```

```bash
pytest
```

If any check fails after fixing:
- Attempt one targeted correction
- If it still fails, revert the problematic fix and report it as unresolvable

### Step 6: Commit and Push

Stage and commit the changes:

```bash
git add -u
```

```bash
git commit -m "fix: address CodeRabbit review comments

Resolved:
- <summary of each fixed comment>

Reported (not auto-fixed):
- <summary of suggestion-only comments>"
```

```bash
git push
```

### Step 7: Report Summary

Report what was done:
- Number of comments addressed (by category)
- Files modified
- Comments left as suggestions (not auto-fixed)
- Whether all local checks pass
- Link to the PR for manual review of remaining suggestions

### Error Handling

- **No PR found**: Report and stop
- **No CodeRabbit comments**: Report and stop
- **gh API errors**: Report the error and suggest manual review
- **Fix causes test failure**: Revert that specific fix, report the issue
- **Never force-push**: Always use `git push`
- **Max 1 fix cycle**: One pass of fixes. If issues remain, report for manual handling

## Safety

- Only fixes Bug/Security and Style categories by default
- Suggestions are reported but not auto-fixed (unless `--all`)
- Local verification before pushing
- One retry per failed fix, then revert
- CodeRabbit's `profile: "chill"` means suggestions are advisory, not blocking
