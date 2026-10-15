---
name: feel
description: Build UI interactions whose motion comes from a physical model instead of durations and easing curves. Turn a feel described in words ("a toggle that feels heavy", "a drawer with a magnetic snap", "a card you throw into a corner", "a knob with heavy detents", "a sticky slider") into a production component driven by mass, stiffness, damping and force fields (magnets, friction, walls), on a line, in a plane or around a dial, plus a test rig that plots position, velocity and the force field, overlays the model's prediction on the measured motion, and exports the same spring to Framer Motion, react-spring, SwiftUI, Compose or CSS linear(). Use this whenever someone asks for an animation, transition, spring, gesture, drag, flick, snap points, bottom sheet, toggle, slider, carousel or any micro-interaction that should "feel" a certain way, or wants to tune or explain a spring, even if they never say "physics".
---

# Feel

This skill makes interactions that move like things. A toggle's thumb is a body with mass on a spring. A drawer is a body coasting through a field of magnets. A drag is a force: the pointer pulls the body through a hand spring, so a heavy thing lags the finger and a light thing doesn't. Nothing in the result has a duration or an easing curve. How long a motion takes is a consequence of the model, and the rig can show you exactly why.

One complete page ships with the skill: `index.html`, with four components, each in its rig: a heavy toggle (a spring), a magnetic drawer (a field), a card thrown to a corner (a body in a plane) and a detented knob (a body in degrees). Open it before you start. Serve the folder (`python3 -m http.server`) and play with all four.

## The one rule

**Every motion comes from a physical model: mass, stiffness, damping and forces. No hand-picked durations.**

That means:

- No `transition: … 300ms`, no `animation-duration`, no `cubic-bezier`, no `ease-out`, no `duration:` options, no timers that move things. `scripts/audit.mjs` fails on any of them.
- A tap is a target change (springs) or an impulse (fields), never a timed slide.
- A drag sets a hand, not a position. Release keeps the body's real velocity.
- A decision on release (which side, which stop) is made from where the body would coast, `x + v·m/c`, or by simulating forward. It is never made from a threshold in milliseconds.
- If a library forces a duration (CSS), the duration is computed from the model, and the code comment says so. `Feel.handoff` does this for you.

It fails in two ways:

- **Tween in disguise.** The code uses a spring but snaps the target on a timer, or reads pointer velocity and throws it away on release. The motion looks springy and feels dead.
- **Untuned physics.** It's a real spring, but the numbers were typed until it "looked fine". Physics with arbitrary numbers is just a fancier easing curve. Start from words, check them against the rig, and write down why each number is what it is.

## Workflow

1. **Size it, before anything else.** Tell the user which size this is.
   - **Interaction**: one component, one body (toggle, button press, card lift, slider thumb). 20–45 minutes. Build it without asking.
   - **Gesture system**: several bodies or a field (bottom sheet with stops, carousel with momentum, reorderable list). 1–3 hours. Say so, then build it.
   - **Motion system**: a whole product's motion vocabulary (tokens, every component, docs). Half a day or more. Don't start it. Propose the 3 interactions that matter most, and list what the full system would add.
2. **Words to physics.** Write the feel as words and run `Feel.words("…")`. It returns mass, natural frequency and damping ratio, then stiffness and damping. `references/vocabulary.md` has every word and how words blend. If the user's word isn't there, map it to the nearest ones and say which you used. Then write one sentence per number:
   - *frequency 1.35 Hz:* slow enough to read as weight;
   - *ζ 0.74:* a 3% overshoot, the thump of something landing;
   - *mass 3:* lags a fast drag by a few px and coasts 80 px per 1000 px/s.
3. **Choose the model.** `references/models.md` covers them:
   - **Spring to a target** for anything with two or more discrete states chosen by the code (toggle, press, expand).
   - **A field** (magnets, friction, walls) for anything the user throws (sheets, carousels, pickers). A field has no target: the body ends up wherever the field holds it.
   - **Walls** at the ends of travel, for rubber-banding. Overshoot past a physical end is caught by the wall, not drawn through it.
   - **A plane** (`Feel.Body2D`) for anything thrown in two directions at once (a picture-in-picture card, a floating panel). Corners and snap points are `Feel.points`, measured in a straight line. Two 1D bodies can't do this, because which stop is nearest depends on both coordinates.
   - **An angle** (`Feel.Body` with `unit: "°"`) for knobs, dials and wheels. Detents are `Feel.magnets` in degrees; a wheel that turns forever adds `period: 360`.
