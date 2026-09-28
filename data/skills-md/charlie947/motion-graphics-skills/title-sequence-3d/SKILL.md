---
name: title-sequence-3d
description: Make a cinematic 3D title sequence (8-15 seconds) in code with Claude Code and Three.js. A camera moves through a lit scene, such as a rainy street at night with brand names as neon signs, then a big question or title lands. Use when someone wants a scroll-stopping opener, a film-style intro, "3D intro", "cinematic opening", "title sequence" or a hook for a video, reel or newsletter.
---

# 3D title sequence, built in code

The first 3 seconds decide whether anyone watches. This skill builds a short cinematic opener: a camera moving through a lit 3D scene, ending on your question or title.

**Before you start:** read `brand.md` and `MOTION.md` if they exist. If not, run `brand-intake` first, or ask for hex codes, a font and a logo file. Never call a result on-brand without them.

## Step 1: Ask for four things, then wait

1. **The line** that lands at the end. Example: "Why does every brand logo look the same now?"
2. **The world.** One setting that fits the story: a night street, an empty office, a desk at 5am, a stage. Default: rainy street at night.
3. **The objects in it.** Real names or logos as signs, screens or posters. Logo files attached, never redrawn from memory.
4. **Brand and size.** One accent colour for the key word. 1920 x 1080 or 1080 x 1920.

## Review rules (from the rounds that got rejected)

- **Sound is not optional.** A silent explainer feels unfinished. Write a score in code: a low bed, a hit on each new shot, a lift on the last line.
- **Cards and images, not lines.** A single bar or line moving across the screen reads as static. Every shot uses cards, real images or objects that move in depth.
- **Logos fill their card** and come from the real files. A logo floating small in a big box looks wrong.
- **Keep grids symmetrical.** Equal card sizes, equal gaps. A lopsided layout reads as a mistake.
- **Stunning or it's not done.** If the first 3 seconds would not stop your own thumb, rebuild them before building the rest.

## Step 2: Build brief (paste into Claude Code)

```
Build one self-contained HTML file called index.html: a [SECONDS]-second cinematic 3D title sequence at [WIDTH] x [HEIGHT], using Three.js from a pinned version and only the files I attached.

Scene: [WORLD]. Low-poly buildings, wet reflective ground, fine rain. Each object I attached becomes a lit sign: draw the logo file onto a canvas texture, put it on a plane, and give it a soft bloom (UnrealBloomPass, subtle, never blown out).

Camera: one slow, steady dolly forward and slightly up, passing the signs. No shake, no spins.

Title: in the last third, [LINE] lands in bold condensed type, lower left, in white with [KEY WORDS] in [ACCENT]. Keep the ground under the title dark enough that reflections never show through the letters.

Sound (optional): a low drone plus soft rain, written in code, faded in over the first second.

Build rules: every frame is worked out from the time alone, including rain (seeded, never Math.random at render time). Add window.seek(seconds). Wait for seek when the URL has ?render.

After the build: capture frames at 1s, the middle and the last second. Check that every sign is readable at phone size, nothing mirrored sits behind the title, and every logo matches its file.
```

## Step 3: Check it

- Does the first second already look like a film, not a slideshow?
- Is the title readable on a phone?
- Are the small labels (dates, captions) at least twice the size you think they need?

## Step 4: Export

HyperFrames (free, open source): `npx skills add heygen-com/hyperframes`, then `npx hyperframes render`. For email or newsletters, also make a 9-second GIF under 5MB (8fps, 540px wide, light denoise so the rain compresses).
