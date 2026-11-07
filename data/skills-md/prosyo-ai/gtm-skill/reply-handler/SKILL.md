---
name: reply-handler
description: "Use this skill when outbound replies need triage and answers: \"sort these replies\", \"draft responses to my inbox\", \"what do I say to this reply\", \"handle replies from my campaign\". Classifies each reply (interested, question, objection, referral, not now, not interested, out of office, wrong person, unsubscribe), sets priority and the next action, drafts a response for each that moves toward a meeting or closes cleanly, and updates what the CRM needs to know. Drafts only: a human approves before anything is sent."
license: MIT
metadata:
  title: Reply handler
  category: replies-meetings
  tags: "SDR, Founders, Sales, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "sales reply handling, cold email reply templates, classify email replies, claude reply handler skill, ai inbox triage sales"
  inputs: "Replies with the original message, Offer and calendar link, Objection answers"
  outputs: "Classified replies, Priority and next action, Draft responses, CRM updates"
---

Use this when replies arrive from a campaign. Speed decides how many positive replies become meetings: interested prospects answered within an hour book far more often than those answered the next day.

## Inputs

- Each reply with the message it answers.
- Offer, a booking link or the sender's availability, and approved answers to common questions.
- Who approves outgoing replies.

## The play

### 1. Classify every reply
| Class | Signal | Priority |
| --- | --- | --- |
| Interested | "Sure", "Tell me more", "Let's talk", asks for times | Now |
| Question | Asks about price, how it works, integrations | Now |
| Referral | "Talk to Sam" | Today |
| Objection | "We already use X", "No budget", "Not a fit because..." | Today |
| Not now | "Reach out in Q3", "Busy until after launch" | Today, then schedule |
| Not interested | "No thanks", "Not interested" | Today, close politely |
| Wrong person | "I don't handle this" | Today, ask who does |
| Out of office | Auto-reply | Pause; resume after return date |
| Unsubscribe or hostile | "Remove me", "Stop" | Now: suppress everywhere |

Read [references/reply-playbook.md](references/reply-playbook.md) for a draft pattern for each class.

### 2. Draft the response
- Answer what they asked first, in their length. A one-line reply gets a short answer.
- Interested: confirm, offer two specific times or the booking link, and one line on what the call will cover.
- Question: answer directly; then the meeting question.
- Objection: acknowledge, one clarifying question, respect the answer.
- Referral: thank them, then contact the referred person naming who suggested it.

### 3. Set the next action
Each reply gets: classification, draft, next step, follow-up date and the CRM update (status, reason, notes).

### 4. Hand over for approval
Group drafts by priority. Unsubscribes are processed immediately (suppression is not a sales message, so it needs no approval to stop sending).

## Output format

```
<prospect> | <class> | priority | draft reply | next step + date | CRM update
```

## What good looks like

- Interested and question replies have drafts ready within minutes.
- Drafts answer the exact question before asking for the meeting.
- "Not now" replies get a dated follow-up, not a lost note.
- The common mistake is answering every positive reply with a calendar link and nothing else, which reads like a bot and drops conversion.

## Rules

- MUST suppress unsubscribes and hostile replies across all channels immediately.
- MUST get approval before sending any drafted reply.
- MUST stop all sequences for anyone who replied.
- NEVER argue with a "not interested".
- NEVER invent pricing, features or availability in an answer.

## Example prompts

- "Here are 37 replies from yesterday's campaign. Classify them and draft responses."
- "They replied 'what does it cost?'. Draft an answer that gets to a meeting."
- "Set up reply categories and templates for our SDR team."
