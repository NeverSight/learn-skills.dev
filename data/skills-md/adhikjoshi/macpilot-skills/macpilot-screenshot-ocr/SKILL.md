---
name: macpilot-screenshot-ocr
description: Capture screenshots and extract text via OCR using MacPilot. Take full-screen, region, or window screenshots, and recognize text in images or screen areas with multi-language support.
---

# MacPilot Screenshot & OCR

Use MacPilot to capture screenshots of the screen, specific regions, or application windows, and extract text from images or screen regions using Apple's built-in Vision OCR.

## When to Use

Use this skill when:
- You need to capture what's currently on screen
- You need to extract text from an image file
- You need to read text from a specific area of the screen
- You need to capture a specific app window
- You need to verify visual state of an application
- You need to capture screen recordings

## Screenshot Commands

### Full Screen
```bash
macpilot screenshot --json                           # Capture to temp file
macpilot screenshot ~/Desktop/screen.png --json      # Capture to specific path
macpilot screenshot --with-permissions --json        # Use CGWindowListCreateImage directly
```

### Specific Region
```bash
macpilot screenshot --region 100,200,800,600 --json
# Region format: x,y,width,height (from top-left corner)
```

### Specific Window
```bash
macpilot screenshot --window "Safari" --json         # Capture Safari window
macpilot screenshot --window "Finder" --json         # Capture Finder window
```

### All Windows
```bash
macpilot screenshot --all-windows --json             # Each window separately
```

### Specific Display
```bash
macpilot screenshot --display 1 --json               # Second display (0-indexed)
```

### Format Options
```bash
macpilot screenshot --format png ~/Desktop/shot.png  # PNG (default, lossless)
macpilot screenshot --format jpg ~/Desktop/shot.jpg  # JPEG (smaller files)
```

## OCR Commands

### Extract Text from Image File
```bash
macpilot ocr scan /path/to/image.png --json
macpilot ocr scan ~/Desktop/screenshot.png --json
```

### Extract Text from Screen Region
```bash
macpilot ocr scan 100 200 800 600 --json
# Arguments: x y width height (captures region then OCRs it)
```

### Multi-Language OCR
```bash
macpilot ocr scan image.png --language en-US --json       # English
macpilot ocr scan image.png --language ja --json           # Japanese
macpilot ocr scan image.png --language zh-Hans --json      # Simplified Chinese
macpilot ocr scan image.png --language de --json           # German
macpilot ocr scan image.png --language fr --json           # French
```

### OCR Click (Find and Click Text on Screen)
```bash
macpilot ocr click "Submit" --json                    # Find text on screen and click it
macpilot ocr click "OK" --app Finder --json           # Click text in specific app
macpilot ocr click "Accept" --timeout 10 --json       # Retry until text appears (10s)
```

OCR click takes a screenshot, runs OCR, finds the matching text (case-insensitive), and clicks at its center coordinates. Use `--timeout` to poll and retry when waiting for text to appear.

## Screen Recording (ScreenCaptureKit)

### Start Recording
```bash
macpilot screen record start --output ~/Desktop/recording.mov --json
macpilot screen record start --output rec.mov --region 0,0,1920,1080 --json  # Region
macpilot screen record start --output rec.mov --window Safari --json          # Window
macpilot screen record start --output rec.mov --display 1 --json              # Display
macpilot screen record start --output rec.mov --audio --json                  # With audio
macpilot screen record start --output rec.mov --quality high --fps 60 --json  # Quality
```

### Control Recording
```bash
macpilot screen record stop --json         # Stop and save
macpilot screen record status --json       # Check if recording
macpilot screen record pause --json        # Pause recording
macpilot screen record resume --json       # Resume recording
```

Quality options: `low` (1 Mbps), `medium` (5 Mbps, default), `high` (10 Mbps). FPS default: 30.

## Display Information

```bash
macpilot display-info --json
# Returns: all displays with resolution, position, scale factor
```

## Workflow Patterns

### Capture and OCR in One Flow
```bash
# Take screenshot of specific region
macpilot screenshot --region 0,0,1920,1080 ~/tmp/capture.png --json
# Extract text from it
macpilot ocr scan ~/tmp/capture.png --json
```

### Quick Screen Region OCR
```bash
# Directly OCR a screen region without saving
macpilot ocr scan 200 100 600 400 --json
```

### Find and Click Text (No Coordinate Math)
```bash
# Instead of screenshot > OCR > parse > click, just:
macpilot ocr click "Submit" --json
macpilot ocr click "Next" --timeout 5 --json   # Wait up to 5s for text to appear
```

### Verify UI State
```bash
# Screenshot a window to see its current state
macpilot screenshot --window "Safari" ~/tmp/safari.png --json
# Read the image to verify content
macpilot ocr scan ~/tmp/safari.png --json
```

### Record an Automation
```bash
macpilot screen record start --output ~/Desktop/demo.mov
macpilot app open Safari
macpilot wait seconds 2
macpilot keyboard key cmd+l
macpilot keyboard type "https://example.com"
macpilot keyboard key enter
macpilot wait seconds 3
macpilot screen record stop
```

## Tips

- Screen Recording permission must be granted to MacPilot.app in System Settings
- PNG format is best for screenshots with text (lossless); JPEG for photos
- OCR works best on high-contrast text; increase screenshot region size if text is small
- Use `display-info` to get screen dimensions before capturing specific regions
- The coordinate system starts at top-left (0,0) with x increasing right and y increasing down
- On Retina displays, coordinates are in logical points (not physical pixels)
