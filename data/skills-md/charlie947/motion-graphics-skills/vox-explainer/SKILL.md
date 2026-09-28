---
name: vox-explainer
description: Make a short Vox-style documentary explainer (30-60 seconds) entirely in code with Claude Code. Torn paper, halftone texture, bold condensed type, motion on twos. Use when someone says "make a Vox-style video", "explainer video about...", "why does X happen", or wants a documentary-style motion graphic for LinkedIn, Instagram or YouTube without After Effects or a video generator.
---

# Vox-style explainer, built in code

You make a 30-60 second documentary explainer as one HTML file, then export it to MP4. Every frame is code. No video generator, no stock footage.

**Before you start:** read `brand.md` and `MOTION.md` if they exist. If not, run `brand-intake` first, or ask for hex codes, a font and a logo file. Never call a result on-brand without them.

## Step 1: Ask for four things, then wait

1. **The question.** One "why" question a stranger half understands. Example: "Why does every brand logo look the same now?"
2. **The facts.** Names, dates and numbers that answer it, each with a source link. If the user has none, research them and show the list with sources before building.
3. **The colours.** Three hex codes plus one accent. Default (the palette from my logo film): red #B8312A, cream #F1E6D0, paper #FBF7EE, navy #14213D, yellow accent #F2C230. Label defaults as defaults.
4. **The size.** 1920 x 1080 (YouTube), 1080 x 1350 (LinkedIn feed) or 1080 x 1920 (Story or Reel).

Do not start building until every fact on screen has a source.

## Review rules (from the rounds that got rejected)

- **Sound is not optional.** A silent explainer feels unfinished. Write a score in code: a low bed, a hit on each new shot, a lift on the last line.
- **Cards and images, not lines.** A single bar or line moving across the screen reads as static. Every shot uses cards, real images or objects that move in depth.
- **Logos fill their card** and come from the real files. A logo floating small in a big box looks wrong.
- **Keep grids symmetrical.** Equal card sizes, equal gaps. A lopsided layout reads as a mistake.
- **The voice sits on top.** If you can't hear the narration over the effects, drop the score until you can. A voice track (your own, or a text-to-speech one) carries a "why" film.
- **The opening line has to promise what's coming.** A small title that undersells the film loses people before the good bit. Say the question big, then show the first surprise within 5 seconds.
- **Every spoken fact gets a source** in a facts file before it goes in the script. Say "looks like", never "is", when the research only shows a similarity.
- **Stunning or it's not done.** If the first 3 seconds would not stop your own thumb, rebuild them before building the rest.

## Step 2: Write the script, one line per shot

- 8-14 shots. One sentence each. Shot 1 is the question itself.
- Every shot answers something the line before it said. If you cannot say what a shot proves, cut it.
- The last shot is the takeaway, in five words or fewer.

Show the script as a numbered list and wait for a yes.

## Step 3: Pick a shot type for each line

| Shot | Use it for |
|---|---|
| Kinetic statement | One sentence you want remembered. Three short lines of bold condensed type on a torn paper strip. |
| Paper cards | Showing several things at once (logos, products, quotes). Torn-edge cards drop in with small shadows. |
| Before / after | A change over time. Same card, date chip flips. |
| Label call-out | Naming one thing inside a picture. A marker circle draws itself, then a label. |
| Counter | A number that grows. Built in code, never guessed. |
| Grid | "They all look the same." Many identical tiles, then one breaks the pattern. |

## Step 4: Build it

Paste this build brief into Claude Code with the script and shot list underneath:

```
Build one self-contained HTML file called index.html. No external fonts, images or libraries unless I attached them. Nothing loaded from the internet.

Look: editorial documentary explainer. Palette strictly [RED], [CREAM], [NAVY] with a [YELLOW] accent. Torn paper cards with small drop shadows. Halftone dots, paper grain and fine film grain over the whole frame. Colour fringing at the frame EDGES ONLY, and a soft vignette. Bold condensed sans-serif type, fully formed as blocks.

Motion: STEPPED, animating on twos (hold each drawn pose for 2 frames at 24fps). Never smooth corporate easing. NO typewriter effect. No gradients on text, no glow, no bouncing.

Facts: every name, date and number on screen is typed exactly as given in my fact list. Add nothing I did not give you.

Timing: follow my shot list. Each shot holds long enough to read aloud.

Build rules: work out every frame from the time alone. Add window.seek(seconds) that draws that exact moment. The last frame can differ from the first (this is a film, not a loop).

After the build: capture one frame from the middle of every shot. Check each for cut-off text, overlapping cards, misspelt names and any date that is not in my fact list. Fix what is real and keep the first version.
```

## Step 5: Check it like an editor

Before export, go through every frame capture and confirm:
- Every date and name matches the fact list, character for character.
- No card covers another card's text.
- Nothing is smooth that should be stepped.
- The first 3 seconds already show the question (people decide in 3 seconds).

## Step 6: Export

Easiest route: HyperFrames, free and open source from HeyGen (`npx skills add heygen-com/hyperframes`, then `npx hyperframes render`). Any tool that steps through window.seek and saves frames as MP4 also works. Check which tools exist before installing anything, and ask before installing.

## What this skill will not do

- Invent a fact, a date or a quote.
- Recreate a real brand's logo from memory. Use the user's files or plain type set in the brand's name.
- Claim a trend is caused by one thing. Say "one reason", not "the reason".
