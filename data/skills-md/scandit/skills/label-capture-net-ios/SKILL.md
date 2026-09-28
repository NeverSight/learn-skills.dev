---
name: label-capture-net-ios
description: Smart Label Capture (Scandit `LabelCapture`) in .NET for iOS projects (`net*-ios` target framework, `Scandit.DataCapture.Label` NuGet, C#) — extracting multiple fields (price, expiry date, serial or lot number, weight) from a label in one scan via barcode and text fields. Use for integration, label definitions (including prebuilt VIN, price label, 7-segment), captured-session handling, overlays, the Validation Flow, and Scandit .NET SDK version migration — for MAUI apps (`<UseMaui>true</UseMaui>`) use label-capture-net-maui instead.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.1"
---

# Label Capture (Smart Label Capture) .NET for iOS Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit Label Capture APIs, and the **.NET binding differs substantially from the Swift/Objective-C native iOS SDK** *and* from the .NET for Android binding. An agent that pattern-matches from the native iOS (Swift) Label Capture docs will get nearly every call wrong, because the .NET binding does **not** use the Swift fluent settings builder — it builds each field with a per-field factory and assembles a list of definitions.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or builder shapes. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

The .NET-iOS-specific facts most often gotten wrong by pattern-matching from the Swift SDK, the .NET Android binding, or MAUI:

- This skill targets the **non-MAUI** .NET for iOS workload (project `<TargetFramework>net10.0-ios</TargetFramework>` or similar, **no** `<UseMaui>` flag). For MAUI apps, the `DataCaptureView` is hosted as a XAML element and wired through handlers — completely different. If you see `<UseMaui>true</UseMaui>`, **stop and tell the user this skill does not apply.** The official iOS Get Started page mixes in MAUI (XAML / `*.Maui`) snippets — ignore those for a non-MAUI project.
- **There is NO `LabelCaptureSettings.builder()` fluent chain.** The Swift/Kotlin pattern `LabelCaptureSettings.settings { ... }` / `builder().addLabel()...buildFluent(...).build()` does **not** exist in .NET. Instead you: (1) build each field via its own factory, (2) collect them in a `List<LabelFieldDefinition>`, (3) `LabelDefinition.Create(name, fields)`, (4) `LabelCaptureSettings.Create(new List<LabelDefinition> { def })`.
- **Each field type is built with a static `Builder()` factory, then `.Build("field-name")`**: `CustomBarcode.Builder().SetSymbologies(IList<Symbology>).Build("Barcode")`, `ExpiryDateText.Builder().SetLabelDateFormat(...).Build("Expiry Date")`, `TotalPriceText.Builder().IsOptional(true).Build("Total Price")`, `CustomText.Builder().SetValueRegex("...").Build("Lot")`. The builder is shared-generic, so `IsOptional(bool)`, `SetValueRegex(es)`, `SetNumberOfMandatoryInstances(int?)` are available on every field builder; `SetSymbology(ies)` on barcode builders; `SetAnchorRegex(es)` / `SetLocation(...)` on custom fields.
- **`LabelCapture` is created with a FACTORY, not `new` and not `forDataCaptureContext`**: `LabelCapture.Create(dataCaptureContext, settings)`. The constructor is private.
- **`DataCaptureView.Create(DataCaptureContext, CGRect frame)` takes a `CGRect` as its second argument on iOS** — typically `this.View!.Bounds`. This is the **opposite** of the .NET Android binding, where `DataCaptureView.Create(context)` takes only the context. The returned view **is** a `UIKit.UIView` (implicit conversion), so you add it yourself with `this.View.AddSubview(dataCaptureView)` and usually set `AutoresizingMask = FlexibleWidth | FlexibleHeight`. There is no `container.AddView(...)` (that's Android).
- **Symbology names are C# PascalCase**: `Symbology.Ean13Upca`, `Symbology.Gs1DatabarExpanded`, `Symbology.Code128`, `Symbology.Code39`, `Symbology.Qr`, `Symbology.DataMatrix`. They are **not** the Swift `.ean13UPCA` / `.code128` style. `Symbology` lives in `Scandit.DataCapture.Barcode.Data`.
- **`SetSymbologies` takes an `IList<Symbology>`** (e.g. `new List<Symbology> { ... }`), not a vararg. For one symbology use `SetSymbology(Symbology)`.
- **Only THREE NuGet packages, no separate text-models package.** `Scandit.DataCapture.Core`, `Scandit.DataCapture.Barcode`, and `Scandit.DataCapture.Label`. Text fields (expiry date, price, weight, custom text) are bundled in `Scandit.DataCapture.Label` — there is **no** `label-text-models` artifact like on native iOS. (`Barcode` is always required because `Symbology` and the barcode field types live there.) Do **not** add any `*.Maui` package.
- **SDK 8.0+ requires explicit initialization with THREE initializers** in `AppDelegate.FinishedLaunching` (`application:didFinishLaunchingWithOptions:`): `ScanditCaptureCore.Initialize()`, `ScanditBarcodeCapture.Initialize()`, **and `ScanditLabelCapture.Initialize()`** before any Scandit type is constructed. Missing the Label one crashes the first `LabelCapture.Create(...)` call. Label Capture is only available on `dotnet.ios` since **8.2**, so this initializer always applies.
- **You manage the camera yourself; the view does not own it.** `Camera.GetDefaultCamera(LabelCapture.RecommendedCameraSettings)`, `dataCaptureContext.SetFrameSourceAsync(camera)`, then `camera.SwitchToDesiredStateAsync(FrameSourceState.On / .Standby / .Off)` across the `UIViewController` lifecycle. `RecommendedCameraSettings` is a **static property** on `LabelCapture`, not a method. iOS additionally has `FrameSourceState.Standby` (a lighter pause for in-app navigation, keeps the camera warm) versus `.Off` when backgrounding.
- **iOS lifecycle is `UIViewController`, not an Android Activity.** Toggle the camera and `labelCapture.Enabled` in `ViewWillAppear`/`ViewWillDisappear`. Keep `ViewDidLoad` **synchronous** (fire-and-forget the async camera setup) — an `async void ViewDidLoad` returns to UIKit at the first `await`, so `ViewWillAppear` runs before the mode/camera are constructed.
- **`ILabelCaptureListener.OnSessionUpdated(LabelCapture, LabelCaptureSession, IFrameData)`** is the result callback (plus optional `OnObservationStarted` / `OnObservationStopped`). The idiomatic C# alternative is the **`labelCapture.SessionUpdated` event** (`EventHandler<LabelCaptureEventArgs>`). `OnSessionUpdated` runs on a **background thread** — dispatch UI work to the main thread with **`UIApplication.SharedApplication.InvokeOnMainThread(...)`** or **`DispatchQueue.MainQueue.DispatchAsync(...)`** (**not** Android's `RunOnUiThread`), and set `labelCapture.Enabled = false` after a successful capture to avoid re-capturing the same label. A listener implementation derives from **`NSObject`** (not Android's `Java.Lang.Object`).
- **Read field values via `LabelField`**: `field.Name`, `field.Barcode?.Data` (a `Barcode?`), `field.Text` (a `string?`), `field.Date` (a `LabelDate?` with `Year`/`Month`/`Day` ints and `*String` accessors). On iOS there is an **extra `field.ValueType` (`LabelFieldValueType`: `Date`/`Price`/`Weight`/`Text`/`Numeric`)** that does not exist on .NET Android. Match fields by the exact `Name` you passed to `.Build("...")`. `CapturedLabel` exposes `Fields`, `Name`, `Complete`, `TrackingId`. `LabelCaptureSession.CapturedLabels` is an `IList<CapturedLabel>`.
- **`LabelCaptureFeedback` exposes a single `Success` slot** (`Core.Common.Feedback.Feedback`) plus the static `LabelCaptureFeedback.Default` (a **property**). To customize: `var fb = LabelCaptureFeedback.Default; fb.Success = new Feedback(Vibration.DefaultVibration, null); labelCapture.Feedback = fb;`.
- **Camera permission is handled by iOS automatically** via the `NSCameraUsageDescription` key in `Info.plist`. The OS shows the permission prompt the first time the camera switches on. There is **no** runtime-permission helper class (that's the Android binding's `CameraPermissionActivity`). If `NSCameraUsageDescription` is missing, the app crashes when the camera starts.
- **iOS `SupportedOSPlatformVersion` must be ≥ `15.0`** in the `.csproj` (the Scandit iOS framework's minimum deployment target); the matching `MinimumOSVersion` goes in `Info.plist`.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating Label Capture from scratch, defining the label (fields, symbologies, regexes, optional vs required), creating the mode, hosting the `DataCaptureView` + `LabelCaptureBasicOverlay`, wiring the camera lifecycle, handling captured labels, customizing feedback or brushes, or using prebuilt definitions (VIN / price label / 7-segment)** (e.g. "add Smart Label Capture to my .NET iOS app", "scan a barcode and an expiry date from a price tag in C#", "read the total price field", "use the recommended camera settings") → read [references/integration.md](references/integration.md) and follow it.
- **Enabling or customizing the Validation Flow** (e.g. "add the guided validation flow so users can review and correct fields", "let the user type a field that didn't scan", "customize the validation-flow hint text / button labels") → read [references/validation-flow.md](references/validation-flow.md) and follow it.
- **Customizing overlay appearance (per-field / per-label brushes, tap handling), adding an advanced overlay with custom native views over labels (AR), enabling Adaptive Recognition cloud fallback (beta), or Receipt Scanning (beta)** (e.g. "tint the barcode highlight a different color than the expiry date", "show a warning view under expiry dates close to expiring", "add cloud fallback / ARE", "scan receipts") → read [references/advanced-overlays.md](references/advanced-overlays.md) and follow it. Adaptive Recognition and Receipt Scanning are **beta** and subscription-gated — always flag this.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, builder shapes, or property names. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures can vary (e.g. an `api/ui/` subdirectory) and guessing will lead to 404s.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Get Started | [Get Started (.NET for iOS)](https://docs.scandit.com/sdks/net/ios/label-capture/get-started/) |
| Label Definitions (fields, regex, presets) | [Label Definitions](https://docs.scandit.com/sdks/net/ios/label-capture/label-definitions/) |
| Advanced topics (Validation Flow, adaptive recognition, advanced overlay) | [Advanced Configurations](https://docs.scandit.com/sdks/net/ios/label-capture/advanced/) |
| Full API reference | [Label Capture API (.NET iOS)](https://docs.scandit.com/data-capture-sdk/dotnet.ios/label-capture/api.html) |

## API surface this skill covers

All classes documented with `:available: dotnet.ios` in the official RST docs (`docs/source/label-capture/api/**`) are addressed in the references. Label Capture is available on `dotnet.ios` since **8.2**.

- **`LabelCapture`** — static `Create(DataCaptureContext?, LabelCaptureSettings)`, `Context` (get), `Enabled` (get/set — set `true` to process frames, `false` after a capture), `ApplySettingsAsync(LabelCaptureSettings)` → `Task`, `AddListener` / `RemoveListener(ILabelCaptureListener)`, static `RecommendedCameraSettings` (property), `Feedback` (get/set), `event EventHandler<LabelCaptureEventArgs> SessionUpdated`, `Dispose()`.
- **`LabelCaptureSettings`** — static `Create(IList<LabelDefinition>)`, `LocationSelection` (get/set, `ILocationSelection?`), `GetSymbologySettings(Symbology)`, `SetProperty`/`GetProperty`/`GetProperty<T>`/`TryGetProperty<T>`, `Dispose`. **No settings builder.**
- **`LabelCaptureSession`** — `CapturedLabels` (`IList<CapturedLabel>`), `FrameSequenceId` (`long`), `LastProcessedFrameId` (`int`).
- **`ILabelCaptureListener`** — `OnSessionUpdated(LabelCapture, LabelCaptureSession, IFrameData)`, optional `OnObservationStarted(LabelCapture)` / `OnObservationStopped(LabelCapture)`. Implementations derive from `NSObject`.
- **`LabelCaptureEventArgs`** — `Mode`, `Session`, `FrameData`.
- **`LabelDefinition`** — static `Create(string name, IList<LabelFieldDefinition>)`; prebuilt `CreateVinLabelDefinition(name)`, `CreatePriceCaptureDefinition(name)`, `CreateSevenSegmentDisplayLabelDefinition(name)`; `Name`, `Fields`, `AdaptiveRecognitionMode` (get/set), `HiddenProperties`.
- **`LabelDefinitionBuilder`** — `AddCustomBarcode`/`AddSerialNumberBarcode`/`AddPartNumberBarcode`/`AddImeiOneBarcode`/`AddImeiTwoBarcode`/`AddCustomText`/`AddExpiryDateText`/`AddPackingDateText`/`AddDateText`/`AddTotalPriceText`/`AddUnitPriceText`/`AddWeightText`, `AdaptiveRecognition(AdaptiveRecognitionMode)`, `SetHiddenProperty/Properties`, `Build(name)`. (An alternative to passing the list directly to `LabelDefinition.Create`.)
- **Field types**, each with a static `Builder()` returning a fluent builder and `Build(string name)`:
  - Barcode fields: `CustomBarcode` (`SetSymbologies(IList<Symbology>)` / `SetSymbology(Symbology)`, `SetAnchorRegex(es)`, `SetLocation(...)`), `SerialNumberBarcode`, `PartNumberBarcode`, `ImeiOneBarcode`, `ImeiTwoBarcode` (preset symbologies/regexes).
  - Text fields: `CustomText` (`SetValueRegex(es)`, `SetAnchorRegex(es)`, `SetLocation(...)`), `ExpiryDateText` / `PackingDateText` / `DateText` (`SetLabelDateFormat(LabelDateFormat)`), `TotalPriceText`, `UnitPriceText`, `WeightText`.
  - Shared builder members (on all): `IsOptional(bool)`, `SetValueRegex(string)` / `SetValueRegexes(IList<string>)`, `SetNumberOfMandatoryInstances(int?)`, `SetHiddenProperty/Properties`.
- **`CapturedLabel`** — `Fields` (`IReadOnlyList<LabelField>`), `Name`, `Complete` (`bool`), `PredictedBounds` (`Quadrilateral`), `DeltaTimeToPrediction`, `TrackingId` (`int`).
- **`LabelField`** — `Name`, `Type` (`LabelFieldType`: `Barcode`/`Text`/`Unknown`), **`ValueType` (`LabelFieldValueType`: `Date`/`Price`/`Weight`/`Text`/`Numeric`, iOS-only)**, `State` (`LabelFieldState`: `Captured`/`Predicted`/`Unknown`), `Required` (`bool`), `Barcode` (`Barcode?`), `Text` (`string?`), `Date` (`LabelDate?`), `PredictedLocation` (`Quadrilateral`).
- **`LabelDate`** — `Year`/`Month`/`Day` (`int?`), `DayString`/`MonthString`/`YearString`. **`LabelDateFormat`** — `new LabelDateFormat(LabelDateComponentFormat, bool acceptPartialDates)`, `ComponentFormat`, `AcceptPartialDates`. **`LabelDateComponentFormat`** enum (component ordering, e.g. `MDY`/`DMY`/`YMD`).
- **`LabelCaptureBasicOverlay`** — static `Create(LabelCapture)` / `Create(LabelCapture, DataCaptureView?)`; `Listener` (`ILabelCaptureBasicOverlayListener?`); `SetBrushForField`/`SetBrushForLabel`; `PredictedFieldBrush`/`CapturedFieldBrush`/`LabelBrush` (get/set) + static `Default*Brush`; `GetFieldBrush`/`SetFieldBrush(LabelFieldState, Brush?)`; `ShouldShowScanAreaGuides`; `Viewfinder` (`IViewfinder?`); `Dispose`.
- **`ILabelCaptureBasicOverlayListener`** — `BrushForField(overlay, field, label)`, `BrushForLabel(overlay, label)`, `OnLabelTapped(overlay, label)`.
- **Validation Flow** (see [references/validation-flow.md](references/validation-flow.md)): `LabelCaptureValidationFlowOverlay` (static `Create(LabelCapture, DataCaptureView?)`, `Listener`, `ApplySettings`; `OnResume`/`OnPause` and `ShouldHandleKeyboardInsetsInternally` exist but are **Android-only no-ops on iOS**), `LabelCaptureValidationFlowSettings` (static `Create()`, hint/button text props, `SetPlaceholderText`/`GetPlaceholderText`), `ILabelCaptureValidationFlowListener` (`OnValidationFlowLabelCaptured(IList<LabelField>)`, `OnManualInputSubmitted`, `OnValidationFlowResultUpdate`), `LabelResultUpdateType`.
- **`LabelCaptureFeedback`** — static `Default` (property), `Success` (`Core.Common.Feedback.Feedback`), `Dispose`.
- **`AdaptiveRecognitionMode`** enum — controls cloud-backed recognition for a definition (`Off` default).

### Advanced topics (available on `dotnet.ios` but intentionally deferred to the docs)

These are real `dotnet.ios` symbols but out of scope for a first integration — don't invent their shapes; fetch the [Advanced Configurations](https://docs.scandit.com/sdks/net/ios/label-capture/advanced/) page if the user asks for them:

- **Adaptive Recognition (cloud backup):** `LabelCaptureAdaptiveRecognitionOverlay`, `LabelCaptureAdaptiveRecognitionSettings`, `ILabelCaptureAdaptiveRecognitionListener`, and the result types `AdaptiveRecognitionResult` / `AdaptiveRecognitionResultType` / `ReceiptScanningResult` / `ReceiptScanningLineItem`. Enabled per-definition via `AdaptiveRecognitionMode`.
- **Advanced overlay (arbitrary native views over labels):** `LabelCaptureAdvancedOverlay`, `ILabelCaptureAdvancedOverlayListener`.
- **`LabelFieldLocation` / `LabelFieldLocationType`** — used with `SetLocation(...)` on custom field builders to constrain where a field is expected on the label.

### iOS vs Android binding differences (do not cross-pollinate)

- **`DataCaptureView` factory**: iOS `DataCaptureView.Create(context, CGRect frame)` + `this.View.AddSubview(view)`; Android `DataCaptureView.Create(context)` + `container.AddView(view)`. Using a bare `Create(context)` on iOS won't compile, and `AddView` doesn't exist on `UIView`.
- **Host & lifecycle**: iOS `UIViewController` (`ViewDidLoad`/`ViewWillAppear`/`ViewWillDisappear`); Android `Activity` (`OnCreate`/`OnResume`/`OnPause`). No `CameraPermissionActivity` on iOS — permission is automatic via `NSCameraUsageDescription`.
- **SDK init**: iOS `AppDelegate.FinishedLaunching`; Android `MainApplication.OnCreate`.
- **Main-thread dispatch**: iOS `UIApplication.SharedApplication.InvokeOnMainThread(...)` / `DispatchQueue.MainQueue.DispatchAsync(...)`; Android `RunOnUiThread(...)`.
- **Listener base class**: iOS `NSObject`; Android `Java.Lang.Object`.
- **`LabelField.ValueType`** (`LabelFieldValueType`) is **iOS-only** — it does not exist on .NET Android.
- **Validation Flow lifecycle**: `overlay.OnResume()` / `overlay.OnPause()` and `ShouldHandleKeyboardInsetsInternally` are **Android-specific** — on iOS they are no-ops. Do **not** call them in an iOS integration.
