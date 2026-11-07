---
name: flutter-text-rendering
description: Diagnose and fix Flutter text display issues including text overflow, orphaned words, line breaking, truncation, multi-style spans, and text scaling. Use when text clips, leaves dangling single words, overflows containers, or requires rich inline spans; route typography tokens and visual hierarchy to flutter-ui-design and screen-level layout constraints to flutter-responsive-layout.
---

# Flutter Text Rendering

Render readable, predictable text across dynamic content lengths, locales, and accessibility settings.

## Diagnose

Identify the failure mechanism before adjusting layout:

1. **Main-axis flex overflow:** A non-flex `Text` can receive an unbounded constraint along a `Flex` main axis and choose an intrinsic size larger than the space available beside its siblings, producing `RenderFlex overflowed`.
2. **Orphaned words (widows):** The last word of a headline or paragraph dangles alone on a new line because line breaking occurred at the final whitespace.
3. **Uncontrolled truncation:** Text clips silently or exceeds intended lines without a visible truncation affordance (`ellipsis`, `fade`).
4. **Broken inline flow:** Multiple adjacent `Text` widgets in a `Row` break across lines awkwardly instead of flowing as a continuous paragraph.
5. **Text scale breakage:** Enlarged system font scale (`TextScaler`) causes text to clip inside fixed-height containers or push critical actions offscreen.

## Rules

- **Constrain the competing branch, not every `Text`:** In a `Row`, use `Flexible`, `Expanded`, `SizedBox`, or `ConstrainedBox` when text must share finite horizontal space with siblings. In a `Column`, flex changes vertical allocation and is not a default fix for horizontal text overflow. Never add a flex child when the parent's main-axis constraint is unbounded.
- **Prevent orphaned words only where segmentation fits:** A non-breaking space (`\u00A0`) can bind the final two words of space-delimited headings, titles, and callouts. Do not apply that heuristic universally across locales.
- **Choose wrapping or truncation deliberately:** Allow natural wrapping when the full copy matters. When the product contract calls for truncation, pair an explicit `maxLines` with `TextOverflow.ellipsis`, `TextOverflow.fade`, or `TextOverflow.clip`. Do not set `softWrap: false` without verifying whether single-line clipping is acceptable.
- **Use `Text.rich` for inline styling:** Prefer `Text.rich` for ambient style and text scaling when mixing weights, colors, inline badges (`WidgetSpan`), or link recognizers. Raw `RichText` needs deliberate span style and scaling, but can inherit ambient text direction.
- **Measure text with `TextPainter` when layout depends on copy size:** When building dynamic chips, custom canvas callouts, or expandable "Read more" widgets, layout a `TextPainter` with explicit `maxWidth` plus the ambient direction, locale, and `TextScaler` to check rendered height and `didExceedMaxLines`.
- **Adapt to text scaling:** Support enlarged system fonts (`MediaQuery.textScalerOf(context)`). Avoid hardcoded container heights around text; prefer flexible or scrollable containers.
- **Account for internationalization:** Design copy containers to tolerate 20–35% text length expansion for localized strings and support bidirectional text (`TextDirection`).

## Conditional references

- Read [text overflow and wrapping](references/text-overflow-and-wrapping.md) when fixing flex overflows, eliminating orphaned words with non-breaking spaces, configuring `TextPainter` measurements, or managing multi-line truncation.

## Verification

Exercise the text component with:
1. Minimum length copy (empty or single short word).
2. Realistic expected copy.
3. Maximum length / localized copy (including accented and long non-whitespace strings).
4. Enlarged font scaling (`TextScaler.linear(1.5)` and `TextScaler.linear(2.0)`).
5. Constrained parent widths (narrow mobile screens, tight cards, list items).

Write a widget test asserting no `RenderFlex` overflow, confirming intended line count, and verifying that truncation or non-breaking word pairing renders as expected.

## Sources

- [Flutter Text class](https://api.flutter.dev/flutter/widgets/Text-class.html)
- [Flutter RichText class](https://api.flutter.dev/flutter/widgets/RichText-class.html)
- [Flutter TextPainter class](https://api.flutter.dev/flutter/painting/TextPainter-class.html)
- [Flutter TextOverflow enum](https://api.flutter.dev/flutter/painting/TextOverflow.html)
- [Flutter TextScaler class](https://api.flutter.dev/flutter/painting/TextScaler-class.html)
