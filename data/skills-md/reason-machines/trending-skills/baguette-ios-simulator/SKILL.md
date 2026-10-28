---
name: baguette-ios-simulator
description: Headless iOS Simulator manager with host-side HID input injection, 60fps streaming, and device farm web UI for iOS 26
triggers:
  - "control iOS simulator headlessly"
  - "inject touch input into simulator"
  - "stream simulator screen"
  - "manage simulator device farm"
  - "tap swipe gesture simulator programmatically"
  - "boot simulator without GUI"
  - "simulator web UI dashboard"
  - "simulate multi-finger pinch zoom on iOS"
---

# Baguette iOS Simulator Manager

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Baguette is a Swift CLI tool that creates, boots, and shuts down iOS Simulator devices, streams their screens at 60fps, and injects taps/swipes/multi-finger gestures entirely headlessly — no Simulator.app GUI required. It also serves a self-contained web UI for single-device and multi-device (farm) control.

## Requirements

- Apple Silicon Mac only
- macOS 15+
- Xcode 26 (links against private SimulatorKit/CoreSimulator frameworks)

## Install

```bash
brew install tddworks/tap/baguette
```

### Build from Source

```bash
git clone https://github.com/tddworks/baguette
cd baguette
make           # release build via ./build.sh
swift test     # run the test suite
```

## Key CLI Commands

### Device Management

```bash
# List all simulators (default + custom sets)
baguette list

# Boot a simulator headlessly (no Simulator.app window)
baguette boot --udid <UDID>

# Shutdown a simulator
baguette shutdown --udid <UDID>
```

### Screen Streaming

```bash
# Stream frames to stdout as MJPEG (default)
baguette stream --udid <UDID> --fps 60 --format mjpeg

# Stream as H.264/AVCC
baguette stream --udid <UDID> --fps 60 --format avcc

# Pipe MJPEG to ffplay for local preview
baguette stream --udid <UDID> --fps 30 --format mjpeg | ffplay -i -
```

### One-Shot Gesture Input

Coordinates are in **device points**; `--width`/`--height` are the simulator screen size in points.

```bash
# Tap at a point
baguette tap --udid <UDID> --x 219 --y 478 --width 438 --height 954

# Tap with custom duration
baguette tap --udid <UDID> --x 219 --y 478 --width 438 --height 954 --duration 0.1

# Swipe from top to bottom (scroll down)
baguette swipe --udid <UDID> \
  --startX 219 --startY 190 \
  --endX 219 --endY 760 \
  --width 438 --height 954

# Pinch to zoom in (startSpread < endSpread)
baguette pinch --udid <UDID> \
  --cx 219 --cy 478 \
  --startSpread 60 --endSpread 200 \
  --width 438 --height 954

# Two-finger pan
baguette pan --udid <UDID> \
  --x1 175 --y1 478 \
  --x2 263 --y2 478 \
  --dx 0 --dy -100 \
  --width 438 --height 954

# Hardware buttons
baguette press --udid <UDID> --button home
baguette press --udid <UDID> --button lock
```

### Streaming Gesture Input (stdin JSON)

For real-time or scripted gesture sequences, pipe newline-delimited JSON to `baguette input`:

```bash
baguette input --udid <UDID>
```

Each line gets an ack: `{"ok":true}` or `{"ok":false,"error":"..."}`.

### Web UI Server

```bash
# Start the web server (default port 8421)
baguette serve

# Custom port and host
baguette serve --port 9000 --host 0.0.0.0

# Custom device set
baguette serve --port 8421 --device-set /path/to/device-set

# Open single-device dashboard
open http://localhost:8421/simulators

# Open multi-device farm dashboard
open http://localhost:8421/farm
```

### DeviceKit Chrome/Bezel Data

```bash
# Print bezel layout JSON for a booted device
baguette chrome layout --udid <UDID>

# Write composite PNG (device screenshot + bezel) to stdout
baguette chrome composite --udid <UDID> > screenshot.png

# By device name (no UDID needed)
baguette chrome layout --device-name "iPhone 17 Pro"
baguette chrome composite --device-name "iPhone 17 Pro" > iphone17pro_bezel.png
```

## Wire Protocol — Streaming Input via stdin

Send newline-delimited JSON to `baguette input --udid <UDID>`:

