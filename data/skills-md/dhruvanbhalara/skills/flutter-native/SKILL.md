---
name: flutter-native
description: Best practices for MethodChannels, EventChannels, and Federated Plugins.
metadata:
    platforms: "flutter, android, ios"
    languages: "dart, kotlin, swift"
    category: "platform"
---

# Native Platform Interoperability

Developing Flutter apps often requires direct communication with the underlying native platform (Android/iOS). This skill covers the standards for maintainable and type-safe interoperability.

## 1. MethodChannels (One-shot)

Use `MethodChannel` for standard request-response patterns between Dart and Native.

### Dart Standard
- Use a unique domain-style channel name.
- ALWAYS wrap calls in a try-catch for `PlatformException`.

```dart
static const _channel = MethodChannel('com.example.app/device_info');

Future<String?> getDeviceOS() async {
  try {
    return await _channel.invokeMethod<String>('getOS');
  } on PlatformException catch (e) {
    AppLogger.error('Failed to get OS', error: e);
    return null;
  }
}
```

## 2. EventChannels (Streams)

Use `EventChannel` for continuous data flow (e.g., sensor data, connectivity).

### Implementation
- Native side MUST handle `onListen` and `onCancel`.
- Dart side MUST dispose the subscription to prevent leaks.

## 3. Type Safety with Pigeon

For complex APIs, avoid manual string-based keys. Use **Pigeon** to generate type-safe interfaces.

## 4. Platform-Specific Directory Structure

Organize native code within the relevant feature if possible, or use a dedicated `plugins/` directory for shared logic.

## 5. Federated Plugins

If the logic is reusable across multiple apps:
- Split implementation into `_platform_interface`, `_android`, `_ios`, and `_web` packages.
- Provide a single entry point for users.
