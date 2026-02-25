---
name: pr-review-and-document
description: This skill should be used when the user asks to "review PR and save results", "run PR review with documentation", "create PR review document", "review and document PR", "save PR review to docs", "document PR review", or mentions reviewing a PR with the intention of saving the review results. Executes comprehensive PR review using pr-review-toolkit with opus model and posts results as a PR comment.
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*)
---

# PR Review and Document

Execute comprehensive PR review using pr-review-toolkit and post structured results as a PR comment.

## When to Use

Invoke this skill when:
- A comprehensive PR review needs to be documented on the PR
- A formal review record is required for a feature branch
- Review findings need to be visible directly on the PR for team reference

## Workflow

### Step 1: Get PR Number (Cache-Aware)

```bash
PR_NUMBER=$("${CLAUDE_PLUGIN_ROOT}/scripts/get-pr-number.sh")
```

This uses the branch-to-PR-number cache (`branch-map.json`) with 1-hour TTL, falling back to GitHub API on cache miss.

If no PR exists for the current branch, inform the user and stop.

### Step 2: Check Existing Review Comment (Cache-Aware)

```bash
EXISTING_CONTENT=$(${CLAUDE_PLUGIN_ROOT}/scripts/cache-read-comment.sh "$PR_NUMBER")
```

This uses the local cache if available, falling back to GitHub API on cache miss.

If content is returned:
- Extract metadata from `<!-- pr-review-metadata ... -->` block
- Note the current `review_round` and issues status

### Step 3: Execute PR Review

Launch the pr-review-toolkit with opus model using the Skill tool:

```
Skill: pr-review-toolkit:review-pr
Args: all
Model: opus
```

**Required agents (always run):**
- **code-reviewer** - General code quality and CLAUDE.md compliance
- **code-simplifier** - Code simplification opportunities
- **silent-failure-hunter** - Error handling and silent failure detection
- **type-design-analyzer** - Type design quality analysis
- **pr-test-analyzer** - Test coverage analysis
- **comment-analyzer** - Comment accuracy and maintainability

**Important:** All agents are mandatory for every review to ensure comprehensive coverage.

### Step 4: Format Review Comment

Structure the review as a PR comment with hidden metadata and collapsible sections.

**Character Limit:** Keep total content under ~40K characters (GitHub limit is 65,536).

#### Metadata Block Format

The metadata block uses HTML comment syntax with a specific marker for identification:
- Opening: `<!-- pr-review-metadata` (marker on same line as opening)
- Content: JSON object with review state
- Closing: `-->` on its own line after the JSON

**Important:** The `find-review-comment.sh` script searches for `<!-- pr-review-metadata` to identify review comments. Do not modify this marker format.

#### Comment Template

```markdown
<!-- pr-review-metadata
{
  "schema_version": "1.0",
  "skill": "pr-review-and-document",
  "review_round": 1,
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "branch": "branch-name",
  "base": "main",
  "issues": {
    "critical": { "total": 0, "fixed": 0 },
    "important": { "total": 0, "fixed": 0 },
    "suggestions": { "total": 0, "fixed": 0 }
  },
  "agents_run": ["code-reviewer", "silent-failure-hunter", "type-design-analyzer", "pr-test-analyzer", "code-simplifier", "comment-analyzer"]
}
-->

## 🤖 PR Review

**Branch:** `branch-name` → `base-branch`
**Round:** N | **Updated:** YYYY-MM-DD
**Reviewer:** claude-opus-4-5 via pr-review-toolkit

---

### 📊 Summary

| Category | Total | Fixed | Remaining |
|----------|-------|-------|-----------|
| 🔴 Critical | X | X | X |
| 🟡 Important | X | X | X |
| 💡 Suggestions | X | X | X |

**Status:** [✅ Ready to merge | ⚠️ Needs attention | 🔴 Blocking issues]

---

### 🔴 Critical Issues

<details open>
<summary><b>1. [Status Emoji] Issue Title</b></summary>

**File:** `path/to/file.ts:line`

**Problem:** Description of the issue.

**Fix:** Resolution or suggested fix.

</details>

[Repeat for each critical issue]

---

### 🟡 Important Issues

<details>
<summary><b>1. [Status Emoji] Issue Title</b></summary>

**File:** `path/to/file.ts:line`

**Problem:** Description.

**Fix:** Resolution.

</details>

[Repeat for each important issue]

---

### 💡 Suggestions

<details>
<summary>View N suggestions (M addressed)</summary>

| # | Suggestion | Status |
|---|------------|--------|
| 1 | Description | ✅ / ⏭️ |

</details>

---

### ✨ Strengths

- Positive observation 1
- Positive observation 2

---

### 📋 Type Design Ratings

| Type | Encap. | Express. | Useful. | Enforce. | Overall |
|------|--------|----------|---------|----------|---------|
| TypeName | X/10 | X/10 | X/10 | X/10 | **X/10** |

---

### 🎯 Action Plan

**Before Merge:**
- [ ] Action item 1
- [x] Completed item

**After Merge (Backlog):**
- [ ] Future improvement

---

<sub>Generated by pr-review-and-document skill | Round N | [View edit history](click edited)</sub>
```

### Step 5: Write Review Comment (Cache-Aware)

Pipe the formatted content directly to `cache-write-comment.sh` via `--stdin`:

```bash
echo "$REVIEW_CONTENT" | ${CLAUDE_PLUGIN_ROOT}/scripts/cache-write-comment.sh --stdin "$PR_NUMBER"
```

The script will:
- Update local cache (`.pr-review-cache/pr-{N}.json`)
- Sync to GitHub via `upsert-review-comment.sh --stdin`（stdin pipe，不使用 temp file）
- Return the comment URL

### Step 6: Verify

Confirm the comment was posted successfully by checking the returned URL.

## Status Indicators

Use consistent status indicators:

| Indicator | Meaning |
|-----------|---------|
| ✅ | Fixed / Resolved |
| ⏭️ | Deferred / Skipped intentionally |
| ⚠️ | Needs attention |
| 🔴 | Blocking / Critical |

## Multi-Round Reviews

When updating an existing review:

1. Increment `review_round` in metadata
2. Update `updated_at` timestamp
3. Update issue counts and statuses
4. Keep the same comment (GitHub tracks edit history)

Previous review content is preserved in GitHub's "edited" dropdown, providing full audit trail.

## Integration Notes

### Using with pr-review-toolkit

This skill wraps the `pr-review-toolkit:review-pr` command and:
1. Forces opus model for comprehensive analysis
2. **Always runs all 6 review agents** (mandatory)
3. Formats output as structured PR comment
4. Posts directly to the PR

### Character Limit Handling

If review content exceeds ~40K characters:
1. Collapse more sections with `<details>`
2. Summarize verbose descriptions
3. Move detailed code examples to collapsed sections

### No PR Available

If the current branch has no open PR:
- Inform the user
- Suggest creating a PR first: `gh pr create`

## Validation Checklist

Before posting the review comment:

- [ ] PR number correctly identified
- [ ] All 6 review agents executed
- [ ] Metadata JSON is valid
- [ ] Issue counts match content
- [ ] Status indicators are consistent
- [ ] Content is under 40K characters
- [ ] Comment posted/updated successfully