```json
{"type":"tap", "x":219, "y":478, "width":438, "height":954, "duration":0.05}

{"type":"swipe", "startX":219, "startY":760, "endX":219, "endY":190, "width":438, "height":954, "duration":0.3}

{"type":"touch1-down", "x":219, "y":478, "width":438, "height":954}
{"type":"touch1-move", "x":225, "y":485, "width":438, "height":954}
{"type":"touch1-up",   "x":225, "y":485, "width":438, "height":954}

{"type":"touch2-down", "x1":175, "y1":478, "x2":263, "y2":478, "width":438, "height":954}
{"type":"touch2-move", "x1":150, "y1":478, "x2":288, "y2":478, "width":438, "height":954}
{"type":"touch2-up",   "x1":150, "y1":478, "x2":288, "y2":478, "width":438, "height":954}

{"type":"pinch", "cx":219, "cy":478, "startSpread":60, "endSpread":200, "width":438, "height":954}

{"type":"button", "button":"home"}
{"type":"button", "button":"lock"}

{"type":"scroll", "deltaX":0, "deltaY":-50}
```

## WebSocket Protocol (for Web UI / Custom Clients)

Connect to `ws://localhost:8421/simulators/<UDID>/stream?format=mjpeg` (or `avcc`).

### Server → Client (binary frames)

- **MJPEG**: raw JPEG bytes per message
- **AVCC**: 1-byte tag prefix:
  - `0x01` — avcC description
  - `0x02` — keyframe
  - `0x03` — delta frame
  - `0x04` — JPEG seed frame (renders before H.264 IDR)

### Client → Server (text JSON)

```json
{"type":"set_bitrate", "bps": 2000000}
{"type":"set_fps",     "fps": 30}
{"type":"set_scale",   "scale": 0.5}
{"type":"force_idr"}
{"type":"snapshot"}
```

Gesture input messages (same format as stdin wire protocol above) are also accepted over the WebSocket.

## Web UI Routes

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Redirects → `/simulators` |
| `GET` | `/simulators` | Device list HTML |
| `GET` | `/simulators.json` | `{running: [...], available: [...]}` |
| `GET` | `/simulators/:udid` | Stream page HTML |
| `POST` | `/simulators/:udid/boot` | Boot device |
| `POST` | `/simulators/:udid/shutdown` | Shutdown device |
| `GET` | `/simulators/:udid/chrome.json` | Bezel layout JSON |
| `GET` | `/simulators/:udid/bezel.png` | Rasterized bezel PNG |
| `WS` | `/simulators/:udid/stream` | Live stream + input |
| `GET` | `/farm` | Multi-device farm HTML |

## Code Examples

### Scripting Gestures from Swift

```swift
import Foundation

// Build a gesture sequence as newline-delimited JSON
func makeGestureScript() -> String {
    let gestures: [[String: Any]] = [
        // Boot sequence: tap the app icon
        ["type": "tap", "x": 100, "y": 200, "width": 390, "height": 844, "duration": 0.05],
        // Scroll down in a list
        ["type": "swipe", "startX": 195, "startY": 600,
         "endX": 195, "endY": 200, "width": 390, "height": 844, "duration": 0.4],
        // Pinch to zoom
        ["type": "pinch", "cx": 195, "cy": 422,
         "startSpread": 50, "endSpread": 180, "width": 390, "height": 844],
        // Press home
        ["type": "button", "button": "home"]
    ]
    return gestures.compactMap { dict -> String? in
        guard let data = try? JSONSerialization.data(withJSONObject: dict) else { return nil }
        return String(data: data, encoding: .utf8)
    }.joined(separator: "\n")
}

// Run baguette input with the script
func runGestureScript(udid: String, script: String) async throws {
    let process = Process()
    process.executableURL = URL(fileURLWithPath: "/usr/local/bin/baguette")
    process.arguments = ["input", "--udid", udid]

    let inputPipe = Pipe()
    let outputPipe = Pipe()
    process.standardInput = inputPipe
    process.standardOutput = outputPipe

    try process.run()

    let inputData = (script + "\n").data(using: .utf8)!
    inputPipe.fileHandleForWriting.write(inputData)
    inputPipe.fileHandleForWriting.closeFile()

    process.waitUntilExit()

    let outputData = outputPipe.fileHandleForReading.readDataToEndOfFile()
    let acks = String(data: outputData, encoding: .utf8) ?? ""
    print("Acks:\n\(acks)")
}
```

### Listing and Booting Simulators

