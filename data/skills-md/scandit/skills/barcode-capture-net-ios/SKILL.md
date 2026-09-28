---
name: barcode-capture-net-ios
description: Scandit BarcodeCapture in .NET for iOS projects (`net*-ios` target framework, `Scandit.DataCapture.Barcode` NuGet, non-MAUI — for MAUI apps use barcode-capture-net-maui) — the low-level, full-control barcode scanning mode without the pre-built SparkScan UI. Use for integration, scan settings, listener and event wiring, overlay customization, camera lifecycle, SDK version migration (v6→v7→v8), replacing ZXing.Net.Mobile or AVFoundation scanners, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# BarcodeCapture .NET for iOS Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeCapture API changes significantly between major SDK versions — properties get renamed, removed, or restructured. The .NET binding also uses **different naming conventions** than the native Swift SDK (PascalCase, `Create(...)` factories instead of `init(context:settings:)`, `Enabled` instead of `isEnabled`, etc.).

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

.NET-iOS-specific gotchas worth flagging:

- This skill targets the **non-MAUI** .NET for iOS workload (project `<TargetFramework>net10.0-ios</TargetFramework>`, no `<UseMaui>` flag). For MAUI apps, use the `barcode-capture-net-maui` skill instead.
- The .NET API uses **PascalCase factories**, not the Swift `BarcodeCapture(context:settings:)` initializer. Use `BarcodeCapture.Create(context, settings)`, `BarcodeCaptureSettings.Create()`, `BarcodeCaptureOverlay.Create(barcodeCapture, dataCaptureView)`, `DataCaptureView.Create(dataCaptureContext, frame)`.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Code128`, `Symbology.InterleavedTwoOfFive`, `Symbology.Qr`, `Symbology.DataMatrix`. They are **not** Swift's `.ean13UPCA` style.
- The capture mode's enabled property is `barcodeCapture.Enabled` (not `IsEnabled` and not Swift's `isEnabled`).
- `CodeDuplicateFilter` is `TimeSpan` — **not** Swift's `TimeInterval`. Use `CodeDuplicate.DefaultDuplicateFilter`, `CodeDuplicate.ReportDataAndSymbologyOnlyOnce`, `TimeSpan.FromMilliseconds(500)`, `TimeSpan.FromSeconds(2.5)`, or `TimeSpan.Zero`. Writing `CodeDuplicateFilter = 0.5` (as a double) is a type error.
- `BarcodeCapture.RecommendedCameraSettings` is a **static property**, not a method. The canonical pattern (used in the official .NET iOS sample) is `camera = Camera.GetDefaultCamera(); camera.ApplySettingsAsync(BarcodeCapture.RecommendedCameraSettings);`. A `Camera.GetDefaultCamera(CameraSettings?)` overload also exists in the .NET binding (it calls `ApplySettingsAsync` internally) but the samples use the explicit two-line form — prefer it for clarity.
- `IBarcodeCaptureListener` callbacks are C#-named: `OnBarcodeScanned`, `OnSessionUpdated`, `OnObservationStarted`, `OnObservationStopped`. The `IFrameData` parameter is named `frameData`.
- The .NET binding also exposes a C# **event-based** API on `BarcodeCapture`: `BarcodeScanned` and `SessionUpdated` (both `EventHandler<BarcodeCaptureEventArgs>`). Use either the listener interface *or* the events — do not register the same handler through both paths.
- `OnBarcodeScanned` is invoked off the UI thread. Any UI update must be dispatched via `DispatchQueue.MainQueue.DispatchAsync(...)`.
- **Always call `frameData.Dispose()`** at the end of `OnBarcodeScanned` and `OnSessionUpdated`. The official iOS sample explicitly disposes the frame to avoid a "frozen, non-responsive, or severely stuttering" video feed. This is not optional on iOS.
- Call `barcodeCapture.Enabled = false` at the top of `OnBarcodeScanned` before doing any work to prevent duplicate or racing scans. Re-enable with `barcodeCapture.Enabled = true` when the app is ready to scan again.
- `DataCaptureView.Create(dataCaptureContext, frame)` takes a `CGRect` (or `this.View.Bounds`) for the initial frame — this is **different from the Android binding**, which takes only the context. Set `AutoresizingMask = UIViewAutoresizing.FlexibleHeight | UIViewAutoresizing.FlexibleWidth` and add it as a subview of `this.View`.
- Lifecycle: `ViewWillAppear` enables the capture mode and starts the camera; `ViewWillDisappear` stops the camera. The official sample only stops the camera in `ViewWillDisappear` and sets `Enabled = false` inside `OnBarcodeScanned` instead — both patterns are valid.
- The required Info.plist key is `NSCameraUsageDescription` (`Privacy - Camera Usage Description`). Without it the app crashes on first camera access.
- The NuGet packages are `Scandit.DataCapture.Core` and `Scandit.DataCapture.Barcode`. No `*.Maui` packages — those are MAUI-only. **Do not guess the version from training data** — fetch the latest stable from `https://www.nuget.org/packages/Scandit.DataCapture.Barcode/` via `WebFetch` before pinning. Inventing a non-existent version (e.g. `8.13.0` when only `8.4.0` is published) causes `dotnet restore` to fail with `Unable to find package Scandit.DataCapture.Core with version (>= …)`. See [references/integration.md](references/integration.md) Step 0 for the full procedure.
- **SDK 8.0+ requires explicit initialization.** Call `ScanditCaptureCore.Initialize()` + `ScanditBarcodeCapture.Initialize()` in `AppDelegate.FinishedLaunching` before any Scandit API is touched (typically before creating the window / root view controller). Without this the SDK's DI container has no registrations and the first `DataCaptureView.Create` / `BarcodeCapture.Create` call crashes at launch. **Not required on 6.x / 7.x** — those majors self-initialized. See the integration guide for the full `AppDelegate` template.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeCapture from scratch, configuring settings, customizing feedback, adding a viewfinder, handling scans, or doing async work after a scan** (e.g. "add BarcodeCapture to my .NET iOS app", "set up barcode scanning in C# / iOS", "how do I use BarcodeCapture in net-ios", "filter duplicate scans", "suppress the beep", "add a viewfinder", "disable scanning while I look up the barcode") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing BarcodeCapture integration** (e.g. "upgrade from v6 to v7", "migrate my BarcodeCapture", "bump the Scandit .NET SDK to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Replacing a third-party barcode scanner with BarcodeCapture** (e.g. "replace my ZXing.Net.Mobile scanner with BarcodeCapture", "migrate from AVFoundation barcode scanning to Scandit", "switch from [library] to BarcodeCapture") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

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
| Get Started | [Get Started (.NET for iOS)](https://docs.scandit.com/sdks/net/ios/barcode-capture/get-started/) |
| Advanced topics (custom feedback, viewfinders, location selection, scan intention, composite codes) | [Advanced Configurations](https://docs.scandit.com/sdks/net/ios/barcode-capture/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/net/ios/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/ios/migrate-7-to-8/) |
| Full API reference | [BarcodeCapture API (.NET iOS)](https://docs.scandit.com/data-capture-sdk/dotnet.ios/barcode-capture/api.html) |

## API surface this skill covers

All classes with `:available: dotnet.ios` in the official RST docs are addressed in [references/integration.md](references/integration.md):

- `BarcodeCapture` — `Create(context, settings)`, `Create(settings)`, `Enabled`, `PointOfInterest`, `Feedback`, `BarcodeCaptureLicenseInfo`, `Context`, static `RecommendedCameraSettings`, `ApplySettingsAsync`, `AddListener` / `RemoveListener`, events `BarcodeScanned` / `SessionUpdated`.
- `BarcodeCaptureSettings` — `Create()`, `EnableSymbology`, `EnableSymbologies(ICollection<Symbology>)`, `EnableSymbologies(CompositeType)`, `GetSymbologySettings`, `EnabledSymbologies`, `EnabledCompositeTypes`, `CodeDuplicateFilter`, `LocationSelection`, `BatterySaving`, `ScanIntention`, `SetProperty` / `GetProperty<T>` / `TryGetProperty<T>`.
- `BarcodeCaptureFeedback` — static `DefaultFeedback`, `Success`.
- `BarcodeCaptureSession` — `NewlyRecognizedBarcode`, `NewlyLocalizedBarcodes`, `FrameSequenceId`, `Reset()`.
- `IBarcodeCaptureListener` — `OnObservationStarted`, `OnObservationStopped`, `OnBarcodeScanned`, `OnSessionUpdated`.
- `BarcodeCaptureEventArgs` — `BarcodeCapture`, `Session`, `FrameData`.
- `BarcodeCaptureLicenseInfo` — `LicensedSymbologies`.
- `BarcodeCaptureOverlay` — `Create(barcodeCapture, view)`, `Create(barcodeCapture)`, `Brush`, static `DefaultBrush`, `Viewfinder`, `ShouldShowScanAreaGuides`, `SetProperty`.
