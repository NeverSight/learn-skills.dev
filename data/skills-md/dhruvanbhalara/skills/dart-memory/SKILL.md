---
name: dart-memory
description: Professional memory management for mobile applications, focusing on resource disposal, garbage collection pressure, and large asset handling.
metadata:
    platforms: "cross-platform, mobile"
    languages: "dart"
    category: "optimization"
---

# Memory Management

Mobile devices have limited RAM. Efficient memory management is critical to prevent crashes and ensure a smooth user experience.

## Resource Lifecycle
- **Explicit Disposal**: Always close `StreamController`, `Timer`, `FocusNode`, and `ChangeNotifier` in the `dispose()` method.
- **Late Initialization**: Use `late` to delay object creation until it's actually needed, reducing initial memory footprint.

## Garbage Collection (GC) Pressure
- **Generational GC**: Dart's GC is optimized for short-lived objects. However, creating thousands of objects in a single frame can still cause jank.
- **Object Re-use**: Avoid creating new objects in `build()` or high-frequency loops. Reuse data structures where possible.
- **Large Collections**: Clearing a large list (`list.clear()`) is better than re-assigning it to a new list if the list itself is long-lived.

## Mobile Specifics
- **Isolates**: Use `Isolate.run()` for heavy computations (JSON parsing > 1MB, image processing). This keeps the main thread free and prevents UI freezes.
- **Image Memory**: Use `cacheWidth` and `cacheHeight` in `Image.network` or `Image.asset` to avoid loading high-resolution images into memory at full size.
- **Memory Leaks**: Use the DevTools Memory View to identify "leaking" objects that stay in the heap after their context (like a screen) is closed.

## Large Data Handling
- **Pagination**: Never load entire datasets into memory. Use server-side or local database pagination (Isar, SQLite).
- **Streaming**: For large files or real-time data, use `Stream` to process data in chunks rather than buffering the entire content in memory.
