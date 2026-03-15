---
name: video-edit
description: Complete video editing toolkit - silence removal, auto-captions, vertical crop, YouTube clipping, 3D transitions, and social media compression. Use when user asks to edit video, remove silences, add captions/subtitles, crop to vertical/shorts, download YouTube clips, compress video, or create video teasers.
---

# Video Editing Toolkit

## Goal
Complete video production pipeline: silence removal, auto-captions, vertical cropping, YouTube clipping, compression, and 3D transitions.

## Scripts (7 total)

| Script | Purpose |
|--------|---------|
| `jump_cut_vad_singlepass.py` | Remove silences with neural VAD (Silero) |
| `auto_captions.py` | Generate + burn styled subtitles (Whisper + FFmpeg) |
| `vertical_crop.py` | Auto-crop 16:9 → 9:16 with face tracking |
| `youtube_clip.py` | Download YouTube + AI chapter clipping |
| `compress_video.py` | Social media compression with platform presets |
| `simple_video_edit.py` | Full pipeline: silence removal + transcription + metadata + upload |
| `insert_3d_transition.py` | 3D swivel teaser insertion |

---

## Quick Start Recipes

### Recipe 1: Full Social Media Pipeline
```bash
# 1. Remove silences
python3 ./scripts/jump_cut_vad_singlepass.py input.mp4 .tmp/edited.mp4

# 2. Add captions
python3 ./scripts/auto_captions.py .tmp/edited.mp4 .tmp/captioned.mp4 --word-level --max-words 2

# 3. Crop to vertical for Shorts/Reels
python3 ./scripts/vertical_crop.py .tmp/captioned.mp4 .tmp/vertical.mp4

# 4. Compress for platform
python3 ./scripts/compress_video.py .tmp/vertical.mp4 output.mp4 --preset instagram-reel
```

### Recipe 2: YouTube → Shorts Pipeline
```bash
# 1. Download + auto-clip YouTube video
python3 ./scripts/youtube_clip.py "https://youtube.com/watch?v=..." --auto-clip --output-dir clips/

# 2. Add captions to best clip
python3 ./scripts/auto_captions.py clips/chapters/01_intro.mp4 .tmp/captioned.mp4 --word-level

# 3. Crop to vertical
python3 ./scripts/vertical_crop.py .tmp/captioned.mp4 .tmp/vertical.mp4

# 4. Compress for YouTube Shorts
python3 ./scripts/compress_video.py .tmp/vertical.mp4 short.mp4 --preset youtube-shorts
```

### Recipe 3: Quick Edit + Upload
```bash
# All-in-one: silence removal + transcription + metadata + Auphonic upload
python3 ./scripts/simple_video_edit.py --video input.mp4 --title "My Video"
```

---

## Script 1: VAD Silence Removal

**File:** `./scripts/jump_cut_vad_singlepass.py`

### How It Works
1. Extracts audio as WAV (16kHz mono)
2. Runs Silero VAD to detect speech segments
3. Merges close segments, adds padding
4. Uses FFmpeg trim+concat to join segments in single pass
5. Hardware encodes with hevc_videotoolbox (H.265, 17Mbps, 30fps)

### CLI Arguments
| Argument | Default | Description |
|----------|---------|-------------|
| `--min-silence` | 0.5 | Min silence duration to cut (seconds) |
| `--min-speech` | 0.25 | Min speech duration to keep (seconds) |
| `--padding` | 100 | Padding around speech (ms) |
| `--merge-gap` | 0.3 | Merge segments closer than this (seconds) |
| `--keep-start` | true | Always start from 0:00 |

### Usage
```bash
python3 ./scripts/jump_cut_vad_singlepass.py input.mp4 output.mp4
python3 ./scripts/jump_cut_vad_singlepass.py input.mp4 output.mp4 --min-silence 1.0 --padding 200
```

### Processing Time
~8 minutes for a 49-min 4K video

---

## Script 2: Auto-Captions

**File:** `./scripts/auto_captions.py`

### How It Works
1. Transcribes video using faster-whisper (word-level timestamps)
2. Generates SRT subtitles (segment-level or word-level)
3. Burns styled captions into video with FFmpeg

### CLI Arguments
| Argument | Default | Description |
|----------|---------|-------------|
| `--model` | base | Whisper model: tiny, base, small, medium, large-v3 |
| `--language` | auto | Force language (en, es, hi, etc.) |
| `--word-level` | false | Short punchy captions (1-3 words at a time) |
| `--max-words` | 3 | Max words per caption in word-level mode |
| `--font-size` | 22 | Caption font size (auto-scales for vertical) |
| `--font-color` | white | Text color: white, yellow, cyan, green, red, orange, pink |
| `--outline-color` | black | Outline color |
| `--position` | bottom | Caption position: bottom, top, middle |
| `--srt-only` | false | Only generate SRT, don't burn |
| `--srt-path` | auto | Custom SRT output path |
| `--bold` | true | Bold text |

