---
name: alpha-cutout
description: Turns an AI-generated (or filmed) clip of a character or product into a transparent, web-ready animation by shooting it on a flat chroma plate and keying it with per-frame plate measurement and edge unmixing. Delivers stacked-alpha MP4 that plays with transparency in every browser including Safari, VP9 alpha WebM, or keyed WebP frame sequences for scroll scrubbing. Use when an animated subject has to sit over page content, between layers of type, or over a 3D scene, when someone asks for "transparent video", "video with alpha", "remove the background from this clip", or when a generated video has a background that should not be there.
---

# Alpha cutout

Image-to-video models never return alpha. A character that should stand between a giant headline and a sun disc, or a bottle that should float over a page, needs its background removed from every frame, cleanly enough that no fringe shows on any page colour. This skill does it the way a film studio does: shoot the subject on a flat key colour, then pull a matte per frame.

## Tools

| File | What it does |
| --- | --- |
| `scripts/plate.py` | Places a cut-out subject on a key plate with headroom; picks the key colour the subject clashes with least |
| `scripts/key.py` | Keys a clip or still into stacked MP4, VP9 alpha WebM, RGBA WebP frames or PNGs |
| `assets/alpha-video.js` | Plays a stacked-alpha MP4 with transparency on a canvas (WebGL), with `seek()` for scrubbing |

Needs Python 3.9+, `pip install numpy opencv-python-headless pillow`, and ffmpeg on PATH.

## Pipeline

1. **Cut the subject out of the still.** Any background remover works. Check what it dropped: thin objects (a ball in the air, racket strings, hair) often go missing. Put them back by hand.

2. **Make the plate.**

   ```bash
   python3 scripts/plate.py subject.png plate.png --size 1350x1800 --fit 0.8
   ```

   The script reports, for magenta, green and blue, how much of the subject sits close to that key, and picks the cleanest. Magenta is usually right: almost nothing in skin, clothing, product or foliage is pure magenta. Green fails on plants and green products; blue fails on denim and sky. The subject is pasted with a hard edge on purpose: a soft edge pre-mixed with the plate colour teaches the model to draw a fringe.

   Leave room for the motion. A serve needs space above the head; a turn needs space to the side. Match the plate's aspect to the video model's output aspect so nothing gets cropped.

3. **Generate on the plate.** Use the plate as the start frame (and as the end frame for a seamless loop; see `motion-assets`). The prompt must name the plate, or the model invents a background:

   > The background must remain a completely flat, uniform, pure chroma-key magenta (exact RGB 255, 0, 255) filling the entire frame, with no shadows, no floor, no gradient, no vignette and no scenery. Locked-off camera.

   **The prompt wins over the image.** A leftover "on a white background" in the prompt gets you a white background whatever the plate was. Re-read the prompt after every edit.

4. **Key it.**

   ```bash
   python3 scripts/key.py clip.mp4 --png check/ --frame-list 0,40,80,120   # inspect first
   python3 scripts/key.py clip.mp4 --stacked hero-1080.mp4 --width 1080
   python3 scripts/key.py clip.mp4 --stacked hero-720.mp4 --width 720      # phones
   python3 scripts/key.py clip.mp4 --frames serve/lg --width 960 --start 0 --end 78
   ```

   `--png` prints the plate colour it measured in each frame. Models drift the plate: a pure magenta can come back pale pink (250, 178, 243) halfway through while the subject keeps its colours. That is why the key colour is measured per frame from the frame's own border instead of being set once. If the subject touches the top edge, the measurement breaks and the script says so.

   Then, per pixel: alpha comes from how far the pixel's key excess is from the plate's, edge pixels are unmixed against the plate (`F = (C - (1 - a) K) / a`), and surviving spill is clamped. Unmixing matters. A plain colour-key or a clamp toward neutral turns magenta edge blends tan, which reads as a salmon outline on a white shirt; unmixing returns the real edge colour.

5. **Check on three backgrounds**: near-black, the page's light colour, and its loudest brand colour. Composite the `--png` output and look at the edges at 100% and 400%. Look hardest at hair, fingers, thin props, motion blur and the frame where the plate drifted most.

## Fixes

| You see | Do |
| --- | --- |
| A thin outline that follows the subject | `--erode 1` (rarely 2). The model copied a fringe into the artwork |
| Holes in light or shiny parts | That colour is too close to the key. Regenerate on a different key (`plate.py --key`) |
| Pink or green wash over the whole background | The plate gradient is stronger than usual; check the measured plate colours and raise `--solid` slightly |
| A detail changed colour mid-clip (a cap turned green) | Model drift, not a keying fault. Recolour that hue in those frames, or regenerate |
| Coloured line round the subject after compression | Already handled: colour under transparent pixels is the subject's own edge colour pushed outward, so chroma subsampling has nothing foreign to bleed in. `--fill` only sets the colour far from the subject |

## Which output

| Output | Plays in | Use for |
| --- | --- | --- |
| `--stacked` MP4 + `assets/alpha-video.js` | Every browser, Safari and iOS included | Looping heroes, characters, anything that plays |
| `--webm` VP9 alpha | Chrome, Edge, Firefox. Not Safari | A plain `<video>` tag where Safari support is not needed |
| `--frames` WebP sequence | Everywhere | Scroll-scrubbed motion (see `scroll-film`): exact frame per scroll position, no seeking lag |

Stacked alpha doubles the frame height (colour on top, matte below) and a shader recombines them, so it is plain H.264: it decodes in hardware everywhere and costs about 1.3 times the bytes of the colour alone. Ship two widths (1080 and 720) and choose by viewport.

```js
import { AlphaVideo } from "./alpha-video.js";
const hero = new AlphaVideo(document.querySelector("canvas.hero"), innerWidth > 900 ? "hero-1080.mp4" : "hero-720.mp4");
hero.onready = () => document.body.classList.add("hero-ready");
function frame() { hero.draw(); requestAnimationFrame(frame); }
requestAnimationFrame(frame);
```

The player pauses itself off screen and uploads a texture only when the video has moved on. For scrubbing, create it with `{ loop: false, autoplay: false }` and call `hero.seek(seconds)` from your scroll handler.

Serve videos from a server that answers HTTP Range requests (the `frame-capture` skill's serve.py does; `python3 -m http.server` does not), or seeking will not work.

## Reduced motion

With `prefers-reduced-motion: reduce`, show one keyed still (`--png` a good frame, convert to WebP) instead of the loop.
