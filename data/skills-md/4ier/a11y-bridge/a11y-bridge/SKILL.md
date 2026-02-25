---
name: a11y-bridge
description: Control Android devices via Accessibility Service HTTP bridge. 100x faster than screencap + uiautomator dump. Read UI tree in 50ms, click elements by text/id/description. Use when automating Android apps, controlling a phone via ADB, or building an AI-powered phone agent. Replaces the slow screenshot → parse → coordinate-tap cycle with instant semantic access.
---

# A11y Bridge — Android Accessibility HTTP Bridge

Control Android devices through a 16KB Accessibility Service that exposes the live UI tree over HTTP (`localhost:7333`). ~50ms to read any screen, click by text without coordinate math.

## Prerequisites

- Android device connected via USB with USB debugging enabled
- ADB installed and accessible in PATH
- Android SDK (build-tools 34, platform android-34) — only needed to build from source

## Setup

### Install pre-built APK

Download the latest APK from [Releases](https://github.com/4ier/a11y-bridge/releases), then:

```bash
# Install
adb install openclaw-a11y.apk

# Enable accessibility service
adb shell settings put secure enabled_accessibility_services \
  com.openclaw.a11y/.ClawAccessibilityService
adb shell settings put secure accessibility_enabled 1

# Forward port
adb forward tcp:7333 tcp:7333

# Verify
curl http://localhost:7333/ping
```

### Build from source (optional)

```bash
chmod +x build.sh && ./build.sh
```

## Usage

### Read screen (~50ms)

```bash
# Full UI tree
curl http://localhost:7333/screen

# Compact mode (only interactive/text elements)
curl 'http://localhost:7333/screen?compact'
```

Returns JSON with all UI elements: text, bounds, clickable, editable, etc.

### Click by text

```bash
# Click element containing "Settings"
curl -X POST http://localhost:7333/click \
  -H "Content-Type: application/json" \
  -d '{"text": "Settings"}'

# Click by resource ID
curl -X POST http://localhost:7333/click -d '{"id": "com.app:id/send"}'

# Click by content description
curl -X POST http://localhost:7333/click -d '{"desc": "Navigate up"}'
```

### Tap coordinates

```bash
curl -X POST http://localhost:7333/tap -d '{"x": 540, "y": 960}'
```

### Health check

```bash
curl http://localhost:7333/ping
```

## Workflow

1. **Read**: `curl http://localhost:7333/screen` → JSON with all UI elements
2. **Find**: Locate target element by text/role in the JSON response
3. **Act**: `curl -X POST /click -d '{"text":"Send"}'` → click by text, no coordinates
4. **Repeat**

## Multi-device support

When multiple devices are connected, specify the target with `-s <serial>` for all ADB commands:

```bash
adb -s <serial> forward tcp:7333 tcp:7333
```

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ping` | GET | Health check |
| `/screen` | GET | Full UI tree as JSON. Add `?compact` for interactive elements only |
| `/click` | POST | Click by `text`, `id`, or `desc` (JSON body) |
| `/tap` | POST | Tap coordinates `x`, `y` (JSON body) |

## Performance

| | uiautomator dump | A11y Bridge |
|---|---|---|
| Read UI | 3-5 seconds | ~50ms |
| Click | Calculate bounds → `input tap x y` | `{"text": "OK"}` |
| Full cycle | 5-8 seconds | 100-200ms |

## Fallback

If the A11y Bridge service is not running (check with `/ping`), fall back to traditional ADB commands:

```bash
adb shell uiautomator dump /sdcard/ui.xml && adb pull /sdcard/ui.xml
adb shell input tap <x> <y>
```
