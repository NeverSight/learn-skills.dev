---
name: issues-workflow
description: "Plan and track work using a GitHub Issues-first workflow with sub-issue hierarchies. Use whenever the user needs to organize issues into parent-child hierarchies, manage sub-issues, track research across multiple issues, or coordinate cross-repo issue workflows. Also use when the user asks about issue tracking strategy or how to structure work breakdown in GitHub. Do NOT use for creating individual issues (use issue-create instead) or for GitHub Projects board management."
allowed-tools: Read, Bash, Grep, Glob, Write
---

# GitHub Issues-First Workflow

**Default**: Use GitHub Issues exclusively for all content, hierarchy, and tracking.
**Optional**: Link to Projects v2 for cross-repo visualization only.

## Critical Principle: Issues Are Everything

**GitHub Issues = Content + Hierarchy + Status + History.**
**GitHub Projects v2 = Visualization layer only (no content, no history).**

With sub-issues (GA April 2025), Issues now handle hierarchy natively. Projects v2 is reduced to an optional visualization dashboard.

### Issues vs Projects v2

| Capability       | Issues (Default)             | Projects v2 (Visualization Only)   |
| ---------------- | ---------------------------- | ---------------------------------- |
| **Content**      | Body, comments, code blocks  | None (links to Issues only)        |
| **Hierarchy**    | Sub-issues (100 per parent)  | Flat list                          |
| **Status**       | Open/Closed + labels         | Custom fields (no history)         |
| **Edit history** | Full diff on every edit      | None                               |
| **Timeline**     | All changes logged           | Status changes only (30-day limit) |
| **Search**       | Full-text + 30+ filters      | Limited                            |
| **CLI**          | `gh issue list/view/create`  | `gh project` (Classic PAT only)    |
| **Cross-repo**   | Manual (`--repo A --repo B`) | Single dashboard view              |

### When to Use Each

```
┌─────────────────────────────────────────────────────────────┐
│                 ISSUES-FIRST WORKFLOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ALWAYS use Issues for:                                     │
│   ├── All content (findings, analysis, conclusions)          │
│   ├── Hierarchy (parent + sub-issues)                        │
│   ├── Status tracking (labels: status:in-progress)           │
│   ├── Categorization (labels: research:regime, priority:P0)  │
│   └── Filtering (gh issue list --label X --state Y)          │
│                                                              │
│   OPTIONALLY use Projects v2 for:                            │
│   ├── Cross-repo dashboard (single view across repos)        │
│   ├── Kanban visualization (drag-and-drop board)             │
│   ├── Roadmap timeline (visual date-based view)              │
│   └── Stakeholder reporting (Status Updates feed)            │
│                                                              │
│   NEVER put in Projects v2:                                  │
│   ├── Research findings (no edit history)                    │
│   ├── Analysis details (lost on update)                      │
│   ├── Any text content (use Issue body/comments)             │
│   └── Anything you need to track changes for                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Decision Tree

```
Need to track work?
├── Single repo, <50 issues → Issues only (skip Projects)
├── Single repo, 50+ issues → Issues + optional Project for kanban
├── Multiple repos → Issues + Project for cross-repo dashboard
└── Stakeholder visibility → Issues + Project Status Updates
```

## When to Use This Skill

Use this skill when:

- Setting up issue hierarchy with sub-issues (default workflow)
- Creating cross-repo visualization dashboards
- Configuring auto-linking from Issues to Projects
- Setting up stakeholder Status Updates

**Remember**: All content lives in Issues. Projects v2 is a read-only visualization layer.

## Invocation

**Slash command**: `/gh-tools:issues-workflow`

**Natural language triggers**:

- "Create sub-issues for this parent"
- "Set up issue hierarchy"
- "Create cross-repo dashboard"
- "Link issues to project for visualization"

## Issues-First Workflow (Default)

### Sub-Issues: Native Hierarchy (GA April 2025)

Sub-issues replace the need for Projects v2 hierarchy. Use for all structured work.

#### When to Use Sub-Issues

| Use Case                     | Example                                                             | Why Sub-Issues                             |
| ---------------------------- | ------------------------------------------------------------------- | ------------------------------------------ |
| **Research breakdown**       | Parent: "Investigate microstructure" → Subs: individual patterns    | Track which patterns validated/invalidated |
| **Epic decomposition**       | Parent: "User authentication" → Subs: login, logout, password reset | Progress bar shows completion %            |
| **Multi-step investigation** | Parent: "Debug performance issue" → Subs: profiling, memory, CPU    | Each sub can be assigned differently       |
| **Phased work**              | Parent: "v2.0 release" → Subs: Phase 1, Phase 2, Phase 3            | Natural ordering with timeline             |

#### When NOT to Use Sub-Issues

| Situation                    | Use Instead                           | Why                            |
| ---------------------------- | ------------------------------------- | ------------------------------ |
| Simple checklist (< 5 items) | Markdown checkboxes in issue body     | Less overhead, editable inline |
| Cross-repo dependencies      | Issue references (`See org/repo#123`) | Sub-issues are same-repo only  |
| Loose relationships          | "Related to #X" in body               | Sub-issues imply containment   |
| One-off tasks                | Single issue with labels              | Don't over-structure           |

