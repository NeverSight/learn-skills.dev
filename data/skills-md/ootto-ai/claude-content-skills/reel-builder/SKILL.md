---
name: reel-builder
description: >
  Turn a teardown (or a rough idea) into a finished, ready-to-shoot reel. Claude writes the
  beat-by-beat script in your voice and lays out the on-screen text, the scene for each beat, the
  pacing cues, and the caption — your words on a proven structure. Use when the user says "build the
  reel", "make the reel", "write the full reel", "turn this into a reel", "script and storyboard
  this", or hands over a breakdown/idea and wants the whole thing assembled.
user-invokable: true
argument-hint: "[a reel-analyzer teardown, or a topic + the structure to follow]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# Reel Builder — Claude assembles the whole reel for you

The last step of the factory. Hand Claude a teardown (from [reel-analyzer](../reel-analyzer/SKILL.md))
or just an idea + the structure to follow, and it **builds the finished reel** — every beat scripted in
your voice, with the on-screen text and the visual for each beat — so you can shoot/render it as-is.

## When to use
You have the structure you want to model (or a hook + topic) and you want the entire reel assembled, not
just notes. Run this after the analyzer + hook writer, or standalone with your own outline.

## What you'll need
The **teardown or structure** to follow, your **topic/offer**, your **voice**, and the **CTA** (what you
want them to do). Optional: your past winners (via [ai-brain](../ai-brain/SKILL.md)) so it sounds like you.

## Instructions
```
You are my reel builder. Build a complete, ready-to-make reel.
STRUCTURE TO FOLLOW: [paste the reel-analyzer teardown, or describe the beat structure].
TOPIC: [what it's about] · VOICE: [yours] · GOAL/CTA: [save / follow / comment / DM].

Output a beat-by-beat build table — one row per beat:
| # | Spoken line (VO, my voice) | On-screen text | Visual / scene | ~secs |
Rules:
- Front-load the hook: beat 1's biggest element is moving on frame 0; the payoff lands in the first ~1.5s.
- The visual CHANGES every beat (show what's said — never plain text for a demo line).
- Original words on the modeled structure; total length matches the reference (±2s).
- End on ONE clear CTA that matches the deliverable.
Then give me: the final hook (3 options), the full VO script as one paragraph, and a caption + hashtags.
```

**Pairs with:** [reel-analyzer](../reel-analyzer/SKILL.md) (what to model) →
[viral-hook-writer](../viral-hook-writer/SKILL.md) (the opener) → this (the full build) →
[caption-and-hashtags](../caption-and-hashtags/SKILL.md) (the post).

## Rendering the reel — the video engine (make it, not just script it)

Scripting is half the job; this is how you turn the build table into a real, cinematic reel that
actually gets watched. Use a **hybrid engine**, matched to the tier:

- **Character-acting / cinematic beats → Seedance (image-to-video).** Seedance runs on **Runway** via
  the RunwayML SDK with `model: "seedance2"` (portrait `720:1280` for a 9:16 reel, ~5s per clip).
  Generate a conditioning still of the character/scene, then i2v it so the subject genuinely MOVES and
  performs. Cost ≈ $6–12 per reel — reserve it for the premium ($599 done-for-you) tier, not the $20 self-serve one.
- **Hook, chapter, text, payoff, CTA beats → Remotion code-render ($0).** Fast, free, on-theme. This is
  the whole $20-tier reel and the text scaffolding of the premium one.

**Non-negotiables (each of these was a real failure once — do not repeat them):**
1. **The hook needs a gripping VISUAL, not just text.** Open on something that grabs (e.g. a creator
   hacking a glowing terminal, a lock cracking, sparks) — the payoff word lands in the first ~1.5s.
2. **The character ACTS through a progressive action — never ping-pong/loop a few poses.** Looping a small
   pose set back-and-forth (A→B→A→B) reads as "replaying" and plays actions in reverse. Each beat is ONE
   forward action, start to finish. Seedance i2v does this natively; posed-frame Remotion does NOT (it
   loops and reads choppy — avoid it for real acting).
3. **Sync the visual to the VOICEOVER, not a wall-clock.** Transcribe the VO (word timestamps) and cut/act
   ON the word — the action must match what's being said. Lead the cut ~10 frames.
4. **Emphasis text must be high-contrast and readable** on every background (e.g. bright amber `#FFCC33`
   with a dark outline stroke reads on both dark and light beats).
5. **Close on an on-screen CTA card, tied to the comment system.** End with a themed "Comment [KEYWORD] and
   I'll DM you [the thing]" card (an IG-composer graphic that types the keyword) — use the SAME keyword the
   caption uses and that the auto-responder is wired to, so comment → auto-DM → lead actually fires. Wire the
   keyword in [comment-responder](../comment-responder/SKILL.md) BEFORE you post, so the moment a viewer
   comments the keyword they get the auto-DM. Honest only: the keyword must be really wired.
6. **No fabricated numbers.** If a metric can't be verified, don't put it on screen.

**Verify before you ship — WATCH and MEASURE the playback, never trust a still.** Extract frames at ~12fps
and confirm: motion is progressive (no repeating/ping-pong autocorrelation period), no frozen beats while
the VO talks, and each action's cut aligns to its narration cue. Then eyeball the whole thing end to end.
A reel that was never watched ships broken.

**Credentials:** use an API key you were explicitly given, from your OWN project's env only. Never search
the filesystem for a key or read another product's `.env` — if you don't have the key, stop and ask.

**Honesty:** only promise a CTA you can deliver (if "comment WORD → I'll DM it", actually send it).

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs
the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
