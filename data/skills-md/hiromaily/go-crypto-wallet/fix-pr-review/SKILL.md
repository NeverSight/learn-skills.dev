---
name: fix-pr-review
description: Address PR review comments by selecting appropriate skills based on modified files. Use when fixing review feedback on pull requests.
---

# Fix PR Review Workflow

Workflow for addressing review comments on pull requests.

## Expected Command Format

```
Please revise the reviews at https://github.com/{owner}/{repo}/pull/{pr_number}#pullrequestreview-{review_id} and reply to each review with your results.
```

## Input Formats

User may provide either:

- **PR number**: `563`, `#563`
- **Full review URL**: `https://github.com/{owner}/{repo}/pull/{pr_number}#pullrequestreview-{review_id}`

Extract `{pr_number}` (and optionally `{review_id}`) from the input.

## Process Overview

```
1. Fetch PR details and review comments
2. Classify files and load development skill
3. Fix each comment
4. Run verification
5. Commit and push changes
6. Reply to each review comment on GitHub
```

## Step 1: Fetch PR Information

```bash
gh pr view {pr_number}
gh pr diff {pr_number} --name-only
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews/{review_id}/comments
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
```

## Step 2: Classify and Load Skill

Classify modified files and load the appropriate development skill.

For file-type-to-skill mapping, see `.claude/rules/general.md` (Language-Specific Skills table).

## Step 3: Address ALL Comments

**IMPORTANT**: Every review comment must be addressed. Do not skip or miss any comment.

1. **List all comments** from the API response
2. **Sort by priority**: Security > Functionality > Code Quality
3. **Fix each one**, one by one
4. **Track status**: FIXED, ALREADY APPLIED, or SKIPPED

## Step 4: Run Verification

Run verification commands from the loaded development skill.

For verification commands by file type, see `.claude/rules/task-context-loading.md` (Verification Commands by File Type).

If PR modifies multiple file types, run all applicable verification commands.

## Step 5: Commit and Push

Follow `git-workflow` skill for commit conventions.

```bash
git add .
git commit -m "$(cat <<'EOF'
fix(scope): address PR review comments

- Fix: [specific fix 1]
- Fix: [specific fix 2]
EOF
)"
git push
```

## Step 6: Reply to Each Review Comment on GitHub

**IMPORTANT**: After pushing fixes, reply to each review comment on GitHub.

### How to Reply

```bash
# Reply to inline review comment
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -f body="Fixed: [description of what was changed]"

# Reply to PR conversation (for summary-level review comments)
gh pr comment {pr_number} --body "Addressed all review comments. See commit [short_hash]."
```

### Reply Templates

| Status             | Reply Template                                                    |
| ------------------ | ----------------------------------------------------------------- |
| FIXED              | `Fixed: [description]. See commit [short_hash].`                  |
| ALREADY APPLIED    | `Already addressed in commit [short_hash].`                       |
| SKIPPED            | `Acknowledged. [reason for not changing, or alternative approach]` |

### Notes

- Reply to **every** comment, not just the ones that resulted in code changes
- Reference the commit hash so reviewers can verify the fix
- Comment IDs are available from the API responses in Step 1 (`.[].id` field)

## Related

- `.claude/rules/general.md` - File-type-to-skill mapping, verification commands
- `.claude/rules/task-context-loading.md` - Verification matrix
- `.claude/skills/git-workflow/SKILL.md` - Commit conventions
