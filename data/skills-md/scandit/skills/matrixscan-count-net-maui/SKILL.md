---
name: matrixscan-count-net-maui
description: MatrixScan Count (BarcodeCount) in .NET MAUI projects (<UseMaui>true</UseMaui>, Scandit.DataCapture.Barcode.Maui NuGet) — counting/receiving workflows with the BarcodeCountView XAML control and capture/receiving lists. For non-MAUI .NET use matrixscan-count-net-android or matrixscan-count-net-ios. Use for integration, XAML and builder-chain setup, result handling, UI customization, SDK version migration, or troubleshooting counting workflows.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Count .NET MAUI Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The .NET binding differs from the Kotlin/Java and Swift native SDKs (factories instead of constructors, PascalCase members, C# events alongside listener interfaces), and the .NET MAUI integration adds its own handler/XAML/lifecycle concerns on top. Patterns from the standalone `matrixscan-count-net-android` / `matrixscan-count-net-ios` skills do not always apply unchanged — and the MAUI `BarcodeCountView` is **not** wired the way the non-MAUI native views are.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

MAUI-specific gotchas worth flagging (and the places people get it wrong by pattern-matching from MatrixScan Batch, SparkScan, or the native Android/iOS Count skills):

- This skill targets MAUI apps with `<UseMaui>true</UseMaui>`. For non-MAUI .NET projects, use `matrixscan-count-net-android` (for `net*-android`) or `matrixscan-count-net-ios` (for `net*-ios`) instead — there the view is hosted natively (added to a `FrameLayout` / a `UIView`), which is completely different from the MAUI XAML control.
- **The MAUI builder chain for BarcodeCount is `.UseScanditCore().UseScanditBarcode(configure => configure.AddBarcodeCountView())`.** `UseScanditCore` takes **no** lambda; `UseScanditBarcode` **does** take a lambda with `AddBarcodeCountView()` inside it. This is the **same shape as SparkScan** (`AddSparkScanView`) and the **opposite** of the BarcodeBatch / BarcodeCapture chain, which is `.UseScanditCore(c => c.AddDataCaptureView()).UseScanditBarcode()`. Do **not** write `AddDataCaptureView()` for BarcodeCount — it has its own pre-built MAUI handler and does **not** use the generic `<scandit:DataCaptureView>`.
- **XAML namespace is `clr-namespace:Scandit.DataCapture.Barcode.Count.UI.Maui;assembly=ScanditBarcodeCaptureMaui`.** Note `assembly=ScanditBarcodeCaptureMaui` (no dots) — the NuGet package is `Scandit.DataCapture.Barcode.Maui` but the assembly it produces is `ScanditBarcodeCaptureMaui`. The control is `<scandit:BarcodeCountView>`, distinct from SparkScan's `<scandit:SparkScanView>` and from the generic `<scandit:DataCaptureView>`.
- **`<scandit:BarcodeCountView>` requires two bound properties: `DataCaptureContext` and `BarcodeCount`.** Both are `OneTime` bindable properties — bind them to view-model properties (`DataCaptureContext="{Binding DataCaptureContext}"`, `BarcodeCount="{Binding BarcodeCount}"`). Without both, the preview is black and counting never starts. Setting `x:Name` alone does **not** wire them.
- **The view-style property is `ViewStyle`, not `Style`, and its default is `Dot`.** In XAML write `ViewStyle="Icon"` (or `ViewStyle="Dot"`). `Style` is a stock MAUI `VisualElement` property and setting it does nothing for the counting UI. `ViewStyle` is `OneTime` — set it in XAML at creation, not later in code.
- **You manage the camera yourself — `BarcodeCountView` does NOT own it.** This is the single biggest difference from SparkScan in MAUI (where the `SparkScanView` drives the camera through `OnAppearing()`/`OnDisappearing()`). For BarcodeCount you must: `Camera.GetDefaultCamera(BarcodeCount.RecommendedCameraSettings)`, `dataCaptureContext.SetFrameSourceAsync(camera)`, and toggle it with `camera.SwitchToDesiredStateAsync(FrameSourceState.On/Off)` from the page's `OnAppearing` / `OnDisappearing`. The MAUI `BarcodeCountView` has **no** `OnAppearing()`/`OnDisappearing()`/`StartScanning()` methods — do not call them (those are SparkScanView's).
- **`barcodeCount.Enabled` (get/set `bool`) must be `true`** for frames to be processed. Set it `true` when resuming and (optionally) `false` when pausing.
- **`BarcodeCount` is created with a FACTORY, not `new`**: `BarcodeCount.Create(dataCaptureContext, settings)` (there is also a `BarcodeCount.Create(settings)` overload with no context). `new BarcodeCount(...)` is a compile error — the constructor is private. `BarcodeCountSettings` **does** use a plain `new BarcodeCountSettings()`.
- **The List / Exit / SingleScan button events are on the MAUI `BarcodeCountView`, but they only fire after the native handler is attached.** Subscribe to them inside the `dataCaptureView.HandlerChanged` (or `HandlerReady`) handler, exactly as the official `MatrixScanCountSimpleSample` does — subscribing in the constructor before the handler exists silently does nothing. The events are `ListButtonTapped` (`ListButtonTappedEventArgs`), `ExitButtonTapped` (`ExitButtonTappedEventArgs`), `SingleScanButtonTapped` (`SingleScanButtonTappedEventArgs`); their event-arg types live in the **non-MAUI** namespace `Scandit.DataCapture.Barcode.Count.UI`.
- **`IBarcodeCountListener` has THREE methods:** `OnScan(BarcodeCount, BarcodeCountSession, IFrameData)`, `OnObservationStarted(BarcodeCount)`, `OnObservationStopped(BarcodeCount)`. The idiomatic C# alternative is the **`barcodeCount.Scanned` event** (`EventHandler<BarcodeCountEventArgs>`), which corresponds to `OnScan` only. The official MAUI sample wires the `Scanned` event on the view model.
- **`Scanned` / `OnScan` fires once per scan phase, on a background thread.** Copy the barcodes you need out of the session immediately (`session.RecognizedBarcodes.ToList()` / `[.. session.RecognizedBarcodes]`); the `BarcodeCountSession` is **not** valid outside the callback. Dispatch UI updates via `MainThread.BeginInvokeOnMainThread(...)` — not `RunOnUiThread` (Android-only) and not `DispatchQueue.MainQueue` (iOS-only).
- **`BarcodeCountSession` exposes `RecognizedBarcodes` and `AdditionalBarcodes` as `IList<Barcode>`** — plain decoded barcodes, not tracked-barcode deltas. There is no `AddedTrackedBarcodes` / `RemovedTrackedBarcodes` on this session (that's the Batch session). Also `FrameSequenceId`, `Reset()`, and `GetSpatialMap()`.
- **`BarcodeCountFeedback` uses `Success` and `Failure`** (`Core.Common.Feedback.Feedback`). The empty constructor `new BarcodeCountFeedback()` is silent; the static `BarcodeCountFeedback.DefaultFeedback` (a **property**, not a method) restores defaults.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Upce`, `Symbology.Code128`, `Symbology.Code39`, `Symbology.Qr`, `Symbology.DataMatrix`, `Symbology.InterleavedTwoOfFive`. They are **not** the Kotlin underscore style (`EAN13_UPCA`) or Swift camelCase (`ean13UPCA`).
- **Capture list (receiving) uses factories:** `BarcodeCountCaptureList.Create(listener, IList<TargetBarcode>)` and `TargetBarcode.Create(data, quantity)`. Apply it with `barcodeCount.SetBarcodeCountCaptureList(list)`. The listener `IBarcodeCountCaptureListListener` has `OnObservationStarted()`, `OnObservationStopped()`, `OnCaptureListSessionUpdated(session)`, `OnCaptureListCompleted(session)`.
- **No manual `ScanditCaptureCore.Initialize()` / `ScanditBarcodeCapture.Initialize()` call is needed.** The MAUI builder extensions (`UseScanditCore` / `UseScanditBarcode`) perform the SDK 8.0+ initialization themselves. This is different from the non-MAUI `matrixscan-count-net-android` / `matrixscan-count-net-ios` skills, which require manual initialization for SDK 8.0+. In a MAUI app the `MainApplication` / `AppDelegate` only forward to `MauiProgram.CreateMauiApp()` — leave them as the MAUI template generates them.
- Required NuGet packages: `Scandit.DataCapture.Core`, `Scandit.DataCapture.Core.Maui`, `Scandit.DataCapture.Barcode`, `Scandit.DataCapture.Barcode.Maui`. All four — Core/Barcode provide the platform bindings, Core.Maui/Barcode.Maui provide the MAUI builder extensions and handlers. **Do not guess the version** — fetch the latest stable from `https://www.nuget.org/packages/Scandit.DataCapture.Barcode.Maui/` via `WebFetch` and use the same version for all four.
- **Android `SupportedOSPlatformVersion` must be ≥ `24`.** The MAUI template defaults to `21`, which is below Scandit's Android AAR minimum and fails the build with `uses-sdk:minSdkVersion 21 cannot be smaller than version 24 declared in library`. Bump the `.csproj` value to `24.0` (or higher). iOS minimum is `15.0` (matches the MAUI template default).
- **iOS `NSCameraUsageDescription` in `Platforms/iOS/Info.plist`** is mandatory — without it the app crashes on first camera access. On Android, MAUI's `Permissions.Camera` adds `android.permission.CAMERA` automatically when requested at build time (or add it explicitly to `Platforms/Android/AndroidManifest.xml`).

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeCount from scratch, registering the builder chain, declaring the `<scandit:BarcodeCountView>`, configuring settings, wiring the camera lifecycle, handling scan results, storing scanned barcodes, capture/receiving lists, the spatial map, customizing feedback, List/Exit/SingleScan taps, brushes, status mode, the not-in-list action, or diagnosing a black preview** (e.g. "add MatrixScan Count to my MAUI app", "count barcodes in .NET MAUI", "store the scanned barcodes when the list button is tapped", "check scans against an expected list in MAUI", "make the beep silent", "use the Icon style", "my MAUI count preview is black") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing MatrixScan Count MAUI integration** (e.g. "upgrade my MAUI BarcodeCount app from v7 to v8", "bump the Scandit .NET MAUI SDK to v8", "what changed between SDK versions for BarcodeCount in MAUI") → read [references/migration.md](references/migration.md) and follow the instructions there.

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
| Get Started | [Get Started (.NET MAUI)](https://docs.scandit.com/sdks/net/maui/matrixscan-count/get-started/) |
| Advanced topics (capture list, status mode, brushes, toolbar, hardware trigger) | [Advanced (.NET Android)](https://docs.scandit.com/sdks/net/android/matrixscan-count/advanced/) · [(.NET iOS)](https://docs.scandit.com/sdks/net/ios/matrixscan-count/advanced/) — MAUI shares both TFMs |
| Migration between major SDK versions | Android: [6 → 7](https://docs.scandit.com/sdks/net/android/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/android/migrate-7-to-8/) · iOS: [6 → 7](https://docs.scandit.com/sdks/net/ios/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/ios/migrate-7-to-8/) |
| Full API reference | [BarcodeCount API (.NET Android)](https://docs.scandit.com/data-capture-sdk/dotnet.android/barcode-capture/api.html) · [BarcodeCount API (.NET iOS)](https://docs.scandit.com/data-capture-sdk/dotnet.ios/barcode-capture/api.html) |

> MAUI inherits the per-TFM .NET API. There is no separate "dotnet.maui" doc filter — pick the .NET Android or .NET iOS API reference depending on which TFM you're debugging against. The MAUI-specific surface is just the XAML control (`<scandit:BarcodeCountView>`), the builder extensions, and the `HandlerChanged` wiring. The cross-platform `BarcodeCount` / `BarcodeCountSettings` / session / capture-list / feedback APIs are identical between the two TFMs.

## API surface this skill covers

All classes documented with `:available: dotnet.android` and / or `:available: dotnet.ios` in the official RST docs (`docs/source/barcode-capture/api/barcode-count*.rst` and `api/ui/barcode-count-*.rst`) are addressed in [references/integration.md](references/integration.md), plus the MAUI-specific surface:

- **Cross-platform Count API** (same as the per-TFM skills):
  - `BarcodeCount` — static `Create(DataCaptureContext?, BarcodeCountSettings)` / `Create(BarcodeCountSettings)`, `Context` (get), `Feedback` (get/set), `Enabled` (get/set), static `RecommendedCameraSettings`, `ApplySettingsAsync(BarcodeCountSettings)` → `Task`, `AddListener` / `RemoveListener(IBarcodeCountListener)`, `Reset()`, `StartScanningPhase()`, `EndScanningPhase()`, `SetBarcodeCountCaptureList(BarcodeCountCaptureList)`, `SetAdditionalBarcodes(IList<Barcode>)`, `ClearAdditionalBarcodes()`, `event EventHandler<BarcodeCountEventArgs> Scanned`, `Dispose()`.
  - `BarcodeCountSettings` — `new BarcodeCountSettings()`, `EnableSymbology(Symbology, bool)`, `EnableSymbologies(ICollection<Symbology>)`, `GetSymbologySettings(Symbology)`, `EnabledSymbologies` (get), `FilterSettings` (get), `ExpectsOnlyUniqueBarcodes` (get/set), `DisableModeWhenCaptureListCompleted` (get/set), `MappingEnabled` (get/set), property bag.
  - `IBarcodeCountListener` — `OnScan`, `OnObservationStarted`, `OnObservationStopped`.
  - `BarcodeCountSession` — `RecognizedBarcodes` (`IList<Barcode>`), `AdditionalBarcodes` (`IList<Barcode>`), `FrameSequenceId` (`long`), `Reset()`, `GetSpatialMap()` / `GetSpatialMap(int, int)`.
  - `BarcodeCountEventArgs` — `BarcodeCount`, `Session`, `FrameData`.
  - Capture list (receiving): `BarcodeCountCaptureList.Create(IBarcodeCountCaptureListListener, IList<TargetBarcode>)`; `TargetBarcode.Create(string, int)`; `IBarcodeCountCaptureListListener`; `BarcodeCountCaptureListSession` (`CorrectBarcodes`, `WrongBarcodes`, `MissingBarcodes`, `AdditionalBarcodes`, `AcceptedBarcodes`, `RejectedBarcodes`).
  - Spatial map: `BarcodeSpatialGrid`, `BarcodeSpatialGridElement`.
  - `BarcodeCountFeedback` — `new BarcodeCountFeedback()` (silent), static `DefaultFeedback`, `Success` / `Failure`.
  - Status mode: `IBarcodeCountStatusProvider`, `IBarcodeCountStatusProviderCallback`, `BarcodeCountStatus` enum, `BarcodeCountStatusItem.Create(...)`, `BarcodeCountStatusResultSuccess/Error/Abort.Create(...)`.
  - `TrackedBarcode` (`Scandit.DataCapture.Barcode.Batch.Data`) — used by `IBarcodeCountViewListener`, the status API, and the capture-list session.

- **MAUI-only surface** (assembly `ScanditBarcodeCaptureMaui`, namespace `Scandit.DataCapture.Barcode.Count.UI.Maui`):
  - `MauiAppBuilderExtensions.UseScanditCore(this MauiAppBuilder)` — no lambda needed for a Count-only app.
  - `MauiAppBuilderExtensions.UseScanditBarcode(this MauiAppBuilder, Action<ConfigureBarcode>)` — the lambda exposes `AddBarcodeCountView()`.
  - `Scandit.DataCapture.Barcode.Count.UI.Maui.BarcodeCountView` — the MAUI `View` control. Bindable properties: `DataCaptureContext` (OneTime), `BarcodeCount` (OneTime), `ViewStyle` (OneTime, default `Dot`), plus `ShouldShowListButton` / `ShouldShowExitButton` / `ShouldShowShutterButton` / `ShouldShowFloatingShutterButton` / `ShouldShowSingleScanButton` / `ShouldShowClearHighlightsButton` / `ShouldShowStatusModeButton` / `ShouldShowUserGuidanceView` / `ShouldShowHints` / `ShouldShowToolbar` / `ShouldShowScanAreaGuides` / `ShouldShowListProgressBar` / `ShouldShowTorchControl`, `ShouldDisableModeOnExitButtonTapped`, `TapToUncountEnabled`, `TorchControlPosition` (`Anchor`), `RecognizedBrush` / `NotInListBrush` / `AcceptedBrush` / `RejectedBrush` (and static `Default*Brush`), and a large set of accessibility / button-text bindable strings. Non-bindable members: `Listener` (`IBarcodeCountViewListener?`), `BarcodeNotInListActionSettings` (get), `SetToolbarSettings`, `ClearHighlights()`, `SetStatusProvider`, `SetBrushForRecognizedBarcode`/`*NotInList`/`*Accepted`/`*Rejected`, `EnableHardwareTrigger(int?)` + static `HardwareTriggerSupported` (Android only), `HardwareTriggerEnabled` (iOS only), events `ExitButtonTapped` / `ListButtonTapped` / `SingleScanButtonTapped`, `HandlerReady` / `ClearPendingCommands()`.
  - `BarcodeCountViewStyle` enum — `Icon`, `Dot`.
  - Event args (namespace `Scandit.DataCapture.Barcode.Count.UI`): `ExitButtonTappedEventArgs`, `ListButtonTappedEventArgs`, `SingleScanButtonTappedEventArgs`.

### Documented for other platforms but NOT in the .NET binding — do not use

- **`BarcodeCountMappingFlowSettings`** / mapping-flow configuration — not surfaced in the .NET binding. Mapping in .NET is limited to `BarcodeCountSettings.MappingEnabled` + `BarcodeCountSession.GetSpatialMap()`.
- **`BarcodeCountSessionSnapshot`** — no .NET equivalent.
