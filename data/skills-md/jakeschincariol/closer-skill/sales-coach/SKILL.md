---
name: sales-coach
description: >-
  Sales Coach. Listens to your sales call and tells you exactly what to say next. Reads the call's
  live captions (Google Meet's own captions, read off the page by Claude in Chrome, or any captions
  file), and the moment the other side raises an objection ("it's too expensive", "let me think
  about it", "I need to ask my partner", "we already have someone") it shows you, and only you, the
  answer to say next, filled from your real offer. Also flags buying signals and questions you
  still owe an answer, and reviews the call afterwards (talk time, questions asked, next step).
  Use when the user says "coach me on this call", "listen to my call", "I have a sales call",
  "what do I say if they say it's too expensive", "objection", "handle objections", or "review my call".
argument-hint: "[listen | card <objection> | review]"
---

# sales-coach

The coach sits beside the user on a live call, reads the captions as they appear, and answers one
question the whole time: what do I say next? It never speaks on the call. It only shows the user a card.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/coach.py" listen --captions closer/calls/live.txt --me You
python3 "${CLAUDE_SKILL_DIR}/coach.py" listen --captions closer/calls/live.txt --me You --follow
python3 "${CLAUDE_SKILL_DIR}/coach.py" card --objection price
python3 "${CLAUDE_SKILL_DIR}/coach.py" review --captions closer/calls/live.txt --me You
```

The answers come from `objections.json` filled with the user's own offer from `closer/pipeline.json`
(`me.offer`, `me.price`, `me.plan_b`, `me.value_line`, `me.proof`). If a field is missing, the card shows
`[your value line]` instead of making one up.

## Before the call

1. Run `/researcher` on the prospect and read the brief together.
2. Check `me.plan_b` and `me.value_line` are set and TRUE. The price answer is only as good as they are.
3. Agree the opening line with the user: "Mind if I keep captions on so I can take good notes?"
   Everyone on the call hears that before anything is captured.

## During the call (Google Meet)

1. The user turns on captions in Meet (the CC button). The captions appear on the page with the speaker's name.
2. With Claude in Chrome, read the captions area every few seconds (`get_page_text` or `read_page` on the
   Meet tab) and append each NEW finished line to `closer/calls/live.txt` as `Name: text`. Never click
   anything in the meeting, never unmute, never type in the chat.
3. After each new line from the other side, run `coach.py listen --captions closer/calls/live.txt` on the
   new lines and show the card in big, plain text:

```
Objection: price  (Dana: "It looks great, but honestly, it's too expensive for us right now.")
Say this next: Totally fair. Most practices win the cost back with 2 new patients a month.
Want to start on the $399 monthly plan instead, with no setup fee?
```

4. Keep it to the card. No paragraphs mid-call. The user is talking.

Zoom, Teams or a phone call: any captions or live transcript the user can see works the same way. Or the
user runs `coach.py listen --follow` in a terminal while the lines are appended.

## The objections it knows

price, timing, needs to think, someone else decides, already has someone, does it work, send me info.
Each has the words it listens for, the answer, and why that answer works. Add the user's own: edit
`objections.json` with what their customers really say and what really works for them.

## After the call

`coach.py review`: how much of the call the user talked (aim for under half), how many questions they
asked, every objection and buying signal, and whether a next step was agreed. Then `/record-keeper call`
with the notes, and `/proposal-writer` or `/contract-writer` for the next step.

## Example from the reel

On the Thursday call at 2:14 PM, after "So that's the site, with online booking built in," Dana Ortiz said,
"It looks great, but honestly, it's too expensive for us right now." The card: Objection: price, "Totally
fair. Most practices win the cost back with 2 new patients a month. Want to start on the $399 monthly plan
instead, with no setup fee?" Then "How soon could we start?": Buying signal, agree the next step. The
transcript is `call.example.txt` (illustrative: Dana and Harbor Lane Dental are fictional).

## What it never does

- Never speaks, types or acts on the call. It only shows the user a card.
- Never keeps audio. The captions text stays in the user's project.
- Never suggests a lie, a fake deadline, a fake discount or pressure. If the true answer is "we're not the
  right fit", it says so.

## Consent and truth

- Calls: tell everyone on the call that captions or notes are on, before you start. Some places (for example
  California, Florida, Washington, and many countries) need every person's consent to record. The coach reads
  live captions as text, keeps no audio, and is shown only to the user. It never speaks on the call.
- Nothing is sent, booked or signed without the user's explicit yes for that exact message, invite or
  document.
- Never invent a number, a result, a client, a review or a deadline. Fill in only what is true and ask when
  something is missing.
