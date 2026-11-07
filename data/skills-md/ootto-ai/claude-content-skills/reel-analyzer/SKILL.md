---
name: reel-analyzer
description: >
  Feed Claude any viral reel (a link or a file) and it studies the whole thing — frame by frame
  plus the transcript — then breaks down exactly why it works: the hook, the beat structure, the
  pacing, and the on-screen visuals. Use when the user says "study this reel", "break down this
  video", "analyze this reel", "why did this go viral", "what's the structure of this", or pastes a
  reel/TikTok/Short link and wants to model it.
user-invokable: true
argument-hint: "[reel/TikTok/Short URL or video file]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# Reel Analyzer — Claude watches the reel so you can model it

Stop guessing why something went viral. Feed Claude the reel you want to take inspiration from and it
**watches the whole thing** — the visuals frame by frame and the spoken words — then hands you a
teardown you can build your own original from. This is step one of the content factory.

## When to use
You found a reel/Short/TikTok that's clearly working and you want to make your **own** version in your
voice. Start here — the breakdown feeds the hook writer, the scripter, and the builder.

## What you'll need
The reel **link** (or a downloaded video file). Don't have one yet, or only have a link?
[agent-reach](../agent-reach/SKILL.md) is the step before this — it **finds** a proven reel to model
(and mines Reddit for what to make it about) and **downloads** any URL to its transcript, which is what
this skill reads. Optional: your niche and the angle you want, so the breakdown is framed for *your* remake.

## Instructions
Give Claude the reel and run this. (In Claude Code, point it at the file/frames + transcript; on
claude.ai, upload the video or paste the transcript + a few screenshots.)

```
You are my reel analyst. Here is a reel I want to model (link/file/transcript + frames): [paste].
WATCH the whole thing, then give me a teardown I can build an original from:

1. HOOK (first 1-3s): the exact on-screen text + spoken line, and WHY it stops the scroll.
2. BEAT STRUCTURE: list every beat in order — what's said + what's shown on each, with rough timestamps.
3. PACING: how fast beats cut, where it speeds up/slows down, total length.
4. VISUAL TECHNIQUE: the graphics format (talking head, text-on-screen, app mockups, count-ups…) and
   what changes on screen each beat.
5. WHY IT WORKS: the 2-3 reusable moves (the format/technique to borrow — NOT the words to copy).
6. MY REMAKE: a one-line plan to redo this in my niche/voice — same structure, original content.

Rule: model the technique, never reproduce the creator's words/voice (copies get reach-suppressed).
```

**Honesty:** this gives you the *structure and technique* to model — your remake must be original
words and your own examples, not a re-upload.

**Next:** feed the teardown into [viral-hook-writer](../viral-hook-writer/SKILL.md) →
[reel-scripter](../reel-scripter/SKILL.md) → [reel-builder](../reel-builder/SKILL.md).

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs
the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
