---
name: capso-screenshot-macos
description: Expert skill for Capso, the open-source macOS screenshot and screen recording app built with Swift 6 and SwiftUI — covers architecture, building from source, package APIs, and contributing.
triggers:
  - "add screenshot functionality to my mac app"
  - "integrate capso into my project"
  - "use CaptureKit or AnnotationKit from capso"
  - "build capso from source"
  - "how to use capso packages in swift"
  - "screen recording swift macos"
  - "capso annotation or OCR API"
  - "contribute to capso open source"
---

# Capso Screenshot & Screen Recording Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Capso is a fully native, open-source macOS screenshot and screen recording app — a free alternative to CleanShot X. Built with Swift 6.0 and SwiftUI targeting macOS 15.0+. Its key strength for developers is a **modular SPM architecture**: 8 independent packages (`CaptureKit`, `AnnotationKit`, `OCRKit`, etc.) you can embed individually in your own app.

---

## Installation

### Download Pre-built App

```bash
# Homebrew (recommended)
brew tap lzhgus/tap
brew install --cask capso
```

Or download the signed DMG from [GitHub Releases](https://github.com/lzhgus/Capso/releases/latest).

### Build from Source

**Requirements:** Xcode 16+, macOS 15.0+, XcodeGen

```bash
brew install xcodegen

git clone https://github.com/lzhgus/Capso.git
cd Capso
xcodegen generate
open Capso.xcodeproj
# Press Cmd+R to build and run
```

**CLI build:**

```bash
xcodegen generate
xcodebuild -project Capso.xcodeproj \
  -scheme Capso \
  -configuration Release \
  build
```

---

## Project Architecture

```
Capso/
├── App/                     # Thin SwiftUI + AppKit shell
│   ├── CapsoApp.swift       # @main entry point
│   ├── MenuBar/
│   ├── Capture/
│   ├── Recording/
│   ├── Camera/
│   ├── AnnotationEditor/
│   ├── OCR/
│   ├── QuickAccess/
│   └── Preferences/
├── Packages/
│   ├── SharedKit/           # Settings, permissions, utilities
│   ├── CaptureKit/          # ScreenCaptureKit wrapper
│   ├── RecordingKit/        # Screen recording engine
│   ├── CameraKit/           # AVFoundation webcam capture
│   ├── AnnotationKit/       # Drawing/annotation system
│   ├── OCRKit/              # Vision framework OCR
│   ├── ExportKit/           # Video/GIF/image export
│   └── EffectsKit/          # Cursor effects, click highlights
└── project.yml              # XcodeGen project definition
```

The app shell is intentionally thin — all logic lives in packages. This means you can pull individual packages into your own app via SPM.

---

## Using Capso Packages in Your Own App

Add a package as a local or remote SPM dependency in your `Package.swift`:

```swift
// Package.swift
let package = Package(
    name: "MyApp",
    platforms: [.macOS(.v15)],
    dependencies: [
        // Remote (once published to a registry or via exact path)
        .package(path: "../Capso/Packages/CaptureKit"),
        .package(path: "../Capso/Packages/AnnotationKit"),
        .package(path: "../Capso/Packages/OCRKit"),
    ],
    targets: [
        .target(
            name: "MyApp",
            dependencies: [
                "CaptureKit",
                "AnnotationKit",
                "OCRKit",
            ]
        ),
    ]
)
```

---

## Package API Examples

### CaptureKit — Screen Capture

CaptureKit wraps `ScreenCaptureKit` for area, fullscreen, and window capture.

```swift
import CaptureKit

// Area capture
let captureManager = CaptureManager()

// Fullscreen capture
Task {
    let image: NSImage = try await captureManager.captureFullscreen()
    // use image
}

// Window capture — pass SCWindow from ScreenCaptureKit
Task {
    let content = try await SCShareableContent.excludingDesktopWindows(false, onScreenWindowsOnly: true)
    if let window = content.windows.first {
        let image: NSImage = try await captureManager.captureWindow(window)
    }
}

// Area capture with a selection rect
Task {
    let rect = CGRect(x: 100, y: 100, width: 800, height: 600)
    let image: NSImage = try await captureManager.captureArea(rect)
}
```

### RecordingKit — Screen Recording

```swift
import RecordingKit

let recorder = ScreenRecorder()

// Configure recording
var config = RecordingConfiguration()
config.includesSystemAudio = true
config.includesMicrophone = false
config.outputFormat = .mp4   // or .gif
config.quality = .maximum    // .social, .web

// Start recording a region
Task {
    let outputURL = URL(fileURLWithPath: "/tmp/recording.mp4")
    try await recorder.startRecording(
        region: CGRect(x: 0, y: 0, width: 1920, height: 1080),
        to: outputURL,
        configuration: config
    )
}

// Pause / resume
recorder.pause()
recorder.resume()

// Stop and get final URL
Task {
    let finalURL = try await recorder.stopRecording()
    print("Saved to \(finalURL)")
}
```

### CameraKit — Webcam PiP

```swift
import CameraKit

let cameraManager = CameraManager()

// Request permission and start preview
Task {
    let granted = await cameraManager.requestPermission()
    guard granted else { return }
    
    // Get AVCaptureVideoPreviewLayer for embedding in a view
    let previewLayer = try await cameraManager.startCapture()
    
    // Set PiP shape
    cameraManager.pipShape = .circle      // .circle, .square, .portrait, .landscape
}

// Stop capture
cameraManager.stopCapture()
```

### AnnotationKit — Drawing & Annotation

```swift
import AnnotationKit

// Create an annotation canvas over an NSImage
let sourceImage = NSImage(named: "screenshot")!
let canvas = AnnotationCanvas(image: sourceImage)

// Add annotations programmatically
let arrow = ArrowAnnotation(
    from: CGPoint(x: 50, y: 50),
    to: CGPoint(x: 200, y: 200),
    color: .red,
    strokeWidth: 3
)
canvas.addAnnotation(arrow)

let rect = RectangleAnnotation(
    frame: CGRect(x: 100, y: 100, width: 300, height: 150),
    color: .blue,
    strokeWidth: 2,
    filled: false
)
canvas.addAnnotation(rect)

let text = TextAnnotation(
    text: "Look here!",
    position: CGPoint(x: 110, y: 110),
    fontSize: 18,
    color: .white
)
canvas.addAnnotation(text)

// Undo / redo
canvas.undo()
canvas.redo()

// Export annotated image
let result: NSImage = canvas.renderToImage()
```

### Screenshot Beautification (AnnotationKit)

```swift
import AnnotationKit

let beautifier = ScreenshotBeautifier(image: rawImage)
beautifier.backgroundColor = .systemBlue   // or gradient/custom
beautifier.padding = 40
beautifier.cornerRadius = 12
beautifier.shadowRadius = 20
beautifier.shadowOpacity = 0.4

let beautified: NSImage = beautifier.render()
```

### OCRKit — Text Recognition

```swift
import OCRKit

let ocrEngine = OCREngine()

// Instant OCR on an NSImage — returns plain text
Task {
    let text: String = try await ocrEngine.recognizeText(in: image)
    print(text)
    // Copy to clipboard
    NSPasteboard.general.clearContents()
    NSPasteboard.general.setString(text, forType: .string)
}

// Visual OCR — returns bounding boxes + text for each block
Task {
    let blocks: [OCRTextBlock] = try await ocrEngine.recognizeBlocks(in: image)
    for block in blocks {
        print("Text: \(block.text), Bounds: \(block.boundingBox)")
    }
}
```

### ExportKit — Video & GIF Export

```swift
import ExportKit

let exporter = MediaExporter()

// Export recorded video with quality preset
Task {
    let inputURL = URL(fileURLWithPath: "/tmp/raw_recording.mp4")
    let outputURL = URL(fileURLWithPath: "/tmp/final.mp4")
    
    try await exporter.exportVideo(
        from: inputURL,
        to: outputURL,
        quality: .social   // .maximum, .social, .web
    )
}

// Export as GIF
Task {
    let inputURL = URL(fileURLWithPath: "/tmp/raw_recording.mp4")
    let outputURL = URL(fileURLWithPath: "/tmp/output.gif")
    
    try await exporter.exportGIF(
        from: inputURL,
        to: outputURL,
        fps: 15,
        scale: 0.75
    )
}
```

### SharedKit — Permissions & Settings

```swift
import SharedKit

// Check and request screen recording permission
let permissionManager = PermissionManager()

Task {
    let hasScreen = await permissionManager.requestScreenRecordingPermission()
    let hasCamera = await permissionManager.requestCameraPermission()
    let hasMic = await permissionManager.requestMicrophonePermission()
}

// Access shared app settings
let settings = CapsoSettings.shared
settings.screenshotShortcut = "⌘⇧4"
settings.defaultSaveLocation = URL(fileURLWithPath: "/Users/me/Screenshots")
settings.showCountdownBeforeRecording = true
settings.countdownSeconds = 3
```

---

## SwiftUI Integration Pattern

Embed a capture button in a SwiftUI view:

```swift
import SwiftUI
import CaptureKit
import AnnotationKit

struct ContentView: View {
    @State private var capturedImage: NSImage?
    @State private var showAnnotationEditor = false
    private let captureManager = CaptureManager()

    var body: some View {
        VStack {
            if let img = capturedImage {
                Image(nsImage: img)
                    .resizable()
                    .scaledToFit()
                    .frame(maxWidth: 600)
                
                Button("Annotate") {
                    showAnnotationEditor = true
                }
            }

            Button("Capture Fullscreen") {
                Task {
                    capturedImage = try? await captureManager.captureFullscreen()
                }
            }
        }
        .sheet(isPresented: $showAnnotationEditor) {
            if let img = capturedImage {
                // Hypothetical SwiftUI wrapper around AnnotationCanvas
                AnnotationEditorView(image: img) { annotated in
                    capturedImage = annotated
                    showAnnotationEditor = false
                }
            }
        }
    }
}
```

---

## Running Package Tests

Each package is independently testable:

```bash
swift test --package-path Packages/SharedKit
swift test --package-path Packages/CaptureKit
swift test --package-path Packages/AnnotationKit
swift test --package-path Packages/OCRKit
swift test --package-path Packages/RecordingKit
swift test --package-path Packages/CameraKit
swift test --package-path Packages/ExportKit
swift test --package-path Packages/EffectsKit
```

---

## Required Entitlements & Info.plist

Your app using Capso packages needs these permissions:

```xml
<!-- Info.plist -->
<key>NSScreenCaptureUsageDescription</key>
<string>Required for screenshot and screen recording.</string>

<key>NSCameraUsageDescription</key>
<string>Required for webcam PiP during screen recording.</string>

<key>NSMicrophoneUsageDescription</key>
<string>Required to capture microphone audio during recording.</string>
```

```xml
<!-- App.entitlements -->
<key>com.apple.security.device.camera</key>
<true/>
<key>com.apple.security.device.microphone</key>
<true/>
<!-- Screen capture is runtime-only via TCC, no entitlement needed -->
```

---

## Common Patterns

### Pin Screenshot to Screen (Always-on-Top)

```swift
import AppKit

func pinScreenshot(_ image: NSImage) {
    let window = NSPanel(
        contentRect: NSRect(x: 100, y: 100, width: image.size.width, height: image.size.height),
        styleMask: [.nonactivatingPanel, .titled, .closable, .resizable],
        backing: .buffered,
        defer: false
    )
    window.level = .floating           // Always on top
    window.isFloatingPanel = true
    window.hidesOnDeactivate = false
    window.contentView = NSImageView(image: image)
    window.makeKeyAndOrderFront(nil)
}
```

### Global Keyboard Shortcut (via SharedKit pattern)

```swift
import Carbon
import AppKit

// Register a global hotkey for area capture
func registerCaptureHotkey() {
    NSEvent.addGlobalMonitorForEvents(matching: .keyDown) { event in
        // Check for ⌘⇧4
        if event.modifierFlags.contains([.command, .shift]),
           event.keyCode == 21 { // keyCode 21 = '4'
            NotificationCenter.default.post(name: .startAreaCapture, object: nil)
        }
    }
}

extension Notification.Name {
    static let startAreaCapture = Notification.Name("startAreaCapture")
}
```

---

## Troubleshooting

### `xcodegen generate` fails
- Ensure XcodeGen ≥ 2.40: `brew upgrade xcodegen`
- Check `project.yml` is not modified with invalid YAML syntax
- Run `xcodegen generate --spec project.yml` for explicit path

### "Screen Recording permission denied" at runtime
- Go to **System Settings → Privacy & Security → Screen Recording** and enable Capso
- For your own app using CaptureKit, you must trigger the permission prompt first via `PermissionManager.requestScreenRecordingPermission()`

### Build errors with Swift 6 concurrency
- Capso targets Swift 6 strict concurrency. Ensure all closures that touch UI are `@MainActor`
- Add `@preconcurrency` import for ScreenCaptureKit if you see warnings in Xcode 16

### GIF export is slow
- Lower the fps (e.g. `fps: 10`) and scale (e.g. `scale: 0.5`) in `ExportKit`
- Use `.web` quality preset for faster encoding

### Camera not showing in PiP
- Verify camera permission is granted in System Settings
- Call `CameraManager.requestPermission()` before `startCapture()`
- Ensure your entitlement includes `com.apple.security.device.camera`

---

## License Note

Capso uses **Business Source License 1.1**:
- ✅ Personal use, internal company use, forking, modifying
- ❌ Selling a competing screen-capture product based on this code
- ✅ Automatically becomes **Apache 2.0** in 2029 per release

When embedding packages in your own non-competing app, you are permitted under BSL 1.1.

---

## Key Links

- [GitHub Repository](https://github.com/lzhgus/Capso)
- [Releases / Download](https://github.com/lzhgus/Capso/releases/latest)
- [Website](https://www.awesomemacapp.com/app/capso)
- [Bug Reports](https://github.com/lzhgus/Capso/issues/new?template=bug_report.yml)
- [Feature Requests](https://github.com/lzhgus/Capso/issues/new?template=feature_request.yml)
- [GitHub Sponsors](https://github.com/sponsors/lzhgus)
