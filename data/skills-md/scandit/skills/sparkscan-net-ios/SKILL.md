---
name: sparkscan-net-ios
description: SparkScan single-barcode scanning with the pre-built `SparkScanView` UI in .NET for iOS projects (`net*-ios` target framework, `Scandit.DataCapture.Barcode` NuGet, non-MAUI — for MAUI apps use sparkscan-net-maui). Use for integration, scan settings, result handling, feedback customization, scanning lifecycle, SDK version migration (v6→v7→v8), replacing third-party scanners (ZXing.Net.Mobile), or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# SparkScan .NET for iOS Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The SparkScan API changes between major SDK versions — button-visibility / color properties get renamed, removed, or restructured. The .NET binding also uses **different naming conventions** than the Swift / Obj-C native SDK (PascalCase, `Enabled` instead of `isEnabled`, `TimeSpan` instead of `TimeInterval`, etc.), and a few naming choices differ from the rest of the .NET API.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

.NET-iOS-specific gotchas worth flagging:

- This skill targets the **non-MAUI** .NET for iOS workload (project `<TargetFramework>net10.0-ios</TargetFramework>`, no `<UseMaui>` flag). For MAUI apps, use the `sparkscan-net-maui` skill instead.
- **`SparkScan` and `SparkScanSettings` use plain `new` constructors, not `Create(...)` factories.** This is unusual compared to the rest of the .NET API (`BarcodeCapture.Create(...)`, `BarcodeCaptureSettings.Create()`, `DataCaptureView.Create(...)`). The canonical pattern is `var settings = new SparkScanSettings(); var sparkScan = new SparkScan(settings);` — writing `SparkScan.Create(...)` or `SparkScanSettings.Create()` is a compile error. `DataCaptureContext.ForLicenseKey(key)` still uses the factory form (it lives in Core, not Spark).
- **`SparkScanView.Create(parent, context, sparkScan, settings)` IS a factory** (unlike `SparkScan` itself). On iOS the parent argument is just `this.View` — there is no coordinator-layout container (that's Android-only). The created view is added to `parentView` automatically; do not call `this.View.AddSubview(sparkScanView)` yourself.
- iOS lifecycle is `sparkScanView.PrepareScanning()` in `ViewWillAppear` and `sparkScanView.StopScanning()` in `ViewWillDisappear`. **Do not** use `OnPause` / `OnResume` here — those are the Android-only API. Calling them on iOS will not compile (the iOS binding does not surface them).
- **Pick the `UIViewController` constructor that matches how the controller is instantiated**, or the camera preview will never appear. The `dotnet new ios` template that ships with modern .NET-iOS is **scene-based** (no `Main.storyboard`, `UIApplicationSceneManifest` in `Info.plist`, `SceneDelegate.WillConnect` builds the window programmatically) — in that project shape, the VC must expose a parameterless `public ViewController() : base() { }` and `SceneDelegate.WillConnect` calls `new ViewController()`. Older Scandit samples are **storyboard-based** (`UIMainStoryboardFile` in `Info.plist`, `customClass="ViewController"` in the storyboard) — those need `public ViewController(IntPtr handle) : base(handle) { }` because storyboard inflation invokes that ctor with a real native handle. **Never call `new ViewController(IntPtr.Zero)`** to bridge the two: `IntPtr.Zero` is a null native handle, so the resulting managed wrapper has no underlying `UIViewController`; `this.View` never attaches to the window, `SparkScanView.Create(parentView: this.View, …)` lands on a detached view, and the app launches into a blank screen with no camera and no scans. See [references/integration.md](references/integration.md) "Scene-based vs storyboard instantiation" for the full callout.
- `NSCameraUsageDescription` in `Info.plist` is mandatory. Without it the app crashes on first camera access. iOS shows the system permission dialog automatically when the camera starts — there is no separate runtime-request API for the camera.
- The .NET `ISparkScanListener` has **only two** methods: `OnBarcodeScanned(SparkScan, SparkScanSession, IFrameData?)` and `OnSessionUpdated(SparkScan, SparkScanSession, IFrameData?)`. **There are no `OnObservationStarted` / `OnObservationStopped` methods** (the way `IBarcodeCaptureListener` has them).
- Prefer the **event API** (`sparkScan.BarcodeScanned += handler`) over the listener interface in idiomatic C# — that's what the official .NET iOS SparkScan sample uses. The event handler receives `SparkScanEventArgs` with `Session`, `FrameData`, and `SparkScan`.
- **`IFrameData` and the image buffers must be `Dispose()`d on iOS.** The official sample uses `using var imageBuffer = args.FrameData?.ImageBuffers.LastOrDefault();` and `using var frame = imageBuffer?.ToImage();`. Failing to dispose causes a frozen / stuttering preview. The `SparkScanEventArgs.FrameData` itself is `IFrameData?`. If you do not need the frame, do not retain it.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Code128`, `Symbology.InterleavedTwoOfFive`, `Symbology.Qr`, `Symbology.DataMatrix`. They are **not** Swift dot-case (`.ean13UPCA`).
- The capture mode's enabled property is `sparkScan.Enabled` (not `IsEnabled`).
- `CodeDuplicateFilter` is `TimeSpan` — **not** `TimeInterval` (that is the Swift type). Use `TimeSpan.FromMilliseconds(500)`, `TimeSpan.FromSeconds(2.5)`, or `TimeSpan.Zero`. `SparkScanSettings` does **not** expose `CodeDuplicate.DefaultDuplicateFilter` / `ReportDataAndSymbologyOnlyOnce` sentinels — those live on `BarcodeCaptureSettings`, not on SparkScan. For SparkScan, set the `TimeSpan` directly.
- Feedback is delivered through `ISparkScanFeedbackDelegate.GetFeedbackForBarcode(Barcode)` and assigned with `sparkScanView.Feedback = this` (or any object that implements `ISparkScanFeedbackDelegate`). Returning `null` from the delegate falls back to the default success feedback.
  - Success feedback: `new SparkScanBarcodeSuccessFeedback()` (default), or pass `(Color)`, `(Color, Brush)`, or `(Color, Brush, Feedback?)`.
  - Error feedback: `new SparkScanBarcodeErrorFeedback(message: "...", resumeCapturingDelay: TimeSpan.FromSeconds(60))`. The view shows the error message, the trigger button shows an error state, and scanning resumes after the delay.
- `GetFeedbackForBarcode(Barcode)` is invoked on a **background thread**. Build the feedback object eagerly (in `SetupSparkScan` / `ViewDidLoad`) and just return it.
- `SparkScan.BarcodeScanned` (and `ISparkScanListener.OnBarcodeScanned`) also run on a **background thread**. Dispatch any UI update via `DispatchQueue.MainQueue.DispatchAsync(() => { … })`.
- **SDK 8.0+ requires explicit initialization in `AppDelegate.FinishedLaunching`.** Call `ScanditCaptureCore.Initialize()` + `ScanditBarcodeCapture.Initialize()` before any Scandit code runs. Without this the SDK's DI container has no registrations and the first `new SparkScan(...)` / `SparkScanView.Create(...)` call crashes at launch. **Not required on 6.x / 7.x.** See [references/integration.md](references/integration.md) for the canonical `AppDelegate.cs` template.
- The NuGet packages are `Scandit.DataCapture.Core` and `Scandit.DataCapture.Barcode`. No separate `*.Maui` packages here — those are only for MAUI projects. **Do not guess the version from training data** — fetch the latest stable from `https://www.nuget.org/packages/Scandit.DataCapture.Barcode/` via `WebFetch` before pinning. Inventing a non-existent version (e.g. `8.13.0` when only `8.4.0` is published) causes `dotnet restore` to fail with `Unable to find package Scandit.DataCapture.Core with version (>= …)`. See [references/integration.md](references/integration.md) Step 0 for the full procedure.
- `SparkScanView.HardwareTriggerSupported` and `SparkScanViewSettings.HardwareTriggerKeyCode` are **Android-only** and not surfaced on dotnet.ios. Do not reference them in iOS code.
- `SparkScanScanningModeDefault` and `SparkScanScanningModeTarget` are constructed with `new`, both taking `(SparkScanScanningBehavior, SparkScanPreviewBehavior)`. There is no parameterless constructor in the .NET binding; the Swift `init()` overloads (no args) are not surfaced on dotnet.ios.
- View state is exposed via `SparkScanView.ViewStateChanged` (event of `EventHandler<SparkScanViewStateEventArgs>`) — there is **no** `UiListener` property on the .NET binding. Use the events `BarcodeCountButtonTapped`, `BarcodeFindButtonTapped`, `LabelCaptureButtonTapped`, and `ViewStateChanged` instead.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating SparkScan from scratch, configuring settings, customizing feedback, customizing the SparkScanView appearance, handling scans, doing async work after a scan, or displaying scanned barcodes in a list** (e.g. "add SparkScan to my .NET iOS app", "set up barcode scanning in C#", "how do I use SparkScan in net-ios", "reject barcodes with error feedback", "hide the torch button", "show a custom toast on scan", "use target mode", "crop a thumbnail from the scanned frame", "show scanned barcodes in a list", "add a results table under the scanner", "build a UITableView of scans") → read [references/integration.md](references/integration.md) and follow the instructions there (the list-building recipe lives in the "Build a results list (UITableView pattern)" subsection under Optional configuration).
- **Migrating or upgrading an existing SparkScan integration** (e.g. "upgrade from v6 to v7", "migrate my SparkScan", "bump the Scandit .NET SDK to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Replacing a third-party barcode scanner with SparkScan** (e.g. "replace my ZXing.Net.Mobile scanner with SparkScan", "migrate from AVFoundation barcode scanning to Scandit", "switch from [library] to SparkScan") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

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
| Get Started | [Get Started (.NET for iOS)](https://docs.scandit.com/sdks/net/ios/sparkscan/get-started/) |
| Advanced topics (custom feedback, scanning modes, UI customization, toast messages) | [Advanced Configurations](https://docs.scandit.com/sdks/net/ios/sparkscan/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/net/ios/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/ios/migrate-7-to-8/) |
| Full API reference | [SparkScan API (.NET iOS)](https://docs.scandit.com/data-capture-sdk/dotnet.ios/barcode-capture/api.html) |

## API surface this skill covers

All classes documented with `:available: dotnet.ios` in the official RST docs (`docs/source/barcode-capture/api/spark-scan*.rst` and `api/ui/spark-scan-*.rst`) are addressed in [references/integration.md](references/integration.md):

- `SparkScan` — `new SparkScan()`, `new SparkScan(SparkScanSettings)`, `Enabled`, `ApplySettingsAsync(settings)`, `AddListener(ISparkScanListener)` / `RemoveListener(ISparkScanListener)`, events `BarcodeScanned` / `SessionUpdated` (both `EventHandler<SparkScanEventArgs>`), `SparkScanLicenseInfo`, `Dispose`.
- `SparkScanSettings` — `new SparkScanSettings()`, `new SparkScanSettings(CapturePreset)`, `EnableSymbology`, `EnableSymbologies(ICollection<Symbology>)`, `EnableSymbologies(CompositeType)`, `GetSymbologySettings`, `EnabledSymbologies`, `EnabledCompositeTypes`, `CodeDuplicateFilter`, `BatterySaving`, `ScanIntention`, `SetProperty` / `GetProperty<T>` / `TryGetProperty<T>`.
- `SparkScanSession` — `NewlyRecognizedBarcode`, `FrameSequenceId`, `Reset()`.
- `SparkScanEventArgs` — `SparkScan`, `Session`, `FrameData`.
- `ISparkScanListener` — `OnBarcodeScanned`, `OnSessionUpdated`. (No `OnObservation*` callbacks.)
- `SparkScanLicenseInfo` — `LicensedSymbologies`.
- Feedback: `SparkScanBarcodeFeedback` (abstract), `SparkScanBarcodeSuccessFeedback` (4 constructors), `SparkScanBarcodeErrorFeedback(message, resumeCapturingDelay, …)` (4 constructors), `ISparkScanFeedbackDelegate.GetFeedbackForBarcode(Barcode)`.
- `SparkScanView` — `Create(parentView, context, sparkScan, settings)`, lifecycle `PrepareScanning()` / `StopScanning()`, control methods `StartScanning()` / `PauseScanning()` / `ShowToast(string)`, button visibility properties (`BarcodeCountButtonVisible`, `BarcodeFindButtonVisible`, `LabelCaptureButtonVisible`, `TargetModeButtonVisible`, `ScanningBehaviorButtonVisible`, `ZoomSwitchControlVisible`, `PreviewSizeControlVisible`, `CameraSwitchButtonVisible`, `TriggerButtonVisible`, `PreviewCloseControlVisible`, `TorchControlVisible`), color / image customization (`ToolbarBackgroundColor`, `ToolbarIconActiveTintColor`, `ToolbarIconInactiveTintColor`, `TriggerButtonCollapsedColor`, `TriggerButtonExpandedColor`, `TriggerButtonAnimationColor`, `TriggerButtonTintColor`, `TriggerButtonImage`), `Feedback` (the `ISparkScanFeedbackDelegate`), static `DefaultBrush`, events `BarcodeCountButtonTapped`, `BarcodeFindButtonTapped`, `LabelCaptureButtonTapped`, `ViewStateChanged`.
- `SparkScanViewSettings` — `TriggerButtonCollapseTimeout`, `DefaultScanningMode`, `DefaultTorchState`, `SoundEnabled`, `HapticEnabled`, `HoldToScanEnabled`, `HardwareTriggerEnabled`, `ZoomFactorOut`, `ZoomFactorIn`, `ToastSettings`, `VisualFeedbackEnabled`, `InactiveStateTimeout`, `DefaultCameraPosition`, `DefaultMiniPreviewSize`, `SmartSelectionCandidateBrush`. (No `HardwareTriggerKeyCode` — Android-only.)
- `SparkScanToastSettings` — `ToastEnabled`, `ToastBackgroundColor`, `ToastTextColor`, plus message strings (`TargetModeEnabledMessage`, `ContinuousModeEnabledMessage`, `ScanPausedMessage`, `ZoomedInMessage`, `TorchEnabledMessage`, etc. — see integration.md for the full list).
- `SparkScanViewState` enum (`Initial`, `Idle`, `Inactive`, `Active`, `Error`), `SparkScanViewEventArgs(View)`, `SparkScanViewStateEventArgs(State)`.
- `SparkScanMiniPreviewSize` enum (`Regular`, `Expanded`).
- `SparkScanPreviewBehavior` enum (`Default`, `Persistent`), `SparkScanScanningBehavior` enum (`Single`, `Continuous`).
- `ISparkScanScanningMode` (`: IDisposable`), `SparkScanScanningModeDefault(scanningBehavior, previewBehavior)`, `SparkScanScanningModeTarget(scanningBehavior, previewBehavior)`.
