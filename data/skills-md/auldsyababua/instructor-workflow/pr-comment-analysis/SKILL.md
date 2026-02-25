---
name: pr-comment-analysis
description: Extract, consolidate, and prioritize all comments from GitHub Pull Requests for systematic code review. Fetches both inline review comments and general PR conversation, then analyzes and organizes them by priority (critical bugs/security, design improvements, style nitpicks). Use when working with PR reviews, consolidating feedback from multiple reviewers, or creating action plans from review comments.
---

# PR Comment Analysis

## Overview

This skill provides comprehensive extraction and analysis of GitHub Pull Request comments, enabling systematic handling of code review feedback. It fetches all comments from a PR (both inline code comments and general conversation), consolidates feedback from multiple reviewers, identifies high-consensus issues, and generates prioritized action plans.

## When to Use

Use pr-comment-analysis when:
1. Working through code review feedback on a GitHub PR
2. Consolidating comments from multiple reviewers
3. Prioritizing which review feedback to address first
4. Tracking resolution of PR review comments
5. Analyzing review patterns for process improvement
6. Creating systematic action plans from PR feedback

## Key Capabilities

### 1. Comprehensive Comment Extraction
- Fetches **ALL** comments from a GitHub PR via API
- Captures both review comments (inline code comments) and issue comments (general PR conversation)
- Supports incremental updates (re-run to fetch new comments without duplicates)
- Handles pagination automatically (works with PRs having hundreds of comments)
- Preserves complete metadata (file paths, line numbers, timestamps, diff hunks)

### 2. Comment Consolidation
- Groups comments by file path and code section
- Identifies semantically similar comments from different reviewers
- Flags "High Consensus Issues" where multiple reviewers raised the same concern
- Tracks comment threads and replies

### 3. Intelligent Prioritization
- **Level 1 (Critical)**: Bugs, security issues, performance problems, high-consensus issues
- **Level 2 (Design)**: Architecture improvements, refactoring suggestions, design patterns
- **Level 3 (Style)**: Code style, naming conventions, formatting, documentation nitpicks

### 4. Context-Aware Validation (NEW)
- Validates comment applicability against project context (.project-context.md)
- Researches proposed fixes using ref.tools and Exa search MCP
- Identifies deprecated patterns or stack-specific considerations
- Filters out comments based on outdated assumptions

### 5. Impact Analysis (NEW)
- Analyzes if proposed fixes might break code elsewhere
- Searches codebase for similar patterns and dependencies
- Identifies code NOT in the PR that could be affected
- Flags potential breaking changes reviewers couldn't see
- Generates "ripple effect" warnings for risky changes

### 6. Actionable Output
- Generates structured action plans in markdown format
- Provides validated, context-aware recommended fixes
- Includes impact warnings for each change
- Includes original comments with context and links
- Creates checkable task lists for systematic resolution

## Workflow

### Step 1: Extract PR Comments

Navigate to your repository and run the comment grabber:

```bash
cd /path/to/your/repo
python /path/to/pr-comment-analysis/scripts/pr-comment-grabber.py owner/repo PR_NUMBER
```

**Example:**
```bash
cd ~/Desktop/projects/my-app
python ~/skills/pr-comment-analysis/scripts/pr-comment-grabber.py myorg/my-app 42
```

This creates `pr-code-review-comments/pr42-code-review-comments.json` in your repo.

**To fetch new comments after initial run:**
```bash
# Same command - it will merge new comments automatically
python ~/skills/pr-comment-analysis/scripts/pr-comment-grabber.py myorg/my-app 42
# Output: "New comments added: 5" (shows incremental update)
```

### Step 2: Analyze, Validate, and Prioritize Comments

Load the JSON output and provide it to an LLM agent with the enhanced analysis prompt from `references/analysis-prompt.md`.

**Critical: The analysis now includes three phases:**

#### Phase A: Initial Consolidation
- Group comments by file and identify consensus
- Categorize by type (critical/design/style)

#### Phase B: Context Validation (NEW)
For each comment:
1. **Read project context**: Check `.project-context.md` for:
   - Deprecated stack/tools that reviewer might not know about
   - Project-specific patterns or constraints
   - Known technical debt or planned refactors
2. **Validate applicability**: Is this comment still relevant given project context?
3. **Flag outdated comments**: Mark comments based on wrong assumptions

#### Phase C: Fix Validation & Impact Analysis (NEW)
For each proposed fix:
1. **Research the fix**: Use `mcp__ref__ref_search_documentation` and `mcp__exasearch__web_search_exa` to validate:
   - Is the suggested approach actually correct?
   - Are there better alternatives?
   - What are known gotchas?
2. **Search for similar patterns**: Use `Grep` to find similar code patterns in the codebase
3. **Identify dependencies**: Find code that might depend on current behavior
4. **Assess impact**: Will this fix break code NOT in the PR?
5. **Generate warnings**: Create "Ripple Effect" warnings for risky changes

