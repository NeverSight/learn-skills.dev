---
name: Daily Brief Planner
description: |
  Generate a time-aware daily briefing that adapts to morning, afternoon, or evening.
  Use when a user asks "catch me up", "what's happening today", "give me my daily brief",
  or wants a summary of their schedule, deals, and tasks for the day.
  Returns a scannable briefing with schedule, priority deals, contacts, and tasks.
metadata:
  author: sixty-ai
  version: "2"
  category: sales-ai
  skill_type: atomic
  is_active: true
  context_profile: full
  agent_affinity:
    - pipeline
    - meetings
  triggers:
    - pattern: "daily briefing"
      intent: "daily_brief"
      confidence: 0.85
      examples:
        - "give me my daily briefing"
        - "daily briefing please"
        - "morning briefing"
    - pattern: "what's happening today"
      intent: "daily_summary"
      confidence: 0.85
      examples:
        - "what do I have today"
        - "what's going on today"
        - "today's summary"
    - pattern: "catch me up"
      intent: "catch_up"
      confidence: 0.80
      examples:
        - "catch me up on everything"
        - "give me the rundown"
        - "what did I miss"
    - pattern: "end of day summary"
      intent: "evening_wrap"
      confidence: 0.80
      examples:
        - "wrap up my day"
        - "evening summary"
        - "how did today go"
  keywords:
    - "briefing"
    - "today"
    - "summary"
    - "morning"
    - "afternoon"
    - "evening"
    - "schedule"
    - "rundown"
    - "catch up"
  required_context:
    - company_name
    - meetings
    - deals
    - contacts
    - tasks
    - time_of_day
  inputs:
    - name: date
      type: string
      description: "The date to generate the briefing for in ISO format"
      required: false
      default: "today"
      example: "2025-01-15"
    - name: time_of_day
      type: string
      description: "Time context that determines briefing mode (morning, afternoon, evening)"
      required: false
      example: "morning"
  outputs:
    - name: daily_brief
      type: object
      description: "Structured briefing with greeting, schedule, priority deals, contacts, tasks, and summary"
  requires_capabilities:
    - calendar
    - crm
    - tasks
  priority: high
  tags:
    - sales-ai
    - daily-briefing
    - productivity
---

## Available Context & Tools
@_platform-references/org-variables.md
@_platform-references/capabilities.md

# Daily Brief Planner

