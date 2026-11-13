---
name: follow-up
description: >-
  Follow-Up. Keeps following up until a call is booked, then stops. Every morning it reads
  closer/pipeline.json and says who is due a follow-up today, who replied and is waiting on you,
  who booked, and who is stopped and why. Drafts each follow-up (a bump, then something useful,
  then a polite last note), waits for your yes, logs it, and stops at the first "no", the moment
  a call is booked, after 3 follow-ups or 30 days. Use when the user says "follow up",
  "who do I need to follow up with", "they haven't replied", "chase", "nudge", "bump this",
  "they replied", or every morning.
argument-hint: "[due | draft <contact> | reply <contact>]"
---

# follow-up

Most deals are lost to silence, not to "no". This skill makes sure nobody is forgotten and nobody
is pestered. It drafts; it never sends by itself.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/followup.py" due --today 2026-10-21
python3 "${CLAUDE_SKILL_DIR}/followup.py" draft --contact dana-harbor-lane --today 2026-10-21
python3 "${CLAUDE_SKILL_DIR}/followup.py" draft --contact dana-harbor-lane --today 2026-10-23 \
    --hook "here's a 1-minute mockup of what online booking could look like for Harbor Lane."
python3 "${CLAUDE_SKILL_DIR}/followup.py" record --contact dana-harbor-lane --text-file /tmp/f.txt \
    --approval "yes" --at 2026-10-21T09:00
python3 "${CLAUDE_SKILL_DIR}/followup.py" reply --contact dana-harbor-lane \
    --text "Sorry, crazy week! Thursday at 2 works." --at 2026-10-27T11:48
python3 "${CLAUDE_SKILL_DIR}/followup.py" stop --contact <id> --said "Please remove me from your list."
```

## The rules (per person, across every channel)

1. **Stop at the first "no"** or any sign of disinterest ("not interested", "no thanks", "we're all
   set", "please remove me"). An unsubscribe goes on the suppression list, and no skill emails them again.
2. **Stop the moment a call is booked.** That is the job. `/scheduler` and `/sales-coach` take over.
3. **A reply is your turn.** Answering them is a conversation, never a "follow-up".
4. **At most 3 follow-ups** after the opening, and the third one says it is the last.
5. **Nothing after 30 days** from the opening without a reply. `/win-back` may try once, much later.

`draft` refuses to draft and `record` refuses to log anything that breaks a rule.

## The cadence

Follow-up 1 is two days after the opening, follow-up 2 two days after that, follow-up 3 four days after
that. A date on a weekend moves to Monday. The reel's thread: Mon Oct 19 (opening), Wed Oct 21, Fri Oct 23,
Tue Oct 27.

1. **Follow-up 1, the bump.** One line: "just bumping this up in case it got buried."
2. **Follow-up 2, give something.** A mockup, a number, a short idea for them. `--hook` is that one new,
   true, specific thing. Without a hook there is no follow-up 2.
3. **Follow-up 3, the last note.** Offer a day for a call and say it is the last email. Either answer is fine.

## Steps, every morning

1. Run `/record-keeper` sync first so replies are on the board.
2. `followup.py due`. Read it to the user grouped as it prints: DUE NOW, YOUR TURN, WAITING, BOOKED, STOPPED.
3. For each DUE NOW, `followup.py draft`. Fill every `[fill: ...]`. Show it: "Send this follow-up to Dana?
   Reply yes or no." One message per question.
4. On a yes: a Gmail draft in the same thread from the user's account, which the user sends (or sent through
   the Gmail connector right after that yes). Then `followup.py record --approval "<their yes, word for word>"`.
5. For each YOUR TURN: when they gave a time, hand it to `/scheduler` (`slots.py parse`), confirm with the
   `confirm-time` template, and book. When they said no, `followup.py reply` with their words: it stops
   everything and marks the deal lost.

A scheduled morning run may list and draft. It never sends: nobody is there to say yes.

## Example from the reel

Dana Ortiz never answered the opening. Follow-up 1 on Wed Oct 21: "just bumping this up in case it got
buried." Follow-up 2 on Fri Oct 23: the 1-minute mockup. Follow-up 3 on Tue Oct 27: "should I close the loop
on this, or is Thursday good for a quick call?" At 11:48 AM she replied, "Sorry, crazy week! Thursday at 2
works." `reply` moved her to YOUR TURN; the call was booked, and from then on she got no more follow-ups.
(Illustrative: Dana and Harbor Lane Dental are fictional.)

## What it never does

- Never sends, and never records a message that did not go out.
- Never follows up after a no, after a booking, after 3 follow-ups or after 30 days.
- Never uses guilt, fake urgency, a fake "Re:" or a made-up reason to write.

## Consent and truth

- Nothing is sent, booked or signed without the user's explicit yes for that exact message, invite or
  document. Claude drafts, the user says "yes", then it goes out from the user's own accounts.
  One yes per message. Never "yes to all".
- Stop at the first "no" or any sign of disinterest. A request to stop is honoured forever, across every skill.
- Every email keeps the opt-out line from the opening thread. Opt-outs are honoured forever.
- Never invent a number, a result, a client, a review or a deadline.
