---
name: no-show-recovery
description: "Use this skill when a prospect misses a booked meeting or keeps rescheduling: \"they didn't show up\", \"no-show follow-up email\", \"how to rebook a no-show\", \"reduce no-shows\". Writes the same-day no-show sequence (gracious message, rebooking options, value touch, close the loop), sets the timing across email, phone and LinkedIn, and diagnoses why no-shows happen so the booking process can be fixed."
license: MIT
metadata:
  title: No-show recovery
  category: replies-meetings
  tags: "SDR, Sales, Founders"
  author: prosyo
  version: "1.0.0"
  keywords: "no show follow up email, missed meeting email, rebook no show prospects, claude no show skill, reduce meeting no shows"
  inputs: "Missed meeting details, How it was booked, Thread history"
  outputs: "No-show sequence, Rebooking message, Diagnosis and fixes"
---

Use this when a meeting is missed. Most no-shows are not rejections: calendars collide, days get away. A gracious, fast follow-up rebooks a large share of them.

## Inputs

- Meeting details: who, when, purpose, how it was booked.
- The thread before the meeting.
- How many times they have rescheduled already.

## The play

### 1. Wait five to ten minutes, then reach out once
At five minutes past: a short email ("I'm on the line; no worries if today got away from you"). If the person's phone number is known and calling is appropriate, one call.

### 2. Same day: rebook without guilt
> Hi Maya, no problem at all about today. I know how quarter-end weeks go. Would Thursday 10:00 or Friday 14:00 work instead? Or pick any time here: <link>

### 3. Day 2-3: add value
If no answer, send something useful tied to the meeting topic (the checklist, the short customer story), plus the link.

### 4. Day 6-7: close the loop
> Hi Maya, I'll take this off my list for now. If month-end close gets back on the agenda, reply "close" and I'll send times.

Optionally, one LinkedIn message between steps 3 and 4 if connected.

### 5. Second no-show
After two missed meetings, do not offer a third slot directly. Ask whether the topic is still a priority; if yes, ask them to pick a time.

### 6. Diagnose patterns
| Pattern | Likely cause | Fix |
| --- | --- | --- |
| No-shows on meetings booked 2+ weeks out | Interest fades | Book within 7 days; add a value touch in between |
| No-shows after links with no agenda | Unclear value | Agenda in invite; confirmation with a prep question |
| High no-shows from one campaign | Weak qualification or a pushy ask | Fix the ask; qualify before booking |
| No-shows at certain times | Time zone errors, Monday mornings, Friday afternoons | Confirm zones; avoid those slots |

## What good looks like

- First message within 15 minutes of the missed start time.
- Rebook rate of 30-50% on first-time no-shows.
- The common mistake is the passive-aggressive "Sorry we missed you, I waited 15 minutes", which makes rebooking awkward.

## Rules

- MUST keep the tone gracious, every time.
- MUST stop after the close-the-loop message unless they reply.
- NEVER charge, threaten or shame a no-show.
- NEVER escalate to their manager because they missed a sales meeting.

## Example prompts

- "My 2pm with the VP of Ops didn't show. Write the follow-up sequence."
- "This prospect has rescheduled twice. What now?"
- "Our no-show rate is 35%. Diagnose and fix our booking process."
