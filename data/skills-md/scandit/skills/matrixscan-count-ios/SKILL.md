---
name: matrixscan-count-ios
description: MatrixScan Count (BarcodeCount) in native iOS projects (Swift/Objective-C, ScanditBarcodeCapture) — counting and receiving barcodes in bulk with the BarcodeCountView UI in UIKit or SwiftUI, scanning against an expected/receiving list, spatial map, explicitly managed camera. Use for integration, settings and symbology configuration, result handling, UI customization, status mode, or troubleshooting counting workflows.
license: Apache-2.0
metadata:
  author: scandit
  version: "0.1.1"
---

# MatrixScan Count iOS Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The MatrixScan Count API has evolved across SDK versions — classes, properties, and initializers may have been renamed or restructured.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or view modifiers. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

The single most common mistake is assuming the view owns the camera: in MatrixScan Count the **`BarcodeCountView` does NOT own or manage the camera** — you create and drive the camera explicitly (`Camera.default`, apply `BarcodeCount.recommendedCameraSettings`, `context.setFrameSource`, and switch its state across the lifecycle). See [references/integration.md](references/integration.md) (Camera section).

## Scope

This skill is scoped to the **MatrixScan Count counting workflow**: `DataCaptureContext`, the `BarcodeCount` mode, `BarcodeCountSettings` (symbologies, per-symbology tuning, `expectsOnlyUniqueBarcodes`), `BarcodeCountView` (the built-in AR counting UI with Icon / Dot styles), the explicitly-managed camera frame source and lifecycle, `BarcodeCountListener` for collecting scanned barcodes, the List / Exit / Single-Scan button callbacks (`BarcodeCountViewUIDelegate`), feedback, control visibility, customizing the AR highlights (per-state brushes / icons / taps), and scanning against an expected/receiving list (`BarcodeCountCaptureList` + `TargetBarcode`).

Also covered: **filtering** (count only some of the barcodes in the scene), the **hardware trigger** (volume button), and **scan preview** (`BarcodeCountSettings(scanPreviewEnabled:)`) — see the Advanced configurations section of `integration.md`.

