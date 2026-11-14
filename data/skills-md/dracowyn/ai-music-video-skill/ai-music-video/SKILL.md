---
name: ai-music-video
description: End-to-end method for making music videos and lyric videos with Claude as the production team, using generated images and video (Midjourney, SD/Flux, Seedance, Kling, Wan, Suno) and/or all-code animation synced to the song. Covers choosing a style route, lyric alignment (word and syllable timings) and beat grids, storyboards and shots.json, character consistency, image and audio-conditioned video prompts, lip-sync divergence checks, karaoke typography, transitions, motion blur, rendering, and multi-agent production and review. Use whenever the user wants a music video, lyric or karaoke video, animation set to a song, a storyboard or shot list for a song, lyric timestamps, generation prompts for such a video, or is fixing lip-sync drift, character drift, washed-out generated footage or mechanical-looking code animation. 中文触发：MV、歌词视频、卡拉OK字幕、对口型、分镜、歌词时间轴。
license: MIT
---

# AI Music Video

One person owns taste; Claude is the production team. This skill is distilled from three music videos made that way (see Terms). The project's own decisions always override this skill: read the project's brief and docs first.

## Principles

1. **The song is the clock.** Fit a beat grid and align the lyrics before anything else. Cuts, camera keys, hits and words are looked up from that data by lyric content and beat number, never typed as seconds. Sync is measured, not eyeballed.
2. **Meaning is drawn in code, on time.** The picture underneath may be generated or drawn by code; the words, the image that says what each line means, and the running device live in a code layer that is exact and on the beat.
3. **Pick one style route and hold it.** The routes disagree on lyric display, transition density and the running device, and each works. Mixing them is what looks amateur.
4. **Fan out, judge, merge, fix.** Research, lyrics, storyboard and animation each run as several independent drafts → judges with different lenses → a merge from the best → a critic who edits the file. The human gives a few decisive notes at gates.
5. **Everything is a file.** Each step writes a file the next step reads (TASTE.md, audio.json, lyrics.json, STORYBOARD.md, shots.json). Agents read files, not memory.

## Terms

| Term | Meaning |
|---|---|
| EV | *ESCAPE VELOCITY* — 5-min lyric video: Midjourney plates, Suno song, Seedance audio-conditioned clips, JS overlay. [cases/escape-velocity.md](references/cases/escape-velocity.md) |
| PD, CAB | *PDoomVideo* (all-code watercolour cartoon, p5.brush) and its later general base *ClaudeAnimationBase*. [cases/pdoom.md](references/cases/pdoom.md) |
| PV | *pdoom-video* (all-code "illustrated treatise" plates, three.js + GLSL, word-synced karaoke). Same song as PD. |
| route | editorial, narrative or plates — see [routes.md](references/routes.md) |
| plate | a still image used as a shot's base (generated or rendered); in the *plates* route, PV's sense: a section drawn in its own visual idiom |
| clip / cover | a generated video segment / a re-take that replaces a clip from its divergence point on |
| running device | the element that carries progress through the whole video (counter, meter, countdown), as an overlay or as a prop inside scenes |
| motif | a simple graphic (a dot, a line) that recurs and carries transitions |
| anchor | how a time is derived: a lyric (line, word) or beat plus a snapping rule |
| reads | what the viewer must understand in a shot, in order, each with its own time |
| out | how a shot hands over to the next one |

## 1. Choose

**Route** (details, per-route edit rhythm and transitions: [routes.md](references/routes.md)):

| Route | Fits | Picture | Lyrics on screen | Steps to run |
|---|---|---|---|---|
| editorial | performer-led songs, fashion, meme-dense lyrics | generated plates and clips + code overlay | many typographic modes + an explainer graphic per line | all |
| narrative | a cartoon character with a story | all code, one world | one karaoke band (or none); lines are acted as visual puns | skip 6–7; code character in 4 |
| plates | abstract, information design, essays | all code, a new visual idiom per section | lyrics *are* the graphics (on curves, typed, stamped, burned) | skip 4, 6–7 |

