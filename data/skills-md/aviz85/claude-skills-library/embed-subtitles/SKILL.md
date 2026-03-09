---
name: embed-subtitles
description: "Burn subtitles onto videos using FFmpeg. Use for: hardcode subtitles, embed captions, video subtitling."
---

# Embed Subtitles

Burn SRT subtitles into video files using FFmpeg.

## Prerequisites

**No SRT file?** Use the `transcribe` skill first to generate subtitles from audio/video.

**Need translation?** After transcribing, read the SRT, translate each entry preserving timestamps, write new SRT file. No API needed.

## Quick Start

```bash
cd ~/.claude/skills/embed-subtitles/scripts

# Burn SRT into video
npx ts-node embed-subtitles.ts -i video.mp4 -s subtitles.srt -o output.mp4

# Custom styling
npx ts-node embed-subtitles.ts -i video.mp4 -s subtitles.srt -o output.mp4 \
  --font-size 24 --position bottom --margin 40

# Add credit text overlay at end
npx ts-node embed-subtitles.ts -i video.mp4 -s subtitles.srt -o output.mp4 \
  --credit "Your Name" --credit-position top
```

## Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--input` | `-i` | (required) | Input video file |
| `--subtitles` | `-s` | (required) | SRT subtitle file |
| `--output` | `-o` | (required) | Output video file |
| `--font-size` | | 20 | Font size in pixels |
| `--font-name` | | Arial | Font family name |
| `--position` | | bottom | Subtitle position: top, center, bottom |
| `--margin` | | 25 | Margin from edge in pixels |
| `--color` | | white | Text color |
| `--outline` | | 2 | Outline thickness |
| `--shadow` | | 1 | Shadow depth |
| `--credit` | | | Credit text to show at end |
| `--credit-position` | | top | Credit position: top, bottom |
| `--credit-duration` | | 2.5 | Credit display duration in seconds |
| `--extract-frame` | | | Extract frame at specified second for verification |

## Position Values

- `top` - Near top of video (good for credits, avoids bottom burned-in text)
- `center` - Middle of video
- `bottom` - Near bottom of video (traditional subtitle position)

## Dependencies

- FFmpeg (must be installed and in PATH)

## RTL Auto-Detection & Fix (CRITICAL)

**Before embedding ANY SRT file, Claude MUST check if the content is RTL.**

### Detection

Read the SRT file and check if the majority of text lines contain Hebrew/Arabic/Farsi characters:
- Hebrew range: `\u0590-\u05FF`
- Arabic range: `\u0600-\u06FF`
- Farsi additional: `\u0750-\u077F`

If RTL content is detected, apply the fix BEFORE passing to FFmpeg.

### RTL Fix

Wrap each text line (not index numbers, not timestamps) with Unicode directional marks:

```python
python3 -c "
import re

with open('SRT_FILE_PATH', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
result = []
for line in lines:
    stripped = line.strip()
    if stripped and not re.match(r'^\d+$', stripped) and not re.match(r'\d{2}:\d{2}:\d{2}', stripped):
        line = '\u202B' + line + '\u202C'
    result.append(line)

with open('SRT_FILE_PATH', 'w', encoding='utf-8') as f:
    f.write('\n'.join(result))
"
```

- **U+202B** (RLE - Right-to-Left Embedding): forces RTL paragraph direction
- **U+202C** (PDF - Pop Directional Formatting): closes the embedding

**This fixes:** English words at line start, periods/commas on wrong side, mixed bidi text.

### When to apply

Claude should analyze the SRT content intelligently:
- If most text is Hebrew/Arabic/Farsi → apply RTL fix
- If mixed but predominantly RTL → apply RTL fix
- If LTR (English, Spanish, etc.) → skip
- No flag needed from the user - detect automatically

## Notes

- For Arabic credits, use English text due to FFmpeg drawtext RTL limitations
- Use `--extract-frame` to verify subtitle positioning before final render
