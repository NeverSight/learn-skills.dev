---
name: macos-dev
description: >-
  This skill should be used to build native Apple macOS (Mac) desktop apps in
  Swift with SwiftUI, SwiftData, and the macOS 26 "Tahoe" stack — whenever the
  user wants to create, scaffold, design, debug, or extend a Mac app: windows &
  scenes (WindowGroup/Window/Settings/MenuBarExtra), the global menu bar and
  keyboard-shortcut Commands, NavigationSplitView/Table/inspectors, Liquid
  Glass, @Observable state and the Mac focus system, SwiftData/CloudKit
  persistence, Swift 6 concurrency, AppKit interop, document-based apps,
  menu-bar/background/login-item processes, on-device Apple Intelligence
  (Foundation Models), StoreKit 2, accessibility, testing, and the Mac ship
  gauntlet (App Sandbox, Hardened Runtime, Developer ID signing + notarization,
  or Mac App Store) — even when the request never says "macOS" or "SwiftUI"
  (e.g. "make me a Mac app", "a menu bar app", "a little utility for my Mac").
  NOT for iPhone/iPad apps (use ios-dev), visionOS (use visionos-dev), Mac
  Catalyst, or Electron/Tauri web wrappers.
metadata:
  version: "1.0.0"
---

# Building native macOS apps

Build **native** Mac apps — Swift + SwiftUI + SwiftData, authored in Xcode
against the current **macOS 26 "Tahoe"** stack. Native is the right default: the
full desktop look-and-feel (Liquid Glass for free, a real menu bar), the deepest
OS integration (menu-bar extras, Services, Spotlight, on-device AI), the best
performance, and both shipping paths (direct download *and* Mac App Store).
Electron, Tauri, and Catalyst suit teams sharing a web or iPad codebase — out of
scope here.

This skill ships a **buildable starter** (a real sidebar → table → inspector app,
**compiled and unit-tested green on Xcode 26.5 / macOS 26**) and **focused
reference files**. Read them on demand — do not dump them all into context. The
map is the decision tree below.

## Start here: the mental model

A SwiftUI Mac app is four nested ideas, plus one thing iOS lacks — a real menu bar:

| Layer | What it is | The modern idiom (macOS 26) |
|---|---|---|
| **App → Scene** | The `@main struct …: App` returns `Scene`s. | `WindowGroup` (main windows) **plus** Mac-only scenes: `Settings` (the ⌘, window), `Window` (one unique window), `MenuBarExtra` (a menu-bar app), `DocumentGroup` (document apps). |
| **Menu bar** | A *global*, always-present surface with no iOS equivalent. | `.commands { … }` adds/extends menus; items act on the **frontmost** window via the **focus system** (`@FocusedValue`), and `.disabled()` when nothing is actionable. |
| **View** | Value-type structs that describe UI; the framework diffs and re-renders. | Composed small views; multi-column `NavigationSplitView`; `Table` for dense data; `.inspector`, `.toolbar`; pointer-first (hover, right-click menus, keyboard shortcuts). |
| **State** | Reference-type models the views observe. | The **`@Observable` macro** (Observation) — *not* `ObservableObject`/`@Published`. Read with `@State` (own), `@Environment` (inject), `@Bindable` (bind); publish to menus with `@FocusedValue`. |
| **Persistence** | Where data lives across launches. | **SwiftData** (`@Model`, `@Query`, `ModelContainer`), optionally synced with CloudKit. In a sandboxed app, data lives in the app *container*. |

Three cross-cutting facts shape *all* current Mac code:

- **Liquid Glass is free and automatic.** Building against the macOS 26 SDK
  restyles standard controls, toolbars, sidebars, and menus to translucent glass
  with **no code changes**. Write `.glassEffect(...)` only on *custom* views.
  Glass is chrome — never stack it on glass, never put it on content.
- **Swift 6.2 makes app code single-threaded by default.** A new Xcode 26 target
  enables **"Approachable Concurrency"** and **default `@MainActor` isolation**, so
  UI, view models, and SwiftData run on the main actor with zero `Sendable`
  ceremony. Opt *in* explicitly: `@concurrent` to offload heavy work, an `actor`
  for shared state, `@ModelActor` for background SwiftData.
- **Shipping a Mac app is a gauntlet iOS lacks.** No single store chokepoint:
  choose **Mac App Store** *or* **direct distribution**, where the direct path
  requires **App Sandbox + Hardened Runtime → Developer ID signing → notarization
  → stapling** or Gatekeeper blocks it on other Macs. Plan from day one —
  forgotten entitlements hurt to add late.

