---
name: daily-digest
description: Use this skill when the user asks for a daily summary, today's to-dos, "what's on my plate today", "daily digest", "daily-digest", "show my notifications", "pending PRs and issues". Requires Gitee MCP Server to be configured.
version: 1.0.0
requires:
  mcp-servers:
    - gitee
---

> **Note**: If you have `mcporter` installed locally, you should use `mcporter` to invoke the MCP tool instead of directly calling the MCP tool. The `mcporter` CLI provides a more convenient interface and better error handling.

# Daily Digest via Gitee MCP

Aggregate unread notifications, pending PRs, and open Issues from Gitee to generate a daily work summary.

## Prerequisites

- Gitee MCP Server configured (tools: `list_user_notifications`, `list_repo_pulls`, `list_repo_issues`, `get_user_info`)
- Optional: user can provide a list of repositories to focus on (otherwise inferred from notifications)

## Steps

### Step 1: Get Current User Info

Use `get_user_info` to retrieve the currently authenticated user's information, used for filtering (e.g., only show tasks assigned to me).

### Step 2: Fetch Unread Notifications

Use `list_user_notifications` to get recent notifications:
- Filter for unread notifications
- Categorize by type: PR-related, Issue-related, @mentions, comment replies

### Step 3: Fetch Pending PRs

For repositories the user cares about (extracted from notifications or specified by the user), use `list_repo_pulls`:
- Filter for `state=open` PRs
- Focus on:
  - PRs assigned to me for review
  - My own PRs waiting for review
  - PRs with new comments that need a reply

### Step 4: Fetch Open Issues

Use `list_repo_issues`:
- Filter for `state=open` Issues assigned to me
- Filter for open Issues I created

### Step 5: Generate Daily Digest

```
# Daily Work Digest
📅 [date]  👤 [username]

---

## 📬 Unread Notifications ([N])

### @Mentions
- [repo] [Issue/PR title] - [notification summary]

### PR Comments
- [repo] PR #N [title] - [comment summary]

### Issue Updates
- [repo] Issue #N [title] - [update summary]

---

## 🔀 Pending PRs

### Needs My Review
| Repo | PR | Author | Updated |
|------|----|--------|---------|
| [repo] | #N [title] | [@author] | [time] |

### My PRs Awaiting Review
| Repo | PR | Status | Updated |
|------|----|--------|---------|
| [repo] | #N [title] | [Awaiting review / Has new comments] | [time] |

---

## 📋 My Open Issues

| Repo | Issue | Priority | Status |
|------|-------|----------|--------|
| [repo] | #N [title] | P1 | In progress |

---

## Today's Suggestions

**Handle first:**
1. [Most urgent item, e.g., a review request blocking someone else]
2. [Second priority item]

**Can defer:**
- [Low priority items]
```

If there is nothing pending:

```
# Daily Work Digest
📅 [date]

All clear! No pending PRs, Issues, or unread notifications.
```

## Notes

- The digest focuses on information aggregation, not deep analysis
- If there are many repositories, prioritize time-sensitive items
- Notifications may span multiple repositories — group them clearly
