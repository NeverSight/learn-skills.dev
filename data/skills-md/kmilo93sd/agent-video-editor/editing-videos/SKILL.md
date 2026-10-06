---
name: editing-videos
description: >
  Gives an editor's judgment, with sourced numbers, for cutting and pacing, J and L cuts, jump cuts, b-roll,
  hooks and retention, captions, on-screen text and graphics, zoom and punch-in, audio levels in LUFS, music
  ducking, sound effects, basic color, thumbnails, titles, chapters and licensing. Use it when planning,
  scripting, editing, reviewing or publishing any video for YouTube, Shorts, Reels or TikTok: a talking
  head, a vlog, a podcast or interview, a screen tutorial, an explainer or a vertical clip from a long video,
  or when looking for royalty-free sound effects, music, animated graphics or a meme to recreate. Works with
  any tool (Premiere Pro, DaVinci Resolve, Final Cut Pro, CapCut, ffmpeg, Remotion, HyperFrames). Ships
  recipes per video type, a review checklist, a CC0 sound library, a CC0 graphics kit for HyperFrames, a
  meme reference with Content ID risk, and tested templates for narrated screen tutorials.
license: MIT (code and text); CC0-1.0 (audio in library/ and graphics in graphics/)
compatibility: >
  The editing craft needs nothing. The narrated screen tutorial templates need Node 20 or later and ffmpeg
  on the PATH, Playwright for recording, an ElevenLabs key for the voice, and HyperFrames for editing and
  rendering. The search tools of the sound library, the graphics kit and the meme reference need Node.
metadata:
  author: kmilo93sd
  version: "2.0.0"
  repository: https://github.com/kmilo93sd/agent-video-editor
---

# Editing videos

This skill gives an editor's judgment: when to cut, how long a shot or a caption lasts, how loud the music
goes, when a graphic helps and when it gets in the way. Every number says where it comes from: **official**
(platform or vendor docs), **study**, **creator** (practice without public data) or **house** (learned
reviewing real cuts). It is organized in two layers:

1. **The core** (this file, `references/` and `review-checklist.md`): craft that holds for any video and
   any tool.
2. **Recipes** (`recipes/`): what changes for one type of video. Load only the one that matches.

