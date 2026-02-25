---
name: linear
description: |
  Manage Linear tickets from your AI agent — read, create, update, and triage issues.
  Automatically fetches linked Notion research pages for full design context.

  Use when:
  - User mentions a ticket ID (e.g., "ENG-123")
  - User asks "what's on my board" or "show my tickets"
  - User wants to create a new issue
  - User asks to update ticket status/priority
allowed-tools: Read, Bash(curl:*), mcp__linear__*, mcp__notion__*
---

# Linear Integration

## Purpose

Provide comprehensive Linear ticket management including reading full ticket context (with images), updating status, and creating issues. **Automatically fetches linked Notion research pages** for full design context.

## Defaults

Configure these for your team:

- **Team:** _(your team name)_
- **Assignee:** _(your name)_
- **Status:** Backlog (don't leave in Triage)
- **Ticket prefix:** _(your team prefix, e.g. ENG-xxx)_

## IMPORTANT: Comments & Edits Policy

**NEVER add comments to Linear tickets without explicit user approval.**

- If you want to add a comment, **draft it first** and ask the user to review before posting
- Only update ticket descriptions when the user explicitly approves or provides content to add
- Reading tickets and fetching context is fine — writing/commenting requires permission
- When the user says "update the ticket," ask what specifically they want changed or draft the update for review

## Reading Tickets

When reading a Linear ticket, always extract **maximum context** from both Linear AND Notion:

### Step 1: Fetch Linear Ticket
1. **Fetch the ticket** using `mcp__linear__get_issue`
2. **Check for images** in the description (markdown syntax: `![...](https://uploads.linear.app/...)`), images can also be in attachments so be sure to read those too.
3. **Download and view images** if present - they often contain critical context

### Step 2: Fetch Linked Notion Research (Important for Design Context)

After fetching the Linear ticket, **always check for linked Notion research**:

1. **Search Notion** for a page with matching Linear ID:
   ```
   notion-search(query: "ENG-123", filter: "page")
   ```

2. **If found, fetch the full page content**:
   ```
   notion-fetch(pageId: "<page-id>")
   ```

3. **Download any images** from the Notion page - these are often:
   - UI patterns and references
   - Competitor screenshots
   - Wireframes and mockups
   - Visual inspiration

   **How to extract Notion images:**
   - Look for blocks with `type: "image"` in the page content
   - Image URLs are in `image.file.url` (Notion-hosted) or `image.external.url` (external)
   - Download each: `curl -s -o /tmp/notion-<ticket>-<n>.jpg "<url>"`
   - View with Read tool
   - Note: Notion-hosted URLs expire — re-fetch page if download fails

**Why this matters:** Notion research contains visual references, patterns, and screenshots that inform implementation. The Linear ticket has the PRD/spec; Notion has the design context.

### Notion Database Reference

- **Linear Tasks Database ID**: _(configure your Notion database ID here)_
- Pages have a "Linear ID" property matching the ticket identifier (e.g., "ENG-123")

### Reading Images from Tickets

Linear ticket descriptions often contain screenshots or diagrams. To view them:

```bash
curl -s -o /tmp/linear-<ticket-id>.jpg "<image-url>"
```

Then use the Read tool to view `/tmp/linear-<ticket-id>.jpg`.

**Note:** Linear image URLs have time-limited signature tokens. If a download fails with 401, refetch the ticket to get a fresh URL.

## Updating Tickets

Use `mcp__linear__update_issue` with the ticket ID. Common updates:

| Action           | Field      | Value           |
| ---------------- | ---------- | --------------- |
| Start work       | `state`    | `"In Progress"` |
| Ready for review | `state`    | `"In Review"`   |
| Complete         | `state`    | `"Done"`        |
| Assign to self   | `assignee` | `"me"`          |
| Add labels       | `labels`   | `["FE", "Bug"]` |

## Creating Tickets

Use `mcp__linear__create_issue`. Required fields:

- `title` - Descriptive title
- `team` - Default to Design team

### Issue Structure

```markdown
## Goal
One sentence on what we're trying to achieve.

## [Context Section]
Varies by type: "The Problem", "Why This Matters", "Market Context", etc.

## Scope
What's included - bullets or subsections.

## Considerations (optional)
Constraints, tradeoffs, or context the team needs.

## Deliverables
Tangible outputs - what "done" looks like.
```

### Titles

- Short and scannable
- Noun-based or action-oriented
- No filler words

## Workflow Integration

### Starting Work on a Ticket

1. Fetch the ticket with `mcp__linear__get_issue`
2. Read any attached images for full context
3. Update status to "In Progress"
4. Create/checkout the git branch (use `gitBranchName` from ticket)

### Completing Work

1. Update ticket status to "In Review" when PR is created
2. Link the PR in ticket attachments if not auto-linked

## Available Linear MCP Tools

### Issues

| Tool                              | Purpose                                      |
| --------------------------------- | -------------------------------------------- |
| `mcp__linear__get_issue`          | Fetch ticket details by ID                   |
| `mcp__linear__list_issues`        | Search/filter tickets                        |
| `mcp__linear__create_issue`       | Create new ticket                            |
| `mcp__linear__update_issue`       | Update existing ticket                       |
| `mcp__linear__list_issue_statuses`| List available issue statuses for a team     |
| `mcp__linear__get_issue_status`   | Get details of a specific issue status       |
| `mcp__linear__list_issue_labels`  | List available issue labels                  |
| `mcp__linear__create_issue_label` | Create a new issue label                     |

### Comments

| Tool                           | Purpose                      |
| ------------------------------ | ---------------------------- |
| `mcp__linear__list_comments`   | Get ticket comments          |
| `mcp__linear__create_comment`  | Add comment to ticket        |

### Projects

| Tool                              | Purpose                              |
| --------------------------------- | ------------------------------------ |
| `mcp__linear__get_project`        | Get project details                  |
| `mcp__linear__list_projects`      | List projects in workspace           |
| `mcp__linear__create_project`     | Create a new project                 |
| `mcp__linear__update_project`     | Update an existing project           |
| `mcp__linear__list_project_labels`| List available project labels        |

### Documents

| Tool                            | Purpose                          |
| ------------------------------- | -------------------------------- |
| `mcp__linear__get_document`     | Get document by ID or slug       |
| `mcp__linear__list_documents`   | List documents in workspace      |
| `mcp__linear__create_document`  | Create a new document            |
| `mcp__linear__update_document`  | Update an existing document      |

### Teams & Users

| Tool                        | Purpose                          |
| --------------------------- | -------------------------------- |
| `mcp__linear__list_teams`   | List available teams             |
| `mcp__linear__get_team`     | Get details of a specific team   |
| `mcp__linear__list_users`   | List users in workspace          |
| `mcp__linear__get_user`     | Get details of a specific user   |

### Cycles & Documentation

| Tool                              | Purpose                              |
| --------------------------------- | ------------------------------------ |
| `mcp__linear__list_cycles`        | List cycles for a team               |
| `mcp__linear__search_documentation`| Search Linear's help documentation  |

## Examples

### Read Ticket with Full Context (Linear + Notion)

```
1. mcp__linear__get_issue(id: "ENG-123")
2. Extract image URLs from Linear description
3. curl -s -o /tmp/linear-ENG-123-1.jpg "<linear-image-url>"
4. Read /tmp/linear-ENG-123-1.jpg

5. notion-search(query: "ENG-123", filter: "page")
6. notion-fetch(pageId: "<found-page-id>")
7. Extract image URLs from Notion content
8. curl -s -o /tmp/notion-ENG-123-1.jpg "<notion-image-url>"
9. Read /tmp/notion-ENG-123-1.jpg
```

This gives you:
- **Linear**: PRD, acceptance criteria, ticket status
- **Notion**: Research notes, UI patterns, screenshots, visual references

### Start Working on Ticket

```
1. mcp__linear__get_issue(id: "ENG-123")
2. notion-search(query: "ENG-123") → fetch research if exists
3. mcp__linear__update_issue(id: "ENG-123", state: "In Progress", assignee: "me")
4. git checkout -b feature/eng-123-description
```

## Status Workflow

```
Triage → Backlog → Todo → In Progress → Done
```

- **Triage** - Unsorted, needs review
- **Backlog** - Confirmed, not yet scheduled
- **Todo** - Ready to start
- **In Progress** - Actively working
- **Done** - Shipped
