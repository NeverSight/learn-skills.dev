---
name: cursor-rig
description: Makes a painted or illustrated character turn its head to follow the visitor's cursor, looking like one continuous painting that moves, without a 3D model or face tracking. Generates head-pose keyframes with an image-editing model and head-turn clips with an image-to-video model, then builds a pose grid on one fixed body (selected by measured head position, aligned, masked, with optical-flow in-betweens) and plays it with a spring-driven canvas player that also blinks. Use when someone wants a hero character, mascot or portrait whose eyes or face follow the mouse, a "look at the cursor" effect, or an illustration that reacts to the visitor.
---

# Cursor rig

A character who looks at you is the strongest hero a page can have. Building one in 3D means modelling, rigging and matching a painting's style, and the result never quite looks like the painting. This skill keeps the painting. It renders the head in every direction once, as a grid of poses, and at runtime shows the pose that faces the cursor. With 19 yaw steps and 8 pitch rows, the turn reads as continuous.

## Tools

| File | What it does |
| --- | --- |
| `scripts/build_rig.py` | Turns head-turn clips into `row_N.webp` pose strips, `plate.webp` and `rig.json` |
| `assets/rig.js` | Loads the rig, places a canvas over the head, follows the pointer with a spring, blinks, glances about when idle |

Needs Python 3.9+, `pip install numpy opencv-python-headless`, ffmpeg, an image-editing model and an image-to-video model that accepts start and end frames (see `motion-assets`).

## Pipeline

### 1. The plate

The plate is the character facing forward: the one image every pose is built on. Upscale the source illustration to at least 1440 px tall. If the hero needs to be wider than the character, outpaint the sides for the page, but build the rig on the square or portrait crop around the character. Outpainting models re-render the whole image, so paste the original pixels back over the middle afterwards.

### 2. Keyframes

With an image-editing model, make the head turned to each extreme from the plate: left, right, up, down, and the four diagonals. The prompt must pin everything except the head:

> Same character, same painting, same framing and crop. Only the head turns to look toward the left edge of the image, about 40 degrees. Hair, face, skin, shirt, hands, body pose, background and brush style stay exactly the same. No new objects.

Flick between the plate and each keyframe at full size. Only the head may change. Models that hold framing almost pixel-exact are worth paying for here; a keyframe with a shifted shoulder costs a whole row.

### 3. Head-turn clips

Image-to-video, start frame = the plate, end frame = a keyframe, 5 seconds, camera locked off:

> Locked-off camera. The character slowly turns only his head and neck from facing forward to [the end pose]. The body, shirt, arms and background stay perfectly still. Smooth, even motion, no blinking, no talking.

Name the clips by row and side: `L.mp4` and `R.mp4` for the level row (required), `UL`/`UR` (up), `HL`/`HR` (half down), `DL`/`DR` (down). Eight clips make a full rig. Two make a rig that only turns left and right.

If two rows differ a lot (the model redrew the hair in the down keyframes, say), do not rely on morphing between them: generate a real middle row instead.

### 4. Build

```bash
python3 scripts/build_rig.py clips/ site/rig --box 300,40,840,800 --track dots --debug work/rig-cells
```

- `--box x,y,w,h` (plate pixels): everything the head ever covers, hair included, with a little neck.
- `--track dots` for cartoon dot eyes: finds the two dark round eyes in every frame, and records their positions so blinks can be painted live. `--eye-band y0,y1` and `--dark` tune it.
- `--track template --point x,y` for any other face: follows a patch around a point you give (the bridge of the nose works) from frame to frame. No blinks are painted with this mode.
- `--poly` sets the head mask polygon if the default oval cuts the hair or includes the collar.

What the script does, and why:

- **Aligns every clip on the body** (ECC, rows below `--body-y`). Video models drift the whole frame a few pixels; without alignment the shirt jitters as the head turns. It prints the drift per clip; above 6 px, the clip was not locked off.
- **Picks columns by measured head position, not by time.** Models ease in and out, so evenly spaced timestamps give uneven steps. Even steps of the measure give an even turn.
- **Blends each head onto the one plate body** through a feathered mask, after matching brightness to the plate, so only the head ever changes.
- **Fills missing pitch rows** with optical-flow in-betweens of the neighbouring rows.

Open the `--debug` cells as a contact sheet and look down every column and across every row: no jumps in head size, no hair popping, no collar seams.

### 5. Page

```html
<figure class="hero-rig" style="position: relative; margin: 0">
  <img src="rig/plate.webp" alt="A painted shopkeeper in a loud shirt, looking at you">
  <canvas></canvas>
</figure>
<script type="module">
  import { loadRig, HeadRig, animate } from "./rig.js";
  const head = new HeadRig(document.querySelector(".hero-rig"), await loadRig("rig/"));
  animate([head]);
</script>
```

If the page shows a wider artwork than the plate, pass where the plate sits in it, in artwork pixels: `new HeadRig(el, data, { art: { w: 3898, h: 1440, plateX: 1229, plateY: 0 } })`.

The player:

- loads the level row first (the head can turn left and right at once), then the rows above and below;
- aims with `tanh` of the pointer's offset from the eyes, so far corners do not snap the head to its limit;
- moves through a slightly under-damped spring (a small settle at the end of each turn reads as alive);
- cuts between neighbouring poses instead of cross-fading (a cross-fade shows two pairs of eyes);
- paints blinks, double blinks and winks over the eyes using the eye positions and skin tones in `rig.json` (dot tracking only);
- glances about by itself when the pointer has been still for 3.5 s, and on touch devices;
- pauses when off screen.

## Budget

Eight clips is the full cost; at typical image-to-video prices that is a few dollars. The finished rig (152 poses at 0.6 scale) is about 2 MB of WebP.

## Accessibility

- The plate `<img>` carries the alt text; the canvas is decoration.
- With `prefers-reduced-motion`, the head still answers the pointer (the visitor is causing it) but critically damped, with no idle glancing and no blinks.
- Nothing depends on the rig: it is a portrait that happens to look at you.
