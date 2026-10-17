---
name: cover-thumbnail-brief
description: >
  Writes the cover-frame text and visual brief that makes your reel stop the scroll on the grid
  and in Explore.
  Use when the user says "write my cover text", "thumbnail brief", "what should the cover say", "grid cover for this reel".
user-invokable: true
argument-hint: "[the reel topic or script]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# Cover & Thumbnail Brief — the frame that stops the scroll on the grid

Writes the cover-frame text and visual brief that makes your reel stop the scroll on the grid and
in Explore.


## When to use
The reel is made and the grid cover decides whether anyone opens it.

## What you'll need
The reel topic or script, and a look at your current grid.

## Instructions
Give Claude the input and run this.

```
You are my cover designer. Reel: [TOPIC/SCRIPT]. My grid currently looks like: [describe or paste].

1. COVER TEXT: 3-5 words max. Give me three options, ranked, each legible at thumbnail size.
2. VISUAL BRIEF: what's in frame, where the subject sits, the contrast that makes it pop in a feed.
3. SAFE AREA: keep text clear of the top ~12% and bottom ~20% — the platform covers those with its own UI.
4. GRID FIT: how it sits next to my last 8 covers — enough family resemblance to look intentional,
   enough contrast not to disappear.
5. TEST: describe it at 150px wide. If it's unreadable there, give me a simpler option.
```

**Honesty:** Legibility beats cleverness. A clever cover nobody can read at thumbnail size does not exist.

**Next:** [caption-and-hashtags](../caption-and-hashtags/SKILL.md)

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
