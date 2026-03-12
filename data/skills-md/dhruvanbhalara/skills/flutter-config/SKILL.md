---
name: flutter-config
description: App Flavors, Environment Config & Build Variants
metadata:
    platforms: "flutter"
    languages: "dart"
    category: "app-config"
---

# Flavor Architecture

-   Define three flavors: `dev`, `staging`, `prod`
-   Use a **single `main.dart`** entry point for all flavors
-   Pass flavor-specific configuration via `--dart-define-from-file`:
    ```bash
    flutter run --flavor dev --dart-define-from-file=config/dev.json
    flutter run --flavor staging --dart-define-from-file=config/staging.json
    flutter run --flavor prod --dart-define-from-file=config/prod.json
    ```
-   NEVER create separate `main_dev.dart`, `main_staging.dart`, `main_prod.dart` entry points

# Config JSON Structure

-   Store per-flavor JSON config files in a `config/` directory at project root:
    ```
    config/
    ├── dev.json
    ├── staging.json
    └── prod.json
    ```
-   Example `config/dev.json`:
    ```json
    {
      "FLAVOR": "dev",
      "BASE_URL": "https://api-dev.example.com",
      "APP_NAME": "MyApp Dev",
      "ENABLE_LOGGING": "true",
      "ENABLE_CRASHLYTICS": "false"
    }
    ```
-   NEVER put secrets (API keys, signing credentials) in these JSON files — use CI-injected env vars or `flutter_secure_storage`
-   Add `config/*.json` to `.gitignore` if they contain any environment-specific secrets; otherwise commit them for team convenience

# Entry Point Pattern

```dart
// lib/main.dart
void main() {
  const flavor = String.fromEnvironment('FLAVOR', defaultValue: 'dev');
  AppConfig.init(flavor: Flavor.fromString(flavor));
  runApp(const App());
}
```

-   Read all compile-time values via `String.fromEnvironment('KEY')` or `bool.fromEnvironment('KEY')`
-   Use a sealed `Flavor` enum: `sealed class Flavor { dev, staging, prod }`
-   `AppConfig` is a singleton holding flavor, base URL, feature flags, and Firebase config

# Environment Configuration

-   Store per-flavor config in a centralized `AppConfig` class:
    -   `baseUrl` — API endpoint per environment
    -   `enableLogging` — verbose logging for dev only
    -   `enableCrashlytics` — disabled in dev
    -   `appName` — display name per flavor (e.g., "MyApp Dev", "MyApp")
-   All values come from the JSON file via `--dart-define-from-file` — NO hardcoded per-flavor logic in Dart code
-   NEVER put secrets in the JSON config files — use `flutter_secure_storage` or CI-injected env vars

# Platform-Specific Flavor Setup

## Android

-   Define `flavorDimensions` and `productFlavors` in `android/app/build.gradle`:
    ```groovy
    flavorDimensions "environment"
    productFlavors {
        dev { dimension "environment"; applicationIdSuffix ".dev"; resValue "string", "app_name", "MyApp Dev" }
        staging { dimension "environment"; applicationIdSuffix ".staging"; resValue "string", "app_name", "MyApp Staging" }
        prod { dimension "environment"; resValue "string", "app_name", "MyApp" }
    }
    ```

## iOS

-   Create Xcode schemes for each flavor (Dev, Staging, Prod)
-   Use xcconfig files for per-flavor bundle ID, display name, and signing
-   Map Flutter flavors to Xcode schemes in `ios/Runner.xcodeproj`

# Firebase Per-Flavor

-   Use separate Firebase projects per flavor (dev, staging, prod)
-   Place `google-services.json` (Android) and `GoogleService-Info.plist` (iOS) in flavor-specific directories
-   Use `flutterfire configure` with `--project` flag for each environment

# Build Commands

```bash
# Development
flutter run --flavor dev --dart-define-from-file=config/dev.json

# Staging
flutter run --flavor staging --dart-define-from-file=config/staging.json

# Production release
flutter build appbundle --flavor prod --dart-define-from-file=config/prod.json --release
flutter build ipa --flavor prod --dart-define-from-file=config/prod.json --release
```

# Rules

-   NEVER hardcode environment-specific values (URLs, API keys, feature flags)
-   NEVER commit production secrets to the repository
-   Every team member MUST be able to run any flavor locally with a single command
-   CI/CD pipelines MUST specify both `--flavor` and `--dart-define-from-file` explicitly
-   Use a single `main.dart` — NEVER create separate entry points per flavor
