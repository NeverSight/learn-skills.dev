---
name: github-actions
description: CI/CD Pipelines, Versioning & Release Management
metadata:
    platforms: "cross-platform"
    languages: "generic"
    category: "automation"
---

# GitHub Actions Pipeline

-   Use GitHub Actions as the primary CI/CD platform
-   Trigger on `push` to `main` and on all Pull Requests
-   Pipeline MUST include these stages in order:

## Stage 1: Quality Gate

```yaml
- name: Analyze
  run: flutter analyze --fatal-infos --fatal-warnings
- name: Format Check
  run: dart format --set-exit-if-changed .
- name: Run Tests
  run: flutter test --coverage
```

-   Zero warnings policy — `--fatal-infos` ensures no info-level issues pass
-   Format check MUST use `--set-exit-if-changed` to enforce consistent formatting

## Stage 2: Build

```yaml
- name: Build APK
  run: flutter build apk --flavor prod --dart-define-from-file=config/prod.json --release
- name: Build IPA
  run: flutter build ipa --flavor prod --dart-define-from-file=config/prod.json --release --export-options-plist=ios/ExportOptions.plist
```

-   Always build with `--flavor prod` and `--dart-define-from-file=config/prod.json`
-   Use a single `main.dart` — do NOT pass `-t lib/main_prod.dart`

## Stage 3: Deploy (on main merge only)

-   Upload to Firebase App Distribution for internal testing
-   Upload to Google Play Internal Track / TestFlight for staging
-   Production release requires manual approval gate

# Versioning Strategy

-   Follow Semantic Versioning: `MAJOR.MINOR.PATCH+BUILD`
-   Bump `PATCH` for bug fixes, `MINOR` for features, `MAJOR` for breaking changes
-   Set version in `pubspec.yaml`: `version: 1.2.3+45`
-   The `+BUILD` number MUST auto-increment in CI (use build number from CI environment)

# Code Signing

-   Store signing keys and certificates in GitHub Secrets (never in repo)
-   Android: Store keystore as base64-encoded secret, decode in CI
-   iOS: Use App Store Connect API key for automated signing
-   NEVER commit `*.jks`, `*.keystore`, `*.p12`, or `*.mobileprovision` files

# PR Requirements

-   All PRs MUST pass: analysis (0 warnings), formatting, and tests before merge
-   Require at least 1 code review approval
-   Branch protection on `main`: no direct pushes, require status checks

# Release Checklist

- [ ] Version bumped in `pubspec.yaml`
- [ ] CHANGELOG.md updated
- [ ] All tests passing on CI
- [ ] Build succeeds for both Android and iOS
- [ ] Tested on physical device with production flavor
- [ ] Git tag created matching version (`v1.2.3`)
