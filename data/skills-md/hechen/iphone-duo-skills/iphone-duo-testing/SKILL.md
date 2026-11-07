---
name: iphone-duo-testing
description: Plan and execute iPhone Duo app QA across open, closed, folded, and rotated poses, Split View, keyboard and sheet states, accessibility, camera and accessory capability loss, and older iPhones, with reproducible evidence. Use when testing an app in the iPhone Duo simulator or Device Hub, writing XCUITest coverage for display transitions, deciding what needs a physical device, or preparing Duo release evidence such as screenshot sizes.
license: MIT
---

# iPhone Duo testing

Read [test matrix](references/test-matrix.md). Build a matrix around the requested flows and the actual available environment. Record the candidate revision and build, Xcode build, SDK, runtime or device, and relevant settings.

## Discover before executing

Use `xcodebuild -version`, `xcodebuild -showsdks`, `xcrun simctl list runtimes`, and `xcrun simctl list devices available` when available. Discover the project's scheme and destinations. Never invent a device identifier or a fold-control command-line flag. Change poses with Device Hub's controls for the iPhone Duo simulator, or with documented automation on a physical device.

If Duo tooling is absent, continue meaningful resize, model, and existing-platform tests. Label those results as proxies. Leave actual Duo transitions untested rather than converting proxy coverage into device validation.

## Exercise transitions

Select a real task with state: an unsaved draft, selected item, queued upload, or playing video. Establish the initial state, apply the transition, and then complete or cancel the task. Verify both visible UI and persistent output.

Test intermediate constraints, not just launch at two endpoint sizes. Check that asynchronous work runs the intended number of times, navigation remains coherent, and focus does not disappear into a hidden view. Include error recovery for features that depend on a camera or accessory.

Use automated assertions for stable observable outcomes. In UI tests, let layout settle after typing, presenting, or changing pose before resolving the next element, and never add a retry tap: it hides real bugs. Use screenshots for layout evidence and interaction checks for reachability and accessibility. An accessibility audit supplements manual assistive-technology testing; it does not replace it.

## Report

For each scenario, record `precondition / action / expected / observed / environment / evidence / status`. Use `pass`, `fail`, `blocked`, or `not run`; give a reason for missing evidence. Separate simulator limitations from app failures. Link relevant screenshots, recordings, test results, or logs using synthetic or redacted data.

Finish with failures ranked by user impact, verified scope, and the remaining device-specific checks. A green build or a type-check certifies neither correct folding behavior nor submission readiness.
