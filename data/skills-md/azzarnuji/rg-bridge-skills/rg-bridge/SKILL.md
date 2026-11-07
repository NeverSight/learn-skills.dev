---
name: rg-bridge
description: Use when integrating or debugging the rg_bridge Flutter SDK (RGBridge) — device info, 16 hardware tests (touchscreen, sensors, camera, mic, GPS, WiFi, Bluetooth, biometric, buttons), the WebView JS bridge, form submission, desk inbox, and QR take-photo file transfer. Covers initialization, one-screen-per-test structure, the mandatory camera/touchscreen library widgets, controller lifecycle, result streams, REQUIRES_USER_ACTION, permissions, and troubleshooting.
---

# RGBridge Flutter SDK

`rg_bridge` is a Flutter package that exposes three public surfaces on one
`RGBridge` instance:

| Surface | Access | Needs `baseUrl` | Purpose |
|---|---|---|---|
| Device | `sdk.device` | No | Device info + 16 hardware tests |
| WebView | `sdk.webview` | Yes | Session, controller, JS ↔ Dart events |
| Form | `sdk.formSubmission` | Yes | Init session + submit form |
| Desk | `sdk.desk` | Yes | Customer inbox URL |
| QR | `sdk.qr` | Yes | Take-photo QR + file transfer |

## When to use this skill

Use for any task that:

- adds `rg_bridge` to a Flutter app, or initializes `RGBridge(...)`;
- runs a hardware capability test and needs result handling;
- builds a WebView flow backed by an rg_bridge session;
- submits an rg_bridge form, creates a desk inbox, or starts a take-photo QR;
- debugs `NOT_SUPPORTED`, timeouts, missing events, or dispose issues.

Do not use for unrelated Flutter plugin work.

## Non-negotiable rules

1. Import only the public barrel: `package:rg_bridge/rg_bridge.dart`.
   Never import `package:rg_bridge/src/...` from app code — except the
   documented `CheckCameraWidget` fallback in rule 10.
2. Create **one** `RGBridge` instance for the app (or per service), not one per
   screen.
3. Hardware results arrive only through `controller.getResultStream`.
   Subscribe **before** `checkStart()`.
4. `REQUIRES_USER_ACTION` is intermediate. Only act on
   `result.status.isTerminal`.
5. Always `checkDispose()` device controllers in `dispose()`. Call
   `sdk.webview.offAllEvents()` when leaving a WebView flow.
6. Only load trusted URLs/HTML in the WebView. Never log session tokens, form
   values, or PII.
7. Never hardcode real `clientId` values in committed code or docs; use
   placeholders / `String.fromEnvironment`.
8. The legacy README shows outdated WebView signatures. Trust this skill and
   the source (`lib/src/addons/...`) over old docs.
9. Every hardware test runs in its **own host-built screen**
   (`Check<Test>Screen`). The screen owns creation, subscription, start, and
   dispose of its controller. The only exception to host-built screens is
   `camera` and `touchscreen`: both **must** render the library widgets
   `CheckCameraWidget` / `CheckTouchscreenWidget` — never re-implement their
   UI and never run those two tests controller-only.
10. `CheckCameraWidget` must come from the barrel. If the host's `rg_bridge`
   version predates its export, importing
   `package:rg_bridge/src/addons/device/check_camera/check_camera_widget.dart`
   is the single allowed `src/` exception; record it as temporary and upgrade
   the package instead of copying the widget.

## Install and initialize

Published on pub.dev: https://pub.dev/packages/rg_bridge

```bash
flutter pub add rg_bridge
```

```yaml
dependencies:
  rg_bridge: ^0.1.1
```

```dart
final sdk = RGBridge(
  baseUrl: 'https://api.example.com',
  clientId: 'rg_your_client_id',
);
```

Device-only code may omit `baseUrl`. WebView, Form, Desk, and QR require a
valid `baseUrl` + `clientId`.

## Device-test screens (required)

Every test gets its own screen. The host builds the screen (route, layout,
buttons); the screen owns the controller lifecycle.

```dart
// import 'dart:async';
// import 'package:rg_bridge/rg_bridge.dart';
class CheckWifiScreen extends StatefulWidget {
  const CheckWifiScreen({super.key, required this.sdk});
  final RGBridge sdk;

  @override
  State<CheckWifiScreen> createState() => _CheckWifiScreenState();
}

class _CheckWifiScreenState extends State<CheckWifiScreen> {
  late final _controller = widget.sdk.device.checkWifi();
  StreamSubscription<DeviceTestResult>? _sub;
  DeviceTestResult? _result;

  @override
  void initState() {
    super.initState();
    // Subscribe BEFORE start.
    _sub = _controller.getResultStream.listen((result) {
      if (!mounted) return;
      if (!result.status.isTerminal) {
        // REQUIRES_USER_ACTION — show instructions, keep waiting.
        setState(() => _result = result);
        return;
      }
      setState(() => _result = result);
    });
    _controller.checkStart(); // fire-and-forget; never await a result.
  }

  @override
  void dispose() {
    _sub?.cancel();
    _controller.checkDispose();
    super.dispose();
  }
  // build(): host UI + notifiers, e.g. checkRequestEnable/checkNotifyScan.
}
```

