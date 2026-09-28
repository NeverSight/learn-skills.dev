---
name: milestone-reveal
description: Make a 12-second looping milestone clip in code with Claude Code. Thousands of tiny points drift like a night sky, pull together into your real number (followers, subscribers, revenue, customers), a line draws underneath and the label settles in. Premium, not a party. Use when someone says "milestone video", "celebrate 10k followers", "animate my subscriber count", "number reveal", "particle number animation" or wants to mark a result on LinkedIn or Instagram.
---

# Milestone reveal, built in code

Each point is one follower, one subscriber or one customer. They gather into the number, hold, then drift apart so the loop has no jump.

**Before you start:** read `brand.md` and `MOTION.md` if they exist. If not, run `brand-intake` first, or ask for hex codes, a font and a logo file. Never call a result on-brand without them.

## Step 1: Ask for four things, then wait

1. **The number, exactly as it should read,** with commas. Example: "250,000".
2. **Where it comes from.** A screenshot or link to the dashboard that shows it. No source, no clip.
3. **The label,** word for word. Example: "LinkedIn followers".
4. **Brand and size.** Background, particle and accent colours, the font file (attached), and the size. Default 1080 x 1350, 12 seconds.

The number is the user's real, sourced number. Never round it up, never add "+", never swap a target for a result. If the source shows 12,431, the clip says 12,431 or the user picks a lower round figure themselves.

## Step 2: Build brief (paste into Claude Code)

```
Build one self-contained HTML file (canvas) for a 12-second seamless loop at [WIDTH] x [HEIGHT]. Tone: premium product launch, not a party. No bounce, overshoot, confetti or sparkle bursts.

Fixed text (real figure, do not alter, round or restyle): "[NUMBER]" and "[LABEL]". No other text on screen.

Brand: background [BG], particles and number [INK], accent line [ACCENT]. Font: the attached [FONT] files, embedded as base64. If the font file is missing, stop and ask me.

Particles: about 3,200 tiny points with varied opacity and a faint twinkle, like a night sky. Build the number's shape by drawing "[NUMBER]" in the bold weight on an offscreen canvas and sampling its filled pixels as targets. Give most points to the number so it reads crisply at feed size, comma included. The rest stay as dimmer drifting stars.

Timing:
1. 0-2s: points drift. Nothing else.
2. 2-6.5s: points pull into the number with a long, staggered ease, like gravity, not a snap.
3. 6.5-7.5s: a thin [ACCENT] line draws left to right under the number.
4. 7.5-8.5s: the label fades in and rises about 12px into place.
5. 8.5-10.5s: hold. The number only shimmers.
6. 10.5-12s: label and line fade, points drift back to their exact start. Frame 12 matches frame 0.

Build rules: a fixed random seed for every position. Add window.seek(seconds) that draws any exact frame from the time alone. Reduced-motion shows the held frame.

After the build: capture frames at 0, 2, 4.5, 6.5, 7.5, 9.5, 11 and 12s. Check the number reads exactly "[NUMBER]", nothing is cut off or overlapping, and frames 0 and 12 are identical. Keep each earlier version when you fix something.
```

## What I learned the hard way

- **The number looked grey at feed size.** Too few points covered each digit. The fix: about 2,700 of 3,200 points on the number, each 2.5px at near full opacity.
- **Chrome can draw the same frame two ways.** After repeated pixel reads it switches drawing mode, so a frame came out slightly different. Create the canvas context with `willReadFrequently: true` and every seek gives the same pixels.
- **Seed everything.** A `Math.random()` at render time makes every export different and breaks the loop.
- **Measure the seam, do not eyeball it.** My passing build had 0 pixels different between frame 0 and frame 12.

## Step 3: Export

HyperFrames (free, open source): `npx skills add heygen-com/hyperframes`, then `npx hyperframes render`. 1080 x 1350 for the LinkedIn feed. For a Reel, hand the MP4 to `reel-export`. Put the source of the number in the caption.
