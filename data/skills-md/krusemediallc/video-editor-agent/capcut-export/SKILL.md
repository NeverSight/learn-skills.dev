---
name: capcut-export
description: >
  Export a finished layered edit (footage + graphic cards + alpha fx overlay + captions
  + SFX/music/VO) into a CapCut desktop draft where EVERY element stays editable —
  footage segments split at zoom boundaries, per-card graphic clips, a true-alpha fx
  overlay, native text captions, per-hit SFX clips, and separate music/VO tracks. Use
  when someone says "export to CapCut", "make this editable in CapCut", "CapCut draft",
  "hand the edit off to a human editor", "open my render in CapCut with layers", or
  mentions pyJianYingDraft / JianYing drafts / draft_content.json / draft_info.json /
  root_meta_info.json. Builds the draft via pyJianYingDraft, then applies a
  work-in-progress schema patch for modern CapCut (~181.x) and registers the draft.
  NOT for rendering the video itself (that is the edit skill's job) — this consumes an
  already-finished layered edit and its render passes.
---

# CapCut Export

Turn a finished layered edit into a CapCut desktop draft where an editor can grab any
element — nudge a caption, swap a card, mute one SFX hit — instead of receiving a baked
MP4.

**Honest status up front:** the draft *generation* works and is well understood. The
*"modern CapCut opens it"* step is a documented work-in-progress. pyJianYingDraft writes
JianYing-era drafts; current CapCut desktop expects a newer schema. Before the patch
described below, CapCut refused the draft with **"Couldn't use project: unusual path"**.
The patch is implemented in the script but **has not been field-verified end to end** on
a current CapCut build. Treat the last mile as debugging work, not a guaranteed one-shot
(see [Debugging](#debugging) — the method is a diff against a native draft).

## Prerequisites

- macOS with CapCut desktop installed (drafts live in
  `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/`).
- `python3` with **pyJianYingDraft in a venv** (`pip install pyJianYingDraft`). Do not
  install globally; the library moves fast and its API varies between versions.
- `ffmpeg` on PATH (or `FFMPEG` env var) — used to split the cards render pass and grab
  a cover thumbnail.
- Optional: PIL (`pip install pillow`) if you want the procedural vignette PNG.
- The finished edit's **render passes** (see next section). Rendering those is the edit
  skill's job, not this skill's.

## Inputs — what the edit pipeline must hand you

| Input | What it is |
|---|---|
| Base footage file(s) | The talking-head / footage video (already reframed to canvas aspect) |
| Cards-only pass | A render of the composition with **only the graphic cards** visible (opaque background is fine — cards are stacked as opaque clips) |
| Alpha fx pass | Everything that must composite over footage with transparency (progress bar, light leaks). Render with `--format mov` → **true-alpha ProRes, `yuva444p`**. An MP4 cannot carry alpha |
| Word-level transcript | JSON `[{"text","start","end"},...]` for native captions |
| VO / music / SFX files | The exact audio used in the edit, one file per SFX hit name |
| The edit's timing data | Zoom boundaries, card in/out times, SFX hit list, caption style beats — copied into the script's CONFIG block |

## Workflow

1. **Copy the template** `scripts/export-capcut-template.py` into the edit's project
   folder and fill in the CONFIG block (durations, cards, hits, caption windows).
2. **Stage media to the local disk.** The script does this automatically into
   `~/Movies/capcut-export-media` (override with `CAPCUT_MEDIA_DIR`). This is not
   optional tidiness: media referenced by a draft from an **external volume can trip
   macOS permission (TCC) prompts inside CapCut** and break media resolution. Keep
   every referenced file on the boot disk.
3. **Build the draft:** `.venv/bin/python export-capcut-template.py` — writes the draft
   to `~/Movies/capcut-draft-staging/<name>/`.
4. **Patch the schema** (see below): rerun with
   `--skip-build --patch-native <path-to-a-native-draft-folder>`.
5. **Quit CapCut completely (Cmd+Q)**, then `--skip-build --install --register`.
6. Open CapCut. If the draft opens: verify tracks, done. If not: [Debugging](#debugging).

## The schema gap (read this before blaming your CONFIG)

pyJianYingDraft targets the **JianYing** (Chinese CapCut) draft format:

- writes `draft_content.json` with `new_version: "110.0.0"`.

Current CapCut desktop (international) loads **`draft_info.json`** with
`new_version` ≈ **`"181.0.0"`** and **8 extra top-level keys** that the old schema
lacks:

```
draft_type, function_assistant_info, is_drop_frame_timecode, lyrics_effects,
mixed_track_mode_on, path, smart_ads_info, uneven_animation_template_info
```

The fix implemented in `--patch-native`:

1. On the **target machine**, create any throwaway project in CapCut natively (this
   gives you a draft written by that exact CapCut build).
2. Clone those 8 keys from the native draft into the generated draft; copy the native
   `new_version` / `version` fields; set `path` to the draft's final installed folder.
3. Write the result as **BOTH filenames** — `draft_content.json` *and*
   `draft_info.json` — so either loader path finds it.

Status, plainly: before this patch CapCut showed "Couldn't use project: unusual path";
the patched draft **was not yet verified to open** on the CapCut build that produced
the error. Expect to iterate via the diff method below.

## Draft installation and the registry

Copying the folder into `com.lveditor.draft/` is not enough — CapCut only lists drafts
that are **registered in `root_meta_info.json`** (top-level key `all_draft_store`).

Rules the script enforces / you must respect:

- **Back up `root_meta_info.json` first** (script writes a timestamped `.bak-*`).
- **Only edit the registry while CapCut is fully quit** — CapCut rewrites it on exit
  and will clobber (or crash on) concurrent edits. The script refuses to run
  `--install`/`--register` while a CapCut process exists.
- New entries are made by **cloning a native entry** and fixing: `draft_name`, every
  path field containing the old name, a fresh uppercase-UUID `draft_id`, `tm_duration`
  (microseconds), timestamps, and `draft_cover` (the script grabs a frame with ffmpeg
  as `draft_cover.jpg`).

## Track layout — mapping a layered edit onto CapCut tracks

Bottom → top:

| Track | Content | Technique |
|---|---|---|
| `footage` | Base video | **Split at every zoom boundary**; each segment gets its own `scale_x/scale_y` in `ClipSettings` — that's how a punch-in stays editable |
| `overlay` | Positioned second video (e.g. a head-card band during split-screen beats) | `ClipSettings(scale_x, scale_y, transform_y)`. **Negative `transform_y` = down**, positive = up (e.g. `-0.5625` parks a 0.9556-scale band in the lower half of 9:16) |
| `cards` | One opaque clip per graphic card | Render a cards-only pass of the composition, then **ffmpeg-split it at card boundaries** (`-crf 16 -g 15` keeps cuts frame-accurate). Editors can retime/swap individual cards |
| `fx` | ONE alpha overlay for the whole timeline | The true-alpha ProRes `.mov`. Don't split it — it's a single ambient layer |
| `image-N` | Static PNGs (vignette etc.) | PNG placed as image segments over specific windows |
| `captions` | Native `TextSegment`s | `TextStyle(size, bold, italic, color)`, `TextBorder(width, color)`, position via `ClipSettings(transform_y=...)`. Fully editable text in CapCut |
| `text-N` | CTAs / keyword pops | Same as captions, on extra tracks |
| `vo`, `music`, `sfx-N` | Audio | One clip per SFX hit so each hit is individually mutable/movable |

### Text-track hard rules

- **A track cannot hold overlapping segments.** Two texts on screen at once must go on
  **separate tracks** — the script packs extra texts greedily onto `text-1`, `text-2`, …
- **Clamp caption windows strictly monotonic.** Word-level timestamps from a
  transcriber routinely overlap; the script forces
  `start ≥ prev_end + 2ms` and `end ≤ next_start − 40ms` before creating segments.
  Skip this and `add_segment` throws (or worse, CapCut mis-renders).

### pyJianYingDraft API gotchas

- **Clamp every segment duration to the material duration** —
  `d = min(d, material.duration/1e6 - source_start)` — or the library throws.
  `material.duration` is in **microseconds**.
- `VideoSegment(material, target_timerange, source_timerange=…, volume=…,
  clip_settings=…)` — `source_timerange` selects which slice of the file plays;
  omit it for stills/full clips.
- `TextStyle(italic=…)` doesn't exist in every version — wrap in
  `try/except TypeError` and degrade to non-italic (the script does).
- Time ranges are built with `trange("12.5s", "0.8s")` (start, duration).

## Debugging

When CapCut refuses or mangles the draft, the method is a **diff against a native
draft made by that exact CapCut install**:

1. In CapCut, create a minimal native project: one video clip, one text, one audio.
   Quit CapCut.
2. Pretty-print both drafts and diff:
   `python3 -m json.tool <native>/draft_info.json > a.json` (same for yours), then
   diff top-level keys first, then per-track/per-segment structure.
3. Fix the highest-level differences first (missing keys, version strings, `path`),
   reinstall, retest. Iterate downward into track/material structure only if the
   draft opens but elements are broken.
4. Registry problems look different from schema problems: a draft that never appears
   in the project list = registry; a draft that appears but errors on open = schema.
5. If CapCut "repairs" your draft on open, immediately copy the repaired
   `draft_info.json` out and diff it against what you wrote — CapCut just told you
   the correct schema.

## Scripts

- `scripts/export-capcut-template.py` — the full exporter template. CONFIG block at
  top; `--patch-native`, `--install`, `--register`, `--skip-build` flags. Read its
  docstring before running.
