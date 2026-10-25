---
name: iphone-duo-readiness
description: Audit an existing SwiftUI or UIKit iPhone app for iPhone Duo and prioritize the migration from its actual Xcode, SDK, deployment target, layouts, navigation, and scene model. Use when asked whether an app is ready for iPhone Duo or the foldable iPhone, what breaks on the outer or inner display, what the Xcode 27.1 SDK changes, how to handle Mac Catalyst and 27.1/27.2 toolchain branches, or where to start a Duo migration.
license: MIT
---

# iPhone Duo readiness

Produce a concrete migration assessment before broad edits. Read [platform evidence](references/platform.md) for the linked-SDK behavior, toolchain branches, and audit searches.

## Establish the baseline

Inspect repository instructions, supported platforms, deployment targets, project generation inputs, and the app's main flows. Record the selected Xcode and installed SDKs with `xcodebuild -version` and `xcodebuild -showsdks`, and the runtimes with `xcrun simctl list runtimes`. Discover actual destinations instead of assuming a Duo simulator is installed.

Separate improvements that compile today from work that needs the iOS 27.1 SDK. A runtime `#available` check cannot resolve a symbol absent from the build SDK, and it does not change what linking the newer SDK does to screen space and bars. Do not raise a deployment target, change the team's selected Xcode, or install a beta as an incidental audit step.

## Trace assumptions to behavior

Search production sources and project configuration for candidates such as:

```sh
rg -n 'UIScreen\.main|UIDevice\.current\.orientation|userInterfaceIdiom|UIRequiresFullScreen|UISupportedInterfaceOrientations|supportedInterfaceOrientations' .
rg -n 'UIToolbar\(|UINavigationBar\(|UITabBar\(|safeAreaInsets\.(left|right)' .
```

Treat matches as review leads. An idiom check for an unrelated platform behavior may be valid. Follow each layout use to its container, coordinate space, and owner; don't replace strings mechanically. Inspect manually positioned overlays, fixed bar heights, cached screen metrics, arithmetic that assumes equal left and right insets, and separate compact/regular view trees that may recreate editor state.

For each issue, explain a user-visible trigger, the responsible code location, a scoped remedy, and how to reproduce and verify it. Rank data loss or unavailable primary actions above cosmetic spacing. Keep public interfaces and existing platform behavior intact unless the requested change requires otherwise.

## Deliver or implement within scope

For an audit, return prioritized findings, the applicable SDK and Catalyst constraints, and a proposed sequence. For an implementation request, make the supported changes and run relevant checks; isolate deferred API adoption with its reason. Hand layout, bar, scene, camera, and QA work to the matching `iphone-duo-*` skill when it is installed.

Use a report table with `flow / file / failure / proposed change / evidence / remaining check`. Distinguish source review, compilation, simulator execution, and device execution. Never convert an unexecuted scenario into a pass.