#### Creating Sub-Issues

```bash
# Create parent issue
gh issue create --title "Research: Range Bar Microstructure" \
  --label "research:parent" --repo terrylica/rangebar-py

# Create sub-issues (reference parent in body or use UI)
gh issue create --title "Regime detection patterns" \
  --body "Parent: #100" --label "research:sub" --repo terrylica/rangebar-py
```

**Structure example**:

```
#100 Research: Range Bar Microstructure (parent)
├── #101 Regime detection patterns - Invalidated ✗
├── #102 Cross-threshold correlations - Validated ✓
├── #103 Duration normalization - In Progress
└── #104 Microstructure features v7.0 - Open
```

#### Sub-Issue Features

- **Progress bar**: Parent shows "X of Y completed" with visual bar
- **Bidirectional links**: Sub shows "Parent issue" in sidebar, parent lists all subs
- **Automatic tracking**: Close sub → parent progress updates
- **Nesting**: Up to 8 levels deep (sub-sub-sub-issues)
- **Limit**: 100 sub-issues per parent

**Migration Note**: Tasklist blocks retired April 30, 2025. Sub-issues are the official replacement. No migration tooling - manual conversion required.

### Status via Labels (No Projects Needed)

Use labels instead of Project custom fields:

| Label Pattern | Purpose                 | Example              |
| ------------- | ----------------------- | -------------------- |
| `status:*`    | Workflow state          | `status:in-progress` |
| `priority:*`  | Urgency                 | `priority:P0`        |
| `research:*`  | Research categorization | `research:validated` |
| `type:*`      | Issue classification    | `type:hypothesis`    |

```bash
# Filter by status
gh issue list --label "status:in-progress" --repo terrylica/rangebar-py

# Filter by research outcome
gh issue list --label "research:validated" --state all

# Combined filters
gh issue list --label "research:regime,status:complete" --state closed
```

### Issue Types (GA 2025)

Organization-level standardization (orgs only, not personal accounts):

```bash
# Configure at: Organization Settings → Issues → Issue Types
# Personal accounts: Use labels instead (type:hypothesis, type:finding)
```

## Projects v2: Visualization Layer (Optional)

Use Projects v2 **only** for cross-repo visualization. All content remains in Issues.

### When to Use Projects v2

| Use Case             | Why Projects v2 Helps                |
| -------------------- | ------------------------------------ |
| Cross-repo dashboard | Single view across multiple repos    |
| Kanban board         | Drag-and-drop visual workflow        |
| Roadmap timeline     | Date-based visual planning           |
| Stakeholder Status   | Status Updates feed (ON_TRACK, etc.) |

