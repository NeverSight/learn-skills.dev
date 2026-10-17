---
name: competitor-teardown
description: >
  Reverse-engineers a rival account's best posts into the patterns, hooks, and posting cadence
  actually driving their growth.
  Use when the user says "break down this account", "why is this competitor growing", "what is @x doing right", "teardown their content".
user-invokable: true
argument-hint: "[competitor handle or a few of their post links]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# Competitor Teardown — the pattern behind a rival's best posts

Reverse-engineers a rival account's best posts into the patterns, hooks, and posting cadence
actually driving their growth.


## When to use
A rival is growing and you want the mechanism, not a vibe.

## What you'll need
Their handle, or 5-10 of their posts with engagement numbers. [agent-reach](../agent-
reach/SKILL.md) can pull them.

## Instructions
Give Claude the input and run this.

```
You are my competitive analyst. Account: [HANDLE]. Posts: [paste 5-10 with views/likes/comments].

1. WINNERS vs REST: which posts beat their median, and the trait the winners share that the others lack.
2. HOOK PATTERN: write their reusable opening as a fill-in template.
3. STRUCTURE: the beat shape they repeat.
4. CADENCE: how often they post, the format mix, what they do after something lands.
5. THE GAP: what their comments keep asking for that they are NOT making. That gap is my lane.
6. MY THREE: three reels I could make this week in that gap, in my voice.

Give me the pattern, never their copy.
```

**Honesty:** This produces a pattern to model. Reproducing their actual words gets you demoted by the
platform and makes you a worse version of them.

**Next:** [comment-mining](../comment-mining/SKILL.md) → [viral-hook-writer](../viral-hook-writer/SKILL.md)

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