4. **Build the component on a body.**
   - Write one `styles(b)` that returns `[[el, props], …]`: transform from position, anything else (fill, shadow, stretch) from position or speed. Paint it with `Feel.paint(styles(b))` in `onFrame`.
   - Bind input with `Feel.drag(el, body, { axis })`: `"x"`, `"y"`, `"xy"` for a plane, `"angle"` for a turn.
   - Keyboard reaches every state.
   - `prefers-reduced-motion` jumps to rest. The runtime does this for you.
   - To let the browser play the motion (CSS keyframes, off the main thread), call `Feel.handoff(body, styles)`. Register any custom property it animates with `@property`.
   - Framework-free: copy the closest of `components/heavy-toggle.js`, `magnetic-drawer.js`, `corner-card.js` or `rotary-knob.js`. React: `runtime/react/useFeel.ts`.
5. **Put it in the rig.** `Feel.rig(host, { body, stage, travel, stops, feel, actions, handoff })`. Check every one of these:
   - **Measured on predicted:** the orange line sits on the dashed prediction after "let go". In a plane, the path sits on the dashed path.
   - **The force plot reads as the idea:** one slope for a spring, a well per stop for magnets, arrows toward each point in a plane.
   - **The readout numbers match your sentences from step 2.** After a tap, the readout's "settled in" matches Measures' "settles in". Both include the walls, so they can be shorter than `Feel.metrics` (the spring alone).
   - **With a `handoff`, switch "Runs on" to CSS keyframes** and do it again: the same motion, and a grab mid-flight doesn't jump.
6. **Export if the target stack needs it.** The rig's export tabs give the same spring for Framer Motion, react-spring and SwiftUI (identical equation), Compose (unit-mass stiffness), and CSS `linear()`, which is sampled from the exact solution and only replays a step from rest.
   - **A release, a flick or a field in CSS** goes through `Feel.handoff`: each release is baked from the model into keyframes, with the velocity it has.
   - **A field exports to Framer Motion's drag inertia** as an approximation, labelled as one.
   - **Everything else has no equivalent.** Say so and ship `runtime/feel.js` (15 kB gzipped, comments included).
7. **Verify.** Run `node scripts/audit.mjs <your files> --feel "<your words>"`. It must print `passed`. Then do it with your hands in the browser:
   - a slow drag, a hard flick, a flick the wrong way, and letting go at exactly halfway;
   - grabbing it mid-motion (it must not jump), in JS and in CSS keyframes;
   - keyboard only;
   - reduced motion.

   Record what you saw in one line each. `references/verify.md` has the checklist.

## The runtime

```js
const body = new Feel.Body({ feel: "heavy", x: 0, target: 0, min: 0, max: 60, onFrame, onRelease });
body.to(60);           // new target: the spring takes it there
body.kick(900);        // an impulse, px/s
body.kickTo(170);      // the push that comes to rest at 170 (solved by simulation in a field)
body.grab(px); body.move(px); body.release();   // what Feel.drag calls for you
body.projected();      // where it would coast: x + v·m/c
body.predict(v);       // where it would come to rest from here with velocity v
body.path(x, v);       // the whole predicted path, for the rig's ghost
body.measureStep(0, 60);  // a tap from rest, walls and forces included → { overshoot, settle }: the rig's Measures
body.lastSettle();     // the last motion's settle (±2% of the move, from "let go"), read off the trace: the readout

const card = new Feel.Body2D({ feel: "airy", x: 0, y: 0, target: null, forces: [Feel.points({ stops })], min: { x: 0, y: 0 }, max: { x: W, y: H } });
card.to({ x, y }); card.kick(vx, vy); card.kickTo(stops[2]);   // the same commands, on points
const knob = new Feel.Body({ feel: "heavy, clicky", unit: "°", target: null, forces: [Feel.magnets({ stops: degrees })], min: -135, max: 135 });

Feel.words("very heavy, snappy")  // → { params: { mass, stiffness, damping }, modal, magnet, friction }
Feel.metrics(params)              // → { freq, zeta, overshoot, settle, rise, peakVelocity }
Feel.magnets({ stops, reachFreq, clickFreq, clickRadius, period }); Feel.points({ stops, … })
Feel.friction({ level }); Feel.friction2d({ level }); Feel.gravity(g)
Feel.drag(el, body, { axis: "x" | "y" | "xy" | "angle", onTap })
Feel.paint(styles(body))          // write [[el, props], …] onto the elements
Feel.handoff(body, styles)        // let the browser play every free motion as keyframes; .off() takes it back
Feel.exportCode(params, "framer" | "react-spring" | "swiftui" | "compose" | "css", body?)
```

