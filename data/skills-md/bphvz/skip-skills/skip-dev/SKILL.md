---
name: skip-dev
description: 'Expert guidance on building, debugging, and testing multiplatform iOS/Android apps and frameworks with Skip (skip.dev). Use when developers mention: (1) Skip, Skip.dev, skip-tools, or SkipStack, (2) building a multiplatform iOS+Android app from Swift/SwiftUI, (3) Skip Fuse (native) or Skip Lite (transpiled) modes, (4) transpiling Swift to Kotlin, (5) SwiftUI to Jetpack Compose bridging, (6) skip.yml configuration, (7) debugging Android builds from Xcode, (8) Skip CLI commands (skip create/init/test/export), (9) conditional compilation with #if SKIP or #if os(Android), (10) Skip Comments (SKIP INSERT/REPLACE/DECLARE/NOWARN), (11) bridging Swift and Kotlin code, (12) Skip module dependencies or Android Gradle configuration.'
---

# Skip Multiplatform Development

## Overview

Skip (https://skip.dev) enables building native iOS and Android apps from a single Swift/SwiftUI codebase. It works as an Xcode plugin that continuously generates an equivalent Android project using Jetpack Compose. iOS runs SwiftUI directly; Android uses Skip-generated Kotlin/Compose code.

## Decision Tree: Skip Mode Selection

Before writing code, determine the correct Skip mode:

```
Is this a NEW project?
├── YES → Does it need C/C++ code or complex Swift features?
│   ├── YES → Use Skip Fuse (native)
│   └── NO → Does app size matter (Fuse adds ~60MB)?
│       ├── YES → Use Skip Lite (transpiled)
│       └── NO → Use Skip Fuse (native) — preferred default
└── NO → Check skip.yml for `mode:` setting
    ├── mode: 'native' → Skip Fuse
    └── mode: 'transpiled' → Skip Lite
```

### Skip Fuse (Native Mode)
- Compiles Swift natively for Android using the Swift SDK for Android
- Full Swift language support, faithful runtime, complete stdlib/Foundation
- Can integrate C/C++ libraries
- Trade-off: +60MB app size, requires bridging for Kotlin interop, slower builds

### Skip Lite (Transpiled Mode)
- Converts Swift source code → Kotlin source code
- Direct access to Kotlin/Java APIs from `#if SKIP` blocks
- Smaller app size, faster builds, more transparent output
- Trade-off: limited Swift language features, limited stdlib support

### Configuration in skip.yml

```yaml
# For Fuse (native) mode:
mode: 'native'
bridging: true

# For Lite (transpiled) mode:
mode: 'transpiled'
```

## Project Structure

### App Projects
```
MyApp/
├── Package.swift              # SPM dependencies & targets
├── Skip.env                   # Skip environment config
├── Sources/
│   ├── MyApp/                 # Main app module (SwiftUI views)
│   │   ├── MyApp.swift        # App entry point (@main)
│   │   ├── ContentView.swift
│   │   └── Skip/              # Android-specific Kotlin files
│   │       └── skip.yml       # Skip module configuration
│   └── MyAppModel/            # Shared model module
│       ├── DataModel.swift
│       └── Skip/
│           └── skip.yml
├── Tests/
│   ├── MyAppTests/
│   └── MyAppModelTests/
├── Darwin/                    # iOS-specific
│   ├── MyApp.xcodeproj
│   ├── MyApp.xcconfig
│   ├── Assets.xcassets/
│   └── Info.plist
└── Android/                   # Android-specific
    ├── settings.gradle.kts
    └── app/
        ├── build.gradle.kts
        ├── src/main/AndroidManifest.xml
        └── src/main/kotlin/.../Main.kt
```

### Framework Projects (SPM Packages)
```
MyFramework/
├── Package.swift
├── Sources/
│   └── MyFramework/
│       ├── MyFramework.swift
│       └── Skip/
│           └── skip.yml
└── Tests/
    └── MyFrameworkTests/
        └── MyFrameworkTests.swift
```

**Key point:** Frameworks do NOT have Darwin/ or Android/ folders. The Android build is triggered by running unit tests, not by building an app.

## Building

### Apps: Build from Xcode
1. Open the `.xcodeproj` in `Darwin/`
2. Select an iOS Simulator destination
3. Build & Run — the Skip plugin automatically generates and builds the Android project
4. Android output appears in the `SkipStone/plugins` group in the Xcode project navigator

**Android build behavior** is controlled in `.xcconfig`:
```
SKIP_ACTION = launch   # Build and launch Android emulator (default)
SKIP_ACTION = build    # Build Android only, don't launch
SKIP_ACTION = none     # Skip Android build entirely
```

### Apps: Build from CLI
```bash
# Build iOS project
xcodebuild -project Darwin/MyApp.xcodeproj -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro,OS=latest' build

# Export Android APK
skip export --project Darwin/MyApp.xcodeproj --appid com.example.myapp
```

### Frameworks: Trigger Android Build via Tests
```bash
# Run against macOS destination to trigger Android build
swift test
# OR
skip test
```

**Critical:** You MUST run framework tests against a **macOS** destination to perform an Android build. Testing against an iOS destination will NOT run Android tests.

## Debugging

### iOS Debugging
- Standard Xcode debugging: breakpoints, LLDB, view hierarchy inspector
- Use `OSLog.Logger` for logging (NOT `print()` — print doesn't work on Android)

```swift
import OSLog

let logger = Logger(subsystem: "com.example.myapp", category: "networking")
logger.info("Request started: \(url)")
logger.error("Request failed: \(error.localizedDescription)")
```

### Android Debugging
1. **Logcat** — primary Android debugging tool:
```bash
# Filter logs by app tag
adb logcat -s MyApp

# Filter by Skip logger output
adb logcat | grep "com.example.myapp"
```

2. **Android Studio** — open the generated Gradle project:
   - For apps: find generated source under `SkipStone/plugins` in Xcode navigator → right-click → "Open in Android Studio"
   - For frameworks: open the `SkipLink/` folder in Android Studio

3. **View generated Kotlin code** — invaluable for debugging transpilation issues:
   - In Xcode, expand `SkipStone/plugins` (apps) or `SkipLink` (frameworks)
    - Find the `.kt` files corresponding to your Swift source
    - Use Kotlin compiler line numbers to locate the failing generated statement, then map it back to the matching Swift declaration
    - Apply fixes in Swift source (or Skip Comments), then rebuild; do not edit generated `.kt` files directly (they are overwritten)

4. **Crash traces** — demangle Swift symbols:
```bash
xcrun swift-demangle <mangled_symbol>
```

### Common Build Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `No such module 'Skip...'` | Skip plugin not installed | Run `skip checkup` |
| `Cannot find type...in scope` | Unsupported Swift API on Android | Use `#if !os(Android)` guard or find Skip equivalent |
| Gradle sync failure | Android SDK issue | Run `skip doctor` then `skip android sdk install` |
| `Bridging error` | Missing bridge annotation | Add `// SKIP @bridge` or enable `bridging: true` in skip.yml |
| `SkipNotSupportedError` | Using unsupported SkipUI feature | Check SkipUI docs; provide Android-specific alternative |

### Transpilation Error Workflow (Using Generated Kotlin)

When Lite mode transpilation fails, use this quick loop:

1. Trigger a build (`xcodebuild`, Xcode Run, or `skip test`) and capture the first Kotlin error.
2. Open the generated Kotlin file and line from the compiler output (`SkipStone/plugins` for apps, `SkipLink` for frameworks).
3. Identify the original Swift declaration that produced that Kotlin block.
4. Fix the Swift source using one of:
    - simpler type annotations (especially around generics/optionals)
    - platform guards (`#if os(Android)` / `#if !os(Android)` / `#if SKIP`)
    - Skip Comments (`SKIP INSERT`, `SKIP REPLACE`, `SKIP DECLARE`, `SKIP NOWARN`)
5. Rebuild and verify the same Kotlin section now compiles.

Rule of thumb: treat generated Kotlin as a diagnostic artifact, not a source of truth. Keep permanent fixes in Swift and `Skip/` support files.

## Testing

### Running Tests
```bash
# Swift tests only (iOS)
swift test

# Cross-platform parity tests (iOS + Android via Robolectric)
skip test

# Android emulator tests
ANDROID_SERIAL=emulator-5554 skip test
```

### Writing Cross-Platform Tests
```swift
import XCTest

final class MyTests: XCTestCase {
    func testSharedLogic() {
        // Runs on both platforms
        XCTAssertEqual(calculate(2, 3), 5)
    }

    #if !os(Android)
    func testIOSOnly() {
        // iOS-specific test
    }
    #endif

    #if os(Android) || ROBOLECTRIC
    func testAndroidOnly() {
        // Android-specific test (runs on Robolectric too)
    }
    #endif
}
```

### Robolectric Testing
Skip uses Robolectric for fast, Mac-based Android testing without an emulator. Use `#if os(Android) || ROBOLECTRIC` to include tests that should run on both Android emulator and Robolectric.

## Conditional Compilation

### Platform Directives
```swift
#if os(Android)
    // Android-only code
#else
    // iOS-only code
#endif

#if !os(Android)
    // iOS-only code
#endif

#if SKIP
    // Only in transpiled Kotlin code (Skip Lite)
    // Can call Kotlin/Java APIs directly here
#endif

#if !SKIP
    // Only in native Swift (iOS, or Fuse Android)
#endif

#if ROBOLECTRIC
    // Only during Robolectric test execution
#endif
```

### Skip Comments
Skip Comments control how Swift code is transpiled to Kotlin:

```swift
// SKIP INSERT: val androidSpecificVal = "only in Kotlin output"

// SKIP REPLACE: fun customKotlinImplementation() { ... }
func swiftImplementation() { ... }

// SKIP DECLARE: annotation class MyAnnotation
// SKIP DECLARE: typealias PlatformType = android.content.Context

// SKIP NOWARN
let _ = someUnsupportedPattern  // Suppresses transpilation warning

// SKIP @bridge
public func bridgedFunction() { }  // Exposes to Kotlin in Fuse mode

// SKIP @nobridge
public func noBridge() { }  // Prevents bridging

// SKIP @nocopy
struct LargeData { }  // Skip copy semantics for structs

// SKIP SYMBOLFILE
// Generates .skipmodule symbol file for the module
```

## Skip CLI Quick Reference

```bash
skip create          # Interactive project creation wizard
skip init            # Non-interactive project init
skip test            # Run cross-platform tests
skip export          # Export Android APK/AAB
skip checkup         # Verify Skip installation
skip doctor          # Diagnose and fix issues
skip upgrade         # Update Skip to latest version
skip verify          # Verify project configuration

# Android-specific
skip android build           # Build Android project
skip android test            # Run Android tests
skip android emulator create # Create AVD emulator
skip android emulator launch # Launch emulator
skip android sdk install     # Install Android SDK components
skip android sdk list        # List available SDK packages
```

## References

For detailed reference material, load from the `references/` directory:

- **`references/transpilation.md`** — Swift language features support table, builtin types, generics, structs, concurrency, numeric types, plus a Kotlin-output troubleshooting workflow for transpilation failures
- **`references/skip-ui.md`** — Supported SwiftUI components, ComposeView integration, composeModifier, Material3 customization, animation, images, navigation, lists, gestures
- **`references/cross-platform.md`** — Calling Kotlin/Java APIs, Compose integration, AnyDynamicObject, Kotlin files in Sources, Android Studio workflow, model integration patterns
- **`references/bridging.md`** — skip.yml configuration, @bridge/@bridgeMembers/@nobridge annotations, bridging Swift↔Kotlin, kotlincompat option, AnyDynamicObject usage
- **`references/dependencies.md`** — Adding Skip/SwiftPM/Java/Kotlin dependencies, platform-conditional dependencies, skip.yml build blocks
- **`references/cli.md`** — Full Skip CLI command reference with options, examples, and common workflows
- **`references/unit-testing.md`** — How unit testing works in Skip, execution model (`swift test` vs `skip test`), cross-platform test patterns, Robolectric usage, and CI strategy

Load a reference with: `read_file('<base_dir>/references/<filename>')`
