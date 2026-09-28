---
name: barcode-capture-net-maui
description: Scandit BarcodeCapture in .NET MAUI projects (`<UseMaui>true</UseMaui>`, `Scandit.DataCapture.Barcode.Maui` NuGet) — the low-level, full-control barcode scanning mode with your own `<scandit:DataCaptureView>` XAML control and overlay in a MAUI page, without the pre-built SparkScan UI (for that use sparkscan-net-maui); for non-MAUI .NET use barcode-capture-net-android or barcode-capture-net-ios. Use for integration, scan settings, result handling, lifecycle wiring, SDK version migration (v6→v7→v8), replacing ZXing.Net.Maui, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# BarcodeCapture .NET MAUI Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeCapture API changes significantly between major SDK versions — properties get renamed, removed, or restructured. The .NET MAUI binding adds platform-specific lifecycle and handler concerns on top of the regular .NET API, so patterns from the standalone `barcode-capture-net-android` / `barcode-capture-net-ios` skills do not always apply.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

MAUI-specific gotchas worth flagging:

- This skill targets MAUI apps with `<UseMaui>true</UseMaui>`. For non-MAUI .NET projects, use `barcode-capture-net-android` or `barcode-capture-net-ios` instead.
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
  `UseScanditBarcode()` takes **no inner configure** — there is no MAUI handler for BarcodeCapture itself, the call exists only to invoke `ScanditBarcodeCapture.Initialize()`. Do **not** write `UseScanditBarcode(configure => configure.AddBarcodeCaptureView())` — that method does not exist.
- `BarcodeCapture` does **not** have a pre-built MAUI view (unlike `BarcodeArView`, `BarcodeCountView`, `BarcodeFindView`, `BarcodePickView`, `SparkScanView`). The MAUI integration uses the generic `<scandit:DataCaptureView>` from `Scandit.DataCapture.Core.UI.Maui` and a `BarcodeCaptureOverlay` is added on top.
- XAML namespace for `DataCaptureView` is `xmlns:scandit="clr-namespace:Scandit.DataCapture.Core.UI.Maui;assembly=ScanditCaptureCoreMaui"`. **`DataCaptureContext="{Binding DataCaptureContext}"` is mandatory on the `<scandit:DataCaptureView>` element** — without it the preview renders as a **black/blank camera** at runtime even though the code-behind compiles and the camera is started. Setting `x:Name="dataCaptureView"` is not enough; the bindable property is what wires the context to the preview. The page's `BindingContext` (view model or `this`) must expose a `DataCaptureContext` property of type `Scandit.DataCapture.Core.Capture.DataCaptureContext`.
- The `BarcodeCaptureOverlay` must be created **after** the platform handler has been attached. The pattern used in the official sample is:
  ```csharp
  this.dataCaptureView.HandlerChanged += (s, e) =>
  {
      var overlay = BarcodeCaptureOverlay.Create(this.viewModel.BarcodeCapture);
      this.dataCaptureView.AddOverlay(overlay);
  };
  ```
  Creating the overlay before `HandlerChanged` fires will fail silently — there is no native view to attach it to yet.