Everything else is detail in the references.

## Decision tree → which reference to read

- **Project / Xcode / SDK & deployment target / Swift 6 build settings / command-line build & run?**
  → `references/project-setup.md`, then scaffold with the template (below).
- **App entry, lifecycle, `NSApplicationDelegateAdaptor`, activation, state restoration?**
  → `references/app-structure.md`
- **Windows & scenes — `WindowGroup` vs `Window` vs `Settings` vs `MenuBarExtra`, multiple/utility windows, sizing/positioning/restoration?**
  → `references/windows-and-scenes.md`
- **The menu bar & shortcuts — `Commands`, `CommandGroup`/`CommandMenu`, `@FocusedValue`-driven items, the responder chain?**
  → `references/menus-and-commands.md`
- **Views, layout, `Table`/`List`, outline views, dense desktop surfaces, animation, SF Symbols?**
  → `references/views-and-layout.md`
- **Adopting Liquid Glass on custom UI (glass effects, containers, toolbars, sidebars)?**
  → `references/liquid-glass.md`
- **State, the `@Observable`/Observation framework, and the Mac focus system (`@FocusedValue`/`@FocusedObject`/`@FocusedBinding`)?**
  → `references/state-and-focus.md`
- **Saving data — SwiftData, migration, CloudKit sync, Core Data, files & the sandbox container?**
  → `references/data-persistence.md`
- **Swift 6 concurrency (actors, `@MainActor`, `@concurrent`), async/await, URLSession networking?**
  → `references/concurrency-and-networking.md`
- **Dropping to AppKit — `NSViewRepresentable`/`NSViewControllerRepresentable`, `NSHostingView`, bridging SwiftUI ⇄ AppKit?**
  → `references/appkit-interop.md`
- **A document-based app — `DocumentGroup`, `FileDocument`/`ReferenceFileDocument`?**
  → `references/documents.md`
- **Moving data in/out — drag-and-drop, pasteboard, Services, Share, Open/Save panels, Spotlight, Quick Look?**
  → `references/system-integration.md`
- **Living in the background — menu-bar-only apps, login items, `launchd` agents, XPC helpers, AppleScript/Shortcuts, extensions?**
  → `references/automation-and-background.md`
- **On-device AI — the Foundation Models framework, Writing Tools, Image Playground, Visual Intelligence on the Mac?**
  → `references/apple-intelligence.md`
- **Charging for it — StoreKit 2 in-app purchase **vs.** the direct-sale licensing fork (MAS vs Developer ID)?**
  → `references/monetization-storekit.md`
- **A system framework (MapKit, Swift Charts, PhotosUI, AVFoundation, Core Location, EventKit, Contacts…) and its entitlements?**
  → `references/frameworks.md`
- **Designing it well (Mac HIG, Liquid Glass craft, typography, color, the squircle app icon) and accessibility + localization?**
  → `references/design-and-accessibility.md`
- **Testing (Swift Testing), Previews, debugging, Instruments, logging?**
  → `references/testing-and-debugging.md`
- **Performance tuning and the Mac App Store path (privacy manifest, App Store Connect, TestFlight for Mac)?**
  → `references/performance-and-shipping.md`
- **The ship gauntlet — App Sandbox, Hardened Runtime, Developer ID signing, **notarization**, stapling, Gatekeeper, entitlements?**
  → `references/distribution-and-signing.md`
- **Dev tooling (Xcode 26 AI features, SPM, swift-format, CI) and which Mac libraries (Sparkle, etc.) to use or skip?**
  → `references/tooling-and-ecosystem.md`

When the latest API details matter, verify against current Apple docs via the
**context7** MCP (e.g. `/websites/developer_apple_swiftui`, the SwiftData and
Foundation Models sites) or **WebSearch/firecrawl** — Apple's reference pages are
JavaScript-rendered (a plain fetch often returns only the title; use firecrawl or
a rendered scrape), and the platform changes every season, so training data may
lag a release. Re-confirm version claims against Apple's live docs
(developer.apple.com) before stating them.

## The build workflow

1. **Confirm prerequisites** (see end of this file). Building a Mac app needs
   **full Xcode 26+** (not just Command Line Tools) with the macOS 26 SDK. Unlike
   iOS, **there is no simulator** — a Mac app runs natively on the dev Mac, so
   verifying behavior is easy. If full Xcode is not the active developer dir,
   prefix builds with `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer`
   (no `sudo`).