### When NOT to Use Projects v2

- Single repo with < 50 issues (use `gh issue list` filters)
- Need edit history (Projects has none)
- Need content storage (use Issue body/comments)
- Need version tracking (Projects loses previous values)

### Auto-Linking Issues to Projects

Link Issues automatically so Projects stay in sync:

**Option 1: Label prefix convention**

| Label              | Auto-links to      |
| ------------------ | ------------------ |
| `project:research` | Research Findings  |
| `project:dev`      | Active Development |

**Option 2: Config file** (`.github/project-links.json`):

```json
{
  "mappings": [
    {
      "labels": ["research:regime", "research:validated"],
      "projectNumber": 2
    }
  ],
  "owner": "terrylica"
}
```

### Status Updates (Stakeholder Communication)

```bash
# Create status update via GraphQL
gh api graphql -f query='
mutation($projectId: ID!, $body: String!, $status: ProjectV2StatusUpdateStatus!) {
  createProjectV2StatusUpdate(input: {
    projectId: $projectId
    body: $body
    startDate: "2026-02-01"
    status: $status
  }) {
    statusUpdate { id status body }
  }
}' -f projectId="PVT_xxx" -f body="Research phase complete" -f status="ON_TRACK"

# Status values: ON_TRACK | AT_RISK | OFF_TRACK | COMPLETE | INACTIVE
```

### Token Requirements

**CRITICAL**: Projects v2 API requires **Classic PAT** with `project` scope.

```bash
# Check token type
cat ~/.claude/.secrets/gh-token-terrylica | head -c 10
# ghp_ = Classic PAT (supports Projects)
# github_pat_ = Fine-grained (NO Projects support)
```

### Project Commands Reference

```bash
# List/create/view projects
gh project list --owner <owner>
gh project create --owner <owner> --title "Dashboard Name"
gh project view <number> --owner <owner>

# Link issues to project (for visualization)
gh project item-add <project-number> --owner <owner> \
  --url https://github.com/<owner>/<repo>/issues/<number>

# Bulk link by label
gh issue list --repo terrylica/rangebar-py \
  --label "research:regime" --json url --jq '.[].url' | \
while read url; do
  gh project item-add 2 --owner terrylica --url "$url"
done
```

## GitHub Issues: Complete Feature Reference

### Core Issue Commands

```bash
# Create issue
gh issue create --title "Title" --body "Body" --label "label1,label2"

# Create with body file (alternative for very long content)
gh issue create --title "Title" --body-file /tmp/issue-body.md

# View issue
gh issue view <number> --repo owner/repo

# List with filters
gh issue list --label "research:validated" --state all --assignee @me

# Edit issue
gh issue edit <number> --add-label "status:complete" --remove-label "status:in-progress"

# Close/reopen
gh issue close <number> --reason completed
gh issue reopen <number>
```

### Advanced Filtering (30+ qualifiers)

```bash
# By multiple labels (AND logic)
gh issue list --label "research:regime,priority:P0"

# By milestone
gh issue list --milestone "Research Phase 1"

# By date
gh issue list --search "created:>2025-01-01 updated:<2025-12-01"

# By author/assignee
gh issue list --author @me --assignee username

# Full-text search
gh issue list --search "microstructure in:title,body"

# Combine everything
gh issue list \
  --label "research:validated" \
  --state closed \
  --search "regime created:>2025-06-01" \
  --json number,title,labels
```

### Issue Relationships

```bash
# Reference in body (creates link in timeline)
"Related to #45"
"Closes #123"
"Fixes #456"

# Cross-repo reference
"See terrylica/other-repo#789"

# Sub-issue (parent reference in body)
"Parent: #100"
```

### Timeline and History

```bash
# View full timeline (all events)
gh api repos/owner/repo/issues/123/timeline --paginate

# View edit history (via web UI or API)
gh api repos/owner/repo/issues/123 --jq '.body_html'

# Comment with preserved history
gh issue comment <number> --body "Update: new findings"
```