### Usage
```bash
# Basic captions
python3 ./scripts/auto_captions.py input.mp4 output.mp4

# Word-level (CapCut/Submagic style)
python3 ./scripts/auto_captions.py input.mp4 output.mp4 --word-level --max-words 2

# Yellow captions at top
python3 ./scripts/auto_captions.py input.mp4 output.mp4 --font-color yellow --position top

# SRT only (no burn)
python3 ./scripts/auto_captions.py input.mp4 --srt-only

# High accuracy
python3 ./scripts/auto_captions.py input.mp4 output.mp4 --model large-v3
```

### Dependencies
```bash
pip install faster-whisper
```

---

## Script 3: Vertical Crop

**File:** `./scripts/vertical_crop.py`

### How It Works
1. Samples frames throughout the video
2. Detects faces using OpenCV Haar cascade
3. Smooths face positions to avoid jitter
4. Crops 16:9 → 9:16 centered on the speaker
5. For moving subjects: segments video into 2s chunks with per-segment tracking

### CLI Arguments
| Argument | Default | Description |
|----------|---------|-------------|
| `--ratio` | 9:16 | Target aspect ratio (e.g., 9:16, 4:5, 1:1) |
| `--position` | auto | Crop position: auto (face tracking), left, center, right |
| `--smoothing` | 30 | Smoothing window in frames |
| `--sample-interval` | 5 | Sample every N frames for detection |

### Usage
```bash
# Auto face-tracking crop
python3 ./scripts/vertical_crop.py input.mp4 output.mp4

# Square crop (Instagram post)
python3 ./scripts/vertical_crop.py input.mp4 output.mp4 --ratio 1:1

# 4:5 crop (Instagram feed)
python3 ./scripts/vertical_crop.py input.mp4 output.mp4 --ratio 4:5

# Center crop (no tracking)
python3 ./scripts/vertical_crop.py input.mp4 output.mp4 --position center
```

### Dependencies
```bash
pip install opencv-python numpy
```

---

## Script 4: YouTube Clip

**File:** `./scripts/youtube_clip.py`

### How It Works
1. Downloads video via yt-dlp (up to 4K)
2. Extracts YouTube chapters if available
3. Falls back to AI chapter generation (Whisper + Claude)
4. Clips video into individual chapter files

### CLI Arguments
| Argument | Default | Description |
|----------|---------|-------------|
| `--download-only` | false | Only download, don't clip |
| `--max-quality` | 1080 | Max quality: 480, 720, 1080, 1440, 2160 |
| `--audio-only` | false | Download audio only (MP3) |
| `--start` | none | Manual clip start (seconds) |
| `--end` | none | Manual clip end (seconds) |
| `--auto-clip` | false | AI-powered chapter detection and clipping |
| `--use-yt-chapters` | true | Use YouTube chapters if available |
| `--max-clips` | none | Limit number of clips |
| `--whisper-model` | base | Whisper model for transcription |
| `--reencode` | false | Re-encode clips (precise cuts) |
| `--output-dir` | .tmp/clips | Output directory |

### Usage
```bash
# Download only
python3 ./scripts/youtube_clip.py "https://youtube.com/watch?v=..." --download-only

# Auto-clip into chapters
python3 ./scripts/youtube_clip.py "https://youtube.com/watch?v=..." --auto-clip

# Extract specific range
python3 ./scripts/youtube_clip.py "https://youtube.com/watch?v=..." --start 60 --end 180 -o clip.mp4

# Download audio only
python3 ./scripts/youtube_clip.py "https://youtube.com/watch?v=..." --audio-only

# Top 3 clips only
python3 ./scripts/youtube_clip.py "https://youtube.com/watch?v=..." --auto-clip --max-clips 3
```

### Dependencies
```bash
pip install yt-dlp faster-whisper anthropic
```

---

## Script 5: Video Compressor

**File:** `./scripts/compress_video.py`

### Platform Presets
| Preset | Resolution | CRF | Max Duration | Max Size | Notes |
|--------|-----------|-----|-------------|----------|-------|
| `youtube` | 1080p | 18 | none | none | High quality |
| `youtube-shorts` | 1080x1920 | 20 | 60s | none | Vertical |
| `instagram-reel` | 1080x1920 | 23 | 90s | none | Vertical |
| `instagram-post` | 1080x1080 | 23 | 60s | none | Square/vertical |
| `tiktok` | 1080x1920 | 23 | 180s | none | Vertical |
| `twitter` | 1080p | 23 | 140s | 512MB | Auto-bitrate |
| `linkedin` | 1080p | 23 | 600s | 200MB | Auto-bitrate |
| `telegram` | 720p | 28 | none | 50MB | For bots |
| `whatsapp` | 720p | 28 | 120s | 16MB | Aggressive |
| `small` | 480p | 30 | none | none | Quick sharing |

### CLI Arguments
| Argument | Default | Description |
|----------|---------|-------------|
| `--preset` | none | Platform preset (see table above) |
| `--resolution` | 1080 | Max height in pixels |
| `--crf` | 23 | Quality (0=lossless, 51=worst) |
| `--audio-bitrate` | 128k | Audio bitrate |
| `--target-size` | none | Target file size in MB |
| `--max-duration` | none | Max duration in seconds |
| `--list-presets` | false | Show all presets |

