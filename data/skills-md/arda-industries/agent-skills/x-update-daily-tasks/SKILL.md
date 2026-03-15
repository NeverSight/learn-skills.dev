---
name: x-update-daily-tasks
description: Refresh obsidian/Timatron/GTD/_DAILY.md for today using Asana tasks (overdue + due today) plus TODOs/topics from recent daily notes.
---

## Goal

Refresh `obsidian/Timatron/GTD/_DAILY.md` for **today (local date)** by pulling:

- Asana tasks assigned to me that are **overdue** or **due today**
- TODOs/topics referenced in the last **14 days** of `obsidian/Timatron/daily/` notes

## File locations

- **Active file**: `obsidian/Timatron/GTD/_DAILY.md` — contains today's section plus persistent sections (Goals, Scratchpad, etc.)
- **Archive file**: `obsidian/Timatron/GTD/_DAILY_archive.md` — stores all previous daily sections
- **Run log**: `obsidian/Timatron/GTD/DAILY_TASK_RUN_LOG.md` — agent memory across sessions

## Step 1 — Read run log for context

Before starting, read `DAILY_TASK_RUN_LOG.md` to retrieve:

- Task-specific notes from prior conversations (e.g., "user said to defer X until March")
- Classification decisions confirmed by user (e.g., "insurance tasks → Personal")
- Pending #CREATE/#POSTPONE actions that were proposed but not yet confirmed
- Any other context that affects today's run

## Step 2 — Archive previous daily sections (preserve other sections)

Before generating today's content:

1. Read `_DAILY.md` and identify:
   - **Daily sections**: Headers matching `## YYYY-MM-DD` pattern (with or without day abbreviation, including `[OLD]` variants)
   - **Persistent sections**: Any other `##` headers (e.g., `## Goals`, `## Scratchpad`) and content before the first daily section
2. **Prepend** only the daily sections to `_DAILY_archive.md` (newest at top)
3. **Keep** persistent sections and any content before the first daily section in `_DAILY.md`

This means `## Goals`, `## Scratchpad`, or freeform notes at the top are preserved across runs.

## Step 3 — Get Asana tasks (assigned to me; any project; overdue or due today)

Hard requirement: **Asana MCP must be available** for this command to work.

- If the Asana MCP server/tools are not available, **throw an error and fail the task immediately** (do not partially update `_DAILY.md`).

Use the Asana MCP tools (server name: `user-asana`):

- Call `asana_get_user` with `user_id="me"` to confirm identity.
- Call `asana_list_workspaces` and pick the correct workspace.
- Fetch tasks assigned to me that are **incomplete only** (never include completed tasks):
  - Due today: `asana_search_tasks` with `assignee_any="me"`, `completed=false`, `due_on=<today YYYY-MM-DD>`
  - Overdue: `asana_search_tasks` with `assignee_any="me"`, `completed=false`, `due_on_before=<today YYYY-MM-DD>`
- Always request `opt_fields`: `name,permalink_url,due_on,projects.name,resource_subtype`
- Deduplicate by task GID (some tasks appear in multiple projects).

## Step 4 — Review last 14 days of daily notes for TODOs/topics

Scan `obsidian/Timatron/daily/` for daily notes within the last 14 days (inclusive).

- Use filenames (e.g. `YYYY-MM-DD.md`) as the date source.
- Read each note and extract explicit and implicit TODOs from the text, plus any important topics to consider.
  - checkbox TODO lines (`- [ ] ...`)
  - explicit "TODO:" / "TODOs" / "Next:" / "Action:" blocks
  - recurring "Topics" sections (capture topic bullets)
- For any extracted item, keep a **source link** back to the daily note using `([[daily/YYYY-MM-DD.md]])` format.

## Step 5 — Scan archive for completed items (deduplication)

Read `_DAILY_archive.md` and scan for checked-off items:

- `- [x] ...` lines indicate completed tasks/topics
- Use these to **omit** the same/similar items from today's fresh list
- If unsure whether an item matches a completed one, include it

## Step 6 — Process #CREATE and #POSTPONE markers

Scan the current `_DAILY.md` (before clearing daily sections) for tasks with markers:

### #POSTPONE markers

Format: `#POSTPONE to DD Mon` or `// #POSTPONE to DD Mon`

For tasks with existing Asana links + #POSTPONE:
1. Parse the new due date from the marker
2. Check current due date in Asana
3. **Add to proposed changes list** — do NOT execute yet

### #CREATE markers

Formats:
- `#CREATE Project > Section, due DD Mon` — create in specified project/section with due date
- `#CREATE Project > Section` — create in specified project/section (will prompt for due date)
- `#CREATE as subtask` — create as subtask of the parent task above

For each #CREATE:
1. Search Asana to check if a task with the same name already exists
   - If found: treat as existing Asana task, plan to add link and remove marker
   - If not found: add to proposed creations list
