---
name: interface-bts
description: Draws a spec poster of an interaction you point it at, with the real component paused at its key moments and every duration, curve and size read from it and drawn in place.
disable-model-invocation: true
---

# interface-bts

This skill turns one interaction in a project into an A4 spec poster: the behind-the-scenes drawing of how it moves. The poster has:
- **Figure 1:** the real component, frozen mid-motion, with its sizes dimensioned on it.
- **Callouts:** numbered parts, with a note for each saying what changes and why.
- **Figure 2:** the curve or mapping that drives it.
- **Moments:** a row you can pick to re-drive the component.
- **Specification:** trigger, properties, duration, easing and reduced motion.

A reader should leave with one sentence about how it works.

The poster documents what the interface does now. It isn't a redesign, a live debug overlay or a video. If someone wants a component changed, say so and leave the poster out of it. Every number on the poster comes from the running component; anything that can't be read is marked as an estimate, never filled in.

Example: `/interface-bts the dropdown in components/menu.tsx`

## 1. Study the interaction

- Find the component, its callers, its styles, its handlers and its animation code. Run it and use the interaction yourself.
- Trace input → decision → output:
  - What triggers it?
  - What changes?
  - Which values drive the change (durations, easings, thresholds, sizes)?
  - Where does each value live?
- Probe the cases that show the rules: a slow input, a reversal, an interruption, the resting state, and reduced motion.

**Done when** you can name the mechanism in one sentence and point to the source of each value it uses.

## 2. Agree the poster in chat

List these and wait for a yes before building:

- **Headline:** the mechanism in plain words ("The pill catches up: its left edge and width ease on one curve").
- **Hero moment:** the frame where the mechanism shows most. Usually mid-motion or just past a threshold, rarely at rest.
- **Moments:** three, in story order, the hero among them (start, the hero, settled; or the hero, past it, settled). The row holds three.
- **Callouts:** 2–4 numbered parts on figure 1, with what each note will say.
- **Figure 2:** pick from the table below.
- **Measurements:** the one or two sizes the headline depends on.

| To explain | Figure 2 draws |
| --- | --- |
| How a value travels over time (most transitions) | The easing curve, with the held moment marked on it |
| Two things on one clock (a cross-fade, an icon swap) | Both curves on one time axis |
| A value that follows input (a drag, a scroll) | Input mapped to output, with the clamp and snap points |
| Keyframes or a loop | The keyframe stops over one cycle |
| A threshold or snap | The decision regions, with the current input inside them |
| A spring | The spring's own response over time: past 1 where it overshoots, ending where it comes to rest |

**Done when** the user has agreed the headline and the moments.

## 3. Freeze the real component

