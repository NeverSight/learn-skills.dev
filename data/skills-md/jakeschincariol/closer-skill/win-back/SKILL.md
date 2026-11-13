---
name: win-back
description: >-
  Win-Back. Brings back the deals that went quiet. Finds lost deals worth one more try (bad timing,
  budget, still thinking, no decision) once enough time has passed or on the date they asked you to
  come back, plus open deals that went silent after every follow-up, and writes one short, honest
  check-in from the reason it was lost. One win-back per deal, never to anyone who said no or
  unsubscribed. Use when the user says "win back", "revive old deals", "follow up on lost deals",
  "who went quiet", "re-engage", "dead leads", or once a week.
argument-hint: "[list | draft <deal>]"
---

# win-back

"Not now" is not "no". The Win-Back skill remembers who said not now and comes back once, at the right
time, with a reason to talk. It never chases anyone who said no.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/winback.py" list --today 2026-10-29
python3 "${CLAUDE_SKILL_DIR}/winback.py" draft --deal lakeline-website --today 2026-10-29
python3 "${CLAUDE_SKILL_DIR}/winback.py" record --deal lakeline-website --text-file /tmp/w.txt \
    --approval "yes" --at 2026-10-29T10:00
```

## Who it tries, and when

- **Lost for timing, budget, "let me think" or no decision:** 60 days after it was lost, or on the deal's
  own `revisit` date if they named one ("ask again in the fall": set `revisit` on the deal).
- **Lost to someone else:** not before 180 days, and only a friendly "how's it going".
- **Open but silent:** no activity for 30 days after `/follow-up` used all 3 follow-ups.
- **Never:** anyone who said no, unsubscribed or is do-not-contact. Never twice: one win-back per deal,
  and if there is no reply, that is the end. Another try only after they write back, and 90 days later.

## Steps, once a week

1. `winback.py list`. Read the READY ones to the user with why, biggest first. Mention LATER ones with their date.
2. For each the user wants, `winback.py draft`. Make it more specific with one true, new thing if you have
   one (a new plan, a result for a similar business). Keep it under 60 words, and keep the easy out:
   "If not, no problem at all, just say so and I'll leave it."
3. Ask: "Send this to Tom at Lakeline Roofing? Reply yes or no."
4. On a yes: a Gmail draft from the user's account, which the user sends (or sent through the Gmail
   connector right after that yes). Then `winback.py record --approval "<their yes>"`. The deal opens again.
5. If they reply, it is a conversation: `/follow-up reply`, then `/scheduler`.

## Example

Tom Becker at Lakeline Roofing liked the idea in July but said it was roofing season: "ask again in the
fall." Lost on Aug 10 for timing. On Oct 29 `list` shows READY, and the draft reads: "Hi Tom, when we spoke
you said the timing wasn't right until the fall. Is now any better for website + reviews widget? If not,
no problem at all, just say so and I'll leave it." Elena Ruiz at Mesa Verde Med Spa asked to be removed, so
she shows as NEVER. (Illustrative: both businesses are fictional.)

## What it never does

- Never emails anyone who said no, unsubscribed or is do-not-contact.
- Never sends a second win-back after an unanswered first one.
- Never invents a reason to write ("just saw your post", "my colleague mentioned you") that is not true.

## Consent and truth

- Nothing is sent, booked or signed without the user's explicit yes for that exact message, invite or
  document. Claude drafts, the user says "yes", then it goes out from the user's own accounts.
  One yes per message. Never "yes to all".
- Stop at the first "no" or any sign of disinterest. A request to stop is honoured forever, across every skill.
- Every email is honest about who is writing and keeps a plain way to opt out. Opt-outs are honoured forever.
- Never invent a number, a result, a client, a review or a deadline.
