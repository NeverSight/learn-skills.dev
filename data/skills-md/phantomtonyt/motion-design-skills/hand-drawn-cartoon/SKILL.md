---
name: hand-drawn-cartoon
description: Hand-drawn storybook cartoon videos - wobbly inked outlines that boil, paper grain and crayon hatching, flat muted colours, simple round characters with big expressive acting - built in code (SVG + GSAP in HyperFrames) and rendered to MP4 at 9:16 or 16:9. Use for cute explainers, character stories, mascot shorts, fables and any request for a handmade, doodly, storybook or less-corporate look. Not for clean flat vector (use flat-vector-explainer), 3D characters (use 3d-toy-character) or text-only videos (use kinetic-typography).
license: MIT
compatibility: HyperFrames (Node 22+, FFmpeg) with GSAP and inline SVG. Fonts from Google Fonts.
---

# Hand-drawn Cartoon

A small character acts out one idea on a paper stage. The lines are inked and slightly alive, as if redrawn every couple of frames. It should feel handmade, warm and funny, like a storybook page that moves.

## Options

| Option | Default | Notes |
|---|---|---|
| format | vertical 1080×1920 | or landscape 1920×1080, square 1080×1080 |
| duration | 15 s | 10–45 s works best |
| tone | playful | `calm` (longer holds, gentle easing), `playful` (default), `slapstick` (bigger squash, faster gags, more cuts) |
| character | a simple round character | or the user's own (match its silhouette and colours) |

Users can say these in plain words: "vertical, 20 seconds, slapstick".

## Brief (answer before planning)

1. What is the one idea or joke, in a sentence?
2. Who is the character, and what does it want?
3. What goes wrong first, and what is the twist or payoff?
4. What is on screen in the first second (the hook)?
5. What line or title closes the video?

Then write a beat list: time, what we see, the character's action, any text, any sound. Durations add up to the target. Default shape: hook (1.5 s), try and fail, idea, attempt, payoff, end card.

## Reads sheet (write it with the beat list)

For every beat, write the one thing the viewer must understand ("the robot can't fly", "the cache missed") and how long it stays readable. One read at a time. Text floors: a label stays at least 0.8 s, a sentence about 0.3 s per word once fully on screen. If the text won't fit the time, cut words rather than speed up.

## Motion discipline

- Motion is causal: the character reacts to something on screen, and every action has a cause and a consequence.
- Characters are never frozen: they breathe, blink and shift weight while waiting. That idle is acting, not filler, so keep it small and irregular.
- Avoid twinning: the arms don't move as mirror images, and the eyes, antenna and body don't all start on the same frame. Offset parts by 2–4 frames.
- Overshoot and squash belong to the character (landings, pops, surprise). The camera and text move with smooth ease-outs.
- Keep one main direction of travel per scene, and carry the character or a prop across scene changes instead of crossfading.
- Add a 0.3–0.75 s held pose right before the payoff, so it lands.

## Style rules (always)

1. Every line is a dark warm ink (`#2b1d16`-ish), 5–8 px at 1080 width, round joins. Never pure black.
2. Lines boil: the whole ink layer gets one of 3 slightly different displacement filters, swapped every 2 frames (12 fps). Without boil it reads as clean vector.
3. Paper is always there: a warm off-white ground, a faint grain overlay and a soft vignette.
4. Shading is crayon hatching or one flat darker tone. No gradients on characters.
5. Characters are round and simple: a big head or body, dot or oval eyes with a white glint, a tiny mouth and stubby limbs. They act with the whole body.
6. Every action gets anticipation, then the move, then squash on contact and a settle.

## Defaults and overrides

Precedence: the user's brand or spec, then the explicit request, then these defaults. If the user gives brand colours, use them for the character and one accent. Keep the ink, paper and grain.

- Paper `#efe6d2`, light paper `#fbf6ea`, ink `#2b1d16`, accent `#b8402f` (titles, key props), sky wash `#b9d8e8`, sun or idea yellow `#f5c842`, character colour `#7fb6c9`.
- Fonts: Caveat Brush for titles and Patrick Hand for labels (Google Fonts). Titles 80–110 px in 9:16.

## Setup (once)

```bash
node -v && ffmpeg -version
npx hyperframes init my-video --non-interactive --resolution portrait && cd my-video   # landscape for 16:9
```

In an existing empty folder use `npx hyperframes init . --non-interactive --resolution portrait`, then replace `index.html` with your composition.

## Route

| Need | SVG + GSAP in HyperFrames (default) | p5.js + p5.brush (canvas) |
|---|:-:|:-:|
| Inked outlines with boil | yes (displacement filters) | yes (re-seeded brush jitter) |
| Watercolour washes and dry-brush texture | approximate (grain, hatching) | yes |
| Fast renders without a GPU | yes | slower |
| Characters with named, reusable parts | yes | harder |

