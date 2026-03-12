---
name: flutter-stream-widget
description: Learn how to build dynamic Flutter UIs by directly using streams within your widget's build method, enabling reactive screen updates and more efficient data handling.
metadata:
  url: https://rodydavis.com/posts/snippets/flutter-stream-widget
  last_modified: Tue, 03 Feb 2026 20:04:29 GMT
---

# Flutter Stream Widget


Work with streams directly in the build method of a [Flutter](https://flutter.dev/) widget:

```
import 'dart:async';

import 'package:flutter/widgets.dart';

abstract class StreamWidget extends StatefulWidget {
  const StreamWidget({Key? key}) : super(key: key);

  Stream<Widget> build(BuildContext context);

  void initState() {}

  void dispose() {}

  void reassemble() {}

  Widget? buildEmpty(BuildContext context) => null;

  Widget? buildError(BuildContext context, Object? error) => null;

  @override
  State<StreamWidget> createState() => _StreamWidgetState();
}

class _StreamWidgetState extends State<StreamWidget> {
  @override
  void initState() {
    widget.initState.call();
    super.initState();
  }

  @override
  void dispose() {
    widget.dispose.call();
    super.dispose();
  }

  @override
  void reassemble() {
    widget.reassemble.call();
    super.reassemble();
  }

  @override
  Widget build(BuildContext context) {
    return StreamBuilder(
      stream: widget.build(context),
      builder: (context, snapshot) {
        if (snapshot.hasError) {
          final result = widget.buildError(context, snapshot.error);
          if (result != null) return result;
        }
        if (snapshot.hasData) {
          return snapshot.data!;
        } else {
          final result = widget.buildEmpty(context);
          if (result != null) return result;
        }
        return const SizedBox.shrink();
      },
    );
  }
}
```

This could also be applied to Future widgets, but for reactive screens, streams are closer to what is actually happening.

## Riverpod Example

```
import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'generated.g.dart';

@riverpod
class GeneratedWidget extends _$GeneratedWidget {
  @override
  Widget build(BuildContext context) {
    return const Text('Generated widget!');
  }
}

@riverpod
class StreamWidget extends _$StreamWidget {
  @override
  Stream<Widget> build(BuildContext context) async* {
    final controller = StreamController<int>();
    final timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      controller.add(timer.tick);
    });
    yield* controller.stream.map((event) => Text('Stream widget: $event'));
    timer.cancel();
    await controller.close();
  }
}

@riverpod
class FutureWidget extends _$FutureWidget {
  @override
  Future<Widget> build(BuildContext context) async {
    await Future.delayed(const Duration(seconds: 3));
    return const Text('Future completed!');
  }
}

class Example extends StatelessWidget {
  const Example({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Column(
          children: [
            Consumer(builder: (context, ref, child) {
              final generated = ref.watch(generatedWidgetProvider(context));
              return generated;
            }),
            Consumer(builder: (context, ref, child) {
              final stream = ref.watch(streamWidgetProvider(context));
              return stream.when(
                data: (data) => data,
                error: (error, stack) => Text(error.toString()),
                loading: () => const CircularProgressIndicator(),
              );
            }),
            Consumer(builder: (context, ref, child) {
              final future = ref.watch(futureWidgetProvider(context));
              return future.when(
                data: (data) => data,
                error: (error, stack) => Text(error.toString()),
                loading: () => const CircularProgressIndicator(),
              );
            }),
          ],
        ),
      ),
    );
  }
}
```