## Goal
Generate a **time-aware daily briefing** that gives the sales rep a complete situational picture in 30 seconds or less. The briefing is not a plan (that is the Daily Focus Planner's job) -- it is a **status report** that answers: "Where do I stand right now?"

Research from the Harvard Business Review shows that reps who start with a structured daily overview are 27% more productive and 19% more likely to hit quota, because they avoid the "inbox drift" problem -- reacting to whatever arrives first instead of working strategically.

## Why Daily Briefings Matter

### The Information Asymmetry Problem
Sales reps juggle 15-30 active relationships, 5-15 open deals, and dozens of tasks. Without a structured briefing:
- **41% of selling time** is spent on non-revenue activities (Salesforce State of Sales, 2024)
- Reps check 4-6 tools before their first call, wasting 30-45 minutes each morning
- Critical signals (stale deal, missed follow-up, important meeting today) get buried

### The Briefing Solution
A well-structured briefing compresses 30 minutes of tool-hopping into a 30-second scan. It surfaces:
1. **Time-sensitive items** -- meetings happening today, tasks due today
2. **Risk signals** -- deals going dark, contacts not engaged
3. **Momentum indicators** -- deals advancing, meetings booked, tasks completed

## Time-Aware Mode Design

The briefing adapts its psychology, content, and structure to the time of day. Each mode has a distinct purpose. Consult `references/brief-templates.md` for the full template structure, formatted examples for each mode, and special Monday/Friday templates.

### Morning Mode (before 12pm) -- "Set the Trajectory"

**Psychology**: The rep is fresh, planning-oriented, and open to structure. This is the highest-leverage moment for the briefing because it shapes the entire day's direction.

**Content priorities (in order)**:
1. **Today's schedule** -- Every meeting with time, attendees, linked deal, and a one-line prep note. Meetings are the backbone of a sales day; missing or arriving unprepared to one is the most expensive mistake.
2. **Priority deals snapshot** -- 3-5 deals that need attention today. Selection criteria:
   - Closing this week (urgency)
   - Health score dropped below 60 (risk)
   - No activity in 7+ days (stale)
   - Stage advancement opportunity (momentum)
3. **Contacts needing attention** -- People who haven't been touched in 7+ days and are linked to active deals.
4. **Tasks due today** -- Grouped by priority. Overdue tasks highlighted first.
5. **One-line energy boost** -- A quick summary that sets a positive, focused tone.

**Greeting**: "Good morning! Here's your day at a glance."

### Afternoon Mode (12pm-5pm) -- "Course Correct"

**Psychology**: The rep has been in the field for hours. Energy dips. They need a quick recalibration -- what landed, what slipped, what still needs doing before end of day.

**Content priorities (in order)**:
1. **Progress check** -- Meetings completed, tasks closed, deals updated. Acknowledge momentum. Seeing progress sustains energy (the Progress Principle, Amabile & Kramer).
2. **Remaining schedule** -- Only what is left today. Do not repeat morning meetings.
3. **Unfinished priority actions** -- Tasks or follow-ups that were due by now but remain open. Flag them as "still needs your attention."
4. **Emerging alerts** -- Anything that changed since morning: new meeting invite, deal stage change, contact replied.
5. **Re-prioritized deal list** -- Recalculate based on what happened this morning. A deal that got a positive call this morning drops in urgency; one that was supposed to get a call but didn't rises.

**Greeting**: "Here's your afternoon check-in."

### Evening Mode (after 5pm) -- "Capture and Close"

**Psychology**: The rep is winding down. They want closure on today and a preview of tomorrow so they can mentally detach without anxiety.

**Content priorities (in order)**:
1. **Day summary** -- What got done: meetings held, tasks completed, deals touched. Quantify it ("You had 4 meetings, completed 6 tasks, and moved 2 deals forward").
2. **Wins** -- Any positive signals: deal advanced, meeting booked, proposal sent, reply received. Always lead with wins; it ends the day on a positive note.
3. **Learnings / flags** -- Things that need attention but not tonight: a deal that went dark, a contact who raised a concern, a task that slipped.
4. **Tomorrow preview** -- First 2-3 meetings of tomorrow, any high-priority tasks due tomorrow, and one focus area.
5. **Sign-off** -- A brief, encouraging close.

**Greeting**: "Wrapping up your day. Here's how it went."

## Required Capabilities
- **Calendar**: To fetch today's (and optionally tomorrow's) meetings
- **CRM**: To fetch deal pipeline status, health scores, and contact engagement data
- **Tasks**: To fetch pending, due, and overdue tasks

## Inputs
- `meetings`: from `execute_action("get_meetings_for_period", { period: "today" })` and optionally `{ period: "tomorrow" }` for evening mode
- `deals`: from `execute_action("get_pipeline_deals", { filter: "stale" })` combined with `{ filter: "closing_soon" }`
- `contacts`: from `execute_action("get_contacts_needing_attention", { days_since_contact: 7 })`
- `tasks`: from `execute_action("list_tasks", { filter: "today" })`
- `time_of_day`: "morning" | "afternoon" | "evening" (derived from current time or sequence context)

## Data Gathering Strategy

### Parallel Fetches (all modes)
Execute these simultaneously to minimize latency:
1. `execute_action("get_meetings_for_period", { period: "today" })`
2. `execute_action("get_pipeline_deals", { filter: "closing_soon", period: "this_week", include_health: true, limit: 10 })`
3. `execute_action("get_contacts_needing_attention", { days_since_contact: 7, limit: 10 })`
4. `execute_action("list_tasks", { status: "pending", filter: "today", limit: 15 })`

### Additional Fetches by Mode
- **Evening mode only**: `execute_action("get_meetings_for_period", { period: "tomorrow" })`
- **Afternoon mode**: `execute_action("list_tasks", { status: "completed", filter: "today" })` to show progress