**Example validation:**
```
Reviewer suggests: "Use async/await instead of callbacks"

VALIDATION:
- Context check: .project-context.md shows Node 12 (async/await supported) ✅
- Research: Exa search confirms async/await best practice ✅
- Pattern search: Found 47 other files using callbacks
- Impact: Converting this one function won't break anything, but creates inconsistency
- Warning: ⚠️ Consider converting all callbacks to async/await in separate PR
```

The agent will generate a **validated, context-aware** action plan.

### Step 3: Work Through Validated Action Plan Systematically

Start with Level 1 (Critical) issues:
- Address each issue
- Mark as complete
- Re-run comment grabber to fetch new review feedback
- Repeat analysis if significant new comments added

## Output Format

### Comment JSON Schema

Each comment in the extracted JSON has this structure:

**Review comment (inline):**
```json
{
  "comment_type": "review",
  "id": 123456789,
  "user": "reviewer-username",
  "body": "Consider using a constant here instead of magic number",
  "path": "src/utils/constants.py",
  "line": 42,
  "diff_hunk": "@@ -40,6 +40,8 @@ ...",
  "created_at": "2025-01-15T14:30:00Z",
  "html_url": "https://github.com/owner/repo/pull/42#discussion_r123456789"
}
```

**Issue comment (general PR conversation):**
```json
{
  "comment_type": "issue",
  "id": 987654321,
  "user": "qodo-merge",
  "body": "## PR Analysis Summary\n\nOverall Score: 85/100...",
  "created_at": "2025-01-15T12:00:00Z",
  "html_url": "https://github.com/owner/repo/pull/42#issuecomment-987654321",
  "path": null,
  "line": null
}
```

**🚨 CRITICAL**: Bot comments (Qodo, CodeRabbit, etc.) with `comment_type: "issue"` often contain actionable suggestions buried in HTML tables/markdown. DO NOT dismiss these as "informational summaries". Parse the full body text for:
- Security compliance issues
- Code suggestions with diffs
- Documentation fixes
- Input validation recommendations
- Breaking change warnings

**Example Qodo actionable content in "issue" comment**:
```
## PR Code Suggestions ✨
Category    Suggestion                                    Impact
General     Fix broken relative link in documentation   Low
Possible    Validate required input to prevent errors   Low
```

### Analysis Action Plan Format

```markdown
# Consolidated Pull Request Review Action Plan

## 1. High Consensus & Critical Issues

### src/auth/validator.py: SQL Injection Vulnerability
**Consensus:** alice-reviewer, bob-security, charlie-lead
**Severity:** CRITICAL - Security issue

**Original Comments:**
- alice-reviewer (Line 156): "This string concatenation could allow SQL injection"
- bob-security (Line 156): "SQL injection risk here - use parameterized queries"
- charlie-lead (Line 158): "Security: parameterize this database query"

**Recommended Fix:**
Replace string concatenation with parameterized query:
```python
# Before
query = f"SELECT * FROM users WHERE id = {user_id}"
# After
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

## 2. Design and Architectural Improvements

### src/services/cache.py: Cache Invalidation Strategy
**Priority:** HIGH - Design issue affecting maintainability
...

## 3. Style and Clarity Nitpicks

### Multiple files: Inconsistent variable naming
**Priority:** LOW - Code style
...
```

## Comment Tracking

### Marking Comments as Addressed

When you resolve a comment:
1. Make the code change
2. Commit with reference to comment: `git commit -m "fix: address SQL injection in validator.py (review comment #123456789)"`
3. Reply to the comment on GitHub linking the commit
4. Re-run the comment grabber to update your local JSON

### Progress Tracking

Create a tracking file in your repo:

```markdown
# PR #42 Review Progress

## Critical Issues (3/5 complete)
- [x] SQL injection in auth/validator.py
- [x] Race condition in services/cache.py
- [x] Memory leak in workers/processor.py
- [ ] Unhandled exception in api/routes.py
- [ ] Missing input validation in forms/user.py

## Design Improvements (2/8 complete)
- [x] Refactor cache invalidation logic
- [x] Extract magic numbers to constants
- [ ] ...
```

## Prerequisites

### Python Requirements
```bash
pip install requests
```

### GitHub Token Setup

**Option 1: Environment variable**
```bash
export GITHUB_TOKEN=ghp_your_token_here
```

**Option 2: 1Password (if configured)**
```bash
export GITHUB_TOKEN=$(op item get "GitHub" --fields label="Personal Access Token")
```

**Option 3: Pass via CLI**
```bash
python pr-comment-grabber.py owner/repo 42 --token ghp_xxxxx
```

**Token Requirements:**
- Scope: `repo` (for private repos) or `public_repo` (for public repos)
- Generate at: https://github.com/settings/tokens

## Troubleshooting

### "Authentication failed"
- Verify token: `echo $GITHUB_TOKEN`
- Check token has required scopes (repo or public_repo)
- Regenerate token if expired

### "PR not found"
- Verify repository format: `owner/repo` (no spaces, no .git)
- Verify PR number is correct
- Confirm you have access to the repository

### "requests library not found"
```bash
pip install requests
```

### "File already exists" when re-running
This is normal - the script merges new comments with existing ones. Check output for:
```
Loaded 27 existing comments
New comments added: 3
Total after merge: 30
```

## Advanced Usage

### Batch Processing Multiple PRs

```bash
# Create a script to process all open PRs
for pr in 42 43 44 45; do
  python pr-comment-grabber.py owner/repo $pr
