---
name: cold-call-script
description: "Use this skill when you need a B2B cold call script or talk track: \"write a cold call script\", \"what do I say when they pick up\", \"help me prep cold calls for this list\", \"handle objections on the phone\". Builds an opener that earns 30 seconds, a problem statement in the buyer's words, two or three discovery questions, a meeting ask and the responses to the most common brush-offs. Written to be said out loud, with a one-page version for the call and a practice drill."
license: MIT
metadata:
  title: Cold call script
  category: multichannel
  tags: "SDR, Sales, Founders"
  author: prosyo
  version: "1.0.0"
  keywords: "cold call script b2b, cold calling opener, sdr call script, claude cold call skill, cold call objection handling"
  inputs: "Persona and problem, Offer and proof, Trigger if any"
  outputs: "Call script, Objection responses, One-page call card, Practice drill"
---

Use this before a calling block. It produces a talk track that sounds like a person, not a reading, and that gets to a decision (meeting or no) in under three minutes.

## Inputs

- Persona and the problem.
- Offer and one strong proof point.
- Trigger or prior touch (an email they may have seen).

## The play

### 1. Opener: honest and short
Name yourself, acknowledge the interruption, give the reason in one sentence, ask for 30 seconds.

> "Hi Maya, it's Sam from Acme. This is a cold call, so feel free to hang up, but can I tell you why I called and you decide if it's worth a minute?"

Permission-based openers convert better than pretending the call is expected.

### 2. Problem statement: the reason
One or two sentences about a problem people in their role usually have, with a peer reference. End with a question.

> "I work with finance leads at companies your size. Most tell me close takes 8 to 10 days because approvals sit in inboxes the last week of the month. Is that true for you, or have you solved it?"

### 3. Discovery: two or three questions
Ask, listen, follow the answer. Good questions are about their current process and its cost: "How long does close take today?", "Where does it get stuck?", "What happens when it runs late?"

### 4. The ask
If there is a problem: "Contoso was at 9 days and now closes in 4. Worth 20 minutes next week to see if the same thing would work for you? Tuesday or Thursday?"
If there is no problem: thank them, ask who else might feel it, and leave.

### 5. Brush-offs
Read [references/call-objections.md](references/call-objections.md) for responses to the ten most common brush-offs. The principle: acknowledge, ask one question, then respect the answer.

## One-page call card

```
Opener: <permission line>
Reason: <problem + peer>  →  "Is that true for you?"
Questions: 1. <current process>  2. <where it breaks>  3. <cost of it>
Proof: <one line>
Ask: <20 minutes, two time options>
If no: "Who else on your team deals with <problem>?"
```

## What good looks like

- The rep speaks less than 50% of the call.
- A clear outcome every time: meeting, referral, follow-up date, or a no.
- The common mistake is the pitch dump: 90 seconds of features before the prospect has said a word.

## Rules

- MUST say who you are and that it is a sales call when asked.
- MUST respect do-not-call lists and local calling rules and hours.
- NEVER pretend to know the prospect or reference a conversation that did not happen.
- NEVER keep pushing after a clear no.

## Example prompts

- "Write a cold call script for IT directors at hospitals. We sell device management."
- "Prep me for 40 calls tomorrow to people who were sent our email last week."
- "Give me responses to 'just send me an email' and 'we're all set'."
