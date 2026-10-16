---
name: flutter-mobile-development
description: Use when building mobile apps with Flutter.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [flutter, dart, mobile-development, widgets, state-management, cross-platform]
---

# Flutter Mobile Development

Building cross-platform mobile apps with Flutter — from widget composition and state management through navigation, platform channels, and performance optimization.

## When to Use

- Building cross-platform iOS/Android apps with single codebase
- Implementing complex UI with Flutter's widget system
- Managing app state with Riverpod, Bloc, or Provider
- Accessing native device features via platform channels
- Optimizing Flutter app performance

## Flutter Patterns

```dart
// Widget composition pattern
class CounterApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('Counter')),
        body: Center(child: Consumer<CounterModel>(
          builder: (context, counter, _) => Text('${counter.value}'),
        )),
        floatingActionButton: FloatingActionButton(
          onPressed: () => context.read<CounterModel>().increment(),
          child: Icon(Icons.add),
        ),
      ),
    );
  }
}

// State management with Riverpod
final counterProvider = StateNotifierProvider<CounterNotifier, int>((ref) {
  return CounterNotifier();
});
```

## Verification Checklist

- [ ] Widget tree organized (small, reusable widgets)
- [ ] State management chosen (Riverpod, Bloc, Provider)
- [ ] Platform channels for native features
- [ ] Navigation (GoRouter or Navigator 2.0)
- [ ] Performance: rebuild minimization, const widgets, DevTools profiling
- [ ] Platform-specific adaptations (Material for Android, Cupertino for iOS)
