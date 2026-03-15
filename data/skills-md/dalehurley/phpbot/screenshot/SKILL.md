---
name: screenshot
description: "Capture screenshots of the desktop, a specific window, or a screen region. Use this skill when the user asks to take a screenshot, capture the screen, grab a screen image, or save what's on screen to a file."
tags: [screenshot, screen-capture, screencapture, display, utility]
version: 0.1.0
---

# Skill: screenshot

## When to Use

Use this skill when the user asks to:

- Take a screenshot
- Capture the screen or desktop
- Grab a screen image
- Save what's on screen to a file
- Capture a specific window or region

## Input Parameters

| Parameter | Required | Description                                                      | Example       |
| --------- | -------- | ---------------------------------------------------------------- | ------------- |
| `mode`    | No       | Capture mode: `fullscreen` (default), `window`, `region`         | fullscreen    |
| `output`  | No       | Output file path (default: ~/Desktop/screenshot-{timestamp}.png) | /tmp/shot.png |
| `delay`   | No       | Delay in seconds before capture                                  | 3             |

## Procedure

1. Run the bundled capture script:

   ```bash
   # Full screen (default)
   bash skills/screenshot/scripts/capture.sh

   # Specific mode with output path
   bash skills/screenshot/scripts/capture.sh --mode window --output /tmp/shot.png

   # With delay
   bash skills/screenshot/scripts/capture.sh --delay 3
   ```

2. Report the saved file path to the user

## Bundled Scripts

| Script               | Type | Description                               |
| -------------------- | ---- | ----------------------------------------- |
| `scripts/capture.sh` | SH   | Capture screenshots using native OS tools |

### Script Usage

```bash
# Full screen capture (default)
bash scripts/capture.sh

# Capture a specific window (interactive selection)
bash scripts/capture.sh --mode window

# Capture a region (interactive selection)
bash scripts/capture.sh --mode region

# Custom output path
bash scripts/capture.sh --output /tmp/my-screenshot.png

# With delay (seconds)
bash scripts/capture.sh --delay 5

# Combined
bash scripts/capture.sh --mode window --output /tmp/win.png --delay 2
```

## Example

```
take a screenshot
capture the screen and save it to my desktop
screenshot the current window
take a screenshot in 3 seconds
grab a screenshot of a region of my screen
```
