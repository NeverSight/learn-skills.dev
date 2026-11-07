---
name: trend-spotter
description: >
  Scans what is breaking in your niche right now — formats, sounds, angles — and tells you which
  trends actually fit your brand, and which to sit out.
  Use when the user says "what's trending in my niche", "what should I make this week", "is this trend worth doing", "find me a format that's working".
user-invokable: true
argument-hint: "[your niche, or a handful of accounts to watch]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# Trend Spotter — what is breaking in your niche, and whether it suits you

Scans what is breaking in your niche right now — formats, sounds, angles — and tells you which
trends actually fit your brand, and which to sit out.


## When to use
You need this week's angle and you don't want to guess. Run it before you pick what to make.

## What you'll need
Your niche in one line, and ideally 3-8 peer handles. With [agent-reach](../agent-reach/SKILL.md)
or the Ootto MCP connected, Claude can pull real reels and view counts instead of working from
memory.

## Instructions
Give Claude the input and run this.

```
You are my trend analyst for [NICHE]. Peers: [HANDLES / paste 10-20 recent reels with view counts].

1. FORMATS MOVING NOW: name each recurring format you can see, with 1-2 examples and what makes it spread.
2. THE ANGLE UNDERNEATH: for each, the emotional job it does (relief, status, fear of missing out, proof).
3. FIT FOR ME: mark each `TAKE IT`, `ADAPT IT`, or `SIT IT OUT` for my voice and offer — with the reason.
4. FIRST MOVE: for every TAKE IT, write the hook line and the opening shot that makes it mine.
5. FADING: anything that looks past peak, so I don't arrive late.

Rank by fit, not by view count. Tell me to skip things.
```

**Honesty:** Only call something a trend if you can point at real examples. If the data isn't there, say so
rather than inventing a wave.

**Next:** [viral-hook-writer](../viral-hook-writer/SKILL.md) → [reel-scripter](../reel-scripter/SKILL.md)

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
