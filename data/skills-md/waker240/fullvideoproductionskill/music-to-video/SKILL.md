---
name: music-to-video
description: Build a HyperFrames video around a supplied music track, using measured rhythm and editable visual concepts. Use when music determines the timeline.
compatibility: Requires sibling skills from this pack, a local filesystem and shell, Node.js 22.20.0+, and FFmpeg/ffprobe for media work. Generation providers and desktop tools are optional, separately configured capabilities.
---

<!-- Public portability adaptation, 2026-09-26. -->

Install this skill with its sibling skills. See [runtime setup and capability boundaries](../hyperframes/references/install-portability.md) before executing commands. User instructions and the requested production stage take precedence over workflow defaults.

# music-to-video — one music-grounded, beat-synced video workflow

Use this skill to turn a **music track** into a beat-synced HyperFrames video. You analyze the track once, lay out the frames, fill in a per-frame plan, and build each frame as a composition. The input is a music track plus optional user images or videos — there is **no narration and no website capture**. Typography and templates are the floor (a complete video needs zero assets); any media the user supplies is cut in on the same beat grid.

You are the **orchestrator**. Work in `videos/<project>/`. Run the steps in order and pass each **Gate** before moving on. Two steps need the user: **Step 3** (plan approval) and **Step 6** (render approval). Do every step yourself except **Step 4**, where you dispatch **one sub-agent per frame**. Keep design and motion rules out of this file — they live in `references/` and the `frame-worker` sub-agent.

`SKILL_DIR` = this skill directory. `PROJECT_DIR` = `videos/<project-name>/`.

Workflow: Step 0 setup → `hyperframes.json` + `assets/bgm.mp3`; Step 1 analyze → `audiomap.json`; Step 2 skeleton → `STORYBOARD.md` (frames, groups `TBD`); Step 3 plan → complete `STORYBOARD.md` + `frame.md`; Step 4 build → `compositions/frames/NN-*.html`; Step 5 assemble → `index.html`; Step 6 render → `renders/video.mp4`.

## Two ideas that shape everything

- **One canonical analysis record.** Use `analyze-beatgrid.py` for consistent timing data, then verify its results against the track. Analysis can fail; do not treat energy, onset or beat estimates as infallible. For weakly rhythmic music, prefer phrases and energy to a tracker-imposed grid. Correct a demonstrated error explicitly and keep one versioned timing source.

---

## Step 0: Setup, BGM, and inputs

Goal: Establish the music source, create the HyperFrames project, and note any user-supplied media.

The **music is the spine** — establish one track before anything else. This skill is tuned for **fast, high-energy BGM**: a strong beat grid drives the cuts (calm tracks work, but pace by phrase rather than beat). If the user gave you audio — a music file, or a video whose audio should drive the edit — use it. If not, select one already-reviewed, frozen local track whose mood fits the brief. Register that file with `/media-use --adopt` and record its provenance before use. This workflow never searches for, retrieves, or generates music. If neither a user track nor a reviewed frozen local track exists, stop clearly: there is no runtime music-engine fallback.

Normalize the selected source with `ffmpeg`; never copy arbitrary bytes to an `.mp3` filename or merely change the extension. This handles WAV/M4A/FLAC inputs and extracts a video's audio while producing the exact codec/container the assembler expects. Stage any user-supplied images or videos so frames can weave them in on the beat grid; otherwise typography carries the whole video.

Initialize only if `hyperframes.json` is missing. Name `<project>` from the brief in kebab-case, such as `midnight-drive-loop` — never a timestamp. `init` checks the installed skills against the latest on GitHub and updates the global set if any are out of date.

```bash
npx --yes hyperframes@0.7.17 init "videos/<project>" --non-interactive --skip-skills --example=blank
mkdir -p "$PROJECT_DIR/assets" "$PROJECT_DIR/renders"
ffmpeg -y -i "<user-or-reviewed-local-track>" -vn -map_metadata -1 \
  -c:a libmp3lame -b:a 256k -ar 48000 -ac 2 "$PROJECT_DIR/assets/bgm.mp3"
node <MEDIA_USE_DIR>/scripts/resolve.mjs --adopt --project "$PROJECT_DIR"
# only if the user gave you images/videos:
node <SKILL_DIR>/scripts/stage-assets.mjs --from <dir> --hyperframes "$PROJECT_DIR" --into public
```

