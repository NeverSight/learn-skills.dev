---
name: Find Available Slots
description: |
  Find mutual calendar availability between participants and present scheduling options,
  optionally via Slack. Use when someone needs to find meeting times, check availability,
  schedule a call, coordinate calendars, or propose time slots for a meeting.
  Also triggers on "find a time to meet", "when can we meet", "schedule a call with",
  "check availability for", "find open slots", "book a meeting with", "what times work",
  "propose meeting times", "coordinate calendars", or "send scheduling options".
  Do NOT use for rescheduling existing meetings, canceling meetings, or viewing your own
  calendar summary. Do NOT use for setting reminders or creating calendar events directly.
metadata:
  author: sixty-ai
  version: "1"
  category: sales-ai
  skill_type: atomic
  is_active: true
  agent_affinity:
    - pipeline
    - outreach
  triggers:
    - pattern: "find a time to meet"
      intent: "find_availability"
      confidence: 0.90
      examples:
        - "find a time to meet with"
        - "when can we meet"
        - "what times work for a meeting"
    - pattern: "schedule a call with"
      intent: "schedule_call"
      confidence: 0.90
      examples:
        - "book a call with"
        - "set up a meeting with"
        - "schedule a demo with"
    - pattern: "check availability for"
      intent: "check_availability"
      confidence: 0.85
      examples:
        - "check calendar for"
        - "find open slots for"
        - "look at availability"
    - pattern: "propose meeting times"
      intent: "propose_times"
      confidence: 0.85
      examples:
        - "send scheduling options"
        - "send available times"
        - "share time slots via Slack"
    - pattern: "coordinate calendars"
      intent: "coordinate_calendars"
      confidence: 0.80
      examples:
        - "find mutual availability"
        - "overlap our calendars"
        - "when are we both free"
  keywords:
    - "availability"
    - "schedule"
    - "calendar"
    - "time slots"
    - "meeting time"
    - "free slots"
    - "book meeting"
    - "open times"
    - "coordinate"
    - "propose times"
  required_context:
    - participant_name
  inputs:
    - name: participant_name
      type: string
      description: "Name of the person or people to meet with"
      required: true
    - name: meeting_duration
      type: number
      description: "Duration in minutes (default auto-detected from meeting type)"
      required: false
    - name: meeting_type
      type: string
      description: "Type: intro_call, demo, follow_up, deep_dive, check_in, or custom"
      required: false
    - name: urgency
      type: string
      description: "Urgency level: today, this_week, next_week, flexible"
      required: false
    - name: time_preference
      type: string
      description: "Preference: morning, afternoon, any, specific time range"
      required: false
    - name: delivery_channel
      type: string
      description: "How to present options: slack, email, inline, or auto"
      required: false
  outputs:
    - name: available_slots
      type: array
      description: "Ranked list of available time slots with scores and timezone displays"
    - name: slot_message
      type: string
      description: "Formatted message ready for Slack or email with proposed times"
    - name: calendar_invite
      type: object
      description: "Pre-built calendar invite payload for the selected slot"
    - name: scheduling_summary
      type: object
      description: "Summary of constraints applied, slots checked, and conflicts found"
  requires_capabilities:
    - calendar
  priority: high
  tags:
    - sales
    - scheduling
    - calendar
    - availability
    - meetings
    - slack
    - coordination
---

## Available Context
@_platform-references/org-variables.md

# Find Available Slots

You find the best times for people to meet. Not just any open gap on a calendar -- the optimal window that accounts for timezones, energy levels, meeting context, and the rhythm of a sales professional's day. The goal is zero back-and-forth: present three to five strong options that get a "yes" on the first message.

## Context Sources

Before checking a single calendar, gather everything that shapes when this meeting should happen. Scheduling is context-dependent -- a demo for an enterprise prospect is not the same as a quick check-in with an existing client.

### Source 1: Google Calendar API

