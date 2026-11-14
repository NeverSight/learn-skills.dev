---
name: clipclipskill
description: Token-efficient long-video clipping skill with a hardcoded workflow and resumable state machine that probes video metadata, generates transcript-driven clip plans, renders clips, and outputs publishing copy for short-video operations.
---

# clipclipskill

Use this skill when the user wants to turn a long video into short clips.

## Required behavior

1. Always ask for:
   - either a local video path or a source URL
   - content template
   - length preference
   - whether Whisper-first transcription should be used
   - whether speaker diarization should be used or auto-decided
   - if URL is used, ensure it is from YouTube or Bilibili
2. Always run metadata probe before transcription.
3. Always report duration, size, audio presence, and estimated processing time.
4. Always require explicit user confirmation of template and strategy before transcription.
5. Always require explicit user confirmation of the clip plan before rendering.
6. Always run a final validation step after ops generation and before marking the job completed.
7. Always persist state in `<workspace-dir>/<job_id>/status.json`.
8. Always prefer resuming from existing artifacts when available.
9. Before each command runs, check that the required local tools and Python dependencies are installed.
10. Never create job folders under system directories by default; always use the user-provided workspace directory.
11. Support binding a default workspace directory so later commands do not need to repeat it.

## Canonical flow

1. Either bind a default output directory with `clipclipskill bind-workspace /path/to/output`, or pass `--workspace-dir /path/to/output`.
2. `clipclipskill start-job ...`
3. `clipclipskill probe --job-id <job_id>`
   - for URL sources, this step downloads the video into the job workspace before probing
4. Stop and ask user to confirm template and strategy.
5. `clipclipskill confirm-template --job-id <job_id> ...`
6. `clipclipskill transcribe --job-id <job_id>`
7. `clipclipskill plan --job-id <job_id>`
8. Stop and ask user to confirm the proposed clip plan.
9. `clipclipskill approve-plan --job-id <job_id>`
10. `clipclipskill render --job-id <job_id>`
11. `clipclipskill ops --job-id <job_id>`
12. `clipclipskill validate --job-id <job_id>`

## Output expectations

Final deliverables live under `<workspace-dir>/<job_id>/` and include:
- `status.json`
- `planning_package/clip_plan.v1.json`
- `planning_package/clip_artifacts/<topic>_<seq>.srt`
- `planning_package/clip_artifacts/<topic>_<seq>.json`
- `clips/<topic>_<seq>.mp4`
- `ops/operations_manual.md`
- `ops/publish_manifest.json`

Rules:
- `clips/` only stores final mp4 deliverables.
- Per-clip intermediate files like subtitle and manifest stay in `planning_package/clip_artifacts/`.
- Ops output stays consolidated under `ops/` instead of being duplicated per clip.
- `ops/operations_manual.md` is the single Markdown operations handoff, covering release intro and risk notes for each clip.
- Final completion requires a validation pass recorded in `status.json`.
- Validation must reject off-topic copy, leaked process/thinking text, and filename-oriented wording in deliverable copy.
- Validation must check rendered clips for playback integrity issues such as missing audio, invalid frame rate, invalid duration, or ffprobe-level signs of broken exports.
