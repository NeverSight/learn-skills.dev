---
name: matrixscan-count-android
description: MatrixScan Count (BarcodeCount) in native Android projects (Kotlin/Java, `com.scandit.datacapture:barcode`) — counting and receiving barcodes in bulk with the BarcodeCountView UI in an Activity or Fragment, scanning against an expected/receiving list, clustering, status mode, explicitly managed camera. Use for integration, settings and symbology configuration, result handling, UI customization, or troubleshooting counting workflows.
license: Apache-2.0
metadata:
  author: scandit
  version: "0.1.1"
---

# MatrixScan Count Android Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The MatrixScan Count API has
evolved across SDK versions — classes, properties, and factory methods may have been renamed or
restructured, and the Android API differs from the iOS one in concrete ways (factory methods, listener
names, view construction).

**Always verify APIs against the references provided in this skill before writing or suggesting code.**
Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in
the provided references, fetch the relevant documentation page before responding.

The single most common mistake is assuming the view owns the camera: in MatrixScan Count the
**`BarcodeCountView` does NOT own or manage the camera** — you create and drive the camera explicitly
(`Camera.getDefaultCamera(...)`, apply `BarcodeCount.createRecommendedCameraSettings()`,
`dataCaptureContext.setFrameSource(...)`, and switch its state across `onResume`/`onPause`). See
[references/integration.md](references/integration.md) (Camera section). (This is unlike `BarcodeArView` in MatrixScan AR, which
*does* manage the camera internally — don't carry that habit over.)

Android-specific gotchas worth flagging:

- `BarcodeCount.forDataCaptureContext(dataCaptureContext, settings)` is the **static factory** that
  creates the mode — **not** a `BarcodeCount(...)` constructor and **not** `forContext(...)`.
- `BarcodeCountView` is created with the **static `BarcodeCountView.newInstance(context, dataCaptureContext, barcodeCount)` factory** — not a constructor. There is an overload taking a `BarcodeCountViewStyle` (`ICON` / `DOT`) and one taking a `DataCaptureView`. The view does **not** add itself to the hierarchy — call `addView(...)`.
- Recommended camera settings come from the **static** `BarcodeCount.createRecommendedCameraSettings()` — not a property like iOS's `recommendedCameraSettings`.
- The result-collecting callback is `BarcodeCountListener.onScan(barcodeCount, session, data)` (the `FrameData` parameter is named `data`). It is called on an **internal recognition thread** — dispatch to the main thread with `runOnUiThread {}` before touching UI/app state. `onSessionUpdated` / `onObservationStarted` / `onObservationStopped` are optional default methods.
- The List/Exit/SingleScan buttons are delivered by **`BarcodeCountViewUiListener`** (`barcodeCountView.uiListener`); per-barcode brushes/icons and barcode-tap callbacks are delivered by the **separate `BarcodeCountViewListener`** (`barcodeCountView.listener`). Prefer the `onListButtonTapped(view, snapshot)` / `onExitButtonTapped(view, snapshot)` overloads — the `snapshot` is a nullable `BarcodeCountSessionSnapshot?` (its `recognizedBarcodes` etc. give you the count at tap time; access with `snapshot?.…`). The single-arg `(view)` forms are **deprecated**.
- Symbology names are uppercase with underscores: `Symbology.EAN13_UPCA`, `Symbology.QR` (not `QR_CODE`), `Symbology.CODE128`. Enable one with `settings.setSymbologyEnabled(symbology, true)` or a set with `settings.enableSymbologies(set)`. All symbologies are disabled by default.
- Highlight appearance is customized per style: on the default **Icon style** customize the **icon** (`iconForRecognizedBarcode` returning a `BarcodeCountIcon`, or `setIconForRecognizedBarcode`); on the **Dot style** customize the **`Brush`** (`recognizedBrush` / `brushForRecognizedBarcode`). `Brush(fillColor, strokeColor, strokeWidth)` takes **Android color ints** and a `Float` width. A `BarcodeCountIcon` wraps a `ScanditIcon` built with `ScanditIconBuilder` (in `core.ui.icon`).
- The hardware trigger takes a **key code**: `barcodeCountView.enableHardwareTrigger(keyCode)` (e.g. `KeyEvent.KEYCODE_VOLUME_DOWN`) — not a boolean.
- `BarcodeCountSettings.filterSettings` is **read-only** — mutate the returned `BarcodeFilterSettings` in place; don't assign a new one.
- `barcodeCount.beginClusterEditing()` returns a **nullable** `BarcodeClusterEditor?`.
- The button-text setters are **methods, not properties**: `barcodeCountView.setNextGroupButtonText("…")`, `setRedoButtonText("…")`, `setTextForClusteringGestureHint("…")`, `setTextForTapToUncountHint("…")` — call them, don't assign. (Booleans/enums like `shouldShowTorchControl`, `groupScanningEnabled`, `expectedNumberOfBarcodesPerCluster` ARE Kotlin properties.)
- Status mode uses the fixed **`BarcodeCountStatus`** enum (`EXPIRED`, `FRAGILE`, `LOW_STOCK`, …) via `BarcodeCountStatusItem.create(trackedBarcode, status)`.
- Request the `CAMERA` permission at runtime before scanning starts; the manifest declaration alone is not sufficient. The SDK requires `minSdk` 24+.
- Import classes from the exact packages in the **Package paths** table in [references/integration.md](references/integration.md) — several are easy to misplace (`TrackedBarcode` is under `barcode.batch.data`, `BarcodeCountFeedback` under `barcode.count.feedback`, `Feedback` under `core.common.feedback`). Reading a barcode's payload is `trackedBarcode.barcode.data` — `TrackedBarcode` itself has no `data`.

**Scan preview** (the iOS `scanPreviewEnabled` flow) is not available on Android — `scanPreviewEnabled`
does not exist on `BarcodeCountSettings`; don't invent it, and say so if asked. Group scanning,
per-barcode highlight icons, and cluster expectation status are all supported and covered in the
references.

## Scope

This skill is scoped to the **MatrixScan Count counting workflow**: `DataCaptureContext`, the
`BarcodeCount` mode, `BarcodeCountSettings` (symbologies, per-symbology tuning,
`expectsOnlyUniqueBarcodes`, clustering, filtering), `BarcodeCountView` (the built-in AR counting UI with
Icon / Dot styles), the explicitly-managed camera frame source and lifecycle, `BarcodeCountListener` for
collecting scanned barcodes, the List / Exit / Single-Scan button callbacks (`BarcodeCountViewUiListener`),
feedback, control visibility, customizing the AR highlights (per-barcode **icon** on the Icon style or
**brush** on the Dot style), status mode, clustering (including the expected-count status), group
scanning, and scanning against an expected/receiving list (`BarcodeCountCaptureList` + `TargetBarcode`).

Also covered: **filtering** (count only some of the barcodes in the scene), the **hardware trigger**, and
carrying a previous batch across a background cycle (`setAdditionalBarcodes`) — see the Advanced
configurations section of `integration.md`.

Out of scope: **tote mapping (MS Map)** is not covered. Mention it only as a pointer.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Setting up or adjusting the MatrixScan Count counting flow** (e.g. "add MatrixScan Count to my app", "count barcodes in bulk", "store the scanned barcodes when the list button is tapped", "mute the beep", "use the Dot style", restrict symbologies, show/hide a built-in control, filtering, hardware trigger) → read [references/integration.md](references/integration.md) and follow the instructions there. If the project already has MatrixScan Count wired up, do not re-create the context, mode, view, camera, or lifecycle — locate the existing ones (grep for `BarcodeCountView`, then `BarcodeCount`) and change only what the user asked for.
- **Customizing the look of the AR highlights** (e.g. "change the highlight color", "use a custom icon per barcode", "color each barcode by its data", "use the dot style with custom colors") → read [references/highlights.md](references/highlights.md). Covers the Icon (default) vs Dot styles: on the Icon style customize the **icon** (`BarcodeCountIcon` built with `ScanditIconBuilder`, via `iconForRecognizedBarcode` / `setIconForRecognizedBarcode`); on the Dot style customize the **`Brush`** (`recognizedBrush`, `brushForRecognizedBarcode`, `setBrushForRecognizedBarcode`). (Reacting to taps lives in `integration.md`.)
- **Scanning against a known list of expected barcodes** (e.g. "scan against a manifest / receiving order", "check scans against an expected list", "show a progress bar of how many were found", "let the user accept or reject items that aren't on the list") → read [references/list-scanning.md](references/list-scanning.md). Covers `BarcodeCountCaptureList.create` + `TargetBarcode.create`, `setBarcodeCountCaptureList`, the `BarcodeCountCaptureListListener` (correct / wrong / missing / accepted / rejected barcodes), `disableModeWhenCaptureListCompleted`, the progress bar, and the not-in-list accept/reject action.
- **Status mode** (e.g. "annotate each counted barcode with a status", "mark items as expired / low stock", "show a status icon per barcode the user can review") → read [references/status-mode.md](references/status-mode.md). Covers implementing `BarcodeCountStatusProvider` and registering it with `barcodeCountView.setStatusProvider(...)`, the `onStatusRequested(barcodes, callback)` flow building per-barcode `BarcodeCountStatusItem`s from the `BarcodeCountStatus` enum, the success / error / abort result types delivered via `callback.onStatusReady(...)`, and `shouldShowStatusModeButton` / `shouldShowStatusIconsOnScan`.
- **Grouping barcodes into clusters** (e.g. "group the barcodes on a multi-pack/pallet", "enable clustering", "let the user group scanned codes", "flag clusters whose count is off") → read [references/clustering.md](references/clustering.md). Covers `BarcodeCountSettings.clusteringMode` (`DISABLED` / `MANUAL` / `AUTO` / `AUTO_WITH_MANUAL_CORRECTION`), the expected-count check (`expectedNumberOfBarcodesPerCluster` + `Cluster.expectationStatus` / `ClusterExpectationStatus`), reading `session.recognizedClusters` (`Cluster.barcodes`), programmatic editing via `beginClusterEditing()` (`formCluster` / `dissolveCluster` / `endEditing`), and the `brushForCluster` / `onClusterTapped` listener callbacks.
- **Group scanning** (e.g. "let the user split the count into groups / one per pallet", "add Next Group / Redo controls", "enable group scanning") → read [references/group-scanning.md](references/group-scanning.md). Covers `BarcodeCountSettings.groupScanningEnabled` (adds the Next Group / Redo controls), the fact that results still come back as a flat list via the normal `BarcodeCountListener` (no grouped-result callback), and customizing the control labels via `setNextGroupButtonText` / `setRedoButtonText`.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess
method signatures, parameters, or property names. If unsure whether an API exists or how it is called —
or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user
to check the docs themselves. After answering, always include the relevant link so the user can explore
further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link
   directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below),
   extract the actual link from it, and follow that.

URL structures can vary (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## References

Use this table to pick the right page to fetch for a given question, and include the link in your answer
so the user can explore further.

| Topic | Resource |
|---|---|
| Get Started | [Get Started (Android)](https://docs.scandit.com/sdks/android/matrixscan-count/get-started/) · [Sample](https://github.com/Scandit/datacapture-android-samples/tree/master/03_Advanced_Batch_Scanning_Samples/02_Counting_and_Receiving/MatrixScanCountSimpleSample) |
| Advanced (capture list, status mode, brushes, filtering, clustering) | [Advanced Configurations](https://docs.scandit.com/sdks/android/matrixscan-count/advanced/) |
| Overview | [MatrixScan Count Intro](https://docs.scandit.com/sdks/android/matrixscan-count/intro/) |
| Full API reference | [Barcode (MatrixScan Count) API](https://docs.scandit.com/data-capture-sdk/android/barcode-capture/api.html) |
