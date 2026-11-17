---
name: stick-scene
description: Make small hand-drawn stick-figure scenes for landing pages and sites, where a stick figure works a machine or prop that shows what a product does (pull a lever, pin a note, stamp a page). Each one is an interactive canvas widget, `<stick-scene>`, that idles quietly and plays one short action on click, hover or scroll into view. Use when the user asks for a stick figure animation, a "worker" or "crew" scene, an animated explainer or doodle widget for a landing page, something "like the stick figures on my story page", or wants a product's feature shown as a little animated scene.
---

# Stick scene

A stick figure in Kamran's ink-and-butter style does one job that shows what a product does. The scene idles (breathes, glances, scratches its chin) and plays one 5–8 second action when triggered, then settles back. It is one `<canvas>` inside a `<stick-scene>` element, with no dependencies.

Everything here is proven on ~90 scenes on kamranahmed.info/story. Start from those patterns; don't invent a new drawing style.

## Files

- `runtime/stick.js`: the whole runtime. The rig (figure, poses, easing, pen), a kit of props, the stage and the `<stick-scene>` element. Copy it into the project's static folder unchanged.
- `templates/scene.js`: the starting point for a new scene.
- `templates/preview.html` + `scripts/frames.mjs`: render a scene frozen at chosen moments into one contact sheet, and report errors.
- `scripts/motion.mjs`: steps a scene at 60 fps and reports glitches a still frame can hide: joints that snap, an arm through the face, a prop drawn over a head, an elbow bent the wrong way or jutting out behind, a squashed turn, sliding feet, a hand that falls short, and a pop where the action starts or ends.
- `references/craft.md`: API cheat sheet, pose cookbook, timing recipe, prop recipes, metaphor catalog and the mistakes already made once. Read it before writing a scene.
- `examples/`: real scenes. `diffity-review.js` (comment → agent fixes → approve, two figures, a board and a desk) is the cleanest full example. `scenes-p3.js` and `scenes-p4.js` hold ~30 more; the metaphor catalog in craft.md says which is which.

## Workflow

1. **Understand the product.** One line each: what the user does, what they get. Read the landing page or README if there is one.
2. **Pitch 2–3 metaphors** and let the user pick, unless they told you to just go. One line per idea: the prop, the action, the payoff. A good one is physical (lever, stamp, conveyor, pinboard, rail of frames, crate stack), reads in one glance without the caption, and ends on a visible result (a tick, a stamp, something rising or lighting up). See the catalog in craft.md.
3. **Write the scene** from `templates/scene.js`. Lay out props in fixed world coordinates first, then the idle, then the action as a timeline over `T` seconds. Give `label` a plain sentence for screen readers.
4. **Check it with the contact sheet.** Look at every sheet before calling it done:
   ```sh
   # once, in a scratch dir:  npm i playwright@1.56.1
   NODE_PATH=<scratch>/node_modules node <skill-dir>/scripts/frames.mjs \
     --scene <id> --src path/to/scene.js \
     --frames "idle:0,idle:2.5,s:0.8,s:1.6,s:2.4,s:3.2,s:4.0,s:5.0" --fw 400 --out /tmp/<id>.png
   ```
   `<skill-dir>` is the folder this SKILL.md is in. Then Read the PNG. `idle:<sec>` freezes the resting loop, `s:<sec>` a moment in the action, `u:<0..1>` a fraction of it. Add `@<n>` to render the nth play (`s:2.4@1`), so scenes that vary with `S.n` get every variant checked. Fix and re-render until: nothing is cropped at the edges, no prop covers a face or the thing being explained, every beat reads on its own, text sits inside its box with room above and below, hands are in front of what they hold, held things meet the body where a real one would (a mic at the mouth, a handle in the palm), arrows are hand-drawn chevrons, not filled triangles, and the last frame matches the idle (no pop when it loops back). Two or three rounds is normal.
   Then check the motion, which the sheet can't show:
   ```sh
   NODE_PATH=<scratch>/node_modules node <skill-dir>/scripts/motion.mjs --scene <id> --src path/to/scene.js
   ```
   Fix every `jump` (blend the pose instead of switching it), `arm-through-face`, `head-covered` (a prop, note or bubble drawn over a face), `bent-back-elbow`, `elbow-out-back` (a broken-wing arm held for more than a moment), `squash`, `start-pop` and `end-pop` until it prints "motion is clean". A short `skate` at the very start or end of a walk is fine.