**Lip-sync mechanism** of the video model, if any singing is on screen ([lipsync-production.md](references/lipsync-production.md)):
- the model generates its own soundtrack from a reference audio → measure with `scripts/avsync_check.py`
- lip-sync applied after generation (the output track *is* your audio) → `avsync_check.py` will always say IN_SYNC; check visually or with a lip-sync confidence model
- no audio input → avoid singing close-ups; cut around mouths

**Alignment precision** ([lyric-alignment.md](references/lyric-alignment.md)): line (layout only) → word (captions, most cuts) → syllable (karaoke wipes, per-letter hits).

## 2. Quick start: a 60-second all-code karaoke video

1. Write TASTE.md from [the template](assets/templates/taste.template.md); pick the plates or narrative route.
2. `make_approx.py` → lyrics.approx.json + audio.approx.json; start animating immediately.
3. `check_timebase.py --write-fixed` on the stems, `fit_beat_grid.py --sections audio.approx.json` → audio.json, `align_lyrics.py` → lyrics.json; spot-check the QA plots.
4. Write shots.json with anchors ([template](assets/templates/shots.template.json)), `resolve_shots.py`, then `validate_shots.py`.
5. Render with a pure-function renderer (Remotion, ClaudeAnimationBase, or your own `renderAt(t)` page). Review with `contact_sheet.py` (a sheet per shot, a hand-off sheet at every cut), fix, encode with BT.709 tags.

## 3. Full pipeline

### 0. Brief (with the human)
- First take apart what makes the reference work great, then plan your own.
- List the director's taste assets and every tool's quota and price. Write **TASTE.md** (concept, voice and motion, anti-slop list, originality limits, colour and type roles, verbatim director quotes, revision log). Every judge and animator reads it.
- Agree concept, song, character and storyboard; then run autonomously and interrupt only for paid-tool failures or taste calls. Show a short result before investing in a fallback.
- Store the director's words verbatim. Requirements arrive late (EV became a lyric video after the song was picked): broadcast every change to all downstream agents.
- Set a target and a ceiling budget.

### 1. Research and lyrics (multi-agent; skip if the song exists)
- Parallel researchers per angle, adversarial fact-checkers whose job is to refute, a synthesiser; several writers with different angles, judges with different lenses, a merger, a critic who counts syllables and fixes the file. Details: [agent-workflows.md](references/agent-workflows.md).
- Write a device into the lyrics that code can render (a countdown, a counter) and a hook line that repeats.
- Spell numbers and acronyms as spoken ("A G I") and keep that spelling identical in the song prompt, the aligner's pronunciation map and video prompts.

### 2. Song
- Generate several versions; the human picks by ear. **Measure the result**: prompted BPM and length are wishes, not facts. Replan to the real length.

### 3. Timing data
- Write approx data first so animation can start; the loader prefers exact data when it exists.
- One timebase: the gapless decode of the final mix. Check every stem against it (`check_timebase.py`).
- Fit the grid (`fit_beat_grid.py`): constant songs → period + phase; drifting songs → tempo curve. Never cut on raw tracker beats. Verify the grid by ear against a click: a grid at 2/3 or 3/2 of the real tempo still "looks" rhythmic (PD shipped one).
- Align words, and syllables where needed (`align_lyrics.py`; heavy pipeline in the reference). Priority: grid > words and syllables > discrete drum events > continuous envelopes.
- Write TIMELINE.md ([template](assets/templates/timeline.template.md)).

### 4. Lead character
- Code character when the style allows: one function with pose, expression vocabulary, eased mood changes, beat-locked moves and prop hooks; render a model sheet first ([code-animation.md](references/code-animation.md) §1).
- Generated character: lock the identity method with a small test batch before mass production; write the canon per framing ([template](assets/templates/canon.template.md)); always state ethnicity/skin (humans) or species, anatomy and colour hex (non-humans); self-check prompts before submitting ([prompt-patterns.md](references/prompt-patterns.md)).
- The face can stay hidden (cap brim, motion blur, detail shots) — as taste and as a hedge against identity drift.

