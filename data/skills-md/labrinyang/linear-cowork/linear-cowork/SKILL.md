---
name: linear-cowork
description: Use when working on any project that uses Linear for issue tracking, or when the user mentions Linear issues, tickets, creating issues, updating issue status, linking commits to issues, or any Linear MCP interaction. Always activate this skill for issue creation, status updates, commit workflows, and project organization in Linear.
---

# Linear Cowork

Standardized Linear collaboration workflow for vibe coding teams.

## MCP Setup

Before using this skill, ensure the Linear MCP server is installed and authenticated.

**Quick setup for Claude Code:**
```bash
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

**Quick setup for Codex:**
```bash
codex mcp add linear --url https://mcp.linear.app/mcp
```

For Cursor setup and detailed instructions for all tools, see `setup-guide.md` in this skill directory.

## Issue Conventions

### Naming Rule

All issue titles MUST follow this format:

```
[Type] Short description
```

**Valid types:**

| Type | When to use |
|------|-------------|
| `[Feature]` | New functionality |
| `[Bug]` | Bug fix |
| `[Chore]` | Maintenance, dependencies, config |
| `[Refactor]` | Code restructuring without behavior change |
| `[Docs]` | Documentation changes |

**Examples:**
- `[Feature] Add OAuth login flow`
- `[Bug] Fix crash on empty cart submission`
- `[Chore] Upgrade React to v19`

**Bad examples (DO NOT use):**
- `add login` — missing type prefix
- `[Feature] Login` — too vague, not descriptive
- `Feature: add login` — wrong format, must use brackets

### Description Template

Every issue description MUST include these two sections:

```markdown
## Background
[Why this issue exists. What problem it solves. Any relevant context.]

## Acceptance Criteria
- [ ] [Specific, testable criterion]
- [ ] [Another criterion]
```

**Do not skip Acceptance Criteria.** Even for small tasks, at least one criterion is required.

## Workflow Rules

### Default Assignment

When creating an issue via the Linear MCP, **always assign it to "me"** (the current authenticated user) unless the user explicitly specifies a different assignee.

### Issue Status Lifecycle

Linear issues have 6 statuses. **Proactively update issue status** as the user's work progresses:

| Status | Type | When to use |
|--------|------|-------------|
| **Backlog** | backlog | Unplanned — collected but not yet confirmed |
| **Todo** | unstarted | Confirmed and ready to be worked on |
| **In Progress** | started | Actively being worked on |
| **Done** | completed | Work finished and verified |
| **Canceled** | canceled | Will not be done |
| **Duplicate** | canceled | Already covered by another issue |

**Status transition rules:**

```
Backlog → Todo → In Progress → Done
                              → Canceled
                              → Duplicate
