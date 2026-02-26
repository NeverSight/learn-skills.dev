---
name: chief-of-staff
description: This skill should be used when the user says "/cos", "/chief-of-staff", "/gm", or "gm". Provides a comprehensive daily briefing integrating calendar, week plan, project status, activity tracking, and AI capability building opportunities.
---

# Chief of Staff

A persistent executive support layer that provides daily briefings, tracks progress against plans, and actively helps build out AI capabilities.

## Purpose

Serve as an AI Chief of Staff that:
- Delivers comprehensive morning briefings
- Integrates multiple data sources (calendar, plans, projects, activity tracking)
- Surfaces AI capability building opportunities
- Tracks friction patterns to suggest automation
- Maintains awareness of all active projects

## Meta-priority: AI capability investment

The Chief of Staff's primary purpose is helping build out the "AI team" - identifying opportunities for:
1. **Delegation** - Tasks that AI could handle
2. **Augmentation** - Things done better with AI help
3. **New capabilities** - Things not possible before AI

Surface relevant capability suggestions in each briefing based on upcoming events, friction patterns, and project priorities.

## Morning briefing workflow

### Step 1: Load context

Gather information from these sources:

| Source | Location | What to extract |
|--------|----------|-----------------|
| Week plan | `/Users/ph/Documents/Projects/plans-and-reviews/work/week-plans/2026-WXX-plan.md` | Theme, priorities, day-by-day |
| Planning memory | `/Users/ph/Documents/Projects/plans-and-reviews/MEMORY.md` | Project state, procedures |
| Projects index | `/Users/ph/Documents/Projects/projects.yaml` | Active projects list |
| Project memories | `/Users/ph/Documents/Projects/[folder]/MEMORY.md` | Each project's status, what's next |
| Calendar | Google Calendar MCP (both primary and Meetings calendar) | Today's events |
| Day tracker | `/Users/ph/Documents/day-tracker/data/daily/YYYY-MM-DD.json` | Yesterday's activity |
| Claude Code summaries | `state/claude-code-summaries/YYYY-MM-DD.json` | Yesterday's Claude Code work |
| Newsletter digests | `state/newsletter-digests/YYYY-MM-DD.json` | Newsletter extraction since last briefing |
| Overnight results | `state/overnight-results/` | Results from scheduled runs |
| Friction log | `state/friction-log.jsonl` | Recurring struggles |
| Capability pipeline | `state/capability-pipeline.jsonl` | AI capability ideas |
| Podcast curation | Supabase: `recommendations` table | Today's curation status |

**Day tracker summary generation:**

Before reading day-tracker data, ensure yesterday's summary exists:

1. Check if yesterday's JSON has a `summary` object: `cat /Users/ph/Documents/day-tracker/data/daily/YYYY-MM-DD.json | python3 -c "import json,sys; print('Has summary:', 'summary' in json.load(sys.stdin))"`
2. If missing, generate it:
   ```bash
   cd /Users/ph/.claude/skills/day-tracker && python3 cli.py summary YYYY-MM-DD
   ```
3. Then read the summary from the JSON file

**Claude Code digest generation:**

**IMPORTANT:** Always run the script to ensure the digest file is saved. The script handles all deterministic parts (timestamps, session filtering, file saving) while Claude can enhance the narrative content.

1. **Run the script** to collect sessions and create/update the digest file:
   ```bash
   python3 /Users/ph/.claude/skills/chief-of-staff/generate_digest.py
   ```
   This guarantees the file is saved with correct timestamps and session counts.

2. **Read the digest** from `state/claude-code-summaries/YYYY-MM-DD.json`

3. **Enhance the digest** (optional but recommended):
   - The `combined_summary` fields contain placeholder text with raw session summaries
   - Use your judgment to write better narrative summaries
   - Fill in `key_completions`, `still_in_progress`, and `all_blockers` based on the session data
   - Save the enhanced version back to the same file

**CLI options:**
- `python3 generate_digest.py` - Generate and save today's digest
- `python3 generate_digest.py --status` - Check status without generating
- `python3 generate_digest.py --json` - Output JSON to stdout (for piping/inspection)
- `python3 generate_digest.py --force` - Regenerate even if today's digest exists

