---
name: matrixscan-batch-net-maui
description: MatrixScan Batch (MatrixScan, BarcodeBatch, legacy BarcodeTracking) in .NET MAUI projects (`Scandit.DataCapture.Barcode.Maui` NuGet, XAML DataCaptureView) — tracking and scanning multiple barcodes at once with basic/advanced overlays. For non-MAUI .NET projects use matrixscan-batch-net-android or matrixscan-batch-net-ios. Use for integration, settings, listeners/events, overlay customization, lifecycle, SDK version migration, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Batch .NET MAUI Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeBatch API changes significantly between major SDK versions — the class itself was renamed from `BarcodeTracking` to `BarcodeBatch` at v7.0, the namespace moved from `Scandit.DataCapture.Barcode.Tracking.*` to `Scandit.DataCapture.Barcode.Batch.*`, and the .NET MAUI binding adds platform-specific lifecycle, handler, and native-view-bridging concerns on top of the regular .NET API. Patterns from the standalone `matrixscan-batch-net-android` / `matrixscan-batch-net-ios` skills do not always apply unchanged.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

MAUI-specific gotchas worth flagging:

- This skill targets MAUI apps with `<UseMaui>true</UseMaui>`. For non-MAUI .NET projects, use `matrixscan-batch-net-android` (for `net*-android`) or `matrixscan-batch-net-ios` (for `net*-ios`) instead.
- **Fetch the SDK version from NuGet before editing the `.csproj`.** WebFetch `https://www.nuget.org/packages/Scandit.DataCapture.Barcode.Maui/` and read the latest **stable** version off the page (skip `-beta.*` / `-preview.*` / `-rc.*` suffixes). Do not guess — versions from training data are stale and `dotnet restore` will fail with `NU1103` if the pinned version isn't published. Use the same version for all four packages.
- **Android `SupportedOSPlatformVersion` must be ≥ `24`.** The MAUI template defaults to `21`, which is below Scandit's Android AAR minimum and fails the build with `uses-sdk:minSdkVersion 21 cannot be smaller than version 24 declared in library`. Bump the `.csproj` value to `24.0` (or higher) as part of the integration.
- Required NuGet packages: `Scandit.DataCapture.Core`, `Scandit.DataCapture.Core.Maui`, `Scandit.DataCapture.Barcode`, `Scandit.DataCapture.Barcode.Maui`. All four are needed — Core/Barcode provide the platform bindings, Core.Maui/Barcode.Maui provide the MAUI builder extensions and handlers.
- `MauiProgram.cs` builder chain is **specific** and the order matters:
  ```csharp
  builder
      .UseMauiApp<App>()
      .UseScanditCore(configure => configure.AddDataCaptureView())
      .UseScanditBarcode();
  ```
  `UseScanditBarcode()` takes **no inner configure** — there is no MAUI handler for BarcodeBatch itself, the call exists only to invoke `ScanditBarcodeCapture.Initialize()`. Do **not** write `UseScanditBarcode(configure => configure.AddBarcodeBatchView())` — that method does not exist. BarcodeBatch in MAUI uses the generic `<scandit:DataCaptureView>`, not a dedicated view.