## Priority Deal Selection Methodology

Not all deals deserve a spot in the briefing. Use this scoring to rank. See `references/priority-rules.md` for the complete scoring model with worked examples, tiebreaker rules, and research backing for each weight.

| Signal | Weight | Rationale |
|--------|--------|-----------|
| Closes this week | +40 | Urgency drives action |
| Health score < 60 | +30 | At-risk deals need intervention |
| No activity in 7+ days | +25 | Stale deals die silently |
| Value > 2x average deal | +20 | High-value deals justify extra attention |
| Stage = Negotiation/Proposal | +15 | Late-stage deals are closest to revenue |
| Champion went dark | +35 | Losing your champion is the #1 deal killer |

**Selection rules**:
- Show 3-5 deals maximum. More than 5 creates decision paralysis.
- Always include at least 1 closing-soon deal if any exist.
- If fewer than 3 deals qualify, that is fine -- do not pad with low-priority deals.
- Never show a deal that was updated in the last 24 hours unless it has a meeting today.

## Contact Attention Thresholds

When silence becomes dangerous depends on deal stage. See `references/priority-rules.md` for the full contact priority scoring model and special escalation rules.

| Deal Stage | Days Without Contact Before Alert | Risk Level |
|------------|----------------------------------|------------|
| Discovery / Qualification | 10 days | Medium |
| Demo / Evaluation | 7 days | High |
| Proposal / Negotiation | 5 days | Critical |
| Closed Won (post-sale) | 14 days | Low |
| No active deal | 21 days | Low |

**Special escalation**: If a contact is the identified champion or economic buyer on a deal closing this month, the threshold drops to 3 days.

## Information Density Principles

The briefing must be scannable in 30 seconds. Apply these formatting rules:

### The 3-5-1 Rule
- **3**: Maximum 3 sections visible without scrolling
- **5**: Maximum 5 items per section
- **1**: Each item is 1 line (2 lines maximum for deals with context)

### Hierarchy of Information
Each item follows: **Entity Name** | Key Metric | Action Signal

Examples:
- "Acme Corp ($45K) | Closing Friday | No reply since Tuesday"
- "10:00 AM - Demo with Sarah Chen (Acme) | Deal: $45K Proposal stage"
- "Follow up with James Park | Last contact: 8 days ago | Deal: TechFlow $28K"

### What NOT to Include
- Meeting descriptions (too long, not useful in a scan)
- Full task descriptions (title only)
- Deal history or change log
- Contacts not linked to active deals (unless explicitly stale and valuable)

## Output Contract

Return a SkillResult with `data.daily_brief`:

- `greeting`: string -- time-appropriate opening
- `time_of_day`: "morning" | "afternoon" | "evening"
- `schedule`: array of today's meetings
  - `time`: string (formatted time, e.g., "10:00 AM")
  - `title`: string
  - `attendees`: array of strings
  - `deal_id`: string | null
  - `deal_name`: string | null
  - `prep_note`: string (one-line context, e.g., "Follow up on pricing discussion")
- `priority_deals`: array of 3-5 deals needing attention
  - `id`: string
  - `name`: string
  - `value`: number
  - `stage`: string
  - `days_stale`: number
  - `health_score`: number | null
  - `close_date`: string | null
  - `alert`: string (one-line reason for inclusion)
- `contacts_needing_attention`: array of contacts to follow up with
  - `id`: string
  - `name`: string
  - `company`: string
  - `days_since_contact`: number
  - `linked_deal`: string | null
  - `suggested_action`: string
- `tasks`: array of pending tasks for today
  - `id`: string
  - `title`: string
  - `priority`: "high" | "medium" | "low"
  - `due_date`: string
  - `is_overdue`: boolean
  - `deal_id`: string | null
- `progress`: object (afternoon/evening only)
  - `meetings_completed`: number
  - `tasks_completed`: number
  - `deals_touched`: number
- `tomorrow_preview`: array (evening only) of tomorrow's key meetings/priorities
  - `time`: string
  - `title`: string
  - `deal_name`: string | null
