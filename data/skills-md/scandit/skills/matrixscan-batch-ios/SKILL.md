---
name: matrixscan-batch-ios
description: MatrixScan Batch (MatrixScan, BarcodeBatch, legacy BarcodeTracking) — tracking and scanning multiple barcodes at once in iOS (Swift, UIKit/SwiftUI) projects. Use for integration, settings and symbologies, tracked-barcode handling, basic/advanced overlay customization, lifecycle, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Batch iOS Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeBatch API changes between major SDK versions — initializer signatures, overlay constructors, and delegate method names have all evolved (e.g. `BarcodeTracking` → `BarcodeBatch`).

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

iOS-specific gotchas worth flagging:

- `BarcodeBatch(context: context, settings: settings)` is a **direct convenience initializer** — not a factory method like Android's `BarcodeBatch.forDataCaptureContext(...)`. Passing a non-nil context auto-attaches the mode to the context.
- Camera setup is **manual**: get `Camera.default`, call `context.setFrameSource(camera, completionHandler: nil)`, then `camera?.apply(BarcodeBatch.recommendedCameraSettings, completionHandler: nil)`. Drive the camera from `viewWillAppear` / `viewWillDisappear`.
- `BarcodeBatchListener.barcodeBatch(_:didUpdate:frameData:)` is called on a **background queue** — not the main thread. Dispatch UI work via `DispatchQueue.main.async {}`.
- **Do not hold references** to `BarcodeBatchSession.trackedBarcodes`, `addedTrackedBarcodes`, `updatedTrackedBarcodes`, or `removedTrackedBarcodes` outside the callback — copy the data before the callback returns.
- `BarcodeBatchBasicOverlay(barcodeBatch:view:)` and `BarcodeBatchAdvancedOverlay(barcodeBatch:view:)` **auto-add the overlay** to the `DataCaptureView` — no separate `addOverlay` call needed.
- **`DataCaptureView` must be `addSubview`'d manually** — unlike `BarcodeArView`, `DataCaptureView` does not auto-attach to a parent view.
- **Per-barcode brush customization** (`barcodeBatchBasicOverlay(_:brushFor:)`, `setBrush(_:for:)`) requires the **MatrixScan AR add-on** license. A uniform default brush (no delegate) does not.
- **BarcodeBatchAdvancedOverlay** requires the **MatrixScan AR add-on** license.
- **No built-in feedback** — `BarcodeBatch` never plays a sound or vibrates on its own (unlike `BarcodeCapture` / `SparkScan`). Emit feedback manually with `Feedback.default.emit()` from inside the listener callback (dispatched to the main thread), gated on `session.addedTrackedBarcodes` so it doesn't beep every frame.
- `session.removedTrackedBarcodes` is an **`[Int]` of tracking identifiers** (barcodes that left the frame) — not `TrackedBarcode` objects. `addedTrackedBarcodes` / `updatedTrackedBarcodes` are `[TrackedBarcode]`.
- iOS symbology cases are **camelCase**: `.ean13UPCA`, `.code128`, `.qr` — not `EAN13_UPCA` / `CODE128` / `QR` like Android.
- iOS delegate methods use Swift naming: `barcodeBatchBasicOverlay(_:didTap:)` (not Android's `onTrackedBarcodeTapped`), `barcodeBatchAdvancedOverlay(_:viewFor:)` (not `viewForTrackedBarcode`).
- `BarcodeBatchAdvancedOverlayDelegate` uses `UIView` — not Android `View` or SwiftUI views.
- SwiftUI: `DataCaptureView` is a `UIView` and cannot be dropped into SwiftUI directly. Wrap a UIKit view controller in a `UIViewControllerRepresentable` and keep all BarcodeBatch APIs inside that view controller.
- Cleanup: `BarcodeBatchListener` is held as a **weak** reference, so a missed `removeListener` won't leak — but call `barcodeBatch.removeListener(self)` in `deinit` to make the lifecycle explicit. When using the shared singleton (`DataCaptureContext.shared`), modes stay attached for the app's lifetime — you don't need to call `removeCurrentMode()` or `dispose()`. Those methods do exist on `DataCaptureContext` if you want to tear down explicitly.
- `DataCaptureContext` exposes two valid initializers: `DataCaptureContext.initialize(licenseKey:)` + `.shared` (added 7.1.0/7.6.0 — the modern singleton pattern, and what this skill uses) and the older `DataCaptureContext(licenseKey:)` convenience init (still non-deprecated, and what the UIKit Get Started page on docs.scandit.com still shows). Prefer the singleton form.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan Batch from scratch, configuring settings, handling tracked barcodes, customizing overlays, adding feedback, or managing lifecycle** → read [references/integration.md](references/integration.md) and follow the instructions there. Before writing code, determine whether the project uses UIKit or SwiftUI (check for `import SwiftUI`, an `@main` `App` struct, `SceneDelegate`/`AppDelegate`, `.storyboard`/`.xib` files, etc.) and use the matching Get Started page from the References table below. If the project already has BarcodeBatch wired up, do not re-create the context, mode, view, or lifecycle — locate the existing ones (grep for `BarcodeBatch`, then `DataCaptureView`) and change only what the user asked for.
- **Upgrading the Scandit SDK version** (e.g. v6→v7, v7→v8, or "upgrade to the latest") → read [references/migration.md](references/migration.md). The headline v6→v7 change for MatrixScan Batch is the `BarcodeTracking` → `BarcodeBatch` rename; the guide also covers the context/camera modernization. Detect the installed version from `Package.resolved` / `Podfile.lock` before asking the user.
- **Replacing a different barcode scanner with MatrixScan Batch** (AVFoundation `AVCaptureMetadataOutput`, VisionKit `DataScannerViewController`, or another third-party multi-barcode SDK) → read [references/third-party-migration.md](references/third-party-migration.md), then follow [references/integration.md](references/integration.md) for the BarcodeBatch integration.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or property names. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures can vary (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## References

| Topic | Resource |
|---|---|
| UIKit integration | [Get Started (UIKit)](https://docs.scandit.com/sdks/ios/matrixscan/get-started/) · [Sample](https://github.com/Scandit/datacapture-ios-samples/tree/master/03_Advanced_Batch_Scanning_Samples/01_Batch_Scanning_and_AR_Info_Lookup/MatrixScanBubblesSample) |
| SwiftUI integration | [Get Started (SwiftUI)](https://docs.scandit.com/sdks/ios/matrixscan/get-started-with-swift-ui/) |
| AR overlays (BasicOverlay brushes, AdvancedOverlay views) | [Adding AR Overlays](https://docs.scandit.com/sdks/ios/matrixscan/advanced/) |
| Version migration (v6→v7→v8) | [Migrate 6→7](https://docs.scandit.com/sdks/ios/migrate-6-to-7/) · [Migrate 7→8](https://docs.scandit.com/sdks/ios/migrate-7-to-8/) |
| Full API reference | [BarcodeBatch API](https://docs.scandit.com/data-capture-sdk/ios/barcode-capture/api.html) |
