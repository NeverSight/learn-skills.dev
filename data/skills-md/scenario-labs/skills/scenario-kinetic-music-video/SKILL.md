---
name: scenario-kinetic-music-video
description: "Use when turning a song into a kinetic-typography or motion-design music video, lyric video, visualizer or K-pop style MV with Scenario: a generated subject sheet, style frames and footage, plus a deterministic JavaScript/three.js engine for lyric type, mattes and tracked graphics timed to sung onsets. Also for revising, recutting or cutting teasers from such a video."
license: MIT
---

# Kinetic Music Video

A song goes in. A 1080p60 music video comes out: a motion designer's showreel cut to the track. Kinetic type, 2D and 3D graphics and transitions land on the beats and sung syllables. Generated footage of the subject is woven through it where the concept wants a performer. The untouched master is the only soundtrack.

The work splits by what each tool does best:

- **Scenario** supplies what code can't: a consistent subject with real physics, choreography, hair and lip-sync, in whatever art style each section needs.
- **The JS engine** supplies what video models can't: exact typography, frame-exact timing to onsets and beats, infographics, compositing around the subject, and endless re-renders at zero generation cost.
- **Sub-agents** give each section a dedicated designer. A shared style bible and a verification loop keep them coherent.

Connection and the core generation loop: see the `scenario` skill in this repo. For a song-to-video cut without the engine, see `scenario-seedance-music-video`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

Read `references/lessons.md` before starting. Every item in it cost real time or money once. `references/motion_library.md` is the design menu.

## Before you start (ask once, then run)

- **Workspace:** the Scenario team and project (`teams_list`; ask if there is more than one).
- **Subject:**
  - Who or what performs: a character from reference images, a mascot, a product, the artist's own likeness (their own photos and consent only), or nobody (a pure motion-graphics or lyric video).
  - Footage share: performer-led, a mix (often about 60/40), or graphics only.
- **Look:**
  - Ask for references: images, videos or links for the mood, the motion and the **color**. Vague color asks without references drift to safe palettes.
  - Decide the 2-4 looks and which sections own which.
  - Ask what must never appear.
  - Defaults: generated footage shown clean (no filters on it), graphics layered on and around it, a fast and upbeat showreel energy.
- **Brand:** any logo, wordmark or credit. Use official files in their official colors, only where the director wants them.
- **Budget:** lean (6-10 video generations), moderate (12-20) or big. Price each paid step with `dry_run` (one run per distinct payload, then total) before spending. Relative anchors: a 6 s 720p clip costs about twenty style frames, a 10 s clip about thirty-five, and a full mixed video about five hundred.
- **Format:** 16:9 1080p60 by default, with 9:16 or 1:1 re-layouts on offer. X caps standard accounts at 2:20, so plan a teaser.
- **Lyrics:** use them if supplied (they beat any transcript). Otherwise transcribe and flag the uncertain words at the end.

With no one around to answer, choose sensible defaults for the creative choices and write them into TREATMENT.md. Do not default the money: with no stated budget or no explicit team and project, stop before the first paid step and say what is missing.

## Workflow

### 1. Scaffold and analyze the song

Run `bash <skill>/scripts/scaffold.sh <song>` inside a new project folder, then follow `references/pipeline.md` §2:

- `audio_analysis.py` writes stems and `engine/data/audio.json`: beats, downbeats, kick/snare/vocal onsets, and 60 fps envelopes. **Measure the tempo**; labels lie (a "130 BPM" song was 98 with double-time drums).
- `lyrics_align.py transcribe`, then hand-correct `analysis/lyrics.txt`, then `lyrics_align.py align` writes `engine/data/lyrics.json` with word onsets.
- Check timing by eye with `plot_lyrics.py`. You can't listen, but the spectrogram shows where each word starts.

### 2. Research (parallel, background)

Launch two sub-agents with web access while you work on other things:

- **Culture:** for the song's subject, find recognizable events, memes and visual tropes, each with a verified fact, its iconic visual form, an insert idea and a short on-screen string.
- **Craft:** study the user's motion references (download them, contact-sheet them, read the frames), plus genre direction techniques. Extract timing numbers, color hex values and implementable JS moves.

Save the condensed results as `analysis/research_*.md`. Scene agents read them alongside `references/motion_library.md`.

