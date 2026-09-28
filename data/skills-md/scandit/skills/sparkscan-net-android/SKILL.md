---
name: sparkscan-net-android
description: SparkScan single-barcode scanning with the pre-built `SparkScanView` UI in .NET for Android projects (`net*-android` target framework, `Scandit.DataCapture.Barcode` NuGet, non-MAUI — for MAUI apps use sparkscan-net-maui). Use for integration, scan settings, result handling, feedback customization, lifecycle wiring, SDK version migration (v6→v7→v8), replacing third-party scanners (ZXing.Net), or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# SparkScan .NET for Android Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The SparkScan API changes between major SDK versions — button-visibility / color properties get renamed, removed, or restructured. The .NET binding also uses **different naming conventions** than the Kotlin/Java native SDK (PascalCase, `Enabled` instead of `isEnabled`, `TimeSpan` instead of `TimeInterval`, etc.), and a few naming choices differ from the rest of the .NET API.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

.NET-Android-specific gotchas worth flagging:

- This skill targets the **non-MAUI** .NET for Android workload (project `<TargetFramework>net10.0-android</TargetFramework>`, no `<UseMaui>` flag). For MAUI apps, use the `sparkscan-net-maui` skill instead.
- **`SparkScan` and `SparkScanSettings` use plain `new` constructors, not `Create(...)` factories.** This is unusual compared to the rest of the .NET API (`BarcodeCapture.Create(...)`, `BarcodeCaptureSettings.Create()`, `DataCaptureView.Create(...)`). The canonical pattern is `var settings = new SparkScanSettings(); var sparkScan = new SparkScan(settings);` — writing `SparkScan.Create(...)` or `SparkScanSettings.Create()` is a compile error. `DataCaptureContext.ForLicenseKey(key)` still uses the factory form (it lives in Core, not Spark).
- **`SparkScanView.Create(parent, context, sparkScan, settings)` IS a factory** (unlike `SparkScan` itself). The parent argument must be a `SparkScanCoordinatorLayout` for everything to position correctly — passing an arbitrary `ViewGroup` is supported by the binding but the official sample uses `SparkScanCoordinatorLayout` and so should you.
- **`SparkScanCoordinatorLayout` is declared in XML, not C#.** It lives in `Scandit.DataCapture.Barcode.Spark.UI.Platform.Android` and is referenced from the activity layout as `<com.scandit.datacapture.barcode.spark.ui.SparkScanCoordinatorLayout … />`. Get it with `FindViewById<SparkScanCoordinatorLayout>(Resource.Id.spark_scan_coordinator)`.
- Lifecycle on the view is `sparkScanView.OnPause()` / `sparkScanView.OnResume()` — these are **not** the activity's `OnPause`/`OnResume`. Forward the activity calls into them: `protected override void OnPause() { base.OnPause(); this.sparkScanView.OnPause(); }`.
- The .NET `ISparkScanListener` has **only two** methods: `OnBarcodeScanned(SparkScan, SparkScanSession, IFrameData?)` and `OnSessionUpdated(SparkScan, SparkScanSession, IFrameData?)`. **There are no `OnObservationStarted` / `OnObservationStopped` methods** (the way `IBarcodeCaptureListener` has them). Implementing those will produce `does not implement interface member` errors only if you try; the interface simply doesn't declare them.
- Prefer the **event API** (`sparkScan.BarcodeScanned += handler`) over the listener interface in idiomatic C# — that's what the official .NET Android SparkScan sample uses. The event handler receives `SparkScanEventArgs` with `Session`, `FrameData`, and `SparkScan`.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Code128`, `Symbology.InterleavedTwoOfFive`, `Symbology.Qr`, `Symbology.DataMatrix`. They are **not** the Kotlin underscore style (`EAN13_UPCA`).
- The capture mode's enabled property is `sparkScan.Enabled` (not `IsEnabled`).
- `CodeDuplicateFilter` is `TimeSpan` — **not** `TimeInterval` (that is the Kotlin/Java type). Use `TimeSpan.FromMilliseconds(500)`, `TimeSpan.FromSeconds(2.5)`, or `TimeSpan.Zero`. `SparkScanSettings` does **not** expose `CodeDuplicate.DefaultDuplicateFilter` / `ReportDataAndSymbologyOnlyOnce` sentinels — those live on `BarcodeCaptureSettings`, not on SparkScan. For SparkScan, set the `TimeSpan` directly.
- Feedback is delivered through `ISparkScanFeedbackDelegate.GetFeedbackForBarcode(Barcode)` and assigned with `sparkScanView.Feedback = this` (or any object that implements `ISparkScanFeedbackDelegate`). Returning `null` from the delegate falls back to the default success feedback.
  - Success feedback: `new SparkScanBarcodeSuccessFeedback()` (default), or pass a `Color` / `Brush` / inner `Feedback` to one of the larger constructors.
  - Error feedback: `new SparkScanBarcodeErrorFeedback(message: "...", resumeCapturingDelay: TimeSpan.FromSeconds(30))`. The view shows the error message, the trigger button shows an error state, and scanning resumes after the delay.