done
```

### Integration with CI/CD

Add to your PR workflow:

```yaml
# .github/workflows/pr-comments.yml
name: Extract PR Comments
on: pull_request_review

jobs:
  extract-comments:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Extract comments
        run: |
          python scripts/pr-comment-grabber.py ${{ github.repository }} ${{ github.event.pull_request.number }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - uses: actions/upload-artifact@v2
        with:
          name: pr-comments
          path: pr-code-review-comments/
```

### Analysis Automation

Create a wrapper script that fetches and analyzes:

```bash
#!/bin/bash
# analyze-pr.sh

PR_NUM=$1
REPO="owner/repo"

# Fetch comments
python pr-comment-grabber.py $REPO $PR_NUM

# Analyze with Claude (requires claude CLI)
claude analyze-reviews --input pr-code-review-comments/pr${PR_NUM}-code-review-comments.json
```

## Configuration

### Customizing Analysis Priorities

Edit `references/analysis-prompt.md` to adjust prioritization criteria:

**Example customizations:**
- Weight security issues higher than performance
- Separate "breaking changes" into their own category
- Add custom categories for your team's standards
- Adjust high-consensus threshold (e.g., require 3+ reviewers instead of 2+)

### Filtering Comments

Filter JSON by comment type before analysis:

```bash
# Only review comments (inline)
jq '[.[] | select(.comment_type == "review")]' pr42-code-review-comments.json > pr42-inline-only.json

# Only comments from specific reviewers
jq '[.[] | select(.user == "security-team-bot")]' pr42-code-review-comments.json > pr42-security-only.json

# Only comments after a certain date
jq '[.[] | select(.created_at > "2025-01-20")]' pr42-code-review-comments.json > pr42-recent.json
```

## MCP Tool Requirements

This skill uses the following MCP tools for validation and impact analysis:

### Required MCP Tools
- **`mcp__ref__ref_search_documentation`**: Search documentation for validation (ref.tools MCP)
- **`mcp__exasearch__web_search_exa`**: Web search for best practices validation (Exa MCP)
- **`Grep`**: Search codebase for similar patterns and dependencies

### Setup
Ensure these MCP servers are configured in your Claude Code settings:
```json
{
  "mcpServers": {
    "ref": {
      "command": "npx",
      "args": ["-y", "@reftools/mcp-server-ref"]
    },
    "exasearch": {
      "command": "npx",
      "args": ["-y", "@exasearch/mcp-server"],
      "env": {
        "EXA_API_KEY": "your-exa-api-key"
      }
    }
  }
}
```

## Best Practices

### For Individual Contributors
1. Run comment grabber **immediately after review** (while context is fresh)
2. **NEW**: Run validation analysis to catch impacts reviewers couldn't see
3. Address critical issues **before** design improvements
4. Reply to comments on GitHub as you resolve them (maintain reviewer engagement)
5. Re-run grabber before pushing new commits (check for new feedback)
6. **NEW**: Challenge outdated comments politely (backed by validation research)

### For Teams
1. **Standardize comment extraction**: Add to team's PR checklist
2. **Track consensus patterns**: Identify recurring issues for team learning
3. **Measure review quality**: Analyze comment distribution (critical vs. nitpicks)
4. **Automate extraction**: Run on PR review webhooks
5. **Archive review analytics**: Track team improvement over time

### For PR Authors
1. Extract comments as soon as **first substantive review** arrives
2. Create action plan **before** making changes (avoid partial fixes)
3. Work systematically through priorities (don't cherry-pick easy items)
4. Update PR description with progress (reviewers see you're addressing feedback)
5. Ask clarifying questions on ambiguous comments **before** implementing

### For Reviewers
1. Use inline comments for **code-specific** feedback
2. Use issue comments for **architectural** or **process** discussions
3. Mark critical issues explicitly (e.g., "🔴 CRITICAL: ...")
4. Group related comments (e.g., "This pattern appears 5 times - consider refactoring")
5. Link to standards/docs when applicable

## Integration with Other Skills

This skill works well with:
- **code-reviewer**: Generate reviews, then extract and prioritize comments
- **git-workflow**: Commit changes with comment references
- **documentation**: Document patterns identified in reviews
- **test-generator**: Create tests for bugs found in reviews

## References

- **Analysis Prompt**: `references/analysis-prompt.md` - Full LLM prompt for comment analysis
- **Example Output**: `references/example-analysis.md` - Sample analyzed PR comments
- **GitHub API Docs**: `references/github-api.md` - API details for comment endpoints

## Limitations

- Requires GitHub Personal Access Token (no anonymous access)
- Does not fetch PR descriptions or commit messages (only comments)
- Does not track comment resolution status (GitHub doesn't provide this via API)
- Large PRs (>200 comments) may require longer analysis time
- External tools (Qodo, CodeRabbit) may have different comment formats

## Version

- **Script Version**: 2.0
- **Skill Version**: 1.0
- **Last Updated**: 2025-10-24
