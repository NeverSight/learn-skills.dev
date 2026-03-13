---
name: github-sync
description: Sync GitHub PRs, merges, and releases to PM workspace. Use when running /sync-github or /sync-dev commands, or generating release notes.
---

# GitHub Sync Skill

Procedural knowledge for synchronizing GitHub PR and merge data with PM workspace initiatives.

## When to Use

- Running `/sync-github` command
- Running `/sync-dev` for unified dev status
- Generating release notes
- Tracking shipped work per initiative
- Building changelog from merged PRs

## Prerequisites

Requires `gh` CLI to be installed and authenticated:

```bash
gh auth status  # Verify authentication
```

## Data Sources

### GitHub Data (via `gh` CLI)

- **PRs**: Merged pull requests with titles, descriptions, authors
- **Commits**: Commit messages (often contain Linear issue refs)
- **Branches**: Branch naming patterns for initiative mapping
- **Labels**: PR labels for categorization

### Local Data

- `pm-workspace-docs/initiatives/active/*/_meta.json` - Initiative metadata
- `pm-workspace-docs/signals/releases/` - Release signal storage
- `pm-workspace-docs/status/dev-status-*.md` - Dev status reports

## Initiative Mapping

### Primary Strategy: Linear Issue References (ASK-XXXX)

**This is the PRIMARY method** - engineers already include Linear issue IDs in branch names.

Extract Linear issue IDs from:

- **Branch names**: `ASK-4591-engagements-card-queries` → `ASK-4591`
- **Commit messages**: `ASK-1234: Fix bug`
- **PR titles**: `[ASK-1234] Add feature`
- **PR body**: `Closes ASK-1234`

Then: Linear issue → project → initiative via `linear_project_id` in `_meta.json`

```
Branch: ASK-4591-engagements-card-queries
         ↓
Extract: ASK-4591
         ↓
Linear API: linear_getIssueById("ASK-4591")
         ↓
Issue.project.id: "05066db9-89d7-432c-bffd-234ca92af024"
         ↓
_meta.json lookup: linear_project_id matches
         ↓
Initiative: internal-search
```

### Mapping Priority

**Based on 2026-01-23 audit - use what engineers actually do:**

1. **Linear issue reference in branch** (MOST RELIABLE - 70%+ of PRs)
   - Regex: `ASK-\d+` in branch name
   - Call `linear_getIssueById(ASK-XXXX)` to get project
   - Map project → initiative via `linear_project_id` in `_meta.json`
2. **Linear issue reference in PR title/body** (SECONDARY)
   - Patterns: `[ASK-XXXX]`, `ASK-XXXX:`, `Closes ASK-XXXX`
   - Same lookup flow as above
3. **Cross-reference with Notion** (VALIDATION)
   - If issue's project matches Notion "Linear Link" → confirmed
   - If Eng Spec has "Linear Epic" for same issue → extra validation

4. **Legacy: Labels/Prefixes** (0% adoption - fallback only)
   - Explicit PR labels if present
   - Branch prefix match if present
5. **Unlinked** (no mapping found)
   - PR has no ASK-XXXX reference
   - Infrastructure/maintenance work often falls here

### ASK-XXXX Extraction Patterns

```regex
# Branch name patterns
ASK-(\d+)[-_].*           # ASK-4591-feature-name
.*[-_]ASK-(\d+)[-_].*     # fix-ASK-4591-bug

# PR title patterns
\[ASK-(\d+)\].*           # [ASK-4591] Add feature
ASK-(\d+):.*              # ASK-4591: Fix bug

# PR body patterns
(?:Closes|Fixes|Resolves)\s+ASK-(\d+)   # Closes ASK-4591
Linear:\s*ASK-(\d+)                      # Linear: ASK-4591
```

### Confidence Scoring

| Signal                                                         | Confidence    |
| -------------------------------------------------------------- | ------------- |
| ASK-XXXX in branch → valid project → `linear_project_id` match | 95%           |
| ASK-XXXX in PR title/body → valid project                      | 90%           |
| Notion "Linear Epic" validates same project                    | +5% bonus     |
| No ASK reference, no labels                                    | 0% → unlinked |

**No labels/prefixes required** - this strategy works with existing engineering workflow.

## Sync Procedures

### Step 1: Fetch Merged PRs

```bash
# Last 24 hours (default)
gh pr list --repo askelephant/elephant-ai \
  --state merged \
  --json number,title,author,mergedAt,headRefName,labels,body \
  --limit 100

# Since specific date
gh pr list --repo askelephant/elephant-ai \
  --state merged \
  --search "merged:>=2026-01-22" \
  --json number,title,author,mergedAt,headRefName,labels,body
```

### Step 2: Extract PR Data

For each merged PR, extract:

