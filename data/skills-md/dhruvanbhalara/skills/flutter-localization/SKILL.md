---
name: flutter-localization
description: Internationalization, ARB Files & Locale Management
metadata:
    platforms: "flutter"
    languages: "dart"
    category: "i18n"
---

# Localization Setup

-   Use Flutter's built-in `flutter_localizations` and `intl` packages
-   Enable `generate: true` in `pubspec.yaml` for automatic code generation
-   Configure `l10n.yaml` at project root:
    ```yaml
    arb-dir: lib/l10n
    template-arb-file: app_en.arb
    output-localization-file: app_localizations.dart
    output-class: AppLocalizations
    nullable-getter: false
    ```

# ARB File Structure

-   Place all `.arb` files in `lib/l10n/`
-   Use `app_{locale}.arb` naming convention (e.g., `app_en.arb`, `app_es.arb`, `app_hi.arb`)
-   The template ARB file (`app_en.arb`) MUST contain `@` metadata for every key:
    ```json
    {
      "loginTitle": "Sign In",
      "@loginTitle": { "description": "Title on the login screen" },
      "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
      "@itemCount": { "description": "Item count with pluralization", "placeholders": { "count": { "type": "int" } } }
    }
    ```
-   Key naming: Use `featureName_context` format (e.g., `settings_title`, `login_emailHint`)
-   Group keys by feature in the ARB file with comment separators

# Usage Rules

-   Access strings via `context.l10n.keyName` using a `BuildContext` extension
-   STRICTLY prohibit hardcoded user-facing strings anywhere in the codebase
-   STRICTLY prohibit using `.l10n` in `initState()` or outside the widget tree — `context` must be available
-   For date/time/number formatting, use `intl` package formatters with the current locale

# Plural & Select Forms

-   Use ICU plural syntax for countable items: `{count, plural, =0{...} =1{...} other{...}}`
-   Use ICU select syntax for gender/category: `{gender, select, male{...} female{...} other{...}}`
-   Always include the `other` case as a fallback

# RTL Support

-   Use `Directionality` and `TextDirection`-aware widgets
-   Prefer `EdgeInsetsDirectional` over `EdgeInsets` for padding/margins
-   Use `start`/`end` instead of `left`/`right` in `MainAxisAlignment` and `CrossAxisAlignment`
-   Test with RTL locales during widget testing

# Adding a New Language

1. Create `app_{locale}.arb` with all keys translated
2. Run `flutter gen-l10n` (or rely on auto-generation)
3. Add the `Locale` to `supportedLocales` in `MaterialApp`
4. Verify with widget tests using the new locale
