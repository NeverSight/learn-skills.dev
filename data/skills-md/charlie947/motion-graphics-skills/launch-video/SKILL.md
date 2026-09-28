---
name: launch-video
description: Make a 30-45 second product launch video in code with Claude Code, the kind SaaS companies post on launch day. One sentence split across scenes, real product screens with slow camera moves, a typed prompt, a proof beat and a clear call to action. Use when someone says "launch video", "promo video for my product", "announce my course/cohort/offer", "make a launch reel" or "trailer for my product".
---

# Launch video, built in code

A launch video sells one thing in 30-45 seconds. You build it as one HTML file with `window.seek(seconds)`, then export to MP4.

**Before you start:** read `brand.md` and `MOTION.md` if they exist. If not, run `brand-intake` first, or ask for hex codes, a font and a logo file. Never call a result on-brand without them.

## Step 1: Ask for five things, then wait

1. **What's launching,** in one line. Example: "LinkedIn AI OS, a six-week cohort that sets up your content system."
2. **The one sentence** the video says, split into 3-5 beats. Example: "Your next post, / in your voice, / checked before you see it."
3. **Proof.** Real screenshots of the product, real results with their source, or real customer posts. Attached files only.
4. **The call to action,** word for word, exactly as it appears on the sales page.
5. **Brand.** Hex codes, font, logo file. Plus the size: 1920 x 1080, 1080 x 1350 or 1080 x 1920.

Never invent a price, a date, a "spots left" count, a testimonial or a result.

## What "premium" means here (learned the hard way)

Three first drafts were rejected as "not premium" and "not my brand colours". What fixed it:
- **Your real brand colours,** sampled from your landing page or your best graphic. Never a default palette.
- **Glass UI.** Product surfaces as frosted, liquid-glass panels with soft depth, like Apple's current UI.
- **The prompt typed live** into a real-looking input box. That is the one place typing belongs.
- **Real, recent work** on the proof cards, not old examples.
- **Variety.** No two beats share the same layout.

Build the first 10 seconds in two or three styles first. Pick one. Only then build the rest.

## Step 2: Lay out the beats

Default 7 beats, 45 seconds:

| # | Time | Beat |
|---|---|---|
| 1 | 0-4s | First words of the sentence, big, on a clean background. The hook. |
| 2 | 4-9s | Next words over real proof (posts, results, screens). |
| 3 | 9-17s | The product working: a screen, a cursor typing a real prompt, the output appearing. |
| 4 | 17-22s | The quality beat: something checks, passes or ticks. |
| 5 | 22-32s | How it works: steps, weeks or features as one simple visual. |
| 6 | 32-38s | The number that matters, counted up, with its source. |
| 7 | 38-45s | Name, call to action, requirement. Holds long enough to read. |

Show the beat sheet and wait for a yes.

## Step 3: Build brief (paste into Claude Code)

```
Build one self-contained HTML file called index.html for a [LENGTH]-second product launch video at [WIDTH] x [HEIGHT]. Use only the files I attached. Nothing loaded from the internet.

Style: clean, premium product launch. Background [BG], text [TEXT], one accent [ACCENT], font [FONT] or a system sans-serif. Generous space. Product screens float on soft shadows with slow push-ins. One sentence is split across the beats and each fragment lands with a short, confident move.

Banned: typewriter reveals on headlines (typing belongs only inside the product's input box), glow, bouncing, gradients on text, stock-photo people, fake testimonials, any number I did not give you.

Beats: follow my beat sheet exactly, with its timings.

Build rules: work out every frame from the time alone. Add window.seek(seconds) that draws that exact moment. Autoplay on a loop when opened normally, wait for seek when the URL has ?render.

After the build: capture one frame from the middle of every beat. Check for cut-off text, overlapping elements, anything unreadable at phone size, and any word or number not in my brief. Fix what is real and keep the first version.
```

## Step 4: Check it like a buyer

- Would a stranger know what's launching by second 4?
- Is every number traceable to a source?
- Does the call to action hold for at least 3 seconds?
- Is it readable on a phone, with the sound off?

## Step 5: Export

HyperFrames (free, open source): `npx skills add heygen-com/hyperframes`, then `npx hyperframes render`. Export a 16:9 and a 4:5 cut. Check which tools exist before installing, and ask first.
