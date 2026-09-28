---
name: matrixscan-count-flutter
description: MatrixScan Count (BarcodeCount) in Flutter projects — scandit_flutter_datacapture_barcode_count package. Multi-barcode counting and receiving workflows (scan-and-count, counting against a target list, status providers) with the BarcodeCountView widget. Use for integration, scan settings, result handling, UI customization, SDK version migration, or troubleshooting counting workflows.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Count Flutter Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeCount API changes between major SDK versions — class names, constructor signatures, listener interfaces, and the Flutter plugin import path have all evolved.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Flutter-specific gotchas worth flagging:

- `await ScanditFlutterDataCaptureBarcode.initialize()` **must** be called (and awaited) in `main()` before `runApp(...)`, after `WidgetsFlutterBinding.ensureInitialized()`. Forgetting this yields a platform-channel error that can look unrelated to initialization.
- `BarcodeCountView` is a Flutter `StatefulWidget`. The sample creates it inline in `build()` using the cascade `..uiListener = _bloc ..listener = _bloc` — this is correct for BarcodeCount because the view is not torn down on rebuild in the same way as BarcodeArView. However, storing it as a field in `initState()` is also acceptable for clarity.
- `BarcodeCount(settings)` is the context-free constructor available on Flutter ≥7.6. On older SDKs (Flutter 6.17–7.5) you must use `BarcodeCount.forDataCaptureContext(context, settings)` which returns a `Future<BarcodeCount>` — **await** it before adding listeners. After ≥7.6, call `dataCaptureContext.setMode(barcodeCount)` explicitly when using the context-free constructor.
- The BLoC owns `DataCaptureContext`, `BarcodeCount`, and the camera lifecycle. The BLoC also implements `BarcodeCountListener`, `BarcodeCountViewListener`, and `BarcodeCountViewUiListener`.
- The BarcodeCount import barrel is `scandit_flutter_datacapture_barcode_count` — a separate barrel from `scandit_flutter_datacapture_barcode`. Always import both.
- `Symbology` enum values use **lowerCamelCase** in Dart: `Symbology.code128`, `Symbology.ean13Upca`, `Symbology.code39`. Do not write `Symbology.Code128` / `Symbology.EAN13UPCA` — that is the JS/TS form and will not compile in Dart.
- **Flutter-only listener methods**: `BarcodeCountListener` on Flutter ≥8.3 has an extended interface `IBarcodeCountExtendedListener` that adds `didUpdateSession`. `BarcodeCountCaptureListListener` on Flutter ≥8.3 has `IBarcodeCountCaptureListExtendedListener` that adds `didCompleteCaptureList`. These are Flutter-exclusive additions.
- `BarcodeCountView` must be presented full screen per the SDK documentation.
- Camera permission is required on both iOS (`NSCameraUsageDescription` in `ios/Runner/Info.plist`) and Android (runtime request via `permission_handler`).
- Min SDK callouts: BarcodeCount Flutter 6.17; context-free constructor 7.6; Status mode 7.0 (earliest on Flutter); Mapping flow 8.3; Not-in-list action settings 8.3; `TextForBarcodesNotInListDetectedHint` 8.3; `TextForClusteringGestureHint` 8.3; `shouldDisableModeOnExitButtonTapped` 8.3.
- License placeholder must be exactly: `'-- ENTER YOUR SCANDIT LICENSE KEY HERE --'`

## Intent Routing

Based on the user's request, load the reference file before responding:

- **Integrating BarcodeCount from scratch** (e.g. "add MatrixScan Count to my app", "set up barcode counting", "how do I use BarcodeCount in Flutter", "how do I count barcodes", "scanning against a list") → read [references/integration.md](references/integration.md) and follow the instructions there.

- **Migrating from an older BarcodeCount constructor or adding newer features** (e.g. "migrate from forDataCaptureContext", "update BarcodeCount constructor", "add status mode", "add mapping flow", "not-in-list actions") → read [references/migration.md](references/migration.md) and follow the guide there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if an analyzer / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it.
2. If no direct link was found, fetch the API index and extract the actual link from it.

## Framework variant policy

Flutter apps use many state-management patterns (StatefulWidget, BLoC, Provider, Riverpod). Examples in this skill use the **BLoC pattern** because it matches the official `MatrixScanCountSimpleSample`, keeps the scan pipeline cleanly separated from the widget tree, and composes well with the camera lifecycle. If the target project already uses a different pattern, keep the BarcodeCount wiring conceptually the same (one owner holds `DataCaptureContext`, `BarcodeCount`, and exposes session data to the UI) and port the code snippets into the project's existing convention.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Flutter integration | [Get Started](https://docs.scandit.com/sdks/flutter/matrixscan-count/get-started/) · [Sample](https://github.com/Scandit/datacapture-flutter-samples/tree/master/03_Advanced_Batch_Scanning_Samples/02_Counting_and_Receiving/MatrixScanCountSimpleSample) |
| Full API reference | [BarcodeCount API](https://docs.scandit.com/data-capture-sdk/flutter/barcode-capture/api.html) |