### 5. Storyboard (multi-agent; the human approves)
- Several directors with different angles → judges (audience, taste, producer feasibility) → a lead who merges into STORYBOARD.md and shots.json. Format, continuity checklist, reads, outs, anchors: [storyboard.md](references/storyboard.md).
- Hard constraints: the timeline is covered 0→end with no gaps; the first 3 s are a hook; no cut inside a sung word; video seconds and clip counts within budget; lead on-screen share if there is a lead.
- Edit rhythm and transition density follow the route ([routes.md](references/routes.md)). After resolving, run `cut_stats.py` and compare with what the docs claim.
- Give the human a contact sheet or PDF. Humans catch what agents miss (a reversed head, one plate used for eight shots).

### 6. Plates (generated route)
- Prompt = framing and composition + concrete scene and action + **empty space where the type goes** + chapter style words + `no text, no letters, no logos` ([prompt-patterns.md](references/prompt-patterns.md)).
- Anything that must carry words is generated **blank**; code prints the words in perspective.
- **Keep generation inputs in full colour; stylise in post.** Monochrome prompts and pre-graded first frames wash the video out.
- Log one line per batch: why it exists.

### 7. Audio-conditioned video (generated route)
- Full procedure: [lipsync-production.md](references/lipsync-production.md). Rules: feed the vocal window for singing clips and the full mix for motion clips; singing shots are frontal, locked, no head turns, 4–5 s windows; budget ≈ 2× on-screen seconds for singing, 1× for motion; check every singing take right away; at most two identical retries, then change one variable or use a lip-sync model; two clips never start from the same frame.

### 8. Motion, lyrics and graphics (multi-agent; the most expensive step)
- The main session writes the shared layer first: engine, timing helpers, the running device, the motif module, a hand-off registry, and ANIMATION_GUIDE.md ([template](assets/templates/animation-guide.template.md)).
- One agent per chapter edits only its file → an art-director agent renders real frames and returns ≤ 14 timed fixes → the chapter agent fixes and re-verifies. Pipeline per chapter; don't wait for the others. Agent prompts must be resumable ("if the file has content, keep what works and finish").
- Engine: every frame is a pure function of song time; no state, no `Math.random`, no clock. With motion blur, follow the sub-frame rules ([code-animation.md](references/code-animation.md) §7).
- Every line gets an on-screen event that says what it means; the form follows the route. Karaoke highlight never leads the voice ([code-animation.md](references/code-animation.md) §4).
- Avoid the code look: no twinning, no constant speed, ease everything, anticipation and follow-through.
- Accent colour is a spice, not a grade; carry the emotional arc with brightness.
- Verify: `N/N` lyric words on screen; contact sheets at shot first/last frames, line first/last words, graphic entrances and transition midpoints — **read every image**; a hand-off sheet at every cut; frame-by-frame strips for key actions; count frames per read; record ms/frame.

### 9. Grade and deliver
- Print-style filters must not kill saturation; keep some camera character.
- Render full frames; encode with BT.709 matrix and tags; `-tune grain` for grainy work. Optional motion blur: shutter 0.2, adaptive sub-frames ([code-animation.md](references/code-animation.md) §8).
- Wrap up: write down lessons and gather reusable assets in one place.

## 4. Checklists

Before production
- [ ] TASTE.md with route, anti-slop list and verbatim director quotes
- [ ] Measured duration and tempo; audio.json fitted and checked by ear against a click
- [ ] All stems checked against the mix timebase
- [ ] Identity method tested on a small batch (generated route) or model sheet rendered (code character)

Every shot
- [ ] Time comes from an anchor, not a typed number
- [ ] `out` written; reads fit with time to land
- [ ] No cut inside a sung word; hits land on the grid
- [ ] Words appear on or after their sung time
- [ ] Singing clip checked (generated route), cut on the suggested eighth note

