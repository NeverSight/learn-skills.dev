---
name: matrixscan-count-net-android
description: MatrixScan Count (BarcodeCount) in .NET for Android projects (net*-android, Scandit.DataCapture.Barcode NuGet, non-MAUI) — counting/receiving barcodes in bulk with BarcodeCountView, capture/receiving lists, spatial map, explicitly managed camera. For MAUI apps use matrixscan-count-net-maui. Use for integration, settings configuration, result handling, UI customization, SDK version migration, or troubleshooting counting workflows.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Count .NET for Android Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs, and the .NET binding differs from the Kotlin/Java and iOS native SDKs in several places: factories instead of constructors, PascalCase members, C# events alongside listener interfaces, an explicitly-managed camera, etc.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

.NET-Android-specific gotchas worth flagging (and the places people get it wrong by pattern-matching from MatrixScan AR or the Kotlin SDK):

- This skill targets the **non-MAUI** .NET for Android workload (project `<TargetFramework>net10.0-android</TargetFramework>` or similar, no `<UseMaui>` flag). For MAUI apps, use a MAUI-targeted skill instead — `BarcodeCountView` is hosted as a XAML element there and the lifecycle is wired through handlers, which is completely different.
- **`BarcodeCount` is created with a FACTORY, not `new`**: `BarcodeCount.Create(dataCaptureContext, settings)` (there is also a `BarcodeCount.Create(settings)` overload with no context). `new BarcodeCount(...)` is a compile error — the constructor is private. `BarcodeCountSettings` **does** use a plain `new BarcodeCountSettings()`. (Note this is the opposite of MatrixScan AR, where `BarcodeAr` uses `new` and the *view* uses a factory.)
- **The camera is explicitly managed by you — `BarcodeCountView` does NOT own it.** This is the single biggest difference from MatrixScan AR. You must: get `Camera.GetDefaultCamera(BarcodeCount.RecommendedCameraSettings)` (or `Camera.DefaultCamera` then `camera.ApplySettingsAsync(...)`), call `dataCaptureContext.SetFrameSourceAsync(camera)`, and toggle the camera yourself with `camera.SwitchToDesiredStateAsync(FrameSourceState.On)` / `FrameSourceState.Off` in the activity's `OnResume` / `OnPause`. There is no `barcodeCountView.OnResume()` / `OnPause()` / `Start()` / `Stop()` — those are MatrixScan AR methods and do not exist on `BarcodeCountView`.
- **`barcodeCount.Enabled` (get/set `bool`) must be set to `true`** for frames to be processed. Set it `true` in `OnResume` and (optionally) `false` in `OnPause`. `BarcodeAr` has no such toggle; `BarcodeCount` does.
- **`BarcodeCountView.Create(Context, DataCaptureContext, BarcodeCount [, BarcodeCountViewStyle])`** takes the Android **`Context`** (the activity) as its first argument — **not** a parentView/ViewGroup (that's the AR signature). The style overload takes `BarcodeCountViewStyle.Icon` (default look) or `BarcodeCountViewStyle.Dot`.
- **`BarcodeCountView` IS a real Android `View`** (via `public static implicit operator View(BarcodeCountView)`). You add it to the hierarchy yourself: `container.AddView(barcodeCountView)`. This is the opposite of `BarcodeArView`, which is *not* a View and auto-attaches itself. Do **not** look for an auto-attach `parentView` argument on `BarcodeCountView.Create`.
- **`IBarcodeCountListener` has THREE methods:** `OnScan(BarcodeCount, BarcodeCountSession, IFrameData)`, `OnObservationStarted(BarcodeCount)`, `OnObservationStopped(BarcodeCount)`. (MatrixScan AR's listener has only one — do not assume parity.) The idiomatic C# alternative is the **`barcodeCount.Scanned` event** (`EventHandler<BarcodeCountEventArgs>`), which corresponds to `OnScan` only.
- **`Scanned` / `OnScan` fires once per scan phase, on a background thread.** Copy the barcodes you need out of the session immediately (`session.RecognizedBarcodes.ToList()`); the `BarcodeCountSession` is **not** valid outside the callback. Dispatch UI updates via `RunOnUiThread(...)`.
- **`BarcodeCountSession` exposes `RecognizedBarcodes` and `AdditionalBarcodes` as `IList<Barcode>`** — plain decoded barcodes, not tracked-barcode deltas. There is no `AddedTrackedBarcodes` / `RemovedTrackedBarcodes` on this session (that's the AR/Batch session). Also `FrameSequenceId`, `Reset()`, and `GetSpatialMap()`.
- **`BarcodeCountFeedback` uses `Success` and `Failure`** (`Core.Common.Feedback.Feedback`), not `Scanned` / `Tapped` (those are AR). The empty constructor `new BarcodeCountFeedback()` is silent on both; the static `BarcodeCountFeedback.DefaultFeedback` (a **property**, not a method) restores defaults.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Upce`, `Symbology.Code128`, `Symbology.Code39`, `Symbology.Qr`, `Symbology.DataMatrix`, `Symbology.InterleavedTwoOfFive`. They are **not** the Kotlin underscore style (`EAN13_UPCA`).
- **List / Exit / Single-Scan buttons are surfaced as C# events** on `BarcodeCountView`: `ListButtonTapped` (`ListButtonTappedEventArgs`), `ExitButtonTapped` (`ExitButtonTappedEventArgs`), `SingleScanButtonTapped` (`SingleScanButtonTappedEventArgs`) — each exposes `.View`. Brush/tap customization is the `Listener` property (`IBarcodeCountViewListener`), which is a separate concern from these events.
- **Capture list (receiving) uses factories:** `BarcodeCountCaptureList.Create(listener, IList<TargetBarcode>)` and `TargetBarcode.Create(data, quantity)`. Apply it with `barcodeCount.SetBarcodeCountCaptureList(list)`. The listener `IBarcodeCountCaptureListListener` has `OnObservationStarted()`, `OnObservationStopped()`, `OnCaptureListSessionUpdated(session)`, `OnCaptureListCompleted(session)`.
- **`SDK 8.0+ requires explicit initialization.`** Subclass `Android.App.Application`, decorate with `[Application]`, and call `ScanditCaptureCore.Initialize()` + `ScanditBarcodeCapture.Initialize()` in `OnCreate()` before any Scandit code runs. Without this, the first `DataCaptureContext.ForLicenseKey(...)` / `BarcodeCount.Create(...)` call crashes at launch because the DI container has no registrations. **Not required on 6.x / 7.x.** See [references/integration.md](references/integration.md) for the full `MainApplication.cs` template.
- The NuGet packages are `Scandit.DataCapture.Core` and `Scandit.DataCapture.Barcode`. No separate `*.Maui` packages here — those are only for MAUI projects. **Do not guess the version from training data** — fetch the latest stable from `https://www.nuget.org/packages/Scandit.DataCapture.Barcode/` via `WebFetch` before pinning. Inventing a non-existent version (e.g. `8.13.0` when only `8.4.0` is published) causes `dotnet restore` to fail with `Unable to find package Scandit.DataCapture.Core with version (>= …)`. See [references/integration.md](references/integration.md) Step 0.
- **Android `SupportedOSPlatformVersion` must be ≥ `24`.** Set it in the `.csproj`. Lower values fail the build with `uses-sdk:minSdkVersion 21 cannot be smaller than version 24 declared in library`.
- **Do not declare `<activity>` elements for `[Activity]`-decorated classes in `AndroidManifest.xml`.** The `[Activity(MainLauncher = true, ...)]` attribute is the canonical registration mechanism in .NET for Android — the build merges a correctly-named entry into the final manifest. A manual `<activity android:name=".MainActivity">` resolves against `<ApplicationId>` and **won't match** the generated class, producing `ClassNotFoundException` at launch. Only add to the manifest the elements the skill explicitly asks for (`<uses-feature>`, `<uses-permission>`).
- The runtime camera permission helper (`CameraPermissionActivity`) inherits from `AppCompatActivity`, so `Xamarin.AndroidX.AppCompat` must be in the `.csproj`. When pinning the version, pick the highest available including the Xamarin patch revision (e.g. `1.7.0.5`, not bare `1.7.0`) — the `.X` suffix marks Xamarin-binding-level updates and carries critical transitive-dep fixes.
- **The activity needs a `Theme.AppCompat` descendant** (because it inherits from `AppCompatActivity`). Set `android:theme` on `<application>` in the manifest (the sample uses `@style/AppTheme`, an AppCompat descendant) or `Theme = "@style/Theme.AppCompat..."` on the `[Activity]` attribute. Without it, `SetContentView` throws `IllegalStateException: You need to use a Theme.AppCompat theme (or descendant) with this activity` at launch.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeCount from scratch, configuring settings, hosting the BarcodeCountView, wiring camera lifecycle, handling scan results, storing scanned barcodes, capture/receiving lists, the spatial map, customizing feedback, List/Exit/SingleScan taps, brushes, status mode, or the not-in-list action** (e.g. "add MatrixScan Count to my .NET Android app", "count barcodes in C#", "store the scanned barcodes when the list button is tapped", "check scans against an expected list", "make the beep silent", "use the Dot style", "show a not-in-list action") → read [references/integration.md](references/integration.md) and follow the instructions there.
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
| Get Started | [Get Started (.NET for Android)](https://docs.scandit.com/sdks/net/android/matrixscan-count/get-started/) |
| Advanced topics (capture list, status mode, brushes, toolbar, hardware trigger) | [Advanced Configurations](https://docs.scandit.com/sdks/net/android/matrixscan-count/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/net/android/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/android/migrate-7-to-8/) |
| Full API reference | [BarcodeCount API (.NET Android)](https://docs.scandit.com/data-capture-sdk/dotnet.android/barcode-capture/api.html) |

## API surface this skill covers

All classes documented with `:available: dotnet.android` in the official RST docs (`docs/source/barcode-capture/api/barcode-count*.rst` and `api/ui/barcode-count-*.rst`) are addressed in [references/integration.md](references/integration.md):

- `BarcodeCount` — static `Create(DataCaptureContext?, BarcodeCountSettings)` / `Create(BarcodeCountSettings)`, `Context` (get), `Feedback` (get/set), `Enabled` (get/set), static `RecommendedCameraSettings`, `ApplySettingsAsync(BarcodeCountSettings)` → `Task`, `AddListener` / `RemoveListener(IBarcodeCountListener)`, `Reset()`, `StartScanningPhase()`, `EndScanningPhase()`, `SetBarcodeCountCaptureList(BarcodeCountCaptureList)`, `SetAdditionalBarcodes(IList<Barcode>)`, `ClearAdditionalBarcodes()`, `event EventHandler<BarcodeCountEventArgs> Scanned`, `Dispose()`.
- `BarcodeCountSettings` — `new BarcodeCountSettings()`, `EnableSymbology(Symbology, bool)`, `EnableSymbologies(ICollection<Symbology>)`, `GetSymbologySettings(Symbology)`, `EnabledSymbologies` (get), `FilterSettings` (get, `BarcodeFilterSettings`), `ExpectsOnlyUniqueBarcodes` (get/set), `DisableModeWhenCaptureListCompleted` (get/set), `MappingEnabled` (get/set), `SetProperty`/`GetProperty`/`GetProperty<T>`/`TryGetProperty<T>`, `Dispose`.
- `IBarcodeCountListener` — `OnScan(BarcodeCount, BarcodeCountSession, IFrameData)`, `OnObservationStarted(BarcodeCount)`, `OnObservationStopped(BarcodeCount)`.
- `BarcodeCountSession` — `RecognizedBarcodes` (`IList<Barcode>`), `AdditionalBarcodes` (`IList<Barcode>`), `FrameSequenceId` (`long`), `Reset()`, `GetSpatialMap()` / `GetSpatialMap(int rows, int cols)` → `BarcodeSpatialGrid?`.
- `BarcodeCountEventArgs` — `BarcodeCount`, `Session`, `FrameData`.
- `Coordinate2d` — `new Coordinate2d(int x, int y)`, `X`, `Y`.
- Capture list (receiving): `BarcodeCountCaptureList.Create(IBarcodeCountCaptureListListener, IList<TargetBarcode>)`; `TargetBarcode.Create(string data, int quantity)` with `Data` / `Quantity`; `IBarcodeCountCaptureListListener` (`OnObservationStarted`, `OnObservationStopped`, `OnCaptureListSessionUpdated`, `OnCaptureListCompleted`); `BarcodeCountCaptureListSession` (`CorrectBarcodes`, `WrongBarcodes`, `MissingBarcodes`, `AdditionalBarcodes`, `AcceptedBarcodes`, `RejectedBarcodes`).
- Spatial map: `BarcodeSpatialGrid` (`Rows()`, `Columns()`, `ElementAt(row, col)`, `Row(i)`, `Column(i)`, `CoordinatesForElement(element)`); `BarcodeSpatialGridElement` (`MainBarcode`, `SubBarcode`).
- `BarcodeCountFeedback` — `new BarcodeCountFeedback()` (silent), static `DefaultFeedback`, `Success` / `Failure` (`Core.Common.Feedback.Feedback`), `Dispose`.
- `BarcodeCountView` — static `Create(Context, DataCaptureContext, BarcodeCount)` / `Create(Context, DataCaptureContext, BarcodeCount, BarcodeCountViewStyle)`; implicit conversion to `Android.Views.View`; `Style` (get); `Listener` (`IBarcodeCountViewListener?`); many `ShouldShow*` toggles (`ShouldShowListButton`, `ShouldShowExitButton`, `ShouldShowShutterButton`, `ShouldShowFloatingShutterButton`, `ShouldShowSingleScanButton`, `ShouldShowClearHighlightsButton`, `ShouldShowStatusModeButton`, `ShouldShowUserGuidanceView`, `ShouldShowHints`, `ShouldShowToolbar`, `ShouldShowScanAreaGuides`, `ShouldShowListProgressBar`, `ShouldShowTorchControl`); `ShouldDisableModeOnExitButtonTapped`, `TapToUncountEnabled`, `TorchControlPosition` (`Anchor`); brush properties (`RecognizedBrush`, `NotInListBrush`, `AcceptedBrush`, `RejectedBrush`) and static default brushes; `BarcodeNotInListActionSettings` (get); customization text properties; `EnableHardwareTrigger(int?)`, static `HardwareTriggerSupported`; `SetToolbarSettings`, `ClearHighlights()`, `SetStatusProvider`, `SetBrushForRecognizedBarcode`/`*NotInList`/`*Accepted`/`*Rejected`; `event ExitButtonTapped` / `ListButtonTapped` / `SingleScanButtonTapped`; `Dispose`.
- `BarcodeCountViewStyle` enum — `Icon`, `Dot`.
- `IBarcodeCountViewListener` — brush-for callbacks (`BrushForRecognizedBarcode`, `*NotInList`, `*Accepted`, `*Rejected`) and tap callbacks (`OnRecognizedBarcodeTapped`, `OnFilteredBarcodeTapped`, `OnRecognizedBarcodeNotInListTapped`, `OnAcceptedBarcodeTapped`, `OnRejectedBarcodeTapped`, and Android-only `OnCaptureListCompleted`).
- Tap event args: `ExitButtonTappedEventArgs`, `ListButtonTappedEventArgs`, `SingleScanButtonTappedEventArgs` — each with `View`.
- `BarcodeCountToolbarSettings` — text/content-description strings for the audio/vibration/strap-mode/color-scheme toggles.
- `BarcodeCountNotInListActionSettings` (from `barcodeCountView.BarcodeNotInListActionSettings`) — `Enabled`, accept/reject/cancel button text + content descriptions, `BarcodeAcceptedHint`, `BarcodeRejectedHint`.
- Status mode: `IBarcodeCountStatusProvider` (`OnStatusRequested(IList<TrackedBarcode>, IBarcodeCountStatusProviderCallback)`), `IBarcodeCountStatusProviderCallback` (`OnStatusReady(IBarcodeCountStatusResult)`), `BarcodeCountStatus` enum (`None`, `NotAvailable`, `Expired`, `Fragile`, `QualityCheck`, `LowStock`, `Wrong`), `BarcodeCountStatusItem.Create(TrackedBarcode, BarcodeCountStatus)`, `IBarcodeCountStatusResult` with factories `BarcodeCountStatusResultSuccess.Create(...)`, `BarcodeCountStatusResultError.Create(...)`, `BarcodeCountStatusResultAbort.Create(...)`.
- `TrackedBarcode` (in `Scandit.DataCapture.Barcode.Batch.Data`) — `Barcode`, `Identifier`, `Location`. Used by `IBarcodeCountViewListener`, the status API, and the capture-list session.

### Documented for other platforms but NOT on `dotnet.android` — do not use

- **`BarcodeCountMappingFlowSettings`** and the mapping-flow configuration class — not surfaced in the .NET binding. Mapping in .NET is limited to `BarcodeCountSettings.MappingEnabled` + `BarcodeCountSession.GetSpatialMap()`.
- **`BarcodeCountSessionSnapshot`** — no .NET equivalent.
- **`HardwareTriggerEnabled`** is iOS-only; on Android use `EnableHardwareTrigger(int? keyCode)` + static `HardwareTriggerSupported`.
