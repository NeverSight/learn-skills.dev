---
name: sakuga-vfx
description: Build, change or wire in a UI control that reacts like anime (squash and overshoot on springs, drawn smoke, impact bursts, slashes and splashes, manga sound-effect lettering), using the Sakuga VFX core. Use when asked to add one of the sakuga-* components to an app, to change how one reacts, to re-theme them, or to make a new control in the same style. Covers the core's effects, the rules the set follows, and the frame-by-frame look that has to happen before calling it done.
---

# Sakuga VFX

A Sakuga control is an ordinary control (a button, a switch, a slider) that is plain at rest and reacts like an anime cut when you use it. The control itself moves on springs; the effects are drawn on one canvas over the page, so they can fly outside the control.

This skill is the workflow the set was made by. It comes with three files:

- `core.js` — the shared core: `Spring`, the effects layer and every effect, the lettering, the palette, and `Base`, a custom-element base class with one shared clock.
- `starter.html` — the smallest whole example, a like button. Copy it to start a new one.
- `look.mjs` — stops the clock, steps a reaction to chosen moments and saves the frames side by side, so you can read them.

If the job is only to put an existing component into an app, skip to **Wire it in** and **Check it**.

## 1. Decide four things before animating

1. **The control.** It must still be that control with every effect switched off: a real `<button>`, `<input>` or `role="switch"` inside, with keys and focus.
2. **The beats.** Write the reaction as beats, the way a key animator would: anticipation (the press), the hit (the frame where it happens), the follow-through (what drifts off), and the settle. Each beat gets one effect or two, not five.
3. **The word.** At most one sound-effect word per reaction, on the hit. The six are ドン (impact), カチッ (click), シュッ (swish), ポン (pop), ズザッ (skid) and ゴゴゴゴ (rumble).
4. **What is real and what is drawn.** State changes happen at once; effects only decorate them. Nothing the user needs to read may depend on an effect.

## 2. The core

Load `core.js` and everything is on `window.SakugaFX`:

- **Motion:** `new Spring(x, stiffness, damping)`, then set `.to` and call `.step(dt)` every frame. `squashy(button, { low, wide })` gives a press that squashes while held and overshoots on release; call its `step(dt)` in `frame()`.
- **Effects,** all in page coordinates (use `at(el, fx, fy)` to get a point on an element): `burst` (the impact star), `puff` (a smoke puff), `donut` (a smoke ring), `shards` (crystal chips), `slash` (a crescent), `lines` (speed lines), `ticks` (accent wedges), `ring`, `splash`, `kira` (a glint), `wob` (wobble marks), and `sfx(word, x, y, { size })`; pass `...hollow()` or `...dotted()` to `sfx` for the two lettering styles.
- **Timing:** `later(ms, fn)` runs on the shared clock, not on `setTimeout`, so `look.mjs` can step it. Use it for every delay.
- **The base class:** extend `Base`, give it `static css`, `render()` (the shadow HTML), `setup()` (listeners, springs) and `frame(dt)`. `backLayer()` gives a canvas inside the element, behind the control, for an effect that must sit behind it (pass `{ layer }` to `burst`). `static formAssociated = true` gets `this.internals` for forms.
- **Colours:** `P` is the effects palette. In CSS use the `--sk-*` variables (`--sk-ink`, `--sk-card`, `--sk-pri`, `--sk-acc`, `--sk-sh`, ...).

## 3. The rules

These are the corrections that came up most.

- **Two tones and a line.** Every drawn shape is a flat light tone, one flat shadow tone and an outline. No gradients, no blur.
- **Things leave by shrinking or thinning, not by fading.** An effect's opacity never changes.
- **Squash keeps volume.** When something squashes to `y` high it gets wider; when it stretches it gets thinner.
- **Springs, not easings,** for anything the hand moves. Stretch comes from the spring's speed, so a fast drag smears and a slow one does not.
- **Effects follow speed.** A slow drag is quiet. Fire the big stuff on the release, the landing, or the moment of change.
- **Pink is for accents.** Wedges, needles and the check are the accent colour; everything else is ink and paper.
- **The control is plain at rest.** No idle animation, and nothing drawn around it until it is used.
- **To match a drawn reference, generate frames from it.** The toggle is 43 frames painted with an image model from a sheet of keyframes, aligned on the housing and played at 30 a second. Simulating a morphing liquid in code did not get close; drawing it did.
- **Reduced motion.** The core already drops every effect when `prefers-reduced-motion` is set. Make sure the state still changes.

## 4. Look before you say it is done

A component that runs without errors has told you nothing about how it reacts.

1. Serve the folder and run `look.mjs` on the page, with `--act` to press, click or drag at the right moment:

   ```sh
   node look.mjs "http://localhost:8000/starter.html" --select like-button --act "0:document.querySelector('like-button').shadowRoot.querySelector('button').click()" --times 0,0.05,0.12,0.25,0.45,0.8
   ```

2. Open the sheet and read each frame: is the hit frame clear, does anything cover the label, does each effect leave by shrinking, is there a frame where nothing is happening that should be.
3. Fix what you see and look again. Expect several rounds.

## 5. Wire it in

- **One file per component.** Each component file carries a copy of the core between its `// >>> sakuga core` markers, so it works on its own; the first one loaded sets `window.SakugaFX`, the rest reuse it. When you change the core, run `node tools/build.mjs` in the repo to stamp it into every file.
- **Load it with a plain script tag,** not as a module, and do not split or rewrite it.
- **Attributes and properties for state, events for what happened:** `change` for value controls (they also work in forms), `click` for buttons, `sakuga:done` for progress.
- **Do not edit the effects to restyle someone else's component.** Set the `--sk-*` variables, or say what needs to look different.

## 6. Check it

Use it the way a person would, in a real browser, and report each separately.

- **Pointer and touch:** real presses and drags sent through the DevTools protocol (`Input.dispatchTouchEvent`, `Input.dispatchMouseEvent`), not calls into the code. `tools/test.mjs` in the repo does this for every component.
- **Keyboard:** Tab to it, then the keys that should work it.
- **Two widths:** a desktop width and 390 pixels, with no sideways scroll.
- **Forms:** if it has a value, `new FormData(form)` should contain it.

## 7. Say what is true

- **What it does now.**
- **What you checked, and how.** "Stepped frame by frame with look.mjs" is not "watched it at real speed". Say which.
- **What is still weak.** Name the frames or beats that do not read.