- `summary`: string -- 1-2 sentence summary of the day's status
- `wins`: array of strings (evening only) -- positive signals from today

## Response Formatting

### Morning Example
```
Good morning! Here's your day at a glance.

SCHEDULE (4 meetings)
  09:30  Team standup
  10:00  Demo with Sarah Chen (Acme Corp - $45K Proposal)
  14:00  Discovery call with Mike Ross (NewTech - $28K Qualified)
  16:00  Internal pipeline review

PRIORITY DEALS (3)
  Acme Corp       $45K  Proposal   Closes Friday - no reply since Tue
  TechFlow Inc    $28K  Qualified  Champion went dark (9 days)
  DataBridge      $62K  Negotiation  Contract review pending

CONTACTS TO REACH (2)
  Sarah Chen (Acme)      Last contact: 4 days  Send pricing follow-up
  James Park (TechFlow)  Last contact: 9 days  Re-engage champion

TASKS DUE TODAY (3)
  [!] Send revised proposal to Acme (overdue)
  [ ] Prepare discovery questions for NewTech
  [ ] Update pipeline forecast
```

### Evening Example
```
Wrapping up your day. Here's how it went.

TODAY'S RESULTS
  4 meetings held | 5 tasks completed | 3 deals touched

WINS
  Acme Corp moved to Negotiation stage
  NewTech discovery call went well - demo booked for Thursday

NEEDS ATTENTION (not tonight - tomorrow)
  TechFlow still dark - consider exec sponsor outreach
  DataBridge contract review now 2 days overdue

TOMORROW PREVIEW
  09:00  Follow-up call with Acme Corp
  11:00  Demo prep for NewTech (Thursday)
  14:00  1:1 with sales manager
```

## Quality Checklist

Before returning the briefing, verify:

- [ ] Time mode correctly detected and greeting matches
- [ ] Schedule shows ALL today's meetings (not just the first few)
- [ ] Priority deals limited to 3-5 (never more than 5)
- [ ] Every deal has a clear "alert" reason for inclusion
- [ ] Contacts are linked to active deals (no orphan contacts)
- [ ] Tasks sorted by priority, overdue items flagged
- [ ] No section exceeds 5 items (trim to most important)
- [ ] Each item fits on 1-2 lines maximum
- [ ] Evening mode includes tomorrow preview and wins
- [ ] Afternoon mode shows progress (completed items count)
- [ ] Summary is 1-2 sentences, not a paragraph
- [ ] All entity IDs included for clickable navigation
- [ ] No fabricated data -- if a field is unknown, omit it

## Error Handling

### No meetings today
Show "No meetings scheduled today" in the schedule section. Do NOT skip the section -- the absence of meetings is itself useful information. Suggest: "Good day for focused pipeline work."

### No deals in pipeline
Show "No active deals in pipeline" and shift emphasis to contacts and tasks. If tasks are also empty, provide a gentle prompt: "Your pipeline is clear. Consider prospecting or scheduling discovery calls."

### Partial data (some fetches fail)
Build the briefing with whatever data is available. Clearly note which sections have incomplete data: "Deal health scores unavailable -- showing deals by close date only."

### No tasks due today
Show "No tasks due today" but check for overdue tasks. If overdue tasks exist, surface them with emphasis: "No tasks due today, but 3 tasks are overdue."

### Time of day not provided
Determine from the current timestamp. If timestamp is also unavailable, default to morning mode (the most comprehensive and safest default).

### Very busy day (10+ meetings)
When schedule is overwhelming, group by time block:
- Morning block (before 12pm): X meetings
- Afternoon block (12pm-5pm): Y meetings
Show the top 3 most important (by linked deal value) and summarize the rest.

### Weekend / holiday
If the date is a weekend or known holiday, adjust: "It's Saturday -- here's a quick look at what's coming Monday." Fetch Monday's schedule and this week's carry-over items instead.

### Stale data warning
If the most recent deal update is more than 48 hours old across the entire pipeline, add a note: "Your pipeline data hasn't been updated in 2+ days. Consider reviewing deal stages."
