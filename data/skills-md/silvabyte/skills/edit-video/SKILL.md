---
name: edit-video
description: |
  Conversational video editing: transcribe, plan edits using transcript analysis, and render. Use when:
  (1) User wants to edit a video by reviewing its transcript
  (2) User asks to trim, cut, or rearrange video segments
  (3) User wants to create a highlight reel or narrative cut from a longer video
  (4) User mentions EDL, transcript analysis, or video editing workflow
  (5) User wants to remove filler, dead air, or silence from a video
  (6) User wants to combine multiple clips into one video
  Triggers: "edit video", "transcribe video", "trim video", "cut video", "EDL", "video editing", "remove filler", "combine videos", "stitch clips", "multiple clips", "add captions", "shorts captions", "burn captions"
---

# Edit Video

Conversational video editing in three phases: transcribe, plan the edit, render.

## Prerequisites

- **bun** — TypeScript runtime
- **ffmpeg** / **ffprobe** — video processing (must be on PATH)

Environment variables (optional, have defaults):

| Variable | Purpose | Default |
|----------|---------|---------|
| `AUDETIC_API_URL` | Audetic transcription service URL | `https://audio.audetic.link` |

## Commands

All paths are relative to this skill's directory. Run with `bun run`.

| Command | Purpose |
|---------|---------|
| `scripts/transcribe.ts <video>` | Transcribe a single video file — produces JSON + markdown transcript + analysis alongside the file |
| `scripts/transcribe.ts <directory>` | Transcribe all video files in a directory — produces merged JSON + markdown transcript + analysis in the directory |
| `scripts/preview.ts <edl.json>` | Validate and preview an EDL before rendering |
| `scripts/render.ts <edl.json>` | Render final video from EDL using ffmpeg stream copy |
| `scripts/caption.ts <video> <transcript.json>` | Burn Shorts-style captions into video (optional `--edl`, `--output`) |

## Workflow — Single File

### 1. Transcribe

```bash
bun run scripts/transcribe.ts <video-file>
```

Compresses audio to MP3, uploads to the audetic transcription service, and produces three files alongside the video:
- `.json` — transcription result (used by tools)
- `-transcript.md` — readable transcript table
- `-analysis.md` — transcript with signal flags (gaps, speech rate)

### 2. Plan the Edit

Read both the transcript and the analysis. The analysis provides mechanical signals:

| Flag | Meaning |
|------|---------|
| `gap:Xs` | Silence of X seconds before this segment |
| `slow` | Fewer than 0.5 words/second (typing, long pauses, dead air) |
| `silence` | Zero words detected in segment |
| WPS column | Words per second (higher = denser speech) |

See [references/signal-interpretation.md](references/signal-interpretation.md) for detailed signal guidance.

Use these signals combined with your understanding of the content to decide what to keep/cut. The tool detects silence and pacing; you judge what's filler vs. substance.

When the edit plan is decided, write an EDL (Edit Decision List) JSON file:

```json
{
  "output": "/absolute/path/to/output.mp4",
  "segments": [
    { "source": "/absolute/path/to/video.mp4", "start": "00:00:00.000", "end": "00:02:15.500", "label": "Introduction" },
    { "source": "/absolute/path/to/video.mp4", "start": "00:05:30.000", "end": "00:12:45.200", "label": "Main discussion" }
  ]
}
```

- Each segment requires a `source` field with the absolute path to its source video
- Timestamps must be `HH:MM:SS.mmm` format (ffmpeg-native)
- Segments are in playback order — rearranging segments reorders the output
- `label` is optional, helps communicate what each segment is
- Only included segments appear in the output; everything else is cut

See [references/edl-schema.md](references/edl-schema.md) for the full schema reference.

### 3. Preview

```bash
bun run scripts/preview.ts <edl.json>
```

Always preview before rendering. Shows segment breakdown, kept/cut percentages, and validates the EDL.

### 4. Render

```bash
bun run scripts/render.ts <edl.json>
```

Uses ffmpeg stream copy (fast, cuts at nearest keyframe). Produces the final video.

### 5. Caption (Optional)

```bash
bun run scripts/caption.ts <edited-video.mp4> <transcript.json> --edl <edl.json>
```

Burns bold, centered captions (Hormozi style) into the video. Use `--edl` to remap transcript times to the edited video's timeline. Requires a full re-encode.

See [references/caption-style.md](references/caption-style.md) for style defaults and customization.

## Workflow — Multiple Clips (Directory)

Use this when the user has multiple short clips that should be edited into a single video.

### 1. Transcribe All Clips

```bash
bun run scripts/transcribe.ts <directory>
```

Finds all video files (`*.mp4`, `*.mkv`, `*.mov`, `*.webm`, `*.ts`), transcribes each one, and produces merged output in the directory:
- `transcript.json` — merged transcript with `source` field on each segment
- `transcript.md` — merged readable table with Source column
- `analysis.md` — merged analysis with Source column (gap detection resets at clip boundaries)

### 2. Plan the Edit

Same process as single-file, but the transcript and analysis include a Source column showing which clip each segment came from. Write an EDL with per-segment `source` paths:

```json
{
  "output": "/absolute/path/to/combined.mp4",
  "segments": [
    { "source": "/absolute/path/to/clip001.mp4", "start": "00:00:02.000", "end": "00:00:12.000", "label": "Opening" },
    { "source": "/absolute/path/to/clip003.mp4", "start": "00:00:00.000", "end": "00:00:08.500", "label": "Key moment" },
    { "source": "/absolute/path/to/clip007.mp4", "start": "00:00:01.000", "end": "00:00:14.000", "label": "Closing" }
  ]
}
```

### 3. Preview + Render

Same as single-file workflow. Preview lists all sources with durations and shows source filename per segment.

### 4. Caption (Optional)

Same as single-file — run `caption.ts` with `--edl` on the rendered output.

## Narrative Editing

Use narrative editing when the user provides a goal beyond "trim the filler" — a theme, tone, target duration, or audience.

See [references/narrative-patterns.md](references/narrative-patterns.md) for the full pattern catalog.

**Thinking process:**
1. Read transcript + analysis. Identify distinct *moments* / content beats.
2. Decide which moments serve the stated narrative goal.
3. Determine the best *order* — chronological is one option, but also consider: Hook-first, Escalation, Question-answer, Bookend.
4. Label each segment with its narrative role.
5. Sum segment durations to verify against target.

**Labels as narrative roles:** Use the `label` field to document function (e.g., `"HOOK: the punchline"`, `"SETUP: context"`, `"PAYOFF: resolution"`).

**Narrative notes:** Use the optional `narrative_notes` field in the EDL to document editorial reasoning.

Example:
```json
{
  "output": "/path/to/output.mp4",
  "narrative_notes": "Goal: 60s punchy clip. Led with the reaction for hook, then backed into the setup.",
  "segments": [
    { "source": "/path/to/video.mp4", "start": "00:05:30.000", "end": "00:05:55.000", "label": "HOOK: surprised reaction" },
    { "source": "/path/to/video.mp4", "start": "00:01:00.000", "end": "00:02:15.500", "label": "SETUP: reading the tweet" },
    { "source": "/path/to/video.mp4", "start": "00:06:00.000", "end": "00:06:30.000", "label": "PAYOFF: final take" }
  ]
}
```

## Output File Naming

### Single-file mode

The `outputPaths` function in `scripts/lib/config.ts` generates standard paths relative to the video:

| Output | Pattern |
|--------|---------|
| Transcript JSON | `<name>.json` |
| Transcript MD | `<name>-transcript.md` |
| Analysis MD | `<name>-analysis.md` |
| EDL | `<name>-edl.json` |
| Edited video | `<name>-edited.mp4` |
| Captioned video | `<name>-captioned.mp4` |

### Directory mode

The `directoryOutputPaths` function generates paths inside the directory:

| Output | Pattern |
|--------|---------|
| Transcript JSON | `transcript.json` |
| Transcript MD | `transcript.md` |
| Analysis MD | `analysis.md` |

## Session Flow

### Single file

1. User provides a video file path
2. Run `transcribe.ts` on it
3. Read the `-analysis.md` and `-transcript.md` files
4. Discuss with user what to keep/cut (or accept a narrative goal)
5. Write the EDL JSON file (each segment has `source` pointing to the video)
6. Run `preview.ts` to validate — review with user
7. Run `render.ts` to produce the final video
8. (Optional) Run `caption.ts` with `--edl` if user wants Shorts-style captions
9. Report output path and final duration

### Multiple clips

1. User provides a directory of clips
2. Run `transcribe.ts` on the directory
3. Read the merged `analysis.md` and `transcript.md` in the directory
4. Discuss with user which clips/segments to include
5. Write the EDL JSON file (each segment has `source` pointing to its clip)
6. Run `preview.ts` to validate — review with user
7. Run `render.ts` to produce the combined video
8. (Optional) Run `caption.ts` with `--edl` if user wants Shorts-style captions
9. Report output path and final duration

## Tips

- **Keyframe imprecision**: Stream copy cuts at the nearest keyframe, so cuts may be off by up to ~0.5s. This is the tradeoff for fast rendering without re-encoding.
- **Large videos**: Transcription time scales with video length. For videos over 30 minutes, warn the user it may take a while.
- **Always preview first**: Never render without previewing. The preview catches validation errors and lets the user confirm before committing.
- **Duration targeting**: When given a target duration, sum the `Dur` column values from the analysis for selected segments. Iterate until the EDL fits.
- **Reinterpret signals**: Gaps aren't just cut candidates — they mark topic boundaries. Slow segments aren't always boring — a pause before a realization can be dramatic.
- **Mixed codecs**: When combining clips from different sources, the preview tool warns about mixed file extensions. Clips from the same device/app are usually safe.
- **Caption re-encoding**: Burning captions requires a full video encode (not stream copy), so it takes longer than rendering. Mention this to the user before starting.
- **Offer captions**: When the user mentions Shorts, Reels, TikTok, or short-form content, offer to add Shorts-style captions after rendering.
