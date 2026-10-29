---
name: video-edit-compare
description: Use when a completed cut-as-code delivery needs a strict side-by-side review against its original source, including cuts, varispeed, color grade, and graphics.
---

# Video Edit Compare

Render the single V1 comparison mode: `original-vs-final-source-time`.

The left panel plays the original continuously. The right panel projects actual final-delivery pixels back onto the original source clock. Dropped ranges are black, kept final ranges are stretched to their source duration, and audio is copied from the original.

## Dependencies

Require `ffmpeg`/`ffprobe` on PATH and Python with `Pillow`. Check them before processing media.

## Inputs

- `work/timeline.json`: canonical chronological source-to-program mapping
- `input/original-video.mp4`: original source
- `final/final-video.mp4`: actual delivery after all selected edits

Do not compare against a cut plan or an intermediate render. The final pixels are required so the review includes grade and cards.

## Render

```text
python scripts/make_compare.py TIMELINE.json SOURCE.mp4 FINAL.mp4 OUT.mp4 [--filter-only]
```

Project example:

```powershell
python skills/video-edit-compare/scripts/make_compare.py `
  work/timeline.json `
  input/original-video.mp4 `
  final/final-video.mp4 `
  review/04-edit-compare/original-vs-final-source-time.mp4
```

The script always writes the durable `work/edit-compare/compare-plan.json`. It writes PIL
label images and the generated filtergraph under disposable `work/cache/`.
`--filter-only` creates the plan and inspectable cache files without rendering the video.

## Mapping Rules

- Keep source clips chronological, non-overlapping, and single-source.
- Trim each clip's `program_range` from the final video.
- Stretch it by the clip speed to recover its `source_range` duration.
- Insert black for every source-time gap.
- Map the original audio without retiming it.
- Derive every part's start and end frame from its absolute source-time boundaries, then
  trim to that frame count and rebuild PTS at the timeline's rational FPS. Never round each
  part duration independently; cumulative concat rounding causes source-time drift.

Reordered, duplicated, overlapping, nonlinear-speed, or multi-source timelines are unsupported in V1 and must fail validation.

## Verify

After rendering, the script automatically checks the complete output:

- duration equals `source_duration_s` within one frame;
- output width is twice the source width;
- every dropped-range sample is black on the right;
- kept-range samples match the corresponding final program frames;
- original audio remains continuous and on the source clock.

On success it writes `review/04-edit-compare/comparison-summary.md` with a passing
verification result. When `work/project.json` exists, it also adds or refreshes the
`original-vs-final-source-time` review node, records exact active operation revisions in
`based_on`, and refreshes `START-HERE.md`. Do not create a separate checks manifest.

This comparison is a review deliverable, not a default preview. Generate it after the final render exists.