- **Do NOT call `ScanditCaptureCore.Initialize()` / `ScanditBarcodeCapture.Initialize()` in `MainApplication.OnCreate` or `AppDelegate.FinishedLaunching`.** The MAUI builder extensions (`UseScanditCore` / `UseScanditBarcode`) perform this SDK initialization themselves. This is different from the non-MAUI `matrixscan-batch-net-android` / `matrixscan-batch-net-ios` skills, which require manual initialization for SDK 8.0+. In a MAUI app, the `MainApplication` / `AppDelegate` only need to forward to `MauiProgram.CreateMauiApp()` — leave them alone.
- `BarcodeBatch` does **not** have a pre-built MAUI view (unlike `BarcodeArView`, `BarcodeCountView`, `BarcodeFindView`, `BarcodePickView`, `SparkScanView`). The MAUI integration uses the generic `<scandit:DataCaptureView>` from `Scandit.DataCapture.Core.UI.Maui` with `BarcodeBatchBasicOverlay` (and optionally `BarcodeBatchAdvancedOverlay`) added on top.
- XAML namespace for `DataCaptureView` is `xmlns:scandit="clr-namespace:Scandit.DataCapture.Core.UI.Maui;assembly=ScanditCaptureCoreMaui"`. **`DataCaptureContext="{Binding DataCaptureContext}"` is mandatory on the `<scandit:DataCaptureView>` element** — without it the preview renders as a **black/blank camera** at runtime even though the code-behind compiles and the camera is started. Setting `x:Name="dataCaptureView"` is not enough; the bindable property is what wires the context to the preview. The page's `BindingContext` (view model or `this`) must expose a `DataCaptureContext` property of type `Scandit.DataCapture.Core.Capture.DataCaptureContext`.
- The `BarcodeBatchBasicOverlay` must be created **after** the platform handler has been attached. The pattern used in the official sample is:
  ```csharp
  this.dataCaptureView.HandlerChanged += (s, e) =>
  {
      var overlay = BarcodeBatchBasicOverlay.Create(
          this.viewModel.BarcodeBatch,
          BarcodeBatchBasicOverlayStyle.Frame);
      this.dataCaptureView.AddOverlay(overlay);
  };
  ```
  Creating the overlay before `HandlerChanged` fires will fail silently — there is no native view to attach it to yet. The same rule applies to `BarcodeBatchAdvancedOverlay`.