Default to SVG + GSAP. Use p5.brush only when real painted washes are the point; then draw every frame from time `t` (no randomness without a fixed seed).

## Visual language

- **Stage:** floor line or rooftop or table edge, one or two props, a sky or wall. Shapes are slightly irregular (hand-drawn paths, not perfect rects).
- **Depth:** a far layer (sun, clouds, hills), a mid layer (the stage) and a near layer (props or clouds passing the camera). Move the camera by moving a world group; far layers move less.
- **Character parts:** separate groups for body, eyes, mouth, each arm and any antenna or ears, so each can act. Size the character with a wrapping group (`<g transform="scale(1.7)">`) and animate x, y and rotation on the outer group. Scaling the animated group itself shifts it, because SVG transforms default to the top-left origin.
- **Squash and stretch:** around the feet, with `svgOrigin` set to the feet point in the character's own coordinates (e.g. `svgOrigin: "0 6"`). Keep volume: 10% taller means about 5% narrower.
- **Effects:** dust puffs (circles that grow by animating the `r` attribute and fade), dizzy stars orbiting, speed lines, sparkles. All of them are inked too.

| Move | Timing |
|---|---|
| Anticipation squash | 0.1–0.12 s |
| Jump up | 0.4–0.5 s, `power2.out` |
| Comic hang at the top | 0.3–0.5 s |
| Fall | 0.25 s, `power3.in` |
| Impact squash | 0.08 s, then an elastic settle over 0.5 s |
| Blink | 0.12 s, every 2–4 s, irregular |
| Head tilt | 0.3 s, 8–12° |

## Make it eye-catching

- The first frame is a finished picture: stage, character, sky and a title on a hand-drawn card.
- Something moves in every beat: birds, a slowly turning sun, drifting clouds, antenna wobble, blinks.
- One big moment uses the camera: follow the character upward or sideways with parallax layers.
- One accent colour for the key prop and the title's key word. Everything else is muted.
- Gags read in silhouette: the fail is a full squash with dust and stars, and the success is a big readable pose.
- The last frame matches the first (same framing, same pose), so the video loops.
- Every frozen frame should be worth posting. If a snapshot looks empty or flat, it isn't done.

## Starter

