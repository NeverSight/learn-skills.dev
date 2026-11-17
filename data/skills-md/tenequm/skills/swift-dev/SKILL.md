---
name: swift-dev
description: Native iOS and macOS apps in Swift 6 - SwiftUI, AppKit, SwiftData, concurrency, Swift Testing, XcodeGen, CallKit and audio, App Intents, devices, TestFlight, code signing, notarization. Use for any iPhone or Mac app, helper or CLI work.
metadata:
  version: "0.3.1"
  categories: "development"
  topics: "swift, swiftui, ios, macos, xcode"
  upstream: "swift@6.4, xcode@27.1, ios@27.1, macos@27.0, LiveKit@2.18.0, xcodegen@2.46.0"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/swift-dev
    emoji: "🍎"
    os:
      - macos
---

# Swift Apple Development (iOS + macOS)

Native apps for iPhone and Mac with Swift 6.4 and Xcode 27.1 (iOS 27.1 and macOS 27.0 SDKs; Xcode 27.2 is at RC). Xcode 27 runs only on Apple silicon and needs macOS 26.6 or later. Deployment targets: iOS 17 / macOS 14 for `@Observable` and SwiftData; iOS 26 / macOS 26 for Liquid Glass, Foundation Models, `IntentModes` and `Observations`.