### Library widgets (mandatory for camera & touchscreen)

| Widget | Test | Rule |
|---|---|---|
| `CheckCameraWidget` | `camera` | **Mandatory.** Host pushes it as a route. |
| `CheckTouchscreenWidget` | `touchscreen` | **Mandatory.** Host pushes it as a route. |
| `TakePhotoQrWidget` | QR photo | QR surface, not a hardware test. |

All other tests are **host-built screens**: the host writes the UI and calls the
controller notifiers (`checkVerifyGuess`, `checkNotify*`, ...).
`navigation_button` is host-built as well (`PopScope` +
`WidgetsBindingObserver`); the library ships no navigation screen.

```dart
// camera — do not rebuild this UI yourself
final result = await Navigator.of(context).push<DeviceTestResult>(
  MaterialPageRoute(
    builder: (_) => CheckCameraWidget(
      checkIsFront: false,
      onCheckFinished: (r) => Navigator.of(context).pop(r),
    ),
  ),
);

// touchscreen — do not rebuild this UI yourself
final result = await Navigator.of(context).push<DeviceTestResult>(
  MaterialPageRoute(
    builder: (_) => CheckTouchscreenWidget(
      columns: 15,
      rows: 26,
      timeout: const Duration(seconds: 60),
      onCheckFinished: (r) => Navigator.of(context).pop(r),
    ),
  ),
);
```

The per-test screen table lives in `references/device-tests.md`.

Status wire values: `PASS`, `FAILED`, `SKIPPED`, `NOT_SUPPORTED`,
`REQUIRES_USER_ACTION`. `DeviceTestStatus.isTerminal` excludes the last one.

Test ids: `touchscreen`, `accelerometer`, `gyroscope`, `biometric`,
`bluetooth`, `wifi`, `gps`, `camera`, `speaker`, `vibration`, `speech`,
`microphone`, `flashlight`, `navigation_button`, `power`, `volume_button`.

## Canonical WebView recipe

```dart
final session = await sdk.webview.initSessionWebView(
  type: 'pengecekan-laptop',
  firstName: 'John',
  lastName: 'Doe',
  memberCode: '123456',
  meta: {'conversation_id': 'conv-123'},
);

for (final type in WebviewEventType.values) {
  sdk.webview.onEvent(type, (event) {
    print('${event.type.name}: ${event.data}');
  });
}

final controller = sdk.webview.createController(
  onConsoleMessage: (m) => print('[JS] ${m.message}'),
);
await sdk.webview.openWebView(
  controller: controller,
  url: session.webViewUrl,
);
// host renders WebViewWidget(controller: controller)
```

Flutter → JS:

```dart
await sdk.webview.sendToWebView(
  controller: controller,
  event: const WebViewEvent(
    type: WebviewEventType.formSuccess,
    data: {'id': 'abc'},
  ),
);
```

`createController` takes no session. `loadHtmlString` and
`loadHtmlStringWithInlineJs` require a `controller`. Events:
`formSubmitted`, `formCancelled`, `formError`, `formSuccess`, `formClosed`,
`imageCaptured`.

## Form, Desk, QR in one glance

```dart
// Form
final session = await sdk.formSubmission.initFormSubmission();
final result = await sdk.formSubmission.submitForm(
  sessionToken: session.sessionToken,
  form: SubmitFormModel(/* ... */),
);

// Desk
final inbox = await sdk.desk.createCustomerInbox(
  name: 'Ahmad', phone: '08...', email: 'a@b.c',
  memberCode: '0001', ttlHours: 24,
);

// QR take-photo
final info = await sdk.qr.photo.show(maxFiles: 5);
sdk.qr.photo.onFileReceived.listen((file) { /* ReceivedFile */ });
// widget: sdk.qr.photo.buildQr(size: 220)
// or: TakePhotoQrWidget(url: info.url, size: 220)
```

## Reference routing

Read the matching file before writing non-trivial code:

| Topic | File |
|---|---|
| Requirements, install, init, lifecycle, platform setup | `references/quickstart.md` |
| All `get*` info APIs, the 16 `check*` tests, the required screen-per-test table, and the mandatory camera/touchscreen widgets | `references/device-tests.md` |
| WebView API, events, channels, HTML loading, permissions | `references/webview.md` |
| Form model contract, desk inbox, QR streams and teardown | `references/form-desk-qr.md` |
| Errors, emulator/iOS limitations, debug checklist | `references/troubleshooting.md` |

## Verification

After editing a Flutter app:

```bash
flutter pub get
flutter analyze
flutter test        # if tests exist
```

Hardware behavior must be verified on a physical Android device. Emulators and
desktop need the simulation notifiers documented in
`references/device-tests.md`.