- **Figure 1 is the real component.** Drive it with its own handlers, and freeze it by pausing its real animations: `getAnimations()`, then `pause()` and set `currentTime`, or seek the animation library's own timeline. Never rebuild it, and never run a second animation to imitate it.
- **Read every number from the running component:** computed style, `getAnimations()`, its timeline, or data attributes it publishes. Never type a duration, an easing or a threshold into the poster. Take the first timing function with `firstEasing()`: splitting a computed list on commas cuts `cubic-bezier()` in half. A CSS `@keyframes` animation keeps its timing function on its keyframes, not on the animation: `getComputedTiming().easing` reads `linear` for it, so read the keyframes (`stopsOf`) or the element's computed `animation-timing-function`. Name an easing with `easeWords()`, which goes by the curve's shape (in, out or in-out), never by assumption.
- **A component that isn't a CSS transition needs its own driver,** and some fight the poster: anything placed by floating-ui (Radix menus, popovers, tooltips), fixed to the window (toasters, sheets), measuring itself on screen (drag and swipe thresholds), or moving focus. Read [references/drivers.md](references/drivers.md) before building one of these.
- **A spring has no duration or easing of its own.** Read its physics (stiffness, damping, mass) from the running animation, and plot its response from the spring function the library itself runs, sampled without moving the animation. The duration on the poster is when the library calls it at rest; say so. If the library's function can't be reached, plot `springAt()` from the config read off the animation and say the curve is derived. A spring handed to CSS or the Web Animations API arrives as a `linear()` easing, which `easeAt()` reads like any other. See [references/drivers.md](references/drivers.md#springs).
- **Check that channels agree before you show them as one mechanism,** for example that opacity follows the same curve as scale. If they don't, the poster shows its error state rather than a wrong drawing.
- **Moments are copies:** static DOM snapshots with computed styles inlined, and inert. Use one camera for all of them, so growth never reads as shrinkage.
- **Report what you measured,** even when it contradicts what the code intends.
- **Notes and specification are written from the held values, never typed.** Every number in them comes from `m` (or whatever your driver holds), so a change to the component changes the poster: write `{m.gap}px`, never `10px`, and don't write fallbacks like `m?.gap ?? 10` (pass the notes only once `m` exists). A rule the component can't report at runtime, a library constant such as a close threshold, goes in one named constant with its source in a comment, and a moment should show it at work (released just under it, and just over).

**Done when** each moment re-drives the component to the same frame every time, the held values match the source, and (for a driven gesture or pointer path) one run has been checked against a real browser mouse or touch.

## 4. Compose the poster

- **All posters on one page.** Each poster is built in its own folder, and every one of them is shown together on one page (`/specs`): a row scrolled sideways, `SpecStrip` in the kit. Add each new poster to it. A poster's own route can stay for working on it alone.
- **The toolbar on that page** lets the reader set every poster's paper (the poster's own white or black, a pale grey, a mid grey, a blueprint blue, or any colour), accent (each poster's own, five system colours, or any colour), orientation (portrait or landscape) and type (Inter or handwritten), and the theme. Pass `SpecStrip` the app's own theme switch as `onTheme` only when the app has a dark theme of its own; without it there's no theme control. A poster laid out for portrait must also read in landscape, where figure 1 and its moments take the left and the foot becomes a column on the right: check it there too.
- **Nothing rearranges in view.** Each poster waits under a spinner until it has settled and gone still, and a change of theme, orientation or type hides them all before it's made. A driver that must show its poster before it's done (a menu or a drag that needs focus while it captures) passes `settled={false}` to `SpecPage` until its last run is held.
- **Always A4 portrait.** Lay it out once on a 794 × 1123 artboard (A4 at 96 dpi), then scale the whole poster to fit the space, centred. Never reflow at a breakpoint: a resize changes the scale, not the arrangement.
- **Order:** the component's name, figure 1 with its moments under it, then the foot. In the foot, the notes and figure 2 sit side by side, and the specification spans the width below them. A title block at the very bottom states the units, the drawing scale and the line types the drawing uses (`lines`), once. Keep notes to two or three short sentences: in landscape the foot is a narrow column, and `btsPosterOverlaps()` fails a foot that runs into the title block.
- **Type:**
  - the name at 16px, weight 500, as the only heading;
  - notes and specification at 13/18;
  - 12px inside drawings;
  - one font, sentence case, nothing heavier than 600;
  - tabular digits, with units lighter than their numbers.
- **Padding:** 20px top and bottom, 32px at the sides.
- **Size each drawing to its slot.** Measure the free height, then pick the drawing scale so the component and its dimensions fit. State it ("drawn at 3×").
- **No housing.** No cards or boxes round notes or figures; use hairlines and flat fills. No glows, no large blurred shadows, no gradients for depth.
- **Accent:**
  - Each poster takes one of Apple's twelve system colours (`SYSTEM` in the kit: the macOS 26 and iOS 26 values from the HIG, light and dark), unique across the project's posters. Record its name in `SPEC_ACCENTS`; a dark poster uses the swatch's dark value.
  - Once all twelve are taken, reuse the least-used one.
  - The accent marks lines and fills, with a 12% tint under the run. Words use a darker ink of the same hue (lightness capped at 0.52), so yellow and mint stay readable.
  - A paper or accent picked in the toolbar is worked out the same way for any pair, by APCA (the perceptual contrast behind WCAG 3, which rightly puts white on a mid blue where WCAG 2's ratio says black): words go black or white, whichever reads better on the paper; every grey is mixed from that ink; accent lines need Lc 40 and accent words Lc 60 against the paper (the accent is moved lighter or darker to get there, losing chroma rather than hue), or the drawings go monochrome in the ink; and on a coloured paper the tints are the ink's, since an accent mixed into another hue makes a third (blue into yellow is green).
- **Theme:** use the app's real theme. Pass `theme="dark"` only when the app itself is dark, read through its own mechanism. An app that follows the system with no switch of its own (`prefers-color-scheme` in its CSS) is read with `matchMedia`, listened to for changes; give `SpecStrip` no `onTheme` then, since there's no switch to drive. Never invent a dark theme, and never put a theme toggle on the poster. Draw nothing until the theme is known, and key the poster on it so a change redraws it and copies the moments again.

Drafting conventions (dimensions from a datum, line types, detail views, aligned views) are in [references/drafting.md](references/drafting.md). Read it before drawing.

**Done when** everything on the poster has a slot and no word sits on the component.

## 5. Polish, then verify by measurement

Polish:
- **Optical alignment:** note numbers sit on their first line's baseline, the foot's columns share a first baseline, and notes and figures share left edges.
- **Concentric radii:** an outline drawn round a part uses the part's own radius at the drawing scale. Anything nested uses the outer radius minus the gap.
- **Soft ends:** drafting grids fade out radially, and the moments row fades at both ends. Dimmed moments blur slightly as they fade.
- **Leaders** leave their parts at 45°, or run straight across where a gap is the only clear path.

Verify:
- **Overlaps:** paste `scripts/overlaps.js` into the page and run `btsPosterOverlaps()`. It checks every kit poster on the page on its own: figure 1's overlay, the timeline and figure 2 against the live component, every word kept on the sheet, every callout leader, and the foot ending above the title block. Run it for every moment at 1280×800, 1000×760 and 1030×1044, in portrait and in landscape (where a long note runs the foot over), and with the handwritten type. Landscape and the handwritten type exist only on `/specs` (its toolbar, or `/specs?layout=landscape&font=hand`); there, scroll each poster into view and run it again, since it checks only posters wholly in the window. It must return nothing. Fix the placement rule, or shorten the note, not the one label. (`btsOverlaps()` checks any other overlay, given elements or selectors; every overlay matched is checked.)
- **Fit:** no page scroll at those sizes, and a resize only changes the scale.
- **Moments:** pick each one. The component, the notes and the curve all follow, and the console stays clean.
- **The row of posters:** every poster is ready on `/specs`, says the same as on its own route (posters share a page, so a driver that clicks, focuses or listens on the document can disturb another), and picking a moment in one leaves the others as they were. The row starts at the first poster. Nothing outside a poster ends up `aria-hidden`, and the toolbar keeps keyboard focus: a modal component hides and traps the rest of the page (see references/drivers.md).
- **The toolbar's settings:** landscape and handwritten pass the overlap check too, and a paper the same colour as the accent turns the drawings monochrome.
- **Numbers in the notes:** read the notes and the specification with the component's source open. Every number traces to a held value, or to a named constant with its source.
- **One value pinned to the source,** such as the poster's duration against the stylesheet.
- **Reduced motion:** the poster tells the truth (no moments row if nothing moves). Check the claim in the specification with reduced motion on: an app-wide rule can override a library's own transitions.
- **Hidden tabs:** an embedded or background preview may not run rAF. Check `document.hidden`, and use headless Playwright for screenshots.

**Done when** every check passes. Say which ones you couldn't run.

## The kit

`assets/kit/` is a React and CSS-modules implementation of everything above. Copy it into the project (`app/specs/kit/` in Next.js, or `src/specs/kit/`) and build each poster as a page beside it. `assets/example/` is a finished poster of a copy button: start from it.

- **`spec-kit.tsx`:**
  - **`SpecPage`:** the poster. Props:
    - `accent`, `name` and `label`;
    - `drawing` (figure 1), `moments`, `notes`, `spec` rows, `fig2` and `units`;
    - `ready`, `error` and `onRetry`;
    - `theme`, `settled`, and `lines` (which line types the title block explains).
  - **`useTransitionSpec({ fractions, setup })`:** the driver for CSS transitions. `setup(root, { stale })` returns the following; a setup that waits before it acts checks `stale()` first (React's development mode runs it twice, and a second click would undo the first):
    - `base` (values at rest);
    - `easing`;
    - `trigger` (the component's own handler);
    - `read` (what to read while it runs);
    - optionally `pick`, to choose among the animations.

    It returns:
    - `m`: the held values, with `elapsed`, `duration`, `easing` and `reduced`;
    - `snapshots`, `selected` and `select`;
    - `ready`, `error` and `retry`;
    - `root`: the ref for the component's wrapper.
  - **Drawing:**
    - `Overlay`;
    - `Dim` and `VDim` (dimensions);
    - `Callout`;
    - `markClass` (line types and hatches);
    - `useCrisp` (hairlines snapped to device pixels);
    - `useDrawingScale`, and `useScreenScale` for a component that has to sit at screen scale 1.
  - **Figures:**
    - `Curve`;
    - `Timeline`;
    - `Moments` (with `crop`, to show just the part that changes).
  - **Reading:**
    - `firstEasing`, `easeAt` and `easeWords`;
    - `stopsOf`, `sampleStops` and `scaleOf` (keyframes: a loop uses one cycle);
    - `within` (box measures to 0.1px);
    - `U` and `Ut` (a number with a lighter unit).
- **`spec-strip.tsx`:** `SpecStrip`, the page that shows every poster in a row, with its toolbar. It takes the app's `theme` and, when the app has a dark theme, `onTheme`. A mouse wheel moves it a poster at a time, a driver's focus doesn't scroll it, and the toolbar's settings are kept for the reader and written into the address (`?paper=yellow&accent=blue&layout=landscape&font=hand`).
- **`spec-toolbar.tsx`** and **`poster-style.ts`:** the toolbar, and the colours behind it: `SYSTEM` (Apple's, light and dark) and `PAPER_TONES`, `posterColours` (a poster's palette for any paper and accent) and `apca`.
- **Springs, in `spec-kit.tsx`:** `springAt` (a spring's progress from its stiffness, damping and mass), `settleTime` and `overshoot` (read off any curve), and `linearStops` (a CSS `linear()` easing as points; `easeAt` reads `linear()` too). `Curve` widens its range when a curve goes past 1.
- **`source-kit.ts`:**
  - `useDataState`: drive a component that keeps its state in a data attribute;
  - `startWithout`: put it at its start with no transition;
  - `ms`: parse CSS times.
- **`sheet-states.tsx`:** snapshot capture and the moments row; `oneCamera` (in `spec-kit.tsx`) puts moments captured one at a time in one frame.
- **`sheet-playback.tsx`:** play, pause and slow playback, for posters that offer it.

For scroll, gestures, pointer paths or a JS animation library, write a small driver with the same shape as `useTransitionSpec` that seeks the library's own clock: see [references/drivers.md](references/drivers.md). Outside React, port the layout and conventions; the kit is a reference, not a dependency.

## Images

`scripts/capture.mjs` saves every poster as images, at A4 proportions: as it opens (its hero moment) and at each moment in its row, in each theme, as PNG and WebP.

```bash
node .claude/skills/interface-bts/scripts/capture.mjs http://localhost:3000/specs --themes light,dark --scale 2 --out specs-out
```

Run it from the project's root, with the path to wherever the skill is installed. It needs Playwright with Chromium in the project (`npm i -D playwright && npx playwright install chromium`). Themes are set through the system colour scheme; an app that keeps its own choice is told it with `--theme-init "localStorage.setItem('theme', THEME)"`. The toolbar's settings ride in the address, so `.../specs?layout=landscape&font=hand` captures them. It keeps the page's own fixed chrome off the shots and reports any error the page logged while it ran. The images go to `specs-out/` in the project: add it to `.gitignore` unless the user wants them committed. Look at the images before handing them over.

## Deliver

Give the `/specs` URL with the new poster in the row, its images from `scripts/capture.mjs` (or a screenshot at 1280×800 if the capture can't run), and the headline. Then list:
- what was measured;
- anything marked as an estimate;
- any check you couldn't run.
