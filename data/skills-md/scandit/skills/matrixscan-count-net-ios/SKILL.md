---
name: matrixscan-count-net-ios
description: MatrixScan Count (BarcodeCount) in .NET for iOS projects (net*-ios, Scandit.DataCapture.Barcode NuGet, non-MAUI) — counting/receiving barcodes in bulk with BarcodeCountView in a UIViewController, capture/receiving lists, spatial map, explicitly managed camera. For MAUI apps use matrixscan-count-net-maui. Use for integration, settings configuration, result handling, UI customization, SDK version migration, or troubleshooting counting workflows.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Count .NET for iOS Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs, and the .NET binding differs from the Swift/Objective-C native SDK and from the Android .NET binding in several places: factories instead of constructors, PascalCase members, C# events alongside listener interfaces, an explicitly-managed camera, and a `CGRect`-based view factory.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

.NET-iOS-specific gotchas worth flagging (the places people get it wrong by pattern-matching from MatrixScan AR, the native Swift SDK, the Android .NET binding, or MAUI):

- This skill targets the **non-MAUI** .NET for iOS workload (project `<TargetFramework>net10.0-ios</TargetFramework>` or similar, no `<UseMaui>` flag). For MAUI apps, use a MAUI-targeted skill instead — there `BarcodeCountView` is hosted as a XAML element and wired through `HandlerChanged`, which is completely different. **The official iOS Get Started page mixes in MAUI (XAML / `Scandit.DataCapture.Barcode.Maui`) snippets — ignore those for a non-MAUI project.**
- **`BarcodeCount` is created with a FACTORY, not `new`**: `BarcodeCount.Create(dataCaptureContext, settings)` (there is also a `BarcodeCount.Create(settings)` overload with no context). `new BarcodeCount(...)` is a compile error — the constructor is private. `BarcodeCountSettings` **does** use a plain `new BarcodeCountSettings()`.
- **`BarcodeCountView.Create(CGRect frame, DataCaptureContext, BarcodeCount [, BarcodeCountViewStyle])`** takes a **`CGRect` frame** as its first argument — typically `this.View!.Bounds`. It does **not** take an Android `Context` (that's the Android binding) and it is **not** a parent view. The style overload takes `BarcodeCountViewStyle.Icon` (default look) or `BarcodeCountViewStyle.Dot`.
- **`BarcodeCountView` IS a real `UIView`** (via `public static implicit operator View(BarcodeCountView)`, where `View` resolves to `UIKit.UIView` on iOS). You add it to the hierarchy yourself: `this.View.AddSubview(barcodeCountView)`, and usually set `AutoresizingMask = FlexibleWidth | FlexibleHeight`.
- **The camera is explicitly managed by you — `BarcodeCountView` does NOT own it.** You must: get `Camera.GetDefaultCamera()` (or the `Camera.DefaultCamera` property), apply `BarcodeCount.RecommendedCameraSettings` with `camera.ApplySettingsAsync(...)`, call `dataCaptureContext.SetFrameSourceAsync(camera)`, and toggle the camera yourself with `camera.SwitchToDesiredStateAsync(FrameSourceState.On / .Standby / .Off)` in `ViewWillAppear` / `ViewWillDisappear`. There is no `barcodeCountView.OnResume()` / `Start()` / `Stop()` — those don't exist. (iOS does have `PrepareScanning`/`StopScanning` on the view, but the camera frame-source toggle is the normal lifecycle handle.)
- **iOS lifecycle is `UIViewController`, not an Android Activity.** Toggle the camera and `barcodeCount.Enabled` in `ViewWillAppear`/`ViewWillDisappear`. iOS additionally has **`FrameSourceState.Standby`** — a lighter "pause" used when navigating to another screen *within* the app (keeps the camera warm), versus `FrameSourceState.Off` when actually backgrounding.
- **`barcodeCount.Enabled` (get/set `bool`) must be set to `true`** for frames to be processed. Set it `true` in `ViewWillAppear`.
- **`IBarcodeCountListener` has THREE methods:** `OnScan(BarcodeCount, BarcodeCountSession, IFrameData)`, `OnObservationStarted(BarcodeCount)`, `OnObservationStopped(BarcodeCount)`. The idiomatic C# alternative is the **`barcodeCount.Scanned` event** (`EventHandler<BarcodeCountEventArgs>`), which corresponds to `OnScan` only.
- **`Scanned` / `OnScan` fires once per scan phase, on a background thread.** Copy the barcodes you need out of the session immediately (`session.RecognizedBarcodes.ToList()`); the `BarcodeCountSession` is **not** valid outside the callback. Dispatch UI updates onto the main thread with `UIApplication.SharedApplication.InvokeOnMainThread(...)` (or `DispatchQueue.MainQueue.DispatchAsync(...)`) — **not** Android's `RunOnUiThread`.
- **`BarcodeCountSession` exposes `RecognizedBarcodes` and `AdditionalBarcodes` as `IList<Barcode>`** — plain decoded barcodes, not tracked-barcode deltas. Also `FrameSequenceId`, `Reset()`, and `GetSpatialMap()`.
- **`BarcodeCountFeedback` uses `Success` and `Failure`** (`Core.Common.Feedback.Feedback`). The empty constructor `new BarcodeCountFeedback()` is silent; the static `BarcodeCountFeedback.DefaultFeedback` (a **property**, not a method) restores defaults.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Upce`, `Symbology.Code128`, `Symbology.Code39`, `Symbology.Qr`, `Symbology.DataMatrix`, `Symbology.InterleavedTwoOfFive`. They are **not** the Swift `.ean13UPCA` / native style.
- **List / Exit / Single-Scan buttons are surfaced as C# events** on `BarcodeCountView`: `ListButtonTapped` (`ListButtonTappedEventArgs`), `ExitButtonTapped` (`ExitButtonTappedEventArgs`), `SingleScanButtonTapped` (`SingleScanButtonTappedEventArgs`) — each exposes `.View`. Brush/tap customization is the `Listener` property (`IBarcodeCountViewListener`), a separate concern from these events.
- **Capture list (receiving) uses factories:** `BarcodeCountCaptureList.Create(listener, IList<TargetBarcode>)` and `TargetBarcode.Create(data, quantity)`. Apply it with `barcodeCount.SetBarcodeCountCaptureList(list)`. The listener `IBarcodeCountCaptureListListener` has `OnObservationStarted()`, `OnObservationStopped()`, `OnCaptureListSessionUpdated(session)`, `OnCaptureListCompleted(session)`.
- **`SDK 8.0+ requires explicit initialization.`** Call `ScanditCaptureCore.Initialize()` + `ScanditBarcodeCapture.Initialize()` in `AppDelegate.FinishedLaunching` (`application:didFinishLaunchingWithOptions:`) before any Scandit code runs. Without this, the first `DataCaptureContext.ForLicenseKey(...)` / `BarcodeCount.Create(...)` call crashes at launch because the DI container has no registrations. **Not required on 6.x / 7.x.** See [references/integration.md](references/integration.md) for the full `AppDelegate.cs` template.
- The NuGet packages are `Scandit.DataCapture.Core` and `Scandit.DataCapture.Barcode`. No separate `*.Maui` packages here — those are only for MAUI projects. **Do not guess the version from training data** — fetch the latest stable from `https://www.nuget.org/packages/Scandit.DataCapture.Barcode/` via `WebFetch` before pinning. Inventing a non-existent version causes `dotnet restore` to fail with `Unable to find package Scandit.DataCapture.Core with version (>= …)`. See [references/integration.md](references/integration.md) Step 0.
- **Camera permission is handled by iOS automatically** via the `NSCameraUsageDescription` key in `Info.plist`. The OS shows the permission prompt the first time the camera switches on. There is **no** runtime-permission helper class (that's the Android binding's `CameraPermissionActivity`). If `NSCameraUsageDescription` is missing, the app crashes when the camera starts.
- **iOS `SupportedOSPlatformVersion` must be ≥ `15.0`.** Set it in the `.csproj` (the Scandit iOS framework's minimum deployment target). The matching `MinimumOSVersion` goes in `Info.plist`.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeCount from scratch, configuring settings, hosting the BarcodeCountView, wiring camera lifecycle, handling scan results, storing scanned barcodes, capture/receiving lists, the spatial map, customizing feedback, List/Exit/SingleScan taps, brushes, status mode, the not-in-list action, or the hardware trigger** (e.g. "add MatrixScan Count to my .NET iOS app", "count barcodes in C#", "store the scanned barcodes when the list button is tapped", "check scans against an expected list", "make the beep silent", "use the Dot style", "show a not-in-list action") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing MatrixScan Count integration** (e.g. "upgrade from v7 to v8", "bump the Scandit .NET SDK to v8", "what changed between SDK versions for BarcodeCount") → read [references/migration.md](references/migration.md) and follow the instructions there.

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
| Get Started | [Get Started (.NET for iOS)](https://docs.scandit.com/sdks/net/ios/matrixscan-count/get-started/) |
| Advanced topics (capture list, status mode, brushes, toolbar, filtering, strap mode) | [Advanced Configurations](https://docs.scandit.com/sdks/net/ios/matrixscan-count/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/net/ios/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/ios/migrate-7-to-8/) |
| Full API reference | [BarcodeCount API (.NET iOS)](https://docs.scandit.com/data-capture-sdk/dotnet.ios/barcode-capture/api.html) |

## API surface this skill covers

All classes documented with `:available: dotnet.ios` in the official RST docs (`docs/source/barcode-capture/api/barcode-count*.rst` and `api/ui/barcode-count-*.rst`) are addressed in [references/integration.md](references/integration.md):

- `BarcodeCount` — static `Create(DataCaptureContext?, BarcodeCountSettings)` / `Create(BarcodeCountSettings)`, `Context` (get), `Feedback` (get/set), `Enabled` (get/set), static `RecommendedCameraSettings`, `ApplySettingsAsync(BarcodeCountSettings)` → `Task`, `AddListener` / `RemoveListener(IBarcodeCountListener)`, `Reset()`, `StartScanningPhase()`, `EndScanningPhase()`, `SetBarcodeCountCaptureList(BarcodeCountCaptureList)`, `SetAdditionalBarcodes(IList<Barcode>)`, `ClearAdditionalBarcodes()`, `event EventHandler<BarcodeCountEventArgs> Scanned`, `Dispose()`.
- `BarcodeCountSettings` — `new BarcodeCountSettings()`, `EnableSymbology(Symbology, bool)`, `EnableSymbologies(ICollection<Symbology>)`, `GetSymbologySettings(Symbology)`, `EnabledSymbologies` (get), `FilterSettings` (get, `BarcodeFilterSettings`), `ExpectsOnlyUniqueBarcodes` (get/set), `DisableModeWhenCaptureListCompleted` (get/set), `MappingEnabled` (get/set), `SetProperty`/`GetProperty`/`GetProperty<T>`/`TryGetProperty<T>`, `Dispose`.
- `IBarcodeCountListener` — `OnScan(BarcodeCount, BarcodeCountSession, IFrameData)`, `OnObservationStarted(BarcodeCount)`, `OnObservationStopped(BarcodeCount)`.
- `BarcodeCountSession` — `RecognizedBarcodes` (`IList<Barcode>`), `AdditionalBarcodes` (`IList<Barcode>`), `FrameSequenceId` (`long`), `Reset()`, `GetSpatialMap()` / `GetSpatialMap(int rows, int cols)` → `BarcodeSpatialGrid?`.
- `BarcodeCountEventArgs` — `BarcodeCount`, `Session`, `FrameData`.
- `Coordinate2d` — `new Coordinate2d(int x, int y)`, `X`, `Y`.
- Capture list (receiving): `BarcodeCountCaptureList.Create(IBarcodeCountCaptureListListener, IList<TargetBarcode>)`; `TargetBarcode.Create(string data, int quantity)` with `Data` / `Quantity`; `IBarcodeCountCaptureListListener` (`OnObservationStarted`, `OnObservationStopped`, `OnCaptureListSessionUpdated`, `OnCaptureListCompleted`); `BarcodeCountCaptureListSession` (`CorrectBarcodes`, `WrongBarcodes`, `MissingBarcodes`, `AdditionalBarcodes`, `AcceptedBarcodes`, `RejectedBarcodes`).
- Spatial map: `BarcodeSpatialGrid` (`Rows()`, `Columns()`, `ElementAt(row, col)`, `Row(i)`, `Column(i)`, `CoordinatesForElement(element)`); `BarcodeSpatialGridElement` (`MainBarcode`, `SubBarcode`).
- `BarcodeCountFeedback` — `new BarcodeCountFeedback()` (silent), static `DefaultFeedback`, `Success` / `Failure` (`Core.Common.Feedback.Feedback`), `Dispose`.
- `BarcodeCountView` — static `Create(CGRect, DataCaptureContext, BarcodeCount)` / `Create(CGRect, DataCaptureContext, BarcodeCount, BarcodeCountViewStyle)`; implicit conversion to `UIKit.UIView`; `Style` (get); `Listener` (`IBarcodeCountViewListener?`); many `ShouldShow*` toggles (`ShouldShowListButton`, `ShouldShowExitButton`, `ShouldShowShutterButton`, `ShouldShowFloatingShutterButton`, `ShouldShowSingleScanButton`, `ShouldShowClearHighlightsButton`, `ShouldShowStatusModeButton`, `ShouldShowUserGuidanceView`, `ShouldShowHints`, `ShouldShowToolbar`, `ShouldShowScanAreaGuides`, `ShouldShowListProgressBar`, `ShouldShowTorchControl`); `ShouldDisableModeOnExitButtonTapped`, `TapToUncountEnabled`, `TorchControlPosition` (`Anchor`); brush properties (`RecognizedBrush`, `NotInListBrush`, `AcceptedBrush`, `RejectedBrush`) and static default brushes; `FilterSettings` (`IBarcodeFilterHighlightSettings?`); `BarcodeNotInListActionSettings` (get); customization text properties; **iOS-only** `HardwareTriggerEnabled` (get/set `bool`), `PrepareScanning(DataCaptureContext)`, `StopScanning()`, and `*AccessibilityLabel` / `*AccessibilityHint` string properties; `SetToolbarSettings`, `ClearHighlights()`, `SetStatusProvider`, `SetBrushForRecognizedBarcode`/`*NotInList`/`*Accepted`/`*Rejected`; `event ExitButtonTapped` / `ListButtonTapped` / `SingleScanButtonTapped`; `Dispose`.
- `BarcodeCountViewStyle` enum — `Icon`, `Dot`.
- `IBarcodeCountViewListener` — brush-for callbacks (`BrushForRecognizedBarcode`, `*NotInList`, `*Accepted`, `*Rejected`) and tap callbacks (`OnRecognizedBarcodeTapped`, `OnFilteredBarcodeTapped`, `OnRecognizedBarcodeNotInListTapped`, `OnAcceptedBarcodeTapped`, `OnRejectedBarcodeTapped`). **On iOS the interface has exactly these 9 methods — there is no `OnCaptureListCompleted` (that is Android-only).**
- Tap event args: `ExitButtonTappedEventArgs`, `ListButtonTappedEventArgs`, `SingleScanButtonTappedEventArgs` — each with `View`.
- `BarcodeCountToolbarSettings` — text strings for the audio/vibration/strap-mode/color-scheme toggles, plus iOS-only `*AccessibilityLabel` / `*AccessibilityHint`.
- `BarcodeCountNotInListActionSettings` (from `barcodeCountView.BarcodeNotInListActionSettings`) — `Enabled`, accept/reject/cancel button text, `BarcodeAcceptedHint`, `BarcodeRejectedHint`, plus iOS-only `*AccessibilityLabel` / `*AccessibilityHint`.
- Status mode: `IBarcodeCountStatusProvider` (`OnStatusRequested(IList<TrackedBarcode>, IBarcodeCountStatusProviderCallback)`), `IBarcodeCountStatusProviderCallback` (`OnStatusReady(IBarcodeCountStatusResult)`), `BarcodeCountStatus` enum (`None`, `NotAvailable`, `Expired`, `Fragile`, `QualityCheck`, `LowStock`, `Wrong`), `BarcodeCountStatusItem.Create(TrackedBarcode, BarcodeCountStatus)`, `IBarcodeCountStatusResult` with factories `BarcodeCountStatusResultSuccess.Create(...)`, `BarcodeCountStatusResultError.Create(...)`, `BarcodeCountStatusResultAbort.Create(...)`.
- `TrackedBarcode` (in `Scandit.DataCapture.Barcode.Batch.Data`) — `Barcode`, `Identifier`, `Location`. Used by `IBarcodeCountViewListener`, the status API, and the capture-list session.

### iOS vs Android binding differences (do not cross-pollinate)

- **View factory first argument**: iOS `BarcodeCountView.Create(CGRect frame, …)`; Android `BarcodeCountView.Create(Context context, …)`. Using a `Context` on iOS — or `View.Bounds` on Android — will not compile.
- **Hardware trigger**: iOS exposes `barcodeCountView.HardwareTriggerEnabled` (`bool` get/set). Android exposes `barcodeCountView.EnableHardwareTrigger(int? keyCode)` + static `BarcodeCountView.HardwareTriggerSupported`. **`EnableHardwareTrigger` / `HardwareTriggerSupported` do not exist on iOS.**
- **`PrepareScanning(context)` / `StopScanning()`** exist only on the iOS view.
- **Accessibility text**: iOS uses `*AccessibilityLabel` / `*AccessibilityHint`; Android uses `*ContentDescription`.
- **`IBarcodeCountViewListener.OnCaptureListCompleted(view)`** exists only on Android.

### Documented for other platforms but NOT on `dotnet.ios` — do not use

- **`BarcodeCountMappingFlowSettings`** and the mapping-flow configuration class — not surfaced in the .NET binding. Mapping in .NET is limited to `BarcodeCountSettings.MappingEnabled` + `BarcodeCountSession.GetSpatialMap()`.
- **`BarcodeCountSessionSnapshot`** — no .NET equivalent.
- **Clustering** (`ClusteringMode`) — described on the iOS Advanced page but not exposed as a configurable enum in the .NET binding. Do not introduce a `ClusteringMode` API; if a user asks, fetch the API reference to confirm before suggesting anything.
