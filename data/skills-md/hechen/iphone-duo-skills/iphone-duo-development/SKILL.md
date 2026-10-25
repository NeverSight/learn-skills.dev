---
name: iphone-duo-development
description: Entry point for building, migrating, or reviewing an iPhone app for iPhone Duo, the foldable iPhone with an outer and an inner display, on iOS 27.1. Use when a SwiftUI, UIKit, or AVFoundation app has to handle opening, closing, folding, or rotating the device; fold divisions and camera occlusions (reserved regions); ArrangementView or UIArrangementViewController; navigation bars, toolbars, and tab bars on the vertical axis; hinge state; Split View and multiple scenes; camera direction; or a CameraCaptureAccessory. Establishes the Xcode 27.1 toolchain baseline, then routes each part of the work to the focused iphone-duo-* skills.
license: MIT
---

# iPhone Duo development

Start here when Duo work is broad or its scope is unclear. This skill sets the toolchain baseline, orders the work, and hands each part to a focused skill. For API spellings, availability, and Apple links, read the [API map](references/api-map.md).

## Establish the baseline

Inspect repository instructions, targets, deployment versions, Mac Catalyst destinations, and the selected toolchain with `xcodebuild -version`, `xcodebuild -showsdks`, and `xcrun simctl list runtimes`. Keep the existing deployment target and a working path for every other iPhone.

As checked 2026-09-25, the Duo SDK and simulator ship with Xcode 27.1 beta, and Apple's Xcode 27.2 beta notes send Duo work back to 27.1 beta. A higher version number does not prove the SDK declares the Duo APIs; check the declaration or compile a probe.

- Linking with the iOS 27.1 SDK is what gives the app the full screen and system bars on the vertical axis. A runtime `#available` check does not change linked-SDK behavior and cannot make a missing symbol compile.
- Put new calls behind iOS 27.1 availability. Xcode 27.1 beta cannot compile 27.1-only APIs for Mac Catalyst; isolate them with `#if !targetEnvironment(macCatalyst)`.
- Do not install a beta, switch the team's Xcode, or raise a deployment target as an incidental step. Report the blocker instead.

## Route the work

| Need | Skill |
| --- | --- |
| Audit an existing app and plan the migration | `iphone-duo-readiness` |
| Review hierarchy, continuity, and reachability before code | `iphone-duo-design` |
| Fold and camera regions, arrangements, custom layout | `iphone-duo-layout` |
| Navigation bars, toolbars, and tab bars on the vertical axis | `iphone-duo-toolbars` |
| Multiple windows, hinge input, scene accessories | `iphone-duo-scenes` |
| Camera direction, mirroring, rotation, capture pipeline | `iphone-duo-camera` |
| Pose and transition QA, UI tests, release evidence | `iphone-duo-testing` |

These are sibling skills from the same collection. Load only the ones the task needs. If one is not installed, install the full set from [hechen/iphone-duo-skills](https://github.com/hechen/iphone-duo-skills) rather than guessing its contents.

## Order the work

1. Audit fixed screen sizes, idiom and orientation branches, symmetric inset arithmetic, and hand-built bars. Reproduce one failing view before changing architecture.
2. Base layout on the current container, size classes, and independent safe-area edges. Keep navigation, selection, drafts, and playback stable while the same scene changes size or display.
3. Use standard navigation and tab containers first. Add an arrangement only for content with a real primary/secondary relationship. Keep essential actions reachable in every pose.
4. For custom layouts, query reserved regions in local coordinates, handle divisions and occlusions separately, filter on `isActive`, and check right-to-left layout.
5. Use hinge state only when the feature needs it. An angle is not a layout region. Handle an absent hinge without disabling ordinary features.
6. Verify the real app through the testing matrix. Report compilation, simulator interaction, physical-device capture, and distribution readiness separately.

## Other UI stacks

For Flutter, React Native, game engines, or web-backed UI, first check the installed framework or plugin's current iOS support. Fix container resizing and safe-area handling in that layer. If it lacks the native information you need, design a small typed bridge for the specific region or camera capability, and document its coordinates, units, availability, and lifecycle. Do not assume an Android fold API reports iOS data. This collection has no tested adapters for those frameworks.

Apple's App Resizability skill in Xcode 27.1 is a separate tool. It can run alongside these skills.

## Report

State what changed, the Xcode build, SDK, and runtime used, which poses and transitions were exercised, and what is still untested. Do not call an app Duo-ready on the strength of a type-check or a static screenshot.
