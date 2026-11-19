---
name: blueprint
description: Make animated explainers drawn like a Victorian patent sheet on blueprint paper. A mechanism is built part by part, each numbered with a leader line, each added because the last one fell short ("but… so…"), while tokens travel along lines and a one-line caption tells the story. Output is a `<blueprint-scene>` element (or a standalone HTML page) with play, step and replay controls. Use when the user asks for a blueprint or patent-drawing explainer, an animated diagram of how a system, algorithm or process works, a "how X works" scene for docs, a README, a blog post or a talk, an explainer of an incident or postmortem, an explainer as a GIF, video, image or slides, or types /blueprint [topic].
---

# Blueprint

One scene explains one mechanism. The sheet starts empty. Each step draws in the parts it needs, moves something along a line, or changes a part's state, and shows one caption. Parts are numbered like a patent drawing, and the captions refer to them by number. The finished sheet must explain the idea on its own as a still image.

The drawing is done by `runtime/blueprint.js`. You never draw SVG: you write a scene, a plain object of parts, lines and steps, and the runtime draws it, animates it and adds the controls.

## Files

- `runtime/blueprint.js`: the whole runtime. Defines `<blueprint-scene>`, `BLUEPRINT.scene(id, spec)` and `BLUEPRINT.mount(el, spec, opts)`. Copy it unchanged.
- `references/craft.md`: the scene format, every part kind with its sizes and states, line kinds, step actions, the metaphor catalogue and the mistakes already made once. **Read it before writing a scene.**
- `templates/scene.js`: the starting point.
- `templates/incident.js`: the starting point for an incident or postmortem sheet (see **Incident sheets**).
- `scripts/check.mjs`: lints a scene without a browser (unknown ids, empty scenes, parts no step draws, overlaps, lines through parts or text, labels off the sheet, long captions).
- `scripts/frames.mjs`: renders the scene frozen at chosen moments into one contact-sheet PNG and reports runtime errors.
- `scripts/build.mjs`: turns scene files into a standalone HTML page with the runtime inlined.
- `scripts/export.mjs`: renders a scene to GIF, MP4 or PNG for places that cannot run JavaScript.
- `examples/small/` (10 scenes, 3–6 steps) and `examples/complex/` (11 scenes, 7–10 steps, camera moves). `examples/small/cache.js` is the cleanest small one, `examples/complex/url.js` the cleanest complex one.

## Workflow

1. **Find the mechanism.** In one line: what goes in, what comes out, and what the reader should understand at the end. Then write the "but… so…" chain: the simplest version first, the problem it has, the part that fixes it, the next problem, and so on. Each link becomes a step. If you cannot write the chain, the topic is too broad: pick one mechanism inside it.
2. **Pick the parts** from the kit, using the metaphor catalogue in craft.md (a cache is a drawer, a queue is a rack of slots, auth is a lock and key, a rate limit is a tank). Pitch two or three framings in one line each and let the user choose, unless they said to just go.
3. **Lay out the sheet on paper first.** Flow runs left to right, layers top to bottom. Fix every part's centre (`at`) on a 20 px grid with at least 40 px between parts, then the lines, then the steps. Start from `templates/scene.js`.
4. **Lint it** until it prints `clean` (it also flags a line running through a label, numeral or note, and parts or lines that no step draws):
   ```sh
   node <skill-dir>/scripts/check.mjs path/to/scene.js
   ```
   `<skill-dir>` is the folder this SKILL.md is in. Fix every warning unless the overlap is deliberate.
5. **Look at it.** Render a contact sheet and Read the PNG:
   ```sh
   # once, in <skill-dir>:  npm i && npx playwright install chromium
   # (or in a scratch dir: npm i playwright@1.56.1 && npx playwright install chromium, and prefix NODE_PATH=<scratch>/node_modules)
   node <skill-dir>/scripts/frames.mjs path/to/scene.js --out /tmp/scene.png
   ```
   It exits 1 if the scene has errors or the page throws. The default sheet shows the middle and the end of every step. Pick other moments with `--frames "s2:0.4,s3:end,end"`. Check that nothing is cropped, no text sits on a line or a part, every token is visible where it should be, the camera frames what the caption talks about, and the last frame explains the whole idea on its own. Two or three rounds is normal.
