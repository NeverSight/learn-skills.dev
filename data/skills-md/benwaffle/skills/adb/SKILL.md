---
name: adb
description: Android Debug Bridge (ADB) assistant for inspecting, debugging, and managing Android devices
user-invocable: true
allowed-tools:
  - Bash(adb bugreport*)
  - Bash(adb devices*)
  - Bash(adb get-serialno*)
  - Bash(adb get-state*)
  - Bash(adb logcat*)
  - Bash(adb pull*)
  - Bash(adb shell cat*)
  - Bash(adb shell content query*)
  - Bash(adb shell date*)
  - Bash(adb shell df*)
  - Bash(adb shell dumpsys*)
  - Bash(adb shell find*)
  - Bash(adb shell getprop*)
  - Bash(adb shell grep*)
  - Bash(adb shell id*)
  - Bash(adb shell ifconfig*)
  - Bash(adb shell ip *)
  - Bash(adb shell ls*)
  - Bash(adb shell mount*)
  - Bash(adb shell netstat*)
  - Bash(adb shell pm list*)
  - Bash(adb shell ps*)
  - Bash(adb shell screencap*)
  - Bash(adb shell service list*)
  - Bash(adb shell settings get*)
  - Bash(adb shell stat*)
  - Bash(adb shell top*)
  - Bash(adb shell uname*)
  - Bash(adb shell uptime*)
  - Bash(adb shell wm*)
  - Bash(adb version*)
---

# ADB — Android Debug Bridge Skill

You are an expert Android developer and debugger with deep knowledge of ADB commands.

## Safe Commands (Auto-Approved)

The following read-only commands run without user confirmation:

| Category | Commands |
|---|---|
| **Device info** | `adb devices`, `adb get-state`, `adb get-serialno`, `adb version` |
| **System properties** | `adb shell getprop` |
| **Package listing** | `adb shell pm list packages`, `adb shell pm list features` |
| **Process info** | `adb shell ps`, `adb shell top -n 1` |
| **System services** | `adb shell dumpsys`, `adb shell service list` |
| **Settings (read)** | `adb shell settings get` |
| **Filesystem (read)** | `adb shell ls`, `adb shell cat`, `adb shell df`, `adb shell stat`, `adb shell find` |
| **Display info** | `adb shell wm size`, `adb shell wm density` |
| **Logs** | `adb logcat -d`, `adb bugreport` |
| **Screenshots** | `adb shell screencap` |
| **Pull files** | `adb pull` |
| **Network** | `adb shell netstat`, `adb shell ifconfig`, `adb shell ip` |
| **Content queries** | `adb shell content query` |

## Dangerous Commands (Require User Confirmation)

These commands modify device state and will prompt the user before running:

- `adb install` / `adb uninstall` — Install or remove apps
- `adb push` — Write files to device
- `adb reboot` — Reboot device
- `adb root` / `adb remount` — Elevate privileges or remount partitions
- `adb shell rm` — Delete files on device
- `adb shell am force-stop` / `adb shell am kill` — Stop running apps
- `adb shell pm clear` — Clear app data
- `adb shell settings put` — Modify system settings
- `adb shell input` — Inject taps, swipes, or key events
- `adb shell cmd` — Arbitrary command execution
- `adb shell setprop` — Modify system properties
- `adb shell svc` — Control system services (wifi, data, power)

## Guidelines

1. **Always start by checking device connectivity** with `adb devices` before running other commands.
2. **For logcat**, prefer `adb logcat -d` (dump and exit) over streaming `adb logcat` to avoid hanging. Use filters like `adb logcat -d -s TAG` or `adb logcat -d *:E` to narrow output.
3. **For top**, use `adb shell top -n 1` (single snapshot) instead of continuous mode.
4. **When targeting a specific device**, use `adb -s <serial>` if multiple devices are connected.
5. **Before destructive actions**, explain what will happen and why, then wait for user confirmation.

## Common Workflows

### Debug a crash
1. `adb devices` — confirm device connected
2. `adb logcat -d *:E` — check recent errors
3. `adb logcat -d -s AndroidRuntime` — find crash stack traces
4. `adb shell dumpsys activity activities` — check activity state

### Inspect an app
1. `adb shell pm list packages | grep <name>` — find package name
2. `adb shell dumpsys package <pkg>` — full package info
3. `adb shell dumpsys meminfo <pkg>` — memory usage
4. `adb shell ps -A | grep <pkg>` — check if running

### Check device health
1. `adb shell getprop ro.build.display.id` — build info
2. `adb shell df` — disk usage
3. `adb shell dumpsys battery` — battery status
4. `adb shell dumpsys cpuinfo` — CPU usage
5. `adb shell top -n 1` — process snapshot

### Capture a screenshot
1. `adb shell screencap /sdcard/screenshot.png`
2. `adb pull /sdcard/screenshot.png ./screenshot.png`
