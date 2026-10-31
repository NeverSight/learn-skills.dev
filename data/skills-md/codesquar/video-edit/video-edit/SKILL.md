---
name: video-edit
description: Make, edit, animate or render a video as HTML compositions rendered frame by frame with the HyperFrames CLI (npx hyperframes), such as launch/promo films, explainers, data/chart pieces, vertical social clips, title cards, kinetic type, captions and cards over footage. Holds the render contract, the work loop (story → spec → build → check → review → render) and the motion/look taste that keeps the result from looking generated. Not for AI-generated footage.
---

# Video Edit

A video is HTML + CSS + one paused GSAP timeline. The HyperFrames CLI seeks that timeline frame by frame and encodes it, so every render is identical. Run it as `npx hyperframes <cmd>` (Node 22+, FFmpeg; `npx hyperframes doctor` if Chrome is missing). Failures print a `Fix:` line. Don't read `--help` or `npx hyperframes docs` unless a command fails: the commands here are enough. From command output take only the result and `Fix:` lines; ignore init's "Get started", update notices, skill suggestions and `Report:` JSON paths.

Bundled scripts do the mechanical work; use them instead of writing your own loops (`<skill>` = this skill's base directory, shown when it loads; run them from the film folder with `python`):

| Script | Does, in one call |
| --- | --- |
| `<skill>/scripts/voice.py voice.txt` | every voiceover take in parallel → wav, trimmed, one tempo, transcribed in one pass → `assets/voice/timings.json`, scene starts and the `const VO = {…};` line for cues (`references/voice-off.md`). A target length: `--tempo fit:45` on the first run. Once `index.html` has the VO line, every rerun (`--only s3`, new `--tempo`) also re-times the film itself (`retime.py`) |
| `<skill>/scripts/images.py search` / `get` / `cut` / `sheet DIR` | image search as one line per hit, parallel download that rejects HTML pages, crop → webp; `sheet` = a local folder as labelled contact sheets to Read in one message |
| `<skill>/scripts/fonts.py "Family:700" "Family:italic:500"` | Google Fonts → `assets/fonts/*.woff2` + the `@font-face` lines to paste |
| `<skill>/scripts/check.py` | `check` showing only what needs a decision (Work loop 5) |

Independent steps go in the same message: the voice takes, the image search and the fonts don't wait on each other.

Defaults: 1920×1080, 30 fps. Build only what was asked: no voiceover, captions or new aspect ratio unless requested (images and sound effects are the exception, see Project). A question or a loose idea gets an answer or a proposal, not an edit.

## Project

Everything lives under one `video/` folder at the repo root:

```
video/
  motion.md, design.md    shared style for every film
  refs/                   references, extracted frames, capture output
  components/*.html       pieces reused across films (character, product, logo)
  films/<name>/           one HyperFrames project per film:
    index.html            the whole film, written in one pass: variables, scenes, one timeline
    compositions/*.html   copies of the components this film uses (render reads only inside the project)
    assets/               media, fonts (assets/fonts/*.woff2), sfx (assets/sfx/), root-relative paths
    SPEC.md               your brief
    renders/              every render output (mp4), never elsewhere
```

Preview and render use these same files: write in this format from the start, view with `npx hyperframes preview`. Never write your own player or a separate preview HTML.

Other films are off-limits: never list, open, snapshot, play or copy anything in another `video/films/<name>/` (HTML, SPEC, assets, renders) as a reference — they bias the new film toward an old one. What films share comes only from `motion.md`, `design.md` and `components/`; anything else (content logs, notes, `refs/`) is fine to read. Only open a film when it is the one you are editing.

New project: `HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init video/films/<name> && cd video/films/<name> && rm -f CLAUDE.md AGENTS.md && mkdir -p assets/img assets/sfx assets/fonts assets/voice renders` (the env var stops init installing the upstream skills; the `rm` drops the files that point to them). Init's `index.html` is a 1920×1080 placeholder: don't read it, overwrite it with your first pass. A website as the subject: `npx hyperframes capture <url> --json` (screenshots, copy, logos, `extracted/tokens.json`), output into `video/refs/`. Code shapes, attributes and lint fixes: `references/format.md`.

Images and b-roll: always use them without asking, unless the person or the project says otherwise. Source: a folder the person names (`python <skill>/scripts/images.py sheet <folder>`, then Read the sheets it prints in one message); otherwise:
1. `python <skill>/scripts/images.py search "q1" "q2" "q3"`: every query of the film in one call (`pip install ddgs pillow` if missing). Pick from the listed size, title and page.
2. `python <skill>/scripts/images.py get "$TEMP/img-<name>" URL a.jpg URL b.jpg …`: all picks at once, 2–3 candidates per slot, since some fail. A page URL works too (it takes the page's `og:image`).
3. Look only at the ones that landed (Read them in one message): no watermarks, edited variants or low resolution.
4. `python <skill>/scripts/images.py cut SRC assets/img/x.webp --box x0,y0,x1,y1 --w 1600` for each one you use (crop in source px; omit `--box` to keep the frame). Only those go into `assets/img/`.

Fonts the design names that HyperFrames doesn't bundle (`references/format.md`, Fonts): `python <skill>/scripts/fonts.py "Archivo:700" "Newsreader:italic:500"` in the film folder, then paste the `@font-face` lines it prints. How many, how long and how they enter is not fixed: infer it from the film's style and `video/motion.md` / `video/design.md`.

Sound effects: every film has them, music or not, unless the person says no. Take them only from this skill's `assets/sfx/<name>.mp3` (not from other skills). The table is the whole library, durations included, so no `manifest.json` read and no `ffprobe`:

| Name (s) | Use |
| --- | --- |
| `click` 0.37, `key-press` 0.40 | UI tap/toggle; one keystroke |
| `pop` 0.72 | element/chip/badge appears |
| `whoosh` 0.57 | fast move, swipe, snappy transition |
| `typing` 1.50 | text being typed; start as it begins |
| `ping` 1.32, `sparkle` 1.80 | key reveal or data point; shine on a hero |
| `chime` 2.50, `notification` 2.46 | success/confirmation; toast or message in |
| `error` 1.62 | failure, a "wrong" beat |
| `glitch-1` 2.64, `glitch-2` 3.50, `glitch-3` 3.10 | hard-cut hit; harsh chaotic reveal; subtle texture under other audio |
| `impact-bass-1` 2.12 | logo/headline slam on the landing |
| `impact-bass-2` 2.59, `whoosh-cinematic` 5.54, `riser` 10.03 | builds: peak at the end |

Copy only the ones you use into the film's `assets/sfx/`. Each effect syncs exactly to its on-screen action. Short accents (click, key-press, pop, whoosh) sit on the action's frame. Hits (impact, glitch) trigger on the landing and their decay bleeds into the next shot (J-cut). Builds are placed so the peak lands on the reveal or cut: start = peak − duration (riser: payoff − 10.03 s). One file per distinct effect, reused for every cue that needs it. One `<audio>` per cue, all in one `sfx` group: `<audio id="sfx-pop-1" class="clip" src="assets/sfx/pop.mp3" data-start="2.43" data-volume="0.35" data-audio-group="sfx"></audio>`. Volume ≈ 0.35, under narration and music. No file fits a cue: skip it, never generate one.

## Contract (`check` enforces most of it)

1. Timed elements: `class="clip"`, `id`, `data-start`, `data-duration` (seconds), visible over `[start, start+duration)` — land the end state *before* the end.
2. Video length = root `data-duration`. Overrun is cut; an early end holds the last frame.
3. One `gsap.timeline({ paused: true })` per file (`index.html`, plus each reused piece), registered **last**: `window.__timelines["<composition-id>"] = tl`. A piece's host id = its root id = timeline key. Never `play()`, never nest a piece's timeline in the root's.
4. Deterministic: no `Date.now()`, unseeded `Math.random()` (use a seeded PRNG), fetches, timers, rAF, or `repeat: -1`. Everything visible is a function of timeline time.
5. Never tween `display`/`visibility`/`autoAlpha` on a `.clip` — animate a child. No CSS `transform` on something GSAP transforms; use `fromTo`, not `from`. Animate transforms, not `left/top/width/height`.
6. Never play/pause/seek media. `<video>` is `muted` or `data-has-audio="true"`; every `<audio>` has an `id`; no `crossorigin`.
7. Paint order is `z-index`, not `data-track-index`.
8. Grades/grain/blur on footage: `npx hyperframes media-treatment`, not CSS filters.
9. Copy, colours and swappable media are variables (`data-var-text`, `data-var-src`, `var(--id)`), so the video can be re-branded without code.
10. Content in the 90% action-safe box; text and captions in the 80% title-safe box. Vertical 9:16 (1080×1920) for Reels/TikTok instead: words, faces, product and CTA inside x 65–940, y 270–1250 px (top 270 px: platform header/tabs; bottom 670 px: caption, username, CTA; right 140 px: like/share rail); outside it only footage, background and texture. The rest of vertical craft: `references/craft.md` (Vertical).

## Work loop

1. **Editing an existing film?** `npx hyperframes timeline --json` in that film shows what plays when (only here, never for a new film). Build on what is there.
2. **Story** (anything over ~30 s that tells something): write **three storylines** in words only — each a different world, device and form (`references/craft.md` §Story). Recommend one first. If the person is there, stop until they pick; if they said "no stops", build your pick.
3. **Spec** (new films over ~30 s; skip for edits and short pieces): write `SPEC.md` — every adjective turned into a number (template below). Build from it, check against it.
4. **Build**: write the whole first pass in `index.html`, then fix with `check` (it runs lint; no separate `lint`). Don't plan every coordinate up front. With a voiceover, scene starts and durations come straight from voice.py's table (`start`, `dur`, `vo`): copy them, don't recompute or parse `timings.json`. Paste its `const VO = {…};` line at the top of the script and write every voice-driven tween position as `VO.s2 + 1.46` (the word's time from the table), never as an absolute number, so a new take moves its cues on its own. Full-frame overlays (flash, wipe) start at `opacity: 0` in CSS, or `check` fails them. Repeated elements are a JS function or CSS class in the same file, not new files.
5. **Check**: `python <skill>/scripts/check.py` in the film folder. It runs `npx hyperframes check` and prints every error in full, each warning kind once with up to 3 places, and only counts for infos and for the warnings one-file films raise on purpose (`nested_structure_needs_subcomposition`, `composition_file_too_large`, `timeline_track_too_dense`). Don't re-run `check` raw or re-filter it. `FAILED` = non-zero exit. Fix every error, weigh every warning (`line_unread`, `dead_stretch`, `text_below_floor`, `first_frame_empty`, `film_silent`). After fixes, re-check and re-snapshot in the same command: `python <skill>/scripts/check.py && npx hyperframes snapshot --at … | tail -1`.
6. **Look** (new films only; skip for small edits or if the person says no review): `npx hyperframes snapshot --review 2>&1 | grep -i sheet` (scene starts/mids, every cut ±0.2 s, phone width) prints the paths of the contact sheets `review-beats-N.jpg` and `review-phone-N.jpg` (N = 1, 2… for long films; there is also a `review-seam-NN.jpg` per cut). Read all the beat and phone sheets in one message: that is how you see the video; open a seam sheet or a single PNG only to inspect a seam or detail. For one move: `snapshot --range A,B --frames 8`, `--at t1,t2` (`| tail -1` gives its `contact-sheet.jpg`), `keyframes --json --selector '#id'`. Then run the **Review** below.
7. **Preview**: `npx hyperframes preview --background`; give the URL and wait for approval, unless they asked for the file.
8. **Render** and measure in one command, always into the project's `renders/` (`--quality draft` while iterating):
   ```bash
   HYPERFRAMES_NO_UPDATE_CHECK=1 npx hyperframes render --quality delivery --output renders/<name>.mp4 2>&1 | tail -3
   ffprobe -v error -show_entries format=duration -of csv=p=0 renders/<name>.mp4
   ffmpeg -hide_banner -i renders/<name>.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
   ```
   Duration must equal root `data-duration`; loudness −14 to −16 LUFS, peak ≤ −1 dBTP (else `npx hyperframes normalize-audio`). The render draws the frames `snapshot` already showed, so don't re-inspect frames unless the render printed a warning. You can measure the sound, not hear it: say so.

Timeline edits without hand-editing: `npx hyperframes timeline move|trim|split|set|duplicate|delete <#ref> … --plan --json`, then without `--plan`.

## SPEC.md

Adjectives are where the default look hides. Every one you turn into a number is a decision taken back.

```
GOAL:    what the viewer feels or does at the end, one sentence
OUTPUT:  W x H, fps
TIME:    seconds x fps = frames; BPM and frames-per-beat if music
LOOK:    ground (hex + texture %), ink, ONE accent and where it may appear;
         display face + weight + px + tracking; body face the same;
         the medium (paper+ink, photographs, product UI, glass, clay, 3D) with numbers;
         shadow offset/blur/opacity, grain %, vignette %
OBJECTS: each thing the viewer must recognise, with the material/details that make it read
MOTION:  eases by role (enter, move, exit, camera); springs as damping; durations in frames
SHOTS:   per shot: frame range, the ONE hero move, what is read (and for how long),
         the sound, how it hands off to the next shot
BANNED:  the defaults below + anything this film must not become
QA:      frames to check and what each must show
```

| Word | Becomes |
| --- | --- |
| premium | a material with numbers: satin paper 2% grain, product on a seamless sweep with 0.55 contact shadow |
| modern | a camera + type system: 30-frame push on one ease, display at 9% frame height, −2% tracking |
| clean | a grid + a ration: 12 cols, 96 px margins, accent on one word per shot |
| dynamic | cuts on the beat, layout change every bar, one hero move per shot |
| playful | springs at damping 0.45–0.6 on position/scale (never opacity/colour), 10–30% exaggeration |
| cinematic | 35 mm framing, key upper-left, rim from behind, 6% vignette |

**Look source, in order:** the project's `DESIGN.md`/`frame.md` (hex and fonts verbatim) → the real brand (`capture`) → a reference the person gave (take its grammar, not its content) → the subject's own world. A look holds when it is the rules of one **medium** (e.g. risograph: flat paper + fibre noise, ink A for all text, one fluorescent ink B, 3 px misregistration, halftone instead of gradients) — and motion comes from that medium too (printed, cut, pressed, refracted), not from fades.

## Taste: the rules that matter most

**Composition**
- The hero fills ≥40% of the frame's height or width. A small thing in an empty middle is never a shot — push in, crop, or give it a world.
- One hero move per shot. Secondary moves travel 50–70% as far and start 100–200 ms later; the rest holds still.
- Something new every 2–4 s. Readable text ≥28 px at 1080 (2.6% of the short side), held 0.5 s + 0.3 s per word; the last line ≥2 s. Too many words: cut words, never shrink type.
- Titles: ≤6 words a line, one line at a time, 4–9% of frame height, one accent word that carries meaning. A landed title is **dead still**.

**Motion**
- Ease by role: arrivals on a long tail (`expo.out`, `power4.out`); camera moves and colour floods both ways (`power2.inOut`); exits and zoom-throughs accelerate (`power3.in`). The same `power2.out` 0.5 s on everything is the "generated" look. Linear only for rotation/progress.
- Arrive slow, leave clean: exits 40–50% shorter than entrances, one motion, never slide-stop-leave. Fast moves 0.3–0.6 s with motion blur.
- Overlap: next element starts when the previous is 30–50% done. Stagger: letters 1 frame, words 60–120 ms, list items 40–80 ms.
- **Vector law at cuts:** the exit decides the entry — same axis, same direction (on Z: same sign of scale change), matched speed via mirrored eases (`power4.in` out → `power4.out` in), cut mid-motion on both sides. Pick one dominant direction for the film; spend other directions only with a visible cause.
- Every cut has a cause on screen: the clicked thing becomes the next shot. 3–5 transition kinds per film, ≤⅓ hard cuts between beats, worlds never crossfade. Catalog: `references/craft.md` §Transitions.
- Pause 0.3–0.75 s before the payoff; the payoff plays at normal speed.
- Pause the film at any second: something meaningful is mid-flight (a reveal landing, the camera travelling, the UI acting) — never idle wobble.

**Story** (any film that tells something)
- One thing to remember, one viewer doing one real task, one real piece of data travelling from hook to payoff.
- Frame 0 is the thumbnail: never black, never a logo alone. The first 2 s are the densest.
- Real UI and real numbers from the source, never a mockup or an invented stat; a missing screen is a labelled placeholder.
- The brand mark lands once, with weight, on a built end card — never docked in a corner.
- Copy bans: "Introducing" as the first line, "unlock", "seamless", "supercharge", "game-changer", "revolutionize", "effortless", unmeasured "in seconds".

**Sound:** every film gets exact effects on visible actions (see Project); a film over ~15 s also gets a music bed. Mix ≈ −14 to −16 LUFS, peaks ≤ −1 dBTP (`npx hyperframes normalize-audio`). No music source → deliver with effects only and say so.

## BANNED by default

Allowed only when the brand or the person's reference uses it, and only as they do:

- dark/navy void ground with small elements floating in the middle;
- glow, bloom, neon, lens flares, orbs, rings, decorative particles;
- purple/blue gradients, mesh gradients, glass cards;
- cream paper + serif display + italic accent word + "01 / 02" labels + mono caps labels + pill chips;
- everything centred; everything fading in at once; every element fading and sliding up;
- text that moves while read; titles drifting or scaling after they land; breathing/floating/pulsing loops on titles or UI; bounce on UI; click rings;
- corner labels, frame borders, corner brackets, HUD readouts as decoration;
- three cards in a row, KPI grids, a title over a dimmed screenshot, bullet slides, icons in circles;
- typing into a prompt box as the opener; the logo docked in a corner;
- Inter / Space Grotesk / Instrument Serif / Geist / JetBrains Mono as the *default* choice (fine when the brand uses them).

After each render, name every default it used anyway (listed or not), add it to `SPEC.md` BANNED (when there is one) and fix it. The list grows per film.

## Review (after `check` passes, before replying or rendering)

Be a harsh motion director, not a proud author.
1. Describe each beat frame in one sentence as a stranger would, naming every object. An object you'd have to explain is a P0.
2. Read the beat frames in order: does each cause the next? With the words covered, do the pictures still tell it? Compare each with its SHOT line.
3. Check: subject/ground separation, one focal point, crops and edge text, collisions at seams, reads shorter than their words, pops with no move, jumps at cuts, everything on one curve, the BANNED list, legibility at 360 px.
4. Notes as `t=4.2s · where · problem → exact change · what stays`. **P0** breaks the read/contract, **P1** weakens it, **P2** polish. Fix all P0, worthwhile P1 — text, then timing, then detail. Re-snapshot only what changed. Never score out of 10. Busy film: remove a third of the motion.
5. In your reply, a short delivery note: creative calls made, storylines not built, what was measured vs only looked at, the weakest shot, warnings kept on purpose. `REVIEW.md` only if asked.

## Read when needed

| Need | Read |
| --- | --- |
| Writing HTML: skeleton, attributes, variables, fonts, media, lint fixes, other runtimes (canvas/Three/Lottie) | `references/format.md` |
| Storylines, beats per film type, transitions catalog, captions, cards over footage, music timing, data/explainer/vertical/launch specifics | `references/craft.md` |
| Voiceover: script, generating takes (OpenRouter TTS), timing scenes to the voice | `references/voice-off.md` |
| `video/motion.md` (how the project's videos move) or `video/design.md` (how each frame looks) is missing, or the person asks to rewrite/change it. Otherwise just read the existing files and follow them | `references/video-motion.md` / `references/video-design.md` |
