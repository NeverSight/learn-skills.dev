---
name: model-showdown
description: Give the same motion brief to three AI models, keep each first try, render all three the same way and stack them into one comparison video with model names and logos. Makes a 16:9 side-by-side for a newsletter and a 1080 x 1920 stacked reel for Instagram and TikTok. Use when someone says "compare three models", "same prompt three AIs", "model showdown", "which AI is the best motion designer", "side by side comparison video" or wants a fair head-to-head of AI outputs.
---

# Model showdown, three AIs on one brief

A fair test people can see for themselves. One brief, three models, first try each, one renderer.

**Before you start:** read `brand.md` and `MOTION.md` if they exist. If not, run `brand-intake` first, or ask for hex codes, a font and a logo file. Never call a result on-brand without them. The brand applies to the headline and labels, never to the models' outputs.

## Step 1: Ask for four things, then wait

1. **The brief,** word for word. Every model gets the exact same text.
2. **The three models,** named exactly as their makers write them, and how the user reaches each one (their own accounts only).
3. **The logo files** for each model, attached. Never redrawn from memory.
4. **The headline,** two short lines. Example: "Same prompt." / "Three AI models."

## Step 2: The fair-test rules

- **First try only.** No re-rolls, no fixes, no "one more go" for the one you hoped would win.
- **The models write HTML, you render it.** Add this to the brief so no model gets a better export:

```
Deliver ONE self-contained index.html, [WIDTH] x [HEIGHT] px. Output the complete HTML only. A shared renderer will execute window.seek(t) and export each model's output at the same settings.
Implementation: deterministic window.seek(seconds), wrap modulo [SECONDS], every visual state derived from time. Automatic playback when not in ?render mode. Under ?render freeze until seek. Set window.__ready=true after initialisation. No external requests. Do not add controls, debug text, the model name or screenshots.
```

- **Same renderer, same settings** for all three: same size, 30fps, same length, same encoder.
- **A failure stays in.** If a model returns broken HTML or nothing, its panel says so. Never swap in a later try.

## Step 3: Stack them

**Newsletter (16:9):** three panels side by side, each with its model name above it on a plain strip.

**Reel (1080 x 1920):** three 1080 x 360 panels stacked at y 540, 900 and 1260, over a dark background. Build a transparent 1080 x 1920 `overlay.png` in HTML holding the headline and the three labels, then:

```
ffmpeg -y -i a.mp4 -i b.mp4 -i c.mp4 -loop 1 -i overlay.png -f lavfi -i anullsrc=r=48000:cl=stereo -filter_complex "color=c=0x0B0B0F:s=1080x1920:r=30:d=12[bg];[0:v]fps=30,scale=1080:360:force_original_aspect_ratio=increase,crop=1080:360,setsar=1[a];[1:v]fps=30,scale=1080:360:force_original_aspect_ratio=increase,crop=1080:360,setsar=1[b];[2:v]fps=30,scale=1080:360:force_original_aspect_ratio=increase,crop=1080:360,setsar=1[c];[bg][a]overlay=0:540[t1];[t1][b]overlay=0:900[t2];[t2][c]overlay=0:1260[t3];[t3][3:v]overlay=0:0,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[out]" -map "[out]" -map 4:a -t 12 -c:v libx264 -crf 18 -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 128k -movflags +faststart showdown-reel.mp4
```

Change `d=12` and `-t 12` to your length. The crop keeps the centre, so check one frame per panel and move the crop if the action sits off-centre.

## What I learned the hard way

- **A logo over footage vanishes on light frames.** Every label (logo plus model name) sits on its own dark rounded tile in the top-left of its panel.
- **Safe zone.** The headline sits between y 360 and 520. No word or logo goes below y 1420 or into the right 120px, where the app draws its buttons and caption.
- **Label with the full model name,** version included. "Opus 5.5", not "Claude".
- **End the caption on a question.** Mine asked "Which one would you post?" and gave my own pick.

## Step 4: Check and export

Pull one frame from the middle. Can you read every label at phone size? Is each logo the right company? Then run the checks in `reel-export` before you upload.
