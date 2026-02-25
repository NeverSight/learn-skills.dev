---
name: macos-permissions
description: macOS permission handling for Accessibility (AXIsProcessTrusted), Screen Recording, Full Disk Access, input monitoring, camera, microphone, location, and contacts. Covers TCC (Transparency Consent and Control) database, graceful degradation when permissions are denied, permission prompting patterns, opening System Settings to the correct pane, detecting permission changes, and the privacy manifest (PrivacyInfo.xcprivacy) requirement. Use when implementing features that require system permissions, building permission onboarding flows, or handling denied permissions gracefully.
---

# macOS Permissions

## Critical Constraints

- ❌ DO NOT assume permissions are granted → ✅ Always check before using protected APIs
- ❌ DO NOT repeatedly prompt after denial → ✅ Guide user to System Settings instead
- ❌ DO NOT block the entire app on missing permission → ✅ Gracefully degrade, offer reduced functionality
- ❌ DO NOT forget PrivacyInfo.xcprivacy → ✅ Required for App Store submission

## Permission Types

| Permission | Check API | Required For |
|------------|-----------|-------------|
| Accessibility | `AXIsProcessTrusted()` | Global hotkeys, text insertion, CGEvent |
| Screen Recording | `CGPreflightScreenCaptureAccess()` | Screen capture, window list |
| Full Disk Access | Try access + handle error | Reading other app data |
| Camera | `AVCaptureDevice.authorizationStatus(for: .video)` | Camera access |
| Microphone | `AVCaptureDevice.authorizationStatus(for: .audio)` | Audio capture |
| Location | `CLLocationManager().authorizationStatus` | Location services |
| Contacts | `CNContactStore.authorizationStatus(for: .contacts)` | Contact access |

## Accessibility Permission
```swift
import ApplicationServices

// Check without prompting
func isAccessibilityGranted() -> Bool {
    AXIsProcessTrusted()
}

// Check and prompt user (shows system dialog)
func requestAccessibilityPermission() -> Bool {
    let options = [kAXTrustedCheckOptionPrompt.takeRetainedValue() as String: true]
    return AXIsProcessTrustedWithOptions(options as CFDictionary)
}

// Open System Settings → Privacy → Accessibility
func openAccessibilitySettings() {
    NSWorkspace.shared.open(URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility")!)
}
```

## Screen Recording Permission
```swift
import CoreGraphics

// Check (macOS 15+)
func isScreenRecordingGranted() -> Bool {
    CGPreflightScreenCaptureAccess()
}

// Request (macOS 15+)
func requestScreenRecording() -> Bool {
    CGRequestScreenCaptureAccess()
}

// Open Settings
func openScreenRecordingSettings() {
    NSWorkspace.shared.open(URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture")!)
}
```

## Camera / Microphone
```swift
import AVFoundation

func checkCameraPermission() async -> Bool {
    switch AVCaptureDevice.authorizationStatus(for: .video) {
    case .authorized: return true
    case .notDetermined: return await AVCaptureDevice.requestAccess(for: .video)
    case .denied, .restricted: return false
    @unknown default: return false
    }
}
```

## Graceful Degradation Pattern
```swift
struct FeatureAvailability {
    var canInsertText: Bool { AXIsProcessTrusted() }
    var canUseGlobalHotkey: Bool { AXIsProcessTrusted() }
    var canCaptureScreen: Bool { CGPreflightScreenCaptureAccess() }

    var degradedFeatures: [String] {
        var features: [String] = []
        if !canInsertText { features.append("Text insertion into other apps") }
        if !canUseGlobalHotkey { features.append("Global keyboard shortcuts") }
        return features
    }
}

struct PermissionBanner: View {
    let availability: FeatureAvailability

    var body: some View {
        if !availability.degradedFeatures.isEmpty {
            VStack(alignment: .leading, spacing: 8) {
                Label("Some features require permissions", systemImage: "lock.shield")
                    .font(.headline)
                ForEach(availability.degradedFeatures, id: \.self) { feature in
                    Text("• \(feature)")
                        .font(.caption)
                }
                Button("Open System Settings") { openAccessibilitySettings() }
                    .buttonStyle(.borderedProminent)
            }
            .padding()
            .glassEffect(.regular.tint(.orange), in: .rect(cornerRadius: 12))
        }
    }
}
```

## Permission Onboarding Flow
```swift
struct OnboardingPermissionView: View {
    @State private var accessibilityGranted = AXIsProcessTrusted()
    let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()

    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: accessibilityGranted ? "checkmark.circle.fill" : "lock.circle")
                .font(.system(size: 48))
                .foregroundStyle(accessibilityGranted ? .green : .orange)

            Text(accessibilityGranted ? "Permission Granted!" : "Accessibility Permission Required")
                .font(.title2)

            if !accessibilityGranted {
                Text("This app needs Accessibility access to insert text into other apps and register global shortcuts.")
                    .multilineTextAlignment(.center)

                Button("Open System Settings") {
                    requestAccessibilityPermission()
                }
                .buttonStyle(.borderedProminent)
            }
        }
        .onReceive(timer) { _ in
            accessibilityGranted = AXIsProcessTrusted()
        }
    }
}
```

## Privacy Manifest (PrivacyInfo.xcprivacy)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
    <key>NSPrivacyTracking</key>
    <false/>
    <key>NSPrivacyTrackingDomains</key>
    <array/>
    <key>NSPrivacyCollectedDataTypes</key>
    <array/>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array><string>CA92.1</string></array>
        </dict>
    </array>
</dict>
</plist>
```

## Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| Prompting repeatedly after denial | Check status first, guide to Settings if denied |
| App crashes without permission | Always check before calling protected API |
| User can't find permission setting | Open specific System Settings pane via URL |
| Missing privacy manifest | Add PrivacyInfo.xcprivacy to app bundle |

## References

- [Accessibility API](https://developer.apple.com/documentation/applicationservices/axuielement_h)
- [TCC and Privacy](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files)