The **brand** (font + palette) is chosen at Step 3, not here. Don't pick a genre or a track type up front — assets are just an optional ingredient, and the genre emerges from the per-frame choices.

**Gate:** `hyperframes.json` + a successfully probed `assets/bgm.mp3` exist; the selected source and license/provenance are recorded in the local media ledger; aspect / length / fps and (if any) the asset inventory are noted.

---

## Step 1: Analyze the music

Goal: Produce the one canonical timing analysis the whole video is built on.

`analyze-beatgrid.py` is the **only** beat analyzer — never re-measure beats with another tool or by ear. It reads the track once and writes `audiomap.json`: energy phases (level / density / feel), onsets + `onset_rate`, rolls, silences, `hard_stops`, `key_moments`, phrases, tempo / grid, and `audio.duration_sec`. It's deterministic — the same file always gives the same map. Most fields are reliable on any music; `bpm` and `beats_sec` are reliable only when the music is genuinely rhythmic, and judging that is the call you make at Step 2.

Prerequisites: Python 3 with `librosa`, `numpy`, and `soundfile` available. If import fails, install them into the active Python environment before running the analyzer:

```bash
python3 -m pip install librosa numpy soundfile
```

```bash
python3 <SKILL_DIR>/scripts/analyze-beatgrid.py "$PROJECT_DIR/assets/bgm.mp3" \
  -o "$PROJECT_DIR/audiomap.json" --print
```

**Gate:** `audiomap.json` exists; `audio.duration_sec` is known.

---

## Step 2: Frame skeleton (structure only)

Goal: Read the music and lay out the frames — the skeleton of `STORYBOARD.md`.

Read [`references/frame-skeleton.md`](references/frame-skeleton.md). Turn `audiomap.json` into the **skeleton** of `STORYBOARD.md` yourself — there is no intermediate JSON. Cut the track into **frames** at real musical changes (`hard_stops`, SURGE / DROP `key_moments`, the edges of a roll, a stretch with no onsets, a big energy jump), snapping every boundary to an audiomap anchor. For each frame set `span_sec`, `pacing` (the verdict from Step 1's trust call — `beat_cut` when the grid is real, `phrase_flow` when it's a metronome imposed on calm music), `mood`, and a one-line `feel` (the plain music situation Step 3 matches a template against). Only classify and lay out here: leave every frame's `### Groups` as `TBD (Step 3)` and the frontmatter `style` blank — no templates, copy, color, or fonts. Expect ~1–6 frames.

**Gate:** frames tile the track (first at 0, last at `duration_s`); each carries `span_sec` + `pacing` + `mood` + `feel`; every `### Groups` is `TBD`; no content anywhere.

---

## Step 3: Fill the plan (user-gated)

Goal: Turn the skeleton into an approved, complete `STORYBOARD.md`.

Read [`references/planning.md`](references/planning.md), [`storyboard-format.md`](references/storyboard-format.md), [`template-catalog.md`](references/template-catalog.md), [`motion-primitive-catalog.md`](references/motion-primitive-catalog.md), and [`montage.md`](references/montage.md) (only if the user supplied assets). Editing the same file in place, do two things:

When a bounded section intentionally accelerates, overloads, or ruptures before a release, also read `../hyperframes-creative/references/fast-paced-editing.md`. Record its orient/baseline → compression/escalation → peak → release/reorientation directly in the existing frame/group plan, with every phase boundary snapped to an `audiomap.json` anchor. `audiomap.json` remains the sole clock; do not add a parallel fast-edit timing file. A generally upbeat track does not automatically admit a fast passage.

