---
name: scroll-film
description: Builds scroll-scrubbed film sections, where scrolling plays a pre-rendered camera move, a product turning, a liquid pour or a fly-through one exact frame at a time, from AI-generated or rendered clips. Covers chaining clips into one seamless film with start and end frames, frame sequences versus scrub-ready video, pinned sections with holds for text, phone versions, loading budgets and reduced motion. Use for "scroll-driven animation", "Apple-style scroll video", "fly through the world as you scroll", scroll cinematics, or when a scrubbed video on a page stutters, jumps at a seam or loads too slowly.
---

# Scroll film

A scroll film pins a canvas while the visitor scrolls through a tall section, and the scroll position picks the frame. The visitor drives the camera, which is why it feels three-dimensional even when every frame was rendered in advance. It is the right tool when the motion is too rich for real-time 3D (generated worlds, liquids, people) and the path is fixed.

## Tools

| File | What it does |
| --- | --- |
| `assets/scroll-film.js` | The engine: pinned canvas, progress-to-frame keys with holds, frame sequences or video, smoothing, reduced motion |
| `scripts/prep.py frames` | Joins clips into one numbered WebP sequence and a manifest |
| `scripts/prep.py video` | Joins clips into one MP4 encoded for instant seeking |
| `scripts/prep.py seams` | Scores every join between clips and fails on a visible jump |

Needs ffmpeg and ffprobe, Python 3.9+ and `pip install pillow numpy`. Making the clips is `motion-assets`; transparent subjects are `alpha-cutout`; checking the result is `site-check` and `frame-capture`.

## Plan before generating anything

1. **Write the story as beats.** One beat per scene: what the camera sees at the start, where it goes, what the visitor reads there. Four to seven beats fill a landing page. A beat is one generated clip (a "leg").
2. **Make the keyframes first, all of them, in one style.** A leg is generated between a start frame and an end frame, and the end frame of one leg is the start frame of the next. Generate every keyframe still with the same model and the same style reference before any video, and lay them out side by side. A style that drifts between stills drifts across the whole film.
3. **Budget it out loud.** Cost is roughly stills plus legs times the price of one clip. A phone version in portrait doubles the video cost (see Phones). Calibrate with one still and one clip before committing (`motion-assets` covers model choice, pricing and rate limits).

## Build

1. **Generate the legs** with start and end frames from step 2. Check every join:

   ```bash
   python3 scripts/prep.py seams legs/01.mp4 legs/02.mp4 legs/03.mp4
   ```

   Under 4 is invisible; over 10 is a jump. Fix a bad seam by regenerating that leg anchored on the exact last frame of the previous one (extract it with ffmpeg rather than reusing the still: models shift colour and framing slightly).

2. **Choose frames or video.**

   | | Frame sequence (default) | Scrub video |
   | --- | --- | --- |
   | Accuracy | Exact frame for every scroll position | Seeks land a little late, worst on Safari and low-end phones |
   | Size | 20 to 60 kB a frame at 1280 to 1600 px | About a third of that |
   | Good for | Up to roughly 300 frames | Long films where size matters more than precision |

   ```bash
   python3 scripts/prep.py frames legs/*.mp4 site/film/lg --width 1600 --fps 24
   python3 scripts/prep.py frames legs/*.mp4 site/film/sm --width 900 --fps 24 --quality 72
   python3 scripts/prep.py video legs/*.mp4 site/film.mp4 --width 1920 --gop 4
   ```

   `frames` drops each later leg's first frame, which duplicates the previous leg's last. `video` uses a 4-frame GOP and no B-frames: a normal export with a 250-frame GOP makes every seek decode hundreds of frames, and scrubbing stutters.

3. **Mark up the section.** Height sets how much scrolling the film takes. Roughly one viewport of scroll per second of film feels deliberate; less feels rushed.

   ```html
   <section id="film" style="height: 600vh">
     <div class="pin" style="position: sticky; top: 0; height: 100vh">
       <canvas style="width: 100%; height: 100%; display: block"></canvas>
       <div class="captions">...</div>
     </div>
   </section>
   ```

4. **Wire the engine.**

   ```js
   import { ScrollFilm } from "./scroll-film.js";
   const small = matchMedia("(max-width: 760px)").matches;
   const film = new ScrollFilm({
     section: document.querySelector("#film"),
     canvas: document.querySelector("#film canvas"),
     frames: { count: 247, src: (i) => `film/${small ? "sm" : "lg"}/${String(i).padStart(3, "0")}.webp` },
     keys: [[0, 0], [0.18, 60], [0.3, 60], [0.62, 160], [0.72, 160], [1, 246]],
     onUpdate: ({ progress }) => captions(progress),
     onReady: () => document.body.classList.add("film-ready"),
   });
   ```

   `keys` are `[progress, frame]` pairs. Two keys with the same frame make a hold: the film waits at a beat while its caption scrolls in and out. Put a hold at every beat that carries words. Without holds, text slides over a moving picture and nobody reads it.

   `smooth` (default 0.18) eases the film toward the scroll position, frame-rate independently, so mouse-wheel steps become motion instead of jumps. If the page already smooths scrolling (Lenis), set `smooth: 1`.

   Captions and layers read `progress` in `onUpdate`. Fade a caption in over a short range at the start of its hold and out at the end; keep it off the busiest part of the frame, with a soft scrim behind if needed.

## Phones

A 16:9 film centre-cropped to a portrait phone usually loses the subject. Check the crop on every beat. If it fails, generate portrait (9:16) legs from portrait keyframes and ship them as a separate set, switched by a media query, and say up front that this doubles the video budget. A centre crop is acceptable only when every beat keeps its subject in the middle third.

Phones also get the small frame set and should stay under about 8 MB for the whole film.

## Loading

- Put frame 0 in the HTML as an `<img>` (or as the canvas background) so the first paint is the film, not a blank box.
- The engine loads frame 0, then the last frame, then a coarse-to-fine spread (every 64th, every 32nd, and so on), six at a time. A visitor who scrolls fast always lands near a decoded frame and sees it sharpen.
- Video mode fetches the whole file into a blob before playing, so seeks never wait on the network.
- Serve from a host that answers Range requests. `python3 -m http.server` does not, and videos it serves cannot seek; locally, use the `frame-capture` skill's serve.py.

## Reduced motion

With `prefers-reduced-motion: reduce`, the engine steps between the key frames (`reducedMotion: "steps"`, the default) instead of playing, so every beat still shows its picture. `"still"` shows only the last key frame.

## Check

- Record a scroll-through at low frame rate to judge pacing in seconds, with the `frame-capture` skill: `record.py URL check.mp4 --fps 8 --seconds 20 --scroll "0:0 18:100%"`.
- Scrub fast up and down: nothing blank, no flash at a seam, the pin releases cleanly at the end.
- Load on a throttled connection: first paint shows frame 0.
- Check a phone viewport and a short laptop viewport (1280x720): captions must not cover the subject.
