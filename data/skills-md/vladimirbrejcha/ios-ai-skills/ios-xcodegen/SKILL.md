---
name: ios-xcodegen
description: "XcodeGen workflows for iOS/iPadOS apps: generate projects from project.yml/project.yaml, fix build/test destination issues, wire asset catalogs, configure test hosts, manage SwiftPM resolution in CI, and resolve App Store packaging errors related to embedded static libraries."
---

# XcodeGen iOS workflow

## Quick start
- Treat `project.yml` (or `project.yaml`) as the source of truth; regenerate with `xcodegen generate` before building.
- Do not edit the generated `.xcodeproj` directly; delete and regenerate as needed.

## Build / Run
- For “Designed for iPad on Mac” builds, use a macOS destination with `variant=Designed for iPad` when available.
- For tests, prefer an iOS Simulator if any vendor frameworks lack Mac Catalyst support.

## Tests
- Ensure the test target is added to the scheme and has a host app if required.
- If tests show 0 cases, recheck the scheme and any test plan configuration.
- If `@testable import` fails, confirm the host app module name and that tests build for the same destination as the host.

## Resources / Assets
- Asset catalogs and storyboards must be in the resources build phase. In XcodeGen, add them under `sources` with `buildPhase: resources`.
- Enable asset symbol generation when code uses generated `ColorAsset`/`ImageAsset` symbols:
  - `ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOLS=YES`
  - `ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS=YES`

## SwiftPM in CI
- If CI disables automatic dependency resolution, ensure `Package.resolved` is committed or copied to the expected location (usually `.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`) before build.
- Keep versions pinned in `project.yml` when deterministic builds are required.

## App Store Connect packaging issues
- Static `.a` files must never appear under `*.app/Frameworks`.
- XcodeGen does not support a `library:` dependency key; to link a `.a` file, use:
  - `framework: path/to/libSomething.a`
  - `embed: false`
- XCFrameworks that contain static libs should also be linked only:
  - set `embed: false` for those XCFrameworks to avoid `.a` slices being copied into `Frameworks/`.
- Verify the generated project’s “Embed Frameworks” build phase contains only dynamic frameworks that must be embedded.

## Diagnostics / sanity checks
- Regenerate and clean Derived Data after changing `project.yml`.
- After archiving, inspect the app bundle’s `Frameworks/` directory; it should contain only dynamic frameworks and Swift runtime libraries.
