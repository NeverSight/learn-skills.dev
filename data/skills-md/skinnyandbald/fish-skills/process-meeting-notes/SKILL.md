---
name: process-meeting-notes
description: "Process Fireflies meeting transcripts to extract action items, create GitHub issues, compare against existing work, and generate EOS Level 10 Meeting summaries. Use after team meetings or when the user mentions meetings, Fireflies, L10, or action item extraction."
---

<essential_principles>
## How This Skill Works

This skill processes meeting transcripts from Fireflies and converts them into actionable GitHub issues with EOS Level 10 Meeting documentation. It works with **any repository** you're currently in.

### Principle 1: Fireflies-First Data Retrieval

Always fetch meeting data via Fireflies MCP tools:
- `mcp__fireflies__fireflies_search` to find meetings
- `mcp__fireflies__fireflies_get_summary` for action items, keywords, overview
- `mcp__fireflies__fireflies_get_transcript` for detailed context when needed

### Principle 2: Dynamic Repository Context

At workflow start, detect the current repository:
- Repository owner and name via `gh repo view`
- Available labels via `gh label list`
- Available milestones via GitHub API
- GitHub Projects (if any exist)

**Never hardcode repo-specific values.** Always detect dynamically.

### Principle 3: Compare Before Creating

Before creating new GitHub issues:
1. Search existing issues in the **current repository** for potential duplicates
2. Check against project milestones (whatever naming convention the repo uses)
3. If related issue exists, suggest commenting/updating rather than duplicating

### Principle 4: Prompt for Confirmation

For each potential GitHub issue:
- Show extracted action item
- Display suggested labels (from detected available labels)
- Ask user to confirm/modify before creation
- Never auto-assign (leave unassigned)

### Principle 5: EOS Level 10 Format

All meeting summaries follow the Level 10 Meeting structure:
- Clear accountability (WHO is responsible)
- Specific deliverables (WHAT is agreed)
- Time-bound commitments (WHEN is the deadline)
</essential_principles>

<intake>
What would you like to do?

1. **Process recent meeting** - Analyze the most recent Fireflies meeting and extract action items
2. **Search specific meeting** - Find a meeting by date, keyword, or participant
3. **Create issues from notes** - I already have meeting notes to convert to GitHub issues
4. **Generate L10 summary only** - Create EOS Level 10 summary without creating issues

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "recent", "latest", "today" | `workflows/process-recent-meeting.md` |
| 2, "search", "find", "specific" | `workflows/search-meeting.md` |
| 3, "create", "notes", "issues" | `workflows/create-issues-from-notes.md` |
| 4, "summary", "L10", "EOS" | `workflows/generate-l10-summary.md` |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
All domain knowledge in `references/`:

**EOS Framework:** eos-level-10-format.md
**GitHub Integration:** github-project-config.md (dynamic detection patterns)
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| process-recent-meeting.md | Full workflow: detect context → fetch → compare → create issues → L10 summary |
| search-meeting.md | Find specific meeting by criteria |
| create-issues-from-notes.md | Convert provided notes to GitHub issues |
| generate-l10-summary.md | Create L10 summary from existing analysis |
</workflows_index>

<templates_index>
| Template | Purpose |
|----------|---------|
| l10-meeting-summary.md | EOS Level 10 Meeting summary structure |
| github-issue-checklist.md | Issue body with implementation checklist |
</templates_index>