6. **Ship it.** Either embed it:
   ```html
   <blueprint-scene scene="cache" play="view" key></blueprint-scene>
   <script src="/blueprint/blueprint.js" defer></script>
   <script src="/blueprint/cache.js" defer></script>
   ```
   (`blueprint.js` must come first in document order), or export one page: `node <skill-dir>/scripts/build.mjs scene.js --out scene.html`.

   When the user asks for a GIF, video, image or slides, or the sheet is going somewhere that cannot run JavaScript (a GitHub README, Slack, X, Notion, a deck), export it:
   ```sh
   node <skill-dir>/scripts/export.mjs scene.js --format gif     # README, Slack
   node <skill-dir>/scripts/export.mjs scene.js --format mp4     # X, LinkedIn, talks
   node <skill-dir>/scripts/export.mjs scene.js --format png     # the finished sheet, 2x
   node <skill-dir>/scripts/export.mjs scene.js --format png --steps   # one PNG per step, for slides
   ```
   `--format all` writes all three. Useful options: `--out` (a name ending in `.png`/`.gif`/`.mp4` sets the file name and each format keeps its own extension; anything else is a folder), `--scene <id>` (for a file with several scenes), `--width` (default 1280), `--speed` (GIF 1.8×, MP4 1.25×), `--fps`, `--paper`, `--audio track.mp3` (MP4 only; the video sets the length). Keep a GIF under about 5 MB: `export.mjs` warns past that, and a complex scene usually fits with `--width 960`. GIF and PNG need only Playwright. MP4 uses ffmpeg when it is on PATH; otherwise Chromium encodes it (WebCodecs), which covers macOS with nothing else installed; on Linux install ffmpeg, or set `BLUEPRINT_CHROMIUM` to a distro Chromium with H.264 (Fedora's has it). `--encoder ffmpeg|browser` forces one. Exports do not carry the scene's `sources`: give the user the links to post with it. Read one exported frame or the PNG back before handing it over.

## The element

- `scene`: the id given to `BLUEPRINT.scene('<id>', …)`.
- `play`: `loop` (default: plays, fades and starts over), `view` (plays once when it scrolls into view, then holds the finished sheet), `click` (waits for a click), `still` (shows the finished sheet).
- `paper`: `blue` (cyanotype, default) or `linen` (ink on cream, the patent-office look). A scene can set its own with `paper: 'linen'`.
- `key`: shows the parts list under the sheet ("1 Cache · a drawer by the door…") from each part's `name` and `note`.
- `no-controls`: hides the play, step and replay bar. Clicking the sheet still pauses and plays.
- `no-font`: does not load IBM Plex Mono from Google Fonts.
- `speed`: playback rate, e.g. `speed="1.25"`.
- Reduced motion shows the finished sheet; the step buttons jump between finished steps. Off-screen scenes do not animate.

## Incident sheets

When the topic is an outage, a breach or a postmortem, start from `templates/incident.js` and keep its story shape: a normal day, the change or trigger, what broke (with a number), how it was noticed, what stopped the damage, recovery, the root cause in plain words, the fix that prevents it (the "So…" step), and a timeline in the last step's note.

- **Facts only.** Every time, number and claim comes from the user's postmortem, status page or tickets, or from published coverage for a public incident. Put the links in the scene's `sources` (`[['Postmortem', 'https://…'], …]`, http(s) only); the site and `build.mjs` pages list them under the sheet, but GIF, MP4 and PNG exports do not, so pass them on with the export. If a fact is missing, ask for it or leave it out; never invent one.
- **Blameless.** Name systems and changes, never people ("a config change", not "Ravi's change").
- **One clock.** All times in one time zone, said once in the timeline.
- **The fix earns its part.** The prevention is a new part drawn in with "So…", like any other part.

## Style rules

These come from the reading behind the style (Byrne, Victor, Ciechanowski, Thing Explainer, patent drawing conventions). Keep them.

- **Concrete first.** Open with one specific thing: a request for item `#42`, the name `example.com`, three key presses. The general rule comes at the end, after the reader has watched one real case.
- **But… so….** Every part after the first arrives because of a problem the reader just saw. The caption of the step that shows the problem ends on it ("…and every lookup is slow."); the next step's caption starts with "So" and adds the part.
- **Number parts in the order they appear** (1, 2, 3…) and refer to them in captions as "(2)". Give every numbered part a `name` and `note` for the key.
- **Plain words in captions.** Write for a curious twelve-year-old: "a drawer by the door that keeps recent answers", not "an LRU cache layer". Put the term of art in the label (`CACHE`) and the key, once.
- **One caption, one sentence, under 100 characters.** It says what is happening now, not what happened.
- **Yellow is for what moves or matters now.** Red only for a failure, green only for success. Everything else is line work.
- **Real numbers.** Notes carry real units: `~120 MS`, `4 KB`, `3 TRIES`. Use the `dim` line for a measured span.
- **Every step changes something.** If a step only has a caption, merge it into the next one.
- **Small scenes: 3–6 steps, 3–6 parts, one sheet.** **Complex scenes: 7–10 steps, 6–14 parts, and the camera (`view`) zooms to the part being discussed, then pulls back.** End complex scenes on the full sheet.
- **The last frame is a summary.** By the final step every part is drawn, the last note stays up, and a reader who only sees the still gets the idea.
