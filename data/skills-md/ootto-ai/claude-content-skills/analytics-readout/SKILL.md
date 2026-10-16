---
name: analytics-readout
description: >
  Reads your reel insights and explains in plain English what to make more of and what to stop —
  no jargon.
  Use when the user says "explain my analytics", "what do my numbers mean", "read my insights", "how did this reel do".
user-invokable: true
argument-hint: "[paste your insights, or connect the MCP]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# Analytics Readout — your numbers, in plain English

Reads your reel insights and explains in plain English what to make more of and what to stop — no
jargon.


## When to use
You're looking at insights and can't tell what to do differently.

## What you'll need
Your reel or account insights. The Ootto MCP can pull them directly.

## Instructions
Give Claude the input and run this.

```
You are my analyst. Here are my insights: [paste]. My goal right now is: [reach/saves/leads/follows].

1. THE METRIC THAT MATTERS for that goal — and tell me which numbers to stop staring at.
2. VS MY MEDIAN: every figure judged against my own baseline, not anyone else's screenshot.
3. WHERE IT BROKE: if retention data exists — a drop at ~3s is a hook problem, at ~12s a middle problem,
   at the end a CTA problem. Name which.
4. TWO ACTIONS. Not twelve. The two that would move the metric in point 1.
5. WHAT I CAN'T TELL from this data, stated plainly.

Every number must come from what I pasted. If something isn't there, say so — do not estimate.
```

**Honesty:** No invented figures, no industry benchmarks presented as my data. 'Not enough signal' is a valid
answer.

**Next:** [content-audit](../content-audit/SKILL.md)

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
