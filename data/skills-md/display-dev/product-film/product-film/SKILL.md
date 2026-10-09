---
name: product-film
version: 0.2.0
license: MIT
user-invocable: true
argument-hint: "[<what the film is about> | <film folder to recut>]"
allowed-tools:
  - Bash(ffprobe *)
  - Bash(bash $SKILL_DIR/templates/new-film.sh *)
  - Bash(bash */product-film/templates/new-film.sh *)
  - Bash(bash $SKILL_DIR/scripts/publish.sh *)
  - Bash(bash */product-film/scripts/publish.sh *)
  - Bash(dsp get-metadata *)
  - Bash(dsp comment list *)
description: "Make a short product film (website hero loop, landing section, launch film, feature walkthrough, store-listing promo, social cut, illustrated story film) in which the product appears as its own real UI, drawn frame by frame from an HTML timeline, rendered with Playwright and cut with ffmpeg. Four routes: licensed footage cut against cinematic product beats, product beats only, a pointer-driven walkthrough with captions or text cards (plain or kinetic), or a cut-paper collage in which an illustrated cast tells a story over real UI captured from the code with fictional data. Use when asked for a product film, hero video, promo or demo video, launch film, explainer, walkthrough video, paper or collage film, or to recut one. Not for plain screen recordings or voice-over walkthroughs; laying a supplied music track under a finished cut is in scope."
---

# Product film

Builds short product films, silent unless the user supplies a music track, in which the product is shown as its own real components, drawn frame by frame. Four routes in three registers: cinematic (Routes A and B: a 3D plate and a camera that never stops), plain (Route C: a still plate and a pointer that drives the UI) and illustrated (Route D: a cut-paper cast over real product screenshots, in stop-motion).

- **Route A, with footage.** Licensed live-action cuts of people alternate with product beats. Each product beat follows the human action that motivates it.
- **Route B, pure product.** Product beats only, joined by the plate, with captions or end cards if the surface needs words. For a launch that needs breadth (several capabilities in 25–35 s), the reel style cuts claim-and-proof sections to the music's bar lines on flat brand plates.
- **Route C, walkthrough.** A pointer drives the product through one causal story (select, comment, publish, share). Use it for store-listing promos and feature launch films. The default register is the kinetic style: isolated UI at extreme close-up on white, morphs instead of cuts, kinetic captions, almost no holds. A plain cut with a caption band over one take, or full-screen text cards between shots, is built only when the user asks for it.
- **Route D, paper collage.** An illustrated cast (jointed paper puppets, busts, marker doodles, captions on torn paper strips) tells a story with a problem, a turn and a payoff over real product UI: screenshots rendered by the product's own code on fictional data. Use it for social cuts, pinned posts and explainers where people and product appear together.

| Read | When |
|---|---|
| `references/camera-rig.md` | Routes A and B, before writing a beat: the rig code and the numbers tuned across sixteen cuts. Do not re-derive them. |
| `references/walkthrough.md` | Route C, and any kinetic or reel cut, before anything else: the pointer, flicker, current-UI and true-claims rules, the numbers, the engine, the checks and the pipeline they share. The cinematic defaults (3D rig, glows, particles, grain, drift, tilt, a zoom on every beat) were rejected for these films. |
| `references/kinetic-style.md` | Route C by default, and a Route B film that should feel fast and designed. It changes the look and pacing, not the pointer and flicker rules. |
| `references/reel-style.md` | A launch reel that shows breadth: claim-and-proof sections cut to the music's bar lines on flat brand plates. |
| `references/live-dom.md` | Product UI that must move at close range (typing, hover, menus, state changes): capture the real UI as DOM snapshots on fictional data and mount it live instead of rebuilding it. |
| `references/paper-collage.md` | Route D, before anything else. It replaces the rest of this file for that route. |
| `references/paper-capture.md` | Route D at the capture step, and any route that captures real UI. |
| `references/paper-lessons.md` | Route D, before building scenes and before every review. |
| `references/publish.md` | Before the first review page: publishing on display.dev, one page per film with a version per cut, and the comment loop. |

## When to use

- A new hero, section or launch film is asked for, or an existing one needs a recut, a new beat or a new ending.
- The product has to be shown at fidelity, in motion, without recording the real app.
- A store listing or a launch needs a short demo of a flow.
- A story film with characters is wanted: an illustrated, collage or paper look, or people reacting to the product without footage (Route D).

