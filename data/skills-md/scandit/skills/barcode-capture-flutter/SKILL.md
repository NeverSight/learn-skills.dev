---
name: barcode-capture-flutter
description: Scandit Barcode Capture (`BarcodeCapture`) in Flutter (Dart) projects — the low-level, full-control single-barcode scanning mode (BarcodeCapture + DataCaptureView + BarcodeCaptureOverlay), without the pre-built SparkScan UI. Use for integration, scan settings, result handling, overlay customization, SDK version migration, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# BarcodeCapture Flutter Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeCapture API changes significantly between major SDK versions — properties get renamed, removed, or restructured, and the Flutter plugin surface (imports, plugin initialization, pub packages) has also evolved.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Flutter-specific gotchas worth flagging:
- `await ScanditFlutterDataCaptureBarcode.initialize()` **must** be called (and awaited) in `main()` before `runApp(...)`, after `WidgetsFlutterBinding.ensureInitialized()`. Forgetting this yields a platform-channel error that can look unrelated to initialization.
- A single `DataCaptureContext` must own the `BarcodeCapture` mode and the `DataCaptureView`. Do not construct multiple contexts per page or per `MaterialApp`; the BLoC / controller that holds the context should outlive any single `State`.
- The `DataCaptureView` is a Flutter `Widget` returned from `DataCaptureView.forContext(context)` — you must explicitly add the `BarcodeCaptureOverlay` to it via `view.addOverlay(...)`. Unlike SparkScan, there is no pre-built scanning UI; the overlay is the only thing that visualizes recognized barcodes on the camera preview.
- `BarcodeCaptureListener.didScan(...)` blocks the recognition pipeline until it returns. Disable the mode (`barcodeCapture.isEnabled = false`) before doing any meaningful work in the callback, and re-enable it (or stop the camera) when finished — otherwise duplicate / unwanted scan events will fire.
- The `getFrameData` parameter on the Flutter listener is a `Future<FrameData?> Function()` — frame data is fetched lazily. Only invoke it if you actually need the frame data, since it crosses the platform channel.
- `flutter pub get` must be run after every package version change. On iOS, the Podfile resolves transitively — no manual pod install needed unless the user has a custom setup.
- Camera permission is required on both iOS (`NSCameraUsageDescription` in `ios/Runner/Info.plist`) and Android (runtime request via `permission_handler` — the plugin declares the manifest permission automatically).
- Hot-reload does not re-run `main()`, so the camera lifecycle (and the `ScanditFlutterDataCaptureBarcode.initialize()` call) survive a hot reload. A full restart is needed to re-trigger plugin init. Drive `camera.switchToDesiredState(...)` from `WidgetsBindingObserver.didChangeAppLifecycleState` so the camera turns off in `paused` and back on in `resumed`.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeCapture from scratch** (e.g. "add BarcodeCapture to my app", "set up barcode scanning", "how do I use BarcodeCapture in Flutter", "how do I handle the camera in BarcodeCapture") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing BarcodeCapture integration** (e.g. "upgrade from v6 to v7", "migrate my BarcodeCapture", "bump the Scandit packages to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if an analyzer / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched (e.g. the Advanced Configurations page) contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and package paths (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## Framework variant policy

Flutter apps use many state-management patterns (StatefulWidget, BLoC, Provider, Riverpod). Examples in this skill use the **BLoC pattern** because it matches the official Scandit Flutter samples, keeps the scan pipeline cleanly separated from the widget tree, and composes well with the camera lifecycle. If the target project already uses a different pattern (Provider, Riverpod, GetX, plain StatefulWidget), keep the BarcodeCapture wiring conceptually the same (one owner holds `DataCaptureContext`, `BarcodeCapture`, the `Camera`, and exposes scan events to the UI) and port the code snippets into the project's existing convention — do not rewrite the project's state management.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Flutter integration | [Get Started](https://docs.scandit.com/sdks/flutter/barcode-capture/get-started/) · [Samples](https://github.com/Scandit/datacapture-flutter-samples) |
| Advanced topics (custom feedback, viewfinders, location selection, scan intention, composite codes) | [Advanced Configurations](https://docs.scandit.com/sdks/flutter/barcode-capture/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/flutter/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/flutter/migrate-7-to-8/) |
| Full API reference | [BarcodeCapture API](https://docs.scandit.com/data-capture-sdk/flutter/barcode-capture/api.html) |
