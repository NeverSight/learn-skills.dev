---
name: xcode
description: Build, test, and manage Xcode projects and Swift packages. Use when the user mentions Xcode, iOS/macOS app development, simulators, Swift packages, or needs to build/test Apple platform apps. Triggers on "build", "run", "test", "simulator", "xcodebuild", "swift package", "iOS app", "macOS app".
allowed-tools: Bash(bunx:*,mcporter:*)
---

# Xcode Build MCP

Build, test, run, and manage Xcode projects and Swift packages via the XcodeBuildMCP server.

## When to Use

- User wants to build an iOS/macOS/watchOS/tvOS/visionOS app
- User wants to run tests on simulator or device
- User wants to launch an app on simulator or device
- User mentions "xcodebuild", "swift build", "swift test"
- User wants to scaffold a new iOS/macOS project
- User wants to interact with iOS simulator (tap, type, screenshot)
- User wants to capture logs from simulator or device
- User wants to discover Xcode projects in a directory

## Quick Reference

All tools are called via mcporter using the XcodeBuildMCP server:

```bash
bunx mcporter call --stdio "xcodebuildmcp" <tool_name> [args...]
```

Assumes `mcporter` and `xcodebuildmcp` are installed globally; `bunx` runs the installed binaries and does not fetch them.

## Session Defaults (IMPORTANT - Set First!)

Before using most build/test tools, you MUST set session defaults:

```bash
bunx mcporter call --stdio "xcodebuildmcp" session-set-defaults \
  projectPath="/path/to/Project.xcodeproj" \
  scheme="MyApp" \
  simulatorName="iPhone 16"
```

Or for a workspace:

```bash
bunx mcporter call --stdio "xcodebuildmcp" session-set-defaults \
  workspacePath="/path/to/Project.xcworkspace" \
  scheme="MyApp" \
  simulatorId="DEVICE_UDID"
```

Check current defaults:
```bash
bunx mcporter call --stdio "xcodebuildmcp" session-show-defaults
```

Clear defaults:
```bash
bunx mcporter call --stdio "xcodebuildmcp" session-clear-defaults all=true
```

## Discovery Tools

### Find Xcode Projects

```bash
bunx mcporter call --stdio "xcodebuildmcp" discover_projs workspaceRoot="$(pwd)"
```

### List Schemes

```bash
bunx mcporter call --stdio "xcodebuildmcp" list_schemes
```

### Doctor (Check Environment)

```bash
bunx mcporter call --stdio "xcodebuildmcp" doctor
```

## Simulator Tools

### List Simulators

```bash
bunx mcporter call --stdio "xcodebuildmcp" list_sims
```

### Boot Simulator

```bash
bunx mcporter call --stdio "xcodebuildmcp" boot_sim
```

### Open Simulator App

```bash
bunx mcporter call --stdio "xcodebuildmcp" open_sim
```

### Build for Simulator

```bash
bunx mcporter call --stdio "xcodebuildmcp" build_sim
```

### Build and Run on Simulator

```bash
bunx mcporter call --stdio "xcodebuildmcp" build_run_sim
```

### Run Tests on Simulator

```bash
bunx mcporter call --stdio "xcodebuildmcp" test_sim
```

### Get Built App Path (Simulator)

```bash
bunx mcporter call --stdio "xcodebuildmcp" get_sim_app_path platform="iOS Simulator"
```

### Install App on Simulator

```bash
bunx mcporter call --stdio "xcodebuildmcp" install_app_sim appPath="/path/to/App.app"
```

### Launch App on Simulator

```bash
bunx mcporter call --stdio "xcodebuildmcp" launch_app_sim bundleId="com.example.MyApp"
```

### Stop App on Simulator

```bash
bunx mcporter call --stdio "xcodebuildmcp" stop_app_sim bundleId="com.example.MyApp"
```

## Simulator UI Automation

### Take Screenshot

```bash
bunx mcporter call --stdio "xcodebuildmcp" screenshot
```

### Describe UI (Get View Hierarchy)

Gets precise frame coordinates for all visible elements - USE THIS before any UI interactions:

```bash
bunx mcporter call --stdio "xcodebuildmcp" describe_ui
```

### Tap

