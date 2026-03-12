---
name: flutter-markdown-view-with-material-3
description: Learn how to customize the Flutter Markdown widget using Material 3 text and color styles for a visually appealing and consistent design.
metadata:
  url: https://rodydavis.com/posts/snippets/flutter-markdown-view-material-3
  last_modified: Tue, 03 Feb 2026 20:04:30 GMT
---

# Flutter Markdown View with Material 3


## Overview 

How to style the [Flutter markdown](https://pub.dev/packages/flutter_markdown) widget with [Material 3](https://m3.material.io/) text and color styles:

```
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:go_router/go_router.dart';
import 'package:markdown/markdown.dart' as md;
import 'package:url_launcher/url_launcher.dart';

class MarkdownView extends StatelessWidget {
  const MarkdownView({
    Key? key,
    required this.markdown,
    this.textScaleFactor = 1,
  }) : super(key: key);

  final String markdown;
  final double textScaleFactor;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    final textTheme = Theme.of(context).textTheme;
    return Markdown(
        data: markdown,
        selectable: true,
        softLineBreak: true,
        onTapLink: (text, link, _) {
          final url = link ?? '/';
          if (url.startsWith('http')) {
            launchUrl(Uri.parse(url));
          } else {
            context.push(url);
          }
        },
        extensionSet: md.ExtensionSet(
          md.ExtensionSet.gitHubFlavored.blockSyntaxes,
          [md.EmojiSyntax(), ...md.ExtensionSet.gitHubFlavored.inlineSyntaxes],
        ),
        styleSheet: MarkdownStyleSheet(
            textScaleFactor: textScaleFactor,
            p: textTheme.bodyLarge!.copyWith(
              fontSize: 16,
              color: colors.onSurface.withOpacity(0.72),
            ),
            a: TextStyle(
              decoration: TextDecoration.underline,
              color: colors.onSurface.withOpacity(0.72),
            ),
            h1: textTheme.displaySmall!.copyWith(
              fontSize: 25,
              color: colors.onSurface,
            ),
            h2: textTheme.headlineLarge!.copyWith(
              fontSize: 20,
              color: colors.onSurface,
            ),
            h3: textTheme.headlineMedium!.copyWith(
              fontSize: 18,
              color: colors.onSurface,
            ),
            h4: textTheme.headlineSmall!.copyWith(
              fontSize: 16,
              color: colors.onSurface,
            ),
            h5: textTheme.titleLarge!.copyWith(
              fontSize: 16,
              color: colors.onSurface,
            ),
            h6: textTheme.titleMedium!.copyWith(
              fontSize: 16,
              color: colors.onSurface,
            ),
            listBullet: textTheme.bodyLarge!.copyWith(
              color: colors.onSurface,
            ),
            em: const TextStyle(fontStyle: FontStyle.italic),
            strong: const TextStyle(fontWeight: FontWeight.bold),
            blockquote: TextStyle(
              fontStyle: FontStyle.italic,
              fontWeight: FontWeight.w500,
              color: colors.onSurfaceVariant,
            ),
            blockquoteDecoration: BoxDecoration(
              color: colors.surfaceVariant,
              borderRadius: BorderRadius.circular(4),
            ),
            code: const TextStyle(fontFamily: 'monospace'),
            tableHead:
                const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
            tableBody:
                const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
            blockSpacing: 8,
            listIndent: 32,
            blockquotePadding: const EdgeInsets.all(8),
            h1Padding: const EdgeInsets.symmetric(vertical: 8),
            h2Padding: const EdgeInsets.symmetric(vertical: 8),
            h3Padding: const EdgeInsets.symmetric(vertical: 8),
            h4Padding: const EdgeInsets.symmetric(vertical: 8),
            h5Padding: const EdgeInsets.symmetric(vertical: 8),
            h6Padding: const EdgeInsets.symmetric(vertical: 8),
            codeblockPadding: const EdgeInsets.all(8),
            codeblockDecoration: BoxDecoration(
              borderRadius: BorderRadius.circular(4),
              color: colors.surfaceVariant,
            ),
            horizontalRuleDecoration: BoxDecoration(
              border: Border(
                top: BorderSide(
                  color: colors.outline.withOpacity(0.4),
                  width: 1,
                ),
              ),
            )),
    );
  }
}
```