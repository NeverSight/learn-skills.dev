---
name: barcode-capture-net-android
description: Scandit BarcodeCapture in .NET for Android projects (`net*-android` target framework, `Scandit.DataCapture.Barcode` NuGet, non-MAUI — for MAUI apps use barcode-capture-net-maui) — the low-level, full-control barcode scanning mode without the pre-built SparkScan UI. Use for integration, scan settings, listener and event wiring, overlay customization, camera lifecycle, SDK version migration (v6→v7→v8), replacing ZXing.Net or ML Kit bindings, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# BarcodeCapture .NET for Android Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeCapture API changes significantly between major SDK versions — properties get renamed, removed, or restructured. The .NET binding also uses **different naming conventions** than the Kotlin/Java native SDK (PascalCase, `Create(...)` factories instead of `forDataCaptureContext`, `Enabled` instead of `isEnabled`, etc.).

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

.NET-Android-specific gotchas worth flagging:

- This skill targets the **non-MAUI** .NET for Android workload (project `<TargetFramework>net10.0-android</TargetFramework>`, no `<UseMaui>` flag). For MAUI apps, use the `barcode-capture-net-maui` skill instead.
- The .NET API uses **PascalCase factories**, not the Kotlin `forDataCaptureContext` / `newInstance` names. Use `BarcodeCapture.Create(context, settings)`, `BarcodeCaptureSettings.Create()`, `BarcodeCaptureOverlay.Create(barcodeCapture, dataCaptureView)`, `DataCaptureView.Create(dataCaptureContext)`.
- Symbology names are C# PascalCase: `Symbology.Ean13Upca`, `Symbology.Ean8`, `Symbology.Code128`, `Symbology.InterleavedTwoOfFive`, `Symbology.Qr`, `Symbology.DataMatrix`. They are **not** the Kotlin underscore style (`EAN13_UPCA`, `INTERLEAVED_TWO_OF_FIVE`).
- The capture mode's enabled property is `barcodeCapture.Enabled` (not `IsEnabled`). The `IDataCaptureMode` interface in the .NET binding exposes `Enabled`.
- `CodeDuplicateFilter` is `TimeSpan` — **not** `TimeInterval` (that is the Kotlin/Java type). Use `CodeDuplicate.DefaultDuplicateFilter`, `CodeDuplicate.ReportDataAndSymbologyOnlyOnce`, `TimeSpan.FromMilliseconds(500)`, `TimeSpan.FromSeconds(2.5)`, or `TimeSpan.Zero`. Writing `CodeDuplicateFilter = 500` is a type error.
- `BarcodeCapture.RecommendedCameraSettings` is a **static property**, not a method. The canonical pattern (used in the official .NET Android sample) is `camera = Camera.GetDefaultCamera(); camera.ApplySettingsAsync(BarcodeCapture.RecommendedCameraSettings);`. A `Camera.GetDefaultCamera(CameraSettings?)` overload also exists in the .NET binding (it calls `ApplySettingsAsync` internally) but the samples use the explicit two-line form — prefer it for clarity.
- `IBarcodeCaptureListener` callbacks are C#-named: `OnBarcodeScanned`, `OnSessionUpdated`, `OnObservationStarted`, `OnObservationStopped`. The `IFrameData` parameter is named `frameData`.
- The .NET binding also exposes a C# **event-based** API on `BarcodeCapture`: `BarcodeScanned` and `SessionUpdated` (both `EventHandler<BarcodeCaptureEventArgs>`). Use either the listener interface *or* the events — do not register the same handler through both paths.
- `OnBarcodeScanned` is invoked off the UI thread. Any UI update must be dispatched via `RunOnUiThread(() => { … })`.
- Call `barcodeCapture.Enabled = false` at the top of `OnBarcodeScanned` before doing any work to prevent duplicate or racing scans. Re-enable with `barcodeCapture.Enabled = true` when the app is ready to scan again.
- Turn the camera off in `OnPause()` and re-enable in `OnResume()` via `camera.SwitchToDesiredStateAsync(FrameSourceState.Off)` / `FrameSourceState.On`. The camera must not be active while the activity is backgrounded.
- Request the `Android.Manifest.Permission.Camera` at runtime before the first scan; the manifest declaration alone is not sufficient on API 23+. The official .NET Android sample uses a `CameraPermissionActivity` base class with `RequestPermissions` and `OnRequestPermissionsResult`.
- **Do not declare `<activity>` elements for `[Activity]`-decorated classes in `AndroidManifest.xml`.** The `[Activity(MainLauncher = true, ...)]` attribute is the canonical registration mechanism in .NET for Android — the build merges a correctly-named entry into the final manifest using the .NET-derived Java class name (typically `<lowercase-namespace>.MainActivity`). A manual `<activity android:name=".MainActivity">` resolves against `<ApplicationId>` (e.g. `com.companyname.MyApp.MainActivity`) and **won't match** the generated class, producing `ClassNotFoundException: Didn't find class ... .MainActivity` at launch. Only add to the manifest the elements the skill explicitly asks for (`<uses-feature>`, `<uses-permission>`, and an `android:theme` on `<application>` when needed) — leave activities to the attribute.
- `DataCaptureView.Create(dataCaptureContext)` returns an Android `View`. Add it to a `FrameLayout` container with `LayoutParams.MatchParent` for both dimensions. The .NET binding does **not** take a `Context` parameter in `DataCaptureView.Create` (Kotlin's `DataCaptureView.newInstance(context, dataCaptureContext)` is different).
- The NuGet packages are `Scandit.DataCapture.Core` and `Scandit.DataCapture.Barcode`. No separate `*.Maui` packages here — those are only for MAUI projects. **Do not guess the version from training data** — fetch the latest stable from `https://www.nuget.org/packages/Scandit.DataCapture.Barcode/` via `WebFetch` before pinning. Inventing a non-existent version (e.g. `8.13.0` when only `8.4.0` is published) causes `dotnet restore` to fail with `Unable to find package Scandit.DataCapture.Core with version (>= …)`. See [references/integration.md](references/integration.md) Step 0 for the full procedure.
- The `CameraPermissionActivity` helper inherits from `AppCompatActivity`, so `Xamarin.AndroidX.AppCompat` must be in the `.csproj`. `dotnet new android` pulls it in transitively; manually scaffolded projects must add it explicitly. **When pinning the version, pick the highest available including the Xamarin patch revision (e.g. `1.7.1.3`, not bare `1.7.1`)** — the `.X` suffix marks Xamarin-binding-level updates and carries critical transitive-dep fixes; the suffix-less form has a known `Xamarin.AndroidX.SavedState` mismatch that fails the build with `CS7069: Reference to type 'ISavedStateRegistryOwner' ... could not be found`.
- **`AndroidManifest.xml` `<application>` must use a `Theme.AppCompat` descendant theme.** Add `android:theme="@style/Theme.AppCompat.DayNight.NoActionBar"` (or another `Theme.AppCompat` subclass) to the `<application>` element. Without this, `AppCompatActivity` throws `java.lang.IllegalStateException: You need to use a Theme.AppCompat theme (or descendant) with this activity` at instant launch. `dotnet new android` does **not** set this attribute by default, so it must be added explicitly when integrating BarcodeCapture.
- When scaffolding a brand-new project, prefer `dotnet new android -o MyApp` over hand-writing the csproj/manifest/resources. It produces a buildable shell with correct `OutputType`, a `strings.xml`, and a launcher icon — all of which the manifest in this skill references. A hand-written csproj with `<OutputType>Library</OutputType>` will silently build an `.aar` instead of an installable `.apk`.
- **SDK 8.0+ requires explicit initialization.** Subclass `Android.App.Application`, decorate with `[Application]`, and call `ScanditCaptureCore.Initialize()` + `ScanditBarcodeCapture.Initialize()` in `OnCreate()` before any Scandit code runs. Without this the SDK's DI container has no registrations and the first `DataCaptureView.Create` / `BarcodeCapture.Create` call crashes at launch. **Not required on 6.x / 7.x** — those majors self-initialized. See the integration guide for the full `MainApplication.cs` template.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeCapture from scratch, configuring settings, customizing feedback, adding a viewfinder, handling scans, or doing async work after a scan** (e.g. "add BarcodeCapture to my .NET Android app", "set up barcode scanning in C#", "how do I use BarcodeCapture in net-android", "filter duplicate scans", "suppress the beep", "add a viewfinder", "disable scanning while I look up the barcode") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing BarcodeCapture integration** (e.g. "upgrade from v6 to v7", "migrate my BarcodeCapture", "bump the Scandit .NET SDK to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Replacing a third-party barcode scanner with BarcodeCapture** (e.g. "replace my ZXing.Net.Mobile scanner with BarcodeCapture", "migrate from ZXing.Net to Scandit", "switch from [library] to BarcodeCapture") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

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
| Get Started | [Get Started (.NET for Android)](https://docs.scandit.com/sdks/net/android/barcode-capture/get-started/) |
| Advanced topics (custom feedback, viewfinders, location selection, scan intention, composite codes) | [Advanced Configurations](https://docs.scandit.com/sdks/net/android/barcode-capture/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/net/android/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/net/android/migrate-7-to-8/) |
| Full API reference | [BarcodeCapture API (.NET Android)](https://docs.scandit.com/data-capture-sdk/dotnet.android/barcode-capture/api.html) |

## API surface this skill covers

All classes with `:available: dotnet.android` in the official RST docs are addressed in [references/integration.md](references/integration.md):

- `BarcodeCapture` — `Create(context, settings)`, `Create(settings)`, `Enabled`, `PointOfInterest`, `Feedback`, `BarcodeCaptureLicenseInfo`, `Context`, static `RecommendedCameraSettings`, `ApplySettingsAsync`, `AddListener` / `RemoveListener`, events `BarcodeScanned` / `SessionUpdated`.
- `BarcodeCaptureSettings` — `Create()`, `EnableSymbology`, `EnableSymbologies(ICollection<Symbology>)`, `EnableSymbologies(CompositeType)`, `GetSymbologySettings`, `EnabledSymbologies`, `EnabledCompositeTypes`, `CodeDuplicateFilter`, `LocationSelection`, `BatterySaving`, `ScanIntention`, `SetProperty` / `GetProperty<T>` / `TryGetProperty<T>`.
- `BarcodeCaptureFeedback` — static `DefaultFeedback`, `Success`.
- `BarcodeCaptureSession` — `NewlyRecognizedBarcode`, `NewlyLocalizedBarcodes`, `FrameSequenceId`, `Reset()`.
- `IBarcodeCaptureListener` — `OnObservationStarted`, `OnObservationStopped`, `OnBarcodeScanned`, `OnSessionUpdated`.
- `BarcodeCaptureEventArgs` — `BarcodeCapture`, `Session`, `FrameData`.
- `BarcodeCaptureLicenseInfo` — `LicensedSymbologies`.
- `BarcodeCaptureOverlay` — `Create(barcodeCapture, view)`, `Create(barcodeCapture)`, `Brush`, static `DefaultBrush`, `Viewfinder`, `ShouldShowScanAreaGuides`, `SetProperty`.
