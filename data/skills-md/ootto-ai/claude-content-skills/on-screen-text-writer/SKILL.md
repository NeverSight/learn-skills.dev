---
name: on-screen-text-writer
description: >
  Writes the tight caption-style overlays that keep silent viewers watching to the end.
  Use when the user says "write the on-screen text", "captions for this reel", "text overlays", "what should appear on screen".
user-invokable: true
argument-hint: "[your script]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# On-Screen Text Writer — for the 80% watching on mute

Writes the tight caption-style overlays that keep silent viewers watching to the end.


## When to use
Most people watch on mute. The text has to carry the reel alone.

## What you'll need
Your script, with the beats marked if you have them.

## Instructions
Give Claude the input and run this.

```
You are my on-screen text writer. Script: [paste].

1. ONE LINE PER BEAT: the headline of that beat, not a transcript. Short enough to read before the cut.
2. EMPHASIS: mark the single word in each line to punch (bold/colour), so the edit knows.
3. TIMING: tie each line to the spoken word it should appear on.
4. MUTE PASS: list the lines in order on their own. Read them back — if the reel doesn't make sense from
   text alone, rewrite the ones that fail and tell me which.
5. LENGTH CHECK: flag any line over ~7 words.
```

**Honesty:** This is not your script written out. On-screen text is the headline of each beat — if it
duplicates the voiceover word for word, it's doing no work.

**Next:** [reel-builder](../reel-builder/SKILL.md)

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
