---
name: matrixscan-ar-net-android
description: MatrixScan AR (Barcode AR, BarcodeAr) in .NET for Android projects (`net*-android` TFM, `Scandit.DataCapture.Barcode` NuGet, non-MAUI — MAUI apps use matrixscan-ar-net-maui) — scanning multiple barcodes at once with AR highlights and annotations. Use for integration, settings, listeners/events, highlight and annotation providers, lifecycle, SDK version migration, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan AR .NET for Android Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The `BarcodeAr` API is relatively new (introduced in dotnet.android 7.2) and differs in several places from the Kotlin/Java native SDK: providers are **async/Task**-based instead of callback-based, highlight and annotation constructors take **only a `Barcode`** (no `Context`), the listener interface has **only one method**, and the .NET binding uses PascalCase, `TimeSpan` instead of `TimeInterval`, etc.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

.NET-Android-specific gotchas worth flagging:

- This skill targets the **non-MAUI** .NET for Android workload (project `<TargetFramework>net10.0-android</TargetFramework>` or similar, no `<UseMaui>` flag). For MAUI apps, use a MAUI-targeted skill instead — `BarcodeArView` is hosted very differently there.
- **`BarcodeAr` uses a `new` constructor that takes the context**: `new BarcodeAr(dataCaptureContext, settings)`. There is no `BarcodeAr.Create(...)` / `BarcodeAr.ForDataCaptureContext(...)` factory in .NET. `BarcodeArSettings` also uses plain `new`. (`DataCaptureContext.ForLicenseKey(key)` still uses the factory form — it lives in Core.)
- **`BarcodeArView.Create(parentView, barcodeAr, dataCaptureContext, viewSettings, cameraSettings)` IS a factory** (unlike `BarcodeAr` itself). The `cameraSettings` argument is nullable — pass `null` to use `BarcodeAr.RecommendedCameraSettings`. The `parentView` is an `Android.Views.View` / `ViewGroup` (typically a `FrameLayout` or the activity's root content view). There is **no `BarcodeArCoordinatorLayout`** — that container is SparkScan-specific; `BarcodeArView` simply attaches itself to whatever `ViewGroup` you pass.
- **`BarcodeArView` is `IDisposable`, not an Android `View` itself.** The class declares `public static implicit operator View(BarcodeArView view)` that converts to `Android.Views.View` when needed (e.g. for native interop), but you do **not** add it to the view hierarchy yourself — the `Create` factory attaches it to `parentView` automatically.
- Lifecycle on the view is `barcodeArView.OnResume()` / `barcodeArView.OnPause()` — these are Android-only methods (guarded by `#if __ANDROID__` in the binding) and they are **not** the activity's `OnPause`/`OnResume`. Forward the activity calls into them. **`OnDestroy()` does not exist on the .NET `BarcodeArView` — call `Dispose()` instead** (in the activity's `OnDestroy` or `Dispose`).
- **`IBarcodeArListener` has only one method:** `OnSessionUpdated(BarcodeAr, BarcodeArSession, IFrameData)`. There are **no `OnObservationStarted` / `OnObservationStopped` callbacks** like the Kotlin `BarcodeArListener` has. Implementing those will produce compile errors — the interface simply does not declare them.
- Prefer the **event API** (`barcodeAr.SessionUpdated += handler`) over the listener interface in idiomatic C#. The handler receives `BarcodeArEventArgs` with `BarcodeAr`, `Session`, and `FrameData`. `AddListener(IBarcodeArListener)` still works for parity with other platforms.
- **`OnSessionUpdated` / `SessionUpdated` runs on a background recognition thread.** Dispatch any UI update via `RunOnUiThread(() => { … })`.
- **Provider interfaces are async, not callback-based.** `IBarcodeArHighlightProvider.HighlightForBarcodeAsync(Barcode)` returns `Task<IBarcodeArHighlight?>` and `IBarcodeArAnnotationProvider.AnnotationForBarcodeAsync(Barcode)` returns `Task<IBarcodeArAnnotation?>`. Do not look for a `Callback` parameter or a `callback.OnData(...)` method — they don't exist in the .NET binding. Return `Task.FromResult<IBarcodeArHighlight?>(null)` (or `null` from an `async` method) to suppress the highlight/annotation for a given barcode.
- **Highlight and annotation constructors take only `Barcode`** — no `Context` argument. Use `new BarcodeArRectangleHighlight(barcode)`, `new BarcodeArCircleHighlight(barcode, BarcodeArCircleHighlightPreset.Dot)`, `new BarcodeArInfoAnnotation(barcode)`, `new BarcodeArStatusIconAnnotation(barcode)`, `new BarcodeArPopoverAnnotation(barcode, buttons)`. Passing a `Context` is a compile error.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Code128`, `Symbology.Code39`, `Symbology.Qr`, `Symbology.DataMatrix`, `Symbology.InterleavedTwoOfFive`. They are **not** the Kotlin underscore style (`EAN13_UPCA`).
- `BarcodeArSettings` does **not** expose an `Enabled` toggle — `BarcodeAr` itself has no `Enabled` property either. To pause/resume scanning, use `barcodeArView.Pause()` / `barcodeArView.Start()`.
- **`BarcodeArViewSettings` is minimal in .NET.** Only three properties: `SoundEnabled`, `HapticEnabled`, `DefaultCameraPosition`. Do **not** invent properties like `TriggerButtonCollapseTimeout`, `InactiveStateTimeout`, `ToastSettings`, or `DefaultMiniPreviewSize` — those are SparkScan, not BarcodeAr.
- **`BarcodeArFeedback`** lives in `Scandit.DataCapture.Barcode.Ar.Feedback` and has two `Core.Common.Feedback.Feedback` properties: `Scanned` and `Tapped`. The empty constructor `new BarcodeArFeedback()` produces a feedback object with both events silent — assigning it to `barcodeAr.Feedback` disables the default beep/vibration. To restore defaults, use the static `BarcodeArFeedback.DefaultFeedback`. (Note: it's a **static property** in .NET, not the Kotlin `BarcodeArFeedback.defaultFeedback()` method.)
- Tap interactions on highlights are exposed as the **`HighlightForBarcodeTapped` event** on `BarcodeArView` (`EventHandler<HighlightForBarcodeTappedEventArgs>`). There is **no `UiListener` property** on the .NET `BarcodeArView` — the Kotlin `IBarcodeArViewUiListener` is surfaced as a C# event instead. Event args expose `BarcodeAr`, `Barcode`, and `Highlight`.
- **`barcodeAr.Feedback` is a property (get/set)**; `ApplySettingsAsync(BarcodeArSettings)` returns a `Task`. `BarcodeAr.RecommendedCameraSettings` is a **static property**, not a method (the Kotlin SDK exposes `BarcodeAr.createRecommendedCameraSettings()` — in .NET it's a getter).
- **No `BarcodeArFilter` / `SetBarcodeFilter` in the .NET API tree.** The Kotlin/iOS `setBarcodeFilter(...)` method (added in 8.1) is not surfaced on `dotnet.android` at present. Do not attempt to use it.
- **SDK 8.0+ requires explicit initialization.** Subclass `Android.App.Application`, decorate with `[Application]`, and call `ScanditCaptureCore.Initialize()` + `ScanditBarcodeCapture.Initialize()` in `OnCreate()` before any Scandit code runs. Without this, the first `new BarcodeAr(...)` / `BarcodeArView.Create(...)` call crashes at launch because the DI container has no registrations. **Not required on 6.x / 7.x.** See [references/integration.md](references/integration.md) for the full `MainApplication.cs` template.
- The NuGet packages are `Scandit.DataCapture.Core` and `Scandit.DataCapture.Barcode`. No separate `*.Maui` packages here — those are only for MAUI projects. **Do not guess the version from training data** — fetch the latest stable from `https://www.nuget.org/packages/Scandit.DataCapture.Barcode/` via `WebFetch` before pinning. Inventing a non-existent version (e.g. `8.13.0` when only `8.4.0` is published) causes `dotnet restore` to fail with `Unable to find package Scandit.DataCapture.Core with version (>= …)`. See [references/integration.md](references/integration.md) Step 0 for the full procedure.
- **Android `SupportedOSPlatformVersion` must be ≥ `24`.** Set it in the `.csproj`. Lower values fail the build with `uses-sdk:minSdkVersion 21 cannot be smaller than version 24 declared in library`.
- **Do not declare `<activity>` elements for `[Activity]`-decorated classes in `AndroidManifest.xml`.** The `[Activity(MainLauncher = true, ...)]` attribute is the canonical registration mechanism in .NET for Android — the build merges a correctly-named entry into the final manifest using the .NET-derived Java class name. A manual `<activity android:name=".MainActivity">` resolves against `<ApplicationId>` and **won't match** the generated class, producing `ClassNotFoundException: Didn't find class ... .MainActivity` at launch. Only add to the manifest the elements the skill explicitly asks for (`<uses-feature>`, `<uses-permission>`) — leave activities to the attribute.
- The runtime camera permission helper (`CameraPermissionActivity`) inherits from `AppCompatActivity`, so `Xamarin.AndroidX.AppCompat` must be in the `.csproj`. When pinning the version, pick the highest available including the Xamarin patch revision (e.g. `1.7.0.5`, not bare `1.7.0`) — the `.X` suffix marks Xamarin-binding-level updates and carries critical transitive-dep fixes.
- **The activity needs a `Theme.AppCompat` descendant.** Because the activity inherits from `AppCompatActivity`, set `Theme = "@style/Theme.AppCompat.Light.NoActionBar"` on the `[Activity]` attribute (or `android:theme=...` on `<application>` in the manifest). Without it, `SetContentView` throws `IllegalStateException: You need to use a Theme.AppCompat theme (or descendant) with this activity` at launch. The `dotnet new android` template's default theme is **not** AppCompat-based, so this must be set explicitly.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeAr from scratch, configuring settings, customizing highlights or annotations, handling session updates, customizing feedback, or wiring tap interactions** (e.g. "add MatrixScan AR to my .NET Android app", "set up barcode AR scanning in C#", "show a rectangle highlight on every tracked barcode", "show an info annotation with the barcode data", "make the beep silent", "react to a highlight tap", "switch to circle highlights") → read [references/integration.md](references/integration.md) and follow the instructions there.
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
| Get Started | [Get Started (.NET for Android)](https://docs.scandit.com/sdks/net/android/matrixscan-ar/get-started/) |
| Advanced topics (custom highlights, custom annotations, tap interactions, popovers, filter) | [Advanced Configurations](https://docs.scandit.com/sdks/net/android/matrixscan-ar/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/net/android/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/android/migrate-7-to-8/) |
| Full API reference | [BarcodeAr API (.NET Android)](https://docs.scandit.com/data-capture-sdk/dotnet.android/barcode-capture/api.html) |

## API surface this skill covers

All classes documented with `:available: dotnet.android` in the official RST docs (`docs/source/barcode-capture/api/barcode-ar*.rst` and `api/ui/barcode-ar-*.rst`) are addressed in [references/integration.md](references/integration.md):

- `BarcodeAr` — `new BarcodeAr(DataCaptureContext?, BarcodeArSettings)`, `Feedback` (get/set), `ApplySettingsAsync(BarcodeArSettings)` → `Task`, `AddListener(IBarcodeArListener)` / `RemoveListener(IBarcodeArListener)`, `event EventHandler<BarcodeArEventArgs> SessionUpdated`, static `RecommendedCameraSettings`, `Dispose`.
- `BarcodeArSettings` — `new BarcodeArSettings()`, `EnableSymbology(Symbology, bool)`, `EnableSymbologies(ICollection<Symbology>)`, `GetSymbologySettings(Symbology)`, `EnabledSymbologies` (get), `ExpectsOnlyUniqueBarcodes` (get/set), `SetProperty` / `GetProperty<T>` / `TryGetProperty<T>`, `Dispose`.
- `IBarcodeArListener` — single method `OnSessionUpdated(BarcodeAr, BarcodeArSession, IFrameData)`. (No `OnObservation*` callbacks.)
- `BarcodeArSession` — `AddedTrackedBarcodes` (`IReadOnlyList<TrackedBarcode>`), `RemovedTrackedBarcodes` (`IReadOnlyList<int>`), `TrackedBarcodes` (`IReadOnlyDictionary<int, TrackedBarcode>`), `Reset()`.
- `BarcodeArEventArgs` — `BarcodeAr`, `Session`, `FrameData`.
- `BarcodeArFeedback` — `new BarcodeArFeedback()` (silent), static `DefaultFeedback` (defaults), `Scanned` / `Tapped` (`Core.Common.Feedback.Feedback`), `Dispose`.
- `BarcodeArView` — `static Create(View parentView, BarcodeAr, DataCaptureContext, BarcodeArViewSettings, CameraSettings?)`, `HighlightProvider` (get/set `IBarcodeArHighlightProvider?`), `AnnotationProvider` (get/set `IBarcodeArAnnotationProvider?`), `ShouldShowTorchControl` / `ShouldShowZoomControl` / `ShouldShowCameraSwitchControl`, `TorchControlPosition` / `ZoomControlPosition` / `CameraSwitchControlPosition` (`Anchor`), `Start()`, `Stop()`, `Pause()`, `Reset()`, `GetNotificationPresenter()`, `OnResume()` / `OnPause()` (Android-only), `event EventHandler<HighlightForBarcodeTappedEventArgs> HighlightForBarcodeTapped`, implicit conversion to `Android.Views.View`, `Dispose`.
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
