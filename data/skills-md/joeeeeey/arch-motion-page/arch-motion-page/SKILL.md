---
name: arch-motion-page
description: Compile a product or technology architecture into a one-page animated A4 blueprint (live HTML, poster PNG, HyperFrames MP4) from a small YAML spec. Use for animated architecture explainers, "A4 architecture page with motion", HyperFrames architecture videos, or turning a system analysis into a motion one-pager.
license: MIT
metadata:
  author: Joey (github.com/joeeeeey)
---

# arch-motion-page (amp)

By **Joey** ([@joeeeeey](https://github.com/joeeeeey)) · [live demo](https://joeeeeey.github.io/arch-motion-page/) · [repo](https://github.com/joeeeeey/arch-motion-page) · MIT

[![The example page drawing itself, then a Director card dispatching packets to six specialist cards](https://raw.githubusercontent.com/joeeeeey/arch-motion-page/gh-pages/media/skills-sh-hero.webp)](https://joeeeeey.github.io/arch-motion-page/)

amp turns an architecture analysis into one A4 page. The page has a header, a brand column, a three-tier figure and three columns of academic-style text. It builds itself in about 3 s, then loops a heartbeat story: the root pulses, signal packets travel the edges, each worker card swells as its packet lands, and the hand-off flows into the substrate. Edges march, mascots bob and a neon gradient wordmark breathes. After the build, every frame is a usable poster. The default skin is white paper with black type (`plush-academic`); `blueprint` is the navy alternative. Pages can be English or Chinese (`meta.lang: zh`).

**Division of labour.** The agent writes only `spec.yaml`. Deterministic compilers own every coordinate, colour and keyframe:

```
spec.yaml ─▶ lib/spec.mjs (validate, budgets)
          ─▶ lib/archetypes/tiered.mjs (boxes, edges, packet routes)
          ─▶ templates/paper-a4.mjs + themes/<name> (HTML/CSS)
          ─▶ lib/motion.mjs (JSON op list) ─▶ runtime/amp-runtime.js (ONE paused GSAP timeline)
          ─▶ out/index.html  (also a valid HyperFrames composition)
```

## Hard rules

- Never hand-edit `out/`. Every fix goes into the spec. Fix the compiler, theme or template only when the defect is generic.
- Keep the page deterministic:
  - No wall-clock reads.
  - No unseeded randomness.
  - No network at view time: the build copies GSAP (from npm) and the Latin fonts (`vendor/fonts/`) into `out/`, subsets CJK fonts into `out/fonts/`, and assets live inside the spec folder.
- Run third-party tools in containers. Font subsetting (zh pages and `--single`) runs pyftsubset in Docker with `--network none`; the CJK sources are pinned downloads, verified by sha256 and cached in `~/.cache/arch-motion-page/`.
- Review at the HTML stage with `scripts/review.mjs`.
  - Render video only after the HTML passes review **and** the user approves.
  - Render only inside Docker (`scripts/render.sh`). Never run `npx hyperframes` on the host.
- Images are optional. Generate them with whatever image tool is available (an installed image-generation skill, or any model that outputs PNG with a transparent background), and keep each prompt next to its asset in `assets/source/*.prompt.txt`.
  - Never print API keys or image-tool config.
  - Never commit generated assets that contain anything sensitive.

## Workflow

0. **Setup (once):** run `npm install` in this skill dir. It needs Node ≥ 22 and a local Chrome (override with `CHROME=/path`).
1. **Analyse the system into three tiers**, using `references/design-grammar.md`:
   - **root**: the entry point or orchestrator, exactly one node.
   - **workers**: 3–7 roles or services.
   - **substrate/outcome**: 2–6 shared stores, platforms or results. The last node is usually the outcome.

   Then pick:
   - The **one story** worth looping: which workers, in which order.
   - An optional **feedback edge**: outcome → root.
2. **Write the spec.**
   - Start a work dir outside the skill, e.g. `/tmp/amp-<slug>/`.
   - Copy `examples/self-intro/spec.yaml` there as a template.
   - Fill it using `references/spec-schema.md`. Respect the character budgets, because the build warns on every overrun. Budgets count a CJK character as width 2.
   - Language variants sit next to it as `spec.<lang>.yaml` (e.g. `spec.zh.yaml` with `meta.lang: zh`) and build into `out-<lang>/`.
3. **Assets (optional):**
   - Use node `icon:`s from the built-in set; no images needed.
   - Or generate a plush cast and a brand image:
     ```bash
     # any image tool: one 2048x1024 PNG character sheet, transparent background
     <image-tool> --prompt-file cast.prompt.txt --size 2048x1024 --background transparent \
       --output /tmp/amp-assets/cast.png
     uv run --with pillow --with numpy python scripts/slice_cast.py /tmp/amp-assets/cast.png \
       <workdir>/assets/mascots --grid 4x2 --names a,b,c,d,e,f,g,h --height 240
     ```
   - The prompt recipe is in `examples/self-intro/assets/source/`.
4. **Build:** `node scripts/build.mjs <workdir>/spec.yaml`. This writes `<workdir>/out/`. Pass `--theme <name>` to try another skin. The first zh build creates the `amp-fonttools` image and downloads the Noto SC fonts once; later builds take seconds.
5. **Review:** `node scripts/review.mjs <workdir>/out`. Then:
   - Read `review/contact.png` and the console fit report.
   - Zoom into the figure with `--zoom 288,148,752,520`, or into the hero with `--zoom 40,148,1000,520`.
   - Score against `references/review-rubric.md`, edit the spec, rebuild, and repeat.
   - The page is done when the fit report says OK, columns fill 88–99%, the review prints `loop seam … OK`, and the rubric passes.
6. **Present or publish as HTML:**
   - `out/index.html` autoplays when opened: the build plays once, then the live story loops from `loopFrom` (about 3.4 s) to the end. Both ends of that window are the same frame, so the page never jumps back to blank. `?once` plays everything once and holds the last frame. It sits centred on a desk at 1:1 when the window is wide enough and scales down to the window width otherwise.
   - Keys: Space play/pause (at the end it resumes the loop), F fit the whole page, ← → step 1 s, Home replay from the build. `prefers-reduced-motion` holds the poster frame.
   - `?fit` starts fitted, `?poster` shows the end-of-build frame, `?t=12.5` holds any frame, `?debug` outlines fit offenders, `?review` is the 1:1 top-left mode the review script uses.
   - To publish, build with `--single`. It writes `out/single/<id>[-<lang>].html` with scripts, subset fonts and images inlined (about 3–4 MB for the example), so it can be sent or hosted as one file. Check it with `review.mjs out --page single/<file> --present`.
7. **Render (approval required):** `scripts/render.sh <workdir>/out [--output video.mp4] [--quality high]`. It runs `hyperframes lint`, `check` and `render` inside a container.

## Commands

| Command | Purpose |
|---|---|
| `node scripts/build.mjs spec.yaml [--out dir] [--theme name] [--single]` | Compile the page. Prints language, build-in time, loop window, op count, packets, budget warnings and loop-seam warnings. `--single` also writes one self-contained HTML file. |
| `node scripts/review.mjs out [--times a,b] [--zoom x,y,w,h] [--scale 2] [--page f.html]` | Frames at named events, `contact.png`, `report.json` and the loop-seam pixel diff. `out-zh` reviews into `review-zh`. |
| `node scripts/review.mjs out --present 1440x900,820x1180,1440x900:fit` | Also capture present mode (centred, scaled; `:fit` = whole page) as `present-WxH.png`. |
| `node scripts/review.mjs out --burst 3:6:15` | Frame burst plus `burst.mp4`, to check motion smoothness without HyperFrames. |
| `node scripts/review.mjs out --times 0.9,1.6,3.2 --thumb 320 --dest d` | Small frames for a `filmstrip` block (the page can show itself). |
| `scripts/render.sh out [--check-only] [--output f.mp4] [--fps 30] [--quality looks]` | HyperFrames lint, check and render in Docker. |

## Files

- `lib/`: spec loader, archetypes, motion compiler, inline markup, icons, `lang.mjs` (locale strings, CJK font families and CSS), `fonts.mjs` (pinned downloads, Docker subsetting).
- `templates/paper-a4.mjs`: page geometry (`GEOM`) and HTML.
- `themes/<name>/`: `theme.json` (hues, fonts, `extends`) and `theme.css`.
- `runtime/amp-runtime.js`: plan interpreter, playback modes and fit report.
- `vendor/fonts/`: Tinos, Inter and JetBrains Mono, all SIL OFL 1.1 (license texts alongside). GSAP 3.15 is an npm dependency, not vendored: its license does not grant redistribution.
- `examples/self-intro/`: amp explaining amp. This is the reference spec, and its filmstrip shows the page's own build.
- `references/`:
  - `spec-schema.md`, `design-grammar.md`, `motion-grammar.md`, `review-rubric.md`.
  - `extending.md`: new themes, archetypes and effects.

## Gotchas

- Text that is too long is the most common failure.
  - Budgets: tier-1 titles ≤ 12 chars, subs ≤ 44; tier-2 titles ≤ 14, subs ≤ 34.
  - Body columns are fixed at 728 px tall. Trim prose or swap blocks instead of shrinking type.
- YAML: quote any value that contains `#`, `: `, or starts with `*`, `&`, `[` or `{`.
- CJK prose: write each paragraph on one line (quoted). Folded `>-` scalars join lines with a space, which shows up as a stray gap between Chinese characters.
- zh node subtitles break only at punctuation and spaces (`keep-all`). Put a `、`, `，` or space where a two-line label should break.
- Assets must sit inside the spec folder. The build copies them into `out/`, so the output folder is self-contained.
- If the story timing looks uneven, check `out/amp-build.json` → `events`. Spot beats should be evenly spaced.
- `render.sh` gates on `hyperframes check`, which audits text contrast: copy needs 4.5:1 (3:1 for large text). Fix the theme colour; only decoration and logotypes may carry `data-layout-ignore` (the template sets it on the stamp and the wordmark).
- `review.mjs` clears its review dir on every run. Copy anything worth keeping (posters, preview MP4s) into a sibling `share/` dir, which is gitignored for the examples.
