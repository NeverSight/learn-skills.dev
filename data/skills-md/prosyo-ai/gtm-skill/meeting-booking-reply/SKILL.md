---
name: meeting-booking-reply
description: "Use this skill when a prospect shows interest and you need to turn it into a booked, confirmed meeting: \"they said yes, what do I send\", \"book the meeting\", \"write the meeting confirmation\", \"reduce back and forth scheduling\". Writes the booking reply with specific times or a link, the calendar invite title and agenda, the confirmation and the day-before reminder, so the meeting gets booked fast and actually happens. Handles time zones, assistants and multiple attendees."
license: MIT
metadata:
  title: Meeting booking reply
  category: replies-meetings
  tags: "SDR, Founders, Sales"
  author: prosyo
  version: "1.0.0"
  keywords: "book a sales meeting email, meeting confirmation email, calendar invite agenda, claude meeting booking skill, reduce no shows"
  inputs: "The positive reply, Availability or booking link, Meeting purpose"
  outputs: "Booking reply, Calendar invite, Confirmation, Reminder"
---

Use this the moment a prospect says yes. Interest fades fast; every extra email of back and forth loses some meetings, and a vague invite causes no-shows.

## Inputs

- The positive reply and thread.
- Availability (2-3 specific slots) or a booking link.
- Meeting purpose and length; who else should attend.

## The play

### 1. Reply fast with two options
Within the hour if possible. Offer two specific times in their time zone, plus the link as a fallback. Choices beat open questions ("When works for you?").

> Great, Maya. 20 minutes on how your close runs and what Contoso changed. Does Tuesday 10:00 or Wednesday 14:00 (your time) work? If neither, pick any time here: <link>

### 2. Send a calendar invite that sells the meeting
- **Title**: "<Their company> + <Your company>: <topic>" (e.g. "Lumen + Acme: month-end close").
- **Description**: three bullet agenda, what they get from it, the video link, and one line on how to reschedule.
- Their time zone in the invite; never assume.

### 3. Confirm in writing
A short confirmation that restates the outcome they will get, and asks one prep question ("Anything specific you want to cover?") which makes them invest in the meeting.

### 4. Remind the day before
A short, useful reminder: the agenda, a relevant one-line insight, the link. Not "just confirming we're still on".

### 5. Handle edge cases
- **Assistant schedules**: give them two slots and the agenda; copy the prospect.
- **Multiple attendees**: ask who else should join and offer to send them a one-line context.
- **Booked 2+ weeks out**: send one value touch in between (a short story or resource) to keep it alive.

## Templates

**Invite description**
```
What we'll cover (20 min):
- How month-end close runs at Lumen today
- What Contoso changed to close in 4 days
- Whether the same approach fits your team
Need to move it? Reply to this invite and I'll find a new time.
```

**Day-before reminder**
> Hi Maya, looking forward to tomorrow at 10. I'll bring the approval checklist Contoso used. Link: <video link>

## What good looks like

- Booked within one or two emails of the yes.
- Invite title and agenda make the value obvious to anyone who sees the calendar.
- Show rate 80%+ for meetings booked within a week.
- The common mistake is "When works for you?", followed by four emails of scheduling while interest cools.

## Rules

- MUST confirm the time zone explicitly.
- MUST send a calendar invite with an agenda and a working video link.
- NEVER book a meeting the prospect did not agree to.
- NEVER add attendees from their company without asking.

## Example prompts

- "They replied 'sure, let's chat next week'. Write the booking reply."
- "Write a calendar invite and confirmation for a discovery call with a CFO."
- "Our show rate is 60%. Fix our confirmation and reminder emails."