- MAUI page lifecycle: `OnAppearing` → start camera + `barcodeBatch.Enabled = true`; `OnDisappearing` → set `barcodeBatch.Enabled = false` **first**, then stop the camera. The official `MatrixScanSimpleSample` explicitly does the `Enabled = false` before the camera shutdown because in-flight frames can still report tracked-barcode updates during the asynchronous camera-off transition. The sample factors this into a `ResumeAsync` / `SleepAsync` pattern on the view model.
- **`IBarcodeBatchListener.OnSessionUpdated(BarcodeBatch, BarcodeBatchSession, IFrameData)` runs on a background recognition thread** — not the main thread. Dispatch any UI work via `MainThread.BeginInvokeOnMainThread(() => …)` or `MainThread.InvokeOnMainThreadAsync(...)`. The third parameter is `IFrameData` (the .NET binding), not `FrameData` (Swift / Kotlin).
- **Do not hold references to `BarcodeBatchSession` or its collections outside `OnSessionUpdated`.** The session is only safe to access within that callback — copy `AddedTrackedBarcodes` / `UpdatedTrackedBarcodes` / `TrackedBarcodes` data first, then dispatch.
- **Always call `frameData.Dispose()` at the end of every `OnSessionUpdated` callback** (including any early-return path). When the MAUI app is running on iOS (multi-targeted `net*-ios`), failing to dispose causes a "frozen, non-responsive, or severely stuttering" video feed because the recognition pipeline runs out of buffers. On Android the binding manages the frame lifetime, but writing the disposal once (in a `try`/`finally`) is safe everywhere and is the recommendation for portable MAUI code. Note that the official `MatrixScanSimpleSample` omits this in the simple path, relying on `lock`-based access; the recommendation here is to add the `try`/`finally` anyway because MAUI apps almost always multi-target iOS.
- UI dispatch is `MainThread.BeginInvokeOnMainThread(() => …)` or `MainThread.InvokeOnMainThreadAsync(...)` — not `RunOnUiThread` (Android-specific) and not `DispatchQueue.MainQueue.DispatchAsync` (iOS-specific). The dispatch wrapper is platform-agnostic.
- The .NET API uses **PascalCase factories**: `BarcodeBatch.Create(context, settings)`, `BarcodeBatchSettings.Create()`, `BarcodeBatchBasicOverlay.Create(barcodeBatch, style)` / `Create(barcodeBatch)`, `BarcodeBatchAdvancedOverlay.Create(barcodeBatch)`, `DataCaptureContext.ForLicenseKey(key)`, `Camera.GetCamera(CameraPosition.WorldFacing)` or `Camera.GetDefaultCamera()`.
- **`BarcodeBatchBasicOverlayStyle` is C# PascalCase**: `Frame` (default) and `Dot`. Not `FRAME` / `DOT` (Kotlin) and not `frame` / `dot` (Swift).
- The capture mode's enabled property is `barcodeBatch.Enabled` (not `IsEnabled` and not Swift's `isEnabled`).
- `BarcodeBatchSession` properties: `AddedTrackedBarcodes` (`IList<TrackedBarcode>`), `UpdatedTrackedBarcodes` (`IList<TrackedBarcode>`), `RemovedTrackedBarcodes` (`IList<int>` — tracking IDs only, not `TrackedBarcode`), `TrackedBarcodes` (`IDictionary<int, TrackedBarcode>`), `FrameSequenceId` (`long`), `Reset()`. `Reset()` lives on the **Session** in the .NET binding (there is no `BarcodeBatch.Reset()` like the Kotlin API has).
- `TrackedBarcode` properties: `Barcode`, `Identifier` (`int`), `Location` (`Quadrilateral`), plus `GetAnchorPosition(Anchor)`. The tracking identifier is reused after a barcode leaves the frame.
- **`BarcodeBatchAdvancedOverlay`** (anchoring custom views on top of tracked barcodes) requires the **MatrixScan AR add-on** license. In MAUI, `IBarcodeBatchAdvancedOverlayListener.ViewForTrackedBarcode` must return a **native** view (`Android.Views.View` on Android, `UIKit.UIView` on iOS) — not a MAUI `View`. The canonical MAUI pattern (from the official `MatrixScanBubblesSample`) is a `partial` view model split into `Platforms/Android/MainPageViewModel.cs` and `Platforms/iOS/MainPageViewModel.cs`, each implementing the platform-specific `ViewForTrackedBarcode` and calling `mauiContentView.ToPlatform(new MauiContext(...))` to convert a MAUI control to the native view type. See "BarcodeBatchAdvancedOverlay (advanced)" in [references/integration.md](references/integration.md).
- **Per-barcode brush customization** (`IBarcodeBatchBasicOverlayListener.BrushForTrackedBarcode` and `BarcodeBatchBasicOverlay.SetBrushForTrackedBarcode`) requires the **MatrixScan AR add-on** license. A uniform default brush via `overlay.Brush = …` (no listener) does not require the add-on.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Upce`, `Symbology.Code39`, `Symbology.Code128`, `Symbology.InterleavedTwoOfFive`, `Symbology.Qr`, `Symbology.DataMatrix`. They are **not** the Kotlin underscore style (`EAN13_UPCA`, `CODE128`) and not Swift's camelCase (`ean13UPCA`).
- `BarcodeBatch.RecommendedCameraSettings` is a static **property**, applied with `camera.ApplySettingsAsync(BarcodeBatch.RecommendedCameraSettings)`. Not a method.
- Camera permission: use `await Permissions.CheckStatusAsync<Permissions.Camera>()` and `await Permissions.RequestAsync<Permissions.Camera>()`. MAUI's permission system also takes care of the underlying `AndroidManifest` / `Info.plist` entries — but on iOS the project still needs the `NSCameraUsageDescription` string set in `Info.plist`. On Android, MAUI adds `android.permission.CAMERA` automatically when `Permissions.Camera` is requested at build time (it can also be added to `Platforms/Android/AndroidManifest.xml` explicitly).
- `BarcodeBatchLicenseInfo` (read via `barcodeBatch.BarcodeBatchLicenseInfo`) is `dotnet.android=8.4+` / `dotnet.ios=8.4+` only. Before 8.4 the property does not exist — gate any usage on the installed SDK version. The value is available once `IDataCaptureContextListener.OnModeAdded` has been called.
- There is **no** `BarcodeScanned` event on `BarcodeBatch` (batch is tracking, not single-scan). Use the `SessionUpdated` event or implement `IBarcodeBatchListener.OnSessionUpdated` — the official MAUI sample uses the listener interface.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan Batch from scratch, configuring settings, handling tracked barcodes, customizing overlays, anchoring custom MAUI ContentViews on tracked barcodes, managing the camera lifecycle, or diagnosing a black or frozen preview** (e.g. "add MatrixScan Batch to my MAUI app", "scan all barcodes in view at once in MAUI", "highlight tracked barcodes in green in MAUI", "anchor a price label to each tracked barcode in MAUI", "show me how to set up BarcodeBatch in .NET MAUI", "my MAUI preview is black after I added BarcodeBatch", "my preview is stuttering on iOS after I integrated BarcodeBatch in MAUI") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing MatrixScan Batch integration** (e.g. "upgrade my MAUI BarcodeBatch app from v6 to v7", "rename BarcodeTracking to BarcodeBatch in my MAUI project", "bump the Scandit .NET MAUI SDK to v8", "what changed between SDK versions for BarcodeBatch in MAUI") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Replacing a third-party multi-barcode scanner with MatrixScan Batch** (e.g. "replace my ZXing.Net.Maui multi-detection scanner with MatrixScan Batch", "migrate from BarcodeScanning.Native.Maui multi-result to Scandit BarcodeBatch", "switch from [library] continuous multi-result scanning to BarcodeBatch in MAUI") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

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
| Get Started (Android target) | [Get Started (.NET for Android)](https://docs.scandit.com/sdks/net/android/matrixscan/get-started/) |
| Get Started (iOS target) | [Get Started (.NET for iOS)](https://docs.scandit.com/sdks/net/ios/matrixscan/get-started/) |
| AR overlays (per-barcode brushes, anchored views) | [Android Adding AR Overlays](https://docs.scandit.com/sdks/net/android/matrixscan/advanced/) · [iOS Adding AR Overlays](https://docs.scandit.com/sdks/net/ios/matrixscan/advanced/) |
| Migration between major SDK versions | [Android 6 → 7](https://docs.scandit.com/sdks/net/android/migrate-6-to-7/) · [Android 7 → 8](https://docs.scandit.com/sdks/net/android/migrate-7-to-8/) · [iOS 6 → 7](https://docs.scandit.com/sdks/net/ios/migrate-6-to-7/) · [iOS 7 → 8](https://docs.scandit.com/sdks/net/ios/migrate-7-to-8/) |
| Full API reference | [BarcodeBatch API (.NET Android)](https://docs.scandit.com/data-capture-sdk/dotnet.android/barcode-capture/api.html) · [BarcodeBatch API (.NET iOS)](https://docs.scandit.com/data-capture-sdk/dotnet.ios/barcode-capture/api.html) |

> Scandit publishes the .NET API reference per underlying TFM (`dotnet.android` and `dotnet.ios`). For MAUI projects, both pages apply — the API surface is identical between them for `BarcodeBatch`, but platform-specific notes (like iOS frame-data disposal, or the `Android.Views.View` vs. `UIKit.UIView` return type of `ViewForTrackedBarcode`) are documented on the per-TFM page.

## API surface this skill covers

All classes documented as `:available: dotnet.android` and `:available: dotnet.ios` in the official RST docs (`docs/source/barcode-capture/api/barcode-batch*.rst` and `api/ui/barcode-batch-*-overlay*.rst`) are addressed in [references/integration.md](references/integration.md):

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
- `BarcodeBatchAdvancedOverlay` — `Create(barcodeBatch, view)`, `Create(barcodeBatch)`, `Listener` (`IBarcodeBatchAdvancedOverlayListener?`), `SetViewForTrackedBarcode(trackedBarcode, view)`, `SetAnchorForTrackedBarcode(trackedBarcode, anchor)`, `SetOffsetForTrackedBarcode(trackedBarcode, offset)`, `ClearTrackedBarcodeViews()`, `ShouldShowScanAreaGuides`, `Dispose`. **Requires MatrixScan AR add-on.**
- `IBarcodeBatchAdvancedOverlayListener` — `ViewForTrackedBarcode(overlay, trackedBarcode)` (returns `Android.Views.View` on Android, `UIKit.UIView` on iOS — use a `partial` class split + `ToPlatform`), `AnchorForTrackedBarcode(overlay, trackedBarcode)`, `OffsetForTrackedBarcode(overlay, trackedBarcode)`. **Requires MatrixScan AR add-on.**
- MAUI-specific glue: `MauiAppBuilder.UseScanditCore(configure => configure.AddDataCaptureView())`, `MauiAppBuilder.UseScanditBarcode()`, `<scandit:DataCaptureView>` XAML control, `dataCaptureView.HandlerChanged` event, `dataCaptureView.AddOverlay(overlay)`, MAUI `Permissions.Camera`, `MainThread.BeginInvokeOnMainThread`, `MainThread.InvokeOnMainThreadAsync`, `IView.ToPlatform(new MauiContext(...))`.