```swift
import Foundation

struct SimulatorInfo: Codable {
    let running: [Device]
    let available: [Device]

    struct Device: Codable {
        let udid: String
        let name: String
        let os: String
        let state: String
    }
}

func fetchSimulators(port: Int = 8421) async throws -> SimulatorInfo {
    let url = URL(string: "http://localhost:\(port)/simulators.json")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(SimulatorInfo.self, from: data)
}

func bootSimulator(udid: String, port: Int = 8421) async throws {
    let url = URL(string: "http://localhost:\(port)/simulators/\(udid)/boot")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    let (_, response) = try await URLSession.shared.data(for: request)
    guard (response as? HTTPURLResponse)?.statusCode == 200 else {
        throw URLError(.badServerResponse)
    }
}

// Usage
Task {
    let sims = try await fetchSimulators()
    print("Running: \(sims.running.map(\.name))")
    if let first = sims.available.first {
        try await bootSimulator(udid: first.udid)
        print("Booted \(first.name)")
    }
}
```

### Connecting to a Live Stream WebSocket

```swift
import Foundation

func connectToSimulatorStream(udid: String, port: Int = 8421) {
    let url = URL(string: "ws://localhost:\(port)/simulators/\(udid)/stream?format=mjpeg")!
    let session = URLSession(configuration: .default)
    let task = session.webSocketTask(with: url)
    task.resume()

    // Reduce bitrate and fps for a thumbnail
    let setFps = URLSessionWebSocketTask.Message.string(
        #"{"type":"set_fps","fps":15}"#
    )
    let setBitrate = URLSessionWebSocketTask.Message.string(
        #"{"type":"set_bitrate","bps":500000}"#
    )
    task.send(setFps) { _ in }
    task.send(setBitrate) { _ in }

    // Receive MJPEG frames
    func receiveFrame() {
        task.receive { result in
            switch result {
            case .success(.data(let jpegData)):
                // jpegData is a raw JPEG — display in NSImageView / UIImageView
                print("Received frame: \(jpegData.count) bytes")
                receiveFrame()
            case .success(.string(let text)):
                print("Control message: \(text)")
                receiveFrame()
            case .failure(let error):
                print("Stream ended: \(error)")
            }
        }
    }
    receiveFrame()
}
```

### Sending Gestures over WebSocket

```swift
func sendTapOverWebSocket(task: URLSessionWebSocketTask, x: Double, y: Double,
                           width: Double, height: Double) {
    let gesture: [String: Any] = [
        "type": "tap",
        "x": x, "y": y,
        "width": width, "height": height,
        "duration": 0.05
    ]
    guard let data = try? JSONSerialization.data(withJSONObject: gesture),
          let json = String(data: data, encoding: .utf8) else { return }
    task.send(.string(json)) { error in
        if let error { print("Send error: \(error)") }
    }
}

func sendPinchOverWebSocket(task: URLSessionWebSocketTask,
                             cx: Double, cy: Double,
                             startSpread: Double, endSpread: Double,
                             width: Double, height: Double) {
    let gesture: [String: Any] = [
        "type": "pinch",
        "cx": cx, "cy": cy,
        "startSpread": startSpread,
        "endSpread": endSpread,
        "width": width, "height": height
    ]
    guard let data = try? JSONSerialization.data(withJSONObject: gesture),
          let json = String(data: data, encoding: .utf8) else { return }
    task.send(.string(json)) { _ in }
}
```

### Shell Script: Full Automation Flow

```bash
#!/usr/bin/env bash
set -euo pipefail

# Start the baguette server in background
baguette serve --port 8421 &
SERVER_PID=$!
sleep 1

# Get the first available simulator UDID
UDID=$(baguette list | grep "iPhone 17 Pro" | head -1 | awk '{print $1}')
echo "Using simulator: $UDID"

# Boot it
baguette boot --udid "$UDID"
sleep 3

# Run a tap sequence
baguette tap --udid "$UDID" --x 195 --y 422 --width 390 --height 844

# Pipe a gesture script
cat <<EOF | baguette input --udid "$UDID"
{"type":"tap","x":195,"y":200,"width":390,"height":844}
{"type":"swipe","startX":195,"startY":600,"endX":195,"endY":200,"width":390,"height":844,"duration":0.3}
{"type":"button","button":"home"}
EOF

# Capture a screenshot with bezel
baguette chrome composite --udid "$UDID" > screenshot.png
echo "Screenshot saved to screenshot.png"

# Shutdown
baguette shutdown --udid "$UDID"
kill $SERVER_PID
```

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `BAGUETTE_WEB_DIR` | Override the served web root (e.g. point to `Sources/Baguette/Resources/Web` for live UI iteration without rebuilding) |

