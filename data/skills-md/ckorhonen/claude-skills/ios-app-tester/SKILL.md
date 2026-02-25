---
name: ios-app-tester
description: Test iOS apps using AXe CLI for accessibility auditing, UI automation, and simulator control. Use when testing iOS Simulator apps, automating UI interactions, recording test videos, or auditing accessibility labels and VoiceOver support.
---

# iOS App Tester (AXe CLI)

## Overview

Test and automate iOS Simulator applications using AXe, a command-line tool that leverages Apple's Accessibility APIs for programmatic simulator control. AXe runs as a single binary with no server setup required.

## When to Use

- Automating iOS Simulator UI interactions for testing
- Auditing accessibility labels and VoiceOver descriptions
- Recording test execution videos
- Scripting repeatable test scenarios
- CI/CD pipeline iOS testing integration

## Prerequisites

- macOS with Xcode installed
- iOS Simulator (included with Xcode)
- Homebrew (for installation)

## Installation

```bash
brew tap cameroncooke/axe
brew install axe
```

Verify installation:
```bash
axe --help
```

## Quick Start

1. Find your simulator UDID:
```bash
axe list-simulators
```

2. Tap a coordinate:
```bash
axe tap -x 200 -y 400 --udid <SIMULATOR_UDID>
```

3. Inspect accessibility elements:
```bash
axe describe-ui --udid <SIMULATOR_UDID>
```

## Command Reference

### Simulator Discovery

```bash
# List all available simulators with UDIDs
axe list-simulators
```

### Touch Interactions

```bash
# Tap at coordinates
axe tap -x 100 -y 200 --udid <UDID>

# Swipe gesture
axe swipe --start-x 100 --start-y 500 --end-x 100 --end-y 200 --udid <UDID>

# Low-level touch events
axe touch-down -x 100 -y 200 --udid <UDID>
axe touch-up -x 100 -y 200 --udid <UDID>
```

### Preset Gestures

```bash
# Scrolling
axe gesture scroll-up --udid <UDID>
axe gesture scroll-down --udid <UDID>
axe gesture scroll-left --udid <UDID>
axe gesture scroll-right --udid <UDID>

# Edge swipes (for navigation)
axe gesture swipe-from-left-edge --udid <UDID>
axe gesture swipe-from-right-edge --udid <UDID>
axe gesture swipe-from-top-edge --udid <UDID>
axe gesture swipe-from-bottom-edge --udid <UDID>
```

### Text Input

```bash
# Type text directly
axe type 'Hello World!' --udid <UDID>

# Type from stdin (useful for passwords/sensitive data)
echo "secret" | axe type --stdin --udid <UDID>

# Type from file
axe type --file input.txt --udid <UDID>
```

### Hardware Buttons

```bash
# Home button
axe button home --udid <UDID>

# Lock/power button
axe button lock --udid <UDID>

# Long press (e.g., for Siri)
axe button lock --duration 2.0 --udid <UDID>

# Side button
axe button side --udid <UDID>

# Apple Pay
axe button apple-pay --udid <UDID>
```

### Accessibility Inspection

```bash
# Describe all UI elements (full screen)
axe describe-ui --udid <UDID>

# Describe element at specific point
axe describe-ui --point 100,200 --udid <UDID>
```

### Video Recording

```bash
# Record to MP4 file
axe record-video --udid <UDID> --fps 15 --output test-recording.mp4

# Stream video (for ffmpeg piping)
axe stream-video --udid <UDID> --fps 30 --format ffmpeg | ffmpeg -i - output.mp4

# Stream as MJPEG
axe stream-video --udid <UDID> --fps 10 --format mjpeg > stream.mjpeg
```

### Timing Control

All commands support delays for sequencing:

```bash
# Wait before action
axe tap -x 100 -y 200 --pre-delay 1.0 --udid <UDID>

# Wait after action
axe tap -x 100 -y 200 --post-delay 0.5 --udid <UDID>

# Combined delays
axe type 'text' --pre-delay 0.5 --post-delay 1.0 --udid <UDID>
```

## Accessibility Testing Workflow

### 1. Audit Full Screen

```bash
# Get all accessibility elements
axe describe-ui --udid <UDID> > accessibility-audit.txt
```

Review output for:
- Missing `accessibilityLabel` values
- Generic labels like "button" or "image"
- Missing `accessibilityHint` for complex actions
- Incorrect `accessibilityTraits`

### 2. Point-Based Inspection

```bash
# Check specific element
axe describe-ui --point 200,400 --udid <UDID>
```

### 3. VoiceOver Simulation Script

```bash
#!/bin/bash
UDID="YOUR_SIMULATOR_UDID"

# Navigate through app elements
axe gesture swipe-from-left-edge --udid $UDID --post-delay 1.0
axe describe-ui --udid $UDID

axe tap -x 200 -y 400 --udid $UDID --post-delay 0.5
axe describe-ui --udid $UDID
```

## Automation Example

```bash
#!/bin/bash
UDID="YOUR_SIMULATOR_UDID"

# Login flow automation
echo "Starting login test..."

# Tap email field
axe tap -x 200 -y 300 --udid $UDID --post-delay 0.3

# Type email
axe type 'test@example.com' --udid $UDID --post-delay 0.3

# Tap password field
axe tap -x 200 -y 380 --udid $UDID --post-delay 0.3

# Type password (from stdin for security)
echo "password123" | axe type --stdin --udid $UDID --post-delay 0.3

# Tap login button
axe tap -x 200 -y 480 --udid $UDID --post-delay 2.0

# Verify result - check for expected element
axe describe-ui --udid $UDID | grep -q "Welcome" && echo "Login successful"
```

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Run iOS UI Tests
  run: |
    # Boot simulator
    xcrun simctl boot "iPhone 15"
    UDID=$(xcrun simctl list devices | grep "iPhone 15" | grep -oE '[A-F0-9-]{36}')

    # Install app
    xcrun simctl install $UDID ./build/MyApp.app
    xcrun simctl launch $UDID com.example.myapp

    # Run AXe tests
    axe describe-ui --udid $UDID > accessibility-report.txt

    # Record test
    axe record-video --udid $UDID --fps 10 --output test.mp4 &
    VIDEO_PID=$!

    # Run automation script
    ./test-scripts/login-flow.sh $UDID

    kill $VIDEO_PID
```

## Troubleshooting

### "Simulator not found"
```bash
# Ensure simulator is booted
xcrun simctl boot "iPhone 15"

# Get correct UDID
axe list-simulators
```

### "Permission denied"
```bash
# Grant accessibility permissions in System Preferences
# Security & Privacy > Privacy > Accessibility
```

### Commands not responding
```bash
# Ensure app is in foreground
xcrun simctl launch <UDID> <BUNDLE_ID>

# Add delays between commands
axe tap -x 100 -y 200 --post-delay 1.0 --udid <UDID>
```

## Best Practices

- Always use `--post-delay` between commands for reliability
- Store UDID in environment variable for scripts
- Use `describe-ui` before and after actions to verify state
- Record video during test runs for debugging
- Pipe sensitive text through stdin, not command line args
- Run accessibility audits as part of CI/CD pipeline
