---
name: update-focus
description: "Update current-focus.md with a structured session summary. Preserves the document's rich structure: weekly focus, session history rotation, open loops, mental state. Use at end of work sessions or when the stop hook nudges."
allowed-tools: Read, Edit, Bash(git log*), Bash(date*), Bash(ls*)
---

# Update Focus Skill

> Structured end-of-session update to `.context/current-focus.md` that preserves the document's full structure.

## Purpose

The stop hook nudges to update `current-focus.md` at session end, but ad-hoc edits risk flattening its rich structure. This skill handles session rotation, open loop management, and targeted questions — so the file stays useful as a working memory between sessions.

## When to Use

- At the end of a work session (triggered by stop hook or manually)
- When the user says "update my focus", "save where I left off", "update current focus"
- After `/session-log` if `current-focus.md` wasn't updated

## Canonical Document Structure

`current-focus.md` follows this structure — **always preserve it**:

```markdown
# Current Focus

> Update this file regularly...

## This Week's Focus (w/c YYYY-MM-DD)

### Primary Goal
[One sentence]

### Active Projects (Top 3)
1. **[Project]** - [Status/phase]
2. **[Project]** - [Status/phase]
3. **[Project]** - [Status/phase]

### Waiting On
- [ ] [Person] - [What] - [Since when]

### Upcoming Deadlines
| Deadline | What | Project |
|----------|------|---------|

## Recent Context

### Last Session Summary (YYYY-MM-DD — [Title])
- [Bullet points of what happened]

### Previous Session (YYYY-MM-DD — [Title])
- [Bullet points]

### Previous Session (YYYY-MM-DD — [Title])
- [Bullet points]

### Previous Session (YYYY-MM-DD — [Title])
- [Bullet points]

### Open Loops
Things I started but haven't finished:
- [ ] [Item]
- [x] [Completed item — remove on next update]

### Mental State
[Optional: How are you feeling about work?]

---

## Quick Reference

### Key Meetings This Week
- [Day]: [Meeting] with [Person] about [Topic]

### Papers in Active Revision
- [Paper title] - [Journal] - [Stage]

---
```

## Workflow

### Step 1: Read current state

Read these three sources to understand what happened:

1. `.context/current-focus.md` — current file contents
2. Latest file in `log/` — most recent session log (if one was created)
3. `git log --oneline -10` — recent commits for concrete evidence of work done

Also note today's date for week rollover detection.

### Step 2: Detect week rollover

Compare the `w/c` date in `## This Week's Focus (w/c YYYY-MM-DD)` against today's date.

- If today is in a **new week** (Monday-based), flag that weekly sections need updating.
- If same week, skip weekly section updates.

Week rollover means: Primary Goal, Active Projects Top 3, Waiting On, Upcoming Deadlines, and Key Meetings may all need refreshing.

### Step 3: Draft session summary

From the session context (conversation history, commits, log), draft a summary in the **same bullet-point format** as existing entries:

```markdown
### Last Session Summary (YYYY-MM-DD — [Short Title])
- [What was done, in bullet points]
- [Key decisions or outputs]
- [Files/commits if relevant]
```

Keep it concise — 3-6 bullet points. Match the style of existing entries.

### Step 4: Ask targeted questions (2-4 max)

Ask only what's needed. Skip questions where the answer is obvious from context.

**Always ask:**
1. "Does this session summary look right?" (show the draft)
2. "Any open loops to add or check off?" (show current list with proposed changes marked)

**Ask only if relevant:**
3. "How are you feeling about work?" — only if Mental State is still a placeholder (`[Optional: ...]`)
4. "Has your primary goal or top 3 changed?" — only on **week rollover**

Present questions concisely with proposed answers. Let the user confirm or adjust.

### Step 5: Apply the update

Use `Edit` to make targeted changes. **Never rewrite the whole file.**

#### Session rotation rules

- **Rename** the current `### Last Session Summary (...)` to `### Previous Session (...)`
- **Insert** the new `### Last Session Summary (...)` in its place
- **Keep a maximum of 4 session entries** in Recent Context (1 Last + 3 Previous)
- If there are already 4 entries, **delete the oldest** Previous Session
- Preserve the exact header format: `### Last Session Summary (YYYY-MM-DD — Title)` for the newest, `### Previous Session (YYYY-MM-DD — Title)` for older ones

#### Open loop management

- **Check off** items that were completed this session (change `- [ ]` to `- [x]`)
- **Remove** items marked `[x]` from previous sessions (they've been acknowledged)
- **Add** new open loops identified during the session
- Keep the intro line: `Things I started but haven't finished:`

#### Other updates

- Update **Mental State** if the user provided one
- Update **weekly sections** if week rollover was detected and the user confirmed changes
- Update **Quick Reference** if meetings or paper revisions changed
- Update **Waiting On** if new blockers emerged or old ones resolved

### Step 6: Confirm

Report what was changed:

```
Updated .context/current-focus.md:
- Session: [title] added to Recent Context
- Open loops: [N checked off, M added]
- [Any other changes]
```

If no session log was created this session, offer: "Want me to run `/session-log` too?"

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `/session-log` | Creates the detailed log; `/update-focus` updates the working memory. Often run together. |
| `/save-context` | For ad-hoc saves to any context file. Defers to `/update-focus` for structured focus updates. |
| `/sync-notion` | Updates `projects/_index.md` and Notion. For full session-level focus updates, defers to `/update-focus`. |

## Example Interaction

**Claude:** Here's what I'd update in `current-focus.md`:

**Session summary:**
```
### Last Session Summary (2026-02-08 — Update Focus Skill)
- Created `/update-focus` skill for structured current-focus.md updates
- Updated stop hook, session-log, and update-context with cross-references
- Updated CLAUDE.md skills list (16 → 17)
```

**Open loops — proposed changes:**
- [x] ~~Commit all pending changes~~ (done this session)
- [ ] Test new skills on CAPE-MOBO or MRes paper *(keep)*
- [ ] Try replication protocol on a real paper *(keep)*
- **New:** [ ] Test `/update-focus` skill end-to-end

Does this look right? Any open loops to add or change?

**the user:** Looks good, also check off the replication one, I decided to skip it.

**Claude:** Got it. *[Applies edits]* Updated `.context/current-focus.md`:
- Session: "Update Focus Skill" added to Recent Context
- Open loops: 2 checked off, 1 added
- Previous sessions rotated (oldest dropped)

Want me to run `/session-log` too?
