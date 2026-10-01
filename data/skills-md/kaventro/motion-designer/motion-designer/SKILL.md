---
name: motion-designer
description: Make a launch film for an app, mobile (inside an iPhone) or desktop (a window on a laptop's desktop, with a real pointer; web apps in a browser window), with its real UI rebuilt or captured in HTML, or a story told in panels with the brand's character and an end card. The film is cut on the beat to an original track made for it (or the user's), in a chosen visual style, with an optional voiceover in a local voice the user picks (Chatterbox or Kokoro), checked frame by frame and rendered to MP4, a muted loop, a poster and a single self-contained HTML. It also makes or cuts a track to the bar and the frame, writes and mixes a voiceover, and checks and installs the tools it needs after asking. Use when the user wants a launch video, promo, teaser or product film of their iOS, Android, macOS, Windows, Linux, Electron, Tauri or web app, wants to change such a film's story, style, pacing, device, music or voiceover, wants music made or a track cut to a film's beat or narration mixed over it, or asks what the tool needs to run.
argument-hint: "[app project dir] [mobile | desktop] [square | vertical | landscape] [length, e.g. 45s]"
---

# motion-designer: launch films

You direct and build a short film of an app in use. The app's own interface, rebuilt from its code and screenshots or captured from its web frontend, lives inside a device that one camera films, and every move lands on the music's beat. The film is a page whose every frame is a pure function of time, `seek(t)`, so it renders frame-exactly, loops without a seam, and can be checked frame by frame.

- **Mobile**: an iPhone (`templates/mobile`). **Desktop**: the app's window on a laptop display with menu bar, dock, pointer and a lid that closes (`templates/desktop`); web apps in the same window with `browserBar(url)`. **Story**: a hook, the product's arrival, features as panels (a headline with an accent word beside the app's real interface as cards), the brand's character, and an end card with a call to action (`templates/story`, [types](reference/types.md)).
- Everything is in this skill's folder, `${CLAUDE_SKILL_DIR}`: `scripts/`, `templates/` and `reference/`. The reference files spell that folder as the variable CLAUDE_SKILL_DIR in `${…}`; read it as ${CLAUDE_SKILL_DIR}.
- One skill, four parts. The film is this file. When a film needs them, or the user asks for one on its own, read the part: [music](reference/music.md) (the sound brief; an original track made for the film, heard before it is used, or the user's; tempo, bars and drops; a cut exact to the bar and the frame; sounds for the actions), [voiceover](reference/voiceover.md) (lines on the timeline, Chatterbox or Kokoro, the mix) and [setup](reference/setup.md) (what the tools need, installed only after the user agrees).
- **First**, run `bash ${CLAUDE_SKILL_DIR}/scripts/doctor.sh`. If it reports something missing, follow [setup](reference/setup.md): say what is missing and why, ask before installing anything, then install with `scripts/install.sh`.

## Deliverables

In a film folder in the project (default `docs/launch-film/`, or `tmp/launch-film/` when it must stay out of git):

| Path | What |
|---|---|
| `brief.md` | the approved brief (see step 0) |
| `src/` | the film: `index.html`, `film.css`, `core.js`, `device.js`, `scenes.js`, `main.js`, `assets.js` |
| `out/<name>.mp4` | the render with music (`out/` stays out of git) |
| `out/<name>-loop.mp4`, `out/<name>-poster.png` | a muted loop for autoplay, and the hero frame |
| `out/<name>-voiceover.mp4` | if asked: the same picture with the voiceover mix, plus `.srt` captions |
| `dist/<name>.html` | one self-contained file (fonts, images, music inlined) |
| `out/<name>-post.txt` | two or three sentences to post with the film: what the app does and for whom, in the app's own words, with the link |
| `README.md` | the beat map with times, the style, how to preview, check, render and rebuild, sources and rights |

## Workflow

Stop for the user's go-ahead after step 0 and again after step 2 unless they asked you to go straight through; after that, work without asking except where [rights](reference/rights.md) says to.

0. **Brief, in plan mode.** Switch to plan mode (`EnterPlanMode`) unless the user asked to go straight to building or gave you a complete brief. Find the product's name (from the user, the app's manifest, the README or the folder; ask if they disagree or nothing is certain), read what the product does and which flows are worth filming, then write a brief for this product alone and present it with `ExitPlanMode` ([brief](reference/brief.md)). Pick the film's type there ([types](reference/types.md)).
1. **Materials.** Find what you can: the app's code (screens, tokens, fonts, icons, copy), a Simulator or desktop build, brand assets, current screenshots or recordings. Ask only for what you can't find: the music (the user's own track; without one, make an original with [music](reference/music.md#make-one) or, with their go-ahead, search licensed libraries in [music sources](reference/music-sources.md)), format and length, the features that must appear, claims to avoid. Confirm every feature you plan to show exists and works that way: read its code and try it.
2. **Concept.** Offer two or three [styles](reference/styles.md) that suit the app. Write the story in beats (one visual change per beat, a hold after each result, the biggest reveal on the drop), a beat-map table (beat, time, what happens), the screens and assets needed, and four stills rendered from the template in the chosen style: the opening, the key product moment, the drop, the final frame. List your assumptions. For a social cut (15–25 s) the first two seconds already show the app's strongest action, and the wordmark can wait for the end. If they asked for an App Store app preview, explain guideline 2.3.4 first ([rights](reference/rights.md)).
3. **Build.**
   - `bash ${CLAUDE_SKILL_DIR}/scripts/new_film.sh <film-dir> mobile|desktop|story`; open `src/index.html` in Chrome to preview and scrub.
   - Set the clock on the first line of `scenes.js`: `film({ BPM, BEATS, holds })`.
   - Pack the app's look: `swift ${CLAUDE_SKILL_DIR}/scripts/symbols.swift <film-dir>/assets/sym plus@semibold …` for SF Symbols, then `python3 ${CLAUDE_SKILL_DIR}/scripts/assets.py <film-dir>/src/assets.js --font "Family=font.ttf" --img icon=AppIcon.png --sym <film-dir>/assets/sym`. The app's family goes first in `film.css`, the style's tokens in its `:root`.
   - Rebuild each screen in `scenes.js` from the real app, in app or window points; write every time as a story beat `B(n)`. For web-tech desktop apps, capture the real UI instead ([capture](reference/capture.md)). Read [motion](reference/motion.md) and [phone](reference/phone.md) or [desktop](reference/desktop.md) first.
4. **Sound** ([music](reference/music.md)): follow the sound brief from the plan. Make the track if there is none (plan the takes, hear them, render the ones that fit), listen to it with `beats.py` and its sheet, pick bars so its lifts and breaks land on the film's, cut it to `<film-dir>/audio/edit.m4a`, put its `BPM` and `BEATS` in `film({...})`. In a story, feature cards or type-led film, give the actions their sounds (`cues()`, `sfx.py`) and render with the mix.
5. **QA loop** ([qa](reference/qa.md)), the part that makes it good:
   - `node ${CLAUDE_SKILL_DIR}/scripts/check.mjs <film-dir>/src/index.html`: no clocks, timers, randomness or CSS animation in the code, no page errors, the loop closes (the frame after the last is the first), frames identical in any seek order.
   - Contact sheets of an overview every 0.5 s, every transition at 0.05 s and every text screen at full size: `node ${CLAUDE_SKILL_DIR}/scripts/render.mjs sheet <page> <out.png> <from> <to> <step>`. Look at each one; fix what the failure catalogue names; repeat until a pass finds nothing.
6. **Render.** `node ${CLAUDE_SKILL_DIR}/scripts/render.mjs video <page> <film-dir>/out/<name>.mp4 --audio <film-dir>/audio/edit.m4a --scale 2` (about 0.4 s a frame, so run it in the background), then the loop, poster and any smaller copy ([qa](reference/qa.md), "Deliverables"). Verify frames, size and duration with `ffprobe` and compare a frame with a still of the same time.
7. **Voiceover**, if asked ([voiceover](reference/voiceover.md)): let the user pick the voice engine, then mux the mix over the rendered picture.
8. **Single file.** `python3 ${CLAUDE_SKILL_DIR}/scripts/build_single.py <film-dir>/src/index.html <film-dir>/dist/<name>.html`, then `check.mjs <page> --dist <film-dir>/dist/<name>.html` proves it shows the same pixels.
9. **Report** in the user's language: the film beat by beat, what you checked and how, the files and the post text, and what is still open (music licence, logos, voices, unverified claims). Send the video.

## Hard rules

- **Deterministic.** Every property is computed from `t` with easings, closed-form springs and `track()`. No CSS transitions or animations, timers, `Math.random`, `Date`, or state carried between frames. Spinners, waveforms, carets and typing are functions of `t`.
- **The device is always there.** Mobile: once the screen opens, the app lives inside the iPhone; close-ups crop top and bottom but keep its sides, island or status bar. Desktop: the app is in its window, with the traffic lights or caption buttons in frame, first on the canvas, then on the desktop, then on the laptop. Never app UI full-bleed.
- **Real features, fictional data.** Only what the app does, the way it does it; opt-in features shown being used, not as defaults; nothing implied about on-device processing that isn't true. Every name, amount, file and person is invented.
- **Readable on a phone.** Each result holds 1–2 s before the next action. Text that matters is at least ~20 px on the stage: move the camera in rather than shrinking the film. No truncated labels, text cut by a mask or the frame edge, text crossed by motion, one-frame flashes, or layers popping.
- **Motion from the app itself.** Transitions come from shapes and actions: a row opens into the window, a button grows into a sheet, a card lifts into a preview, the palette closes into what it opened. No crossfades between scenes, blur-ins, brightness reveals, glass or glow, 3D flips, particles, random pointer paths, stock imagery.
- **Local only.** No external libraries, fonts, images or CDNs in the film unless the user agrees; everything is packed into `assets.js` and inlined in the single file.
- **Never overwrite the user's source assets or app code**; derived files go in the film folder.

## What viewers asked for

- To see it is a phone, or a desktop app, at every moment.
- Slow enough to follow: one action per beat, a hold after each result, the camera easing in during holds.
- Nothing that looks broken: a label reading "Savi" or "Uncategori…" gets reframed or scrolled until it fits; badges are sized from DOM-measured text.
- A voice clearly on top of the music, with the music still present between lines.

## References

- [brief](reference/brief.md): the plan-mode brief: the product's name, what to read, the shape, what makes it this product's ([example](reference/brief-example.md))
- [types](reference/types.md): product film, story, feature cards, type-led, sting: when each fits and how it is built
- [styles](reference/styles.md): seven looks with tokens, motion and a signature move each; how to choose
- [motion](reference/motion.md): the engine, the grid, vocabulary, timing, transitions that worked, traps
- [phone](reference/phone.md): the iPhone, building screens, the camera, the Home Screen, endings
- [desktop](reference/desktop.md): the window, laptop and desktop, camera, pointer, keyboard, platforms
- [capture](reference/capture.md): filming the real frontend of Tauri, Electron and web apps
- [qa](reference/qa.md): checks, review routine, failure catalogue, deliverables, render verification
- [rights](reference/rights.md): claims, data, music, brands, voices, App Store previews