1. **Pick the brand.** Choose one preset from `../hyperframes-creative/frame-presets/` using the table in `../hyperframes-creative/references/design-spec.md` (match the track's mood; **only its fonts and colors matter** — templates own composition). Copy it into `frame.md` **unmodified** and fill the frontmatter `style` (font + a ≤4–6 swatch palette) from it.
2. **Fill every frame.** Decide its groups and give each a treatment: a matched template from the catalog (with bound params and real audiomap anchors), a free-compose from the primitive catalog, or an asset treatment that **obeys `pacing`**. Write the copy. You own WHAT (template / primitives + content + anchors); the frame-worker owns HOW — **never write millisecond tweens into the storyboard**.

```bash
node <SKILL_DIR>/scripts/validate-plan.mjs --storyboard "$PROJECT_DIR/STORYBOARD.md" \
  --audiomap "$PROJECT_DIR/audiomap.json" --templates <SKILL_DIR>/references/templates
```

Fix every `✗` (hard errors: duration mismatch, frames not tiling the track, a missing `src`); warnings are best-effort. Then show the user a frame-by-frame summary and iterate until they approve.

**Gate:** `frame.md` is a verbatim preset copy; `validate-plan.mjs` exits 0; every admitted fast passage has an audiomap-anchored baseline/escalation/peak/release, focal path, primary family, and luminance restraint; the user approved the plan.

---

## Step 4: Build frames from the plan

Goal: Build every frame as a self-contained composition file.

Create `compositions/frames/`. Read [`sub-agents/frame-worker.md`](sub-agents/frame-worker.md) and `../hyperframes-core/references/subagent-dispatch.md`. Dispatch **one frame-worker per frame**, in parallel where possible (otherwise in waves). Each worker gets exactly one frame and this context:

```text
PROJECT_DIR: <abs path>
frame_id: <NN-frame_id>              # = the frame file stem, e.g. 02-f2; the composition id
Your block: the `## Frame N — <frame_id>` block in PROJECT_DIR/STORYBOARD.md
audiomap: PROJECT_DIR/audiomap.json
frame.md: PROJECT_DIR/frame.md
Materials: for each group, <SKILL_DIR>/references/templates/<id>/index.html (templates) and
           <SKILL_DIR>/references/motion-primitives/<id>/ (free); staged assets/ (asset groups)
Contracts: ../hyperframes-core/references/sub-compositions.md + determinism-rules.md
Canvas: <w>×<h>   Pacing: <beat_cut|phrase_flow>
Fast passage: <none | shared audiomap-anchored arc + this frame/group's exact role, receiver, and handoff>
Write to: PROJECT_DIR/compositions/frames/<frame_id>.html
```

The worker forks the cited materials, converts every anchor to frame-local seconds (`local_t = track_t − span_sec[0]`), gates its groups with 0ms cuts, and writes one seek-safe frame file. **The worker never runs the `hyperframes` CLI** — those commands operate on the assembled project, which doesn't exist yet, so they'd report on the wrong files. The worker just writes to the contract and stops; you verify after assembly (Step 6). As each worker returns, you can confirm its file landed on disk.

**Gate:** every frame has its `compositions/frames/NN-*.html` on disk.

---

## Step 5: Assemble

Goal: Wire the built frames + BGM into the playable `index.html`.

`assemble-index.mjs` is deterministic — no subagent, no judgment. It references each frame file at its cumulative `data-start`, mounts `assets/bgm.mp3` on track 11, and hard-cuts frame → frame (frames tile the track with no gaps, so there is **no transition injector**).

```bash
node <SKILL_DIR>/scripts/assemble-index.mjs --storyboard "$PROJECT_DIR/STORYBOARD.md" \
  --hyperframes "$PROJECT_DIR" --audiomap "$PROJECT_DIR/audiomap.json"
```

Fix any `✗` it reports — a missing or blank frame file means that worker wrote a partial file; re-dispatch it (Step 4) and re-assemble.

**Gate:** `index.html` exists; total duration == `audiomap.audio.duration_sec`.

---

## Step 6: Verify and render

Goal: Verify the assembled video, get user approval, and render the final MP4.

Run the CLI on the **assembled project** — that's the correct unit (the per-frame workers couldn't run it). `lint` checks structure, `validate` runs headless Chrome (catching JS errors and missing assets), `inspect` snapshots frames.

```bash
( cd "$PROJECT_DIR" && npx hyperframes lint . && npx hyperframes validate . && npx hyperframes inspect . )
```

Inspect at `t=0`, each frame start, the strongest DROP / SURGE, every `hard_stops[].t`, and the final frame. On failure, make the **cheapest safe fix** yourself: edit the offending `compositions/frames/NN-*.html`. Never change duration or audio timing to hide a sync issue. Once the gates pass, pause for user review, then render only on approval:

For each admitted fast passage, preview the complete audiomap-anchored lead-in through release at final fps with the track. Confirm the peak grows from a readable baseline, the eye follows one focal path, any deliberate disorientation resolves, and full-frame luminance/color changes do not become repeated strobe grammar. Still inspection is not sufficient.

```bash
( cd "$PROJECT_DIR" && npx hyperframes render . --skill=music-to-video -q draft -o renders/video.mp4 --fps 30 )
```

After rendering, replay those same windows from the encoded MP4 with final audio. Fix, rerender, and rewatch any failed arc; source preview alone does not approve the master.

**Gate:** `lint` / `validate` / `inspect` passed; every admitted fast passage passed source and encoded full-motion review; the user approved; `renders/video.mp4` exists with audio, duration == `audiomap.audio.duration_sec`. The final reply states the MP4 path and duration.

---

## Resume table

| You have                   | Continue from |
| -------------------------- | ------------- |
| `assets/bgm.mp3` only      | Step 1        |
| `audiomap.json`            | Step 2        |
| `STORYBOARD.md` (skeleton) | Step 3        |
| `STORYBOARD.md` (complete) | Step 4        |
| all frame files            | Step 5        |
| `index.html`               | Step 6        |

## Quick Reference

**Formats:** landscape `1920x1080` by default; portrait `1080x1920`; square `1080x1080`. Set the canvas once in the storyboard frontmatter (`canvas: { w, h, fps }`).

**Scripts** under `scripts/`: `analyze-beatgrid.py` (the one analyzer), `validate-plan.mjs` (plan check), `assemble-index.mjs` (index assembly), `stage-assets.mjs` (stage user media), `lib/storyboard.mjs` (vendored parser). Everything else is the `hyperframes` CLI.

| Read                                                                                                           | When                                                    |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| [`references/frame-skeleton.md`](references/frame-skeleton.md)                                                 | Step 2: read the music, lay out the frames, set pacing  |
| [`references/planning.md`](references/planning.md) · [`storyboard-format.md`](references/storyboard-format.md) | Step 3: pick the brand, fill each frame, write the plan |
| [`references/template-catalog.md`](references/template-catalog.md)                                             | Step 3: pick a template per group                       |
| [`references/motion-primitive-catalog.md`](references/motion-primitive-catalog.md)                             | Step 3/4: L0 recipes for free-compose                   |
| [`references/montage.md`](references/montage.md)                                                               | Step 3/4: asset treatments (beat-cut / ken-burns)       |
| [`sub-agents/frame-worker.md`](sub-agents/frame-worker.md)                                                     | Step 4: dispatch + build one frame                      |
| `../hyperframes-core/references/subagent-dispatch.md`                                                          | Step 4: dispatch sub-agents safely                      |
| `../hyperframes-creative/references/design-spec.md`                                                            | Step 3: pick the preset (the brand)                     |
| `../hyperframes-creative/references/fast-paced-editing.md`                                                     | Steps 3–6: direct/review bounded acceleration or rupture |

## Directory layout

```
music-to-video/
  SKILL.md
  references/   frame-skeleton.md · planning.md · storyboard-format.md
                template-catalog.md · motion-primitive-catalog.md · montage.md
                templates/<id>/          { index.html (+ assets/ · program.json) }  ← L1 catalog impls
                motion-primitives/<id>/  { index.html } (+ ../assets/gsap.min.js shared by recipes) ← L0 catalog impls
  scripts/      analyze-beatgrid.py · assemble-index.mjs · validate-plan.mjs · stage-assets.mjs · lib/storyboard.mjs
  sub-agents/   frame-worker.md   ← the one subagent (one per frame)
```