Out of scope: **tote mapping (MS Map)** is not covered. Mention it only as a pointer.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Setting up or adjusting the MatrixScan Count counting flow** (e.g. "add MatrixScan Count to my app", "count barcodes in bulk", "store the scanned barcodes when the list button is tapped", "mute the beep", "use the Dot style", restrict symbologies, show/hide a built-in control, "enable scan preview") → read [references/integration.md](references/integration.md) and follow the instructions there. If the project already has MatrixScan Count wired up, do not re-create the context, mode, view, camera, or lifecycle — locate the existing ones (grep for `BarcodeCountView`, then `BarcodeCount`) and change only what the user asked for. Before writing code, determine whether the project uses UIKit or SwiftUI (check for `import SwiftUI`, an `@main` `App` struct, `SceneDelegate`/`AppDelegate`, `.storyboard`/`.xib` files, etc.) and use the matching Get Started page from the References table below.
- **Customizing the look of the AR highlights** (e.g. "change the highlight color", "use a custom icon/brush per barcode", "use the dot style with custom colors") → read [references/highlights.md](references/highlights.md). This assumes the basic integration is already in place; it covers the Icon (default) vs Dot styles, customizing the **icon** per barcode (`BarcodeCountIcon` built with `ScanditIconBuilder`, via the `iconForRecognizedBarcode` delegate callback / `setIcon`), and customizing the **Dot-style color** via `Brush` (the `recognizedBrush` property, the `brushForRecognizedBarcode` callback, and `setBrush`). (Reacting to taps lives in `integration.md`, not here.)
- **Scanning against a known list of expected barcodes** (e.g. "scan against a manifest / receiving order", "check scans against an expected list", "show a progress bar of how many were found", "let the user accept or reject items that aren't on the list") → read [references/list-scanning.md](references/list-scanning.md). Covers `BarcodeCountCaptureList` + `TargetBarcode`, `setCaptureList`, the `BarcodeCountCaptureListListener` (correct / wrong / missing / accepted / rejected barcodes), `disableModeWhenCaptureListCompleted`, the progress bar, and the not-in-list accept/reject action.
- **Advanced counting configurations** — **filtering** (count only some of the barcodes in the scene: `BarcodeFilterSettings` + `excludedSymbologies` / `excludedCodesRegex`), the **hardware trigger** (react to the volume button: `barcodeCountView.hardwareTriggerEnabled`), **expects-only-unique** (`BarcodeCountSettings.expectsOnlyUniqueBarcodes`), **carrying a previous batch across background** (`barcodeCount.setAdditionalBarcodes(_:)`), and **resetting** (`barcodeCount.reset()`) → read [references/integration.md](references/integration.md) (the Advanced configurations / step 2 / step 7 / Beyond the basics sections).
- **Grouping barcodes into clusters** (e.g. "group the barcodes on a multi-pack/pallet", "enable clustering", "group the codes that are on the same label", "let the user group scanned codes", "color or read the clusters") → read [references/clustering.md](references/clustering.md). Covers `BarcodeCountSettings.clusteringMode` (`.disabled` / `.manual` / `.auto` / `.autoWithManualCorrection`), `automaticClusteringMethod` (`.vicinity` / `.label` / `.outline`) and `expectedNumberOfBarcodesPerCluster`, reading `session.recognizedClusters` (`Cluster.barcodes` / `expectationStatus`), programmatic editing via `BarcodeClusterEditor` (`beginClusterEditing` / `formCluster` / `dissolveCluster` / `endEditing`), the `brushForCluster` / `didTap` (cluster) view-delegate callbacks, and how clustering behaves under scan preview.
- **Status mode** (e.g. "annotate each counted barcode with a status", "mark items as expired / low stock", "show a status icon per barcode the user can review") → read [references/status-mode.md](references/status-mode.md). Covers implementing `BarcodeCountStatusProvider` and registering it with `barcodeCountView.setStatusProvider(_:)`, the `statusRequested(for:callback:)` flow building per-barcode `BarcodeCountStatusItem`s (the icon-based initializer), the `BarcodeCountStatusSuccessResult` / error / abort results delivered via `callback.onStatusReady(_:)`, and `shouldShowStatusModeButton` / `shouldShowStatusIconsOnScan`.
- **Group scanning** (e.g. "let the user split the count into groups / per pallet", "add Next Group / Redo controls", "enable group scanning") → read [references/group-scanning.md](references/group-scanning.md). Covers `BarcodeCountSettings.groupScanningEnabled` (adds the Next Group / Redo controls), the fact that results still come back as a flat list via the normal `BarcodeCountListener` (no grouped-result callback), and customizing the control labels via `setNextGroupButtonText` / `setRedoButtonText`.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or view modifiers. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures can vary (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## References

Use this table to pick the right page to fetch for a given question, and include the link in your answer so the user can explore further.

| Topic | Resource |
|---|---|
| UIKit integration | [Get Started (UIKit)](https://docs.scandit.com/sdks/ios/matrixscan-count/get-started/) · [Sample](https://github.com/Scandit/datacapture-ios-samples/tree/master/03_Advanced_Batch_Scanning_Samples/02_Counting_and_Receiving/MatrixScanCountSimpleSample) |
| SwiftUI integration | [Get Started (SwiftUI)](https://docs.scandit.com/sdks/ios/matrixscan-count/get-started-with-swift-ui/) |
| Advanced (capture list, status mode, brushes, toolbar, filtering, clustering) | [Advanced Configurations](https://docs.scandit.com/sdks/ios/matrixscan-count/advanced/) |
| Overview | [MatrixScan Count Intro](https://docs.scandit.com/sdks/ios/matrixscan-count/intro/) |
| Full API reference | [Barcode (MatrixScan Count) API](https://docs.scandit.com/data-capture-sdk/ios/barcode-capture/api.html) |
