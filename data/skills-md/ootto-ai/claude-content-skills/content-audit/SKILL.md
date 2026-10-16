---
name: content-audit
description: >
  Reviews your last 30 posts to find what is worth doubling down on, what is dead weight, and the
  gaps to fill.
  Use when the user says "audit my content", "what is working on my account", "what should I stop posting", "review my last 30 posts".
user-invokable: true
argument-hint: "[paste your recent post list with their numbers]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# Content Audit — what to double down on, and what to stop

Reviews your last 30 posts to find what is worth doubling down on, what is dead weight, and the
gaps to fill.


## When to use
Before making more, work out what to stop.

## What you'll need
Your last 30 posts with views, saves, comments and shares. The Ootto MCP or your Instagram
insights export.

## Instructions
Give Claude the input and run this.

```
You are my content analyst. Here are my last 30 posts with their numbers: [paste].

1. MEDIAN FIRST: state my median views/saves so everything is judged against ME, not someone else.
2. OUTLIERS: the posts that beat it, and the trait they share.
3. DEAD WEIGHT: formats or topics I keep making that consistently underperform. Name them plainly.
4. BY TRAIT: score hook style, length, format and topic, each with its real multiple vs median.
5. STOP / KEEP / TEST: three short lists.
6. NEXT FIVE: five posts to make, each justified by a number above.

If a pattern isn't in the data, say "not enough signal" rather than guessing.
```

**Honesty:** Every multiple must come from the numbers pasted in. No estimated figures, and no advice that
contradicts my own data.

**Next:** [content-pillar-builder](../content-pillar-builder/SKILL.md) → [content-calendar](../content-calendar/SKILL.md)

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