Delivery
- [ ] `validate_shots.py` passes; `cut_stats.py` matches what the docs say
- [ ] Hand-off sheet reviewed at every cut
- [ ] BT.709 tagged; final audio is the master mix, not the model's track

## 5. Anti-patterns

| Don't | Because | Do |
|---|---|---|
| Trust prompted BPM or length | the song drifts or runs long | measure, fit a grid |
| Cut on raw tracker beats, or on line-level subtitle times | jitter, missed beats, off-grid cuts | fitted grid + anchors |
| Type seconds into scene code | re-alignment breaks everything | look times up by lyric and beat |
| Estimate karaoke progress from character counts | highlight drifts from the singing | word/syllable alignment |
| Mix stems with different timebases | words 1–2 frames off | cross-correlate against the mix |
| Monochrome generation prompts, pre-graded first frames | grey, lifeless video | full colour in, style in post |
| Test identity while mass-producing | the same batch made three times | small test batch first |
| Paste the whole outfit into every prompt | close-ups widen, paste errors | per-framing canon + self-check |
| Turn heads during sung lines | covers double, fall back to lip-sync models | frontal, locked; turn in motion clips |
| Retry the same settings a third time | wasted budget | change one variable or fall back |
| The same effect on every cut; a chorus function re-skinned four times | reads like slides, no build | design each out; escalate repeats |
| Several events in one shot at one speed | nobody understands it | reads with time to land |
| Agents that read code but never look at frames | visual bugs ship | render and read contact sheets |
| Let the image model write text | gibberish, uneditable | blank props + code type |
| Change a constraint for some agents only | work follows the old rule | broadcast to every downstream agent |

## 6. Files

| File | Use when |
|---|---|
| [routes.md](references/routes.md) | choosing and executing a route: edit rhythm, transitions, running device, lyric display |
| [storyboard.md](references/storyboard.md) | writing STORYBOARD.md / shots.json |
| [lyric-alignment.md](references/lyric-alignment.md) | timing data: timebase, grid, word/syllable alignment, CJK lyrics, QA |
| [code-animation.md](references/code-animation.md) | the code layer or an all-code video: characters, transitions, karaoke, motion, rendering, review |
| [prompt-patterns.md](references/prompt-patterns.md) | any image, video or song prompt |
| [lipsync-production.md](references/lipsync-production.md) | planning or fixing sung shots |
| [agent-workflows.md](references/agent-workflows.md) | running the multi-agent stages |
| [tool-versions.md](references/tool-versions.md) | which tool versions the findings were measured on, prices, obsolete methods |
| [cases/escape-velocity.md](references/cases/escape-velocity.md), [cases/pdoom.md](references/cases/pdoom.md) | benchmarks, evidence, director quotes |
| `assets/templates/`, `assets/schemas/` | TASTE, CANON, STORYBOARD, ANIMATION_GUIDE, TIMELINE templates; JSON schemas for audio, lyrics, shots |

Scripts (`scripts/`, Python ≥ 3.9, ffmpeg ≥ 5.1 and ffprobe on PATH; install with `pip install -r scripts/requirements.txt`, or run one with `uv run scripts/<name>.py`; each has `--help`; full CLI docs in `scripts/README.md`):

| Script | Does |
|---|---|
| `make_approx.py` | approx lyrics/audio data from lyrics text + LRC or a guessed tempo |
| `check_timebase.py` | offset of stems vs the mix |
| `fit_beat_grid.py` | fitted beat grid → audio.json |
| `align_lyrics.py` | word/syllable forced alignment → lyrics.json (needs torch, torchaudio) |
| `resolve_shots.py` | anchors → shot times |
| `validate_shots.py` | coverage, cuts in words, reads, budgets, reuse |
| `cut_stats.py` | edit statistics recomputed from data |
| `contact_sheet.py` | sheets, hand-off sheets at cuts, frame strips, crops |
| `avsync_check.py` | lip-sync divergence and cut point for a generated singing clip |

Tool versions and prices change; this skill states capabilities and keeps versions in [tool-versions.md](references/tool-versions.md).
