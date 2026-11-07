---
name: linkedin-message-sequence
description: "Use this skill when you need a LinkedIn outreach sequence that starts conversations instead of collecting ignored pitches: \"write a LinkedIn message sequence\", \"what do I send after they accept\", \"LinkedIn prospecting messages\". Designs the steps from connection to meeting (note, first message, value message, soft ask, close), writes each message in a conversational tone, sets timing and exit rules, and includes reply branches for the most common answers."
license: MIT
metadata:
  title: LinkedIn message sequence
  category: linkedin
  tags: "SDR, Founders, Agencies, Sales"
  author: prosyo
  version: "1.0.0"
  keywords: "linkedin message sequence, linkedin outreach templates, linkedin prospecting messages, claude linkedin outreach skill, linkedin follow up message"
  inputs: "Persona and problem, Offer and proof, Reason to connect"
  outputs: "Message sequence with timing, Reply branches, Exit rules"
---

Use this to plan a LinkedIn campaign end to end. LinkedIn is a conversation channel; messages that read like emails pasted into a chat window get ignored.

## Inputs

- Persona and the problem the campaign is about.
- Offer and approved proof.
- The reason to connect (from research, an event, content or a trigger).

## The play

### 1. Shape the sequence
| Step | Timing | Job | Length |
| --- | --- | --- | --- |
| Connection request | Day 0 | Get accepted | Under 200 characters, no pitch |
| Message 1 | 1-3 days after accept | Start a conversation on the topic | 1-3 sentences, ends in a question |
| Message 2 | 4-5 days later | Give value: an insight, resource or story | 2-4 sentences |
| Message 3 | 5-7 days later | Soft ask tied to their answer or the topic | 2-3 sentences |
| Message 4 | 7-10 days later | Close the loop warmly | 1-2 sentences |

Voice notes and short videos can replace message 2 or 3 for Tier 1 contacts; they stand out because few people use them.

### 2. Write like a chat
Short lines, no subject, no sign-off block, no bullet lists, no links in message 1. Ask questions people can answer from their phone in five seconds.

### 3. Bridge from topic to problem
Message 1 is about the topic that made you connect. The bridge to your problem comes through their answer, or in message 2 with a peer insight. Read [references/linkedin-sequence-example.md](references/linkedin-sequence-example.md) for a full example with reply branches.

### 4. Handle replies fast
LinkedIn replies expect a response within hours. Positive replies get a meeting link or two time options; questions get a direct answer, not a pitch.

### 5. Exit rules
Stop on any reply (switch to manual), if they decline, or if someone at the same account books a meeting. Withdraw connection requests not accepted after 14-21 days.

## What good looks like

- Message 1 gets a reply because it is a question about their world, not your product.
- No message is longer than a phone screen.
- Acceptance 30%+, reply rate on accepted connections 15-25%+ for a well-targeted list.
- The common mistake is "Thanks for connecting! We help companies like yours..." sent seconds after acceptance.

## Rules

- MUST wait at least a day after acceptance before the first message.
- MUST stop automation the moment someone replies.
- MUST stay within safe daily limits for invitations and messages.
- NEVER pitch in the connection note or message 1.
- NEVER send links in the first message.

## Example prompts

- "Build a LinkedIn sequence for heads of finance at 50-200 person companies. Problem: slow month-end close."
- "What should I send after people accept my connection request?"
- "Rewrite our LinkedIn messages; they read like emails."