```

- **Creating an issue**: Set to **Todo** (not Backlog) unless user specifies otherwise
- **User starts working on an issue**: Update to **In Progress**
- **Committing code for an issue**: Update to **Done**
- **User says to cancel/skip**: Update to **Canceled**
- **User identifies a duplicate**: Update to **Duplicate**

**Proactive status updates:** When context makes it obvious (e.g., user says "I'm working on ONE-42" or "let's start ONE-42"), update the status to In Progress without needing to be asked. Similarly, when committing code linked to an issue, update to Done automatically.

### Labels

Every issue MUST have a label. Choose based on the issue type:

| Label | Color | When to use |
|-------|-------|-------------|
| **Feature** | purple | New functionality (`[Feature]` issues) |
| **Bug** | red | Bug fixes (`[Bug]` issues) |
| **Improvement** | blue | Enhancements, refactors, chores, docs (`[Refactor]`, `[Chore]`, `[Docs]` issues) |

**Mapping from issue type to label:**

| Issue Type | Label |
|------------|-------|
| `[Feature]` | Feature |
| `[Bug]` | Bug |
| `[Chore]` | Improvement |
| `[Refactor]` | Improvement |
| `[Docs]` | Improvement |

Apply the label automatically when creating an issue — do not ask the user unless the mapping is ambiguous.

### Priority

Every issue MUST have a priority set. **Default to Medium (3)** unless the user specifies otherwise.

| Value | Level | When to use |
|-------|-------|-------------|
| 0 | No priority | Never use as default |
| 1 | Urgent | Production down, data loss, security vulnerability |
| 2 | High | Blocks other work, major user-facing issue |
| 3 | **Medium** | **Default** — standard feature work, normal bugs |
| 4 | Low | Nice-to-have, minor polish, tech debt |

### Subagent Strategy

Use different models for different tasks to balance cost and quality:

| Task | Model | Why |
|------|-------|-----|
| Read from Linear (list issues, get details) | Haiku subagent | Cheap, fast, repetitive |
| Write to Linear (create/update issues, comments) | Haiku subagent | Simple API calls |
| Explore codebase for issue context | Explore subagent | Efficient file search |
| Draft issue content (title, description, criteria) | **Main model** | Requires quality writing |

**Issue creation workflow:**

```
1. Haiku    → Read Linear (check existing issues, projects, team context)
2. Explore  → Search codebase if needed (understand context for the issue)
3. Main     → Draft issue title, description, and acceptance criteria
4. Preview  → Show draft to user for confirmation
5. Haiku    → Submit to Linear after user approves
```

**Issue update workflow:**

```
1. Haiku    → Read current issue state from Linear
2. Main     → Determine changes needed (may explore codebase if needed)
3. Preview  → Show changes to user for confirmation (if content changes)
4. Haiku    → Apply updates to Linear
```

**Key rules:**
- **Always preview issue content before submission.** Show the user the full title, description, labels, priority, and status before creating or making content changes.
- Status-only updates (e.g., Todo → In Progress) do NOT need preview — apply directly.
- Simple reads and writes go through Haiku to save context tokens.
- Content that users will see (titles, descriptions, criteria) must be drafted by the main model for quality.

### Project Organization

- Use Linear **Projects** to group related issues by feature area or milestone
- Before creating issues, check if a relevant project exists
- If no project exists and the work spans 3+ issues, create a project first

## Pre-commit Checklist

**Before every commit, follow this flow:**

```
About to commit?
  ├─ Related to Linear issue?
  │   ├─ Unknown → Ask user for issue ID
  │   │   ├─ User confirms → Update status to completed, include ID in commit
  │   │   └─ No issue → Proceed with commit
  │   ├─ Yes, known → Update status to completed, include ID in commit
  │   └─ No → Proceed with commit
```

**Steps:**

1. Before committing, ask: *"Is this commit related to a Linear issue? If so, which one (e.g., ONE-123)?"*
2. If user provides an issue ID:
   - Use a **subagent** to update the issue status to **Done**
   - Include the issue ID in the commit message, e.g.: `[ONE-123] Fix cart crash on empty submission`
3. If user says no issue is related, proceed with the commit normally.

### Commit Message Format with Issue ID

```
[ISSUE-ID] commit message

# Examples:
[ONE-42] Add OAuth login flow
[ONE-15] Fix crash on empty cart submission
```

## Quick Reference

| Action | Rule |
|--------|------|
| Issue title | `[Type] Short description` |
| Issue description | Background + Acceptance Criteria sections |
| Assign issue | Default to "me" unless user specifies otherwise |
| Label | Auto-apply: Feature / Bug / Improvement based on issue type |
| Priority | Default to Medium (3) unless user specifies otherwise |
| New issue status | Default to "Todo" |
| Start working | Update to "In Progress" |
| Commit linked to issue | Update to "Done" |
| Read/write Linear | Haiku subagent |
| Draft issue content | Main model, then preview before submit |
| Before commit | Confirm issue ID, update status to completed |
| Commit message | `[ISSUE-ID] message` |
| Multiple related issues | Group under a Project |
