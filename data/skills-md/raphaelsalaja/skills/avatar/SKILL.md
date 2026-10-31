---
name: avatar
description: Draws any object as a flat character with two capsule eyes, then animates its whole body so it glances, blinks, breathes, follows the pointer and falls asleep.
disable-model-invocation: true
---

# Avatar

This skill turns an object into a small living character. It draws one flat silhouette with two capsule eyes, then drives the whole body from one loop so it glances, blinks, breathes and reacts.

## Measured eyes, a body that is never still

The gaze, eye and blink values in [face.js](face.js) are measured off reference footage and are exact. The moods past idle are tuned starting points. A character whose eyes move while its body holds still is a finding.

Gathering references belongs to `gather`. Taking a reference animation apart frame by frame belongs to `deconstruct`. Offering silhouette variants belongs to `prototype`. Interface motion and its 300ms budget belong to `motion`, not a character's body. Frame cost belongs to `frames`. Opening the result belongs to `verify`.

## 1. Study the reference

When the user names a reference character, open its source and step its recording at 10fps. Measure eye size, tilt, spacing and blink timing off the frames. A character drawn from one glance at the reference is `avatar-measure-the-reference`.

Keep measured values as measured. Rounding a `15.5°` eye spacing to `15°` or a `180ms` blink to `200ms` is `avatar-keep-the-measurements`. With no reference named, start from `face.js`.

## 2. Draw the silhouette

Reduce the object to one flat, solid shape in one saturated colour. An outline, shading, a mouth or a nose is `avatar-flat-silhouette`.

It reads at its shipped size, usually 28–40px. Draw it on a small grid, such as a 14 by 17 viewBox, and crop the viewBox tight to the ink. A part that moves on its own, like a lid, gets its own path.

Pick the view whose outline alone names the object: the side for vessels and tools, the front for devices. Given a role or a hobby, draw its single most iconic object. A view that needs its details to be named is `avatar-iconic-view`.

The part that carries the face is the main mass. Grow that part in place until the `head` ellipse, plus one eye width of margin, sits on calm solid fill. Size it for the widest mood, since happy eyes are nearly twice as wide as idle ones. A block added to hold the face, or eyes shrunk to fit, is `avatar-face-part-leads`.

Size every other part by its outline, enclosed space included, not by its fill. It stays clearly smaller than the face part and reaches out only as far as recognition needs. A handle loop as tall as its cup is `avatar-size-by-outline`.

Keep the few steps that name the object, such as a neck, a lid or a lip, and drop every other detail. Build the shape from one to seven soft primitives that overlap into one outline.

Every join is a clear step or a smooth flow. A step is at least half an eye width, and a flow runs one edge straight on with the inner corners buried. A part joined at two points stays joined at both. Edges that nearly line up and leave a sliver or a notch are `avatar-clean-joins`.

Cut a hole only for a real opening, such as a mug handle or a ring, and wind it against its outline so the fill leaves it open. A slot, a button or a decorative cut-out is `avatar-holes-are-openings`.

Keep toy proportions. No part is thinner than an eye is wide, every corner is rounded and every taper ends in a soft tip. An organic part, like a leaf or a flame, keeps its curve and direction. A hairline, a sharp point or a leaf flattened into an oval is `avatar-toy-proportions`.

Centre the mass and sit it on a flat or gently rounded base. Then look at the whole shape at 28px, at rest and mid-lean. If it reads as another object or a broken one, rebalance the parts or change the view, even when every rule above holds.

Colour comes from two variables, `--avatar-body` and `--avatar-eyes`, checked in both themes. A fill written into the path is `avatar-colour-variables`.

## 3. Put the eyes on a sphere

Two white capsules, each about 2.2 times as tall as wide, rest high and to the right. They lean like a backslash, with the head tilted about 12°.

The eyes sit on a sphere behind the face. A yaw, pitch and roll place them, so they narrow near the edge and fade as they turn behind. Eyes sliding flat across the face is `avatar-eyes-on-a-sphere`. `drawEyes` in `face.js` does the projection.

Clip both eyes to the silhouette path, inside the group that moves the body. An eye drawn past the outline is `avatar-clip-to-the-body`.

## 4. Give the whole body life

Nothing holds still. The gaze drifts on layered sine waves and glances to a new spot every 1.5–4s, and big glances bring a blink. A gaze parked at rest between events is `avatar-never-still`.

Blinks take 180ms and close in the first 45% of it. They land 1.9–4.6s apart, and 18% are doubles. A blink on a fixed interval is `avatar-irregular-blinks`.

The body breathes 1.2% on a 3.4s cycle, floats slightly and leans toward its gaze a beat late. Eyes settle in about 60ms and the body in 220ms. Eyes moving inside a frozen body is `avatar-whole-body`.

## 5. Make moods from eye shapes

A mood is one row of numbers: eye width, height, tilt, spacing, openness and a gaze offset. Moods blend over about 90ms on an exponential ease-out and never overshoot. A separate drawing swapped in per mood is `avatar-moods-as-numbers`.

Start from idle, attentive, excited, happy, sleepy and asleep. Add one or two moves only this object can make, such as a lid that lags behind a hop. A character with no move of its own is `avatar-object-move`.

## 6. Wire the reactions

Each reaction answers one input from the page:

