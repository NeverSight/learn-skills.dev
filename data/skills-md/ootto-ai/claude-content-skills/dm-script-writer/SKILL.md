---
name: dm-script-writer
description: >
  Writes the DM flow that turns an inbound comment or lead-magnet request into a booked call or a
  sale.
  Use when the user says "write my DM script", "what do I send after they comment", "DM flow", "turn DMs into calls".
user-invokable: true
argument-hint: "[what they commented for, and what you sell]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# DM Script Writer — from comment to booked call

Writes the DM flow that turns an inbound comment or lead-magnet request into a booked call or a
sale.


## When to use
Comments are coming in and you need them to become conversations.

## What you'll need
The keyword they commented, what you're delivering, and what you sell.

## Instructions
Give Claude the input and run this.

```
You are my DM strategist. They commented: [KEYWORD]. I'm sending: [RESOURCE]. I sell: [OFFER].

1. MESSAGE ONE — DELIVER: give them the thing, no pitch. Short. Must earn a reply.
2. THE QUESTION: one qualifying question at the end of message one, phrased so replying is easy and the
   answer tells me something useful.
3. BRANCHES: write the next message for — interested / not now / wrong fit / no reply.
4. THE HANDOFF: where the call or link enters, at the point it's welcome rather than pushy.
5. TONE: match how they wrote to me. If they sent one word, don't send five paragraphs.

Keep every message under 950 characters.
```

**Honesty:** On Instagram a private reply to a comment works ONCE. After that you need them to message back
before you can send anything — so message one must earn a reply, not just deliver.

**Next:** [comment-responder](../comment-responder/SKILL.md)

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
