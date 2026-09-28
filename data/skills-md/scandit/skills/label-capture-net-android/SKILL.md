---
name: label-capture-net-android
description: Smart Label Capture (Scandit `LabelCapture`) in .NET for Android projects (`net*-android` target framework, `Scandit.DataCapture.Label` NuGet, C#) — extracting multiple fields (price, expiry date, serial or lot number, weight) from a label in one scan via barcode and text fields. Use for integration, label definitions (including prebuilt VIN, price label, 7-segment), captured-session handling, overlays, the Validation Flow, and Scandit .NET SDK version migration — for MAUI apps (`<UseMaui>true</UseMaui>`) use label-capture-net-maui instead.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.1"
---

# Label Capture (Smart Label Capture) .NET for Android Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit Label Capture APIs, and the **.NET binding differs substantially from the Kotlin/Java native Android SDK**. An agent that pattern-matches from the native Android (Kotlin) Label Capture docs will get nearly every call wrong, because the .NET binding does **not** use the Kotlin fluent settings builder — it builds each field with a per-field factory and assembles a list of definitions.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or builder shapes. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

The .NET-Android-specific facts most often gotten wrong by pattern-matching from the Kotlin/iOS SDK:

- This skill targets the **non-MAUI** .NET for Android workload (project `<TargetFramework>net10.0-android</TargetFramework>` or similar, **no** `<UseMaui>` flag). For MAUI apps, the `DataCaptureView` is hosted as a XAML element and wired through handlers — completely different. If you see `<UseMaui>true</UseMaui>`, **stop and tell the user this skill does not apply.**
- **There is NO `LabelCaptureSettings.builder()` fluent chain.** The Kotlin pattern `LabelCaptureSettings.builder().addLabel().addCustomBarcode().setSymbologies(...).buildFluent("x").buildFluent("label").build()` does **not** exist in .NET. Instead you: (1) build each field via its own factory, (2) collect them in a `List<LabelFieldDefinition>`, (3) `LabelDefinition.Create(name, fields)`, (4) `LabelCaptureSettings.Create(new List<LabelDefinition> { def })`.
- **Each field type is built with a static `Builder()` factory, then `.Build("field-name")`**: `CustomBarcode.Builder().SetSymbologies(IList<Symbology>).Build("Barcode")`, `ExpiryDateText.Builder().SetLabelDateFormat(...).Build("Expiry Date")`, `TotalPriceText.Builder().IsOptional(true).Build("Total Price")`, `CustomText.Builder().SetValueRegex("...").Build("Lot")`. The builder is shared-generic, so `IsOptional(bool)`, `SetValueRegex(es)`, `SetNumberOfMandatoryInstances(int?)` are available on every field builder; `SetSymbology(ies)` on barcode builders; `SetAnchorRegex(es)` / `SetLocation(...)` on custom fields.
- **`LabelCapture` is created with a FACTORY, not `new` and not `forDataCaptureContext`**: `LabelCapture.Create(dataCaptureContext, settings)`. The constructor is private.
- **Symbology names are C# PascalCase**: `Symbology.Ean13Upca`, `Symbology.Gs1DatabarExpanded`, `Symbology.Code128`, `Symbology.Code39`, `Symbology.Qr`, `Symbology.DataMatrix`. They are **not** the Kotlin underscore style (`EAN13_UPCA`). `Symbology` lives in `Scandit.DataCapture.Barcode.Data`.
- **`SetSymbologies` takes an `IList<Symbology>`** (e.g. `new List<Symbology> { ... }`), not a vararg. For one symbology use `SetSymbology(Symbology)`.
- **Only THREE NuGet packages, no separate text-models package.** `Scandit.DataCapture.Core`, `Scandit.DataCapture.Barcode`, and `Scandit.DataCapture.Label`. Text fields (expiry date, price, weight, custom text) are bundled in `Scandit.DataCapture.Label` — there is **no** `label-text-models` artifact like on native Android. (`Barcode` is always required because `Symbology` and the barcode field types live there.)
- **SDK 8.0+ requires explicit initialization with THREE initializers** in a `[Application]` subclass: `ScanditCaptureCore.Initialize()`, `ScanditBarcodeCapture.Initialize()`, **and `ScanditLabelCapture.Initialize()`** in `OnCreate()`. Missing the Label one crashes the first `LabelCapture.Create(...)` call. Label Capture is only available on `dotnet.android` since **8.1**, so this initializer always applies.
- **The view is a generic `DataCaptureView`, not a dedicated label view.** `DataCaptureView.Create(dataCaptureContext)`, add it to your layout with `container.AddView(...)`, then `dataCaptureView.AddOverlay(overlay)`. The overlay is created with `LabelCaptureBasicOverlay.Create(labelCapture)` (single-arg; the constructor does **not** require the view). There is no `LabelCaptureBasicOverlay.newInstance(mode, view)` two-arg native shape — use `Create(labelCapture)` then `AddOverlay`.
- **You manage the camera yourself.** `Camera.GetDefaultCamera(LabelCapture.RecommendedCameraSettings)`, `dataCaptureContext.SetFrameSourceAsync(camera)`, then `camera.SwitchToDesiredStateAsync(FrameSourceState.On)` / `FrameSourceState.Off` across the lifecycle. `RecommendedCameraSettings` is a **static property** on `LabelCapture`, not a method.
- **`ILabelCaptureListener.OnSessionUpdated(LabelCapture, LabelCaptureSession, IFrameData)`** is the result callback (plus optional `OnObservationStarted` / `OnObservationStopped`). The idiomatic C# alternative is the **`labelCapture.SessionUpdated` event** (`EventHandler<LabelCaptureEventArgs>`). `OnSessionUpdated` runs on a **background thread** — dispatch UI work to the main thread, and set `labelCapture.Enabled = false` after a successful capture to avoid re-capturing the same label.
- **Read field values via `LabelField`**: `field.Name`, `field.Barcode?.Data` (a `Barcode?`), `field.Text` (a `string?`), `field.Date` (a `LabelDate?` with `Year`/`Month`/`Day` ints and `*String` accessors). Match fields by the exact `Name` you passed to `.Build("...")`. `CapturedLabel` exposes `Fields`, `Name`, `Complete`, `TrackingId`. `LabelCaptureSession.CapturedLabels` is an `IList<CapturedLabel>`.
- **`LabelCaptureFeedback` exposes a single `Success` slot** (`Core.Common.Feedback.Feedback`) plus the static `LabelCaptureFeedback.Default` (a **property**). To customize: `var fb = LabelCaptureFeedback.Default; fb.Success = new Feedback(Vibration.DefaultVibration, null); labelCapture.Feedback = fb;`.
- **Android `SupportedOSPlatformVersion` must be ≥ `24`**; the activity must use a `Theme.AppCompat` descendant (the `CameraPermissionActivity` helper inherits from `AppCompatActivity`); and do **not** declare `<activity>` for `[Activity]`-decorated classes in `AndroidManifest.xml`. Same Android plumbing as any Scandit .NET Android app — see [references/integration.md](references/integration.md).

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating Label Capture from scratch, defining the label (fields, symbologies, regexes, optional vs required), creating the mode, hosting the `DataCaptureView` + `LabelCaptureBasicOverlay`, wiring the camera lifecycle, handling captured labels, customizing feedback or brushes, or using prebuilt definitions (VIN / price label / 7-segment)** (e.g. "add Smart Label Capture to my .NET Android app", "scan a barcode and an expiry date from a price tag in C#", "read the total price field", "use the recommended camera settings") → read [references/integration.md](references/integration.md) and follow it.
- **Enabling or customizing the Validation Flow** (e.g. "add the guided validation flow so users can review and correct fields", "let the user type a field that didn't scan", "customize the validation-flow hint text / button labels", "the keyboard covers the input field") → read [references/validation-flow.md](references/validation-flow.md) and follow it.

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
| Get Started | [Get Started (.NET for Android)](https://docs.scandit.com/sdks/net/android/label-capture/get-started/) |
| Label Definitions (fields, regex, presets) | [Label Definitions](https://docs.scandit.com/sdks/net/android/label-capture/label-definitions/) |
| Advanced topics (Validation Flow, adaptive recognition, advanced overlay) | [Advanced Configurations](https://docs.scandit.com/sdks/net/android/label-capture/advanced/) |
| Full API reference | [Label Capture API (.NET Android)](https://docs.scandit.com/data-capture-sdk/dotnet.android/label-capture/api.html) |

## API surface this skill covers

All classes documented with `:available: dotnet.android` in the official RST docs (`docs/source/label-capture/api/**`) are addressed in the references. Label Capture is available on `dotnet.android` since **8.1** (a few symbols since **8.2**).

- **`LabelCapture`** — static `Create(DataCaptureContext?, LabelCaptureSettings)`, `Context` (get), `Enabled` (get/set — set `true` to process frames, `false` after a capture), `ApplySettingsAsync(LabelCaptureSettings)` → `Task`, `AddListener` / `RemoveListener(ILabelCaptureListener)`, static `RecommendedCameraSettings` (property), `Feedback` (get/set), `event EventHandler<LabelCaptureEventArgs> SessionUpdated`, `Dispose()`.
- **`LabelCaptureSettings`** — static `Create(IList<LabelDefinition>)`, `LocationSelection` (get/set, `ILocationSelection?`), `GetSymbologySettings(Symbology)`, `SetProperty`/`GetProperty`/`GetProperty<T>`/`TryGetProperty<T>`, `Dispose`. **No settings builder.**
- **`LabelCaptureSession`** — `CapturedLabels` (`IList<CapturedLabel>`), `FrameSequenceId` (`long`), `LastProcessedFrameId` (`int`).
- **`ILabelCaptureListener`** — `OnSessionUpdated(LabelCapture, LabelCaptureSession, IFrameData)`, optional `OnObservationStarted(LabelCapture)` / `OnObservationStopped(LabelCapture)`.
- **`LabelCaptureEventArgs`** — `Mode`, `Session`, `FrameData`.
- **`LabelDefinition`** — static `Create(string name, IList<LabelFieldDefinition>)`; prebuilt `CreateVinLabelDefinition(name)`, `CreatePriceCaptureDefinition(name)`, `CreateSevenSegmentDisplayLabelDefinition(name)` (8.2); `Name`, `Fields`, `AdaptiveRecognitionMode` (get/set), `HiddenProperties`.
- **`LabelDefinitionBuilder`** — `AddCustomBarcode`/`AddSerialNumberBarcode`/`AddPartNumberBarcode`/`AddImeiOneBarcode`/`AddImeiTwoBarcode`/`AddCustomText`/`AddExpiryDateText`/`AddPackingDateText`/`AddDateText`/`AddTotalPriceText`/`AddUnitPriceText`/`AddWeightText`, `AdaptiveRecognition(AdaptiveRecognitionMode)`, `SetHiddenProperty/Properties`, `Build(name)`. (An alternative to passing the list directly to `LabelDefinition.Create`.)
- **Field types**, each with a static `Builder()` returning a fluent builder and `Build(string name)`:
  - Barcode fields: `CustomBarcode` (`SetSymbologies(IList<Symbology>)` / `SetSymbology(Symbology)`, `SetAnchorRegex(es)`, `SetLocation(...)`), `SerialNumberBarcode`, `PartNumberBarcode`, `ImeiOneBarcode`, `ImeiTwoBarcode` (preset symbologies/regexes).
  - Text fields: `CustomText` (`SetValueRegex(es)`, `SetAnchorRegex(es)`, `SetLocation(...)`), `ExpiryDateText` / `PackingDateText` / `DateText` (`SetLabelDateFormat(LabelDateFormat)`), `TotalPriceText`, `UnitPriceText`, `WeightText`.
  - Shared builder members (on all): `IsOptional(bool)`, `SetValueRegex(string)` / `SetValueRegexes(IList<string>)`, `SetNumberOfMandatoryInstances(int?)`, `SetHiddenProperty/Properties`.
- **`CapturedLabel`** — `Fields` (`IReadOnlyList<LabelField>`), `Name`, `Complete` (`bool`), `PredictedBounds` (`Quadrilateral`), `DeltaTimeToPrediction`, `TrackingId` (`int`).
- **`LabelField`** — `Name`, `Type` (`LabelFieldType`: `Barcode`/`Text`/`Unknown`), `State` (`LabelFieldState`: `Captured`/`Predicted`/`Unknown`), `Required` (`bool`), `Barcode` (`Barcode?`), `Text` (`string?`), `Date` (`LabelDate?`), `PredictedLocation` (`Quadrilateral`). (`ValueType` is iOS-only.)
- **`LabelDate`** — `Year`/`Month`/`Day` (`int?`), `DayString`/`MonthString`/`YearString`. **`LabelDateFormat`** — `new LabelDateFormat(LabelDateComponentFormat, bool acceptPartialDates)`, `ComponentFormat`, `AcceptPartialDates`. **`LabelDateComponentFormat`** enum (component ordering, e.g. `MDY`/`DMY`/`YMD`).
- **`LabelCaptureBasicOverlay`** — static `Create(LabelCapture)` / `Create(LabelCapture, DataCaptureView?)`; `Listener` (`ILabelCaptureBasicOverlayListener?`); `SetBrushForField`/`SetBrushForLabel`; `PredictedFieldBrush`/`CapturedFieldBrush`/`LabelBrush` (get/set) + static `Default*Brush`; `GetFieldBrush`/`SetFieldBrush(LabelFieldState, Brush?)`; `ShouldShowScanAreaGuides`; `Viewfinder` (`IViewfinder?`); `Dispose`.
- **`ILabelCaptureBasicOverlayListener`** — `BrushForField(overlay, field, label)`, `BrushForLabel(overlay, label)`, `OnLabelTapped(overlay, label)`.
- **Validation Flow** (see [references/validation-flow.md](references/validation-flow.md)): `LabelCaptureValidationFlowOverlay` (static `Create(LabelCapture, DataCaptureView?)`, `Listener`, `ApplySettings`, `OnResume`/`OnPause`, `ShouldHandleKeyboardInsetsInternally`), `LabelCaptureValidationFlowSettings` (static `Create()`, hint/button text props, `SetPlaceholderText`/`GetPlaceholderText`), `ILabelCaptureValidationFlowListener` (`OnValidationFlowLabelCaptured(IList<LabelField>)`, `OnManualInputSubmitted`, `OnValidationFlowResultUpdate`), `LabelResultUpdateType`.
- **`LabelCaptureFeedback`** — static `Default` (property), `Success` (`Core.Common.Feedback.Feedback`), `Dispose`.
- **`AdaptiveRecognitionMode`** enum — controls cloud-backed recognition for a definition (`Off` default).

### Advanced topics (available on `dotnet.android` but intentionally deferred to the docs)

These are real `dotnet.android` symbols but out of scope for a first integration — don't invent their shapes; fetch the [Advanced Configurations](https://docs.scandit.com/sdks/net/android/label-capture/advanced/) page if the user asks for them:

- **Adaptive Recognition (cloud backup):** `LabelCaptureAdaptiveRecognitionOverlay`, `LabelCaptureAdaptiveRecognitionSettings`, `ILabelCaptureAdaptiveRecognitionListener`, and the result types `AdaptiveRecognitionResult` / `AdaptiveRecognitionResultType` / `ReceiptScanningResult` / `ReceiptScanningLineItem`. Enabled per-definition via `AdaptiveRecognitionMode`.
- **Advanced overlay (arbitrary Android views over labels):** `LabelCaptureAdvancedOverlay`, `ILabelCaptureAdvancedOverlayListener`.
- **`LabelFieldLocation` / `LabelFieldLocationType`** — used with `SetLocation(...)` on custom field builders to constrain where a field is expected on the label.

### Documented for other platforms but NOT on `dotnet.android` — do not use

- **`LabelField.ValueType`** / `LabelFieldValueType` — iOS-only (`#if __IOS__` in the binding). On .NET Android use `Type` (`LabelFieldType`) plus the typed accessors `Barcode` / `Text` / `Date`.
- **The Kotlin `LabelCaptureSettings.builder()` / `.addLabel()` / `.buildFluent(...)` fluent API** — not present in .NET. Use `LabelDefinition.Create` + `LabelCaptureSettings.Create`.
- **Native `LabelFieldDefinitionBuilder` regex method names** (`setPattern`, `setDataTypePattern`) — those are the old native names. In .NET use `SetValueRegex(es)` (value) and `SetAnchorRegex(es)` (anchor/context).