2. **Scaffold from the template** rather than hand-rolling project files:

   ```bash
   python3 <skill>/scripts/new_macos_app.py "AppName" \
       --bundle-id com.yourco.appname --dest ~/Developer/AppName
   ```

   This produces a verified, renamed source tree (a sidebar → `Table` → detail +
   inspector app with SwiftData, Liquid Glass, an `@Observable` window model
   feeding menu commands via `@FocusedValue`, App Sandbox + Hardened Runtime, and
   a Swift Testing suite) and runs `xcodegen generate` if XcodeGen is installed.
   Then `open AppName.xcodeproj` and press Run (⌘R). It signs **ad-hoc** ("Sign
   to Run Locally"), so running it locally needs no Apple Developer account.

3. **Build features** by reading the relevant reference(s) and following their
   patterns. Keep model state in `@Observable` classes (or SwiftData `@Model`s),
   share it through the environment, publish what menus act on via `@FocusedValue`,
   and stay on the main actor unless there is a measured reason to leave it.

4. **Verify behavior before claiming success** — the user may not read Swift,
   so run it. Because it is a Mac app, build and launch it
   directly: compile, run, drive the feature, and capture a screenshot or
   describe what happened. Exercise the menu commands and shortcuts, resize the
   window, toggle the sidebar/inspector. To build and test from the CLI:

   ```bash
   DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer \
     xcodebuild -project AppName.xcodeproj -scheme AppName \
     -destination 'platform=macOS' -derivedDataPath /tmp/AppName-DD test
   ```

5. **Profile and ship** — view-update cost, launch time, memory — then walk the
   **distribution gauntlet** for the chosen path (sandbox/entitlements →
   Developer ID + notarize + staple, or Mac App Store) using
   `references/distribution-and-signing.md` and `references/performance-and-shipping.md`.

## High-leverage rules (the things that most often go wrong)

The "why" matters more than the rule — understand it and the rest generalizes.

- **Build SDK ≠ deployment target.** Since **April 28, 2026** the App Store
  rejects uploads not built with the **macOS 26 SDK (Xcode 26+)** — but that does
  not force users onto macOS 26. Keep the **deployment target** as low as needed
  (macOS 14/15…) and guard macOS 26-only APIs with `if #available(macOS 26, *)`.
  Never ship a build made with the Xcode 27 / macOS 27 **beta** SDK.

- **Use `@Observable`, not `ObservableObject`.** The modern idiom is the
  `@Observable` macro + `@State`/`@Environment`/`@Bindable`. Avoid the legacy
  `@Published`/`@StateObject`/`@ObservedObject`/`@EnvironmentObject` Combine stack
  in new code — it invalidates views far more coarsely.

- **Menu commands act on the *frontmost* window via focus, not view-local state.**
  The menu bar is global; a command cannot reach into one window's `@State`.
  Publish what it needs with `.focusedSceneValue(model)` / `@FocusedValue`, read
  that in the `Commands`, and `.disabled(...)` the item when nothing is
  actionable. This is the biggest SwiftUI-on-Mac concept iOS never teaches.

- **`NavigationSplitView` columns are selection-driven; register `navigationDestination` once.**
  The Mac default is the three-column split driven by **selection bindings**, not
  `NavigationLink`. Where a push happens, declare `.navigationDestination(for: T.self)`
  **once** at push time (not inside a row or lazy branch) or pushes silently fail.

- **Stay on the main actor; offload deliberately.** With Swift 6.2 default
  isolation, UI and models are `@MainActor` for free. Do not sprinkle
  `@MainActor`/`@unchecked Sendable` to silence errors, and note a plain
  `nonisolated async func` runs on the caller's actor (SE-0461), not the
  background. To go off-main, mark the heavy function `@concurrent` or use an `actor`.

- **SwiftData models are not `Sendable`.** `@Model` objects and `ModelContext`
  cannot cross actor/thread boundaries — passing them is a compile error. For
  background work use a `@ModelActor`, pass `PersistentIdentifier`s, then re-fetch.
  Mark `@Model` classes `final`.

- **CloudKit sync imposes a model contract.** SwiftData + CloudKit requires every
  property optional-or-defaulted, every relationship optional, and **no**
  `@Attribute(.unique)`/`#Unique`. Add the iCloud + Background Modes capabilities
  and deploy the schema to **Production** before release.

- **The App Sandbox is a wall, not a suggestion.** A sandboxed app touches only
  its own container until granted entitlements. Reading a user-picked file needs
  `files.user-selected.read-write`; *re-opening* it next launch needs a
  **security-scoped bookmark**. Network, camera, mic, location each need their own
  entitlement **and** an Info.plist usage string. Add only what the app uses —
  every extra entitlement narrows what App Review and notarization accept.

- **Direct distribution = sign + notarize + staple, or Gatekeeper blocks it.**
  Outside the Mac App Store: enable **Hardened Runtime**, sign with a **Developer
  ID Application** cert, submit for **notarization**, then **staple** the ticket to
  the app/DMG. Skip a step and users hit "cannot be opened… Apple could not check
  it for malicious software." The Mac App Store is the alternative (different
  signing, App Review instead of notarization).

