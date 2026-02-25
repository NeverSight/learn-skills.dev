---
name: swiftui-simulator-ui
description: Run SwiftUI apps in iOS Simulator and capture screenshots for visual verification. Use when building UI, reviewing layouts, validating designs, or when you need to see what SwiftUI code looks like. Essential for any UI work requiring visual feedback.
allowed-tools: Bash, Read, Grep, Glob, Write
---

# SwiftUI Simulator UI Feedback Loop

Build, run, and capture SwiftUI apps in iOS Simulator for visual verification. This skill enables AI agents to see what their UI code produces.

## When to Use This Skill

Use this skill when:
- Building or modifying SwiftUI views and need visual verification
- Reviewing UI layouts, spacing, colors, or typography
- Validating designs against specifications
- Debugging visual issues (clipping, alignment, overlapping)
- Capturing screenshots for documentation or handoffs
- Testing different device sizes or appearances (dark mode, Dynamic Type)

## Prerequisites

Before starting:
1. **Xcode installed** with iOS Simulator support
2. **Project builds successfully** (run `xcodebuild -list` to verify)
3. **At least one iOS Simulator** available (`xcrun simctl list devices available`)

## Quick Start (5-Step Workflow)

### Step 1: Find Your Project Structure

```bash
# For .xcworkspace (if using CocoaPods/SPM packages)
xcodebuild -workspace /path/to/App.xcworkspace -list

# For .xcodeproj
xcodebuild -project /path/to/App.xcodeproj -list

# Output shows available schemes - pick the one you want to run
```

### Step 2: Find Available Simulators

```bash
# List available iPhone simulators
xcrun simctl list devices available | grep iPhone

# Get UDID for a specific device (e.g., iPhone 16)
xcrun simctl list devices available | sed -nE '/iPhone 16/{s/.*\(([A-F0-9-]+)\).*/\1/p; q;}'
```

### Step 3: Build the App

```bash
# Set your variables
PROJECT_PATH="/path/to/App.xcodeproj"  # or .xcworkspace
SCHEME="YourScheme"
DEVICE_NAME="iPhone 16"
DERIVED_DATA="/tmp/MyAppBuild"

# Get UDID
UDID=$(xcrun simctl list devices available | sed -nE "/$DEVICE_NAME/{s/.*\(([A-F0-9-]+)\).*/\1/p; q;}")

# Build
xcodebuild \
  -project "$PROJECT_PATH" \
  -scheme "$SCHEME" \
  -destination "platform=iOS Simulator,id=$UDID" \
  -derivedDataPath "$DERIVED_DATA" \
  build
```

### Step 4: Install and Launch

```bash
# Find the built .app
APP_PATH=$(find "$DERIVED_DATA" -name "*.app" -type d | head -1)

# Boot simulator if needed
xcrun simctl boot "$UDID" 2>/dev/null || true

# Install
xcrun simctl install "$UDID" "$APP_PATH"

# Launch (get bundle ID from Info.plist or build settings)
BUNDLE_ID="com.example.yourapp"
xcrun simctl launch "$UDID" "$BUNDLE_ID"
```

### Step 5: Capture Screenshot

```bash
# Create output directory
mkdir -p /tmp/UIScreenshots

# Take screenshot
xcrun simctl io "$UDID" screenshot "/tmp/UIScreenshots/screenshot-$(date +%Y%m%d-%H%M%S).png"

# The path is printed - use this to view the screenshot
```

## Complete Workflow Script

Copy and adapt this script for your project:

```bash
#!/usr/bin/env bash
set -euo pipefail

# ============ CONFIGURATION (EDIT THESE) ============
PROJECT_PATH="${PROJECT_PATH:-/path/to/App.xcodeproj}"  # or .xcworkspace
SCHEME="${SCHEME:-YourScheme}"
BUNDLE_ID="${BUNDLE_ID:-com.example.yourapp}"
DEVICE_NAME="${DEVICE_NAME:-iPhone 16}"
DERIVED_DATA="${DERIVED_DATA:-/tmp/AppBuild}"
SCREENSHOT_DIR="${SCREENSHOT_DIR:-/tmp/UIScreenshots}"
# ====================================================

# Resolve simulator UDID
resolve_udid() {
  xcrun simctl list devices available | sed -nE "/$1/{s/.*\(([A-F0-9-]+)\).*/\1/p; q;}"
}

UDID=$(resolve_udid "$DEVICE_NAME")
if [[ -z "$UDID" ]]; then
  echo "error: Simulator '$DEVICE_NAME' not found. Available devices:"
  xcrun simctl list devices available | grep iPhone
  exit 1
fi

echo "Using simulator: $DEVICE_NAME ($UDID)"

# Boot simulator
if ! xcrun simctl list devices booted | grep -q "$UDID"; then
  echo "Booting simulator..."
  xcrun simctl boot "$UDID" 2>/dev/null || true
  sleep 2
fi

# Build
echo "Building..."
xcodebuild \
  -project "$PROJECT_PATH" \
  -scheme "$SCHEME" \
  -destination "platform=iOS Simulator,id=$UDID" \
  -derivedDataPath "$DERIVED_DATA" \
  -quiet \
  build

# Find app
APP_PATH=$(find "$DERIVED_DATA" -name "*.app" -type d | head -1)
if [[ ! -d "$APP_PATH" ]]; then
  echo "error: Built app not found in $DERIVED_DATA"
  exit 1
fi

# Install
echo "Installing..."
xcrun simctl install "$UDID" "$APP_PATH"

# Terminate if running, then launch
xcrun simctl terminate "$UDID" "$BUNDLE_ID" 2>/dev/null || true
xcrun simctl launch "$UDID" "$BUNDLE_ID"

echo "Launched $SCHEME on $DEVICE_NAME"

# Screenshot
mkdir -p "$SCREENSHOT_DIR"
SCREENSHOT_PATH="$SCREENSHOT_DIR/$(date +%Y%m%d-%H%M%S).png"
sleep 1  # Wait for app to render
xcrun simctl io "$UDID" screenshot "$SCREENSHOT_PATH"

echo "Screenshot saved: $SCREENSHOT_PATH"
```

## Advanced Patterns

### Pattern 1: Navigate to Specific Screen via Deep Link

```bash
# Launch app with deep link
xcrun simctl openurl "$UDID" "yourapp://settings/profile"

# Wait and screenshot
sleep 1
xcrun simctl io "$UDID" screenshot /tmp/profile-screen.png
```

### Pattern 2: Configure App State via UserDefaults

```bash
# Write defaults before launch
xcrun simctl spawn "$UDID" defaults write "$BUNDLE_ID" ShowOnboarding -bool false
xcrun simctl spawn "$UDID" defaults write "$BUNDLE_ID" DebugMode -bool true
xcrun simctl spawn "$UDID" defaults write "$BUNDLE_ID" MockUserName -string "Test User"

# Terminate and relaunch to pick up changes
xcrun simctl terminate "$UDID" "$BUNDLE_ID"
xcrun simctl launch "$UDID" "$BUNDLE_ID"
```

### Pattern 3: Test Different Appearances

```bash
# Enable dark mode
xcrun simctl ui "$UDID" appearance dark
sleep 0.5
xcrun simctl io "$UDID" screenshot /tmp/dark-mode.png

# Enable light mode
xcrun simctl ui "$UDID" appearance light
sleep 0.5
xcrun simctl io "$UDID" screenshot /tmp/light-mode.png
```

### Pattern 4: Override Status Bar for Clean Screenshots

```bash
# Set time to 9:41, full battery, WiFi
xcrun simctl status_bar "$UDID" override \
  --time "9:41" \
  --batteryLevel 100 \
  --batteryState charged \
  --dataNetwork wifi \
  --wifiBars 3

xcrun simctl io "$UDID" screenshot /tmp/clean-screenshot.png

# Clear overrides
xcrun simctl status_bar "$UDID" clear
```

### Pattern 5: Test Multiple Device Sizes

```bash
# Test on different devices
for DEVICE in "iPhone SE (3rd generation)" "iPhone 16" "iPhone 16 Pro Max"; do
  UDID=$(xcrun simctl list devices available | sed -nE "/$DEVICE/{s/.*\(([A-F0-9-]+)\).*/\1/p; q;}")
  if [[ -n "$UDID" ]]; then
    xcrun simctl boot "$UDID" 2>/dev/null || true
    xcrun simctl install "$UDID" "$APP_PATH"
    xcrun simctl launch "$UDID" "$BUNDLE_ID"
    sleep 2
    xcrun simctl io "$UDID" screenshot "/tmp/${DEVICE// /-}.png"
    xcrun simctl shutdown "$UDID"
  fi
done
```

### Pattern 6: Preview Lab Target (Isolated UI Testing)

Create a dedicated target for UI preview:

```swift
// In a PreviewLab target
@main
struct PreviewLabApp: App {
    var body: some Scene {
        WindowGroup {
            // Show specific view based on launch argument
            switch ProcessInfo.processInfo.environment["PREVIEW_VIEW"] {
            case "settings":
                SettingsView()
            case "profile":
                ProfileView()
            default:
                ContentView()
            }
        }
    }
}
```

