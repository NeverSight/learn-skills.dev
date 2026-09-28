---
name: sparkscan-net-maui
description: SparkScan single-barcode scanning with the pre-built `SparkScanView` UI in .NET MAUI projects (`<UseMaui>true</UseMaui>`, `Scandit.DataCapture.Barcode.Maui` NuGet) — for non-MAUI .NET projects use sparkscan-net-android or sparkscan-net-ios. Use for integration, scan settings, result handling, feedback and UI customization, SDK version migration (v6→v7→v8), replacing third-party MAUI scanners (ZXing.Net.Maui), or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# SparkScan .NET MAUI Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The SparkScan API changes between major SDK versions — button-visibility / color properties get renamed, removed, or restructured. The .NET binding also uses **different naming conventions** than the Kotlin / Swift native SDKs (PascalCase, `Enabled` instead of `isEnabled`, `TimeSpan` instead of `TimeInterval`, etc.), and the MAUI control has its own quirks that are separate from both the BarcodeCapture MAUI integration and the non-MAUI .NET-Android / .NET-iOS SparkScan integrations.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

MAUI-specific gotchas worth flagging:

- This skill is for MAUI apps (`<UseMaui>true</UseMaui>` in the `.csproj`). If the project does **not** have `<UseMaui>true</UseMaui>`, use the `sparkscan-net-android` or `sparkscan-net-ios` skill instead — those cover the non-MAUI .NET Android / .NET iOS workloads.
- **The MAUI builder chain for SparkScan is different from the BarcodeCapture MAUI builder chain.** SparkScan uses `.UseScanditCore().UseScanditBarcode(configure => configure.AddSparkScanView())` — `UseScanditCore` takes **no** `configure` lambda and `UseScanditBarcode` **does** take a configure lambda with `AddSparkScanView()` inside it. This is the **opposite** shape of the BarcodeCapture builder, which is `.UseScanditCore(c => c.AddDataCaptureView()).UseScanditBarcode()` (Core takes a configure lambda; Barcode takes none). Do not cross-pollinate — if you see a BarcodeCapture MAUI sample online with `UseScanditCore(c => c.AddDataCaptureView()).UseScanditBarcode()`, that pattern is correct **for BarcodeCapture only**. For SparkScan, the builder line must read `.UseScanditCore().UseScanditBarcode(c => c.AddSparkScanView())`. Cross-reference the BarcodeCapture MAUI skill if both modes coexist in the same app — both registrations are needed in that case.
- **`AddDataCaptureView()` is not needed for SparkScan.** SparkScan has its own pre-built MAUI handler (`<scandit:SparkScanView>`) — it does not use the generic `<scandit:DataCaptureView>`. Calling `UseScanditCore(c => c.AddDataCaptureView())` on a SparkScan-only project is harmless but unnecessary; the simpler `UseScanditCore()` is what the official sample uses.
- **XAML namespace is `clr-namespace:Scandit.DataCapture.Barcode.Spark.UI.Maui;assembly=ScanditBarcodeCaptureMaui`.** Note: `assembly=ScanditBarcodeCaptureMaui` (no dots in the assembly name) — the NuGet package is `Scandit.DataCapture.Barcode.Maui` but the assembly it produces is `ScanditBarcodeCaptureMaui`. Easy to get wrong if you just copy the package id.
- **`<scandit:SparkScanView>` requires three bindable properties: `DataCaptureContext`, `SparkScan`, `SparkScanViewSettings`.** Without all three bound, the preview is black and scanning never starts. There is also an optional `Feedback` bindable property for the `ISparkScanFeedbackDelegate`. The MAUI control is a pre-built `View`, **not** the generic `<scandit:DataCaptureView>` — for SparkScan there is no separate camera preview, overlay, or context-view wiring to do.
- **MAUI lifecycle for the SparkScan control is `OnAppearing()` / `OnDisappearing()` — called on the control, not just the page.** Forward the page's `OnAppearing` / `OnDisappearing` into `this.SparkScanView.OnAppearing()` / `this.SparkScanView.OnDisappearing()`. These are MAUI-specific methods on the SparkScan MAUI control — they don't exist on the non-MAUI dotnet.android / dotnet.ios bindings (which use `OnPause`/`OnResume` and `PrepareScanning`/`StopScanning` respectively).
- **`SparkScan` and `SparkScanSettings` use plain `new` constructors, not `Create(...)` factories.** This is unusual compared to the rest of the .NET API (`BarcodeCapture.Create(...)`, `BarcodeCaptureSettings.Create()`). The canonical pattern is `var settings = new SparkScanSettings(); var sparkScan = new SparkScan(settings);` — writing `SparkScan.Create(...)` or `SparkScanSettings.Create()` is a compile error. `DataCaptureContext.ForLicenseKey(key)` still uses the factory form (it lives in Core, not Spark).
- The .NET `ISparkScanListener` has **only two** methods: `OnBarcodeScanned(SparkScan, SparkScanSession, IFrameData?)` and `OnSessionUpdated(SparkScan, SparkScanSession, IFrameData?)`. **There are no `OnObservationStarted` / `OnObservationStopped` methods** (the way `IBarcodeCaptureListener` has them).
- Prefer the **event API** (`sparkScan.BarcodeScanned += handler`) over the listener interface in idiomatic C#. The official MAUI SparkScan sample wires the event on the view model. The handler receives `SparkScanEventArgs` with `Session`, `FrameData`, and `SparkScan`.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Code128`, `Symbology.InterleavedTwoOfFive`, `Symbology.Qr`, `Symbology.DataMatrix`.
- The capture mode's enabled property is `sparkScan.Enabled` (not `IsEnabled`).
- `CodeDuplicateFilter`, `TriggerButtonCollapseTimeout`, `InactiveStateTimeout`, `SparkScanBarcodeErrorFeedback.resumeCapturingDelay` are all `TimeSpan` — **not** `TimeInterval`. `SparkScanSettings` does **not** expose `CodeDuplicate.DefaultDuplicateFilter` / `ReportDataAndSymbologyOnlyOnce` sentinels — those live on `BarcodeCaptureSettings`. For SparkScan, set the `TimeSpan` directly.
- Feedback is delivered through `ISparkScanFeedbackDelegate.GetFeedbackForBarcode(Barcode)` and assigned with `this.SparkScanView.Feedback = this` from the page code-behind (where `this` implements `ISparkScanFeedbackDelegate`). Returning `null` from the delegate falls back to the default success feedback.
  - Success feedback: `new SparkScanBarcodeSuccessFeedback()` (default), or pass `(Color)`, `(Color, Brush)`, or `(Color, Brush, Feedback?)`.
  - Error feedback: `new SparkScanBarcodeErrorFeedback(message: "...", resumeCapturingDelay: TimeSpan.FromSeconds(60))`. The view shows the error message, the trigger button shows an error state, and scanning resumes after the delay.
