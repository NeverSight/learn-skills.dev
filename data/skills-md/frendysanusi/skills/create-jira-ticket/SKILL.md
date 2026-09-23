---
name: create-jira-ticket
description: >-
  Create a well-structured Jira issue from a short brief — turn a title, rough
  notes, a parent/epic, and an assignee into a properly formatted ticket via the
  Atlassian MCP. Use this whenever the user wants to create, file, open, draft,
  or "make a ticket/issue/story/task/bug", log a backlog item, or capture the
  current chat/work as a Jira ticket. Handles description formatting (a default
  section template with an optional Additional Notes, or mirroring a referenced
  template ticket like "use
  PROJ-123's format"), parent/epic linking, assignee resolution, and backlog vs
  sprint placement. Trigger even when the user only says "create a ticket for
  this", names a project key like ABC or PROJ, references a parent such as
  "under PROJ-100", or asks to file something in Jira/Atlassian.
---

# Create a Jira ticket

Turn a rough brief into a clean, well-linked Jira issue. The goal is a ticket a
teammate can pick up cold: a clear title, a skimmable description, correct
parent/type, and the right assignee and placement — created in as few round
trips as possible by reading context up front rather than guessing.

## Step 0 — Load the Jira tools

The Atlassian MCP tools are usually deferred (name known, schema not loaded), so
load the ones you'll need before calling them:

```
ToolSearch("select:mcp__mcp-atlassian__jira_get_issue,mcp__mcp-atlassian__jira_create_issue,mcp__mcp-atlassian__jira_get_user_profile,mcp__mcp-atlassian__jira_assign_issue,mcp__mcp-atlassian__jira_move_issues_to_backlog")
```

Add more only if the task calls for them — `jira_add_issues_to_sprint` (sprint
placement), `jira_get_transitions` + `jira_transition_issue` (move to a specific
status column), `jira_create_issue_link` / `jira_link_to_epic` (linking).

If the `mcp__mcp-atlassian__` prefix doesn't match the connected server, find the
real names with a keyword search like `ToolSearch("jira create issue")`.

## Step 1 — Gather the essentials (ask only for what's missing)

A good ticket needs: **project, summary, issue type, description**, and usually
**parent/epic, assignee, placement**. Pull each from the brief; ask only for
what you genuinely can't infer.

- **Project key** — never guess it blind. But if the user gave a parent, epic,
  or template ticket key (e.g. `PROJ-100`), the prefix (`PROJ`) *is* the project;
  reuse it instead of asking. Only ask when there's nothing to infer from.
- **Summary** — the user's title, tightened if needed.
- **Issue type** — Story / Task / Bug / Epic / Subtask. Often decided by the
  parent (see Step 2). If nothing hints at it, default to `Task` or ask.
- **Description** — the user's rough notes; you'll shape these in Step 3.
- **Parent/epic, assignee, placement** — use whatever the user specified.

## Step 2 — Read context up front (batch these in one turn)

These reads are independent — issue them together so creation happens on the
first try with correct links:

- **Template ticket** (if referenced, e.g. "follow PROJ-123's format"): fetch
  with `jira_get_issue(fields: "description,issuetype,parent")` and copy its
  section structure in Step 3.
- **Parent/epic** (if given): fetch it to confirm it exists and learn its type.
  This drives both the child's type and how you link it:
  - Parent is an **Epic** → child is typically a **Story** (or Task/Bug); link
    with `additional_fields: {"parent": "<EPIC-KEY>"}`.
  - Parent is a **Story/Task** → child is a **Subtask** (`issue_type: "Subtask"`),
    linked via the same `parent` field.
- **Assignee** (if given by email/name): resolve with `jira_get_user_profile`.
  Passing the email straight to create usually works, but confirming the account
  exists avoids a silent misassignment.

## Step 3 — Compose the description

Convert the brief into something skimmable. Preserve the user's own wording and
**keep any links they gave** (Jam/Loom/Confluence URLs, screenshots) — those
carry detail you'd lose by paraphrasing.

**If a template ticket was fetched**, follow *its* section headings and order.
Don't layer the default structure on top — mirroring means matching what's there.

**Otherwise, use this default template** — four core sections plus an optional
Additional Notes. Bake the section number into the bold heading as literal text
(`**1. Title**`); do **not** write it as a Markdown ordered-list marker
(`1. **Title**`). Jira turns each `1.`-prefixed line into its own single-item
ordered list, so the list-marker form renders *every* section as "1." — visibly
false numbering. A number inside the bold text always displays sequentially,
whatever Jira does with lists:

```markdown
**1. Background & Objective**

<why this exists; the problem and the goal>

**2. Current State (As-Is)**

- <how it behaves / is handled today>

**3. Proposed Solution (To-Be)**

- <what should change>

**4. Action Items**

- **<Team/Owner>:** <concrete step>

**5. Additional Notes** *(optional)*

- <links, caveats, context — e.g. "Refer to recording: https://…">
```

The first four sections are the core of the ticket. **Additional Notes is
optional** — include it only when there's genuinely something extra to carry
(links, caveats, an original-request quote); otherwise leave it out rather than
padding it with filler. The same goes for any core section that doesn't apply:
drop it instead of writing a hollow placeholder.

## Step 4 — Create the issue

Call `jira_create_issue` with `project_key`, `summary`, `issue_type`,
`description` (markdown), `assignee` (email is fine), and `additional_fields`
for linking / priority / labels. Examples:

- Link under an Epic (team-managed projects): `{"parent": "PROJ-100"}`
- Link to an Epic (classic projects, if `parent` is rejected): `{"epic_link": "PROJ-7"}`
- Priority: `{"priority": {"name": "Medium"}}`
- Labels: `{"labels": ["backend", "ingestion"]}`

## Step 5 — Placement and assignment check

- **Backlog**: `jira_move_issues_to_backlog(<key>)`. New issues often land there
  by default, but call it explicitly when the user asked for backlog so the
  outcome is unambiguous.
- **Sprint**: `jira_add_issues_to_sprint` — needs a sprint id; find it via the
  board if the user didn't give one.
- **Specific status column** (e.g. "Ready for Dev"): `jira_get_transitions`
  then `jira_transition_issue`.
- **Verify the assignee stuck**: some Jira configs silently drop assignee on
  create. If the created issue comes back Unassigned but one was requested, fix
  it with `jira_assign_issue` (the dedicated endpoint is more reliable).

## Step 6 — Report back

Give the user the key, the browse URL, and a compact summary so they can confirm
at a glance — a small table reads well:

| Field | Value |
|-------|-------|
| Type | Story |
| Parent | PROJ-100 (Epic — …) |
| Assignee | … |
| Status | To Do — moved to backlog |

## Why these steps matter

- **Inferring the project key from a parent prefix** saves a round trip and a
  needless question — but guessing it blind risks filing into the wrong project,
  so only infer when there's a key to infer from.
- **`parent` vs `epic_link`**: modern team-managed projects use `parent` even for
  Epic links; `epic_link` is the classic-project fallback. Try `parent` first.
- **Assignee-on-create is sometimes ignored** by the Jira config, which is why
  Step 5 verifies and falls back to the dedicated assign endpoint.
- **Mirroring means matching**: when the user points at a template ticket, its
  structure is the spec — don't impose the default shape over it.
