---
name: apple-launch-film
description: Rebuild an Apple-style Mac launch film entirely in code with Claude Code. A thin menu bar, the black notch growing into widgets one scene at a time, full-screen gradient wallpapers and one short caption per scene. No screen recording, no After Effects. Use when someone says "Apple-style launch", "Mac launch video", "notch animation", "make it look like an Apple keynote", "macOS UI launch film" or wants a product launch that looks like native Mac interface.
---

# Apple-style launch film, built in code

Every pixel of the Mac is drawn in code: the menu bar, the notch, the widgets and the wallpapers. One HTML file with `window.seek(seconds)`, exported to MP4.

**Before you start:** read `brand.md` and `MOTION.md` if they exist. If not, run `brand-intake` first, or ask for hex codes, a font and a logo file. Never call a result on-brand without them.

**Pairs with a free skill (not mine)** that turns Apple's design guidelines into rules Claude follows. Install it once:

```
npx skills add emilkowalski/skills --skill apple-design
```

## Step 1: Ask for five things, then wait

1. **The product name** and its one line, word for word.
2. **The facts list.** Every feature, number and requirement the film may show. Nothing else goes on screen.
3. **The scenes.** 6 to 8, each one feature plus one short caption. Example: "Your voice lives here."
4. **A reference** (optional): a real Mac launch film or frames of one, in a folder called `ref`. It sets the look only.
5. **Size and length.** Default 1920 x 1080, 30fps, about 2.5 seconds a scene.

## Step 2: Build brief (paste into Claude Code)

```
Use the apple-design skill. [If ref/ exists: Match the LOOK of the reference in ref/. Read every frame first. Do not copy its words or its product name.]

It is a launch film for [PRODUCT]: the black MacBook notch at the top centre grows into Apple-style widgets, one scene at a time. Each scene has its own full-screen colour-gradient wallpaper and one centred caption below the notch, with the last word or two tinted a lighter shade of the wallpaper colour. It opens with the notch expanded and the word "hello" handwritten in a white script line, like the Mac hello screen.

Use only these facts, and add no others:
[FACTS LIST]

Scenes, about 2.5 seconds each:
[1. Notch expanded on black, "hello" handwritten.]
[2..n. Wallpaper colour, what the notch opens into, the caption.]
[Last. Black: the notch closes to its resting shape. Caption: PRODUCT and its one line.]

Size [WIDTH] x [HEIGHT], 30fps. The frame is a Mac screen: a thin macOS menu bar across the top with the notch in the middle of it. System fonts (-apple-system, Helvetica Neue fallback).

Build it as one self-contained HTML file with window.seek(seconds) that draws any exact frame. Capture one frame from each scene [and compare it side by side with the matching reference frame]. Fix what differs, and check the motion against the apple-design skill.
```

## What I learned the hard way

- **Name the notch in words.** Given the same brief, one model drew a whole laptop instead. "The notch at the top centre of the screen" is the anchor.
- **Springs, not tweens.** The notch looks right when width and height spring on their own curves, open soft and close without overshoot.
- **Work motion out from the start of the film.** If the notch reopens before it has finished closing, it carries on from where it is. A per-scene tween jumps.
- **Compare against the reference, scene by scene.** Side-by-side frames caught a "hello" that sat off-centre and too big, a chunky progress bar that should be thin ticks, and a prompt jammed into the menu bar.
- **Keep the menu bar short.** A full menu of words gets cut in half by wide widgets. Five items is plenty.
- **Widgets add no claims.** Placeholder text is grey lines. Any UI word the facts list did not give you (button labels, a clock time) gets listed back for approval.

## Step 3: Check and export

Would a stranger believe it is a real Mac for the first second? Is every word on screen from the facts list? Add a reduced-motion setting that swaps springs for quick fades.

Export with HyperFrames (free, open source): `npx skills add heygen-com/hyperframes`, then `npx hyperframes render`. For a vertical cut, hand the MP4 to `reel-export`.