```bash
# Tap by coordinates (use describe_ui first to get coordinates)
bunx mcporter call --stdio "xcodebuildmcp" tap x=100 y=200

# Tap by accessibility ID
bunx mcporter call --stdio "xcodebuildmcp" tap id="myButton"

# Tap by label
bunx mcporter call --stdio "xcodebuildmcp" tap label="Submit"
```

### Long Press

```bash
bunx mcporter call --stdio "xcodebuildmcp" long_press x=100 y=200 duration=1000
```

### Swipe

```bash
bunx mcporter call --stdio "xcodebuildmcp" swipe x1=100 y1=400 x2=100 y2=100
```

### Gesture Presets

```bash
bunx mcporter call --stdio "xcodebuildmcp" gesture preset="scroll-down"
# Presets: scroll-up, scroll-down, scroll-left, scroll-right, 
#          swipe-from-left-edge, swipe-from-right-edge, 
#          swipe-from-top-edge, swipe-from-bottom-edge
```

### Type Text

```bash
bunx mcporter call --stdio "xcodebuildmcp" type_text text="Hello World"
```

### Press Button

```bash
bunx mcporter call --stdio "xcodebuildmcp" button buttonType="home"
# Types: apple-pay, home, lock, side-button, siri
```

### Key Press

```bash
bunx mcporter call --stdio "xcodebuildmcp" key_press keyCode=40  # Return key
# Common: 40=Return, 42=Backspace, 43=Tab, 44=Space
```

## Simulator Settings

### Set Appearance (Dark/Light Mode)

```bash
bunx mcporter call --stdio "xcodebuildmcp" set_sim_appearance mode="dark"
```

### Set Location

```bash
bunx mcporter call --stdio "xcodebuildmcp" set_sim_location latitude=37.7749 longitude=-122.4194
```

### Reset Location

```bash
bunx mcporter call --stdio "xcodebuildmcp" reset_sim_location
```

### Set Status Bar Network

```bash
bunx mcporter call --stdio "xcodebuildmcp" sim_statusbar dataNetwork="5g"
# Options: clear, hide, wifi, 3g, 4g, lte, lte-a, lte+, 5g, 5g+, 5g-uwb, 5g-uc
```

### Erase Simulator

```bash
bunx mcporter call --stdio "xcodebuildmcp" erase_sims shutdownFirst=true
```

## Simulator Log Capture

### Start Log Capture

```bash
bunx mcporter call --stdio "xcodebuildmcp" start_sim_log_cap bundleId="com.example.MyApp"
# Returns a logSessionId
```

### Stop Log Capture

```bash
bunx mcporter call --stdio "xcodebuildmcp" stop_sim_log_cap logSessionId="SESSION_ID"
```

## Video Recording

### Start Recording

```bash
bunx mcporter call --stdio "xcodebuildmcp" record_sim_video start=true
```

### Stop Recording

```bash
bunx mcporter call --stdio "xcodebuildmcp" record_sim_video stop=true outputFile="/path/to/output.mp4"
```

## Physical Device Tools

### List Connected Devices

```bash
bunx mcporter call --stdio "xcodebuildmcp" list_devices
```

### Build for Device

```bash
bunx mcporter call --stdio "xcodebuildmcp" build_device
```

### Test on Device

```bash
bunx mcporter call --stdio "xcodebuildmcp" test_device
```

### Install App on Device

```bash
bunx mcporter call --stdio "xcodebuildmcp" install_app_device appPath="/path/to/App.app"
```

### Launch App on Device

```bash
bunx mcporter call --stdio "xcodebuildmcp" launch_app_device bundleId="com.example.MyApp"
```

### Stop App on Device

```bash
bunx mcporter call --stdio "xcodebuildmcp" stop_app_device processId=12345
```

### Device Log Capture

```bash
# Start
bunx mcporter call --stdio "xcodebuildmcp" start_device_log_cap bundleId="com.example.MyApp"

# Stop
bunx mcporter call --stdio "xcodebuildmcp" stop_device_log_cap logSessionId="SESSION_ID"
```

## macOS Tools

### Build macOS App

```bash
bunx mcporter call --stdio "xcodebuildmcp" build_macos
```

### Build and Run macOS App

```bash
bunx mcporter call --stdio "xcodebuildmcp" build_run_macos
```

### Test macOS App

