---
name: grill-me
description: Interview the user until the plan is clear, before any code gets written. Use when the user shares a new product idea or feature, or asks to build something whose person, problem, core action or scope is not already written down in an approved IDEA_SCOPE.md or scoping doc. Also use when they say "grill me", "poke holes", "stress-test this", "what am I missing", or seem unsure what to build. Skip small fixes, copy tweaks, and work an approved scoping doc already covers.
---

# Grill me

Interview the user relentlessly until you both understand exactly what they are building. Do not write code or a plan until they confirm the interview is done.

## How to ask

- One question at a time. Wait for the answer before asking the next.
- Give your recommended answer with every question, so they can just say "yes".
- Offer concrete choices ("email login or no login?"), never abstract ones ("what auth strategy?").
- Plain words. If you use a technical term, explain it in the same sentence.
- Only ask questions whose prerequisites are settled. If an answer depends on something still open, ask that first.
- Facts are your job: if something can be found in the project files or by searching, look it up instead of asking. Decisions are theirs.

Format each question like this:

```
❓ <question, with the choices if there are any>

➡️ my suggestion: <recommended answer, one line on why>
```

## What to cover

Work through these in order, skipping anything already answered:

1. **The one person.** A name, an age, a real situation. Not a segment.
2. **The moment.** When exactly the frustration happens, and what they do today instead.
3. **The core action.** User does X → gets Y. One action, one result.
4. **What v1 does not do.** Push every extra feature here. Login, settings and dashboards usually belong here.
5. **What can go wrong.** At least three failure modes: bad input, wrong AI output, lost data.
6. **The riskiest assumption.** The one thing that makes the product pointless if it's false, and a 30-minute test for it that needs no code.
7. **The first three users.** Real people they can reach this week, and where those people already gather.

Then keep following every branch their answers open up. Push back when an answer is vague, too big to ship in a weekend, or a pain they admire rather than one they feel.

## When to stop

Stop when nothing is left silently assumed, or when the user says "enough" or "just build it". Then:

1. Summarise the decisions in a short list, and flag any you had to assume.
2. Ask them to confirm or correct it.
3. Offer to write it into IDEA_SCOPE.md (or their scoping doc). Only after that, move on to planning or building.

---

Adapted from `grill-me` and `grilling` in [mattpocock/skills](https://github.com/mattpocock/skills), MIT License, Copyright (c) 2026 Matt Pocock.
