---
name: Slack History Query
namespace: slack
description: |
  Show activity history, meeting timeline, and past interactions from Slack DM.
  Use when a Slack user asks when they last spoke to someone, wants to see recent
  meetings, asks about their calendar this week or next week, or wants a timeline
  of interactions with a contact or company. Returns meeting summaries and activity
  timeline as Slack Block Kit cards.
metadata:
  author: sixty-ai
  version: "1"
  category: slack-copilot
  skill_type: atomic
  is_active: true
  context_profile: sales
  agent_affinity:
    - slack
  triggers:
    - pattern: "when did I last talk to [name]"
      intent: "last_interaction"
      confidence: 0.92
      examples:
        - "when did I last talk to Sarah Chen?"
        - "when did I last speak to John at Acme?"
        - "when did I last meet with GlobalTech?"
    - pattern: "show my meetings this week"
      intent: "meeting_schedule"
      confidence: 0.88
      examples:
        - "show me my meetings this week"
        - "what meetings do I have today?"
        - "show my calendar for tomorrow"
        - "upcoming meetings"
        - "meetings next week"
    - pattern: "recent activity"
      intent: "activity_history"
      confidence: 0.80
      examples:
        - "show recent activity"
        - "what have I been doing this week?"
        - "show my activity log"
        - "what's happened recently?"
    - pattern: "last meeting"
      intent: "last_meeting"
      confidence: 0.85
      examples:
        - "when was my last meeting with Acme?"
        - "what was the last call with Sarah?"
        - "last time I talked to them"
  keywords:
    - "when did"
    - "last time"
    - "last meeting"
    - "last call"
    - "last email"
    - "history"
    - "talked to"
    - "spoke to"
    - "spoke with"
    - "met with"
    - "meetings this week"
    - "meetings today"
    - "calendar"
    - "schedule"
    - "upcoming"
    - "recent"
  required_context:
    - slack_user_id
  inputs:
    - name: contact_name
      type: string
      description: "Person name if asking about a specific contact's history"
      required: false
    - name: is_schedule_query
      type: boolean
      description: "Whether asking about upcoming meetings vs past history"
      required: false
      default: false
    - name: raw_query
      type: string
      description: "The original Slack message text"
      required: true
  outputs:
    - name: slack_blocks
      type: array
      description: "Slack Block Kit blocks to render in the DM response"
    - name: text
      type: string
      description: "Fallback plain text if blocks are unavailable"
  requires_capabilities:
    - crm
  priority: high
  tags:
    - slack
    - history
    - meetings
    - activity
    - timeline
---

## Available Context & Tools
@_platform-references/org-variables.md
@_platform-references/capabilities.md

# Slack History Query

## Goal
Answer "when did I last…" and "show my meetings…" questions from Slack with a clean timeline view. Context matters — people ask these questions when preparing for calls or catch-ups.

## Intent Patterns

### Last Interaction with a Contact
Triggered when `contact_name` is extracted from the message.

1. Search contacts by name (partial match, case-insensitive)
2. Search recent meetings where title or summary mentions the contact name
3. Show contact profile header + last meeting details

**Response format**:
- Section: `*Full Name* — Title at Company` (if contact found in CRM)
- Section: `*Last Meeting:* Meeting Title — Day, Mon DD`
- Section (italic): truncated meeting summary (max 300 chars)
- Context: "N more meetings in the past week" (if applicable)
- Divider + link to full contact profile

**No interaction found**: "I couldn't find any recent interactions with [name]. Check the name or try their full name."

### Meeting Schedule Query
Triggered when message contains: "meetings this week", "meetings today", "meetings tomorrow", "upcoming meetings", "next week"

1. Fetch meetings for the relevant time window
2. Filter for upcoming (future) vs. this week (all)
3. Show list of up to 8 meetings with time and attendee count

**Response format**:
- Header: "Upcoming Meetings (N)" or "This Week's Meetings (N)"
- Bullet list: `• *Meeting Title* — Tue, Jan 15 2:30 PM (N attendees)`
- Context: "N more. View calendar" link if >8 meetings

**No meetings**: "No upcoming meetings scheduled." or "No meetings found this week."

### General Recent Activity
Triggered when no specific contact is named and not a schedule query.

1. Fetch last 5 meetings + last 5 activities from the past 7 days
2. Merge and sort by date descending
3. Show unified timeline

**Response format**:
- Section: "Recent Activity (Past 7 Days):"
- Bullet list (up to 8 items):
  - Meetings: `:calendar: *Meeting Title* — Tue, Jan 15`
  - Activities: `:clipboard: Activity Type — Subject — Jan 15`

**No activity**: "No recent activity found this week."

## Data Sources

- **Meetings**: `execute_action("list_meetings", { owner: slack_user_id, days_back: 7 })`
- **Contacts**: `execute_action("search_contacts", { query: contact_name })`
- **Activities**: `execute_action("list_activities", { owner: slack_user_id, days_back: 7 })`

## Date Formatting

- Meeting dates: `new Date(start_time).toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' })`
- Schedule view: include time — `{ weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }`
- Activity dates: short format — `Mon Jan 15`

## Response Constraints

- Maximum 8 items in any timeline/list view
- Meeting summaries: truncate to 300 characters
- Attendee count: show as "(N attendees)" not raw number
- Sort all timeline items by date descending (most recent first)
- For upcoming meetings filter: use `start_time > now` comparison
- Always include link to `/calendar` for schedule queries

## Error Cases

- **No meetings in period**: Context-appropriate plain text ("No meetings found this week." vs "No upcoming meetings scheduled.")
- **Contact not in CRM**: Show meeting history anyway if meetings mention the name, without the contact profile block
- **No activities or meetings**: "No recent activity found this week."