Not this skill: a plain screen recording of the app used as the film itself, a voice-over walkthrough cut from a screen recording, composing music or voice, or putting a finished file on a website (hand it to the site's video pipeline). Route D does capture the real app, but as stills composed into the collage.

## Project context

Read what the project already has before asking for it. Each item feeds the film; none is required.

| Look for | Use it for |
|---|---|
| `FILM.md` at the project root | The team's film notes: reference builds, looks they rejected, capture setup, house rules. Read it first; it overrides this skill's defaults where they conflict. |
| `DESIGN.md`, `tokens.css`, a Tailwind config, CSS custom properties, a component library | Colors, type, radii, borders and focus rings. Every template keeps its brand values in one custom-property block; replace that block. |
| The shipped UI code and a way to run it (a dev server, Storybook) | The components on screen (see Product fidelity). |
| `PRODUCT.md`, `VOICE.md`, a style guide | Audience, naming, tone and banned terms for captions and on-screen copy. |
| Docs, changelog, pricing page, specs, and the code | The truth sheet: every claim the film makes needs a source. |

When the project has none of these, ask for the brand colors, the font and the one-line story, and state every other assumption.

## Inputs to settle before any rendering

Ask only for what cannot be inferred; state assumptions otherwise.

1. **Reference.** A film the user points at. Fetch it, find the video URL, probe it (`ffprobe`: resolution, fps, length, bitrate, audio track, poster, `preload`). The spec becomes the target; the structure becomes the grammar.
2. **Story in one line and the subject on screen.** Who does what, what the product does in response, who receives the result. The copy on screen: prompt, headline, comments, notification, email.
3. **Route.** A if people footage is wanted and licensable; B if the film is product-only or footage is out of scope; C if the film shows someone using a flow step by step (kinetic, unless the user asks for captions or cards); B in the reel style if a launch should show several capabilities cut to music; D if an illustrated cast should tell a story around the product. For C, also settle the items in `references/walkthrough.md § Settle before building`. For D, settle the brief in `references/paper-collage.md § Settle the brief first`.
4. **Surface and length.** Home hero loop (30 s, silent, poster, `preload="none"`), landing section (20–25 s), social (45–60 s, captions; for Routes A–C the 9:16 reflow is a separate pass, while Route D builds every format at once). A length the user names wins over these defaults.
5. **Third-party products in the UI** (an AI assistant, a mail client, a chat app): name them in text; do not show their logos unless the user has the right to.

## Start a film

```sh
bash <skill>/templates/new-film.sh <cinematic|walkthrough|paper> <film folder>
```

`cinematic` serves Routes A and B, `walkthrough` serves Route C (kinetic by default) and the reel style, `paper` serves Route D. The script copies the route's template and the shared helpers into the folder, installs Playwright there once if it does not resolve, and runs the route's setup. It never overwrites an existing file.

Put the film folder outside the repository and outside any temporary or scratch directory: a film takes several sessions, and temporary folders get pruned. The script refuses temporary paths. Keep `NOTES.md` in the folder current: the current cut, the pipeline, what the user rejected and why.

## The engine

Every product beat is an HTML page that exposes `window.seek(t)` and draws frame `t` deterministically, from scratch, with no dependence on earlier frames. A renderer opens it headless with Playwright at device scale factor 2, calls `seek` for each frame, screenshots to JPEG, and ffmpeg encodes. An assembly script cuts footage segments (Route A) and concatenates everything into a master, a 1080p web file, a 720p review file, a poster and a contact sheet.

| Route | Template | Engine |
|---|---|---|
| A, B | `templates/cinematic/` | `beats.html` (one `<div class="beat">` per beat, real product markup and CSS inside, 3D world and camera, particles, `seek(t)`, lengths in `window.BEATS`), `render.js` (frames → `seg/<beat>.mp4`; `ONLY=b2` renders one beat, `ONLY=b2 FRAMES=40:60` a few frames for a look), `assemble.sh` (cut list → `film_master.mp4`, `film.mp4`, `film_720.mp4`, `poster.jpg`, `sheet.jpg`) |
| C, plain | `templates/walkthrough/` | `beats.html` (2D engine with holds, clip plans, captions and cards for the on-request cuts; plans `plan-A.json` and `plan-B.json`), plan-driven `render.js` and `assemble.sh` at 60 fps with dissolves, `plan-jobs.py` (parallel workers), `previewq.js` (single frames), `audit.js` (pointer rests, one-frame jumps, stateful seeks) |
| C, kinetic (default) | `templates/walkthrough/` | `kinetic.html` with `plan-K.json` (16:9) and `plan-Ksq.json` (square) on the same render, audit and assemble pipeline |
| B, reel | `templates/walkthrough/` | `reel.html` with `plan-R.json` on the same pipeline; `beatmap.py` finds a track's tempo and bar lines |
| D | `templates/paper/` | One canvas per frame from `timeline.json`, a frozen paper kit, capture harnesses for the real UI (the app, its CLI, an agent window), sound synthesis, review, gate and delivery tools; see `references/paper-collage.md` |

Every film folder also gets the shared helpers from `templates/common/`: `pw.cjs` (loads Playwright), `capture/lib.mjs` (boxes from the live DOM, fixture routing, in-flight states, `snapshot()` for live DOM) and `tools/make-chart-bg.mjs` (renders the engraved chart background in the brand colors into `backgrounds/`).

Copy the templates (new-film.sh does); do not start from a blank file. Each template's example product is the fictional Tidewell; replace its brand block, components and copy with the product's.

## Product fidelity

The UI on screen must be the product's own components, not a mock-up.

- Take markup and CSS from the product's shipped components and reuse them with new copy. The template's example components show the structure; replace them with the product's.
- For any surface the film zooms into and animates, prefer captured DOM from the running code (`references/live-dom.md`) to a hand-built copy: it is pixel-identical and stays true to recent UI changes.
- Colors, radii, borders and focus rings come from the product's tokens and shipped CSS. At 2× zoom a mismatched border reads as a defect.
- Emails, notifications and messages on screen follow the product's real templates: subject format, headline phrasing, link color.
- Before mirroring any UI, check for recent redesigns (`git log --since="1 month ago" -- <ui paths>`). Stale UI costs a full review round.
- Fonts: Routes A–C load web fonts at render time, and the renderer waits for `document.fonts.ready`. Route D uses local font files only (`tools/fetch-fonts.mjs`).
- Data on screen is fictional and looks real at a glance: fictional people, companies and emails (`@example.com`), never real customers.

When a component is not available in code, rebuild it from the product's tokens and shipped CSS, and say so on the review page.

## Procedure (Routes A–C)

Route D follows its own gated procedure in `references/paper-collage.md § Procedure`.

1. **Reference and concept.** Probe the reference. Write a one-page concept: what the film is not, who the protagonist is, the beat sheet, the register of the humans (Route A). Share it for review.
2. **Storyboard.** Route A: search the footage library (many stock sites block headless browsers; use a headed, persistent browser profile), sample frames, build the storyboard from real frames, all shots from one shoot, every shot 0.5–2 s. Routes B and C: the storyboard is the beat list with the copy per beat.
3. **Sources.** Route A: the user buys the license and downloads the files (download flows usually defeat automation); sources go in `footage/`. Routes B and C: nothing to fetch.
4. **Beats.** Start the film folder (§ Start a film); replace the example beats with the product's; build one beat at a time and check it with a contact sheet (`ffmpeg -vf "fps=2.5,scale=480:-1,tile=4x2" -frames:v 1`) before rendering the next. Route C: build the kinetic cut; build a captions or cards cut only when the user asks. Reel: set the tempo and section bars first (`beatmap.py` on the track), then build the sections on that grid.
5. **Render** with the template's `render.js`.
6. **Assemble** with `assemble.sh`: cut list with in-points, durations and per-cut comments; build; look at the whole-film contact sheet at 1 fps. Route C: run the checks in `references/walkthrough.md § Check before every publish`, `audit.js` first.
7. **Review page.** One HTML page with the 720p cut and the poster embedded as base64 and "What changed since cut vN" on top, published on display.dev (`references/publish.md`). Republish each cut as a new version of the same page (`--id`, `--base-version`); never a new page per cut. Send the MP4 as a file too. Post frames, not prose, when asking for a decision.
8. **Loop on feedback.** Read the open comment threads on the review page, act on each note in one new version, reply in each thread with what changed, resolve it, and record durable taste notes in the project's `FILM.md`.
9. **Ship.** Hand the 1080p web file and the poster (the same frame as the film's own poster) to the site's video pipeline.

## Review discipline

- One review page, many versions, the change log on top of each.
- Before sending any cut, look at four frames of every changed beat at full size: its start, middle, end and the frame after the last change. Clipping at the frame edge and blurred children are the two recurring defects.
- Every walkthrough-pipeline cut (plain, kinetic, reel): `audit.js` reports no problems before it is sent. Stuck pointers and one-frame flickers are hard to see in stills and easy for the viewer to see.
- Watch the 720p file once at real speed before sending. Pacing notes come only from watching.
- An agent cannot hear. When a cut has sound, measure it and say that it needs the user's ears.

## Gotchas already paid for

- A CSS `filter` on a parent blurs its children; sharp objects must be siblings of blurred panels.
- `zoompan` at 1080p jitters on slow pushes; compute it on a 7680-wide upscale.
- The concat list's paths resolve relative to the list file.
- zsh mangles `$var:flags` and aborts a chain on an unmatched glob; assembly scripts are bash.
- A phone-portrait UI in 16:9 is a floating device on the plate with the camera pushing into its screen.
- An email beat is the mobile mail app if the previous shot is a phone.

## What this skill does not do

- Choose the shoot, write the shot outline, buy a license, or make taste calls. Present candidates and frames; the user decides.
- Screen-record the real application as the film. Route D captures stills from the real code on fictional data and composes them.
- Compose music or record voice. Laying a track the user supplies under a finished cut is in scope: `references/kinetic-style.md § Music`.
- Publish anything except the review page on display.dev, and that only when the user asks.