- **Number**: PR number (#123)
- **Title**: PR title
- **Author**: GitHub username
- **Merged At**: Merge timestamp
- **Branch**: Head branch name (for prefix matching)
- **Labels**: PR labels (for label matching)
- **Body**: PR description (for Linear refs)

### Step 3: Map to Initiatives

```
For each PR:
  1. Check labels for initiative:* pattern
  2. If no match, check branch prefix against _meta.json
  3. If no match, extract Linear issue refs (ASK-1234)
  4. If Linear ref found, lookup project → initiative
  5. If no match, mark as "unlinked"
```

### Step 4: Update Initiative Metadata

For each mapped initiative:

```json
{
  "dev_activity": {
    "last_synced": "2026-01-23T18:00:00Z",
    "github_prs_merged_30d": 15,
    "last_pr_merged": "2026-01-23",
    "recent_prs": [{ "number": 123, "title": "...", "merged_at": "..." }]
  }
}
```

### Step 5: Generate Release Summary

**Release Signal Format:**

```markdown
# Release Summary: YYYY-MM-DD

**Period:** [start_date] to [end_date]
**Repository:** elephant-ai
**PRs Merged:** X
**Contributors:** [list of unique authors]

## By Initiative

### Global Chat

**PRs Merged:** 3 | **Lines Changed:** +500/-200

- **#123**: Fix context window bug (@skylar) - merged Jan 23
- **#125**: Add keyboard shortcuts (@dylan) - merged Jan 23
- **#128**: Improve error handling (@palmer) - merged Jan 22

### CRM Agent

**PRs Merged:** 2 | **Lines Changed:** +300/-100

- **#124**: HubSpot app card POC (@palmer) - merged Jan 23
- **#127**: Agent permission fixes (@adam) - merged Jan 22

## Unlinked Changes

PRs without initiative mapping:

- **#126**: Dependency updates (@matt) - merged Jan 23
- **#129**: CI improvements (@jason) - merged Jan 22

## Changelog

### Features

- Global Chat: Added keyboard shortcuts (#125)
- CRM Agent: HubSpot app card POC (#124)

### Bug Fixes

- Global Chat: Fixed context window bug (#123)
- CRM Agent: Fixed agent permissions (#127)

### Improvements

- Global Chat: Improved error handling (#128)

### Maintenance

- Dependency updates (#126)
- CI improvements (#129)
```

## CLI Commands Reference

### List Merged PRs

```bash
# Recent merges (default repo)
gh pr list -s merged --json number,title,author,mergedAt,headRefName

# With date filter
gh pr list -s merged --search "merged:>=2026-01-20"

# Specific repo
gh pr list -R askelephant/elephant-ai -s merged
```

### Get PR Details

```bash
gh pr view 123 --json title,body,author,mergedAt,labels,commits
```

### Get Commits

```bash
# Commits in date range
gh api repos/askelephant/elephant-ai/commits \
  --jq '.[].commit.message' \
  -f since=2026-01-20T00:00:00Z
```

## Output Formats

### Dev Status Section (for /sync-dev)

```markdown
## Recently Shipped (GitHub)

**Last 24 Hours:** 5 PRs merged
**Last 7 Days:** 23 PRs merged

### By Initiative

| Initiative  | PRs | Contributors    |
| ----------- | --- | --------------- |
| Global Chat | 3   | @skylar, @dylan |
| CRM Agent   | 2   | @palmer, @adam  |
| Unlinked    | 2   | @matt, @jason   |

### Recent Merges

- #128: Improve error handling (@palmer) - 2 hours ago
- #127: Agent permission fixes (@adam) - 5 hours ago
- #126: Dependency updates (@matt) - 8 hours ago
```

### JSON Output

```json
{
  "generated_at": "2026-01-23T18:00:00Z",
  "period": {
    "start": "2026-01-22T00:00:00Z",
    "end": "2026-01-23T18:00:00Z"
  },
  "repository": "askelephant/elephant-ai",
  "summary": {
    "total_prs": 8,
    "unique_authors": 5,
    "initiatives_touched": 3
  },
  "by_initiative": [
    {
      "slug": "global-chat",
      "prs_count": 3,
      "authors": ["skylar", "dylan", "palmer"],
      "prs": [...]
    }
  ],
  "unlinked": [...],
  "changelog": {
    "features": [...],
    "fixes": [...],
    "improvements": [...]
  }
}
```

## PR Categorization

Categorize PRs by title/label patterns:

| Category      | Patterns                                                     |
| ------------- | ------------------------------------------------------------ |
| Feature       | `feat:`, `feature:`, `Add`, `Implement`, label:`enhancement` |
| Bug Fix       | `fix:`, `bug:`, `Fix`, `Resolve`, label:`bug`                |
| Improvement   | `improve:`, `refactor:`, `Improve`, `Update`, `Enhance`      |
| Maintenance   | `chore:`, `deps:`, `ci:`, `Bump`, `Update deps`              |
| Documentation | `docs:`, `Doc`, `README`                                     |

## Error Handling

### gh CLI Not Installed

```
⚠️ GitHub CLI (gh) not found.

Install with: brew install gh
Then authenticate: gh auth login
```

### Not Authenticated

```
⚠️ GitHub CLI not authenticated.

Run: gh auth login
```

### Repository Access Denied

```
⚠️ Cannot access repository: askelephant/elephant-ai

Verify you have read access to this repository.
```

### No PRs Found

```
ℹ️ No merged PRs found in the specified time range.

Try expanding the date range:
/sync-github --since 2026-01-15
```

## Integration Points

### With Linear Sync

- **Primary flow**: ASK-XXXX in branch → Linear issue → project → initiative
- Cross-reference Linear issues in PR messages
- Build complete work-to-ship pipeline
- Correlate cycle issues with merged PRs

### With Notion Sync

- Validate mappings against Notion "Linear Link" in Projects DB
- Cross-check against Notion "Linear Epic" in Eng Specs
- If PR's Linear project matches Notion-linked project → high confidence

### With Portfolio Status

- Include `github_prs_merged_30d` in health calculations
- Surface active GitHub work in artifact matrix
- Alert on initiatives with code changes but no doc updates

### With Sync Queue

- PRs without ASK-XXXX reference → check if common pattern
- Suggest adding Linear issue to PR if pattern detected
- Truly unmapped work → add to unlinked summary

### Save Locations

| Output              | Location                                 |
| ------------------- | ---------------------------------------- |
| Release signal      | `signals/releases/YYYY-MM-DD-release.md` |
| Dev status          | `status/dev-status-YYYY-MM-DD.md`        |
| Initiative metadata | `initiatives/active/*/_meta.json`               |
| Sync queue          | `sync-queue.md`                          |
