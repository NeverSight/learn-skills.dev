---
name: pr-checks
description: Run comprehensive PR checks including reviewing CodeRabbit comments, ensuring PR description quality, running pre-commit hooks, tests, and validation. Use on an existing PR to address review feedback.
---

# PR Checks Skill

This skill runs comprehensive PR checks to ensure code quality and address review feedback on an existing pull request.

## When to Use

Run this skill when:
- A PR has been created and CodeRabbit has posted review comments
- You want to address existing review feedback systematically
- Before requesting final review/merge on a PR

## Usage

```
/pr-checks
```

## Workflow

### 1. Analyze Current State

First, understand what's being reviewed:

```bash
# Check current branch and status
git branch --show-current
git status --short

# Show diff summary vs main
git diff --stat main...HEAD

# Get the PR number for this branch
gh pr view --json number,title,state
```

### 2. Review and Fix PR Description

Ensure the PR has a proper description before addressing code comments:

```bash
# View current PR description
gh pr view --json body,title
```

**A good PR description should include:**
- **Summary**: 1-3 bullet points explaining what the PR does
- **Test plan**: How to verify the changes work
- **Related issues**: Links to Linear/GitHub issues (e.g., `Closes MAS-XXX`)

**If the description is missing or inadequate:**

```bash
# Update the PR description
gh pr edit --body "$(cat <<'EOF'
## Summary
<1-2 sentence overview of what this PR accomplishes>

### Changes
- <change 1: what was added/modified/removed>
- <change 2>
- <change 3>
- ...

### Technical details (if applicable)
<Brief explanation of implementation approach, architectural decisions, or non-obvious changes>

## Test plan
- [ ] <verification step 1>
- [ ] <verification step 2>
- [ ] <edge case or error scenario tested>

## Related issues
Closes MAS-XXX

## Screenshots/recordings (if applicable)
<Add screenshots for UI changes, terminal output for CLI changes>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Fix the title if needed** (should follow conventional commits format):

```bash
# Update PR title
gh pr edit --title "feat: descriptive title here"
```

### 3. Review Existing CodeRabbit Comments

**This is the primary workflow.** CodeRabbit automatically reviews PRs and posts comments. Use `/pr-comments` to fetch and process them:

```
/pr-comments
```

This fetches all review comments from the PR. For each CodeRabbit comment:

1. **Read the comment** - Understand what CodeRabbit is suggesting
2. **Evaluate relevance** - Is this a valid concern for this codebase?
3. **Decide action** - One of:
   - ✅ **Implement** - The suggestion is valid and worth fixing
   - ❌ **Skip** - The suggestion doesn't apply or is too minor
   - ❓ **Clarify** - Need more context from user before deciding

**Walk through comments one by one with the user:**

```
## CodeRabbit Comment #1 of 5

**File:** `massgen/backend/foo.py:45`

**Original code:**
```python
response = client.api_call(params)
return response.data
```

**CodeRabbit suggestion:**
> Consider adding error handling for the API call. The request could fail
> due to network issues or API errors, which would cause an unhandled
> exception. This is especially important since this is called from the
> main orchestration loop where failures could crash the entire run.
> [truncated - 8 more lines]

**Suggested change:**
```python
try:
    response = client.api_call(params)
    return response.data
except APIError as e:
    logger.error(f"API call failed: {e}")
    raise
```

**My assessment:** Valid concern - the API call could fail and there's no error handling.

**Recommendation:** ✅ Implement

Do you want me to:
1. Implement this fix
2. Skip this comment
3. Need more information
```

**After user decides, resolve the comment on GitHub:**

```bash
# If implemented or intentionally skipped, resolve the comment thread
gh api graphql -f query='
  mutation {
    resolveReviewThread(input: {threadId: "THREAD_ID"}) {
      thread { isResolved }
    }
  }
'
```

Alternatively, reply to the comment explaining the action taken:

```bash
# Reply to the comment
gh pr comment <PR_NUMBER> --body "Addressed in <commit-sha>: <brief description of fix>"
```

When showing comments:
- Show the **original code** being discussed
- Show the **full suggestion text** (truncate if >15 lines with "[truncated - N more lines]")
- Show the **suggested change** if CodeRabbit provided one
- Include **line numbers** for context

Wait for user approval before implementing each fix. This ensures:
- User maintains control over what changes are made
- No unnecessary changes are introduced
- Context-specific decisions can be made

### 4. Run Pre-commit Hooks

After making fixes, run pre-commit to ensure code style:

```bash
uv run pre-commit run --all-files
```

If issues are found, fix them and commit.

### 5. Run Tests

```bash
# Run tests (skip expensive API tests)
uv run pytest massgen/tests/ -v -m "not expensive and not docker" -x --tb=short
```

### 6. Validate Configs (if modified)

```bash
uv run python scripts/validate_all_configs.py
```

### 7. Commit and Push Fixes

```bash
# Stage fixes
git add -u .

# Commit with descriptive message
git commit -m "fix: address CodeRabbit review comments

- Fix error handling in foo.py
- Add missing type hints in bar.py

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to trigger CodeRabbit re-review
git push
```

### 8. Run PR Review Toolkit (Optional)

For additional analysis beyond CodeRabbit:

```
/pr-review-toolkit:review-pr
```

This runs specialized agents for:
- Code review against project guidelines
- Silent failure detection
- Type design analysis
- Test coverage analysis

### 9. (Optional) Run Local CodeRabbit Review

If you want to run a fresh local review (separate from GitHub PR comments):

```bash
coderabbit --prompt-only --type committed
```

**Note:** This runs CodeRabbit's own analysis locally, which may differ from the automated PR review. The GitHub PR comments from step 3 are typically more thorough since they have full PR context.

### 10. Generate Summary

After all checks, output a summary:

```
## PR Checks Summary

### Branch: feature/my-feature
- PR #123: "feat: add new feature"
- Commits ahead of main: 3
- Files changed: 5

### PR Description
✅ Has summary, test plan, and issue links

### CodeRabbit Comments Addressed

| Comment | File | Action |
|---------|------|--------|
| Add error handling | foo.py:45 | ✅ Implemented |
| Consider caching | bar.py:12 | ❌ Skipped (not applicable) |
| Missing type hint | baz.py:78 | ✅ Implemented |

### Check Results

| Check | Status |
|-------|--------|
| Pre-commit | ✅ Passed |
| Tests | ✅ 47 passed |
| Config Validation | ✅ Valid |

### Ready for Merge?
✅ All critical issues addressed, ready for final review
```

## Reference

### PR Description Template

```markdown
## Summary
<1-2 sentence overview of what this PR accomplishes>

### Changes
- <change 1: what was added/modified/removed>
- <change 2>
- <change 3>

### Technical details (if applicable)
<Implementation approach, architectural decisions, or non-obvious changes>

## Test plan
- [ ] Step to verify functionality
- [ ] Edge cases tested
- [ ] Error scenarios handled

## Related issues
Closes MAS-XXX

## Screenshots/recordings (if applicable)
<For UI/CLI changes>

## Breaking changes (if applicable)
<What breaks and migration steps>
```

### PR Title Format

Use conventional commits format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `refactor:` - Code change that neither fixes a bug nor adds a feature
- `perf:` - Performance improvement
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### Pre-commit Hooks
- **black** - Python formatter (200 char line)
- **isort** - Import sorter
- **flake8** - Style checker
- **autoflake** - Remove unused imports

### Test Markers
- `@pytest.mark.expensive` - Skip in quick checks
- `@pytest.mark.docker` - Docker-dependent

### CodeRabbit Config
See `.coderabbit.yaml` for path-specific review instructions and exclusions.