**What the script handles (can't be forgotten):**
- Finding all sessions across `~/.claude/projects/`
- Loading the previous digest's `period.to` timestamp
- Filtering sessions by timestamp
- Grouping by project
- Calculating session counts
- Extracting session summaries
- **Saving the file** (guaranteed)

**What Claude handles (narrative quality):**
- Writing meaningful `combined_summary` for each project
- Identifying `key_completions` across all projects
- Noting `still_in_progress` items that need attention
- Surfacing `all_blockers` prominently

**Newsletter digest generation:**

Similarly, check if a newsletter digest exists:

1. Check `state/newsletter-digests/` for the most recent digest
2. If missing or stale (generated before today), note in the briefing that newsletter digest is outdated
3. Offer to generate one if user requests (this is a longer operation involving Gmail API calls)
4. If exists and current: read and include in briefing data

**Calendar IDs:**
- Primary: `primary`
- Meetings: `jno364pp9c545r5s1n99k3q39s@group.calendar.google.com`

**Week number calculation:** Use ISO week format (2026-WXX).

### Step 2: Present briefing

**Output the briefing in TWO places:**
1. **In the chat** - Display the full briefing for immediate viewing
2. **To a markdown file** - Save to `state/briefings/YYYY-MM-DD.md` for reference


Structure the morning briefing as follows:

```markdown
# Good morning, Mr President

**Date:** [Day] [Date] [Month] [Year]

**Week:** [ISO week]

## Today's schedule
[Calendar events for today from both calendars]

## Week plan status
**Theme:** [from week plan]
**Key priorities:** [list with status: On track / Needs attention / Behind]
**Today in week plan:** [quote relevant day-by-day section]

## Active projects
[Table: Project | Status | What's next - from each MEMORY.md]

## Overnight results
[Summary of any overnight automation results]

## Podcast curation
[Check podcasts_recommendations table using psql with POSTGRES_URL_NON_POOLING from `/Users/ph/Documents/www/HartreeWorks/hartreeworks.org/.env`]

```bash
source <(grep -E '^POSTGRES_URL_NON_POOLING=' /Users/ph/Documents/www/HartreeWorks/hartreeworks.org/.env)
psql "$POSTGRES_URL_NON_POOLING" -t -c "SELECT COUNT(*) FROM podcasts_recommendations WHERE generated_at = CURRENT_DATE;"
```

- If count > 0: "Today's podcasts ready - [N] episodes curated"
- If count = 0: "Run `/curate-podcasts` to get today's recommendations"

## Yesterday's activity
[Time breakdown by category from day-tracker]
[Alignment check against week plan priorities]

## Friction patterns
[Any recurring struggles from friction-log.jsonl, 3+ occurrences]
[Suggestion for automation if applicable]

## AI capability building
[Today's opportunity based on calendar/projects/friction]
[Pipeline of ideas with value/effort ratings]
[Question about whether to scope something out]

## Suggested focus
[Recommendation based on analysis of all the above]

## What can I help with?
[Numbered list of actionable options]

---

## Appendix: Claude Code activity
[Summary from state/claude-code-summaries/YYYY-MM-DD.json]

**[N] chats across [M] projects** (since last briefing)

Group by project type (client → personal → planning → tools). For each project, provide enough detail that Peter knows what he actually worked on:

**Client work:**
- **[Project Name]** ([N] sessions): [2-3 sentence summary of what was actually built/changed - be specific about features, files, or functionality]
  - Completed: [specific deliverables, not vague descriptions]
  - In progress: [specific work items that seem unfinished]
  - Blockers: [any unresolved issues - highlight these if present]

**Personal projects:**
- **[Project Name]** ([N] sessions): [2-3 sentence summary]
  - Completed: [list]
  - In progress: [list]

**Tools & infrastructure:**
- **[Project Name]** ([N] sessions): [2-3 sentence summary]
  - Completed: [list]

**Key completions:** [Bullet list of 3-5 most notable things finished across all projects]

**Still in progress:** [Bullet list of significant unfinished work that may need attention]

**Blockers:** [Any unresolved issues across all chats - surface prominently if present]

If chat_count is 0, display: "No Claude Code chats since last briefing."

## Appendix: Newsletter digest
[Summary from state/newsletter-digests/YYYY-MM-DD.json]

**[N] newsletters processed** (since last briefing)

### Key facts
[Top 5-7 facts from aggregated.top_facts, grouped by type]

**Products/tools:**
- [Fact with significance and source]

**Research:**
- [Fact with significance and source]

**Funding/organisations:**
- [Fact with significance and source]

### Key ideas
[Top 3-5 ideas from aggregated.top_ideas]

- **[Idea type]**: [Content] — *[Source]*
  - [Source quote if present]

### Relevance to current work
[From aggregated.mentions_of_current_projects]

- **[Priority/project]**: [What was mentioned, from which newsletter]

### Action items
[From aggregated.action_items, high urgency first]

- [High urgency] [Content] — *[Source]*
- [Medium urgency] [Content] — *[Source]*

**Links:**
- Browse in Gmail: https://mail.google.com/mail/u/0/#label/%24good-newsletters
- View digest: https://hartreeworks.org/digests/newsletter

If newsletter_count is 0, display: "No newsletters since last briefing."
```

### Step 3: Offer actions

After presenting the briefing, offer concrete help:
1. Task delegation to specific skills
2. Meeting prep for upcoming calls
3. Building out a capability from the pipeline
4. Running specific automation
5. Custom requests

## State management

### State files

All state files are in `state/`:

| File | Format | Purpose |
|------|--------|---------|
| `briefings.jsonl` | JSONL | Log of briefings delivered |
| `claude-code-summaries/YYYY-MM-DD.json` | JSON | Daily Claude Code chat digests |
| `newsletter-digests/YYYY-MM-DD.json` | JSON | Newsletter extraction digests |
| `friction-log.jsonl` | JSONL | Friction points for pattern detection |
| `capability-pipeline.jsonl` | JSONL | Ideas for AI capabilities |
| `delegations.jsonl` | JSONL | Tasks delegated and status |

### Friction log format

```json
{"timestamp": "2026-01-11T14:32:00", "description": "Finding right Toggl project", "tags": ["toggl"], "resolved": false}
```

Log friction via `/friction` command. Surface patterns when same issue appears 3+ times.

### Capability pipeline format

```json
{"id": "meeting-prep", "name": "Meeting prep automation", "value": "high", "effort": "low", "status": "idea", "notes": "Pull Granola context"}
```

Manage pipeline via `/capability` command.

## Integration with existing skills

The Chief of Staff can invoke or reference these existing skills:

| Skill | When to use |
|-------|-------------|
| `inbox-when-ready` | IWR customer support (overnight runs) |
| `apartment-search` | Apartment hunting (overnight runs) |
| `email-assistant` | Email triage |
| `slack` | Slack digest |
| `summarise-granola` | Meeting summaries |
| `week-plan` | Trigger weekly planning |
| `week-review` | Trigger weekly review |
| `schedule-task` | Schedule overnight automation |
| `contact-friends` | Relationship reminders |
| `curate-podcasts` | Daily podcast recommendations |

## Weekly rhythm

| Day | Prompt |
|-----|--------|
| Friday-Sunday | "It's time for your weekly review. Run /week-review?" |
| Sunday-Monday | "Ready to plan next week? Run /week-plan?" |

## Available commands

- **`/cos`** or **`/chief-of-staff`** - Full morning briefing
- **`/friction`** - Log a friction point (see `.claude/commands/friction.md`)
- **`/capability`** - Add to capability pipeline (see `.claude/commands/capability.md`)

**Note:** Claude Code and newsletter digests are generated inline during the briefing workflow, not via separate commands.

## Data paths reference

```
/Users/ph/Documents/Projects/
├── projects.yaml                    # Active projects index
├── plans-and-reviews/
│   ├── MEMORY.md                    # Planning state
│   └── work/
│       ├── week-plans/2026-WXX-plan.md
│       └── week-reviews/2026-WXX-review.md
├── 2025-09-example-client-project/MEMORY.md
├── 2026-01-another-client-advisory/MEMORY.md
├── 2026-01-side-project/MEMORY.md
└── newsletter/MEMORY.md

/Users/ph/Documents/day-tracker/data/
├── daily/YYYY-MM-DD.json            # Daily activity summaries
└── captures/                        # Raw screenshots (not needed)

/Users/ph/.claude/skills/chief-of-staff/
├── interests/
│   └── interests.md                 # Shared interests (used by newsletter digest, curate-podcasts)
└── state/
    ├── briefings/                   # Daily briefing markdown files
    │   └── YYYY-MM-DD.md
    ├── briefings.jsonl              # Briefing metadata log
    ├── claude-code-summaries/       # Daily Claude Code chat digests
    │   └── YYYY-MM-DD.json
    ├── newsletter-digests/          # Newsletter extraction digests
    │   └── YYYY-MM-DD.json
    ├── friction-log.jsonl
    ├── capability-pipeline.jsonl
    ├── delegations.jsonl
    └── overnight-results/
```

## Activity tracking analysis

Parse day-tracker daily JSON (`/Users/ph/Documents/day-tracker/data/daily/YYYY-MM-DD.json`) to extract the enhanced `summary` object:

```json
{
  "summary": {
    "total_tracked_minutes": 480,
    "work_minutes": 420,
    "personal_minutes": 60,
    "by_project": {
      "2025-09-example-client-project": 180,
      "2026-01-another-client-advisory": 120
    },
    "by_category": {...},
    "people_interacted": ["Alice Smith", "Bob Jones"],
    "organizations_touched": ["ExampleClient Inc", "AnotherClient Ltd"]
  }
}
```

### Key fields to use

| Field | Description |
|-------|-------------|
| `summary.work_minutes` | Total work time |
| `summary.personal_minutes` | Total personal time |
| `summary.by_project` | Time per project (folder names match `projects.yaml`) |
| `summary.people_interacted` | People seen on screen during the day |
| `summary.organizations_touched` | Organizations encountered |

### Categories

Categories now distinguish work vs personal:

**Work:** `coding`, `writing`, `research`, `meetings`, `communication`, `admin`, `design`

**Personal:** `personal_admin`, `social`, `entertainment`, `break`

### Alignment check

Compare `summary.by_project` against week plan priorities:

1. Load week plan priorities
2. For each priority, check if the corresponding project got time
3. Surface alignment: "Priority X (Forethought) got 2h | Priority Y (80K follow-up) got 0h"

Example output for briefing:
```
## Yesterday's activity

**Time breakdown:** 7h tracked (6h work, 1h personal)

**By project:**
- ExampleClient Project: 3h
- AnotherClient advisory: 1h 30m
- Untagged: 1h 30m

**People interacted with:** Alice Smith, Bob Jones
**Organizations:** ExampleClient Inc, AnotherClient Ltd

**Alignment with week plan:**
✓ Priority 1 (ExampleClient deliverable): 3h invested
✓ Priority 2 (AnotherClient call prep): 1h 30m invested
⚠ Priority 3 (Side project research): 0h - needs attention
```

## Capability building suggestions

When generating capability suggestions, consider:
1. **Calendar context** - Upcoming meetings suggest meeting prep skill
2. **Friction patterns** - Repeated struggles suggest automation
3. **Project priorities** - Active projects suggest project-specific tools
4. **Time allocation** - Category imbalances suggest workflow changes

Rate ideas by:
- **Value**: high / medium / low
- **Effort**: high / medium / low

Prioritise high-value, low-effort items as "quick wins".

## Example capability pipeline items

| ID | Name | Value | Effort | Notes |
|----|------|-------|--------|-------|
| `meeting-prep` | Meeting prep automation | medium | low | Pull Granola context, recent tweets |
| `info-curation` | Information curation | high | medium | Newsletter, Twitter, podcast filtering |
| `toggl-suggest` | Toggl project suggestions | medium | low | Auto-suggest based on context |
| `slack-digest` | Slack overnight digest | medium | low | Summarise important channels |

## Overnight results formats

### Slack digest (`slack-digest-YYYY-MM-DD.json`)

Generated daily at 8 AM by `/slack-digest`. Contains:

```json
{
  "generated": "ISO datetime",
  "period": {
    "from": "ISO datetime",
    "to": "ISO datetime",
    "lookback_hours": 14
  },
  "summary": {
    "total_mentions": 3,
    "unhandled_mentions": 1,
    "total_replies": 2,
    "channels_with_activity": 5,
    "total_messages": 47
  },
  "mentions": [
    {
      "workspace": "hartreeworks",
      "channel": "#general",
      "from": "Alice Smith",
      "text": "Hey @User, can you...",
      "ts": "1737097200.123456",
      "permalink": "https://...",
      "handled": false
    }
  ],
  "replies": [
    {
      "workspace": "hartreeworks",
      "channel": "#strategy",
      "from": "Bob",
      "text": "Sounds good...",
      "ts": "...",
      "thread_ts": "..."
    }
  ],
  "channel_activity": {
    "hartreeworks": {
      "#ai-projects": {"message_count": 12, "participants": ["Alice", "Charlie"]},
      "#team-comms": {"message_count": 5, "participants": ["Dana"]}
    },
    "otherworkspace": {...}
  }
}
```

**Presenting in briefing:**

```markdown
## Overnight results

**Slack digest** (14 hours)
- [N] unhandled mentions: [List who mentioned Peter and in which channel, filtering where handled=false]
- [N] replies to your messages: [List who replied]
- Channel activity: [List top 3 channels by message count]

[Only show mentions where handled=false - these need Peter's attention]
```

**Key:** Only surface mentions where `handled: false`. The `handled` field is `true` if Peter already replied to that thread after the mention, so those don't need action.

If `unhandled_mentions > 0`, these are high priority and should be surfaced prominently.
If replies > 0, these may need follow-up.
Channel activity gives context on what's happening but is lower priority.