5. **Embed it.** Copy `runtime/stick.js` and the scene file into the site's static folder and add:
   ```html
   <stick-scene scene="<id>" play="view" style="height:230px; max-width:560px"></stick-scene>
   <script src="/scenes/stick.js" defer></script>
   <script src="/scenes/<id>.js" defer></script>
   ```
   In Astro use `<script is:inline ... defer>`. `stick.js` must come before every scene script in document order (deferred scripts run in order and scenes read `window.RIG` on load). On a landing page with several scenes, put each in a frame so it doesn't float on a bare ground line: a rounded card with a 1px border, white background, a faint dot grid (`radial-gradient(#e6e6e6 1px, transparent 1.2px)` at 14px) and the floor band kept on (no `no-floor`); the ground line then runs edge to edge like a little stage. Give every scene on the page the same frame and full content width. Then load the real page in a headless browser, scroll the element into view, wait ~3 s and screenshot desktop and phone widths.

## The element

- `scene`: the id registered as `SCENES['<id>']`.
- `play`: `view` (plays once when half visible, then on click; best default for landing pages), `click`, `hover` (loops while the mouse is over it, click on touch), `loop` (always running, use sparingly), `idle` (never plays).
- `no-floor`: drop the light grey band under the ground line. Use on plain white pages. `no-ground`: drop the line too.
- `zoom`: scale the drawing up or down inside the box (default 1).
- `label` or `aria-label`: what the scene shows. Defaults to the scene's `label`.
- `no-font`: don't load Balsamiq Sans from Google Fonts (when the site already self-hosts it or must not call Google).
- Size it with CSS. The drawing fits the height (230px is the native size) and the scene's `width` in world units, centred.
- Reduced motion shows one still frame and never plays. Off-screen scenes don't draw.
- `STICK.theme({ butter: '#…', greenInk: '#…' })` swaps palette colours for the whole page. Prefer local colour constants in the scene (like the GitHub add/delete greens in `diffity-review.js`) when only one scene needs them.

## Style rules

- Ink `#141414`, white paper fills, one butter or accent highlight, lots of empty space. Balsamiq Sans at 8.5–11px for any words, and only a few words.
- The figure is the hero: never hide its head or the active hand behind a prop. Draw props first, then figures, then things held or flying.
- One idea per scene. If you need a caption to explain it, the metaphor is wrong.
- Show the result, not the work: end on something that changed state and stays for a beat.
- Physical objects over drawn animals or detailed characters. A second figure (a helper) gets a single colour via `ink`/`far`. An AI agent is a robot: `fig(..., { ink: '#d97757', far: '#e8b7a3', bot: { col: '#d97757', dark: '#a8553a', glow, blink, happy } })` draws a rounded head with a dark visor and glowing eyes, ear bolts, an antenna bulb and a chest light. A second agent goes teal (`#3d7a8c`, dark `#2a5866`, far `#a9c9d1`). A black agent also works: a dark `col` gets a white visor and ink eyes automatically. Light `glow` while it works, `happy` when it's done, and put a small label (`you`, `agent`, `claude`) under each figure at `y = 16`.
- Agents shouldn't react instantly. Hold a beat after a request lands (a `thinking…` line, a `hmm…` bubble, a hand to the chin, a slow antenna blink) before the work starts.
- Don't use other companies' logos. Product names as plain text on a prop are fine.