### Milestones (Alternative to Project Iterations)

```bash
# List milestones
gh api repos/owner/repo/milestones

# Create milestone
gh api repos/owner/repo/milestones -f title="Research Phase 2" -f due_on="2026-03-01"

# Assign issue to milestone
gh issue edit <number> --milestone "Research Phase 2"
```

## Workflow Examples

### Issues-Only Research Workflow

```bash
# 1. Create parent research issue
gh issue create \
  --title "Research: Range Bar Microstructure Patterns" \
  --label "research:parent,priority:P1" \
  --body-file /tmp/research-parent.md

# 2. Create sub-issues for each investigation
for topic in "regime-detection" "cross-threshold" "duration-normalization"; do
  gh issue create \
    --title "Sub: $topic analysis" \
    --label "research:sub" \
    --body "Parent: #100"
done

# 3. Track progress via labels
gh issue edit 101 --add-label "research:invalidated"
gh issue edit 102 --add-label "research:validated"
gh issue close 101 --reason "not planned"

# 4. Filter to see status
gh issue list --label "research:sub" --state all --json number,title,state,labels
```

### Optional: Add to Project for Visualization

```bash
# Only if you need cross-repo dashboard
gh issue list --label "research:validated" --json url --jq '.[].url' | \
while read url; do
  gh project item-add 2 --owner terrylica --url "$url"
done
```

## Title Evolution: Re-evaluate on New Comments

**PRINCIPLE**: GitHub issue titles have a **256-character limit**. Maximize this limit to create informative titles that reflect the current state of the issue.

### When to Re-evaluate

Re-evaluate and potentially update the issue title when significant new information is added - new findings, status changes, scope expansion, or when the journey is complete.

### Commands

```bash
# Check current title length
gh issue view <number> --json title --jq '.title | length'

# Update title (maximize 256 chars based on content)
gh issue edit <number> --title "..."
```

The AI agent determines the best way to maximize informativeness based on the nature of the content.

## GFM Rendering Anti-Patterns

**NEVER use bare `#N` in issue/PR comments.** GitHub auto-links any `#N` where issue N exists — in prose, tables, lists. This is unpredictable and inconsistent (some numbers link, others don't).

- **To reference an issue**: Use explicit full URL → `[Issue 13](https://github.com/owner/repo/issues/13)`
- **For non-issue numbers**: Suppress with backtick → `` `#1` ``
- **Backslash `\#1` does NOT work** inside table cells

See the full reference for 6 documented anti-patterns: **[GFM Anti-Patterns Reference](./references/gfm-antipatterns.md)**

## Troubleshooting

| Issue                          | Cause                       | Fix                                                                                                                          |
| ------------------------------ | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `#N` auto-links in tables      | GFM auto-reference          | Use backtick code span: `` `#1` `` ([details](./references/gfm-antipatterns.md#ap-01-n-auto-links-to-issues-in-table-cells)) |
| "Resource not accessible"      | Fine-grained PAT            | Use Classic PAT for Projects v2                                                                                              |
| Sub-issues not linking         | Wrong body format           | Use exact "Parent: #123" syntax                                                                                              |
| Labels not filtering correctly | Typo in label name          | `gh label list` to verify exact names                                                                                        |
| Long body truncated            | GitHub 65536-char API limit | Shorten content or split across comments                                                                                     |
| Title too short/vague          | Not using full limit        | Maximize 256-char limit for context                                                                                          |

## References

- [gh-tools Issue Create Skill](../issue-create/SKILL.md)
- [GFM Anti-Patterns](./references/gfm-antipatterns.md)
- [Field Types Reference](./references/field-types.md)
- [Auto-Link Configuration](./references/auto-link-config.md)
- [GraphQL Queries Reference](./references/graphql-queries.md)
- [GitHub Issues Documentation](https://docs.github.com/en/issues)