It does not replace the tool. On mechanics (file formats, APIs, a renderer's contract), the tool's own docs
or skills rule; on editorial matters, this skill does. `references/tools.md` maps the craft onto each tool.

## Process

| # | Step | What happens | Read |
|---|---|---|---|
| 1 | **Brief** | Video type, audience, platform and format (16:9 or 9:16), length, tool available. Pick the recipe | "Pick your recipe" below |
| 2 | **Story** | The promise (title and thumbnail idea) and a hook that delivers it in the first seconds; sections or chapters | `references/hook-and-retention.md` |
| 3 | **Assembly** | Select the best takes and order them; cut dead time; nothing is polished yet | `references/pacing-and-cuts.md`, the recipe |
| 4 | **Rhythm** | Shot length for the type, J and L cuts, jump cuts, b-roll, punch-ins | `references/pacing-and-cuts.md` |
| 5 | **Graphics and text** | Graphics only where they explain; text anchored to speech; captions | `references/graphics-and-text.md`, `graphics/`, `memes/` |
| 6 | **Audio** | Clean the dialogue, room tone, music under the voice, sound effects, then the master | `references/audio-and-sfx.md`, `library/` |
| 7 | **Color** | Exposure, white balance, matching shots; a look only after | `references/color.md` |
| 8 | **Review** | The recipe's checklist, then the core checklist, with frames and headphones | `review-checklist.md` |
| 9 | **Export** | Only with the person's approval: format, loudness master, check the file | `references/audio-and-sfx.md`, `references/tools.md` |
| 10 | **Publishing** | Title, thumbnail, description, chapters, captions, credits | `references/thumbnail-title-description.md`, `references/licenses.md` |

If the agent cannot touch the editor, it still does steps 1–8 as decisions: an edit decision list, a marker
list, caption files and instructions with numbers (`references/tools.md`).

## Hard rules (any video, any tool)

1. **Every cut has a reason**: it removes dead time, changes the information, or follows an action. Never
   in the middle of a word.
2. **Deliver the promise early.** What the title and thumbnail promise is seen or said in the first
   seconds; no logo intro or greeting before it.
3. **The voice is never fighting anything.** Music 18–25 dB under it and ducked, sound effects under it and
   never on a key word, room tone under every gap.
4. **Master once, to the destination**: -14 LUFS integrated and ≤ -1 dBTP for YouTube; -16 LKFS ± 1 for a
   podcast feed. Measured, not guessed.
5. **A graphic is never empty.** It enters at most 0.5 s before its word, has content within 1 s, and each
   element enters ≤ 0.6 s from when the voice names it **[house]**.
6. **Text stays long enough to read**: `max(1.5 s; words × 0.33 s + 0.5 s)`; captions ≤ 42 characters per
   line, ≤ 2 lines, ≥ 20 frames each.
7. **Zoom and punch-in only when motivated** by what is said, sharp, and never across a cut.
8. **Shots match**: exposure, white balance and levels consistent within a scene.
9. **Only licensed media**: CC0, the YouTube Audio Library, or a written license that allows commercial use.
   Nothing NC, nothing "found on YouTube". New sounds for the library leave their evidence in
   `library/LICENSES.md`. Graphics come from `graphics/` (CC0) or carry a recorded license. No copyrighted
   meme images, clips or sounds without a license: recreate the joke instead (`memes/README.md`).
10. **No invented numbers.** If no source supports a figure, say so and decide by the content.
11. **Nothing is rendered or published without approval**, and no cut is shown without passing its
    recipe's checklist and `review-checklist.md`.

## Pick your recipe

| The video is… | Recipe | What it adds to the core |
|---|---|---|
| One person talking to camera | [`recipes/talking-head.md`](recipes/talking-head.md) | Removing filler, softening jump cuts, punch-ins, b-roll on what is said |
| A day, a trip, an event | [`recipes/vlog.md`](recipes/vlog.md) | Finding the story, cold open, sequences, wind and location audio, matching cameras |
| A conversation with several cameras | [`recipes/podcast-to-youtube.md`](recipes/podcast-to-youtube.md) | Sync, cutting between angles, open mics, podcast master, chapters per topic |
| Vertical clips from a long video | [`recipes/shorts-from-long-form.md`](recipes/shorts-from-long-form.md) | Picking the moment, reframing to 9:16, burned-in captions, loops |
| A narrated software tutorial (screen recording) | [`recipes/narrated-screen-tutorial.md`](recipes/narrated-screen-tutorial.md) | The screen leads, honest speed, demo data, synthetic voice, chapter cards; tested templates (Playwright, ElevenLabs, HyperFrames) |
| Something else (explainer, essay, review…) | none | Use the core: the pacing table has a row per type; borrow from the closest recipe |

## Pacing at a glance

The full table, with the source of each number, is in `references/pacing-and-cuts.md`.

| Type | What is seen changes | Silence between phrases |
|---|---|---|
| Talking head | Every 2–5 s (creator) | 200–400 ms (creator) |
| Vlog | On events; film averages ≈ 4–5 s per shot (study) | Natural, with room tone |
| Explainer | First interrupt at 25–35 s, then every 2–3 min (creator) | 200–400 ms (creator) |
| Screen tutorial | When the action changes; shots ≥ 5 s (house) | ≥ 0.4 s (house) |
| Podcast / interview | On speaker changes and reactions; no source for a frequency | Natural pauses kept |
| Short / Reel / TikTok | Every 2–3 s; something new every 5–7 s (creator) | 200–300 ms (creator) |

## Audio at a glance

- **Master**: -14 LUFS, ≤ -1 dBTP for YouTube; upload AAC at 48 kHz.
- **Music** 18–25 dB under the voice, ducked 6–12 dB while someone talks.
- **Sound effects** 12–24 dB under the voice, one per on-screen event, the transient 2–4 frames before it.
- **Gains from measured levels**: `gain = 10^((voice_lufs - under_voice - sound_lufs)/20)`, capped at 1.

## CC0 sound library

`library/` ships 128 CC0 files, each measured in LUFS and true peak: 113 sound effects (mono WAV, 48 kHz,
-22 LUFS) and 15 music tracks (stereo MP3, 48 kHz, -16 LUFS). Categories: transition 18, click 12, appear
12, notification 11, success 7, error 5, typing 9, impact 5, stinger 14, office 17, ambience 3, music 15.
Paths below are relative to this skill's folder (for example `~/.claude/skills/editing-videos/`).

```bash
node library/search.mjs                          # categories
node library/search.mjs --category transition
node library/search.mjs whoosh --paths           # paths to copy
node library/search.mjs pop --voice -17          # with the gain for a voice at -17 LUFS
```

`--voice` puts effects 15 dB under the voice, music 20 dB and ambience 30 dB. Copy the files into the video
project; do not link them from outside it. Licenses and sources: `library/LICENSES.md` and
`references/licenses.md`. After adding a sound, run `node library/verify.mjs`.

## Graphics kit (CC0)

`graphics/` has 26 drop-in graphics for HyperFrames: arrows, circles and highlight rings, underlines and
scribbles, a spotlight, a cursor click ripple, callouts and tooltips, a lower third, keyboard-key chips, a
step counter, a progress bar, a countdown, a checkmark and a cross, a before/after split, chapter cards, an
end-screen layout, light-leak and grain overlays, and a generic like-and-subscribe prompt. Each is an HTML
snippet (plus an SVG for the shapes): a timed `.clip`, colors and sizes in `--gfx-*` custom properties, and a
`gfx.<name>(tl, el, opts)` function that adds seekable tweens to the composition's timeline. Anchor `at` to
the word that names the target; `catalog.json` gives each asset's duration and when not to use it.

```bash
node graphics/search.mjs                         # categories
node graphics/search.mjs --category arrows
node graphics/search.mjs shortcut --paths        # paths to copy
```

Open `graphics/preview.html` to see them all animate. After adding one, run `node graphics/build-preview.mjs`
and `node graphics/check.mjs`.

## Memes

`memes/catalog.json` is a reference of 59 memes and meme formats, with no media: what each one means, when
it fits in a tutorial, how long it stays on screen, how to recreate it with `graphics/`, who owns the
original and its Content ID risk. Recreate the joke or license the original; never use a meme's music. Read
`memes/README.md` first.

```bash
node memes/search.mjs fail --risk low
```

## Index

| File | What it covers |
|---|---|
| `references/pacing-and-cuts.md` | Pacing table by video type with sources; what a cut is for; shot length; J and L cuts; jump cuts; b-roll; transitions; segmentation |
| `references/hook-and-retention.md` | How YouTube measures retention; the hook by type; open loops; chapters; end screen and closing |
| `references/graphics-and-text.md` | When to use a graphic; anchored and never empty; text duration; captions and subtitles; zoom and punch-in; entrances; safe zones; legibility |
| `references/audio-and-sfx.md` | Target levels; dialogue cleanup; room tone; music and ducking; computing gains; sound effects; mastering |
| `references/color.md` | Order of work; LUTs as a starting point; matching shots; SDR and HDR delivery |
| `references/thumbnail-title-description.md` | Thumbnail spec and practices, A/B tests, title, description, hashtags, chapters |
| `references/licenses.md` | Music, SFX and footage sources for a monetized channel; fair use; Content ID |
| `references/tools.md` | Applying the craft in an NLE (EDL, markers, captions, instructions), ffmpeg, Remotion and HyperFrames |
| `review-checklist.md` | The universal review: measured, by eye, by ear, before publishing |
| `recipes/talking-head.md` | Talking-head recipe and checklist |
| `recipes/vlog.md` | Vlog recipe and checklist |
| `recipes/podcast-to-youtube.md` | Podcast and interview (multicam) recipe and checklist |
| `recipes/shorts-from-long-form.md` | Vertical clips from long videos: recipe and checklist |
| `recipes/narrated-screen-tutorial.md` | Narrated screen tutorial recipe, its house rules, process and checklist |
| `recipes/narrated-screen-tutorial/voice.md` | Script and synthetic voice for the tutorial: phonetic acronyms (Spanish narration), ElevenLabs, LUFS per chapter, whisper |
| `recipes/narrated-screen-tutorial/hyperframes-generator.md` | The tutorial edit in HyperFrames: skills per step, rules in the contract, the generator and its checks, pitfalls, review loop |
| `recipes/narrated-screen-tutorial/templates/` | Tested templates for that pipeline; each has `--help` |
| `library/` | CC0 sounds: `catalog.json`, `search.mjs`, `verify.mjs`, `LICENSES.md`, `sfx/`, `music/`, `tools/synthesize.py` |
| `graphics/` | CC0 HyperFrames graphics: `catalog.json`, `search.mjs`, `preview.html`, `check.mjs`, `LICENSES.md`, one folder per category |
| `memes/` | Meme reference with no media: `README.md` (read first), `catalog.json`, `search.mjs` |