- **Liquid Glass is chrome, not content.** Glass cannot sample other glass — never
  nest `.glassEffect`, never make rows or large content surfaces glass, and do not
  over-tint. Group custom glass shapes in a `GlassEffectContainer`. The redesign
  comes **free** from building with Xcode 26; only custom UI needs adoption.

- **On-device Apple Intelligence needs Apple silicon — and Tahoe still runs on
  Intel.** macOS 26 is the *last* Intel-supporting release, but the Foundation
  Models LLM runs **only on Apple silicon with Apple Intelligence enabled**. Check
  `SystemLanguageModel.default.availability` and degrade gracefully — the app may
  sit on an Intel Mac that cannot run the model.

- **AppKit is never far.** SwiftUI covers most of a Mac app; for the gaps —
  fine-grained text, certain window behaviors, status-item nuance, drag sessions —
  drop to AppKit via `NSViewRepresentable`/`NSViewControllerRepresentable` or hook
  the app with `NSApplicationDelegateAdaptor`. See `references/appkit-interop.md`.

## Platform status (verify before relying on it — macOS moves fast)

As of mid-2026 (research-dated **2026-06-21**, the week after WWDC 2026; verified
on macOS **26.5.1** / Swift **6.3.2**, 2026-06-21):

- **macOS 26 "Tahoe"** is the current shipping line (numbering jumped 15 → 26 at
  WWDC 2025; no macOS 16–25). GA **Sep 15, 2025**; latest **26.5.1** (June 1,
  2026). It introduced **Liquid Glass**, the **Foundation Models** on-device LLM,
  **Swift 6.2 Approachable Concurrency**, SF Symbols 7, and Metal 4. **Tahoe is
  the last Intel-supporting macOS.**
- **macOS 27 "Golden Gate"** (WWDC 2026, June 8–12) is in developer beta —
  **pre-GA, ships fall 2026, Apple-silicon-only**. Treat its APIs as subject to
  change; do not target it as a deployment floor.
- **Toolchain:** **Xcode 26.5** is current (Swift **6.3**; use **Swift 6 language
  mode**). **Xcode 27** (Swift 6.4) is a beta needing a host on macOS 26.4+.
- **App Store:** since **April 28, 2026**, uploads must use **Xcode 26+ / the
  macOS 26 SDK** or later. **SF Symbols 7** ships with macOS 26; **8** is pre-GA.
  App icons must be **squircles** under Tahoe's icon look.

Re-confirm "latest" claims against Apple's docs (context7 / WebSearch) before
stating them.

## Prerequisites & environment

- **macOS Tahoe 26.x** with **full Xcode 26+** and the **macOS 26 SDK** (bundled).
  *Command Line Tools alone cannot build an app target.* (If `xcode-select -p`
  points at CommandLineTools, prefix builds with
  `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer`.)
- **No simulator** — a Mac app runs natively on the development Mac.
- **Swift 6 language mode** with Approachable Concurrency (the template sets
  `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`).
- Optional: **XcodeGen** (`brew install xcodegen`) for project generation.
- An **Apple Developer account** ($99/yr) is required to **ship** (Developer ID +
  notarization, or the Mac App Store) — but **not** to build and run locally,
  since the template signs ad-hoc.

If a required piece is missing, surface it immediately and offer to help — do not
generate code and imply it ran when it could not.

## What's in this skill

```
macos-dev/
├── SKILL.md                        (this file — orientation + workflow + map)
├── README.md                       (human-facing overview & install)
├── references/                     (21 focused deep-dives; read on demand — see the decision tree)
├── scripts/new_macos_app.py        (scaffold a renamed copy of the template)
└── assets/templates/MacScaffold/   (verified buildable starter: sidebar → Table →
                                     detail + inspector, SwiftData, Liquid Glass,
                                     @FocusedValue menu commands, Swift Testing)
```
