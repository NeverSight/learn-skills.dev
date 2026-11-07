---
name: puremac-macos-cleaner
description: Free open-source macOS cleaner built with SwiftUI — CleanMyMac alternative with zero telemetry, scheduled auto-cleaning, and Xcode/Homebrew/system cache cleanup.
triggers:
  - clean my mac with PureMac
  - set up PureMac cleaner
  - build PureMac from source
  - add scheduled cleaning to my mac
  - integrate PureMac into my workflow
  - configure PureMac auto-cleaning
  - contribute to PureMac
  - how does PureMac clean Xcode cache
---

# PureMac macOS Cleaner

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

PureMac is a free, native SwiftUI macOS application that cleans system junk, user caches, Xcode derived data, Homebrew caches, mail attachments, and purgeable APFS space. It is a privacy-respecting, open-source alternative to CleanMyMac X with no telemetry, no subscriptions, and no network calls.

---

## Install

### Homebrew (recommended)

```bash
brew tap momenbasel/tap
brew install --cask puremac
```

### Direct Download

Download the latest `.app` from [Releases](https://github.com/momenbasel/PureMac/releases/latest), unzip, and drag to `/Applications`.

### Build from Source

```bash
brew install xcodegen
git clone https://github.com/momenbasel/PureMac.git
cd PureMac
xcodegen generate
xcodebuild \
  -project PureMac.xcodeproj \
  -scheme PureMac \
  -configuration Release \
  -derivedDataPath build \
  build
open build/Build/Products/Release/PureMac.app
```

Requirements: macOS 13.0+, Swift 5.9, Xcode 15+.

---

## Project Structure

```
PureMac/
├── PureMac/
│   ├── App/
│   │   └── PureMacApp.swift          # App entry point
│   ├── Views/
│   │   ├── ContentView.swift         # Main window
│   │   ├── ScanView.swift            # Smart scan UI
│   │   ├── CategoryDetailView.swift  # Per-category drill-down
│   │   └── SettingsView.swift        # Schedule & preferences
│   ├── Models/
│   │   ├── CleanCategory.swift       # Category definitions
│   │   └── ScanResult.swift          # Scan result model
│   ├── Services/
│   │   ├── ScannerService.swift      # File scanning logic
│   │   ├── CleanerService.swift      # Deletion logic
│   │   ├── SchedulerService.swift    # Auto-clean scheduling
│   │   └── PurgeableService.swift    # APFS purgeable space
│   └── Utilities/
│       └── FileSizeFormatter.swift
├── project.yml                       # XcodeGen spec
└── CONTRIBUTING.md
```

---

## Core Concepts

### Clean Categories

PureMac operates on named categories, each mapping to specific filesystem paths:

| Category | Key Paths |
|---|---|
| System Junk | `/Library/Caches`, `/Library/Logs`, `/tmp`, `~/Library/Logs` |
| User Cache | `~/Library/Caches`, npm/pip/yarn/pnpm caches |
| Mail Attachments | `~/Library/Mail Downloads` |
| Trash | `~/.Trash` |
| Large & Old Files | `~/Downloads`, `~/Documents`, `~/Desktop` (>100 MB or >1 year old) |
| Purgeable Space | APFS Time Machine snapshots via `tmutil` |
| Xcode Junk | `DerivedData`, `Archives`, `CoreSimulator/Caches` |
| Homebrew Cache | `~/Library/Caches/Homebrew` |

**Large & Old Files are never auto-selected** — the user must explicitly choose items before cleaning.

---

## Working with the Codebase

### Adding a New Clean Category

1. **Define the category** in `CleanCategory.swift`:

```swift
// CleanCategory.swift
enum CleanCategory: String, CaseIterable, Identifiable {
    case systemJunk       = "System Junk"
    case userCache        = "User Cache"
    case mailAttachments  = "Mail Attachments"
    case trash            = "Trash"
    case largeOldFiles    = "Large & Old Files"
    case purgeableSpace   = "Purgeable Space"
    case xcodeJunk        = "Xcode Junk"
    case homebrewCache    = "Homebrew Cache"
    // Add your new category here:
    case gradleCache      = "Gradle Cache"

    var id: String { rawValue }

    var iconName: String {
        switch self {
        case .systemJunk:      return "trash.circle"
        case .userCache:       return "internaldrive"
        case .xcodeJunk:       return "hammer"
        case .homebrewCache:   return "shippingbox"
        case .gradleCache:     return "archivebox"   // new
        default:               return "folder"
        }
    }
}
```

2. **Add scanning logic** in `ScannerService.swift`:

```swift
// ScannerService.swift
func scanCategory(_ category: CleanCategory) async throws -> ScanResult {
    switch category {
    case .gradleCache:
        return try await scanPaths([
            FileManager.default.homeDirectoryForCurrentUser
                .appendingPathComponent(".gradle/caches")
        ])
    // ...existing cases
    default:
        throw ScannerError.unsupportedCategory
    }
}

private func scanPaths(_ urls: [URL]) async throws -> ScanResult {
    var files: [ScannedFile] = []
    let fm = FileManager.default

    for url in urls {
        guard fm.fileExists(atPath: url.path) else { continue }
        let enumerator = fm.enumerator(
            at: url,
            includingPropertiesForKeys: [.fileSizeKey, .contentModificationDateKey],
            options: [.skipsHiddenFiles]
        )
        while let fileURL = enumerator?.nextObject() as? URL {
            let values = try fileURL.resourceValues(forKeys: [.fileSizeKey, .contentModificationDateKey])
            let size = Int64(values.fileSize ?? 0)
            let modified = values.contentModificationDate ?? Date.distantPast
            files.append(ScannedFile(url: fileURL, size: size, modifiedDate: modified))
        }
    }

    let totalBytes = files.reduce(0) { $0 + $1.size }
    return ScanResult(category: .gradleCache, files: files, totalBytes: totalBytes)
}
```

3. **Add cleaning logic** in `CleanerService.swift`:

```swift
// CleanerService.swift
func clean(_ result: ScanResult, selectedFiles: Set<URL>? = nil) async throws -> Int64 {
    let filesToDelete = selectedFiles.map { Array($0) } ?? result.files.map(\.url)
    var bytesFreed: Int64 = 0
    let fm = FileManager.default

    for url in filesToDelete {
        do {
            let attrs = try fm.attributesOfItem(atPath: url.path)
            let size = attrs[.size] as? Int64 ?? 0
            try fm.removeItem(at: url)
            bytesFreed += size
        } catch {
            // Log but continue — don't abort on single-file failure
            print("Failed to delete \(url.lastPathComponent): \(error.localizedDescription)")
        }
    }
    return bytesFreed
}
```

---

### Scheduled Auto-Cleaning

Configure via Settings → Schedule tab. Intervals: hourly, 3h, 6h, 12h, daily, weekly, biweekly, monthly.

```swift
// SchedulerService.swift — how scheduling is implemented
import UserNotifications

class SchedulerService: ObservableObject {
    @AppStorage("schedulingEnabled")    var schedulingEnabled: Bool = false
    @AppStorage("cleaningInterval")     var cleaningInterval: String = "daily"
    @AppStorage("autoCleanAfterScan")   var autoCleanAfterScan: Bool = false
    @AppStorage("autoPurgePurgeable")   var autoPurgePurgeable: Bool = false

    private var timer: Timer?

    func scheduleIfNeeded() {
        timer?.invalidate()
        guard schedulingEnabled else { return }
        let interval = intervalSeconds(for: cleaningInterval)
        timer = Timer.scheduledTimer(withTimeInterval: interval, repeats: true) { [weak self] _ in
            Task { await self?.runScheduledClean() }
        }
    }

    private func intervalSeconds(for key: String) -> TimeInterval {
        switch key {
        case "hourly":    return 3_600
        case "3h":        return 10_800
        case "6h":        return 21_600
        case "12h":       return 43_200
        case "daily":     return 86_400
        case "weekly":    return 604_800
        case "biweekly":  return 1_209_600
        case "monthly":   return 2_592_000
        default:          return 86_400
        }
    }

    @MainActor
    private func runScheduledClean() async {
        let scanner = ScannerService()
        let cleaner = CleanerService()
        for category in CleanCategory.allCases where category != .largeOldFiles {
            if let result = try? await scanner.scanCategory(category), autoCleanAfterScan {
                _ = try? await cleaner.clean(result)
            }
        }
        if autoPurgePurgeable {
            try? await PurgeableService.shared.purge()
        }
    }
}
```

**Enable scheduling programmatically:**

```swift
let scheduler = SchedulerService()
scheduler.cleaningInterval = "weekly"
scheduler.autoCleanAfterScan = true
scheduler.autoPurgePurgeable = false
scheduler.schedulingEnabled = true
scheduler.scheduleIfNeeded()
```

---

### Purgeable Space (APFS Snapshots)

PureMac uses `tmutil` to delete local Time Machine snapshots — this is the only operation requiring elevated privileges:

```swift
// PurgeableService.swift
import Foundation

class PurgeableService {
    static let shared = PurgeableService()

    func listSnapshots() async throws -> [String] {
        let output = try await shell("tmutil listlocalsnapshots /")
        return output
            .split(separator: "\n")
            .map(String.init)
            .filter { $0.hasPrefix("com.apple.TimeMachine") }
    }

    func purge() async throws {
        let snapshots = try await listSnapshots()
        for snapshot in snapshots {
            try await shell("tmutil deletelocalsnapshots \(snapshot)")
        }
    }

    @discardableResult
    private func shell(_ command: String) async throws -> String {
        try await withCheckedThrowingContinuation { continuation in
            let task = Process()
            task.launchPath = "/bin/bash"
            task.arguments = ["-c", command]
            let pipe = Pipe()
            task.standardOutput = pipe
            task.terminationHandler = { _ in
                let data = pipe.fileHandleForReading.readDataToEndOfFile()
                continuation.resume(returning: String(data: data, encoding: .utf8) ?? "")
            }
            do { try task.run() } catch { continuation.resume(throwing: error) }
        }
    }
}
```

---

### Xcode Cache Paths

```swift
// Paths cleaned by the Xcode Junk category
let home = FileManager.default.homeDirectoryForCurrentUser

let xcodePaths: [URL] = [
    home.appendingPathComponent("Library/Developer/Xcode/DerivedData"),
    home.appendingPathComponent("Library/Developer/Xcode/Archives"),
    home.appendingPathComponent("Library/Developer/CoreSimulator/Caches"),
]
```

Scan these and safely delete their contents without removing the directories themselves.

---

## SwiftUI View Patterns

### Scan Progress View

```swift
// Example: triggering a scan from a SwiftUI view
struct ScanView: View {
    @StateObject private var scanner = ScannerService()
    @State private var results: [ScanResult] = []
    @State private var isScanning = false

    var body: some View {
        VStack {
            if isScanning {
                ProgressView("Scanning…")
            } else {
                Button("Smart Scan") {
                    Task { await runScan() }
                }
            }
            List(results, id: \.category) { result in
                CategoryRow(result: result)
            }
        }
    }

    private func runScan() async {
        isScanning = true
        results = []
        for category in CleanCategory.allCases {
            if let result = try? await scanner.scanCategory(category) {
                results.append(result)
            }
        }
        isScanning = false
    }
}
```

### File Inspector (Click-to-Inspect)

```swift
// Show files before deletion — users can deselect
struct CategoryDetailView: View {
    let result: ScanResult
    @State private var selected: Set<URL> = []
    @State private var cleaned = false

    var body: some View {
        List(result.files, id: \.url, selection: $selected) { file in
            HStack {
                Image(systemName: "doc")
                Text(file.url.lastPathComponent)
                Spacer()
                Text(ByteCountFormatter.string(fromByteCount: file.size, countStyle: .file))
                    .foregroundStyle(.secondary)
            }
        }
        .toolbar {
            Button("Clean Selected") {
                Task {
                    let cleaner = CleanerService()
                    _ = try? await cleaner.clean(result, selectedFiles: selected)
                    cleaned = true
                }
            }
            .disabled(selected.isEmpty)
        }
    }
}
```

---

## Configuration (AppStorage Keys)

All preferences are stored in `UserDefaults` via `@AppStorage`:

| Key | Type | Default | Description |
|---|---|---|---|
| `schedulingEnabled` | Bool | false | Enable scheduled cleaning |
| `cleaningInterval` | String | "daily" | Interval key (see above) |
| `autoCleanAfterScan` | Bool | false | Auto-clean after scheduled scan |
| `autoPurgePurgeable` | Bool | false | Auto-purge APFS snapshots |

Read/write from anywhere:

```swift
UserDefaults.standard.set(true,    forKey: "schedulingEnabled")
UserDefaults.standard.set("weekly", forKey: "cleaningInterval")
```

---

## Building & Testing

```bash
# Generate Xcode project from project.yml
xcodegen generate

# Build Release
xcodebuild \
  -project PureMac.xcodeproj \
  -scheme PureMac \
  -configuration Release \
  -derivedDataPath build \
  build

# Run tests
xcodebuild test \
  -project PureMac.xcodeproj \
  -scheme PureMac \
  -destination 'platform=macOS'

# Open built app
open build/Build/Products/Release/PureMac.app
```

---

## Contributing

1. Fork and clone the repo.
2. Run `xcodegen generate` to create the `.xcodeproj`.
3. Create a feature branch: `git checkout -b feature/gradle-cache-cleaning`
4. Follow existing patterns in `ScannerService` / `CleanerService`.
5. Never add network calls, analytics SDKs, or telemetry of any kind.
6. Large & Old Files must never be auto-selected for deletion.
7. Open a PR against `main`.

See [CONTRIBUTING.md](https://github.com/momenbasel/PureMac/blob/main/CONTRIBUTING.md) for full guidelines.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `xcodegen: command not found` | `brew install xcodegen` |
| App blocked by Gatekeeper | The release build is notarized; if building from source, run `xattr -cr PureMac.app` |
| Purgeable scan returns 0 bytes | No local Time Machine snapshots exist — this is normal if TM is off |
| Xcode paths not found | Xcode has not been used yet or DerivedData was already cleared |
| `tmutil` requires password | Purgeable purge may prompt for admin credentials — this is expected macOS behavior |
| Scheduled cleaning not triggering | Ensure the app is running (it is not a background daemon); check Settings → Schedule |

---

## Safety Guarantees

- **Never** deletes system-critical files or application bundles.
- Only removes caches, logs, temp files, and user-selected items.
- Large & Old Files require explicit user selection before deletion.
- Purgeable operations target only APFS Time Machine snapshots — not free space.
- All filesystem operations use `FileManager.removeItem(at:)` — no `rm -rf` shell calls for regular cleaning.