Launch with environment:

```bash
# Set environment variable
xcrun simctl spawn "$UDID" launchctl setenv PREVIEW_VIEW settings

# Launch
xcrun simctl launch "$UDID" "$BUNDLE_ID"
```

### Pattern 7: Record Video of Interaction

```bash
# Start recording in background
xcrun simctl io "$UDID" recordVideo /tmp/recording.mp4 &
RECORD_PID=$!

# Wait for interaction (or interact manually)
sleep 5

# Stop recording
kill -INT $RECORD_PID
```

## Finding Bundle ID

If you don't know the bundle ID:

```bash
# From build settings
xcodebuild -project "$PROJECT_PATH" -scheme "$SCHEME" -showBuildSettings | grep PRODUCT_BUNDLE_IDENTIFIER

# From installed app
xcrun simctl listapps "$UDID" | grep -A1 CFBundleIdentifier

# From .app Info.plist after build
/usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" "$APP_PATH/Info.plist"
```

## Troubleshooting

### Build Fails: "No matching destination"

```bash
# Check available destinations
xcodebuild -project "$PROJECT_PATH" -scheme "$SCHEME" -showDestinations

# Use exact simulator name from list
xcrun simctl list devices available
```

### Simulator Won't Boot

```bash
# Check current state
xcrun simctl list devices | grep -A5 "== Devices =="

# Force shutdown and reboot
xcrun simctl shutdown "$UDID"
xcrun simctl boot "$UDID"

# If still failing, reset simulator
xcrun simctl erase "$UDID"
```

### App Won't Install

```bash
# Check if app is built correctly
ls -la "$APP_PATH"

# Check architecture (must be x86_64 or arm64 for sim)
file "$APP_PATH/$(basename "$APP_PATH" .app)"

# Check minimum deployment target
/usr/libexec/PlistBuddy -c "Print MinimumOSVersion" "$APP_PATH/Info.plist"
```

### Screenshot Shows Wrong Simulator

When multiple simulators are booted:

```bash
# List booted simulators
xcrun simctl list devices booted

# Always specify UDID explicitly
xcrun simctl io "$UDID" screenshot /tmp/screenshot.png

# Or shutdown other simulators
xcrun simctl shutdown all
xcrun simctl boot "$UDID"
```

### App Launches but UI Doesn't Load

```bash
# Check console output
xcrun simctl launch --console "$UDID" "$BUNDLE_ID"

# Stream logs
xcrun simctl spawn "$UDID" log stream --predicate 'processImagePath CONTAINS "YourApp"' --level debug
```

### Screenshot is Black

```bash
# Wait longer for app to render
sleep 2
xcrun simctl io "$UDID" screenshot /tmp/screenshot.png

# Ensure simulator window is visible (not minimized)
# Or run in headless mode properly
```

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `PROJECT_PATH` | Path to .xcodeproj or .xcworkspace | Required |
| `SCHEME` | Xcode build scheme | Required |
| `BUNDLE_ID` | App bundle identifier | Required |
| `DEVICE_NAME` | Simulator device name | `iPhone 16` |
| `DEVICE_UDID` | Specific simulator UDID | Auto-resolved |
| `DERIVED_DATA` | Build output directory | `/tmp/AppBuild` |
| `SCREENSHOT_DIR` | Screenshot output directory | `/tmp/UIScreenshots` |

## Detailed References

- **references/simulator-commands.md** - Complete `xcrun simctl` command reference
- **references/xcodebuild-patterns.md** - Build patterns and configurations
- **references/troubleshooting.md** - Extended troubleshooting guide
- **assets/run_app.sh** - Reusable run script template
- **assets/screenshot.sh** - Standalone screenshot script

## Integration with Handoffs

When using this skill for UI work:

1. Run the UI feedback loop after making changes
2. Capture a screenshot
3. Include the screenshot path in your handoff file
4. Example handoff entry:

```markdown
## Progress

- [x] Implemented ProfileView header
- Screenshot: `/tmp/UIScreenshots/20250131-143022.png`
- Notes: Layout matches spec, tested on iPhone 16 and iPhone SE
```

## Key Principles

1. **Always verify visually** - Don't assume UI code is correct; run it and see
2. **Use consistent device** - Pick one simulator and stick with it for consistency
3. **Clean screenshots** - Override status bar for professional captures
4. **Test edge cases** - Dark mode, small screens, Dynamic Type
5. **Document with screenshots** - Include paths in handoffs for traceability
