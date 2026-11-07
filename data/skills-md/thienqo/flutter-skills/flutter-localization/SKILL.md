---
name: flutter-localization
description: Implement or review Flutter localization with gen_l10n, ARB resources, plurals, locale-aware formatting, RTL layout, and locale testing. Use for multi-language UI or localization infrastructure; not for arbitrary copy editing.
---

# Flutter Localization

Keep user-facing text in the project's localization pipeline and model meaning rather than concatenated fragments.

## Inspect

Read `pubspec.yaml`, `l10n.yaml`, existing ARB files, generated localization access, supported locales, and formatting packages. Preserve the established localization tool unless migration is requested.

## Rules

- Use descriptive, stable message keys and document placeholders where translators need context.
- Use ICU plural, select, and placeholder features instead of assembling translated sentences in code.
- Format dates, times, numbers, currencies, and units for the active locale.
- Avoid hardcoded user-facing strings, including errors, semantics labels, and empty states.
- Let directional APIs and start/end alignment support RTL; mirror only assets whose meaning requires it.
- Define a deliberate fallback and unsupported-locale policy.
- Do not infer language from country or persist a locale override the user did not choose.

## Verification

Generate localizations, analyze, and test representative locales including an RTL locale, long strings, plurals, missing resources, and locale-aware formats. Run key screens with large text because localization and layout failures often combine.

When formatting messages or localization is in scope, follow the [ICU messages and formatting reference](references/icu-messages-and-formatting.md).

## Sources

- [Internationalizing Flutter apps](https://docs.flutter.dev/ui/internationalization)
