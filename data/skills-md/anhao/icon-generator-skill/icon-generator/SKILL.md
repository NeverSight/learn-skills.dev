---
name: icon-generator
description: Generate Android and iOS app icon sets from one source image with a bundled Pillow script. Use when Codex needs to create mobile app launcher icons, iOS AppIcon.appiconset assets, Android mipmap icons, adaptive icon foreground/background/XML files, extra square sizes, or rounded-corner icon exports from a logo or artwork file.
---

# Icon Generator

## Overview

Use the bundled script to turn one source image into Android and iOS app icon assets. Prefer this skill when the task is deterministic icon export rather than manual image editing.

## Quick Start

1. Confirm the input image path.
2. Run `python3 scripts/icon_generator.py <input-image> -o <output-dir>`.
3. Inspect the generated `android/` and `ios/AppIcon.appiconset/` folders.

Install Pillow first if needed:

```bash
python3 -m pip install 'Pillow>=10.0.0'
```

## Workflow

### Choose output behavior

- Use the default `contain` mode when the full logo must stay visible and padding is acceptable.
- Use `cover` when the icon must fill the square and center-cropping is acceptable.
- Use `--background` to control padding color for non-square sources.
- Use `--corner-radius` when the exported icons should already include rounded corners.
- Use `--extra-sizes` when the user wants additional square PNGs beyond the built-in Android and iOS sizes.
- Use `--android-adaptive` when the user explicitly needs Android adaptive icon resources.

### Run the script

Basic export:

```bash
python3 scripts/icon_generator.py input.png -o output_icons
```

Export with crop, white padding, extra sizes, and rounded corners:

```bash
python3 scripts/icon_generator.py input.png \
  -o output_icons \
  --mode cover \
  --background '#FFFFFFFF' \
  --extra-sizes 256 384 \
  --corner-radius 18
```

Export Android adaptive icons too:

```bash
python3 scripts/icon_generator.py input.png \
  -o output_icons \
  --android-adaptive \
  --adaptive-background '#FFFFFF'
```

## Validate Result

- Check `android/mipmap-*` for launcher PNGs.
- Check `android/play-store/play_store_icon.png` for the 512px store asset.
- Check `ios/AppIcon.appiconset/Contents.json` plus the generated PNG files.
- If adaptive icons were requested, check `android/mipmap-anydpi-v26/` for the XML files and `ic_launcher_foreground.png` / `ic_launcher_background.png`.

## Troubleshooting

- If the script exits with a Pillow import error, install Pillow and rerun.
- If colors fail to parse, pass `#RRGGBB` or `#RRGGBBAA`.
- If the source image is missing, stop and confirm the path before regenerating.
- If the user asks for non-square outputs or hand-tuned retouching, this skill is the wrong tool; use an image editing workflow instead.

## Resources

- Use `scripts/icon_generator.py` for the actual export.
- Read `references/usage.md` for argument details, size lists, and output structure.