The primary data source. For each participant whose calendar you can access, retrieve:
- **Existing events** in the target date range (title, start, end, status, attendee count)
- **Working hours** if configured in Google Calendar settings
- **Out-of-office events** and all-day blocks
- **Tentative/maybe events** (treated as soft conflicts -- see references/scheduling-rules.md)
- **Recurring events** that may not show as busy in simple free/busy queries
- **Focus time blocks** (Google Calendar's focus time feature marks these distinctly)

For external participants whose calendars you cannot access, note this limitation and widen the slot window to compensate.

### Source 2: CRM Contact Data

Look up each participant in the CRM to extract:
- **Timezone** from contact record, company record, or last known location
- **Company name and role** (determines meeting type defaults if not specified)
- **Deal stage** (early-stage prospects get different scheduling urgency than closing deals)
- **Last meeting date** (avoid scheduling too soon after a recent touchpoint, or flag urgency if overdue)
- **Communication preferences** noted in CRM (some contacts prefer morning calls, some hate Mondays)
- **Relationship owner** (ensure the right internal team member is included)

### Source 3: User Preferences

Check the requesting user's settings and patterns:
- **Default working hours** and timezone from user profile
- **Buffer preferences** (minimum gap between meetings)
- **Meeting-free blocks** (lunch hours, admin time, personal commitments)
- **Preferred meeting days** for sales calls (most reps prefer Tuesday-Thursday)
- **Video platform preference** (Zoom, Google Meet, Teams) for the invite link

### What to Ask For

After checking all three sources, only ask the user for what you truly cannot infer:
- **Who** -- if the participant name is ambiguous, use the resolve_entity tool
- **Duration** -- if the meeting type is unclear and no default applies
- **Date range** -- if urgency was not specified (default to "this week or next")
- **Internal attendees** -- if the deal has multiple owners or the user might want to include a colleague

Do NOT ask for timezone if it is available in the CRM or calendar. Do NOT ask for duration if the meeting type implies a standard length.

## Step 1: Parse the Scheduling Request

Extract the key parameters from the user's message and fill in defaults from context:

**Who is meeting?**
- Resolve each participant name to a contact record. Use `resolve_entity` for ambiguous first-name-only references.
- Identify their timezone from CRM data, calendar settings, or company HQ location.
- Flag if any participant's timezone is unknown -- you will need to ask or assume.

**How long?**
- If the user specified a duration, use it.
- If they specified a meeting type, apply the default from `references/scheduling-rules.md`:
  - Intro call: 30 minutes
  - Demo: 45 minutes
  - Follow-up: 25 minutes
  - Deep dive / technical review: 60 minutes
  - Quick check-in: 15 minutes
- If neither was specified, infer from deal stage and relationship:
  - First meeting with a new prospect: 30 minutes
  - Active deal, mid-pipeline: 45 minutes
  - Existing client, relationship maintenance: 25 minutes
  - Default fallback: 30 minutes

**What type of meeting?**
- Determines not just duration but also scheduling preferences (demos should not be at 8am, check-ins are fine anytime).
- If the user said "schedule a demo," tag it as demo. If they said "find a time to chat," tag it as check_in.

**How urgent?**
- "Today" -- search remaining hours today only
- "This week" -- search today through Friday
- "Next week" -- search Monday through Friday of the following week
- "Flexible" or unspecified -- search the next 10 business days
- If a deal is in a late stage (negotiation, closing), bias toward sooner slots

## Step 2: Fetch Calendar Data

Query each accessible calendar for the target date range. Apply a buffer of +2 days beyond the range to catch edge-case conflicts.

**For each day in the range:**
1. Retrieve all events between the participant's working hours start and end.
2. Mark each time block as one of:
   - **Hard busy** -- confirmed meetings with 2+ attendees, interviews, client calls
   - **Soft busy** -- tentative events, maybe RSVPs, internal optional meetings
   - **Blocked** -- out-of-office, all-day events, focus time, personal calendar blocks
   - **Free** -- no events in this window

**Working hours determination (in priority order):**
1. Google Calendar configured working hours for the user
2. User preferences in the platform settings
3. CRM timezone + default working hours from `references/scheduling-rules.md`
4. Fallback: 9:00 AM - 5:30 PM in the participant's inferred timezone

**Buffer enforcement:**
- Apply pre-meeting and post-meeting buffers per `references/scheduling-rules.md`
- Default: 15 minutes before and after each existing meeting
- Back-to-back avoidance: if a participant already has 2+ consecutive meetings, add a 30-minute buffer
- Never schedule a meeting that would create a 3+ meeting back-to-back chain

See `references/scheduling-rules.md` for the complete buffer rules and conflict detection logic.

## Step 3: Find Free Slots

With all calendar data loaded and buffers applied, identify candidate slots:

1. **Overlay calendars** -- for each minute in the target range, determine if ALL participants are free. A slot is only valid if every participant with a visible calendar shows as free, and no hard or blocked conflicts exist.

2. **Apply minimum duration** -- a free window must be at least as long as the meeting duration PLUS the configured post-meeting buffer. A 30-minute meeting needs a 45-minute free window (30 + 15 buffer).

3. **Snap to clean boundaries** -- round slot start times to the nearest 15-minute mark. Meetings starting at :07 or :22 feel unprofessional and cause calendar clutter.

4. **Respect working hours** -- no slot should start before the earliest participant's working hours start or end after the latest participant's working hours end. For cross-timezone meetings, find the overlap window per `references/scheduling-rules.md`.

5. **Handle soft conflicts** -- if a tentative or optional meeting overlaps, still include the slot but flag it with a warning: "Note: [Participant] has a tentative event at this time."

6. **External participant handling** -- for participants whose calendars are not accessible, present all slots that work for the accessible participants and note: "Cannot verify [Name]'s availability -- these times work on your end."

**Aim for 5-8 candidate slots** before scoring. If fewer than 3 candidates exist:
- Expand the date range by 3 business days
- Relax buffer rules to 10 minutes (note this in the output)
- Consider early morning or late afternoon slots outside preference but within working hours
- If still fewer than 3, report this clearly and explain the constraints

## Step 4: Score and Rank Slots

Not all free slots are equal. Score each candidate on a 0-100 scale using these weighted factors. See `references/scheduling-rules.md` for the full algorithm and weights.

**Time-of-day preference (25% weight)**
- Morning (9-11 AM in the prospect's timezone): highest score for sales meetings
- Mid-morning to early afternoon (10 AM - 2 PM): strong for demos
- Late afternoon (after 3:30 PM): penalized for first meetings, acceptable for check-ins
- Apply the user's stated time_preference if provided (overrides defaults)

**Day-of-week effectiveness (20% weight)**
- Tuesday, Wednesday, Thursday: highest acceptance rates for B2B sales meetings
- Monday: moderate (people are catching up)
- Friday: lowest (end-of-week energy, higher no-show rates)
- See `references/scheduling-rules.md` for exact scoring by day

**Timezone friendliness (20% weight)**
- Bonus for slots that fall within core hours (10 AM - 3 PM) for ALL participants
- Penalty for slots that are before 9 AM or after 5 PM for any participant
- Heavy penalty for slots outside working hours for the prospect (even if technically allowed)
- Cross-timezone overlap calculation per `references/scheduling-rules.md`

**Calendar density (15% weight)**
- Penalty for days where the user already has 5+ meetings (meeting fatigue)
- Bonus for days with lighter schedules (more energy for important calls)
- Slight penalty if the slot is sandwiched between two other meetings (no breathing room)

**Recency and spacing (10% weight)**
- If the last meeting with this contact was 1-2 days ago, slight penalty (too soon)
- If the last meeting was 7+ days ago, slight bonus (overdue follow-up)
- If the deal is stale (no activity in 14+ days), strong bonus for earliest available slot

**User preference match (10% weight)**
- Bonus if the slot matches the user's stated time_preference
- Bonus if the slot is on a day the user typically takes sales calls
- Bonus if the slot avoids known personal blocks (lunch, school pickup, gym)

**Sort candidates by score descending. Present the top 3-5 slots.**

## Step 5: Format for Presentation

Format the slots based on the delivery channel. The default is inline (in the copilot chat), but if the user asked for Slack or email, format accordingly.

### Inline Format (Chat Response)

Present slots as a clean, scannable list:

```
Here are the best times to meet with [Name]:

1. Tuesday, Feb 17 at 10:00 AM EST (3:00 PM GMT) -- 30 min
   Score: Excellent | Both in core hours, light calendar day

2. Wednesday, Feb 18 at 2:00 PM EST (7:00 PM GMT) -- 30 min
   Score: Good | Mid-week, but later in [Name]'s day

3. Thursday, Feb 19 at 9:30 AM EST (2:30 PM GMT) -- 30 min
   Score: Good | Morning slot, Thursday has high acceptance rates

Want me to send these via Slack, create a calendar invite, or email the options?
```

**Always show dual timezone display** when participants are in different timezones. The user's timezone comes first, the prospect's timezone in parentheses.

**Flag edge cases visually:**
- Early morning for prospect (before 9 AM their time): add a warning icon note
- Late day for prospect (after 5 PM their time): add a warning icon note
- Friday slots: note "Friday -- slightly lower acceptance rates"
- Same-day slots: note "Today -- short notice"

### Slack Format

When delivering via Slack, use Block Kit formatting:

```
Hey [Name], here are a few times that work for a [meeting type]:

* Tue Feb 17, 10:00 AM EST / 3:00 PM GMT (30 min)
* Wed Feb 18, 2:00 PM EST / 7:00 PM GMT (30 min)
* Thu Feb 19, 9:30 AM EST / 2:30 PM GMT (30 min)

Let me know which works best, or suggest another time!
```

Keep Slack messages concise -- no scoring details, no internal notes. The Slack message is prospect-facing. Use a friendly, professional tone that matches the relationship stage.

### Email Format

For email delivery, structure as a short, easy-to-reply message:

```
Subject: A few times for our [meeting type]

Hi [Name],

I'd love to find a time for us to [purpose]. Here are a few options that work on my end:

- Tuesday, February 17 at 10:00 AM EST (3:00 PM your time)
- Wednesday, February 18 at 2:00 PM EST (7:00 PM your time)
- Thursday, February 19 at 9:30 AM EST (2:30 PM your time)

Each would be about [duration]. Do any of these work for you?

If not, feel free to suggest a time -- happy to work around your schedule.

Best,
[User Name]
```

## Step 6: Handle Approval and Next Steps

Once the user selects a slot (or the prospect replies with a preference):

**If creating a calendar invite:**
1. Build the invite payload with:
   - Title: "[Meeting Type] - [User Name] & [Prospect Name]" (or the user's preferred format)
   - Duration: as determined in Step 1
   - Attendees: all participants with their email addresses
   - Video link: generate based on user's preferred platform (Zoom, Google Meet, Teams)
   - Description: brief context from the deal or conversation
   - Reminders: 15 minutes before (default)
2. Present the invite for confirmation before sending (HITL pattern)
3. On confirmation, create the calendar event and notify all parties

**If sending times via email or Slack:**
1. Format the selected options per Step 5
2. Present the draft message for approval
3. On confirmation, send via the selected channel
4. Create a follow-up task to check if the prospect responded within 24 hours

**After scheduling is confirmed:**
- Log the meeting in the CRM as an upcoming activity
- Create a pre-meeting prep task if the meeting is 2+ days away
- Update the deal's last activity date
- If this is a first meeting, suggest running the meeting-prep-brief skill before the call

## Quality Check

Before presenting any scheduling options, verify:

- [ ] All timezones are correctly identified and displayed?
- [ ] Dual timezone format is used when participants span zones?
- [ ] Buffer rules are respected (no back-to-back-to-back chains)?
- [ ] All slots fall within working hours for ALL participants?
- [ ] No slots conflict with hard-busy or blocked events?
- [ ] Soft conflicts (tentative events) are flagged with warnings?
- [ ] Slots are rounded to 15-minute boundaries?
- [ ] The meeting duration includes buffer time in the free window check?
- [ ] Day-of-week scoring is applied (Tue-Thu preferred)?
- [ ] Early morning and late evening slots carry appropriate warnings?
- [ ] The message tone matches the delivery channel (internal vs. prospect-facing)?
- [ ] The user was not asked for information already available in CRM or calendar?

## Error Handling

### "No available slots found"
This happens when calendars are packed or timezone overlap is too narrow. Response approach:
1. Explain the constraint: "Between your schedule and [Name]'s timezone (GMT+8), the overlap window is only 2 hours per day."
2. Offer alternatives: expand date range, suggest shorter meeting duration, consider early/late exceptions.
3. If truly no overlap exists: suggest an async alternative (Loom video, email exchange) and create a task to revisit scheduling in 3 days.

### "Calendar not connected"
The user's Google Calendar integration is not set up or the token has expired.
1. Direct them to Settings > Integrations > Google Calendar to connect.
2. Do NOT attempt to guess availability without calendar data -- offer to find slots manually once connected.
3. If the prospect's calendar is unavailable (external), proceed with the user's calendar only and note the limitation.

### "Timezone unknown for participant"
Cannot determine a participant's timezone from CRM or calendar data.
1. Check the company's headquarters location as a proxy.
2. Check the participant's LinkedIn location if available via enrichment.
3. If still unknown, ask the user: "What timezone is [Name] in? Their CRM record doesn't have a location."
4. Never assume a timezone silently -- incorrect timezone handling destroys scheduling trust.

### "Participant not found in CRM"
The named person does not match any contact record.
1. Use `resolve_entity` to attempt fuzzy matching.
2. If multiple matches, present the options: "I found several contacts named Sarah -- which one? Sarah Chen (Acme Corp) or Sarah Williams (Beta Inc)?"
3. If no matches, ask for the full name and company, then proceed with manual timezone input.

### "Too many participants"
Group scheduling with 4+ people is exponentially harder.
1. For 4-6 participants: widen the date range to 15 business days and relax time-of-day preferences.
2. For 7+ participants: suggest using a scheduling poll tool (Calendly, When2Meet) instead.
3. Always note: "With [N] participants, availability is limited. Consider whether all attendees are required or if some could be optional."

### "Recurring meeting request"
The user wants to find a regular slot (weekly, biweekly).
1. Search for slots that recur consistently across multiple weeks.
2. Check that the slot does not conflict with existing recurring events.
3. Present with a note: "This slot is open for the next 4 weeks" or flag specific weeks where conflicts exist.
4. Suggest booking the first occurrence and setting recurrence, with a note to review conflicts manually.
