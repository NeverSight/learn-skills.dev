---
name: matrixscan-ar-net-ios
description: MatrixScan AR (Barcode AR, BarcodeAr) in .NET for iOS projects (`net*-ios` TFM, `Scandit.DataCapture.Barcode` NuGet, non-MAUI — MAUI apps use matrixscan-ar-net-maui) — scanning multiple barcodes at once with AR highlights and annotations (info annotations, popovers, status icons) in C#. Use for integration, settings, listeners/events, highlight and annotation providers, torch/zoom/macro controls, lifecycle, SDK version migration, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan AR .NET for iOS Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The `BarcodeAr` API is relatively new (introduced in `dotnet.ios` 7.2) and differs in several places from the Swift native SDK: providers are **async/Task**-based instead of delegate-based, highlight and annotation constructors take **only a `Barcode`** (no `context` argument), the listener interface has **only one method**, `BarcodeArView` is **`IDisposable`** rather than a `UIView` subclass, and the .NET binding uses PascalCase, `TimeSpan` instead of `TimeInterval`, etc.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

.NET-iOS-specific gotchas worth flagging:

- This skill targets the **non-MAUI** .NET for iOS workload (project `<TargetFramework>net10.0-ios</TargetFramework>` or similar, no `<UseMaui>` flag). For MAUI apps, use a MAUI-targeted skill instead — `BarcodeArView` is hosted very differently there (XAML / `Microsoft.Maui.Controls.View`).
- **`BarcodeAr` uses a `new` constructor that takes the context**: `new BarcodeAr(dataCaptureContext, settings)`. There is no `BarcodeAr.Create(...)` / `BarcodeAr.ForDataCaptureContext(...)` factory in .NET. `BarcodeArSettings` also uses plain `new`. (`DataCaptureContext.ForLicenseKey(key)` still uses the factory form — it lives in Core.)
- **`BarcodeArView.Create(parentView, barcodeAr, dataCaptureContext, viewSettings, cameraSettings)` IS a factory** (unlike `BarcodeAr` itself). The `cameraSettings` argument is nullable — pass `null` to use `BarcodeAr.RecommendedCameraSettings`. The `parentView` is a `UIView` (typically `this.View` of the hosting view controller, or a dedicated container `UIView` outlet). `BarcodeArView` attaches itself to the `parentView` automatically — do **not** call `this.View.AddSubview(...)` on it.
- **`BarcodeArView` is `IDisposable`, not a `UIView` subclass.** The class declares `public static implicit operator View(BarcodeArView view)` that converts to `UIKit.UIView` when needed (e.g. for native interop, since `View` is aliased to `UIView` on iOS via `global using View = UIKit.UIView;`), but you do **not** add it to the view hierarchy yourself — the `Create` factory attaches it to `parentView` automatically.
- **There is no `OnResume()` / `OnPause()` on the .NET `BarcodeArView` on iOS.** Those methods are **Android-only** (guarded by `#if __ANDROID__` in the binding). On iOS the lifecycle is `barcodeArView.Start()` in `ViewWillAppear` and `barcodeArView.Stop()` in `ViewWillDisappear` — matching the official `MatrixScanARSimpleSample`. Calling `barcodeArView.OnResume()` from a .NET iOS view controller is a compile error.
- **`BarcodeArView.Dispose()` does the teardown.** There is no `OnDestroy()` method on `BarcodeArView` (that is an Android Java/Kotlin idiom). Call `Dispose()` from your view controller's `Dispose(bool)` override or rely on `using` semantics if you own a short-lived instance.
- **iOS-only view controls.** `ShouldShowMacroModeControl` (`bool`) and `MacroModeControlPosition` (`Anchor`) exist **only on iOS** (Android does not expose these). They sit alongside the cross-platform `ShouldShowTorchControl` / `ShouldShowZoomControl` / `ShouldShowCameraSwitchControl` and their `*Position` siblings. Mention them when the user asks about controls on iOS.
- **`IBarcodeArListener` has only one method:** `OnSessionUpdated(BarcodeAr, BarcodeArSession, IFrameData)`. There are **no `OnObservationStarted` / `OnObservationStopped` callbacks** like the Swift `BarcodeArListener` protocol has on `dotnet.ios`. Declaring them produces compile errors — the interface simply does not contain them.
- Prefer the **event API** (`barcodeAr.SessionUpdated += handler`) over the listener interface in idiomatic C#. The handler receives `BarcodeArEventArgs` with `BarcodeAr`, `Session`, and `FrameData`. `AddListener(IBarcodeArListener)` still works for parity with other platforms.
- **`OnSessionUpdated` / `SessionUpdated` runs on a background recognition queue.** Dispatch any UI update via `DispatchQueue.MainQueue.DispatchAsync(() => { … })` (from `CoreFoundation`). Do **not** use `InvokeOnMainThread` — it works, but the official Scandit .NET iOS samples consistently use `DispatchQueue.MainQueue.DispatchAsync`.
- **Provider interfaces are async, not delegate-based.** `IBarcodeArHighlightProvider.HighlightForBarcodeAsync(Barcode)` returns `Task<IBarcodeArHighlight?>` and `IBarcodeArAnnotationProvider.AnnotationForBarcodeAsync(Barcode)` returns `Task<IBarcodeArAnnotation?>`. Do not look for a delegate / `completionHandler` parameter — they don't exist in the .NET binding. Return `Task.FromResult<IBarcodeArHighlight?>(null)` (or `null` from an `async` method) to suppress the highlight/annotation for a given barcode.
- **Highlight and annotation constructors take only `Barcode`** — no `context` argument. Use `new BarcodeArRectangleHighlight(barcode)`, `new BarcodeArCircleHighlight(barcode, BarcodeArCircleHighlightPreset.Dot)`, `new BarcodeArInfoAnnotation(barcode)`, `new BarcodeArStatusIconAnnotation(barcode)`, `new BarcodeArPopoverAnnotation(barcode, buttons)`. Passing a `UIViewController` or `UIView` is a compile error.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Code128`, `Symbology.Code39`, `Symbology.Qr`, `Symbology.DataMatrix`, `Symbology.InterleavedTwoOfFive`. They are **not** the Swift camelCase style (`.ean13UPCA`, `.qr`).
- `BarcodeArSettings` does **not** expose an `Enabled` toggle — `BarcodeAr` itself has no `Enabled` property either. To pause/resume scanning, use `barcodeArView.Pause()` / `barcodeArView.Start()`.
- **`BarcodeArViewSettings` is minimal in .NET.** Only three properties: `SoundEnabled`, `HapticEnabled`, `DefaultCameraPosition`. Do **not** invent properties like `TriggerButtonCollapseTimeout`, `InactiveStateTimeout`, `ToastSettings`, or `DefaultMiniPreviewSize` — those are SparkScan, not BarcodeAr.
- **`BarcodeArFeedback`** lives in `Scandit.DataCapture.Barcode.Ar.Feedback` and has two `Core.Common.Feedback.Feedback` properties: `Scanned` and `Tapped`. The empty constructor `new BarcodeArFeedback()` produces a feedback object with both events silent — assigning it to `barcodeAr.Feedback` disables the default beep/vibration. To restore defaults, use the static `BarcodeArFeedback.DefaultFeedback`. (Note: it's a **static property** in .NET, not the Swift `BarcodeArFeedback.default()` method.)
- Tap interactions on highlights are exposed as the **`HighlightForBarcodeTapped` event** on `BarcodeArView` (`EventHandler<HighlightForBarcodeTappedEventArgs>`). There is **no `UiListener` / `UIDelegate` property** on the .NET `BarcodeArView` — the Swift `BarcodeArViewUIDelegate` is surfaced as a C# event instead. Event args expose `BarcodeAr`, `Barcode`, and `Highlight`.
- **`barcodeAr.Feedback` is a property (get/set)**; `ApplySettingsAsync(BarcodeArSettings)` returns a `Task`. `BarcodeAr.RecommendedCameraSettings` is a **static property**, not a method (the Swift SDK exposes `BarcodeAr.recommendedCameraSettings` as a class var — in .NET it's a getter; there is **no** `BarcodeAr.CreateRecommendedCameraSettings()` method on `dotnet.ios`).
- **No `BarcodeArFilter` / `SetBarcodeFilter` in the .NET API tree.** The Swift `setBarcodeFilter(...)` method (added in 8.1) is not surfaced on `dotnet.ios` at present. Do not attempt to use it.
- **View-controller constructor depends on how the VC is instantiated.** If the VC is inflated by a storyboard / XIB (typical when the project has a `Main.storyboard` with `UIMainStoryboardFile` set in `Info.plist`), keep the `public MyVC(IntPtr handle) : base(handle) { }` constructor — the runtime calls it with a real native handle. For **programmatically-instantiated VCs** (no `Main.storyboard`, root view controller set from `SceneDelegate.WillConnect` or `AppDelegate`), declare a parameterless `public MyVC() : base() { }` and instantiate via `new MyVC()`. **Do not pass `IntPtr.Zero` to the `(IntPtr)` ctor** — that leaves the native peer uninitialized and `ViewDidLoad` may never fire, which manifests as a black screen with no camera preview and no scans.
- **SDK 8.0+ requires explicit initialization.** Call `ScanditCaptureCore.Initialize()` + `ScanditBarcodeCapture.Initialize()` in `AppDelegate.FinishedLaunching` (or the very top of `SceneDelegate.WillConnect` if the project has no `AppDelegate`) before any Scandit code runs. Without this, the first `new BarcodeAr(...)` / `BarcodeArView.Create(...)` call crashes at launch because the DI container has no registrations. **Not required on 6.x / 7.x.** See [references/integration.md](references/integration.md) for the full `AppDelegate.cs` template.
- The NuGet packages are `Scandit.DataCapture.Core` and `Scandit.DataCapture.Barcode`. No separate `*.Maui` packages here — those are only for MAUI projects. **Do not guess the version from training data** — fetch the latest stable from `https://www.nuget.org/packages/Scandit.DataCapture.Barcode/` via `WebFetch` before pinning. Inventing a non-existent version (e.g. `8.13.0` when only `8.4.0` is published) causes `dotnet restore` to fail with `Unable to find package Scandit.DataCapture.Core with version (>= …)`. See [references/integration.md](references/integration.md) Step 0 for the full procedure.
- **iOS `SupportedOSPlatformVersion` must be ≥ `15.0`.** Set it in the `.csproj`. The official Scandit iOS sample `Info.plist` `MinimumOSVersion` is `15.0` and the project's `<SupportedOSPlatformVersion>` matches.
- **The required `Info.plist` key is `NSCameraUsageDescription`** (`Privacy - Camera Usage Description`). Without it the app crashes on first camera access. iOS prompts the user automatically the first time the camera opens; there is **no separate runtime-request API** to call (no Android-style `RequestPermissions`). This is a key difference from the .NET Android skill, which requires a manual permission flow.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeAr from scratch, configuring settings, customizing highlights or annotations, handling session updates, customizing feedback, or wiring tap interactions** (e.g. "add MatrixScan AR to my .NET iOS app", "set up barcode AR scanning in C#", "show a rectangle highlight on every tracked barcode", "show an info annotation with the barcode data", "make the beep silent", "react to a highlight tap", "switch to circle highlights", "show the macro-mode toggle") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing MatrixScan AR integration** (e.g. "upgrade from v7 to v8", "bump the Scandit .NET SDK to v8", "what changed between SDK versions for BarcodeAr", "do I need to change my BarcodeAr code when moving to 8.x") → read [references/migration.md](references/migration.md) and follow the instructions there.

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
| Get Started | [Get Started (.NET for iOS)](https://docs.scandit.com/sdks/net/ios/matrixscan-ar/get-started/) |
| Advanced topics (custom highlights, custom annotations, tap interactions, popovers, filter) | [Advanced Configurations](https://docs.scandit.com/sdks/net/ios/matrixscan-ar/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/net/ios/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/ios/migrate-7-to-8/) |
| Full API reference | [BarcodeAr API (.NET iOS)](https://docs.scandit.com/data-capture-sdk/dotnet.ios/barcode-capture/api.html) |

## API surface this skill covers

All classes documented with `:available: dotnet.ios` in the official RST docs (`docs/source/barcode-capture/api/barcode-ar*.rst` and `api/ui/barcode-ar-*.rst`) are addressed in [references/integration.md](references/integration.md):

- `BarcodeAr` — `new BarcodeAr(DataCaptureContext?, BarcodeArSettings)`, `Feedback` (get/set), `ApplySettingsAsync(BarcodeArSettings)` → `Task`, `AddListener(IBarcodeArListener)` / `RemoveListener(IBarcodeArListener)`, `event EventHandler<BarcodeArEventArgs> SessionUpdated`, static `RecommendedCameraSettings`, `Dispose`.
- `BarcodeArSettings` — `new BarcodeArSettings()`, `EnableSymbology(Symbology, bool)`, `EnableSymbologies(ICollection<Symbology>)`, `GetSymbologySettings(Symbology)`, `EnabledSymbologies` (get), `ExpectsOnlyUniqueBarcodes` (get/set), `SetProperty` / `GetProperty<T>` / `TryGetProperty<T>`, `Dispose`.
- `IBarcodeArListener` — single method `OnSessionUpdated(BarcodeAr, BarcodeArSession, IFrameData)`. (No `OnObservation*` callbacks.)
- `BarcodeArSession` — `AddedTrackedBarcodes` (`IReadOnlyList<TrackedBarcode>`), `RemovedTrackedBarcodes` (`IReadOnlyList<int>`), `TrackedBarcodes` (`IReadOnlyDictionary<int, TrackedBarcode>`), `Reset()`.
- `BarcodeArEventArgs` — `BarcodeAr`, `Session`, `FrameData`.
- `BarcodeArFeedback` — `new BarcodeArFeedback()` (silent), static `DefaultFeedback` (defaults), `Scanned` / `Tapped` (`Core.Common.Feedback.Feedback`), `Dispose`.
- `BarcodeArView` — `static Create(UIView parentView, BarcodeAr, DataCaptureContext, BarcodeArViewSettings, CameraSettings?)`, `HighlightProvider` (get/set `IBarcodeArHighlightProvider?`), `AnnotationProvider` (get/set `IBarcodeArAnnotationProvider?`), `ShouldShowTorchControl` / `ShouldShowZoomControl` / `ShouldShowCameraSwitchControl` / `ShouldShowMacroModeControl` (iOS-only), `TorchControlPosition` / `ZoomControlPosition` / `CameraSwitchControlPosition` / `MacroModeControlPosition` (iOS-only) (`Anchor`), `Start()`, `Stop()`, `Pause()`, `Reset()`, `GetNotificationPresenter()`, `event EventHandler<HighlightForBarcodeTappedEventArgs> HighlightForBarcodeTapped`, implicit conversion to `UIKit.UIView`, `Dispose`. **No `OnResume()` / `OnPause()` on iOS — those are Android-only.**
- `BarcodeArViewSettings` — `SoundEnabled` (default `true`), `HapticEnabled` (default `true`), `DefaultCameraPosition` (default `WorldFacing`).
- `HighlightForBarcodeTappedEventArgs` — `BarcodeAr`, `Barcode`, `Highlight` (`IBarcodeArHighlight`).
- Highlights: `IBarcodeArHighlight : IDisposable`, `IBarcodeArHighlightProvider.HighlightForBarcodeAsync(Barcode) → Task<IBarcodeArHighlight?>`, `BarcodeArRectangleHighlight(Barcode)` with `Barcode` / `Brush` / `Icon`, `BarcodeArCircleHighlight(Barcode, BarcodeArCircleHighlightPreset)` with `Barcode` / `Brush` / `Icon` / `Size`, `BarcodeArCircleHighlightPreset` enum (`Dot`, `Icon`).
- Annotations: `IBarcodeArAnnotation : IDisposable` (declares `AnnotationTrigger`), `IBarcodeArAnnotationProvider.AnnotationForBarcodeAsync(Barcode) → Task<IBarcodeArAnnotation?>`.
  - `BarcodeArStatusIconAnnotation(Barcode)` — `AnnotationTrigger`, `HasTip`, `Icon`, `Text`, `TextColor`, `BackgroundColor`.
  - `BarcodeArInfoAnnotation(Barcode)` — `HasTip`, `EntireAnnotationTappable`, `Anchor` (`BarcodeArInfoAnnotationAnchor`), `AnnotationTrigger`, `Width` (`BarcodeArInfoAnnotationWidthPreset`), `Body` (`IReadOnlyCollection<BarcodeArInfoAnnotationBodyComponent>`), `Header` (`BarcodeArInfoAnnotationHeader?`), `Footer` (`BarcodeArInfoAnnotationFooter?`), `BackgroundColor`, `Listener` (`IBarcodeArInfoAnnotationListener?`).
  - `BarcodeArPopoverAnnotation(Barcode, IList<BarcodeArPopoverAnnotationButton>)` — `AnnotationTrigger`, `EntirePopoverTappable`, `Listener` (`IBarcodeArPopoverAnnotationListener?`), `Buttons`.
  - `BarcodeArPopoverAnnotationButton(ScanditIcon, string)` — `Text`, `TextSize`, `Typeface`, `TextColor`, `Enabled`, `Icon`.
  - `BarcodeArAnnotationTrigger` enum: `HighlightTapAndBarcodeScan`, `HighlightTap`.
- Info-annotation sub-package (`Scandit.DataCapture.Barcode.Ar.UI.Annotations.Info`): `BarcodeArInfoAnnotationBodyComponent` (`Text`, `TextColor`, `TextSize`, `Typeface`, `StyledTextFormatted`, `LeftIcon`, `RightIcon`, `LeftIconTappable`, `RightIconTappable`, `TextAlignment`), `BarcodeArInfoAnnotationHeader` (`Text`, `TextSize`, `Typeface`, `TextColor`, `Icon`, `BackgroundColor`), `BarcodeArInfoAnnotationFooter` (`Text`, `TextSize`, `Typeface`, `TextColor`, `Icon`, `BackgroundColor`), `BarcodeArInfoAnnotationAnchor` enum (`Left`, `Right`, `Bottom`, `Top`), `BarcodeArInfoAnnotationWidthPreset` enum (`Small`, `Medium`, `Large`), `IBarcodeArInfoAnnotationListener` (`OnInfoAnnotationHeaderTapped`, `OnInfoAnnotationFooterTapped`, `OnInfoAnnotationLeftIconTapped`, `OnInfoAnnotationRightIconTapped`, `OnInfoAnnotationTapped`).
- `IBarcodeArPopoverAnnotationListener` — `OnPopoverButtonTapped`, `OnPopoverTapped`.
- `TrackedBarcode` (in `Scandit.DataCapture.Barcode.Batch.Data`) — `Barcode`, `Identifier`, `Location`.