### Usage
```bash
# Platform preset
python3 ./scripts/compress_video.py input.mp4 output.mp4 --preset instagram-reel
python3 ./scripts/compress_video.py input.mp4 output.mp4 --preset whatsapp

# Target file size
python3 ./scripts/compress_video.py input.mp4 output.mp4 --target-size 25

# Custom
python3 ./scripts/compress_video.py input.mp4 output.mp4 --resolution 720 --crf 28

# List all presets
python3 ./scripts/compress_video.py input.mp4 output.mp4 --list-presets
```

---

## Script 6: Simple Video Edit (Full Pipeline)

**File:** `./scripts/simple_video_edit.py`

### How It Works
1. FFmpeg silence detection + cutting
2. Audio normalization (loudnorm)
3. Whisper transcription
4. Claude-generated YouTube metadata (summary + chapters)
5. Auphonic upload → YouTube (private draft)

### CLI Arguments
| Argument | Default | Description |
|----------|---------|-------------|
| `--video` | required | Input video path |
| `--title` | required | YouTube title |
| `--thumbnail` | none | Thumbnail image path |
| `--no-upload` | false | Skip Auphonic upload |
| `--no-normalize` | false | Skip audio normalization |
| `--upload-only` | false | Skip editing, just upload |
| `--silence-threshold` | -35 | Silence threshold in dB |
| `--silence-duration` | 3.0 | Min silence duration (seconds) |

### Usage
```bash
# Full pipeline
python3 ./scripts/simple_video_edit.py --video input.mp4 --title "My Video"

# Local only
python3 ./scripts/simple_video_edit.py --video input.mp4 --title "Test" --no-upload
```

### Dependencies
```bash
pip install anthropic faster-whisper requests python-dotenv
# Requires: ANTHROPIC_API_KEY, AUPHONIC_API_KEY in .env
```

---

## Script 7: 3D Swivel Teaser

**File:** `./scripts/insert_3d_transition.py`

### How It Works
1. Extracts frames from later in video (default: 60s onwards)
2. Creates 3D rotating "swivel" animation via Remotion
3. Splits video: intro → transition → main content
4. Re-encodes and concatenates with audio preserved

### CLI Arguments
| Argument | Default | Description |
|----------|---------|-------------|
| `--insert-at` | 3 | Where to insert teaser (seconds) |
| `--duration` | 5 | Teaser duration (seconds) |
| `--teaser-start` | 60 | Where to sample content from (seconds) |
| `--bg-color` | #2d3436 | Background color (hex) |
| `--bg-image` | none | Background image path |

### Final Timeline
```
[0-3s intro] [3-8s swivel teaser @ 100x] [8s onwards: edited content]
Audio: Original audio plays continuously
```

### Dependencies
```bash
pip install torch  # For Silero VAD (jump_cut script)
brew install ffmpeg node  # macOS
cd video_effects && npm install  # For Remotion 3D rendering
```

---

## All Dependencies (Install Once)

```bash
# Core (required for all scripts)
brew install ffmpeg

# Silence removal
pip install torch

# Auto-captions + YouTube clip
pip install faster-whisper

# Vertical crop
pip install opencv-python numpy

# YouTube download
pip install yt-dlp

# AI features (chapters, metadata)
pip install anthropic

# Full pipeline (simple_video_edit)
pip install requests python-dotenv

# 3D transitions
brew install node
cd scripts/video_effects && npm install
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Cuts feel abrupt | `--padding 200` in jump_cut |
| Too much cut | `--min-silence 1.0` in jump_cut |
| Captions too small | `--font-size 32` in auto_captions |
| Vertical video detected | Font auto-scales 1.3x |
| Won't play in QuickTime | Ensure hvc1 codec tag |
| Face not detected | Try `--position center` in vertical_crop |
| YouTube download fails | Update yt-dlp: `pip install -U yt-dlp` |
| File too large | Use `--preset whatsapp` or `--target-size 25` |
| Hardware encoder fails | Auto-falls back to software (libx264) |

## Technical Details
- macOS: Hardware encoding (hevc_videotoolbox / h264_videotoolbox)
- Fallback: libx264/libx265 with CRF
- Audio: AAC 128-192kbps
- Uses `hvc1` codec tag for QuickTime compatibility
- All scripts support `--help` for full argument list

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_video` | file_path | Yes | Input video file path |
| `recipe` | string | No | Pipeline recipe: full-social, youtube-shorts, quick-edit |
| `preset` | string | No | Compression preset: youtube, instagram-reel, tiktok, whatsapp, etc. |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `output_video` | file_path | Processed video file path |

### Credentials
| Name | Source |
|------|--------|
| `ANTHROPIC_API_KEY` | .env (for AI chapters) |
| `AUPHONIC_API_KEY` | .env (for upload) |

### Composable With
Skills that chain well with this one: `pan-3d-transition`, `recreate-thumbnails`

### Cost
Free locally (FFmpeg + Silero VAD)