This file is the platform-neutral core plus a router. Load a reference only when the task needs it - the [Platform](#platform) tables say which.

## Start here

| Task | Default |
|------|---------|
| New iOS app | XcodeGen `project.yml` (generated `.xcodeproj` gitignored) + logic in a local SPM package - `ios-project-setup.md` |
| New Mac app | XcodeGen for a full app; a bare SPM executable only for CLIs and small agents (manual `.app` assembly in `spm-and-builds.md`) |
| Logic, models, networking | A local SPM package with `platforms: [.iOS(.v26), .macOS(.v15)]`, tested with `swift test` on the Mac - no simulator |
| Run on an iPhone | `ios-devices-and-signing.md` (Developer Mode, `devicectl`, automatic signing flags) |
| Ship | iOS: `ios-distribution.md` (TestFlight, App Store). Mac: `macos-distribution.md` (Developer ID + notarization, Mac App Store) |

SPM alone cannot produce an iOS `.app` - an app target needs an Xcode project, which is why XcodeGen generates one. XcodeGen traps (details and fixes in `ios-project-setup.md`):

- Files added after `xcodegen generate` are silently left out of the build (even with syntax errors) until you regenerate - use the `syncedFolder` source type or regenerate before every build.
- The generated Info.plist hardcodes version 1.0 (1) and ignores `MARKETING_VERSION` / `CURRENT_PROJECT_VERSION` unless you map them in `info.properties`.
- Gitignoring all of `*.xcodeproj/` also drops `Package.resolved`, so clean clones float to the newest dependency versions. Keep that one file committed.
- XcodeGen's defaults are `SWIFT_VERSION 5.0` and iPhone+iPad; set both explicitly.

### Build and test from the command line

```bash
swift test --package-path Core                      # logic, on the Mac, seconds
xcodegen generate                                   # project.yml -> App.xcodeproj
xcodebuild -project App.xcodeproj -scheme App \
  -destination 'generic/platform=iOS' CODE_SIGNING_ALLOWED=NO build   # compile check, no signing
xcodebuild -project App.xcodeproj -scheme App \
  -destination 'platform=iOS Simulator,name=iPhone 17' test           # needs a simulator runtime
xcrun simctl list runtimes                          # empty on a fresh Xcode
xcodebuild -downloadPlatform iOS                    # installs the iOS simulator runtime (GBs)
xcrun devicectl list devices                        # simulators and paired iPhones
```

Simulator.app is called DeviceHub.app in Xcode 27. CallKit runs in the iOS 27 Simulator only with two Simulator-only stand-ins - claim the `facetime` URL scheme and activate the audio session yourself (`ios-audio-and-callkit.md`). UI tests in the Simulator can also press the Action Button, lock the screen and run App Intents out of process (`testing.md`). Starting a CallKit call or Live Activity from an App Intent while the app sits in the background needs the iOS 27 `.phone.startCall` App Schema; a plain `AppIntent` is refused (`app-intents.md`).

## Concurrency (Swift 6 language mode)

Swift 6 mode makes data races compile errors. Two module-level defaults decide most of the friction:

```swift
// Package.swift target settings
swiftSettings: [
    .swiftLanguageMode(.v6),
    .defaultIsolation(MainActor.self),   // app targets: everything is @MainActor unless marked
]
```

In Xcode the same is `SWIFT_VERSION = 6` and `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` (plus `SWIFT_APPROACHABLE_CONCURRENCY = YES`, which the Xcode 27 app template sets - that template still says `SWIFT_VERSION = 5.0`, so switch it to 6). `SWIFT_STRICT_CONCURRENCY` does nothing in Swift 6 mode - checking is already complete. Make app targets MainActor by default; leave library packages nonisolated. Misspelled `enableUpcomingFeature` names are silently ignored.

```swift
nonisolated struct Report: Decodable {               // see the conformance trap below
    let title: String
}

@concurrent
func decode(_ data: Data) async throws -> Report {   // always runs off the caller's actor
    try JSONDecoder().decode(Report.self, from: data)
}

actor Cache {                                          // mutable shared state
    private var items: [URL: Data] = [:]
    func value(for url: URL) -> Data? { items[url] }
    func store(_ data: Data, for url: URL) { items[url] = data }
}
```

- **Conformance trap under MainActor default isolation**: a type's `Codable`/`Hashable` conformances become main-actor isolated, so decoding it in `@concurrent` code (or storing it with `@Attribute(.codable)`) fails with `main actor-isolated conformance of 'Report' to 'Decodable' cannot be used in @concurrent context`. Declare plain data types `nonisolated struct`.
- A plain `nonisolated async` function runs on the caller's actor (Swift 6.2+ behavior). Use `@concurrent` when you need it off the main actor.
- Value types of Sendable members are implicitly `Sendable`; a `final class` with only `let` Sendable properties can declare it. Otherwise use an `actor` or `Mutex` (Synchronization).
- Typed throws: `func load() async throws(LoadError) -> T` gives callers an exhaustive `catch`; use it for domain errors you map at a boundary, not for everything.

### Bridging delegates into a `@MainActor` class

CallKit, AVFoundation and SDK delegates call back on their own queues. Mark the delegate methods `nonisolated`, then get back onto the main actor:

```swift
@MainActor @Observable
final class CallController: NSObject, CXProviderDelegate {
    private let provider: CXProvider

    override init() {
        provider = CXProvider(configuration: CXProviderConfiguration())
        super.init()
        provider.setDelegate(self, queue: nil)   // nil = main queue, so assumeIsolated below is safe
    }

    nonisolated func providerDidReset(_ provider: CXProvider) {
        MainActor.assumeIsolated { endCall() }
    }

    nonisolated func provider(_ provider: CXProvider, perform action: CXEndCallAction) {
        action.fulfill()                          // CXAction is not Sendable - finish with it here
        MainActor.assumeIsolated { endCall() }
    }

    private func endCall() { /* update observable state */ }
}
```

- Delegate delivered on the main queue (you chose it): `MainActor.assumeIsolated` - synchronous, traps if the premise is wrong. Shorter equivalent: an isolated conformance, `extension CallController: @MainActor CXProviderDelegate`, with no `nonisolated` (rejected for protocols that require `Sendable`). Use that form when an action must be fulfilled after an `await` (e.g. `CXSetMutedCallAction` once the mic change succeeds): carrying a `CXAction` into a `Task` from a `nonisolated` method fails with `sending 'action' risks causing data races`. Inside `assumeIsolated`, write `_ = Task { ... }` - a bare `Task` is the closure's unused result and warns.
- Delegate on another thread (LiveKit `RoomDelegate`, which is `Sendable` and calls from an internal queue): `Task { @MainActor in ... }`. Tasks created that way from one serial queue start in order, but they are not ordered against callbacks from other queues, an `await` inside one lets later ones interleave, and the callback's arguments are stale by the time it runs. Make the handler idempotent (re-read the source of truth in one `refresh()`), and copy Sendable values (IDs, Bools) out of non-Sendable arguments such as `CXAction` before the hop.
- Verify concurrency code with a real build or `swiftc -emit-sil -o /dev/null`, not `-typecheck`: region-isolation errors (`sending 'x' risks causing data races`) come from the SIL pass and never appear in a typecheck. A single-file probe that uses `@main` needs `swiftc -parse-as-library` (otherwise: `'main' attribute cannot be used in a module that contains top-level code`).
- To check where async code runs, use `MainActor.assertIsolated()` / `preconditionIsolated()`: `Thread.isMainThread` is an error in async contexts in Swift 6 (`class property 'isMainThread' is unavailable from asynchronous contexts`).

Deep dives: `concurrency-isolation.md` (isolation, Sendable, delegates, typed throws), `concurrency-tasks.md` (tasks, cancellation, streams, `Observations`), `concurrency-migration.md` (GCD/Combine to async, Swift 6 migration, Swift 6.4 changes).

## State: `@Observable` controllers

```swift
@MainActor @Observable
final class AppModel {
    static let shared = AppModel()               // one instance that views and App Intents both reach
    private(set) var items: [Item] = []
    @ObservationIgnored private var loadTask: Task<Void, Never>?

    func reload() {
        loadTask?.cancel()
        loadTask = Task { items = (try? await ItemService.fetchAll()) ?? [] }
    }
}

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView().environment(AppModel.shared)
        }
    }
}

struct ContentView: View {
    @Environment(AppModel.self) private var model
    var body: some View {
        List(model.items) { Text($0.title) }
            .task { model.reload() }
    }
}
```

Owner: `@State var model = AppModel()` or a shared instance; inject with `.environment(model)`; read with `@Environment(AppModel.self)`; bind with `@Bindable var model = model`. Mark non-UI fields `@ObservationIgnored`. Architecture options and DI: `architecture.md`.

## SwiftData

```swift
@Model
final class Project {
    var name: String
    var createdAt: Date = Date.now
    @Relationship(deleteRule: .cascade, inverse: \ProjectTask.project) var tasks: [ProjectTask] = []
    init(name: String) { self.name = name }       // @Model never synthesizes an init
}

@Model
final class ProjectTask {                         // not `Task` - that shadows Swift.Task
    var title: String
    var project: Project?
    init(title: String) { self.title = title }
}

// In a view
@Query(filter: #Predicate<Project> { !$0.name.isEmpty }, sort: \Project.createdAt, order: .reverse)
private var projects: [Project]

// Scene: .modelContainer(for: [Project.self, ProjectTask.self])
// Tests: ModelContainer(for: Project.self, configurations: ModelConfiguration(isStoredInMemoryOnly: true))
```

Traps that compile but break, or do not compile at all (all reproduced on the 27 SDKs):

- `#Predicate { $0.priority == .high }` fails ("member access without an explicit base is not supported in this predicate"), and `$0.priority == Priority.high` fails with "key path cannot refer to enum case" - capture `let high = Priority.high` first. Optional chains through composite attributes (`$0.address?.city`) crash at runtime.
- The SwiftUI `.modelContainer(...)` modifiers take no `migrationPlan:`; build `ModelContainer(for:migrationPlan:configurations:)` yourself and pass it in. `VersionedSchema.versionIdentifier` must be `static let` in Swift 6.
- `ModelConfiguration` defaults to `cloudKitDatabase: .automatic`, which turns on sync as soon as the target has any CloudKit entitlement. Pass `.none` unless you want sync; with sync, every property must be optional or defaulted, no `.unique`, relationships optional.
- `ModelContext` is not Sendable. A `@ModelActor` awaited from main-actor code ran on the main thread in testing; call it from `@concurrent` code for real background work.

Models, predicates, sectioned queries: `swiftdata-models.md`. Containers, background contexts, observers, migrations, CloudKit: `swiftdata-store.md`.

## Swift Testing

```swift
import Testing
@testable import Core

struct ParserTests {
    @Test func parsesLink() throws {
        let line = try #require(Line(link: "https://example.com/voice?t=abc"))
        #expect(line.token == "abc")
    }

    @Test(arguments: ["", "http://x/voice?t=a", "https://x/voice"])
    func rejects(_ link: String) {
        #expect(Line(link: link) == nil)
    }
}
```

Traps:

- `x == .init(a: 1, b: 2)` against a `public` struct from another module that has some other public init (e.g. Decodable's `init(from:)`) fails with a misleading overload error - `cannot convert ... to '(any (~Copyable & ~Escapable).Type)?'` when `x` is optional, an `AttributedStringProtocol` or `'Grant' and '()'` error otherwise (inside or outside `#expect`). The cause: synthesized memberwise initializers are `internal`. Spelling out the type (`Grant(a:b:)`) shows the real error. Fix with `@testable import` (on by default under `swift test`), an explicit `public init`, or by comparing fields.
- A package target built with `.defaultIsolation(MainActor.self)` makes its API `@MainActor`, so its tests must be `@MainActor` too. Keep logic packages nonisolated by default.
- An iOS app target's tests need a simulator runtime (36 s warm through `xcodebuild` versus 1.4 s for the same tests under `swift test`). Exit tests are unavailable on iOS.
- `xcodebuild` UI-test runs can stall for ~10 minutes after a failure (it spawns `simctl diagnose`) or never exit after a pass - wrap them in `timeout` and enable test timeouts (`testing.md`).

Exit tests, attachments, XCTest interop, UI and simulator tests: `testing.md`.

## Swift packages

```swift
// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "Core",
    platforms: [.iOS(.v26), .macOS(.v15)],
    products: [.library(name: "Core", targets: ["Core"])],
    targets: [
        .target(name: "Core", swiftSettings: [.swiftLanguageMode(.v6)]),
        .testTarget(name: "CoreTests", dependencies: ["Core"]),
    ]
)
```

`.iOS(.v27)` / `.macOS(.v27)` need `swift-tools-version: 6.4`; older tools versions fail with `'v27' is unavailable`. Plugins, macros, Swift Build, `xcodebuild` basics, the Xcode MCP server and Xcode 27 build-breakers: `spm-and-builds.md`.

## Keychain

Store tokens and credentials with `SecItemAdd` / `SecItemCopyMatching` / `SecItemUpdate` as generic passwords. Use `kSecAttrAccessibleAfterFirstUnlock` when a background task or a locked-phone call must read the item; the default `...WhenUnlocked` fails while locked. `...ThisDeviceOnly` variants never leave the device (no backup restore, no migration). Update an existing item with `SecItemUpdate` rather than delete-then-add. On macOS the data protection keychain (`kSecUseDataProtectionKeychain`) fails with `-34018 errSecMissingEntitlement` unless the binary carries a provisioning profile - ad hoc and plain Apple Development signatures are not enough. Helper and macOS differences: `keychain.md`.

## Foundation Models (iOS 26+ / macOS 26+)

```swift
import FoundationModels

@Generable
struct Summary {
    @Guide(description: "At most five words") var title: String
    var points: [String]
}

func summarize(_ text: String) async throws -> Summary? {
    guard case .available = SystemLanguageModel.default.availability else { return nil }
    let session = LanguageModelSession(instructions: "Summarize the user's text.")
    return try await session.respond(to: text, generating: Summary.self).content
}
```

The on-device model has a 4096-token context (read `SystemLanguageModel.default.contextSize` rather than hard-coding it - on 27 it comes from the runtime model); `PrivateCloudComputeLanguageModel()` (27+, managed entitlement) has 32K. Errors: `LanguageModelError` (iOS/macOS 27+) replaces the deprecated `LanguageModelSession.GenerationError`; apps that still deploy to 26 catch both behind `#available`. Custom adapters are unavailable at a 27.0 deployment target. Tools, streaming, image input, PCC and Core AI: `foundation-models.md`.

## Xcode 27 / iOS 27 / macOS 27 changes that bite

- **Liquid Glass is mandatory** for apps built with the 27 SDKs: `UIDesignRequiresCompatibility` is ignored.
- **ld64 is removed**: `-ld_classic` is now ignored with a warning (fatal only under warnings-as-errors); delete it from `OTHER_LDFLAGS`.
- **SwiftPM 6.4 builds with Swift Build**: products land in `.build/out/Products/<Config>` (`.build/release` is a symlink); hardcoded `.build/arm64-apple-macosx/release` paths break.
- **macOS universal binaries**: `ARCHS_STANDARD` drops x86_64 when the deployment target is macOS 27+.
- **Export methods** (renamed back in Xcode 15.3, still common in old scripts): `app-store` / `ad-hoc` / `development` are deprecated; use `app-store-connect` / `release-testing` / `debugging`.
- **Device registration** from the command line needs `-allowProvisioningDeviceRegistration` in addition to `-allowProvisioningUpdates`.
- **Audio interruptions**: `AVAudioSession.interruptionNotification` is deprecated on iOS 27 in favor of the typed `didBecomeInactive` and `resumptionRecommendation` messages. Swift does not warn on leftover `interruptionNotification` observers - grep for them.
- **Documents**: new class-bound `Document` (`ReadableDocument` + `WritableDocument`) protocols whose `DocumentReader` / `DocumentWriter` do the `@concurrent` read/write; `FileDocument` is soft-deprecated.
- **UIKit life cycle**: apps built with the iOS 27 SDK must adopt the scene-based life cycle or they fail to launch.
- **Launch screen required**: iOS apps built with the 27 SDK need `UILaunchScreen` (or `UILaunchStoryboardName`, `UILaunchStoryboards`, `UILaunchScreens`) in Info.plist; App Store submission rejects them otherwise.
- **On-Demand Resources** and `NSBundleResourceRequest` are deprecated; use Background Assets.
- **Previews**: `PreviewProvider` is deprecated in favor of `#Preview`, whose body now runs on the main actor.
- **Mac Catalyst (Xcode 27.1/27.2 known issue)**: iOS 27.1-only APIs fail to compile for Catalyst ("cannot find", "has no member") - guard them with `#if !targetEnvironment(macCatalyst)`.

## Platform

### iOS

| Topic | Reference |
|-------|-----------|
| XcodeGen project, Info.plist keys, local package, build commands | `ios-project-setup.md` |
| WindowGroup, scenePhase, NavigationStack, sheets, toolbars, Settings deep link, Liquid Glass | `ios-swiftui.md` |
| Simulator runtimes, `simctl`/`devicectl`, Developer Mode, CLI signing, ASC API keys | `ios-devices-and-signing.md` |
| Dev install, ad hoc, TestFlight, App Store, certificates | `ios-distribution.md` |
| `AVAudioSession`, mic permission, interruptions, CallKit outgoing calls, LiveKit, screen-locked audio | `ios-audio-and-callkit.md` |
| App Intents, App Shortcuts, Action Button, Siri, App Schemas (background call start), Live Activities, Control Center controls (also macOS) | `app-intents.md` |

### macOS

| Topic | Reference |
|-------|-----------|
| Scenes, windows, Settings, MenuBarExtra, documents, termination, `LSUIElement` | `macos-app-lifecycle.md` |
| Table, sidebar, inspector, menus and commands, forms, popovers, 27-SDK SwiftUI changes | `macos-swiftui.md` |
| `NSViewRepresentable`, hosting, AppKit Liquid Glass, pasteboard, `NSPanel` HUDs | `macos-appkit-interop.md` |
| Shortcuts, drag and drop, bookmarks, AXUIElement (read it before using `kAXTrustedCheckOptionPrompt`, which Swift 6 rejects as shared mutable state), login items, XPC, logging, privacy strings | `macos-system-integration.md` |
| ScreenCaptureKit (`SCStream`, filters, audio-only capture, TCC) | `macos-screencapturekit.md` |
| Recording pipeline: AVAudioEngine, AVAssetWriter, SpeechAnalyzer, silent-recording traps | `macos-audio-pipeline.md` |
| Per-process audio with Core Audio taps | `macos-core-audio-tap.md` |
| Developer ID, notarization, signing bare CLI binaries, sandbox, Mac App Store, Sparkle | `macos-distribution.md` |

### Shared

| Topic | Reference |
|-------|-----------|
| Isolation, actors, Sendable, delegate bridging, typed throws | `concurrency-isolation.md` |
| Tasks, cancellation, AsyncStream, Observations, continuations | `concurrency-tasks.md` |
| GCD/Combine migration, Swift 6 migration, Swift 6.4 features | `concurrency-migration.md` |
| `@Model`, relationships, predicates, `@Query` | `swiftdata-models.md` |
| Container, contexts, observers, migrations, CloudKit | `swiftdata-store.md` |
| App structure, controllers, DI | `architecture.md` |
| Swift Testing, traps, UI and simulator tests (Action Button, lock, App Intents), `xcodebuild` stalls | `testing.md` |
| Package.swift, plugins, macros, Swift Build, build-breakers, Xcode MCP server | `spm-and-builds.md` |
| Generic-password helper, accessibility classes | `keychain.md` |
| Foundation Models (on-device and Private Cloud Compute), Core AI | `foundation-models.md` |
