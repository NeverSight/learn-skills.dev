---
name: colorize
description: Turn photos, videos, and Live Photos into a black-and-white to color reveal clip (单彩渐变 + 动感模糊 + 丁达尔旋焦). The frame starts monochrome and spun, color sweeps in from the left under a horizontal motion blur, and the spin settles from the center outward into a softly glowing full-color frame. Use when users ask for 上色效果, 黑白变彩色, 丁达尔旋焦, 旋焦上色, 剪映上色特效, color reveal, colorize transition, or want this effect on images, iPhone Live Photos (HEIC/JPG + MOV), Android motion photos, or video clips. Outputs H.264 MP4.
---

# Colorize

## Workflow

1. Collect the user's inputs: images, videos, or Live Photos. Use absolute paths.
2. Resolve the skill directory and install dependencies once (see Requirements).
3. Run `scripts/colorize.py` with the inputs and an output path.
4. Wait for `VALIDATION=PASS` and `OUTPUT_VIDEO=<absolute path>`.
5. Optionally extract a few frames with `ffmpeg` to check the look before replying.
6. Return the output path and the settings used.

## Quick Start

```bash
skill_dir=""
for base in "${AGENTS_HOME:-$HOME/.agents}" "${CLAUDE_HOME:-$HOME/.claude}" "${CODEX_HOME:-$HOME/.codex}"; do
  if [ -d "$base/skills/colorize" ]; then
    skill_dir="$base/skills/colorize"
    break
  fi
done
[ -n "$skill_dir" ] || { echo "colorize skill not found under ~/.agents, ~/.claude, or ~/.codex"; exit 1; }

python3 -m pip install -r "$skill_dir/scripts/requirements.txt"
python3 "$skill_dir/scripts/colorize.py" "/abs/path/photo.jpg" -o "$(pwd)/out/photo_colorize.mp4"
```

If the agent already knows the directory containing this `SKILL.md`, use that as `skill_dir`.

## Inputs

| Input | What happens |
| --- | --- |
| Image (`png jpg jpeg webp heic heif avif bmp tif`) | Static plate; the reveal lasts `--duration` seconds, then `--hold` seconds of the settled frame. |
| Video (`mp4 mov m4v webm mkv avi gif`) | Each source frame keeps moving; the reveal runs over the first `--duration` seconds and the rest of the clip keeps the settled look. Audio is kept. |
| iPhone Live Photo | Pass the still (`IMG_0001.HEIC` or `.JPG`). A same-name `.MOV` beside it is used automatically, with its audio. Pass the `.MOV` directly for the same result. |
| Android motion photo | Pass the `.jpg`; the embedded MP4 (Google `MP.jpg` / `MVIMG`, Samsung) is extracted automatically. |
| Several inputs | Rendered in order and joined into one MP4. Each input gets its own reveal. |

Use `--still` to ignore Live Photo or motion photo video and animate only the still.

## Common Commands

```bash
# One photo, 2 s reveal + 0.5 s hold
python3 "$skill_dir/scripts/colorize.py" photo.jpg --hold 0.5 -o out/photo.mp4

# Live Photo (IMG_0001.MOV next to it is picked up)
python3 "$skill_dir/scripts/colorize.py" IMG_0001.HEIC -o out/live.mp4

# Video: slower 3 s reveal, keep the first 6 s
python3 "$skill_dir/scripts/colorize.py" clip.mov --duration 3 --max-length 6 -o out/clip.mp4

# Several images and videos as one vertical reel
python3 "$skill_dir/scripts/colorize.py" a.jpg b.heic c.mov --size 1080x1920 -o out/reel.mp4

# Stronger spin and a little more glow
python3 "$skill_dir/scripts/colorize.py" photo.jpg --set angle=0.09 --set bloom=0.7 -o out/strong.mp4
```

## Options

| Option | Default | Meaning |
| --- | --- | --- |
| `-o, --output` | `<first input>_colorize.mp4` | Output MP4 path. |
| `--duration` | `2` | Reveal length in seconds. |
| `--hold` | `0` | Images only: seconds to hold the settled frame. |
| `--fps` | `30` | Output frame rate. |
| `--size WxH` | first input's aspect, long edge ≤ `--max-edge` | Force output size; other inputs are center-cropped to it. |
| `--max-edge` | `1920` | Long-edge cap when `--size` is not set. Never upscales. |
| `--max-length` | full clip | Videos: keep at most this many seconds. |
| `--still` | off | Ignore Live Photo / motion photo video. |
| `--mute` | off | Drop audio. |
| `--set KEY=VALUE` | — | Override one effect parameter (repeatable). |
| `--params file.json` | — | Override several effect parameters. |
| `--crf` | `17` | x264 quality; lower is larger and sharper. |

## Effect Parameters

The defaults were fitted to the Jianying effect stack on static photos. Useful knobs for `--set`:

| Key | Default | Effect |
| --- | --- | --- |
| `angle` | `0.0503` | Spin-blur arc in radians; larger is stronger, the sign sets direction. Decays to zero. |
| `focus_scale` | `0.9` | Final width of the sharp center disc; larger settles the edges sooner. |
| `motion` | `0.70` | Horizontal motion-blur strength; decays to zero. |
| `blur_power` | `1.0` | Blur decay curve; larger fades faster. |
| `front_speed` | `0.63` | Speed of the color sweep. |
| `edge` | `0.24` | Softness of the color/mono boundary. |
| `bloom` / `rays` | `0.54` / `0.29` | Soft glow and radial light-ray strength. |
| `softness` | `2.3` | Residual softening; `0` is sharpest. |
| `saturation` | `0.98` | Final saturation. |
| `center_x`, `center_y` | `0.5` | Spin center in UV (y up). |

## Behavior

- Renders on the GPU with OpenGL 3.3 through `moderngl` (falls back to EGL on headless Linux) and encodes H.264 `yuv420p` BT.709 MP4 with `ffmpeg`.
- Output follows the first input's aspect ratio and orientation, including rotation metadata on phone videos.
- HDR (HLG/PQ) videos are tone-mapped to SDR when `ffmpeg` has `zscale`.
- HEIC/AVIF stills need `pillow-heif`, macOS `sips`, or an `ffmpeg` with HEIF support.
- When any input has audio, every segment carries an AAC track (silence for images) so joined clips stay in sync.
- Videos shorter than `--duration` get a compressed reveal that still ends fully settled.
- Prints `VALIDATION=PASS` after checking the output's size, duration, and audio with `ffprobe`.

## Requirements

- Python 3.9+ with `numpy`, `moderngl`, `Pillow` (`scripts/requirements.txt`); optional `pillow-heif`
- `ffmpeg` and `ffprobe` on `PATH`
- A GPU or driver with OpenGL 3.3 (macOS, Windows, desktop Linux, or Linux with EGL)

On macOS, if `moderngl` has to build from source: `CXXFLAGS='-std=c++11' python3 -m pip install moderngl`.
