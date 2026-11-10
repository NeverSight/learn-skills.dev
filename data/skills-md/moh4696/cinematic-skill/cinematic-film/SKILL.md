---
name: cinematic-film
description: Makes narrated cinematic films entirely from code, on any subject. One continuous camera glides over one designed world of photos, documents, cards, maps with routes and big numbers, with every stamp, highlight and number landing on the narrator's word, then sound effects, an optional score and burned-in captions. For documentaries and history, product launches, brand and founder stories, science and tech explainers, biographies and true crime. Covers the script, voiceover from any TTS split into timed lines, images (archives with their licences, your own photos, AI stills), a beat table, the scene, self-review stills and a memory-safe parallel render. Use for "make a cinematic video about", "documentary about", "explainer video", "launch film", "Vox-style video", "evidence board animation", or turning a story into a video for X, YouTube or TikTok.
---

# Cinematic film

A film made this way is one camera move over one world. Every photo, card, clipping, map and number lives on one big board, and the camera travels between them along string, routes and arrows as the story moves. Every visual hit is timed to the word the narrator says. It is all code (Skia in Python), so it renders the same every time, any topic fits, and a new voice re-times the whole film by itself.

Built from a 5:22 documentary about Al Capone, then opened up to any subject. The rules here were written from what broke while making it.

## Tools

| File | What it does |
| --- | --- |
| `scripts/check_setup.py` | Checks Python, skia-python, ffmpeg, fonts and memory; says what to install |
| `scripts/get_fonts.py` | Fetches open-licensed fonts (Bebas Neue, Homemade Apple) for any text role this machine lacks |
| `scripts/new_project.py` | Starts a project from `assets/template/` (a runnable explainer), or the documentary example with `--example` |
| `scripts/make_beats.py` | Writes `beats.md`, the table you approve; lints chronology, line length, digits in spoken text |
| `scripts/tts_say.py` | Free scratch voice (macOS `say`, espeak-ng, or any TTS command) to time the film before the final voice |
| `scripts/split_takes.py` | Cuts whole-section takes into one clip per line and flags suspect cuts |
| `scripts/build_narration.py` | Joins the lines into `audio/narration.m4a` and `audio/timing.json`, which the film is built on |
| `scripts/fetch_commons.py` | Searches Wikimedia Commons, downloads with licence and credit, refuses non-free files, writes `credits.md` |
| `scripts/make_map.py` | Projects public-domain boundaries (any country or region) for the map |
| `scripts/prep_assets.py` | Grades every image into one look (black and white, sepia or natural colour); generates the board textures |
| `scripts/engine.py` | The film engine: camera, spotlight, items, maps, looks, film finish |
| `scripts/render.py` | Stills, contact strips, the cue list, and the parallel MP4 render |
| `scripts/build_sfx.py` | Synthesises every sound effect from the cue list (no samples, nothing to license) |
| `scripts/mix_soundtrack.py` | Voice, effects and optional music, ducked and loudness-normalised |
| `scripts/burn_captions.py` | Burns one of four caption styles into the finished film and writes an SRT |

Needs Python 3.9+, `pip install skia-python numpy pillow` (scipy optional) and ffmpeg. Run `scripts/check_setup.py` first; on Linux or Windows, also run `scripts/get_fonts.py` per project. All commands take `--project <folder>`.

## Pick the film

| Kind | Look | Images | Typical items |
| --- | --- | --- | --- |
| History, true crime, investigation | `wall`, `slate` | Archive photos and documents, graded `bw` | Prints, torn clippings, stamps, red string, map routes |
| Product launch, brand or founder story | `studio`, `charcoal` | Your product shots and team photos, graded `natural` | Cards, big numbers, counters, arrows |
| Science, engineering, how it works | `blueprint`, `paper` | Diagrams, archive or AI stills | Cards, counters, pen marks, maps |
| Tech, space, trailers | `night` | Screenshots, renders, AI stills | Big type, counters, routes, cards |

Mix freely: the looks are a board and a finish, and every item works on every look. `references/story.md` has a story shape for each kind.

## The rules