- The pointer enters after 6s away. The eyes spin 360° round the back over 1.1s, then follow the pointer.
- The pointer rests on the primary action. The eyes widen and the body bounces slightly.
- The user presses the action or the character. It hops for 750ms with squash and stretch, then squints happily back out.
- Nothing happens for 24s. It grows sleepy, falls asleep at 30s with slow deep breaths and wakes with a spin.

Clamp the followed gaze to ±45° of yaw so the eyes stay on the face, and ignore touch pointers for following. A character that ignores the page around it is `avatar-react-to-the-page`.

When the character is the main toy on its page, it may also react to distance. It turns curious inside 640px, wary inside 260px and recoils inside 100px. A poked eye shuts while the other stays open.

## 7. Run it from one loop

One `requestAnimationFrame` loop steps `createAvatar` from `face.js` and writes SVG attributes through refs. The step caps at 64ms so a returning tab does not jump. Per-frame state updates belong to `frames`.

Run the loop only while the character is on screen, through an `IntersectionObserver`. A loop that keeps running offscreen is `avatar-pause-offscreen`.

Render the resting pose on the server from `restingEyes`, so the first paint already has eyes. A face that pops in on hydration is `avatar-render-the-rest`.

Under `prefers-reduced-motion: reduce`, the character holds its resting pose and starts no loop. A character that still glances and hops is `avatar-still-when-reduced`. The character is decorative, so its SVG takes `aria-hidden="true"`.

## 8. Prove it on a contact sheet

A single screenshot cannot show motion, and a hidden tab throttles the loop. Run [sheet.js](sheet.js) through the browser's evaluate call, then call `window.__avatarSheet.start({ selector })`.

Drive each mood with pointer events: idle, enter, hover, press and leave. Call `window.__avatarSheet.stop()` and screenshot the sheet it lays out. One still frame offered as proof is `avatar-contact-sheet`.

A `warning` in the result means the tab was hidden or the loop stalled, so frames repeat or gaps widen. Keep the tab visible and sample again. Sleep needs 30s without input, so sample it once on its own.

Finish with the character at its shipped size in both themes, then call `window.__avatarSheet.clear()`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `avatar-measure-the-reference` | Eyes placed from one look at the reference | Size, tilt, spacing and blinks measured off frames at 10fps |
| `avatar-keep-the-measurements` | `split: 15`, rounded to look tidy | `split: 15.5`, as measured |
| `avatar-flat-silhouette` | A cup with an outline, shading and a smile | One solid shape and two eyes |
| `avatar-iconic-view` | A watering can from the front, which reads as a box | The side view, where the spout and handle name it |
| `avatar-face-part-leads` | A slab stuck on the mug to hold the eyes, or eyes at half size | The cup widened until the head and its margin fit |
| `avatar-size-by-outline` | A thin handle loop as tall as the cup | A compact handle, clearly smaller than the cup |
| `avatar-clean-joins` | A lid edge 0.3 units past the cup, leaving a sliver | A step of half an eye width, or edges matched exactly |
| `avatar-holes-are-openings` | A cut-out slot for a coin or a button | Holes only where the object is open, such as the handle |
| `avatar-toy-proportions` | A hairline stem and a sharp leaf tip | Parts at least an eye wide, rounded corners, soft tips |
| `avatar-colour-variables` | `fill="#c27a3e"` in the path | `fill="var(--avatar-body)"`, set per theme |
| `avatar-eyes-on-a-sphere` | `translate(dx, dy)` on both eyes | `drawEyes(face, gaze, lid, head)` from yaw, pitch and roll |
| `avatar-clip-to-the-body` | An eye hanging past the outline on a wide glance | Eyes inside a `clipPath` of the body path |
| `avatar-never-still` | Eyes parked at rest between blinks | Layered drift and a glance every 1.5–4s |
| `avatar-irregular-blinks` | `animation: blink 5s infinite` | 180ms blinks 1.9–4.6s apart, 18% doubles |
| `avatar-whole-body` | Only the eyes move | The body breathes, floats and leans 220ms behind the gaze |
| `avatar-moods-as-numbers` | `{happy ? <HappyFace /> : <Face />}` | `happy: { eyes: pair(0.522, 0.217, 18) }`, blended over 90ms |
| `avatar-object-move` | A cup that moves like any blob | The lid lifting a beat behind the hop |
| `avatar-react-to-the-page` | One idle loop whatever the pointer does | Spin on enter, follow, widen on hover, hop on press, sleep when left |
| `avatar-pause-offscreen` | A loop running below the fold | The loop started and stopped by an `IntersectionObserver` |
| `avatar-render-the-rest` | Eyes appearing after hydration | `restingEyes(head)` in the server HTML |
| `avatar-still-when-reduced` | Glancing and hopping under reduced motion | The resting pose and no loop |
| `avatar-contact-sheet` | One screenshot of the idle pose | A `sheet.js` sheet through every mood, then shipped size in both themes |

## Reporting

**Severity.** `HIGH` is a body that never moves, eyes escaping the silhouette or motion under reduced motion. `MEDIUM` is flat sliding eyes, a fixed blink, swapped mood drawings, an offscreen loop, a missing reaction or proof from one screenshot. A view that does not name the object, a cramped face or an oversized secondary part is also `MEDIUM`. `LOW` is a rounded measurement, a fill in the path, a rest pose that pops in or a character with no move of its own. A sliver at a join, a decorative hole or a hairline part is also `LOW`.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Mark a reference you could not open or step through as `Not verified`.
