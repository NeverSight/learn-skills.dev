---
name: ios-debugger
description: "Build, run, and debug iOS apps via CLI without Xcode UI. Use when user wants to build iOS app, run on simulator, capture logs, take screenshots, or automate simulator interactions. Not for Swift code patterns (use apple-swift)."
compatibility: "Requires Xcode and iOS Simulator. Optionally XcodeBuildMCP for enhanced integration."
---

# ABOUTME: XcodeBuildMCP integration for building, running, and debugging iOS apps via CLI
# ABOUTME: Simulator control, UI interaction, log capture, screenshot automation

# iOS Debugger

## When to Invoke
- Build/run iOS apps without Xcode UI
- Automate simulator interactions
- Capture app logs programmatically
- UI testing via CLI
- CI/CD iOS workflows

## Capabilities
- Build and run on booted simulator
- Interact with simulator UI (tap, type, gestures)
- Capture and filter app logs
- Take screenshots
- Install/uninstall apps

## Prerequisites

```bash
# Ensure XcodeBuildMCP is available
# Check if simulator is booted
xcrun simctl list devices | grep Booted

# Boot simulator if needed
xcrun simctl boot "iPhone 16 Pro"
```

## Build and Run

```bash
# Build for simulator
xcodebuild -workspace MyApp.xcworkspace \
    -scheme MyApp \
    -sdk iphonesimulator \
    -destination 'platform=iOS Simulator,name=iPhone 16 Pro' \
    build

# Install app on simulator
xcrun simctl install booted path/to/MyApp.app

# Launch app
xcrun simctl launch booted com.example.myapp
```

## UI Interaction

```bash
# Tap at coordinates
xcrun simctl io booted tap 200 400

# Type text
xcrun simctl io booted type "Hello World"

# Swipe gesture (x1 y1 x2 y2 duration)
xcrun simctl io booted swipe 200 600 200 200 0.5

# Take screenshot
xcrun simctl io booted screenshot screenshot.png
```

## Log Capture

```bash
# Stream all logs from booted simulator
xcrun simctl spawn booted log stream --predicate 'processImagePath CONTAINS "MyApp"'

# Filter by subsystem
xcrun simctl spawn booted log stream --predicate 'subsystem == "com.example.myapp"'

# Capture logs to file
xcrun simctl spawn booted log stream \
    --predicate 'processImagePath CONTAINS "MyApp"' \
    > app.log &
```

## Common Workflows

### Reset Simulator
```bash
# Erase all data
xcrun simctl erase "iPhone 16 Pro"

# Shutdown and boot
xcrun simctl shutdown "iPhone 16 Pro"
xcrun simctl boot "iPhone 16 Pro"
```

## Tips
- Always check simulator is booted before commands
- Use `log stream` predicates to filter noise
- Coordinate-based taps are fragile (prefer accessibility IDs in XCTest)
- Capture screenshots for visual regression tests
- Use `xcrun simctl openurl` to test deep links

## Integration with Tests
```bash
# Run XCTests on simulator
xcodebuild test \
    -workspace App.xcworkspace \
    -scheme App \
    -destination 'platform=iOS Simulator,name=iPhone 16 Pro' \
    -resultBundlePath TestResults.xcresult
```
