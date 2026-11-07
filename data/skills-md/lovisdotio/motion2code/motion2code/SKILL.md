---
name: motion2code
description: >-
  Rebuilds an AI-generated (or any) flat motion design video as clean, editable code: inline SVG shapes animated by
  one GSAP timeline, seekable frame by frame, looping seamlessly, checked side by side against the source; and
  optionally turns an interface recording into a real interactive website (GSAP ScrollTrigger, real clicks).
  Ships scripts to study the video (frames, cuts, contact sheet, exact palette), render the code to mp4/GIF through
  anim.seek, compare it with the source frame by frame and check the loop seam and page contract. Use when the user
  wants a video, GIF, Lottie-like clip, motion design shot, animated logo, UI screen recording or AI video
  "recreated in code", "converted to SVG/GSAP", "made into an HTML animation" or "made into a real site". Not for
  photographic footage, 3D rendering or video editing.
license: MIT
metadata:
  hermes:
    tags:
      - svg
      - gsap
      - motion-design
      - animation
      - video-to-code
      - scrolltrigger
    category: development
---

# Motion2Code

The video is the spec, and you cannot watch it. Treat the job as reconstruction: turn the clip into images you can
look at, write down what happens and when, build the shapes, drive them with one clock, then prove every moment
against the source with images side by side. Never animate from a memory of the video.

## Workflow

1. **Study the source.** `python3 scripts/study_video.py source.mp4 -o study/` saves a frame every 0.25 s, the
   frames around every cut, a contact sheet, the exact flat palette and whether the source already loops. Open the
   sheet, then the frames. Read the prompt file next to the video if there is one: it holds the exact words.
2. **Write the shot list.** One line per beat: time range, what each shape does, how it eases, what it becomes
   next. Note the stage size (1920x1080 or 1080x1920) and the real duration (ffprobe, e.g. 15.10 s means a 15 s
   loop). See `references/study-the-source.md`.
3. **Build the stage** from `templates/index.html`: one inline SVG at the source resolution, every shape drawn
   around its own origin, flat fills from the sampled palette, the closest Google Font subset to the exact letters.
4. **Animate on one GSAP timeline.** Tweens for the shots, plus a pure `draw(t)` for procedural parts (particles,
   morphs, physics) called from the same clock. Match the timing of the frames, not your idea of it.
   See `references/animation-architecture.md` and `references/motion-vocabulary.md`.
5. **Close the loop in code.** The last moment returns to the exact opening frame, even when the source does not.
   See `references/seamless-loop.md`.
6. **Verify, fix, repeat.**
   `python3 scripts/frame_diff.py source.mp4 index.html -o diff/` writes source|code pairs and a score per time;
   open the pairs, fix the worst first, then zoom on transitions with `--every 1/24 --start a --end b`.
   `python3 scripts/check_anim.py index.html --runtime` checks the contract, the loop seam, determinism, console
   errors and network. Ship only when both are clean. See `references/verification.md`.
7. **Deliver:** `index.html`, `compare.html` (from `templates/compare.html`), and when asked the proof videos:
   `python3 scripts/render_anim.py index.html -o anim.mp4` then
   `python3 scripts/side_by_side.py source.mp4 anim.mp4 -o side_by_side.mp4 --html index.html`.
8. **Optional real site.** For an interface recording, after the faithful replay, build `site.html` from
   `templates/site.html`: scroll becomes ScrollTrigger, fake clicks become real buttons.
   See `references/interfaces-and-sites.md`.

Scripts need Python 3.9+, ffmpeg, and Playwright for anything that opens a browser
(`uv run --with playwright python scripts/...`, or `pip install playwright && python -m playwright install chromium`).
Run them from this skill's directory or with full paths.

## The page contract

```js
window.anim = { tl, duration, seek(t), play(from), pause() }   // seek(t) is a pure function of t
```

- `index.html?t=6.5` freezes at 6.5 s; `?external=1` does not autoplay (compare.html and the scripts drive it);
  with no parameter it plays by itself and loops forever.
- `<html data-ready="1">` once fonts are loaded and frame 0 is drawn. Renderers wait for it.
- `frame(duration)` equals `frame(0)`; `frame(duration - 1/24)` is one step away from it.
- Self-contained: inline SVG, GSAP 3 from cdnjs, flubber from jsdelivr only when a morph needs it, Google Fonts.
  Nothing else is loaded.

## Hard rules

- **Use only the given source video.** Never regenerate it, never fetch "a better version", never trace a frame
  into the page. No `<img>`, `<video>`, SVG `<image>`, canvas `drawImage` or raster data URI in the animation.
- **Words exactly as in the source prompt** (or the video if there is no prompt), even when the video misspells
  them. Invented gibberish words in UI recordings become flat bars or are removed.
- **Flat shapes as SVG.** Solid fills, the sampled hex colors, no gradients, shadows or filters the source does not
  have. Strokes with `stroke-linecap="round"` for sticker outlines.
- **GSAP timeline is the single clock.** No `requestAnimationFrame` loops, `setTimeout` choreography, CSS
  animations or `Date.now()` driving visuals. Randomness is seeded and precomputed.
- **The loop is done in code.** If the source does not return to its opening frame, add a short clean transition
  back to it. The seam is checked numerically.
- **Every moment is checked against the source side by side**, at least every 0.5 s and frame by frame around
  every transition and the loop seam. "Looks right" without a pair image is not a check.
- **Same timing as the source.** Measure from the frames; do not compress, pad or reorder beats.

## Reference routing

Read only what the task needs:

| File | Read when |
|---|---|
| `references/study-the-source.md` | starting: frames, cuts, palette, shot list, words, duration, aspect |
| `references/animation-architecture.md` | building: stage, shape origins, timeline vs draw(t), keyframe helper, morphs, fonts, determinism |
| `references/motion-vocabulary.md` | matching the feel: snaps, squash and stretch, smears, elastic settles, iris wipes, morph chains |
| `references/seamless-loop.md` | the source does not loop, or the seam jumps |
| `references/verification.md` | checking and proof videos: frame_diff, compare.html, check_anim, render, side by side |
| `references/interfaces-and-sites.md` | the source is a website/app recording, or a real `site.html` is wanted |

Templates: `templates/index.html` (the contract, a tiny looping example), `templates/compare.html` (video and code
side by side, synced to the video clock, frame stepping, onion skin), `templates/site.html` (ScrollTrigger pin and
scrub, menu, tabs, flip card, draggable slider, cart counter, keyboard, reduced motion).

## Output expectations

- Deliver `index.html` (+ `compare.html`, + `site.html` for interfaces) and say what was checked and how:
  frame_diff times, worst scores and what they were, `check_anim.py --runtime` result, page size.
- List honestly what differs from the source (a simplified texture, a merged beat), never "pixel perfect".
- Keep names readable: one group per character or object, ids that say what they are, the palette as constants,
  shots commented with their time range, so a designer can retime or recolor without reading everything.
