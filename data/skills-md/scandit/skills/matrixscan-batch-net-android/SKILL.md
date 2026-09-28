---
name: matrixscan-batch-net-android
description: MatrixScan Batch (MatrixScan, BarcodeBatch, legacy BarcodeTracking) in .NET for Android projects (`net*-android` TFM, `Scandit.DataCapture.Barcode` NuGet, non-MAUI — MAUI apps use matrixscan-batch-net-maui) — tracking and scanning multiple barcodes at once. Use for integration, settings and symbologies, listeners/events, basic/advanced overlay customization, camera lifecycle, SDK version migration, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Batch .NET for Android Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeBatch API changes between major SDK versions — the class itself was renamed from `BarcodeTracking` to `BarcodeBatch` at v7.0, overlay factories evolved, and the .NET binding deviates from the Kotlin / iOS native APIs in several places (`Create` factories instead of `forDataCaptureContext`, `Enabled` instead of `isEnabled`, `TimeSpan` instead of `TimeInterval`, PascalCase symbology names, etc.).

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

.NET-Android-specific gotchas worth flagging:

- This skill targets the **non-MAUI** .NET for Android workload (project `<TargetFramework>net10.0-android</TargetFramework>`, no `<UseMaui>` flag). For MAUI apps, use the `matrixscan-batch-net-maui` skill instead (planned).
- **`BarcodeBatch.Create(dataCaptureContext, settings)` is the .NET factory** — not `new BarcodeBatch(...)` (the public constructor is `private`) and not `BarcodeBatch.ForDataCaptureContext(...)` (that name appears in the Kotlin / docs API but the C# binding is `Create`). When the context is non-null, the factory attaches the mode to the context automatically.
- **`BarcodeBatchSettings.Create()` is a factory** — also `private` constructor. Writing `new BarcodeBatchSettings()` is a compile error.
- **`BarcodeBatchBasicOverlay.Create(...)` and `BarcodeBatchAdvancedOverlay.Create(...)` are factories**, each with multiple overloads. When passed a non-null `DataCaptureView`, both auto-add the overlay to the view — no separate `AddOverlay` call is needed.
- **`BarcodeBatch.RecommendedCameraSettings` is a static property**, not a method. The canonical pattern (mirroring the official .NET Android sample) is `camera = Camera.GetDefaultCamera(); camera.ApplySettingsAsync(BarcodeBatch.RecommendedCameraSettings);`. The Kotlin form `createRecommendedCameraSettings()` does **not** exist in the .NET binding.
- Camera setup is **manual**, mirroring BarcodeCapture on .NET Android: `Camera.GetDefaultCamera()` → `camera.ApplySettingsAsync(BarcodeBatch.RecommendedCameraSettings)` → `dataCaptureContext.SetFrameSourceAsync(camera)` (the .NET binding is `SetFrameSourceAsync`, not the synchronous Kotlin `setFrameSource`).
- **`DataCaptureView.Create(dataCaptureContext)` takes no `Context` parameter** in .NET — different from Kotlin's `DataCaptureView.newInstance(context, dataCaptureContext)`. The returned Android `View` is added to a `FrameLayout` container via `container.AddView(dataCaptureView)`.
- **`IBarcodeBatchListener.OnSessionUpdated(BarcodeBatch, BarcodeBatchSession, IFrameData)` runs on a background recognition thread** — not the UI thread. Dispatch any UI work via `RunOnUiThread(() => { … })`. The third parameter is `IFrameData` (the .NET binding), not `FrameData` (Kotlin).
- The .NET binding also exposes the **event API** on `BarcodeBatch`: `barcodeBatch.SessionUpdated += handler` (`EventHandler<BarcodeBatchEventArgs>`). Use either the listener interface OR the event — not both for the same handler. There is **no** `BarcodeScanned` event on `BarcodeBatch` (batch is tracking, not single-scan).
- **Do not hold references to `BarcodeBatchSession` or its collections outside `OnSessionUpdated`.** The session is only safe to access within that callback — copy `AddedTrackedBarcodes` / `UpdatedTrackedBarcodes` / `TrackedBarcodes` data first, then dispatch.
- `BarcodeBatchSession` properties: `AddedTrackedBarcodes` (`IList<TrackedBarcode>`), `UpdatedTrackedBarcodes` (`IList<TrackedBarcode>`), `RemovedTrackedBarcodes` (`IList<int>` — tracking IDs only, not `TrackedBarcode`), `TrackedBarcodes` (`IDictionary<int, TrackedBarcode>`), `FrameSequenceId` (`long`), `Reset()`. Note: `Reset()` lives on the **Session** in the .NET binding (there is no `BarcodeBatch.Reset()` like Kotlin has).
- `TrackedBarcode` properties: `Barcode`, `Identifier` (`int`), `Location` (`Quadrilateral`), plus `GetAnchorPosition(Anchor)`. The tracking identifier is reused after a barcode leaves the frame.
- The capture mode's enabled property is `barcodeBatch.Enabled` (not `IsEnabled`). `IDataCaptureMode` exposes `Enabled` in the .NET binding.
- **`BarcodeBatchBasicOverlayStyle` is C# PascalCase**: `Frame` (default) and `Dot`. Not `FRAME` / `DOT` (Kotlin) and not `frame` / `dot` (Swift).
- **Per-barcode brush customization** (`IBarcodeBatchBasicOverlayListener.BrushForTrackedBarcode` and `BarcodeBatchBasicOverlay.SetBrushForTrackedBarcode`) requires the **MatrixScan AR add-on** license. A uniform default brush via `overlay.Brush = …` (no listener) does not require the add-on.
- **`BarcodeBatchAdvancedOverlay`** (anchoring custom Android `View`s to tracked barcodes) requires the **MatrixScan AR add-on** license. `IBarcodeBatchAdvancedOverlayListener` has `ViewForTrackedBarcode(overlay, trackedBarcode)`, `AnchorForTrackedBarcode(...)`, `OffsetForTrackedBarcode(...)` — all three are called on the main thread.
- `BarcodeBatchLicenseInfo` (read via `barcodeBatch.BarcodeBatchLicenseInfo`) is `dotnet.android=8.4+` only. Before 8.4 the property does not exist — gate any usage on the installed SDK version. The value is available once `IDataCaptureContextListener.OnModeAdded` has been called.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Upce`, `Symbology.Code39`, `Symbology.Code128`, `Symbology.InterleavedTwoOfFive`, `Symbology.Qr`, `Symbology.DataMatrix`. They are **not** the Kotlin underscore style (`EAN13_UPCA`, `CODE128`).
- The NuGet packages are `Scandit.DataCapture.Core` and `Scandit.DataCapture.Barcode`. No separate `*.Maui` packages here — those are only for MAUI projects. **Do not guess the version from training data** — fetch the latest stable from `https://www.nuget.org/packages/Scandit.DataCapture.Barcode/` via `WebFetch` before pinning. Inventing a non-existent version causes `dotnet restore` to fail with `Unable to find package Scandit.DataCapture.Core with version (>= …)`. See [references/integration.md](references/integration.md) Step 0 for the full procedure.
- **Android `SupportedOSPlatformVersion` must be ≥ `24`.** Set it in the `.csproj`. Lower values fail the build with `uses-sdk:minSdkVersion 21 cannot be smaller than version 24 declared in library`.
- **Do not declare `<activity>` elements for `[Activity]`-decorated classes in `AndroidManifest.xml`.** The `[Activity(MainLauncher = true, ...)]` attribute is the canonical registration mechanism in .NET for Android — the build merges a correctly-named entry into the final manifest using the .NET-derived Java class name. A manual `<activity android:name=".MainActivity">` resolves against `<ApplicationId>` and **won't match** the generated class, producing `ClassNotFoundException: Didn't find class ... .MainActivity` at launch. Only add to the manifest the elements the skill explicitly asks for (`<uses-feature>`, `<uses-permission>`, and an `android:theme` on `<application>` when needed) — leave activities to the attribute.
- The runtime camera permission helper (`CameraPermissionActivity`) inherits from `AppCompatActivity`, so `Xamarin.AndroidX.AppCompat` must be in the `.csproj`. When pinning the version, pick the highest available including the Xamarin patch revision (e.g. `1.7.0.5`, not bare `1.7.0`) — the `.X` suffix marks Xamarin-binding-level updates and carries critical transitive-dep fixes.
- **The activity needs a `Theme.AppCompat` descendant.** Because the activity inherits from `AppCompatActivity`, set `android:theme="@style/Theme.AppCompat.DayNight.NoActionBar"` (or another `Theme.AppCompat` subclass) on the `<application>` element of `AndroidManifest.xml`, or set `Theme = "@style/Theme.AppCompat.Light.NoActionBar"` on the `[Activity]` attribute. Without it, `SetContentView` throws `IllegalStateException: You need to use a Theme.AppCompat theme (or descendant) with this activity` at launch. The `dotnet new android` template's default theme is **not** AppCompat-based, so it must be set explicitly.
- **SDK 8.0+ requires explicit initialization.** Subclass `Android.App.Application`, decorate with `[Application]`, and call `ScanditCaptureCore.Initialize()` + `ScanditBarcodeCapture.Initialize()` in `OnCreate()` before any Scandit code runs. Without this the SDK's DI container has no registrations and the first `BarcodeBatch.Create(...)` / `DataCaptureView.Create(...)` call crashes at launch. **Not required on 6.x / 7.x.** See [references/integration.md](references/integration.md) Step 0 / Prerequisites for the full `MainApplication.cs` template.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan Batch from scratch, configuring settings, handling tracked barcodes, customizing overlays, anchoring custom views, or managing the camera lifecycle** (e.g. "add MatrixScan Batch to my .NET Android app", "scan all barcodes in view at once in C#", "highlight tracked barcodes in green", "anchor a price label to each tracked barcode", "show me how to set up BarcodeBatch in net-android") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing MatrixScan Batch integration** (e.g. "upgrade from v6 to v7", "rename BarcodeTracking to BarcodeBatch", "bump the Scandit .NET SDK to v8", "what changed between SDK versions for BarcodeBatch") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Replacing a third-party multi-barcode scanner with MatrixScan Batch** (e.g. "replace my ZXing.Net.Mobile loop with MatrixScan Batch", "migrate from ZXing.Net continuous scanning to Scandit", "switch from ML Kit batch scanning to BarcodeBatch") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

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
| Get Started | [Get Started (.NET for Android)](https://docs.scandit.com/sdks/net/android/matrixscan/get-started/) |
| AR overlays (per-barcode brushes, anchored views) | [Adding AR Overlays](https://docs.scandit.com/sdks/net/android/matrixscan/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/net/android/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/android/migrate-7-to-8/) |
| Full API reference | [BarcodeBatch API (.NET Android)](https://docs.scandit.com/data-capture-sdk/dotnet.android/barcode-capture/api.html) |

## API surface this skill covers

All classes documented with `:available: dotnet.android` in the official RST docs (`docs/source/barcode-capture/api/barcode-batch*.rst` and `api/ui/barcode-batch-*-overlay*.rst`) are addressed in [references/integration.md](references/integration.md):

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
- `IBarcodeBatchAdvancedOverlayListener` — `ViewForTrackedBarcode(overlay, trackedBarcode)`, `AnchorForTrackedBarcode(overlay, trackedBarcode)`, `OffsetForTrackedBarcode(overlay, trackedBarcode)`. **Requires MatrixScan AR add-on.**