```html
<div id="root" data-composition-id="main" data-start="0" data-duration="15" data-width="1080" data-height="1920">
<svg viewBox="0 0 1080 1920" width="1080" height="1920">
  <defs>
    <filter id="boil0"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="2"/><feDisplacementMap in="SourceGraphic" scale="4"/></filter>
    <filter id="boil1"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="9"/><feDisplacementMap in="SourceGraphic" scale="4"/></filter>
    <filter id="boil2"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="17"/><feDisplacementMap in="SourceGraphic" scale="4"/></filter>
    <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" seed="5"/>
      <feColorMatrix type="matrix" values="0 0 0 0 .3  0 0 0 0 .24  0 0 0 0 .16  0 0 0 .2 0"/></filter>
    <pattern id="hatch" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="14" stroke="#2b1d16" stroke-width="3" stroke-opacity=".28"/></pattern>
  </defs>
  <rect width="1080" height="1920" fill="#efe6d2"/>
  <g id="world"><g id="ink" filter="url(#boil0)" stroke="#2b1d16" stroke-width="7" stroke-linejoin="round" stroke-linecap="round">
    <path d="M-60 1312 L770 1304 Q810 1306 812 1330 L800 2200 L-60 2200 Z" fill="#c9b79a"/>          <!-- stage -->
    <g id="hero"><g transform="scale(1.7)">                                                         <!-- size here -->
      <g id="body"><circle cx="0" cy="-100" r="92" fill="#7fb6c9"/><path d="M-92 -100 a92 92 0 0 0 184 0" fill="url(#hatch)" stroke="none"/>
        <rect x="-58" y="-128" width="116" height="62" rx="30" fill="#fbf6ea"/>
        <g id="eyes" stroke="none" fill="#2b1d16"><ellipse cx="-24" cy="-98" rx="11" ry="15"/><ellipse cx="24" cy="-98" rx="11" ry="15"/></g>
        <g id="armR"><path d="M88 -92 q40 10 52 46" fill="none" stroke-width="12"/></g></g>
    </g></g>
  </g></g>
  <rect width="1080" height="1920" filter="url(#grain)"/>
</svg></div>
<script>
const tl = gsap.timeline({ paused: true });
for (let i = 0; i < 90; i++) tl.set("#ink", { attr: { filter: `url(#boil${i % 3})` } }, i / 6);   // boil on twos
gsap.set("#hero", { x: 400, y: 1316 });                                                          // feet on the stage
tl.to("#body", { scaleY: 0.85, scaleX: 1.1, svgOrigin: "0 6", duration: 0.1, yoyo: true, repeat: 1 }, 1.7);  // anticipation
tl.to("#hero", { y: 956, duration: 0.45, ease: "power2.out" }, 1.95).to("#hero", { y: 1316, duration: 0.25, ease: "power3.in" }, 2.9);
tl.to("#body", { scaleY: 0.5, scaleX: 1.35, svgOrigin: "0 6", duration: 0.08 }, 3.15)
  .to("#body", { scaleY: 1, scaleX: 1, svgOrigin: "0 6", duration: 0.5, ease: "elastic.out(1,0.4)" }, 4.3);
tl.to("#armR", { rotation: -60, svgOrigin: "88 -92", duration: 0.16, yoyo: true, repeat: 5 }, 13.6);   // wave
tl.set({}, {}, 15);
window.__timelines["main"] = tl;
</script>
```

Add a `<head>` with the GSAP script (`https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js`), the Google Fonts link, and `html,body{margin:0;width:1080px;height:1920px;overflow:hidden}`. Build out the beats from your beat list on the same `tl`.

## Parameters to expose

`format` · `duration` · `tone` · `characterColor` · `accent` · `paper` · `title` · `endLine` · `beats`. Keep them as constants at the top of the script.

## Avoid

- Perfect geometric shapes and clean, unboiled lines (looks like flat vector).
- Gradients, glows and drop shadows on characters.
- Small characters lost in empty space. The character should be 25–45% of the frame height.
- Text over the character's face, and text in the bottom 670 px or top 270 px of a 9:16 frame.
- `Math.random()` or time-of-day logic. Boil and effects must come from the timeline.

## Failure modes

| Looks like | Cause | Fix |
|---|---|---|
| Clean vector, not hand-drawn | no boil, perfect shapes | swap the 3 displacement filters every 2 frames; use hand-drawn paths |
| Character drifts or sinks when scaled | scale animated on the moving group | put size on an inner `<g transform="scale()">`; squash with `svgOrigin` at the feet |
| Effects start in the corner | x/y not set before they appear | `gsap.set` their start position at time 0 |
| Muddy, low contrast | too many mid tones | paper light, ink dark, one accent |
| Stiff acting | moves without anticipation or settle | add the squash before and the elastic settle after |
| Text overlap warning on stacked titles | line boxes of handwritten fonts touch | add 10–20 px between lines; confirm on a snapshot |

## Validate

```bash
npx hyperframes check
npx hyperframes snapshot --at <one time per beat, plus one mid-transition>
npx hyperframes render -o renders/<name>.mp4
```

Look at every snapshot and `snapshots/contact-sheet.jpg`:
- [ ] lines visibly differ between two snapshots 1/6 s apart (boil works)
- [ ] the character stands on the stage (not sinking) and is readable at phone size
- [ ] each beat reads in silhouette; the fail and the payoff are big
- [ ] text inside the safe area; nothing collides mid-transition
- [ ] the last frame matches the first

## Self-critique before the final render

Score the snapshot sheet 1–10 on: hook (first second), readability at phone width, motion quality, composition, accuracy, and the "muted test" (can a viewer summarise it in one sentence with no sound?). Fix only what scores 7 or below, re-snapshot, and repeat until everything is 8 or above. If you can, have a separate read-only pass do the scoring, so you aren't grading your own work.

| Don't | Instead |
|---|---|
| Crossfade between two busy layouts | exit the old content, then bring in the new, or carry one object across |
| Make several things move at once | stagger, one focus per moment |
| Fill pauses with floating or wobble | hold still, or let the character act |
| Add particles, rainbow gradients or 3D flips for "energy" | add a stronger event: a reveal, a hit, a camera move |
| Rush text to fit the time | cut words |

## Deliver

- Pick the strongest settled frame as the poster: `ffmpeg -ss <t> -i renders/<name>.mp4 -frames:v 1 poster.jpg`. Bake it in as frame 0 so thumbnails show it: `ffmpeg -i renders/<name>.mp4 -i poster.jpg -filter_complex "[0:v][1:v]overlay=enable='eq(n,0)'" -c:a copy renders/<name>-final.mp4`.
- Write a 1–2 sentence caption that names the idea, not the technique.
- Tell the user what happens in each beat and which parameter to change for a revision.

## Study these

- @other__reality, "I'm Upping My P(doom)" music video, made in code with p5.js + p5.brush: https://x.com/other__reality/status/2102514581684052169 (open recipe: github.com/JohnHeibel/PDoomVideo)
- @devteamdrew, every Claude effort level as storybook vignettes: https://x.com/devteamdrew/status/2105353836638744578
- @shfred0, "The Life of Opus", procedural brush strokes in JavaScript: https://x.com/shfred0/status/2102495989194236158
- @akokoi1, an ink-wash storybook made purely in code: https://x.com/akokoi1/status/2102699703309898026
- Ideas adapted (not copied) from the HyperFrames motion doctrine and faceless-explainer skills, JohnHeibel/ClaudeAnimationBase's animation guide, howseen-ai/claude-motion-design's critique loop, and latent-spaces/brag.
