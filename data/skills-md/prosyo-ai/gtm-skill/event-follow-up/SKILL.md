---
name: event-follow-up
description: "Use this skill when you need to turn a conference, trade show, webinar or roundtable into pipeline: \"follow up with event leads\", \"post-webinar email\", \"trade show follow-up sequence\", \"pre-event outreach to book meetings\". Plans pre-event outreach to book meetings, sorts leads after the event by conversation quality, and writes follow-ups that reference the actual conversation or session, with timing and channel for each lead group."
license: MIT
metadata:
  title: Event follow-up
  category: abm-expansion
  tags: "Marketing, Sales, SDR, Demand Gen"
  author: prosyo
  version: "1.0.0"
  keywords: "trade show follow up email, post webinar follow up, conference lead follow up, claude event follow up skill, pre event outreach"
  inputs: "Event and attendee or lead list, Conversation notes, What was presented"
  outputs: "Pre-event outreach, Lead groups, Follow-up messages by group, Timing plan"
---

Use this around any event. Most event leads go cold because follow-up is slow and generic; a fast follow-up that references the real conversation stands out from every other booth.

## Inputs

- The event, your presence (booth, talk, sponsor, attendee) and dates.
- Lead list with notes: who you spoke with and about what; webinar registrants and attendees.
- What you presented or demoed.

## The play

### 1. Before the event: book meetings
Two to three weeks before, reach target accounts attending: a short email or LinkedIn message with a reason to meet (a specific session, a private demo, a small dinner). Meetings booked before the event beat badge scans after it.

### 2. Sort leads within 24 hours
| Group | Who | Follow-up |
| --- | --- | --- |
| Hot | Real conversation about a live need; asked for a next step | Personal email same or next day, meeting proposal |
| Warm | Good conversation, no clear need yet | Personal email within 2 days, useful resource |
| Session | Attended your talk or webinar | Recording, slides, one insight, soft ask |
| Cold | Badge scan, giveaway, no conversation | Light nurture, not sales outreach |
| Registered, did not attend | Webinar no-shows | Recording plus a 3-bullet summary |

### 3. Reference the conversation
The first line names what you talked about or what they heard: "Good to talk at the booth about your night-shift scheduling problem." Generic "Great to meet you at the event!" emails are indistinguishable from the fifty others in their inbox.

### 4. Time and channel
Hot leads: email plus LinkedIn connection the same day. Warm: within 48 hours. Session and webinar: within 24 hours while it is fresh. Then a short sequence (3 touches over 2 weeks) for each group.

### 5. Measure
Meetings booked per event, pipeline per event, cost per meeting. Badge counts are not results.

## Example (hot lead)

> Subject: night-shift scheduling
>
> Hi Ana, good talking at the booth yesterday about covering night shifts across your three new sites. As promised, here is how Northwind handles cross-site cover; the part on swap approvals is on page 2.
>
> Would Thursday at 10 work for 20 minutes to look at your setup?

## What good looks like

- Hot leads get a personal message within 24 hours.
- Every message references something real from the event.
- Badge-scan-only leads are not sent sales sequences as if they asked for them.
- The common mistake is one mass "thanks for visiting our booth" email to every scan, a week later.

## Rules

- MUST follow up hot leads within 24 hours.
- MUST respect the consent people gave at the event (badge scans and webinar terms differ by event and region).
- NEVER claim a conversation that did not happen.

## Example prompts

- "We had 140 badge scans and 22 real conversations at the summit. Sort them and write the follow-ups."
- "Write pre-event outreach to book meetings with our target accounts attending next month."
- "Write a post-webinar sequence for attendees and no-shows."
