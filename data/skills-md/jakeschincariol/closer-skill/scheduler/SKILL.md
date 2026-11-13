---
name: scheduler
description: >-
  Scheduler. Puts every booked call on your calendar. Reads a reply like "Thursday at 2 works" and
  turns it into the right date and time, checks your calendar for a clash, offers open slots when
  they ask "when are you free?", creates the invite with a Google Meet link from your own calendar
  after your yes, confirms by email, and moves the deal to call-booked so follow-ups stop. Use when
  the user says "book it", "schedule a call", "put it on my calendar", "send an invite",
  "when am I free", "they said Thursday works", or when /follow-up shows a reply with a time.
argument-hint: "[parse <reply> | free | book <contact> <time>]"
---

# scheduler

The moment someone says yes to a call, the Scheduler gets it on both calendars before the moment
passes. One booked call is worth more than ten more follow-ups.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/slots.py" parse --text "Sorry, crazy week! Thursday at 2 works." --today 2026-10-27
python3 "${CLAUDE_SKILL_DIR}/slots.py" free --busy closer/busy.json --from 2026-10-28 --days 3 --length 30
python3 "${CLAUDE_SKILL_DIR}/slots.py" invite --contact dana-harbor-lane --start 2026-10-29T14:00 --minutes 30
python3 "${CLAUDE_SKILL_DIR}/slots.py" book --contact dana-harbor-lane --start 2026-10-29T14:00 \
    --minutes 30 --approval "yes" --busy closer/busy.json
```

## Steps

1. **When.** `slots.py parse` on their reply. "at 2" with no am or pm is read as 2 PM (1 to 7 is afternoon,
   8 to 12 is morning). If it prints "No clear time", ask them for one; never guess a day.
   Say the full date back to the user: "Thursday, October 29 at 2:00 PM your time. Right?"
2. **Clash.** With the calendar connector, read the user's events for that day and write them to
   `closer/busy.json` as `[{"start": "...", "end": "..."}]`. If they asked for options instead,
   `slots.py free` lists open slots in working hours; offer two or three.
3. **Ask.** "Book Harbor Lane Dental x Your Agency, Thursday October 29, 2:00 to 2:30 PM, Google Meet,
   with Dana Ortiz invited? Reply yes or no."
4. **Book.** On a yes, create the event on the user's calendar with the calendar connector (title, time,
   Google Meet, Dana as a guest). No calendar connector: `slots.py invite` writes an .ics the user can
   open or attach.
5. **Log.** `slots.py book --approval "<their yes>"`. The deal moves to call-booked and `/follow-up` stops.
6. **Confirm.** Draft the reply with `/follow-up`'s confirm-time template ("Thursday at 2 works, Dana.
   Sending the invite now."), and send it only on its own yes.
7. **Prep.** Remind the user to run `/researcher` before the call.

## Example from the reel

Tue Oct 27, 11:48 AM: "Sorry, crazy week! Thursday at 2 works." `parse` gives Thursday, October 29,
2:00 PM. The user is free, says yes, and the calendar shows "Harbor Lane Dental x Your Agency, Thursday,
October 29, 2:00 to 2:30 PM, Google Meet, guests Dana Ortiz and You". (Illustrative: Dana and Harbor Lane
Dental are fictional.)

## What it never does

- Never books, moves or cancels an event without the user's yes for that exact event.
- Never double-books over something already on the user's calendar.
- Never reads calendar details beyond free and busy times to find a slot.

## Consent and truth

- Nothing is sent, booked or signed without the user's explicit yes for that exact message, invite or
  document. Claude drafts, the user says "yes", then it goes out from the user's own accounts:
  calendar invites through the user's own calendar. One yes per message. Never "yes to all".
- Stop at the first "no" or any sign of disinterest. A request to stop is honoured forever, across every skill.
- Never invent a time someone agreed to. When it is unclear, ask.