### 3. Concept, style bible and treatment

- **Give the video a spine.** The strongest concepts make the edit itself carry the song's meaning: a device that progresses through the whole video, for example a counter, clock or countdown that moves with the song while the cut rate or the looks escalate with it. The spine usually lives in the HUD counters.
- **STYLE.md** (the law):
  - a one-line concept and the spine
  - the footage rules (clean plate and the back/mid/front layers, or another policy)
  - the looks, each with ground, ink, accent, rendering rule and matching footage style
  - the palette with roles
  - 4-5 type roles with named fonts
  - lyric display rules
  - a motion grammar mapping beats to effects, with the cut density per section
  - the subject (identity, design details usable as graphic motifs)
  - brand rules, references and bans
- **TREATMENT.md:**
  - song facts and the energy map
  - the arc
  - the **hook for the first 3 seconds** (the strongest idea in the video, and it must work as a muted autoplay)
  - one row per section: time range on downbeats, lyrics, look, must-have ideas
  - a footage map (filled in as clips land)
- **PLAN.md:** a one-page version for the director to approve before you spend on footage (unattended, this is the stop point if the budget is unstated).

### 4. Subject, style frames and footage on Scenario

Skip this for a graphics-only video, apart from any stills or 3D props. Otherwise follow `references/pipeline.md` §3-5:

- **Subject sheet:** a turnaround, expressions and callouts from the user's references. Look at it, then crop identity references from it.
- **Style frames:** one still per shot (an image model that takes reference images), in its section's look. Compose with negative space for type, on a set that composites (black void with rim light, flat color cyc, or white high-key). No text. Contact-sheet them and get the look approved cheaply (unattended: proceed only inside a stated budget).
- **Footage routes:**
  - Image-to-video from the frame for actions.
  - A video model with reference images and reference audio, given a **synthesized beat track** for dances that lock to the song, then beat-warp.
  - **Audio-to-video** from a frame plus a vocal-stem slice for lip-sync. The alternative is reference-audio video plus a lip-sync correction model.
  - Code instead of generation for networks, charts, UI and particles.
- Never send the song to a video model. Turn the model's native audio off when its schema offers it (the render takes sound only from the master either way), and launch everything in parallel (`jobs_wait` re-called with `pending_job_ids`, never `job_get`, never a relaunch).
- **Prep** every clip with `tools/prep_clip.sh`: frames, a subject matte (Apple Vision, with Scenario background removal as the fallback; see `references/pipeline.md` §5) and tracking (MediaPipe pose plus the matte bbox). Inspect the mattes. Write each clip's content, key moments, slot and matte quality into the footage map.

### 5. Engine and scene agents

- **Smoke-test first:**
  - Set `PAL` in `core.js`, and in `engine/timeline.js` set the sections on downbeats, `HUD` (title, mark, section codes, spine counters) and `POST` (neutral by default).
  - Write a tiny `_smoke.js`: plate → type behind the subject → matte → tracked label.
  - Render one still and a 5 s clip, then confirm audio and flashes line up with `av_sync_check.py`.
- **Brief the agents.** Fill in `AGENTS_BRIEF.md` from the template, then launch one background agent per section in a single message. Each gets its file, time range, lyrics, must-have ideas and clips, and reads AGENTS_BRIEF, STYLE, TREATMENT, ENGINE_API and the research first. Log the agent ids. For a teaser or anything under about 30 s, the lead may write the scenes itself and skip the research agents, PLAN.md and the per-section agents; keep the smoke test.
- **Deliver clips as they land.** Message the agent that needs each one ("clip ready: content, key moments, slot").
- **Review every report.** Contact-sheet the best stills and Read them. Fix engine-level problems yourself (they affect everyone) and tell the agents what changed.

### 6. Assemble, watch, iterate

- **Render the full cut** (3 workers, about 5 min for 2:00 on an M-series Mac). Wait for it in the foreground (or poll until it prints `wrote`) and carry on to verification and delivery: never end the run while a render or encode is still going, because a headless session that stops kills it.
- **Verify:**
  - `av_sync_check.py`: expect 0.0 ms audio and 0 to +1 frame visual. Below a correlation of about 0.15 the visual lag means nothing (type leading by `E.LEAD` reads as up to -3 frames): check onset stills instead.
  - `freezedetect`: no frozen footage.
  - Contact sheets at 0.5 s steps, 20 s per sheet.
  - Every section boundary, frame by frame.
