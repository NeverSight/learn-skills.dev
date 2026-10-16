---
name: best-time-scheduler
description: >
  Recommends the posting times and weekly cadence that fit your audience's actual activity
  windows.
  Use when the user says "when should I post", "best time to post", "posting schedule", "how often should I post".
user-invokable: true
argument-hint: "[your audience and timezone, or your insights]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# Best-Time Scheduler — a cadence you will actually keep

Recommends the posting times and weekly cadence that fit your audience's actual activity windows.


## When to use
You're posting whenever and wondering if timing is the problem.

## What you'll need
Your audience's timezones and, ideally, your insights showing when they're active.

## Instructions
Give Claude the input and run this.

```
You are my scheduler. Audience: [WHO/WHERE]. My insights: [paste activity data if you have it].
I can realistically post [N] times a day.

1. TIMES: the specific slots, from MY data if provided. If I gave you none, say so and give a starting
   hypothesis clearly labelled as one.
2. CADENCE: a weekly pattern I can actually sustain at [N]/day.
3. SLOT ROLES: which slot gets my strongest piece, which is for testing.
4. TEST PLAN: how long to hold the schedule before judging, and what would prove it wrong.
5. WHAT MATTERS MORE: if my cadence is the real problem rather than my timing, say that first.
```

**Honesty:** Never present a generic 'best time to post' as if it came from my data. Label a hypothesis as a
hypothesis.

**Next:** [content-calendar](../content-calendar/SKILL.md)

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
