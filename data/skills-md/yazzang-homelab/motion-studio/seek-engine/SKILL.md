---
name: seek-engine
description: "Build, debug or speed up the seek(t) render engine: render contract, canvas vs page capture, workers/subframes/chunks, determinism fixes, Remotion or HyperFrames handoff. Use for 'render is slow', 'frames differ', 'use Remotion'."
argument-hint: "[symptom or goal]"
---

# Seek engine (course step 07)

A film here is a program, not a video. The page paints the exact frame for any time `t`; the renderer walks time,
captures each frame and pipes it into ffmpeg. Nothing depends on a clock, so a render is identical on every run and a
fix is a one-line edit plus a re-render. This is route A, the route Opus picks by default. Use it unless the user
names Remotion or HyperFrames (then read [references/route-b.md](references/route-b.md)).

Run everything from the film project root (the folder with `studio.json`). If there is none, run
`/motion-studio:studio-init` first. Files of this skill live in `${CLAUDE_SKILL_DIR}`; the relative links below point
there (`${CLAUDE_SKILL_DIR}/references/determinism.md`, `${CLAUDE_SKILL_DIR}/references/route-b.md`).

## 1. The two halves

| Half | Files | Job |
|---|---|---|
| Page | `index.html`, `film/film.js`, `lib/runtime.js` (+ `lib/*.js`) | `boot(film)` loads `studio.json`, `audio/beats.json` (optional) and bundled fonts, then exposes `window.seek(t)` and `window.__studio` |
| Driver | `tools/render.mjs` (+ `tools/studio.mjs`) | serves the project on `http://127.0.0.1:<random>`, launches a headless browser (Windows: Playwright's headless shell, never an installed Chrome or Edge; macOS and Linux: Chrome, Edge, then the bundled one), opens N worker pages, captures frames in order, encodes one H.264 stream |

The page is always served over http. `file://` breaks `fetch('studio.json')`, ES modules and paths containing `#` or `%`.

## 2. The render contract

| Member | Contract |
|---|---|
| `?format=9x16&scale=1&render=1` | query the driver sends; `format` defaults to `studio.primaryFormat`, `scale` 0.1–1 |
| `window.seek(t, blur?)` | synchronous paint of time `t`; loop films wrap with `loopT`, others clamp to `[0, duration]`; returns `true`. The optional second argument `{ frameT, sub, subs }` says this paint is subframe `sub` of `subs` of the output frame centred on `frameT` (page capture sends it for every screenshot) |
| `__studio.ready` | Promise; resolves after config, beat grid, fonts (`loadFonts` asserts every face) and `setup()` are done |
| `__studio.error` | string stack when boot failed (the driver prints it) |
| `__studio.meta` | `{ title, duration, fps, format, width, height, logicalWidth, logicalHeight, scale, bpm, loop, capture }` |
| `__studio.frame({ t, sub, shutter, fps, wrap })` | PNG data URL of frame `t`; `sub > 1` accumulates centred subframes in the page (motion blur); `wrap: false` paints the raw time clamped to `[0, duration]` even in a loop film |
| `__studio.hash(t, { wrap, sub, shutter, fps })` | sha256 of the raw pixels after `paint(t)` (determinism checks); `hash({ t, wrap: false })` is accepted too. `hash(0)` versus `hash(duration, { wrap: false })` is the loop-closure invariant |
| `__studio.pixels(t, w)` | small RGBA thumbnail as base64 (critique metrics); always wraps in loop films |
| `__studio.cues()` / `shots()` / `grid` | SFX cues, shot windows, beat grid as JSON (read by `sfx.mjs`, `stills.mjs --shots`, `critique.mjs`). `shots()` is in time order and lists scenes only, never `overlays`; `grid` carries `hits` |
| `__studio.textUse()` / `coverage(family, weight, style, chars)` / `textTrack` | the critique's glyph check. With `window.__TEXT_TRACK__ = true` before load (or `?texttrack=1`) `lib/draw.js` records the characters `text()`, `kinetic()` and `textWidth()` draw per font; `textUse()` resolves `[{ family, weight, style, chars }]` for the frames painted so far (`seek()` through the film first), `coverage()` resolves `{ missing, checked }` for one face. Off by default, never changes a pixel; `text()` and `kinetic()` do not throw for an unregistered family |

What a scene sees in `c` while a motion-blurred frame is made: `c.t` is the time being painted (the SUBFRAME time, so
motion blurs by itself), `c.frameT` the output frame's centre time (the same for every subframe), `c.frame` the output frame
index `floor(frameT x fps)` (the same for every subframe), `c.sub` / `c.subs` the subframe index and count. Frame-indexed
noise uses `c.frame` (`grain(g, W, H, c.frame)` then looks the same in stills, preview and the final), and "on twos" uses
`stepTime(c.frameLt, 12)`. Details: `docs/ARCHITECTURE.md` section 5.2 in the plugin.

Film code obeys the rules in [references/determinism.md](references/determinism.md). The short form: every value is a
function of `t`; seeded randomness per element with `rngFor(name, i)`; no `Math.random`, `Date`, `performance.now`,
timers, `requestAnimationFrame`, CSS transitions or state carried between frames; fonts and assets are local files.
`npm run lint` checks this, and the plugin hook lints each edit to `film/`, `lib/` and `index.html`.

## 3. Commands

| Goal | Command |
|---|---|
| Live preview (scrub, Space, arrows, `[`/`]` shots, F formats, G safe guides) | `npm run preview` |
| Environment check (Node, Playwright, browser, ffmpeg, fonts, keys present) | `npm run doctor` |
| Install the Windows default browser (Playwright's headless shell, about 115 MB) | `npx playwright install chromium-headless-shell` (`npm run setup:browser`) |
| Fast pacing check (half scale, 30 fps, no blur) | `npm run animatic` (writes `out/animatic/<fmt>/silent.mp4`) |
| Render the primary format | `npm run render` |
| Render a time range for a check | `node tools/render.mjs --from 4 --to 6 --draft --out out/check` (writes `out/check/<fmt>/clip_4.00-6.00.mp4`) |
| Render every format | `npm run render:all` |
| Final render, all formats (blocked until the critique gate passes; about 4 min for the 12 s demo, so run it in the background) | `npm run render:final` |
| Long form, resumable segments | `node tools/render.mjs --format all --final --chunk 10` |
| Per-frame hash manifest | `node tools/render.mjs --hash` (writes `frames.sha256`; a range writes `clip_<from>-<to>.sha256`) |

Output per format: `out/<fmt>/silent.mp4`, `out/<fmt>/poster.png` (at `studio.poster` or 0.35 x duration) and
`out/<fmt>/render.json` (fps, frames, workers, browser version, capture, encode settings, seconds). `mix.mjs` reads
`render.json` for the exact audio length. Everything is built in `out/<fmt>/.staging/` and published as one unit: the
old files move aside first, the new ones move in with `silent.mp4` last, and any failure puts the old ones back. If
another program holds an output open (a video player, an image viewer on Windows), the render waits up to 30 s
(`MOTION_PUBLISH_WAIT_MS`), warns at the start which files are open, and otherwise stops with `cannot replace <file>:
EBUSY ...` and KEEPS the finished render in `out/<fmt>/.staging/` (the previous outputs stay untouched). Close the
program and copy the files from `.staging/`, or render again. A full render with `--no-poster` removes the previous
`poster.png`, and one without `--hash` removes the previous `frames.sha256`, so no output describes an older cut.

A range render is partial only when `--from`/`--to` leave frames out; it writes `clip_<from>-<to>.mp4` with its own
`.json` and `.sha256` instead, never replaces `silent.mp4`, and cannot be `--final`. A range that covers the whole film
(or a `--to` past the end) is a full render. Keep check renders under `--out out/check` so `out/<fmt>/` holds only the
real film.

## 4. Capture modes

| Mode | Set by | How a frame is made | Use for |
|---|---|---|---|
| `canvas` (default) | nothing | `__studio.frame` paints `sub` subframes at `t + ((j + 0.5) / sub - 0.5) * shutter / fps`, sums pixels in the page, returns one PNG | everything drawn on `<canvas id="stage">` |
| `page` | factory returns `capture: 'page'` or `studio.json` `"capture": "page"` | `seek(t)` then `page.screenshot` per subframe; ffmpeg `tmix` + `select` blends each group | DOM films (styled elements updated from `t`) |

`shutter` 0.5 is a 180-degree shutter: the blur spans half a frame interval. Fast whips and pans can show ghost copies
at `--sub 4`; raise to `--sub 8` for those films. Page capture is slower (one screenshot per subframe) and inherits
DOM rendering differences, so prefer canvas.

## 5. Performance knobs

Paint count = frames x subframes. A 12 s film at 60 fps with `--sub 4` is 2,880 paints per format.

| Flag | Default | Effect | When |
|---|---|---|---|
| `--workers N` | `min(4, max(1, floor(cpus / 3)))` | parallel pages in one browser feed one ordered encoder | raise on big machines; lower if RAM is tight |
| `--scale s` | 1 | canvas = even(round(W x s)); 0.5 = a quarter of the pixels | drafts, stills of long films |
| `--sub N` | `studio.subframes` (4) | subframes per frame | `--sub 1` for drafts; 8 for fast motion |
| `--fps N` | `studio.fps` (60) | output frame rate | 30 for animatics |
| `--draft` | off | `encode.previewPreset` + CRF 23 | any non-final render |
| `--crf N` / `--preset p` | 16 / slow | x264 quality / speed | leave for finals |
| `--chunk S` | off | resumable `out/<fmt>/.parts/seg_<a>_<b>.mp4`, then concat `-c copy` | films over ~30 s, a final of three formats, overnight runs (an interruption then resumes instead of restarting) |
| `--no-poster` | poster on | skip the poster still | batch checks |

Measured on the reference laptop (12-thread i7-1255U, installed Chrome, 1080x1920, 60 fps, 4 subframes, 4 workers; the Windows
default is now the headless shell, whose per-frame speed was not re-measured, and which adds 15 to 25 s per tool run for
start-up on a machine with real-time antivirus, measured):

| Setup | Time per output frame | Time for 15 s at 60 fps |
|---|---|---|
| the course's screenshot-per-subframe loop (capture only, synthetic scene of 200 arcs, text and a gradient) | about 1,575 ms | about 24 min |
| in-page accumulation with 4 pages (the same synthetic scene, capture only, pixel-identical) | about 148 ms | about 2.2 min |
| this renderer end to end on the template's 12 s demo film, final x264 encode | 123 ms in 9x16, 75 ms in 1x1, 118 ms in 16x9 | 1.8 min in 9x16 (about 4 min for the three formats of the 12 s film) |

The first two rows are the capture-only benchmark that chose the design; the last row is what a real film costs, and is
the figure to quote as an estimate (it rises with scene complexity and with other programs loading the machine, up to
about 5 min for the three formats). x264 `-preset slow` encodes about 18 fps at that size, so capture is the
bottleneck. Progress, fps and ETA print on stderr once per film-second. Start a final render in the background and poll
the log; never wait for it in the foreground.

## 6. Proving determinism

1. `npm run critique` runs the determinism check: `__studio.hash` at times that straddle every shot boundary and cue
   (plus and minus one frame), pass A in order, pass B shuffled, pass C after a reload. `out/review/<fmt>/metrics.json`
   lists every mismatching `t`.
2. After a range render, prove the range is deterministic with two hashed renders of the same range. Vary the worker
   count so parallelism is covered too:
   `node tools/render.mjs --from 0 --to 2 --hash --draft --no-poster --json --workers 1 --out out/check/a` and
   `node tools/render.mjs --from 0 --to 2 --hash --draft --no-poster --json --workers 4 --out out/check/b`.
   A range never touches `silent.mp4`. Each run writes `out/check/<a|b>/<fmt>/clip_0.00-2.00.mp4` plus `.json` and
   `.sha256` (one line per frame: `index t sha256`), and its `--json` line reports `framesDigest`, the sha256 of the
   hash column joined by newlines. Equal `framesDigest` values in every format mean identical frames. If they
   differ, compare the two `.sha256` files: `git diff --no-index --quiet out/check/a/<fmt>/clip_0.00-2.00.sha256
   out/check/b/<fmt>/clip_0.00-2.00.sha256` exits 0 when they match and `git diff --no-index` shows the first frame
   that differs. Never `md5`, which does not exist on Windows or Linux.
3. Do not hash the mp4: x264 output changes with the thread count, so mp4 hashes differ across machines. The
   `framesDigest` covers the frame PNGs that go into the encoder, which is what determinism is about.

The promise is bit-identical frames on the same machine and browser build (recorded in `render.json`). Across
machines, fonts rasterize differently (DirectWrite, CoreText, FreeType); compare visually.

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Executable doesn't exist ... chromium_headless_shell`, or `could not launch a browser: no safe browser found.` (Windows) | Playwright's headless shell is not downloaded (`npm install` does not fetch it) | `npx playwright install chromium-headless-shell`. On macOS and Linux an installed Chrome or Edge also works; on Windows an installed one is a guarded opt-in (`studio.json` `"browser": "chrome"`, `MOTION_BROWSER=chrome`) because each fresh-profile launch counts as a failed Windows logon |
| Windows account locked, Security log events 4625 from `chrome.exe`, or `refusing to start chrome: N launches ...` | an installed Chrome or Edge was started with a fresh profile (blank-password test = failed logon) | switch to the headless shell as above and unset `MOTION_BROWSER` / `MOTION_CHROME_PATH`; the confirm commands and the reasons are in `${CLAUDE_SKILL_DIR}/../studio-init/references/troubleshooting.md`, "Windows account gets locked out while rendering or testing" |
| `ffmpeg not found` | not on PATH, `ffmpeg-static` missing | `npm i -D ffmpeg-static` or set `FFMPEG_PATH`; `npm run doctor` prints per-OS commands |
| `spawn EINVAL` in your own script on Windows | spawning `npm`/`npx` `.cmd` shims without a shell | use `spawn('npm.cmd', args, { shell: true })`; the tools already do |
| `font missing: 700 64px "X"` or ready timeout | family not bundled or misspelled | `npm run fonts -- add "X:400,700"`; use the names in `studio.json` `brand.fonts` |
| blank or partial frames, page errors in the log | exception inside a scene draw | the driver prints `__studio.error` and console errors; reproduce with `npm run preview` at that time |
| an element is missing only on some frames | a NaN input (draw helpers skip NaN draws) | log the input in preview; usually `t - from` before a scene starts or a division by zero |
| hashes differ in pass B (shuffled) | state carried between frames | move caches and counters into the factory or `setup()` ([determinism](references/determinism.md)) |
| still elements jitter while others move | one RNG stream shared across elements | `rngFor(name, i)` per element, created inside the draw |
| accent color shifted in a player | encode without BT.709 tags | use `tools/render.mjs`; if you re-encode, keep the four `bt709` tags |
| `width not divisible by 2` in custom encodes | odd dimensions | the renderer pads to even; keep scales that give even sizes |
| `film failed to load (<url>): the page threw while booting: ...` or `window.__studio was never created within 15 s` | an exception at import (bad import path, syntax error) or `index.html` never calls `boot(film)` | fix the first `pageerror:` / `console:` line the message lists; a 404 on an import shows up there too |
| `film failed to load ...: __studio.ready rejected: <text>` | `setup()`, the beat grid or `loadFonts` threw (`font missing: <spec>`) | the text names the cause; `__studio.error` carries the stack |
| `note: the browser did not close within N s; killed it` | the installed Chrome's profile cleanup is slow on Windows (measured); the tools bound every browser and context close | harmless, the output is already written; `MOTION_CLOSE_TIMEOUT_MS` (default 8000) changes the wait |
| a frame takes longer than 2 minutes and the render aborts | a scene draw is extremely slow or stuck | reproduce that time in `npm run preview`; `MOTION_FRAME_TIMEOUT_MS` (default 120000) changes the limit |
| `--final renders the whole film; drop --from/--to` | a range combined with `--final` | final renders are always the full film; use a range without `--final` for checks |
| `cannot replace <file>: EBUSY ... The finished render is kept in out/<fmt>/.staging` | a player or viewer holds `silent.mp4`, `poster.png` or `render.json` open (Windows) | close it and copy the files from `.staging/`, or render again; `MOTION_PUBLISH_WAIT_MS` (default 30000) sets how long a held file is waited for |
| `film failed to load ...: __studio.ready rejected: <cause> (__studio.error: ...)` | the boot promise rejected; the cause comes first | fix the named cause; a `the page threw while booting: ...` line means an import or syntax error before `boot()` finished |
| a request for `/.env`, `/.git/config` or an 8.3 short name of one returns 404 | the tools' static server hides every dot-file and dot-directory of the project, also through symlinks, junctions and 8.3 names, and on Windows any request path containing a backslash or `:` | expected; keep film assets out of dot-folders |
| hero type looks soft | the context was scaled to size the text, or DOM `will-change` on a scaled subtree | set the font size instead of scaling; never `will-change` on scaled elements |

For hard cases delegate to the `render-engineer` subagent with the failing command, its stderr and `render.json`.

## 8. Route B handoff

Only when the user names Remotion or HyperFrames. Both need Node 22 or newer; Remotion needs a Company License for
for-profit organizations with more than 3 employees. Follow [references/route-b.md](references/route-b.md) step by
step: pre-flight, install, explicit invocation, preview in the background, render only after the user's OK.

Next: `/motion-studio:springs` to make the motion feel physical, then `/motion-studio:critique-loop` to review the frames.
