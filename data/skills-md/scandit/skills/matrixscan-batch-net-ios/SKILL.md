---
name: matrixscan-batch-net-ios
description: MatrixScan Batch (MatrixScan, BarcodeBatch, legacy BarcodeTracking) in .NET for iOS projects (`net*-ios` TFM, `Scandit.DataCapture.Barcode` NuGet, non-MAUI — MAUI apps use matrixscan-batch-net-maui) — tracking and scanning multiple barcodes at once. Use for integration, settings and symbologies, listeners/events, basic/advanced overlay customization, camera lifecycle, SDK version migration, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Batch .NET for iOS Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeBatch API changes between major SDK versions — the class itself was renamed from `BarcodeTracking` to `BarcodeBatch` at v7.0, overlay factories evolved, and the .NET binding deviates from the native Swift API in several places (`Create` factories instead of `init(context:settings:)`, `Enabled` instead of `isEnabled`, PascalCase symbology names, `DispatchQueue.MainQueue.DispatchAsync` for UI dispatch, etc.).

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

.NET-iOS-specific gotchas worth flagging:

- This skill targets the **non-MAUI** .NET for iOS workload (project `<TargetFramework>net10.0-ios</TargetFramework>`, no `<UseMaui>` flag). For MAUI apps, use the `matrixscan-batch-net-maui` skill instead (planned).
- **`BarcodeBatch.Create(dataCaptureContext, settings)` is the .NET factory** — not `new BarcodeBatch(...)` (the public constructor is `private`) and not `BarcodeBatch.ForDataCaptureContext(...)` (that name appears in the Swift / docs API but the C# binding is `Create`). When the context is non-null, the factory attaches the mode to the context automatically.
- **`BarcodeBatchSettings.Create()` is a factory** — also `private` constructor. Writing `new BarcodeBatchSettings()` is a compile error.
- **`BarcodeBatchBasicOverlay.Create(...)` and `BarcodeBatchAdvancedOverlay.Create(...)` are factories**, each with multiple overloads. When passed a non-null `DataCaptureView`, both auto-add the overlay to the view — no separate `AddOverlay` call is needed.
- **`BarcodeBatch.RecommendedCameraSettings` is a static property**, not a method. The canonical pattern (mirroring the official .NET iOS sample) is `camera = Camera.GetDefaultCamera(); camera.ApplySettingsAsync(BarcodeBatch.RecommendedCameraSettings);`. The Swift form `createRecommendedCameraSettings()` does **not** exist in the .NET binding.
- Camera setup is **manual**, mirroring BarcodeCapture on .NET iOS, **in this order**: `Camera.GetDefaultCamera()` → `dataCaptureContext.SetFrameSourceAsync(camera)` → `camera.ApplySettingsAsync(BarcodeBatch.RecommendedCameraSettings)`. Bind the camera to the context **before** applying settings (matches the official `MatrixScanSimpleSample` order). The .NET binding is `SetFrameSourceAsync` — not the synchronous Swift `setFrameSource(_:completionHandler:)`.
- **`DataCaptureView.Create(dataCaptureContext, frame)` takes a `CGRect`** as the second argument on iOS — different from the Android `Create(dataCaptureContext)` overload. The canonical call site is `DataCaptureView.Create(dataCaptureContext, this.View!.Bounds)`. Set `AutoresizingMask = UIViewAutoresizing.FlexibleHeight | UIViewAutoresizing.FlexibleWidth` and add it with `this.View.AddSubview(dataCaptureView)` followed by `this.View.SendSubviewToBack(dataCaptureView)`.
- **View-controller constructor depends on how the VC is instantiated.** If the VC is inflated by a storyboard / XIB (typical when the project has a `Main.storyboard` with `UIMainStoryboardFile` set in `Info.plist`), keep the `public MyViewController(IntPtr handle) : base(handle) { }` constructor — the runtime calls it with a real native handle. **For programmatically-instantiated VCs** (no `Main.storyboard`, root view controller set from `SceneDelegate.WillConnect` or `AppDelegate`), declare a parameterless `public MyViewController() : base() { }` constructor and instantiate via `new MyViewController()`. **Do not pass `IntPtr.Zero` to the `(IntPtr)` ctor** — that leaves the native peer uninitialized and `ViewDidLoad` may never fire, which manifests as a black screen with no camera preview and no scans.
- **`IBarcodeBatchListener.OnSessionUpdated(BarcodeBatch, BarcodeBatchSession, IFrameData)` runs on a background recognition queue** — not the main queue. Dispatch any UI work via `DispatchQueue.MainQueue.DispatchAsync(() => { … })`. The third parameter is `IFrameData` (the .NET binding), not `FrameData` (Swift).
- **Always call `frameData.Dispose()` at the end of every `OnSessionUpdated` callback** (including any early-return path). The official iOS sample explicitly disposes the frame to avoid a "frozen, non-responsive, or severely stuttering" video feed. This is not optional on iOS, and is a difference from the Android skill where the disposal is not required.
- The .NET binding also exposes the **event API** on `BarcodeBatch`: `barcodeBatch.SessionUpdated += handler` (`EventHandler<BarcodeBatchEventArgs>`). Use either the listener interface OR the event — not both for the same handler. The event-handler body must still call `args.FrameData.Dispose()`. There is **no** `BarcodeScanned` event on `BarcodeBatch` (batch is tracking, not single-scan).
- **Do not hold references to `BarcodeBatchSession` or its collections outside `OnSessionUpdated`.** The session is only safe to access within that callback — copy `AddedTrackedBarcodes` / `UpdatedTrackedBarcodes` / `TrackedBarcodes` data first, then dispatch.
- `BarcodeBatchSession` properties: `AddedTrackedBarcodes` (`IList<TrackedBarcode>`), `UpdatedTrackedBarcodes` (`IList<TrackedBarcode>`), `RemovedTrackedBarcodes` (`IList<int>` — tracking IDs only, not `TrackedBarcode`), `TrackedBarcodes` (`IDictionary<int, TrackedBarcode>`), `FrameSequenceId` (`long`), `Reset()`. Note: `Reset()` lives on the **Session** in the .NET binding (there is no `BarcodeBatch.Reset()` like the Android Kotlin API has).
- `TrackedBarcode` properties: `Barcode`, `Identifier` (`int`), `Location` (`Quadrilateral`), plus `GetAnchorPosition(Anchor)`. The tracking identifier is reused after a barcode leaves the frame.
- The capture mode's enabled property is `barcodeBatch.Enabled` (not `IsEnabled` and not Swift's `isEnabled`). `IDataCaptureMode` exposes `Enabled` in the .NET binding.
- **`BarcodeBatchBasicOverlayStyle` is C# PascalCase**: `Frame` (default) and `Dot`. Not `frame` / `dot` (Swift) and not `FRAME` / `DOT` (Kotlin).
- **Per-barcode brush customization** (`IBarcodeBatchBasicOverlayListener.BrushForTrackedBarcode` and `BarcodeBatchBasicOverlay.SetBrushForTrackedBarcode`) requires the **MatrixScan AR add-on** license. A uniform default brush via `overlay.Brush = …` (no listener) does not require the add-on.
- **`BarcodeBatchAdvancedOverlay`** (anchoring custom `UIView`s to tracked barcodes) requires the **MatrixScan AR add-on** license. `IBarcodeBatchAdvancedOverlayListener` has `ViewForTrackedBarcode(overlay, trackedBarcode) → UIView?`, `AnchorForTrackedBarcode(...)`, `OffsetForTrackedBarcode(...)` — all three are called on the main thread. The return type is `UIView?` (the .NET binding maps `View` to `UIKit.UIView` on iOS via a global `using View = UIKit.UIView;`).
- `BarcodeBatchLicenseInfo` (read via `barcodeBatch.BarcodeBatchLicenseInfo`) is `dotnet.ios=8.4+` only. Before 8.4 the property does not exist — gate any usage on the installed SDK version. The value is available once `IDataCaptureContextListener.OnModeAdded` has been called.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Upce`, `Symbology.Code39`, `Symbology.Code128`, `Symbology.InterleavedTwoOfFive`, `Symbology.Qr`, `Symbology.DataMatrix`. They are **not** Swift's `.ean13UPCA` / `.code128` / `.qr` style.
- The NuGet packages are `Scandit.DataCapture.Core` and `Scandit.DataCapture.Barcode`. No separate `*.Maui` packages here — those are only for MAUI projects. **Do not guess the version from training data** — fetch the latest stable from `https://www.nuget.org/packages/Scandit.DataCapture.Barcode/` via `WebFetch` before pinning. Inventing a non-existent version causes `dotnet restore` to fail with `Unable to find package Scandit.DataCapture.Core with version (>= …)`. See [references/integration.md](references/integration.md) Step 0 for the full procedure.
- **iOS `SupportedOSPlatformVersion` must be ≥ `15.0`.** Set it in the `.csproj`. The official `MatrixScanSimpleSample` `Info.plist` `MinimumOSVersion` is `15.0` and the project's `<SupportedOSPlatformVersion>` matches.
- **The required `Info.plist` key is `NSCameraUsageDescription`** (`Privacy - Camera Usage Description`). Without it the app crashes on first camera access. iOS prompts the user automatically the first time the camera opens; there is **no separate runtime-request API** to call (no Android-style `RequestPermissions`).
- **SDK 8.0+ requires explicit initialization.** Call `ScanditCaptureCore.Initialize()` + `ScanditBarcodeCapture.Initialize()` in `AppDelegate.FinishedLaunching` before any Scandit code runs (typically before creating the window / root view controller). Without this the SDK's DI container has no registrations and the first `BarcodeBatch.Create(...)` / `DataCaptureView.Create(...)` call crashes at launch. **Not required on 6.x / 7.x.** See [references/integration.md](references/integration.md) Step 0 / Prerequisites for the full `AppDelegate` template.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan Batch from scratch, configuring settings, handling tracked barcodes, customizing overlays, anchoring custom UIViews, managing the camera lifecycle, or diagnosing a frozen/stuttering preview** (e.g. "add MatrixScan Batch to my .NET iOS app", "scan all barcodes in view at once in C#", "highlight tracked barcodes in green", "anchor a price label to each tracked barcode", "show me how to set up BarcodeBatch in net-ios", "my preview is stuttering after I integrated BarcodeBatch") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing MatrixScan Batch integration** (e.g. "upgrade from v6 to v7", "rename BarcodeTracking to BarcodeBatch", "bump the Scandit .NET SDK to v8", "what changed between SDK versions for BarcodeBatch") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Replacing a third-party multi-barcode scanner with MatrixScan Batch** (e.g. "replace my AVFoundation multi-barcode loop with MatrixScan Batch", "migrate from ZXing.Net.Mobile continuous scanning to Scandit", "switch from AVCaptureMetadataOutput to BarcodeBatch") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or property names. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures can vary (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Get Started | [Get Started (.NET for iOS)](https://docs.scandit.com/sdks/net/ios/matrixscan/get-started/) |
| AR overlays (per-barcode brushes, anchored UIViews) | [Adding AR Overlays](https://docs.scandit.com/sdks/net/ios/matrixscan/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/net/ios/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/ios/migrate-7-to-8/) |
| Full API reference | [BarcodeBatch API (.NET iOS)](https://docs.scandit.com/data-capture-sdk/dotnet.ios/barcode-capture/api.html) |

## API surface this skill covers

All classes documented with `:available: dotnet.ios` in the official RST docs (`docs/source/barcode-capture/api/barcode-batch*.rst` and `api/ui/barcode-batch-*-overlay*.rst`) are addressed in [references/integration.md](references/integration.md):

- `BarcodeBatch` — `Create(DataCaptureContext?, BarcodeBatchSettings)`, `Enabled`, `ApplySettingsAsync(settings)`, `AddListener(IBarcodeBatchListener)` / `RemoveListener(IBarcodeBatchListener)`, event `SessionUpdated` (`EventHandler<BarcodeBatchEventArgs>`), static `RecommendedCameraSettings` (property, not method), `Context`, `BarcodeBatchLicenseInfo` (8.4+), `Dispose`.
- `BarcodeBatchSettings` — `Create()`, `EnableSymbology(Symbology, bool)`, `EnableSymbologies(ICollection<Symbology>)`, `GetSymbologySettings(Symbology)`, `EnabledSymbologies` (get), `SetProperty` / `GetProperty<T>` / `TryGetProperty<T>`.
- `BarcodeBatchSession` — `AddedTrackedBarcodes`, `UpdatedTrackedBarcodes`, `RemovedTrackedBarcodes` (`IList<int>` of tracking IDs), `TrackedBarcodes` (`IDictionary<int, TrackedBarcode>`), `FrameSequenceId`, `Reset()`.
- `BarcodeBatchEventArgs` — `BarcodeBatch`, `Session`, `FrameData`.
- `IBarcodeBatchListener` — `OnObservationStarted(BarcodeBatch)`, `OnObservationStopped(BarcodeBatch)`, `OnSessionUpdated(BarcodeBatch, BarcodeBatchSession, IFrameData)`.
- `BarcodeBatchLicenseInfo` (8.4+) — `LicensedSymbologies`.
- `TrackedBarcode` — `Barcode`, `Identifier`, `Location` (`Quadrilateral`), `GetAnchorPosition(Anchor)`.
- `BarcodeBatchBasicOverlay` — `Create(barcodeBatch, view, style)`, `Create(barcodeBatch, style)`, `Create(barcodeBatch, view)`, `Create(barcodeBatch)`, `Listener` (`IBarcodeBatchBasicOverlayListener?`), `Brush` (uniform default brush), static `DefaultBrushForStyle(style)`, `Style` (read-only), `ShouldShowScanAreaGuides`, `SetBrushForTrackedBarcode(trackedBarcode, brush)`, `ClearTrackedBarcodeBrushes()`, `Dispose`.
- `BarcodeBatchBasicOverlayStyle` enum — `Frame`, `Dot`.
- `IBarcodeBatchBasicOverlayListener` — `BrushForTrackedBarcode(overlay, trackedBarcode)`, `OnTrackedBarcodeTapped(overlay, trackedBarcode)`. **Requires MatrixScan AR add-on.**
- `BarcodeBatchAdvancedOverlay` — `Create(barcodeBatch, view)`, `Create(barcodeBatch)`, `Listener` (`IBarcodeBatchAdvancedOverlayListener?`), `SetViewForTrackedBarcode(trackedBarcode, UIView?)`, `SetAnchorForTrackedBarcode(trackedBarcode, anchor)`, `SetOffsetForTrackedBarcode(trackedBarcode, offset)`, `ClearTrackedBarcodeViews()`, `ShouldShowScanAreaGuides`, `Dispose`. **Requires MatrixScan AR add-on.**
- `IBarcodeBatchAdvancedOverlayListener` — `ViewForTrackedBarcode(overlay, trackedBarcode) → UIView?`, `AnchorForTrackedBarcode(overlay, trackedBarcode)`, `OffsetForTrackedBarcode(overlay, trackedBarcode)`. **Requires MatrixScan AR add-on.**
