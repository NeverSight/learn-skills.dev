---
name: flutter-input-output-preview
description: Build responsive Flutter apps with a reusable `TwoPane` widget and an `InputOutputPreview` component for side-by-side code and preview display on both mobile and desktop.
metadata:
  url: https://rodydavis.com/posts/snippets/flutter-input-output-preview
  last_modified: Tue, 03 Feb 2026 20:04:31 GMT
---

# Flutter Input Output Preview


First we need a two pane widget to properly render on mobile and desktop:

```
import 'package:flutter/material.dart';

class TwoPane extends StatefulWidget {
  const TwoPane({
    super.key,
    required this.primary,
    required this.secondary,
    required this.title,
    this.actions = const [],
    this.loading = false,
  });

  final (String, WidgetBuilder) primary, secondary;
  final List<Widget> actions;
  final String title;
  final bool loading;

  @override
  State<TwoPane> createState() => _TwoPaneState();
}

class _TwoPaneState extends State<TwoPane> {
  bool darkMode = false;

  void toggleDarkMode() {
    if (mounted) {
      setState(() {
        darkMode = !darkMode;
      });
    }
  }

  ThemeData theme(Color color, Brightness brightness) {
    return ThemeData(
      brightness: brightness,
      colorScheme: ColorScheme.fromSeed(
        seedColor: color,
        brightness: brightness,
      ),
      useMaterial3: true,
    );
  }

  @override
  void didUpdateWidget(covariant TwoPane oldWidget) {
    if (oldWidget.loading != widget.loading ||
        oldWidget.title != widget.title ||
        oldWidget.actions != widget.actions) {
      if (mounted) setState(() {});
    }
    super.didUpdateWidget(oldWidget);
  }

  @override
  Widget build(BuildContext context) {
    return Theme(
      data: theme(Colors.purple, darkMode ? Brightness.dark : Brightness.light),
      child: Builder(builder: (context) {
        final (primaryTitle, primaryBuilder) = widget.primary;
        final (secondaryTitle, secondaryBuilder) = widget.secondary;
        return Scaffold(
            appBar: AppBar(
              title: Text(widget.title),
              centerTitle: false,
              actions: [
                IconButton(
                  tooltip: 'Toggle dark mode',
                  onPressed: toggleDarkMode,
                  icon: Icon(darkMode ? Icons.light_mode : Icons.dark_mode),
                ),
                ...widget.actions,
              ],
            ),
            body: LayoutBuilder(
              builder: (context, dimens) {
                if (dimens.maxWidth > 800 && dimens.maxHeight > 600) {
                  return Column(
                    children: [
                      if (widget.loading) const LinearProgressIndicator(),
                      Expanded(
                        child: Row(
                          children: [
                            Flexible(
                              flex: 1,
                              child: primaryBuilder(context),
                            ),
                            Flexible(
                              flex: 1,
                              child: secondaryBuilder(context),
                            ),
                          ],
                        ),
                      ),
                    ],
                  );
                }
                return DefaultTabController(
                  length: 2,
                  child: Column(
                    children: [
                      SizedBox(
                        height: kToolbarHeight,
                        width: double.infinity,
                        child: TabBar(
                          tabs: [
                            Tab(text: primaryTitle),
                            Tab(text: secondaryTitle),
                          ],
                        ),
                      ),
                      if (widget.loading) const LinearProgressIndicator(),
                      Expanded(
                        child: TabBarView(
                          children: [
                            primaryBuilder(context),
                            secondaryBuilder(context),
                          ],
                        ),
                      ),
                    ],
                  ),
                );
              },
            ));
      }),
    );
  }
}
```

Then we can pass some text fields for one pane to render an output:

```
import 'package:flutter/material.dart';

import 'two_pane.dart';

class InputOutputPreview extends StatefulWidget {
  const InputOutputPreview({
    super.key,
    required this.title,
    required this.input,
    required this.output,
    required this.preview,
    required this.placeholder,
    this.actions = const [],
    this.codeTitle = 'Code',
    this.previewTitle = 'Preview',
    this.loading = false,
    this.lazy = false,
    this.previewSize = const Size(300, 700),
  });

  final (
    String,
    ValueChanged<(TextEditingController, TextEditingController)>
  ) input, output;
  final Widget? preview;
  final Widget placeholder;
  final String title;
  final List<Widget> actions;
  final String codeTitle, previewTitle;
  final Size? previewSize;
  final bool loading;
  final bool lazy;

  @override
  State<InputOutputPreview> createState() => _InputOutputPreviewState();
}

class _InputOutputPreviewState extends State<InputOutputPreview> {
  final input = TextEditingController();
  final output = TextEditingController();
  String? lastInput;
  String? lastOutput;

  @override
  void initState() {
    super.initState();
    if (!widget.lazy) input.addListener(onInput);
    output.addListener(onOutput);
  }

  @override
  void dispose() {
    super.dispose();
    if (!widget.lazy) input.removeListener(onInput);
    output.removeListener(onOutput);
    input.dispose();
    output.dispose();
  }

  void onInput() {
    final (_, update) = widget.input;
    final str = input.text;
    if (lastInput == str) return;
    update((input, output));
    lastInput = str;
  }

  void onOutput() {
    final (_, update) = widget.output;
    final str = output.text;
    if (lastOutput == str) return;
    update((output, input));
    lastOutput = str;
  }

  @override
  Widget build(BuildContext context) {
    final (inputTitle, _) = widget.input;
    final (outputTitle, _) = widget.output;
    return TwoPane(
      title: widget.title,
      actions: widget.actions,
      loading: widget.loading,
      primary: (
        widget.codeTitle,
        (context) => SizedBox(
              height: double.infinity,
              child: Column(
                children: [
                  Flexible(
                    child: Padding(
                      padding: const EdgeInsets.all(8),
                      child: Card(
                        child: ListTile(
                          title: Text(inputTitle),
                          subtitle: TextField(
                            maxLines: null,
                            controller: input,
                            expands: true,
                            decoration: InputDecoration(
                              isCollapsed: true,
                              border: InputBorder.none,
                              suffix: widget.lazy
                                  ? IconButton(
                                      onPressed: onInput,
                                      icon: const Icon(Icons.save),
                                      tooltip: 'Submit',
                                    )
                                  : null,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                  Flexible(
                    child: Padding(
                      padding: const EdgeInsets.all(8),
                      child: Card(
                        child: ListTile(
                          title: Text(outputTitle),
                          subtitle: TextField(
                            maxLines: null,
                            controller: output,
                            expands: true,
                            decoration: const InputDecoration(
                              isCollapsed: true,
                              border: InputBorder.none,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
      ),
      secondary: (
        widget.previewTitle,
        (context) => Container(
              color: Theme.of(context).colorScheme.surfaceVariant,
              child: Builder(builder: (context) {
                if (widget.previewSize == null) {
                  return widget.preview ?? widget.placeholder;
                }
                return Center(
                  child: Material(
                    elevation: 8,
                    child: SizedBox.fromSize(
                      size: widget.previewSize,
                      child: widget.preview ?? widget.placeholder,
                    ),
                  ),
                );
              }),
            )
      ),
    );
  }
}
```