- `GetFeedbackForBarcode(Barcode)` is invoked on a **background thread**. Build the feedback object eagerly (in `OnCreate`) and just return it — do not dispatch to the UI thread inside the delegate.
- `SparkScan.BarcodeScanned` (and `ISparkScanListener.OnBarcodeScanned`) also run on a **background thread**. Dispatch any UI update via `RunOnUiThread(() => { … })`.
- **SDK 8.0+ requires explicit initialization.** Subclass `Android.App.Application`, decorate with `[Application]`, and call `ScanditCaptureCore.Initialize()` + `ScanditBarcodeCapture.Initialize()` in `OnCreate()` before any Scandit code runs. Without this the SDK's DI container has no registrations and the first `new SparkScan(...)` / `SparkScanView.Create(...)` call crashes at launch. **Not required on 6.x / 7.x.** See [references/integration.md](references/integration.md) for the full `MainApplication.cs` template.
- The NuGet packages are `Scandit.DataCapture.Core` and `Scandit.DataCapture.Barcode`. No separate `*.Maui` packages here — those are only for MAUI projects. **Do not guess the version from training data** — fetch the latest stable from `https://www.nuget.org/packages/Scandit.DataCapture.Barcode/` via `WebFetch` before pinning. Inventing a non-existent version (e.g. `8.13.0` when only `8.4.0` is published) causes `dotnet restore` to fail with `Unable to find package Scandit.DataCapture.Core with version (>= …)`. See [references/integration.md](references/integration.md) Step 0 for the full procedure.
- **Android `SupportedOSPlatformVersion` must be ≥ `24`.** Set it in the `.csproj`. Lower values fail the build with `uses-sdk:minSdkVersion 21 cannot be smaller than version 24 declared in library`.
- **Do not declare `<activity>` elements for `[Activity]`-decorated classes in `AndroidManifest.xml`.** The `[Activity(MainLauncher = true, ...)]` attribute is the canonical registration mechanism in .NET for Android — the build merges a correctly-named entry into the final manifest using the .NET-derived Java class name. A manual `<activity android:name=".MainActivity">` resolves against `<ApplicationId>` and **won't match** the generated class, producing `ClassNotFoundException: Didn't find class ... .MainActivity` at launch. Only add to the manifest the elements the skill explicitly asks for (`<uses-feature>`, `<uses-permission>`) — leave activities to the attribute.
- The runtime camera permission helper (`CameraPermissionActivity`) inherits from `AppCompatActivity`, so `Xamarin.AndroidX.AppCompat` must be in the `.csproj`. When pinning the version, pick the highest available including the Xamarin patch revision (e.g. `1.7.0.5`, not bare `1.7.0`) — the `.X` suffix marks Xamarin-binding-level updates and carries critical transitive-dep fixes.
- **The activity needs a `Theme.AppCompat` descendant.** Because the activity inherits from `AppCompatActivity`, set `Theme = "@style/Theme.AppCompat.Light.NoActionBar"` on the `[Activity]` attribute (or `android:theme=...` on `<application>` in the manifest). Without it, `SetContentView` throws `IllegalStateException: You need to use a Theme.AppCompat theme (or descendant) with this activity` at launch. The `dotnet new android` template's default theme is **not** AppCompat-based, so this must be set explicitly.
- Hardware trigger support: `SparkScanView.HardwareTriggerSupported` is a **static property** (Android-only) that returns `true` on Android API 28+. Enable hardware triggers via `viewSettings.HardwareTriggerEnabled = true`; set a custom key code via `viewSettings.HardwareTriggerKeyCode` (also Android-only, nullable).
- `SparkScanScanningModeDefault` and `SparkScanScanningModeTarget` are constructed with `new`, both taking `(SparkScanScanningBehavior, SparkScanPreviewBehavior)`. There is no parameterless constructor in the .NET binding; the Swift `SparkScanScanningModeDefault()` overload (no args) is iOS-only and not surfaced on dotnet.android.
- View state is exposed via `SparkScanView.ViewStateChanged` (event of `EventHandler<SparkScanViewStateEventArgs>`) — there is **no** `SetListener(...)` / `UiListener` property on the .NET binding. Use the events `BarcodeCountButtonTapped`, `BarcodeFindButtonTapped`, `LabelCaptureButtonTapped`, and `ViewStateChanged` instead.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating SparkScan from scratch, configuring settings, customizing feedback, customizing the SparkScanView appearance, handling scans, or doing async work after a scan** (e.g. "add SparkScan to my .NET Android app", "set up barcode scanning in C#", "how do I use SparkScan in net-android", "reject barcodes with error feedback", "hide the torch button", "enable hardware trigger", "show a custom toast on scan", "use target mode") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing SparkScan integration** (e.g. "upgrade from v6 to v7", "migrate my SparkScan", "bump the Scandit .NET SDK to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Replacing a third-party barcode scanner with SparkScan** (e.g. "replace my ZXing.Net.Mobile scanner with SparkScan", "migrate from ZXing.Net to Scandit", "switch from [library] to SparkScan") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

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
| Get Started | [Get Started (.NET for Android)](https://docs.scandit.com/sdks/net/android/sparkscan/get-started/) |
| Advanced topics (custom feedback, hardware triggers, scanning modes, UI customization, toast messages) | [Advanced Configurations](https://docs.scandit.com/sdks/net/android/sparkscan/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/net/android/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/android/migrate-7-to-8/) |
| Full API reference | [SparkScan API (.NET Android)](https://docs.scandit.com/data-capture-sdk/dotnet.android/barcode-capture/api.html) |

## API surface this skill covers

All classes documented with `:available: dotnet.android` in the official RST docs (`docs/source/barcode-capture/api/spark-scan*.rst` and `api/ui/spark-scan-*.rst`) are addressed in [references/integration.md](references/integration.md):

- `SparkScan` — `new SparkScan()`, `new SparkScan(SparkScanSettings)`, `Enabled`, `ApplySettingsAsync(settings)`, `AddListener(ISparkScanListener)` / `RemoveListener(ISparkScanListener)`, events `BarcodeScanned` / `SessionUpdated` (both `EventHandler<SparkScanEventArgs>`), `SparkScanLicenseInfo`, `Dispose`.
- `SparkScanSettings` — `new SparkScanSettings()`, `new SparkScanSettings(CapturePreset)`, `EnableSymbology`, `EnableSymbologies(ICollection<Symbology>)`, `EnableSymbologies(CompositeType)`, `GetSymbologySettings`, `EnabledSymbologies`, `EnabledCompositeTypes`, `CodeDuplicateFilter`, `BatterySaving`, `ScanIntention`, `SetProperty` / `GetProperty<T>` / `TryGetProperty<T>`.
- `SparkScanSession` — `NewlyRecognizedBarcode`, `FrameSequenceId`, `Reset()`.
- `SparkScanEventArgs` — `SparkScan`, `Session`, `FrameData`.
- `ISparkScanListener` — `OnBarcodeScanned`, `OnSessionUpdated`. (No `OnObservation*` callbacks.)
- `SparkScanLicenseInfo` — `LicensedSymbologies`.
- Feedback: `SparkScanBarcodeFeedback` (abstract), `SparkScanBarcodeSuccessFeedback` (4 constructors), `SparkScanBarcodeErrorFeedback(message, resumeCapturingDelay, …)` (4 constructors), `ISparkScanFeedbackDelegate.GetFeedbackForBarcode(Barcode)`.
- `SparkScanView` — `Create(parentView, context, sparkScan, settings)`, lifecycle `OnPause()` / `OnResume()`, control methods `StartScanning()` / `PauseScanning()` / `ShowToast(string)`, button visibility properties (`BarcodeCountButtonVisible`, `BarcodeFindButtonVisible`, `LabelCaptureButtonVisible`, `TargetModeButtonVisible`, `ScanningBehaviorButtonVisible`, `ZoomSwitchControlVisible`, `PreviewSizeControlVisible`, `CameraSwitchButtonVisible`, `TriggerButtonVisible`, `PreviewCloseControlVisible`, `TorchControlVisible`), color / image customization (`ToolbarBackgroundColor`, `ToolbarIconActiveTintColor`, `ToolbarIconInactiveTintColor`, `TriggerButtonCollapsedColor`, `TriggerButtonExpandedColor`, `TriggerButtonAnimationColor`, `TriggerButtonTintColor`, `TriggerButtonImage`), `Feedback` (the `ISparkScanFeedbackDelegate`), static `DefaultBrush`, static `HardwareTriggerSupported` (Android-only), events `BarcodeCountButtonTapped`, `BarcodeFindButtonTapped`, `LabelCaptureButtonTapped`, `ViewStateChanged`.
- `SparkScanViewSettings` — `TriggerButtonCollapseTimeout`, `DefaultScanningMode`, `DefaultTorchState`, `SoundEnabled`, `HapticEnabled`, `HoldToScanEnabled`, `HardwareTriggerEnabled`, `HardwareTriggerKeyCode` (Android-only), `ZoomFactorOut`, `ZoomFactorIn`, `ToastSettings`, `VisualFeedbackEnabled`, `InactiveStateTimeout`, `DefaultCameraPosition`, `DefaultMiniPreviewSize`, `SmartSelectionCandidateBrush`.
- `SparkScanToastSettings` — `ToastEnabled`, `ToastBackgroundColor`, `ToastTextColor`, plus message strings (`TargetModeEnabledMessage`, `ContinuousModeEnabledMessage`, `ScanPausedMessage`, `ZoomedInMessage`, `TorchEnabledMessage`, etc. — see integration.md for the full list).
- `SparkScanViewState` enum (`Initial`, `Idle`, `Inactive`, `Active`, `Error`), `SparkScanViewEventArgs(View)`, `SparkScanViewStateEventArgs(State)`.
- `SparkScanMiniPreviewSize` enum (`Regular`, `Expanded`).
- `SparkScanPreviewBehavior` enum (`Default`, `Persistent`), `SparkScanScanningBehavior` enum (`Single`, `Continuous`).
- `ISparkScanScanningMode` (`: IDisposable`), `SparkScanScanningModeDefault(scanningBehavior, previewBehavior)`, `SparkScanScanningModeTarget(scanningBehavior, previewBehavior)`.
- `SparkScanCoordinatorLayout` — XAML-declared container, referenced from C# via `FindViewById<SparkScanCoordinatorLayout>(...)`. Inherits from `FrameLayout`.
