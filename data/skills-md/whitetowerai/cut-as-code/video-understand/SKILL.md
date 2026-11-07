---
name: video-understand
description: Use when a video project needs reusable media metadata, word-level transcription, objective speech analysis, or evidence-backed semantic understanding before optional editing skills run.
---

# Video Understand

Build the shared evidence layer once. Keep observations in source time and leave editorial decisions to downstream skills.

This skill is a prerequisite for `/video-cut`, `/video-to-shorts`,
`/video-add-captions`, `/video-add-content-cards`, and `/video-add-motion-graphics`.
Run it first so those skills consume the same validated evidence and timeline.

## Dependencies

Require `ffmpeg`/`ffprobe`, Python, and `faster-whisper` for transcription. Check them before processing media.

## Workflow

1. Initialize a project from the original source:

   ```powershell
   python scripts/init_project.py path/to/source.mp4 path/to/my-video-project
   ```

   This creates `input/`, `review/00-video-understanding/`, `final/`, the minimal
   machine-facing `work/` tree, an identity timeline, `project.json`, media facts, and
   `START-HERE.md`. It does not create folders for unselected edit operations.

2. Probe again only when the source needs an explicit metadata refresh:

   ```powershell
   python scripts/probe.py input/original-video.mp4 work/understand/media.json
   ```

3. Extract 16 kHz mono audio and transcribe it:

   ```powershell
   ffmpeg -y -i input/original-video.mp4 -ac 1 -ar 16000 work/cache/audio16k.wav
   python scripts/transcribe.py work/cache/audio16k.wav work/understand/transcript medium `
     --lang auto --cache-dir work/cache/faster-whisper
   ```

   Use `--lang auto` for unknown or mixed-language speech. Never infer the spoken language
   from the language of the user's prompt. Pass a fixed language such as `--lang zh` only
   when the audio itself or explicit user metadata establishes it. Keep model downloads in
   the project-local `work/cache/faster-whisper/` cache. Faster-whisper may emit an
   occasional point-timed word with equal start/end values; the shared timeline mapper
   preserves it as a 1 ms interval so captions and derivatives do not silently lose text.

4. Generate objective metrics and semantic candidates:

   ```powershell
   python scripts/analyze.py work/understand/transcript.json work/understand/analysis.json
   ```

5. Read the source, transcript, and analysis. Author `work/understand/understanding.json` with factual summaries, source-time ranges, confidence, and transcript evidence. Do not prescribe cuts, cards, or looks.

6. Validate before downstream use:

   ```powershell
   python scripts/validate.py understanding work/understand/understanding.json work/understand/transcript.json
   ```

7. Create only these useful review artifacts under `review/00-video-understanding/`:
   `video-summary.md`, `transcript.srt`, and `contact-sheet.jpg`. Verify metadata,
   timestamps, evidence references, and visible frames. Do not substitute PNG or ad hoc
   filenames for the protocol names.

8. Mark the understanding operation `check.status` as `pass` only after the review artifacts
   and semantic evidence validate. Operation lifecycle `status` and check result are separate;
   never write `verified` into `check.status`.

## Contracts

- Read [project-schema.md](reference/project-schema.md) when creating or validating `project.json`.
- Read [timeline-schema.md](reference/timeline-schema.md) when mapping source and program time.
- Read [understanding-schema.md](reference/understanding-schema.md) before authoring semantic understanding.
- Use [understanding.example.json](examples/understanding.example.json) as a compact example.

All durable machine files live in `work/understand/`. Treat `work/cache/` as disposable.
