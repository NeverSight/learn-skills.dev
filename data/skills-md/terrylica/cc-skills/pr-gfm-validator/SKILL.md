---
name: pr-gfm-validator
description: Validate and fix GFM links in PR descriptions. TRIGGERS - PR links, gh pr create, GFM validation, broken PR links.
allowed-tools: Bash, Read, Grep
---

# PR GFM Link Validator

Validate and auto-convert GFM links in pull request descriptions to prevent 404 errors.

## When to Use This Skill

This skill triggers when:

- Creating a pull request from a feature branch
- Discussing PR descriptions or body content
- Mentioning GFM links, PR links, or link validation
- Using `gh pr create` or `gh pr edit`

## The Problem

Repository-relative links in PR descriptions resolve to the **base branch** (main), not the feature branch:

| Link in PR Body            | GitHub Resolves To            | Result                            |
| -------------------------- | ----------------------------- | --------------------------------- |
| `[ADR](/docs/adr/file.md)` | `/blob/main/docs/adr/file.md` | 404 (file only on feature branch) |

## The Solution

Convert repo-relative links to absolute blob URLs with the correct branch:

```
/docs/adr/file.md
    ↓
https://github.com/{owner}/{repo}/blob/{branch}/docs/adr/file.md
```

---

## Workflow

### Step 1: Detect Context

Before any PR operation, gather repository context:

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
# Get repo owner and name
gh repo view --json nameWithOwner --jq '.nameWithOwner'

# Get current branch
git rev-parse --abbrev-ref HEAD

# Check if on feature branch (not main/master)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  echo "On default branch - no conversion needed"
  exit 0
fi
PREFLIGHT_EOF
```

### Step 2: Identify Links to Convert

Scan PR body for GFM links matching these patterns:

**CONVERT these patterns:**

- `/path/to/file.md` - Repo-root relative
- `./relative/path.md` - Current-directory relative
- `../parent/path.md` - Parent-directory relative

**SKIP these patterns:**

- `https://...` - Already absolute URLs
- `http://...` - Already absolute URLs
- `#anchor` - In-page anchors
- `mailto:...` - Email links

### Step 3: Construct Blob URLs

For each link to convert:

```python
# Pattern
f"https://github.com/{owner}/{repo}/blob/{branch}/{path}"

# Example
owner = "Eon-Labs"
repo = "alpha-forge"
branch = "feat/2025-12-01-eth-block-metrics"
path = "docs/adr/2025-12-01-file.md"

# Result
"https://github.com/Eon-Labs/alpha-forge/blob/feat/2025-12-01-eth-block-metrics/docs/adr/2025-12-01-file.md"
```

### Step 4: Apply Conversions

Replace all identified links in the PR body:

```markdown
# Before

[Plugin Design](/docs/adr/2025-12-01-slug.md)

# After

[Plugin Design](https://github.com/Eon-Labs/alpha-forge/blob/feat/branch/docs/adr/2025-12-01-slug.md)
```

### Step 5: Validate Result

After conversion, verify:

1. All repo-relative links are now absolute blob URLs
2. External links remain unchanged
3. Anchor links remain unchanged

---

## Integration with gh pr create

When creating a PR, apply this workflow automatically:

```bash
/usr/bin/env bash << 'GIT_EOF'
# 1. Get context
REPO_INFO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
OWNER=$(echo "$REPO_INFO" | cut -d'/' -f1)
REPO=$(echo "$REPO_INFO" | cut -d'/' -f2)
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# 2. Process PR body (convert links)
# ... link conversion logic ...

# 3. Create PR with converted body
gh pr create --title "..." --body "$CONVERTED_BODY"
GIT_EOF
```

---

## Link Detection Regex

Use this regex pattern to find GFM links:

```regex
\[([^\]]+)\]\((/[^)]+|\.\.?/[^)]+)\)
```

Breakdown:

- `\[([^\]]+)\]` - Capture link text
- `\(` - Opening parenthesis
- `(/[^)]+|\.\.?/[^)]+)` - Capture path starting with `/`, `./`, or `../`
- `\)` - Closing parenthesis

---

## Examples

### Example 1: Simple Repo-Relative Link

**Input:**

```markdown
See the [ADR](/docs/adr/2025-12-01-eth-block-metrics.md) for details.
```

**Context:**

- Owner: `Eon-Labs`
- Repo: `alpha-forge`
- Branch: `feat/2025-12-01-eth-block-metrics-data-plugin`

**Output:**

```markdown
See the [ADR](https://github.com/Eon-Labs/alpha-forge/blob/feat/2025-12-01-eth-block-metrics-data-plugin/docs/adr/2025-12-01-eth-block-metrics.md) for details.
```

### Example 2: Multiple Links

**Input:**

```markdown
## References

- [Plugin Design](/docs/adr/2025-12-01-slug.md)
- [Probe Integration](/docs/adr/2025-12-02-slug.md)
- [External Guide](https://example.com/guide)
```

**Output:**

```markdown
## References

- [Plugin Design](https://github.com/Eon-Labs/alpha-forge/blob/feat/branch/docs/adr/2025-12-01-slug.md)
- [Probe Integration](https://github.com/Eon-Labs/alpha-forge/blob/feat/branch/docs/adr/2025-12-02-slug.md)
- [External Guide](https://example.com/guide)
```

Note: External link unchanged.

### Example 3: Credential File Link

**Input:**

```markdown
**See [`.env.clickhouse`](/.env.clickhouse)** for credentials.
```

**Output:**

```markdown
**See [`.env.clickhouse`](https://github.com/Eon-Labs/alpha-forge/blob/feat/branch/.env.clickhouse)** for credentials.
```

---

## Edge Cases

### Already on main/master

- Skip conversion entirely
- Repo-relative links will work correctly

### Empty PR Body

- Nothing to convert
- Proceed with PR creation

### No GFM Links Found

- Nothing to convert
- Proceed with PR creation

### Mixed Link Types

- Convert only repo-relative links
- Preserve external URLs, anchors, mailto links

---

## Post-Change Checklist

After modifying this skill:

1. [ ] Regex patterns still match intended link formats
2. [ ] Examples reflect current behavior
3. [ ] Edge cases documented
4. [ ] Workflow steps are executable

---

## References

- [GitHub Blob URLs](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files)
- [GFM Link Syntax](https://github.github.com/gfm/#links)
- [gh CLI Documentation](https://cli.github.com/manual/gh_pr_create)

---

## Troubleshooting

| Issue                    | Cause                          | Solution                                          |
| ------------------------ | ------------------------------ | ------------------------------------------------- |
| Links still 404 after PR | File not pushed to branch yet  | Push commits before creating PR                   |
| Regex not matching links | Escaped parentheses in content | Use raw string regex pattern                      |
| Branch name has slashes  | URL encoding needed            | Encode branch name for URL construction           |
| External links converted | Pattern too broad              | Check link starts with `/`, `./`, or `../` only   |
| gh repo view fails       | Not in a git repository        | Run from repository root directory                |
| Anchor links broken      | Incorrectly included in scan   | Skip links starting with `#`                      |
| Wrong repo detected      | Remote not set correctly       | Check `git remote -v` output                      |
| Conversion duplicated    | Running validator twice        | Check if links already absolute before converting |
