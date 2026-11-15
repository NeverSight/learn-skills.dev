---
name: motion-kit
description: Code-drawn motion graphics, animated videos, explainers of 1-3 minutes with a story, kinetic typography, transitions, editing, Three.js scenes, pixel-art and retro films (fixed palettes, dithering, chiptune, demoscene effects) and browser games with strong game feel. Use when you need to make a good-looking animation, video, explainer, intro, interactive scene or game in HTML/JS and render it to MP4, or to break down a reference video.
---

# Motion Kit

1. Read `00-agent-brief.md` in full. These rules are mandatory.
2. Read the files for the task:
   - any video: `01-pipeline.md`, `04-motion-easing.md`, `06-montage.md`, `12-render-qa.md`, `13-performance.md`;
   - choosing a style: `03-visual-style.md`;
   - transitions between scenes: `05-transitions.md`;
   - fire, particles, glow, grain, shaders: `07-effects-cookbook.md`;
   - titles and animated text: `08-kinetic-typography.md`;
   - music, sound effects, voice-over: `09-audio-sync.md`;
   - games: `10-games-juice.md`;
   - 3D: `11-threejs.md`;
   - pixel art, retro or fixed-palette looks, Mode 7 floors, dithered transitions, turning any scene into pixel art: `15-pixel-retro.md` and `runtime/pixel.js`, see `examples/pixel/`;
   - chiptune music and 8-bit sound effects as text (MML): `16-chiptune.md` and `runtime/chip.js`;
   - demoscene effects (plasma, tunnel, rotozoom, copper bars, metaballs, starfield) as functions of x, y, t: `17-demoscene.md` and `runtime/pixel-fx.js`;
   - a film longer than ~45 s, an explainer, a story on any topic: `14-long-form.md` and `runtime/README.md`, build on `runtime/film.js`, see `examples/gps/`;
   - a reference video to learn from: `node render/analyze.mjs ref.mp4 out/`, then read its report and sheets.
3. Show the plan as data first (style, beat grid, shots, events), then write the code. For a long film, the plan is `SCRIPT.md`: thesis, spine, through-line and the shot table (`14-long-form.md`).
4. Write the page to render fast from the start (`13-performance.md`): sprites instead of per-draw blur, no pixel readbacks in the frame loop, static layers cached. Iterate with `render.mjs --draft` on fragments.
5. After rendering, build a contact sheet (`render/contact-sheet.sh`), look at it, and fix issues by specific timecodes. Check single frames at full size with `render/still.mjs`.
