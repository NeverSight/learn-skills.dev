---
name: ascii-art
description: Converts text, images, or video to ASCII art with multiple styles and export formats. Use when the user asks to create ASCII art, convert images/videos to text art, or mentions ascii-art, braille art, or block art.
---

# ASCII Art Converter

## Setup

Before first use, run the environment setup (idempotent, <1s after first run):

```bash
bash {{SKILL_DIR}}/scripts/setup.sh
```

## Input Detection

1. **File path** → check extension: `.jpg/.jpeg/.png/.webp/.bmp/.tiff` → **image**, `.mp4/.webm/.avi/.mov/.mkv` → **video**, `.gif` → check if animated (video) or static (image)
2. **Pasted/attached image** → **save IMMEDIATELY** before doing anything else. Run:
   ```bash
   {{SKILL_DIR}}/scripts/.venv/bin/python {{SKILL_DIR}}/scripts/save_image.py --clipboard
   ```
   This grabs the image from the system clipboard (still there after paste), saves to `ascii/tmp/` with a timestamped name, and prints the saved path to stdout. Use that output path as `--input`.
   If `--clipboard` fails (no image in clipboard), fall back to asking: "Please provide the file path (e.g. `~/Downloads/photo.jpg`)." You can also pass a known file path directly: `save_image.py <path>`.
   **Do NOT proceed to options until you have a valid file path on disk.**
3. **Plain text** (no file, or file doesn't exist) → **text** (FIGlet banner)
4. **Nothing provided** → ask what they want to convert

## Options Prompt

Parse the user's message for pre-specified options. Then prompt for **unspecified options** using `AskUserQuestion`.

- "defaults" or "just do it" → skip prompting, use all defaults
- "random" or "surprise me" → skip prompting, use `--random`
- All options specified → skip prompting

Use `questions` array (max 4 per call, 3 options per question). List ALL choices with numbers in the `question` text. Top 3 as selectable options — user can type any number/name in free-text. No "Other" option. Default as option 1.

**Image/video** — ask in two rounds:
1. **Round 1** (4 questions): Style → Color → Export → Background
2. **Round 2** (only if export is `interactive` or `tsx`): Mouse Mode → Animation

**Text**: Font → Color → Export → Background (single round).

### Image/video options

| Option | Choices | Default |
|--------|---------|---------|
| Style | classic, braille, block, edge, dot-cross, halftone, particles, retro-art, terminal | classic |
| Color | grayscale, original, matrix, amber, custom (hex/named) | grayscale |
| Ratio | original, 16:9, 4:3, 1:1, 3:4, 9:16 | original |
| Background | dark, light, transparent | dark |
| Dither | none, floyd-steinberg, bayer, atkinson | none |
| Font size | 6-30 px | 14 |
| Export | png, html, svg, txt, md, clipboard, interactive, tsx | auto (image→png, video→gif) |
| Mouse mode | push, attract | push |
| Animation | none, noise-field, intervals, beam-sweep, glitch, crt | none |

Mouse mode and animation only apply to interactive/tsx exports. Only ask when export is `interactive` or `tsx`. Don't ask for `--hover-strength`, `--area-size`, or `--spread` — use defaults.

### Text options

| Option | Choices | Default |
|--------|---------|---------|
| Font | standard, doom, banner, slant, big, small, block, lean, mini, script, shadow, speed, ansi_shadow, ansi_regular | standard |
| Color | grayscale, original, matrix, amber, custom | grayscale |
| Background | dark, light, transparent | dark |
| Export | terminal (stdout), txt, md, png, html, svg, clipboard | terminal |

Interactive/tsx exports require image or video input — text is not supported.

### Disambiguation

- "block" as a **style** = Unicode block elements (█▓▒░) for images
- "block" as a **font** = block-letter FIGlet font for text
- For block-style text art, use `--font ansi_shadow` or `--font block`
- Custom colors: hex (`#ff6600`) or named (`coral`, `skyblue`). Translate creative descriptions to hex.

## Running the Conversion

```bash
{{SKILL_DIR}}/scripts/.venv/bin/python {{SKILL_DIR}}/scripts/convert.py \
  --input "<input>" \
  --type <text|image|video> \
  --style <style> \
  --color <color> \
  --background <background> \
  --export <format> \
  [--dither <algorithm>] \
  [--ratio <ratio>] \
  [--font-size <pixels>] \
  [--cols <number>] \
  [--font <font_name>] \
  [--custom-color "<hex>"] \
  [--mouse-mode <push|attract>] \
  [--animation <preset>] \
  [--invert] [--random] \
  [--fps <number>] \
  [--filename <custom_name>]
```

## Output

All files save to an `ascii/` folder in the current working directory (created automatically).

- **Text (terminal)**: prints to stdout + auto-copies to clipboard. Show in a code block.
- **File exports (png, html, svg, txt, md, gif)**: show the file path. Use Read tool to display images inline.
- **Interactive HTML**: show the file path. Suggest: `open <path>` to view in browser.
- **React TSX**: show the file path. Show usage: `import { AsciiArt } from './<filename>'`
- **Never preview in terminal** for image/video/interactive exports.

## Error Handling

- **Video fails**: likely missing ffmpeg or opencv. Suggest: `pip install opencv-python-headless`
- **Image fails**: check file exists and is a valid image format
- **Interactive/tsx + text**: prints error — interactive requires image/video input

## Follow-up

After showing the result, offer to: try a different style/color, adjust settings, export in another format, or try random mode. Remember the previous input path for re-runs.