- `GetFeedbackForBarcode(Barcode)` is invoked on a **background thread**. Build the feedback objects once (in the page constructor or `OnAppearing`) and return cached instances.
- `SparkScan.BarcodeScanned` (and `ISparkScanListener.OnBarcodeScanned`) also run on a **background thread**. Dispatch UI updates via `MainThread.BeginInvokeOnMainThread(() => { … })`. `MainThread.StartTimer` does **not** exist — `StartTimer` is on `IDispatcher` (`Dispatcher.StartTimer(...)` / `Application.Current.Dispatcher.StartTimer(...)`).
- **Four NuGet packages are required:** `Scandit.DataCapture.Core`, `Scandit.DataCapture.Core.Maui`, `Scandit.DataCapture.Barcode`, `Scandit.DataCapture.Barcode.Maui`. All four must be pinned to the **same** version. Fetch the latest stable version from `https://www.nuget.org/packages/Scandit.DataCapture.Barcode.Maui/` — skip `-beta` / `-preview` / `-rc` suffixes. Versions from training data are stale.
- **Android `SupportedOSPlatformVersion` must be ≥ `24.0`** — the MAUI template's default is `21.0`, which fails the build because Scandit's Android AAR has `minSdkVersion=24`. iOS minimum is `15.0` (matches the MAUI template default).
- **iOS `NSCameraUsageDescription` in `Platforms/iOS/Info.plist`** is mandatory. Without it the app crashes on first camera access. Android relies on `Permissions.Camera` (MAUI adds the manifest entry automatically when the permission is requested at build time) or you can add `<uses-permission android:name="android.permission.CAMERA" />` to `Platforms/Android/AndroidManifest.xml` explicitly.
- The MAUI sample does **not** call `ScanditCaptureCore.Initialize()` / `ScanditBarcodeCapture.Initialize()` directly — `UseScanditCore()` and `UseScanditBarcode(...)` invoke them as part of the builder chain. Do **not** add a separate `Initialize()` call in `MainApplication.cs` / `AppDelegate.cs` on top of the builder — it is redundant in MAUI.
- **MAUI single-file `Platforms/Android/MainApplication.cs` and `Platforms/iOS/AppDelegate.cs` are the standard MAUI shims** that call `MauiProgram.CreateMauiApp()`. Do **not** override their `OnCreate` / `FinishedLaunching` with manual Scandit initialization — that's a non-MAUI pattern.
- `SparkScanScanningModeDefault` and `SparkScanScanningModeTarget` are constructed with `new`, both taking `(SparkScanScanningBehavior, SparkScanPreviewBehavior)`. There is no parameterless constructor.
- View state is exposed via `SparkScanView.ViewStateChanged` (event of `EventHandler<SparkScanViewStateEventArgs>`) — use the events `BarcodeCountButtonTapped`, `BarcodeFindButtonTapped`, `LabelCaptureButtonTapped`, and `ViewStateChanged`.
- Hardware trigger: `SparkScanViewSettings.HardwareTriggerEnabled` is available cross-platform in MAUI but only has effect on Android. `HardwareTriggerKeyCode` is **Android-only** in the .NET binding — it is wrapped in `#if __ANDROID__` and not visible to cross-platform MAUI code. For cross-platform code, only set `HardwareTriggerEnabled` and rely on the default key code.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating SparkScan from scratch, configuring settings, customizing feedback, customizing the SparkScanView appearance, handling scans, MVVM wiring, or doing async work after a scan** (e.g. "add SparkScan to my MAUI app", "set up barcode scanning in MAUI", "how do I use SparkScan in net-maui", "reject barcodes with error feedback", "hide the torch button", "show a custom toast on scan", "use target mode", "bind SparkScan to my view model") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing SparkScan MAUI integration** (e.g. "upgrade from v6 to v7", "migrate my MAUI SparkScan", "bump the Scandit .NET SDK to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Replacing a third-party barcode scanner with SparkScan in MAUI** (e.g. "replace my ZXing.Net.Maui scanner with SparkScan", "migrate from BarcodeScanning.Native.Maui to Scandit", "switch from [library] to SparkScan in MAUI") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or property names. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below for both TFMs), extract the actual link from it, and follow that.

URL structures can vary (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Get Started | [Get Started (.NET MAUI)](https://docs.scandit.com/sdks/net/maui/sparkscan/get-started/) |
| Advanced topics (custom feedback, scanning modes, UI customization, toast messages) | [Advanced Configurations (.NET Android)](https://docs.scandit.com/sdks/net/android/sparkscan/advanced/) · [(.NET iOS)](https://docs.scandit.com/sdks/net/ios/sparkscan/advanced/) — MAUI shares both TFMs |
| Migration between major SDK versions | Android: [6 → 7](https://docs.scandit.com/sdks/net/android/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/android/migrate-7-to-8/) · iOS: [6 → 7](https://docs.scandit.com/sdks/net/ios/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/ios/migrate-7-to-8/) |
| Full API reference | [SparkScan API (.NET Android)](https://docs.scandit.com/data-capture-sdk/dotnet.android/barcode-capture/api.html) · [SparkScan API (.NET iOS)](https://docs.scandit.com/data-capture-sdk/dotnet.ios/barcode-capture/api.html) |

> MAUI inherits the per-TFM .NET API. There is no separate "dotnet.maui" doc filter — pick the .NET Android or .NET iOS API reference depending on which TFM you're debugging against. The MAUI-specific surface is just the XAML control, the builder extensions, and the `OnAppearing`/`OnDisappearing` lifecycle methods.

## API surface this skill covers

All classes documented with `:available: dotnet.android` and / or `:available: dotnet.ios` in the official RST docs (`docs/source/barcode-capture/api/spark-scan*.rst` and `api/ui/spark-scan-*.rst`) are addressed in [references/integration.md](references/integration.md), plus the MAUI-specific surface:

- **Cross-platform Spark API** (same as the per-TFM skills):
  - `SparkScan` — `new SparkScan()`, `new SparkScan(SparkScanSettings)`, `Enabled`, `ApplySettingsAsync`, `AddListener` / `RemoveListener`, events `BarcodeScanned` / `SessionUpdated`, `SparkScanLicenseInfo`, `Dispose`.
  - `SparkScanSettings` — `new`, symbology APIs, `CodeDuplicateFilter`, `BatterySaving`, `ScanIntention`, property bag.
  - `SparkScanSession` — `NewlyRecognizedBarcode`, `FrameSequenceId`, `Reset()`.
  - `SparkScanEventArgs` — `SparkScan`, `Session`, `FrameData`.
  - `ISparkScanListener` — `OnBarcodeScanned`, `OnSessionUpdated`.
  - `SparkScanLicenseInfo` — `LicensedSymbologies`.
  - Feedback: `SparkScanBarcodeFeedback`, `SparkScanBarcodeSuccessFeedback`, `SparkScanBarcodeErrorFeedback(message, resumeCapturingDelay, …)`, `ISparkScanFeedbackDelegate.GetFeedbackForBarcode(Barcode)`.
  - `SparkScanViewSettings` — `TriggerButtonCollapseTimeout`, `DefaultScanningMode`, `DefaultTorchState`, `SoundEnabled`, `HapticEnabled`, `HoldToScanEnabled`, `HardwareTriggerEnabled`, `ZoomFactorOut`, `ZoomFactorIn`, `ToastSettings`, `VisualFeedbackEnabled`, `InactiveStateTimeout`, `DefaultCameraPosition`, `DefaultMiniPreviewSize`, `SmartSelectionCandidateBrush`.
  - `SparkScanToastSettings` — `ToastEnabled`, `ToastBackgroundColor`, `ToastTextColor`, plus message strings.
  - `SparkScanViewState` enum, `SparkScanViewEventArgs`, `SparkScanViewStateEventArgs`.
  - `SparkScanMiniPreviewSize`, `SparkScanPreviewBehavior`, `SparkScanScanningBehavior` enums.
  - `ISparkScanScanningMode`, `SparkScanScanningModeDefault`, `SparkScanScanningModeTarget`.

- **MAUI-only surface** (assembly `ScanditBarcodeCaptureMaui`):
  - `Scandit.DataCapture.Barcode.Maui.MauiAppBuilderExtensions.UseScanditBarcode(this MauiAppBuilder, Action<ConfigureBarcode>)` — the configure lambda exposes `AddSparkScanView()`.
  - `Scandit.DataCapture.Core.Maui.MauiAppBuilderExtensions.UseScanditCore(this MauiAppBuilder)` — no configure lambda is needed for a SparkScan-only app.
  - `Scandit.DataCapture.Barcode.Spark.UI.Maui.SparkScanView` — the MAUI `View` control with bindable properties `DataCaptureContext`, `SparkScan`, `SparkScanViewSettings`, `Feedback`, plus instance methods `OnAppearing()`, `OnDisappearing()`, `StartScanning()`, `PauseScanning()`, `ShowToast(string)`, and the full set of cross-platform button-visibility / color / image properties and events inherited from the underlying SparkScan view.