2. Validate project and section names exist in Asana
   - If close match found (typo): note the correction
   - If not found: note that project/section needs to be created
3. If no due date specified: note that user confirmation of due date is required

### Propose all Asana changes

After scanning, present a **single confirmation prompt** listing:

```
## Proposed Asana Changes

### Tasks to create:
- [ ] "Hang basement hallway mirror" → Favourites > Twin Ponds Projects, due: [NEEDS DATE]
- [ ] "Claim Oxford Health Insurance payment" → Favourites > Finance, due: 2026-02-05

### Due dates to update:
- [ ] "Refresh insurance claims/EOBs" — change due from 2026-01-12 → 2026-02-05

### Notes:
- Section "Finances" not found; did you mean "Finance"?
- Task "Activate free dash pass" already exists in Asana (will link instead of create)

Proceed with these changes? (y/n, or specify modifications)
```

**Wait for explicit user confirmation** before making any Asana API calls.

After confirmation:
- Execute the approved changes via Asana API
- Remove processed markers from tasks
- Add Asana links to newly created tasks

## Step 7 — Deduplicate tasks

Before writing the daily section:

- Identify obviously identical tasks (same text, same Asana GID)
- Dedupe these automatically
- For tasks that might be duplicates but have different markers/dates/details, **ask the user** which to keep

## Step 8 — Classify tasks into Personal / Work / Misc

Classify each task into one of three categories:

### Work
- Technical, business, product, engineering tasks
- Arda-related tasks
- Customer/partner tasks
- Anything explicitly work-related

### Personal
- TimTracker (this is a personal project, not work)
- Home maintenance, family, health, finance
- Relational tasks (calls, scheduling with friends/family)
- Personal errands

### Misc
- Tasks that don't clearly fit Personal or Work
- Productivity/tooling tasks that span both
- When uncertain, default to Misc

Use context from:
- Task content and keywords
- Project names (e.g., "Favourites" → Personal, work project names → Work)
- Run log notes about prior classifications

## Step 9 — Write today's section to `_DAILY.md`

Append today's section after the preserved persistent sections:

### Header format

```
## YYYY-MM-DD Day
```

Example: `## 2026-02-05 Wed`

Always include the three-letter day abbreviation (Mon, Tue, Wed, Thu, Fri, Sat, Sun).

### Section structure

```markdown
## 2026-02-05 Wed

### Personal

#### Asana
##### Favourites (overdue)
- [ ] Task name [Asana](url) due YYYY-MM-DD

##### Favourites
- [ ] Task name [Asana](url) due YYYY-MM-DD

##### No project
- [ ] Task name [Asana](url) due YYYY-MM-DD

#### Notes
- [ ] Task from daily notes ([[daily/2026-01-22.md]])

### Work

#### Asana
##### ProjectName
- [ ] Task name [Asana](url) due YYYY-MM-DD

#### Notes
- [ ] Task from daily notes ([[daily/2026-01-22.md]])

### Misc

- [ ] Task that doesn't fit elsewhere ([[daily/2026-01-22.md]])

### Topics

- [ ] Topic to consider ([[daily/2026-01-22.md]])
```

### Sort order

Within each category (Personal/Work/Misc):
- Asana tasks first, grouped by project
- Overdue tasks before due-today tasks (oldest → newest within overdue)
- Notes-derived tasks after Asana tasks

### Task format

- `- [ ] <taskSentence> [Asana](<permalink_url>) due YYYY-MM-DD` for Asana tasks
- `- [ ] <taskSentence> ([[daily/YYYY-MM-DD.md]])` for notes-derived tasks
- Keep task text short and imperative

## Step 10 — Update run log

Append an entry to `DAILY_TASK_RUN_LOG.md`:

```markdown
## YYYY-MM-DD HH:MM

### Summary
- Asana tasks: X overdue, Y due today
- Notes items: Z extracted from N daily notes
- Created in Asana: [list or "none"]
- Updated in Asana: [list or "none"]

### Classifications confirmed
- [any new classification decisions user confirmed]

### Task-specific notes
- [any notes user provided about specific tasks]

### Pending items
- [any #CREATE/#POSTPONE that were proposed but not confirmed]

### Issues encountered
- [any errors, ambiguities, or items needing follow-up]
```

Keep entries concise. The purpose is to provide context for future runs, not exhaustive logging.

## Summary

After running this command:

- `_DAILY.md` contains persistent sections (Goals, Scratchpad, etc.) plus exactly **one daily section** for today
- Daily section is organized into **Personal / Work / Misc** categories
- All daily sections use `## YYYY-MM-DD Day` format (e.g., `## 2026-02-05 Wed`)
- `_DAILY_archive.md` contains all prior daily sections (prepended, newest first)
- Any #CREATE/#POSTPONE markers have been processed (with user confirmation) and removed
- Completed items in the archive are used for deduplication, not repeated
- Run log updated with session context for future runs
