---
name: ab-hook-tester
description: >
  Generates two genuinely distinct hook variants for the same reel so you can post-test which
  opening actually wins.
  Use when the user says "give me two hooks to test", "A/B this hook", "which opening should I use", "hook variants".
user-invokable: true
argument-hint: "[the reel idea or script]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# A/B Hook Tester — two hooks, one variable, a real answer

Generates two genuinely distinct hook variants for the same reel so you can post-test which
opening actually wins.


## When to use
You have a reel and two instincts about how to open it.

## What you'll need
The script or the idea, plus what you're optimising for (retention, saves, DMs).

## Instructions
Give Claude the input and run this.

```
You are my hook tester. Reel: [paste script or idea]. I care most about: [retention/saves/DMs].

Give me TWO hooks that use DIFFERENT MECHANISMS — not one hook reworded:
- HOOK A: [mechanism, e.g. result-first] — the exact on-screen text + spoken line.
- HOOK B: [a different mechanism, e.g. objection-first] — same.

Then:
1. HYPOTHESIS: what I learn if A wins, and what I learn if B wins.
2. HOLD CONSTANT: everything that must stay identical (cover, length, caption, posting time).
3. READ: which metric decides it, and at what point (3s retention, not likes).
4. SAMPLE: roughly how many views before the result means anything.

If both hooks pull the same lever, say so and replace one.
```

**Honesty:** One variable. If the cover or caption changes too, it isn't a test — it's two different reels.

**Next:** [reel-scripter](../reel-scripter/SKILL.md) → [cover-thumbnail-brief](../cover-thumbnail-brief/SKILL.md)

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
