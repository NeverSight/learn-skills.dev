---
name: motion-effects
description: Build any of 16 premium motion effects from scratch in your own brand, as one 8-second looping HTML file with window.seek(seconds) so it exports frame-exact to MP4 or GIF. Interfaces (button to player, search to results, card to workspace, tabs to panels), data (chart morph, dashboard zoom, spring stack, magnetic dock), type (masked type, elastic type, text to layout, image reveal) and systems (perspective shift, glass focus, flowing paths, particle logo). Use when someone says "build the chart morph", "make a button that turns into a video player", "animate my logo with particles", "motion effect", "UI animation", "product animation", "animated dashboard", "kinetic type" or names any of the 16 effects.
---

# Motion effects, built in your brand

Sixteen effects that make a product, a number or a word move like it was made by a motion designer. Each one is a recipe: what it is, where it starts, where it ends, when each part moves inside an 8-second loop, and the one detail that makes it look premium. You pick the effect, give it your real words, and it gets built from scratch in your colours and type.

**Before you start:** read `brand.md` and `MOTION.md` if they exist. If not, run `brand-intake` first, or ask for hex codes, a font and a logo file. Never call a result on-brand without them.

## Step 1: Ask for four things, then wait

1. **The effect.** One of the 16 by name or number. If they describe a job instead ("show our pricing", "reveal the launch name"), suggest the two effects from the table below that fit best and let them pick.
2. **The real content.** The words, labels and numbers that go in it. Real figures, or say they are samples.
3. **The size.** 1080 x 1080 (square), 1080 x 1350 (LinkedIn portrait), 1080 x 1920 (Reel) or 1920 x 1080 (YouTube).
4. **Loop or hold.** Loop repeats forever (a post or a GIF). Hold plays once and stays on the finished frame (under a voiceover, so it never resets mid-sentence).

| # | Effect | Use it when you |
|---|---|---|
| 01 | Button → player | add a "watch the demo" moment to a landing page or launch email |
| 02 | Search → results | show what people find in your help centre or content library |
| 03 | Card → workspace | announce a feature, and one small card becomes the whole editor |
| 04 | Tabs → panels | compare plans, packages or channels without a wall of text |
| 05 | Chart morph | drop a weekly result into a client report or results post |
| 06 | Dashboard zoom | pull the one KPI that matters out of a dashboard |
| 07 | Spring stack | show three offers, case studies or testimonials in turn |
| 08 | Magnetic dock | show the tools you use, or a product's integrations |
| 09 | Masked type | reveal a campaign name, issue number or launch headline |
| 10 | Elastic type | open an event, webinar or podcast with a title card |
| 11 | Text → layout | turn a headline into a carousel cover or article teaser |
| 12 | Image reveal | tease a product drop, then swap in your own photo |
| 13 | Perspective shift | explain the layers of a service, brand system or stack |
| 14 | Glass focus | make people read the one line of a report that matters |
| 15 | Flowing paths | show one piece of content feeding several channels |
| 16 | Particle logo | close a video, reel or post on your mark |

## Step 2: Read the recipe

Open `references/effects.md` and read the chosen effect in full: start state, end state, timing, the premium detail. The recipe is the spec. Swap the demo words for the user's real ones, and map every colour role (ground, surface, ink, muted, accent, second accent) to a colour in MOTION.md.

## Step 3: Build it

Build one self-contained file, `effect.html`, to these rules:

1. **One clock.** Every frame is worked out from the time alone. Add `window.seek(seconds)` that draws the exact frame for that moment, in any order, as often as it is called. No `setTimeout`, no CSS animations running on their own, no randomness that is not seeded.
2. **One loop, 8 seconds.** Move from 0.0 to 2.2, hold to 6.6, return by 8.0. `seek(0)` and `seek(8)` must draw the same frame. In hold mode, play the move once and stay on the finished frame from 6.6 onwards.
3. **Back to the start.** The return eases every element back to exactly where it began. Nothing snaps home.
4. **Real content, never lorem.** The user's words and numbers. Sample numbers carry a visible "illustrative" or "example" label on every frame.
5. **Self-contained.** Fonts embedded, images inlined, no network requests, so it opens offline and renders the same every time.
6. **Autoplay unless told not to.** Play in real time when opened in a browser, and stop the clock when the URL ends in `?render`, so an exporter drives `window.seek()` itself.
7. **Scale the effect up.** It fills the frame at the chosen size, with margins from MOTION.md. It is not a small tile in a big empty canvas.

## Step 4: Check it before you show it

Capture frames at 0, 1, 2.2, 4.4, 6.6, 7.9 and 8 seconds and look at every one.

- **The loop:** frame 0 and frame 8 are identical.
- **The move:** frames 0, 1 and 2.2 are all different. If two match, part of the effect is not running.
- **The fit:** no text runs past its box, and nothing is cut off at any of the seven moments.
- **The still:** pause on 4.4. The point of the effect reads from that single frame.
- **The brand:** every colour and font on screen is in MOTION.md.

Fix what fails, capture again, and only then show the user the 2.2 and 4.4 frames with the file path.

## Step 5: Export it

```
Now turn effect.html into a video and a GIF I can post. Use tools already on this computer. If you need something that is not installed, stop and tell me what it is before you install anything. Load the page with ?render, call window.seek() for every frame at 30 frames per second (240 frames for 8 seconds), and encode an MP4 in H.264 at [SIZE]. Then make a GIF that loops forever. Show me three frames from the finished GIF so I can check it came out right.
```

HyperFrames (`npx skills add heygen-com/hyperframes`) does this in one step if it is installed.

## What I learned the hard way

- **"Make it premium" means one object changing shape.** Every one of the 16 effects is a thing turning into another thing: a button into a player, bars into a line, a card into a window. A fade from one picture to another looks cheap every time.
- **The hold is where people actually look.** 4.4 of the 8 seconds is the hold. If nothing moves in it, the loop feels dead. Each recipe keeps something small alive there: a progress bar, a cursor, a second wave of light.
- **A ghost of the start state sells the change.** A faint outline left where the button or card began lets the eye follow the move. Without it the end state looks like it appeared from nowhere.
- **Stagger by a beat, not all at once.** Rows, slats, letters and dots each start a fraction later than the last. Everything moving together reads as a slide transition.
- **Frame 0 drew in the wrong font.** An embedded font does not load until something uses it, so the first frame can paint in a fallback. Load every font explicitly before the first `seek(0)`.
- **Scale it up, do not redraw it.** An effect drawn with fixed coordinates ends up in one corner when you just change the canvas size. Scale the whole drawing to fill the frame instead.
- **A blank page is usually a name declared twice.** Copying helpers between files duplicated a colour constant and stopped the whole script. Declare each name once, and paste the red console error back to Claude if the page is empty.
- **Eight seconds is too slow for a Reel cut.** A full loop dropped into Instagram B-roll failed a motion check. Cut the active move (about 1.4 seconds of it) and use hold mode under narration.
- **Pick one unit for time and keep it.** The exporter and the page must agree on seconds or milliseconds. This pack uses seconds everywhere.
- **Label made-up numbers on the frame.** I made up every figure on my own board for the demo, so every effect carries an "example" label until real numbers go in.

## Hand off

Give the user `effect.html`, the MP4 and the GIF, with the three checked frames. Then offer the next step in one line: another effect from the same group, or `reel-export` to turn it into a vertical Reel with safe-zone text.