```bash
# Live-iterate on web UI without rebuilding
export BAGUETTE_WEB_DIR="$(pwd)/Sources/Baguette/Resources/Web"
baguette serve
```

### Device Sets

```bash
# Use a custom simulator device set
baguette serve --device-set /path/to/my-device-set
baguette list  # uses default device set
```

## Common Patterns

### CI/CD: Boot, Test, Shutdown

```bash
#!/usr/bin/env bash
UDID=$(xcrun simctl list devices available -j | \
  python3 -c "import sys,json; devs=[d for v in json.load(sys.stdin)['devices'].values() for d in v if 'iPhone 17' in d['name'] and d['isAvailable']]; print(devs[0]['udid'])")

baguette boot --udid "$UDID"

# Run your XCTest suite or UI tests here
xcodebuild test -scheme MyApp -destination "id=$UDID"

baguette shutdown --udid "$UDID"
```

### Streaming to a File

```bash
# Capture 10 seconds of MJPEG to file
baguette stream --udid <UDID> --fps 30 --format mjpeg \
  | head -c $((10 * 30 * 50000)) > recording.mjpeg

# Convert to MP4 with ffmpeg
baguette stream --udid <UDID> --fps 30 --format mjpeg \
  | ffmpeg -f mjpeg -i - -t 10 -c:v libx264 output.mp4
```

### Multi-Finger Gesture Sequence (Real-Time)

```bash
# Send a real-time 2-finger swipe up (simulate pull-to-refresh for two fingers)
cat <<'EOF' | baguette input --udid <UDID>
{"type":"touch2-down","x1":160,"y1":600,"x2":230,"y2":600,"width":390,"height":844}
{"type":"touch2-move","x1":160,"y1":500,"x2":230,"y2":500,"width":390,"height":844}
{"type":"touch2-move","x1":160,"y1":400,"x2":230,"y2":400,"width":390,"height":844}
{"type":"touch2-move","x1":160,"y1":300,"x2":230,"y2":300,"width":390,"height":844}
{"type":"touch2-up","x1":160,"y1":300,"x2":230,"y2":300,"width":390,"height":844}
EOF
```

## Troubleshooting

### "Command not found: baguette"

```bash
# Ensure Homebrew's bin is in PATH
export PATH="/opt/homebrew/bin:$PATH"
# Or check install location
brew --prefix tddworks/tap/baguette
```

### Simulator Won't Boot

```bash
# Check Xcode 26 is selected (required for SimulatorKit frameworks)
xcode-select -p
# Should show Xcode 26 path, e.g. /Applications/Xcode-26.0.app/Contents/Developer
sudo xcode-select -s /Applications/Xcode-26.0.app/Contents/Developer

# Verify the UDID exists
baguette list
```

### Stream Connects but No Frames

```bash
# Make sure the simulator is booted (not just created)
baguette boot --udid <UDID>
sleep 3
baguette stream --udid <UDID> --fps 30 --format mjpeg | xxd | head
```

### Input Gestures Not Registering

- Coordinates must be in **device points**, not pixels. For a 3x display at 390pt wide, pixel width is 1170 — always use point values.
- Ensure `--width` and `--height` match the simulator's actual screen size in points (check with `baguette chrome layout --udid <UDID>`).
- Only `home` and `lock` buttons are functional on iOS 26 (`press` command).

### Web UI Not Updating

```bash
# Use BAGUETTE_WEB_DIR for live file iteration
export BAGUETTE_WEB_DIR="$(pwd)/Sources/Baguette/Resources/Web"
baguette serve
# Edit .html/.js/.css files and hard-refresh the browser
```

### Port Already in Use

```bash
# Check what's using port 8421
lsof -i :8421
# Use a different port
baguette serve --port 9000
open http://localhost:9000/simulators
```

### Build Failures (Source Build)

```bash
# Ensure arm64e target and Xcode 26 SDK
xcrun --sdk macosx --show-sdk-path
# Should show macOS 15+ SDK from Xcode 26
swift --version
# Should show Swift 6.1+
make clean && make
```