- **Global look pass:** a still sheet across all sections, then tune `POST`, the palette and the HUD theme.
- **Revisions:** map each director note (they arrive as timestamps) to its section and send it back to the owning agent via SendMessage. Resuming keeps its context. Fix a weak shot by replacing it with a new generation in a different look, or with code, never by adding effects. Offer alternatives as timeline `variant`s (render with `--variant b`) instead of guessing.

### 7. Deliver

- **Videos:** an X-ready file (2-pass 21 Mb/s, under 512 MB), a teaser (verse plus first chorus) and a master, plus one file per variant. Use distinct filenames, because macOS is case-insensitive.
- **Stills:** full-res PNGs rendered by the engine, never grabbed from the compressed video.
- **Style sheet / making-of:** publish it as an artifact or doc: palette, type, subject sheet, source-vs-final footage pairs, a frame index, the pipeline and iteration counts.
- **Report:** tell the user what was verified, which lyrics you guessed, and the CU spent, summed from this run's `jobs_wait` rows (`cuCost`, logged in `analysis/jobs.md`); `usage` is project-wide and includes other work.

## Quality bar

- **Every word shows on time.** Each sung word is visible at its onset (as a hero or in the subtitle track), and hero words peak on the onset frame.
- **Integration, not decoration.** Every footage moment has a graphic that reacts to it (behind via the matte, tracked to it, timed to its move, or continuing its shapes). The footage pixels are untouched.
- **No static frames.** Footage always plays live, and something always moves.
- **One focal point per frame.** Type frames the subject and never covers the face. Behind-the-subject type still reads.
- **Section variance.** Mix the looks, 2D and 3D, poster slams and quiet subtitles. Never use the same type treatment on two consecutive lines. Cut density climbs with the song's energy, and showcase moments (logo, end card) get time.
- **Photosensitivity.** At most 3 full-frame luminance flips per second.
- **Watch it yourself** before calling it done, then take a second look at the first 3 seconds.

## Files in this skill

- Setup and analysis: [scaffold.sh](scripts/scaffold.sh), [audio_analysis.py](scripts/audio_analysis.py), [lyrics_align.py](scripts/lyrics_align.py), [plot_lyrics.py](scripts/plot_lyrics.py)
- Footage generation helpers: [synth_beat.py](scripts/synth_beat.py), [beatwarp.py](scripts/beatwarp.py)
- Footage prep: [prep_clip.sh](scripts/prep_clip.sh), [prep_video.py](scripts/prep_video.py), [matte.swift](scripts/matte.swift), [fixmatte.py](scripts/fixmatte.py), [matte_keyed.py](scripts/matte_keyed.py), [matte_fallback.py](scripts/matte_fallback.py), [track.py](scripts/track.py)
- Sync checks: [lipsync_check.py](scripts/lipsync_check.py), [dance_sync_check.py](scripts/dance_sync_check.py), [av_sync_check.py](scripts/av_sync_check.py)
- Rendering and review: [render.mjs](scripts/render.mjs), [still.mjs](scripts/still.mjs), [serve.mjs](scripts/serve.mjs), [sheet.py](scripts/sheet.py)
- Engine, copied into the project by scaffold.sh: [index.html](assets/engine/index.html), [main.js](assets/engine/main.js), [core.js](assets/engine/core.js), [plate.js](assets/engine/plate.js), [roto.js](assets/engine/roto.js), [typekit.js](assets/engine/typekit.js), [hud.js](assets/engine/scenes/hud.js), plus [timeline.template.js](assets/timeline.template.js) and [scene.template.js](assets/scene.template.js)
- [references/pipeline.md](references/pipeline.md): every command and Scenario call, step by step
- [references/engine_api.md](references/engine_api.md): the scene contract and the full `E` API (plates, mattes, tracking, post, HUD, variants)
- [references/motion_library.md](references/motion_library.md): looks, type system, a 40-move technique library, integration ideas, transitions, timing, easing and springs, sync and cut density
- [references/agent_brief_template.md](references/agent_brief_template.md): the brief each scene agent reads
- [references/lessons.md](references/lessons.md): production gotchas and direction defaults that held
