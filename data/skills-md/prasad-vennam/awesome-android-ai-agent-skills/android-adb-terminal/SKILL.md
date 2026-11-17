---
name: android-adb-terminal
description: "Use when interacting with Android emulators or physical devices via ADB (Android Debug Bridge)."
category: operations
risk: low
source: community
date_added: "2026-03-31"
metadata:
  triggers:
    - "@adb"
    - "emulator-control"
    - "logcat"
    - "device-management"
    - "adb-shell"
---

# Android ADB Automation 📲⌨️

Expert commands and scripts for seamless Android device interaction and debugging.

## ⚡ When to Use

- **App Installation**: Installing APKs or bundles.
- **Logcat Debugging**: Filtering and searching system logs.
- **Device Interaction**: Typing text, tapping buttons, or swiping via shell.
- **Data Cleanup**: Clearing application data or cache.
- **Screen Captures**: Taking screenshots or recording videos.
- **Port Forwarding**: Connecting local servers to the device.

## 🛠️ Essential Commands

### 1. Device Discovery

```bash
adb devices
adb get-serialno
```

### 2. Package & Activity Management

- **Force Stop**: `adb shell am force-stop <package_name>`
- **Launch Activity**: `adb shell am start -n <package_name>/<activity_name>`
- **Clear Data**: `adb shell pm clear <package_name>`
- **List Installed Packages**: `adb shell pm list packages | grep <filter>`

### 3. Screen Interaction (Agent Favorites)

- **Type Text**: `adb shell input text "HelloAgent"`
- **Tap Coordinate**: `adb shell input tap 500 500`
- **Back Button**: `adb shell input keyevent 4`
- **Unlock Device**: `adb shell input keyevent 82`

### 4. File Transfers

```bash
adb push local_file /sdcard/remote_path
adb pull /sdcard/remote_path local_destination
```

## 📜 Advanced Automation

### Port Forwarding (Connect Host to Device)

```bash
adb forward tcp:8080 tcp:8080
```

### Port Reverse (Connect Device to Host - e.g. Local Backend)

```bash
adb reverse tcp:3000 tcp:3000
```

### Advanced Logcat Filtering

```bash
adb logcat -v time *:E # All errors with timestamps
adb logcat MyTag:D *:S # Show 'MyTag' debug only, silent for everything else
```

## 🧪 Scripting Patterns

### Wait for Device Online

```bash
adb wait-for-device
```

### Get Screen Dimensions

```bash
adb shell wm size
```

### Take and Pull Screenshot

```bash
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png ./screenshot.png
```

## 🔗 Related Resources

- [Android UI Verification Skill](../android_ui_verification/SKILL.md)
- [Official ADB Guide](https://developer.android.com/tools/adb)