Units are px (or degrees) and seconds. Mass 1 is a normal UI element, and the hand spring is tuned for it. All bodies share one `requestAnimationFrame` loop that stops when everything has settled. With a handoff, nothing runs per frame: each release is simulated once at 240 Hz, simplified to keyframes within 0.2 px of the path, and played by the browser. A grab or a command mid-flight reads the state at that instant from the same path.

`Feel.ui` holds the rig's own controls (fluid hover, tabs, the scrubber slider, copy), after [Fluid Functionalism](https://www.fluidfunctionalism.com/). They move on Feel springs too, so a page can use them without adding a duration.

## Craft rules

- **Name the model in one sentence before writing code.** For example: "The thumb is a 3-unit mass on a 1.35 Hz spring with ζ 0.74; the track walls catch the overshoot."
- **Mass is felt in interaction, frequency and damping in motion.** Two toggles with the same frequency and damping but different mass look identical when tapped and feel different when dragged. If the feel is about weight, the demo must include a drag.
- **Everything visual derives from state, not time.** Fill from position, stretch from speed, shadow from height.
- **Overshoot belongs to the thing, not the frame.** If the track ends, a wall catches the thumb. Never let a spring draw a thumb outside its track.
- **Interruptible by construction.** A grab mid-motion takes over from the current x and v. Never reset velocity on grab, and never queue animations.
- **One accent in the rig** (orange). The component's own colours are untouched.

## Limits (v0.2)

- A body has a position or an angle, not both. A card that also tilts as it flies needs a second body for the tilt, driven by the first one's velocity.
- A `Body2D` spring is isotropic: one stiffness and one damping for both axes. Walls are per axis, so travel is a rectangle.
- `Feel.handoff` plays free motion only. A drag still runs in JavaScript, because the hand needs it. Custom properties it animates must be registered with `@property`, or the browser flips them instead of interpolating.
- The CSS `linear()` export replays a step from rest. For a flick or a field in CSS, use `Feel.handoff`.
- The Framer Motion export for fields is an approximation (inertia plus a snap spring), not the same force law. Points in a plane and detented knobs have no Framer equivalent.
- The drag model reads pointer events at their own rate. On very low frame rates the hand velocity estimate gets noisy, and the 60 ms rule zeroes stale velocity at release.

## Files

| File | Use it for |
|---|---|
| `runtime/feel.js` | Bodies on a line and in a plane, the exact spring solution, metrics, words, force fields, drag, the shared loop, the CSS handoff, export. Works in the browser and in Node. |
| `runtime/rig.js` + `runtime/feel.css` | The test rig: bench, position/velocity/force plots with the predicted ghost (path, speed and arrows in a plane), dials, word chips, readout, keys, JS or CSS, export tabs. Also `Feel.ui`, its controls. Light by default; `theme: "dark"` for dark pages. |
| `runtime/react/useFeel.ts` | React hook: a body that writes styles through a ref, without re-rendering. |
| `components/heavy-toggle.js` | Example: a spring with walls, a drag through the hand spring, a flick decided by projection. |
| `components/magnetic-drawer.js` | Example: a field with no target, taps as impulses solved by simulation. |
| `components/corner-card.js` | Example: a body in a plane, thrown to the nearest corner, with lift from speed. |
| `components/rotary-knob.js` | Example: a body in degrees, turned around its centre, with detents as magnets. |
| `scripts/audit.mjs` | No-durations scan, solver vs exact solution on a line and in a plane, passivity, settling, taps land (stops, corners, detents, across a wheel's seam), baked keyframes against the loop, and one settle time for the rig's Measures and readout. |
| `references/vocabulary.md` | Every feel word, its numbers, and how words blend. |
| `references/models.md` | Springs, fields, walls, the hand, projection, and how to write a new force. |
| `references/verify.md` | The hands-on checklist. |
