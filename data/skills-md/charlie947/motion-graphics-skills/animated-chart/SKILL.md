---
name: animated-chart
description: Make a looping animated chart for LinkedIn or a newsletter in code with Claude Code. Bars that become a line, a number that counts up, a before and after. Every value stays exactly as given. Use when someone says "animate my chart", "animated graph", "make my results move", "stat animation" or wants a data graphic that loops.
---

# Animated chart, built in code

Three prompts from a blank page: build it, make it look again, export it.

**Before you start:** read `brand.md` and `MOTION.md` if they exist. If not, run `brand-intake` first, or ask for hex codes, a font and a logo file. Never call a result on-brand without them.

## Step 1: Ask for the numbers, then wait

The title, the labels, the exact values, and whether they are real results or sample data. Sample data gets an "Illustrative data" label on every frame. Never round, reformat or add a number.

## Prompt 1: build it

```
I want one animated graphic for a LinkedIn post. Build it as a single HTML file I can open in my browser.

Title: "[TITLE]". [If sample data: keep "Illustrative data" visible.]
Values: [LABEL 1: VALUE 1], [LABEL 2: VALUE 2], ...

The motion has four states:
1. Start: [what it looks like first].
2. Change: [the one thing that moves]. Nothing fades out and gets replaced.
3. Hold: the finished chart, with [the headline value] labelled.
4. Return: it eases back to the start, so the loop has no jump.

Timing: 8 seconds in total. About 2 seconds for the change, 4 holding, 1.5 to return.

Look: background [BG], text [TEXT], accent [ACCENT], [FONT]. No external fonts or images. No gradients, no glow, no bouncing.

Size: 1080 x 1350 pixels.

Rules for the build:
- Work out every frame from the time alone. Add window.seek(seconds).
- The title, labels and axis never move. Only the chart changes.
- The last frame must match the first frame exactly.

After you build it, take screenshots at 0, 1, 2, 4 and 7 seconds. Check them for overlapping text or anything cut off. Fix what you find and tell me what you changed.
```

## Prompt 2: make it look again

```
Inspect the five captured frames and the loop boundary. Check that the values stay the same, labels are readable, nothing overlaps, and each element appears only when it should. Report only problems you actually observe. Fix any you find, preserve the earlier version, and capture the same frames again. If no problems are found, say so and do not invent a revision.
```

## Prompt 3: export it

```
Now turn this into a video and a GIF I can post. Use tools already on this computer. If you need something that is not installed, stop and tell me what it is before you install anything. Give me an MP4 (1080 x 1350, 8 seconds) and a GIF that loops forever. Then show me three frames from the finished GIF so I can check it came out right.
```