1. **One hero per line.** Each narration line has exactly one thing the camera is on. The spotlight dims everything else.
2. **Hits land on the spoken word.** A stamp slams on "charged", not on the line start. Time everything with `doc.W(line, "word")`.
3. **Show a phrase one way.** Either type it on screen or show it on a real document, never both. Body copy on documents is grey rows, never filler words.
4. **Time only moves forward after the opening.** A cold open may jump ahead. After one bridge line ("Four years earlier..."), story time only goes forward.
5. **Type you can read on a phone in one second.** Big condensed caps. A typed label on screen should be about 3% or more of frame height.
6. **Less is more.** Strings fade after their beat, and old items dim. The final pull-back should look composed, not cluttered.
7. **Nothing invented that looks real.** Real photos and documents get credits. A document drawn in code is labelled a recreation and quotes only words that were really written. AI images are fine for illustration, but never as evidence of a real event or a real person.

## Workflow

Stop for the user's approval at the four gates (marked **Gate**).

1. **Story.** Research, then write `script.json`: takes (sections) of lines, each with `text`, `spoken` (numbers as words), `hero` and `typed`. Keep fact notes alongside. 60 to 90 seconds is about 150 to 230 words. Details are in `references/story.md`.
2. **Beat table.** Run `scripts/make_beats.py` and fix every lint warning. **Gate:** the user approves `beats.md`, including the facts.
3. **Images.** List every image in `photos.json`: its id, kind and where it comes from.
   - Archive images: `fetch_commons.py search`, `category` and `get`.
   - The user's own files: drop them in `<project>/assets/photos/`.
   - AI stills: generate them in one style (the `motion-assets` skill plans and prices them).
   - `references/archive.md` covers other archives and the rights rules.
4. **Scratch voice.** Run `tts_say.py`, then `split_takes.py`, then `build_narration.py`. Listen to every line `split_takes.py` flags. Now the timings are real.
5. **Assets.** Run `make_map.py` if the story travels, then `prep_assets.py`.
6. **Scene.** Write `scene.py`: lay out the board in clusters per section, add items on `doc.L`/`doc.W` times, then camera and spotlight keys (`film.shot`). Read `references/film.md`. Both shipped projects show the patterns: `assets/template/scene.py` (explainer, studio look) and `assets/wright-flyer/scene.py` (documentary, every item type).
7. **Look test.** Run `render.py --probe` on one still per line at 1280x720 and look at all of them, then `--strip` on every big camera move. **Gate:** show the user stills of the opening and the look.
8. **Draft.** Render the first 30 seconds at 1280x720 with the scratch voice. **Gate:** the user watches it.
9. **Final voice.** Record it with any TTS or a person (`references/voice.md`). Run split, build, and probes again; nothing in the scene changes.
10. **Sound.** Run `render.py --cues`, then `build_sfx.py`, then `mix_soundtrack.py`, adding a score if wanted. Read `references/sound.md`.
11. **Finish.** Do the full render, then `burn_captions.py` and the SRT. Read `references/performance.md` before rendering at 1440p or 4K. Hand over `credits.md` with the film.

## Self-review, every time

Look at the stills before you claim anything works. These are the mistakes that showed up, every one in a real render:

- Dark ink on a dark board: invisible. Use light type on dark looks, or `bar_h=0.92` for a full label block behind dark type.
- The camera moved on but the spotlight stayed behind, leaving a dark frame. Use `film.shot()` unless they should part.
- Map scale too small: a whole coast smaller than one photo. Pick `K` so each place with prints gets its own room (`references/film.md`).
- Map labels colliding. Put the label on the side away from its neighbour.
- A cluster straddling the map's edge. Keep clusters either on the map or clearly off it.
- Highlights a few pixels off their words. Use `PaperDoc.phrase_spans`, and `doc.on(print, fx, fy)` with fractions read off a grid overlay of the image.

## Shipped projects

- `assets/template/`: "From Cherry to Cup", a 25 second explainer in the studio look, made of cards, arrows and a counter, with no images. `new_project.py my-film` copies it. Give it a scratch voice and it renders.
- `assets/wright-flyer/`: "Twelve Seconds", a 90 second documentary about the first flight and the $50,000 rival who crashed twice. It uses seven public-domain photos, the US map, two typeset documents and every item type.

```bash
python3 scripts/new_project.py wright --example
python3 scripts/fetch_commons.py get --project wright
python3 scripts/make_map.py --project wright && python3 scripts/prep_assets.py --project wright
python3 scripts/tts_say.py --project wright && python3 scripts/split_takes.py --project wright && python3 scripts/build_narration.py --project wright
python3 scripts/render.py --project wright --size 1280x720 --out out/draft.mp4 --audio audio/narration.m4a
```

## Related skills

From [Open 3D Skills](https://github.com/Moh4696/open-3d-skills): `motion-assets` plans and prices AI stills when a film needs illustration, and `frame-capture` records web pages instead of code-drawn films.