```bash
bunx mcporter call --stdio "xcodebuildmcp" test_macos
```

### Get macOS App Path

```bash
bunx mcporter call --stdio "xcodebuildmcp" get_mac_app_path
```

### Launch macOS App

```bash
bunx mcporter call --stdio "xcodebuildmcp" launch_mac_app appPath="/path/to/App.app"
```

### Stop macOS App

```bash
bunx mcporter call --stdio "xcodebuildmcp" stop_mac_app appName="MyApp"
```

## Swift Package Tools

### Build Package

```bash
bunx mcporter call --stdio "xcodebuildmcp" swift_package_build packagePath="$(pwd)"
```

### Test Package

```bash
bunx mcporter call --stdio "xcodebuildmcp" swift_package_test packagePath="$(pwd)"
```

### Run Package Executable

```bash
bunx mcporter call --stdio "xcodebuildmcp" swift_package_run packagePath="$(pwd)"
```

### Clean Package

```bash
bunx mcporter call --stdio "xcodebuildmcp" swift_package_clean packagePath="$(pwd)"
```

### List Running Packages

```bash
bunx mcporter call --stdio "xcodebuildmcp" swift_package_list
```

### Stop Package Process

```bash
bunx mcporter call --stdio "xcodebuildmcp" swift_package_stop pid=12345
```

## Project Scaffolding

### Create New iOS Project

```bash
bunx mcporter call --stdio "xcodebuildmcp" scaffold_ios_project \
  projectName="MyApp" \
  outputPath="$(pwd)" \
  bundleIdentifier="com.example.myapp"
```

### Create New macOS Project

```bash
bunx mcporter call --stdio "xcodebuildmcp" scaffold_macos_project \
  projectName="MyMacApp" \
  outputPath="$(pwd)" \
  bundleIdentifier="com.example.mymacapp"
```

## Utility Tools

### Clean Build

```bash
bunx mcporter call --stdio "xcodebuildmcp" clean
```

### Show Build Settings

```bash
bunx mcporter call --stdio "xcodebuildmcp" show_build_settings
```

### Get Bundle ID from App

```bash
bunx mcporter call --stdio "xcodebuildmcp" get_app_bundle_id appPath="/path/to/App.app"
```

## Typical Workflows

### Build and Test iOS App on Simulator

```bash
# 1. Discover projects
bunx mcporter call --stdio "xcodebuildmcp" discover_projs workspaceRoot="$(pwd)"

# 2. List simulators
bunx mcporter call --stdio "xcodebuildmcp" list_sims

# 3. Set session defaults
bunx mcporter call --stdio "xcodebuildmcp" session-set-defaults \
  projectPath="$(pwd)/MyApp.xcodeproj" \
  scheme="MyApp" \
  simulatorName="iPhone 16"

# 4. Build and run
bunx mcporter call --stdio "xcodebuildmcp" build_run_sim

# 5. Run tests
bunx mcporter call --stdio "xcodebuildmcp" test_sim
```

### UI Testing Flow

```bash
# 1. Build and launch app
bunx mcporter call --stdio "xcodebuildmcp" build_run_sim

# 2. Get UI hierarchy (ALWAYS do this before interacting)
bunx mcporter call --stdio "xcodebuildmcp" describe_ui

# 3. Take screenshot for visual reference
bunx mcporter call --stdio "xcodebuildmcp" screenshot

# 4. Interact with elements using coordinates from describe_ui
bunx mcporter call --stdio "xcodebuildmcp" tap x=187 y=423

# 5. Type text
bunx mcporter call --stdio "xcodebuildmcp" type_text text="test@example.com"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No project/workspace set | Session defaults not configured | Run `session-set-defaults` first |
| Simulator not found | Invalid simulator name | Run `list_sims` to get valid names |
| Build failed | Code errors or config issues | Check build output, run `doctor` |
| App not installed | Build didn't complete | Run `build_sim` before `launch_app_sim` |

## Tips

1. **Always set session defaults first** - Most tools require project/scheme/simulator to be set
2. **Use describe_ui before UI interactions** - Never guess coordinates from screenshots
3. **Check doctor for environment issues** - Run `doctor` if tools aren't working
4. **Use preferXcodebuild=true** if incremental builds fail - Falls back to standard xcodebuild
