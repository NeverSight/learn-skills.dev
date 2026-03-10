---
name: project-issues-batch
description: Process all linked issues from a GitHub project and implement them as separate PRs. Use when the user provides a GitHub project URL (github.com/owner/repo/projects/N or github.com/orgs/NAME/projects/N) and wants to implement all issues in that project. Each issue becomes its own PR. Handles dependencies using cascading PRs where dependent issues branch off their dependency's PR branch.
---

# Project Issues Batch

Implement all issues from a GitHub project as separate PRs with dependency-aware ordering.

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status`)
- Git repository with remote configured
- Write access to the repository
- `issue-to-implementation` skill available

## Workflow

Processing a GitHub project involves these phases:

1. **Fetch Issues** - Get all open issues from the project
2. **Analyze Dependencies** - Build dependency graph from issue content
3. **Sort Issues** - Topological sort by dependencies
4. **Process Each Issue** - Delegate to issue-to-implementation skill
5. **Report Progress** - Summary of all implementations

### Phase 1: Fetch Issues

```bash
# Project URL formats:
# - https://github.com/owner/repo/projects/N
# - https://github.com/orgs/ORG/projects/N

# List all items in the project
gh project item-list <PROJECT_NUMBER> --owner <OWNER> --format json

# For each item, check if it's an open Issue (not PR or Draft)
gh issue view <NUMBER> --repo <OWNER/REPO> --json number,title,body,state,labels
```

Filter for:
- Type: `Issue` (exclude `PullRequest`, `DraftIssue`)
- State: `OPEN`

### Phase 2: Analyze Dependencies

Scan issue bodies and comments for dependency patterns:

| Pattern | Example |
|---------|---------|
| Explicit | `Depends on #123` |
| Explicit | `Blocked by #456` |
| Explicit | `Requires #789` |
| Explicit | `After #100` |
| Checkbox | `- [ ] #200` |

Build a dependency graph: `{issue: [dependencies]}`

### Phase 3: Sort Issues

Topological sort to determine implementation order:

1. Issues with no dependencies → process first
2. Issues whose dependencies are completed → process next
3. Repeat until all processed

### Phase 4: Process Each Issue

For each issue in sorted order:

**1. Check for existing PR:**
```bash
gh pr list --repo <OWNER/REPO> --state all --search "fixes #<NUMBER>"
```

**2. If no existing PR, determine base branch:**
- No dependencies → `main`
- Has dependencies → dependency's feature branch

**3. Delegate to issue-to-implementation skill:**
- Reference: `.agents/skills/issue-to-implementation/SKILL.md`
- Pass issue URL and base branch

**4. Create cascading PR if needed:**
```bash
git checkout <dependency-branch>
git checkout -b feat/issue-N-short-desc
# ... implement ...
gh pr create --base <dependency-branch> --title "..."
```

### Phase 5: Report Progress

Provide summary:

```
## Project Implementation Summary

**Implemented (PRs created):**
- #123: Add feature X → PR #456
- #124: Fix bug Y → PR #457 (cascades from #456)

**Skipped (already had PRs):**
- #125: Already has PR #400

**Blocked (dependencies not met):**
- #126: Waiting for #127 (not in project)
```

## Cascading PR Strategy

When issue B depends on issue A:

```
main
  └── feat/issue-A (PR #1)
        └── feat/issue-B (PR #2, base: feat/issue-A)
```

After PR #1 merges:
1. Rebase PR #2 onto main: `git rebase main`
2. Update PR #2's base to main
3. PR #2 ready for review

## Parallel Processing

Issues without dependencies can be processed in parallel. Use the Task tool to spawn multiple agents:

```
Issue A (no deps) ──┬──> Agent 1
Issue B (no deps) ──┼──> Agent 2
Issue C (no deps) ──┴──> Agent 3
```

## Error Handling

| Scenario | Action |
|----------|--------|
| Issue implementation fails | Log error, continue with other issues |
| Dependency not in project | Mark as blocked, report to user |
| Circular dependency detected | Report to user, skip affected issues |

## Reference

For individual issue implementation details, see: `.agents/skills/issue-to-implementation/SKILL.md`

## Success Criteria

- [ ] All open issues from project fetched
- [ ] Dependencies analyzed and sorted
- [ ] Each issue processed (implemented or skipped)
- [ ] Cascading PRs created for dependencies
- [ ] Summary report provided
