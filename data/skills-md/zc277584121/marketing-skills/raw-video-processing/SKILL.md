---
name: raw-video-processing
description: Post-process raw screen recordings by removing silent segments and applying speed adjustments. Uses FFmpeg-based Python scripts to optimize video pacing automatically.
---

# Skill: Raw Video Processing

Post-process raw screen recordings to improve pacing — remove silent segments, then speed up the result.

> **Prerequisite**: FFmpeg and Python 3 must be installed.

---

## When to Use

The user has recorded a screencast and wants to clean it up before publishing. Typical issues in raw recordings:
- Long pauses / dead air while thinking or waiting for loading
- Overall pacing feels slow and could benefit from a slight speed boost

---

## Default Workflow

When the user provides a raw video file, **run both scripts in sequence** by default:

### Step 1: Remove Silent Segments

```bash
python /path/to/skills/raw-video-processing/scripts/remove_silence.py <input.mp4>
```

This detects and cuts out silent portions, producing `<input>_nosilence.mp4`.

**Default parameters** (good for most screencasts):
- `--threshold -30dB` — silence detection sensitivity
- `--duration 0.8` — minimum silence length (seconds) to remove
- `--padding 0.2` — seconds of breathing room kept around speech boundaries

The script prints a detailed summary: number of silent segments found, total silence removed, and all kept segments with timestamps. Review this output to confirm the result looks reasonable.

### Step 2: Speed Up the Video

```bash
python /path/to/skills/raw-video-processing/scripts/speed_video.py <input>_nosilence.mp4
```

This applies a speed multiplier to the silence-removed video, producing `<input>_nosilence_1.2x.mp4`.

**Default parameters**:
- `--speed 1.2` — 1.2x playback speed (a subtle boost that doesn't feel rushed)

---

## Script Options

### remove_silence.py

| Flag | Default | Description |
|------|---------|-------------|
| `-o`, `--output` | `<input>_nosilence.mp4` | Custom output path |
| `-t`, `--threshold` | `-30dB` | Silence threshold in dB (lower = more sensitive) |
| `-d`, `--duration` | `0.8` | Minimum silence duration in seconds to remove |
| `-p`, `--padding` | `0.2` | Padding kept around non-silent segments |
| `--dry-run` | off | Only print detected segments, don't export |

### speed_video.py

| Flag | Default | Description |
|------|---------|-------------|
| `-o`, `--output` | `<input>_<speed>x.mp4` | Custom output path |
| `-s`, `--speed` | `1.2` | Playback speed multiplier |

---

## Custom Scenarios

- **Only remove silence** — run just Step 1.
- **Only speed up** — run just Step 2 directly on the input file.
- **Aggressive cleanup** — use `--threshold -25dB --duration 0.5` for stricter silence removal, and `--speed 1.5` for faster playback.
- **Preview before committing** — use `--dry-run` on remove_silence.py to see what would be cut without creating a file.
- **Custom output name** — use `-o` on either script to control the output path.

---

## Important Notes

- Always run remove_silence **before** speed_video. Silence detection works on the original audio; speeding up first would alter the audio characteristics and make silence detection less accurate.
- For long videos (>30 min), the silence removal step may take a few minutes as it processes each segment individually.
- Both scripts preserve video quality — remove_silence uses stream copy (no re-encoding), while speed_video re-encodes with FFmpeg defaults.