- MAUI page lifecycle: `OnAppearing` → start the camera; `OnDisappearing` → stop the camera. The official sample factors this into a `ResumeAsync` / `SleepAsync` pattern on the view model.
- UI dispatch is `MainThread.BeginInvokeOnMainThread(() => …)` — not `RunOnUiThread` (Android-specific) and not `DispatchQueue.MainQueue.DispatchAsync` (iOS-specific). The dispatch wrapper is platform-agnostic.
- **`MainThread.StartTimer` does not exist.** `StartTimer` is an extension on `IDispatcher`. To re-enable scanning after a delay, use `await Task.Delay(...)` inside a `MainThread.BeginInvokeOnMainThread(async () => …)` lambda, or call `Dispatcher.StartTimer(...)` / `Application.Current.Dispatcher.StartTimer(...)`. See the "Re-enabling after a delay" section in [references/integration.md](references/integration.md).
- Camera permission: use `await Permissions.CheckStatusAsync<Permissions.Camera>()` and `await Permissions.RequestAsync<Permissions.Camera>()`. MAUI's permission system also takes care of the underlying `AndroidManifest` / `Info.plist` entries — but on iOS the project still needs the `NSCameraUsageDescription` string set in `Info.plist`. On Android, MAUI adds `android.permission.CAMERA` automatically when `Permissions.Camera` is requested at build time (it can also be added to `Platforms/Android/AndroidManifest.xml` explicitly).
- The .NET API uses **PascalCase factories**: `BarcodeCapture.Create(context, settings)`, `BarcodeCaptureSettings.Create()`, `BarcodeCaptureOverlay.Create(barcodeCapture, view)` or `BarcodeCaptureOverlay.Create(barcodeCapture)`, `DataCaptureContext.ForLicenseKey(key)`, `Camera.GetCamera(CameraPosition.WorldFacing)` or `Camera.GetDefaultCamera()`.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Code128`, `Symbology.InterleavedTwoOfFive`, `Symbology.Qr`, `Symbology.DataMatrix`.
- The capture mode's enabled property is `barcodeCapture.Enabled` (not `IsEnabled` or `isEnabled`).
- `CodeDuplicateFilter` is `TimeSpan` — **not** `TimeInterval`. Use `CodeDuplicate.DefaultDuplicateFilter`, `CodeDuplicate.ReportDataAndSymbologyOnlyOnce`, `TimeSpan.FromMilliseconds(500)`, `TimeSpan.FromSeconds(2.5)`, or `TimeSpan.Zero`.
- `BarcodeCapture.RecommendedCameraSettings` is a static **property**, applied with `camera.ApplySettingsAsync(BarcodeCapture.RecommendedCameraSettings)`.
- The official MAUI sample wires up the event-based API (`barcodeCapture.BarcodeScanned += handler`). Prefer that over `IBarcodeCaptureListener` in MAUI view-model code — it is the idiomatic C# pattern. The interface still works if the user prefers it.
- **Displaying the scan result**: call `await this.DisplayAlertAsync(title, message, "OK")` — the method name **ends in `Async`**. The non-`Async` `DisplayAlert(string, string, string)` overload is obsolete in MAUI 9 and produces `CS0618`; both overloads compile, so the deprecation is easy to miss if you reuse pre-MAUI-9 snippets. Prefer this (or the `IMessageService` wrapper used by the official sample) over inventing a `Label`/`VerticalStackLayout` on the page. The awaited alert blocks until dismissal, which is the natural point to re-enable scanning (`barcodeCapture.Enabled = true`). See "Displaying the scan result to the user" in [references/integration.md](references/integration.md) for both the inline and the injectable `IMessageService` patterns.
- iOS frame-data disposal note: when the MAUI app is running on iOS, `frameData.Dispose()` should still be called inside `OnBarcodeScanned` if the project uses the `IBarcodeCaptureListener` interface. The official sample uses the event API and does not dispose the frame explicitly there because the event-args lifetime is managed by the SDK — if disposing inside the event handler, do it in a `try`/`finally` block so a thrown exception cannot leave a frame undisposed.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeCapture from scratch, configuring settings, customizing feedback, adding a viewfinder, handling scans, or doing async work after a scan** (e.g. "add BarcodeCapture to my MAUI app", "set up barcode scanning in MAUI", "how do I use Scandit BarcodeCapture in MAUI", "filter duplicate scans", "suppress the beep", "add a viewfinder", "disable scanning while I look up the barcode", "where do I create the BarcodeCaptureOverlay in MAUI") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing BarcodeCapture integration** (e.g. "upgrade from v6 to v7", "migrate my BarcodeCapture", "bump the Scandit .NET MAUI SDK to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Replacing a third-party barcode scanner with BarcodeCapture** (e.g. "replace my ZXing.Net.Maui scanner with BarcodeCapture", "migrate from BarcodeScanning.Native.Maui to Scandit", "switch from [library] to BarcodeCapture") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

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
| Get Started (Android target) | [Get Started (.NET for Android)](https://docs.scandit.com/sdks/net/android/barcode-capture/get-started/) |
| Get Started (iOS target) | [Get Started (.NET for iOS)](https://docs.scandit.com/sdks/net/ios/barcode-capture/get-started/) |
| Advanced topics (custom feedback, viewfinders, location selection, scan intention, composite codes) | [Android Advanced Configurations](https://docs.scandit.com/sdks/net/android/barcode-capture/advanced/) · [iOS Advanced Configurations](https://docs.scandit.com/sdks/net/ios/barcode-capture/advanced/) |
| Migration between major SDK versions | [Android 6 → 7](https://docs.scandit.com/sdks/net/android/migrate-6-to-7/) · [Android 7 → 8](https://docs.scandit.com/sdks/net/android/migrate-7-to-8/) · [iOS 6 → 7](https://docs.scandit.com/sdks/net/ios/migrate-6-to-7/) · [iOS 7 → 8](https://docs.scandit.com/sdks/net/ios/migrate-7-to-8/) |
| Full API reference | [BarcodeCapture API (.NET Android)](https://docs.scandit.com/data-capture-sdk/dotnet.android/barcode-capture/api.html) · [BarcodeCapture API (.NET iOS)](https://docs.scandit.com/data-capture-sdk/dotnet.ios/barcode-capture/api.html) |

> Scandit publishes the .NET API reference per underlying TFM (`dotnet.android` and `dotnet.ios`). For MAUI projects, both pages apply — the API surface is identical between them, but platform-specific notes (like iOS frame-data disposal) are documented on the per-TFM page.

## API surface this skill covers

All classes documented as `:available: dotnet.android` and `:available: dotnet.ios` in the official RST docs are addressed in [references/integration.md](references/integration.md):

- `BarcodeCapture` — `Create(context, settings)`, `Create(settings)`, `Enabled`, `PointOfInterest`, `Feedback`, `BarcodeCaptureLicenseInfo`, `Context`, static `RecommendedCameraSettings`, `ApplySettingsAsync`, `AddListener` / `RemoveListener`, events `BarcodeScanned` / `SessionUpdated`.
- `BarcodeCaptureSettings` — `Create()`, `EnableSymbology`, `EnableSymbologies(ICollection<Symbology>)`, `EnableSymbologies(CompositeType)`, `GetSymbologySettings`, `EnabledSymbologies`, `EnabledCompositeTypes`, `CodeDuplicateFilter`, `LocationSelection`, `BatterySaving`, `ScanIntention`, `SetProperty` / `GetProperty<T>` / `TryGetProperty<T>`.
- `BarcodeCaptureFeedback` — static `DefaultFeedback`, `Success`.
- `BarcodeCaptureSession` — `NewlyRecognizedBarcode`, `NewlyLocalizedBarcodes`, `FrameSequenceId`, `Reset()`.
- `IBarcodeCaptureListener` — `OnObservationStarted`, `OnObservationStopped`, `OnBarcodeScanned`, `OnSessionUpdated`.
- `BarcodeCaptureEventArgs` — `BarcodeCapture`, `Session`, `FrameData`.
- `BarcodeCaptureLicenseInfo` — `LicensedSymbologies`.
- `BarcodeCaptureOverlay` — `Create(barcodeCapture, view)`, `Create(barcodeCapture)`, `Brush`, static `DefaultBrush`, `Viewfinder`, `ShouldShowScanAreaGuides`, `SetProperty`.
- MAUI-specific glue: `MauiAppBuilder.UseScanditCore(configure => configure.AddDataCaptureView())`, `MauiAppBuilder.UseScanditBarcode()`, `<scandit:DataCaptureView>` XAML control, `dataCaptureView.HandlerChanged` event, `dataCaptureView.AddOverlay(overlay)`, MAUI `Permissions.Camera`, `MainThread.BeginInvokeOnMainThread`.
