---
name: flutter-package-development
description: Create, evolve, test, or prepare reusable Dart packages and Flutter plugins for distribution. Use when the package itself, its public API, platform support, federation, example app, compatibility, or publication readiness is the deliverable; route app-owned native bridges to flutter-platform-integration.
---

# Flutter Package Development

Treat reusable packages as versioned contracts consumed by independent projects. Preserve SDK bounds, package architecture, supported platforms, and release conventions unless migration is requested.

## Preflight

Inspect `pubspec.yaml`, public exports, examples, tests, platform folders, CI, changelogs, and consumers.
Choose the smallest viable shape:
- Dart package for reusable Dart-only logic.
- Flutter package for reusable widgets without native code.
- Plugin or FFI package when native platform implementations are required.
- Federated plugin only when independent platform ownership or release cadence justifies multiple packages.

Do not convert app-owned bridges into packages merely because code reuse is possible.

## Load references conditionally

- Read [public API and package quality](references/public-api-and-quality.md) for exports, deprecations, semver, and consumer compatibility.
- Read [plugins and federation](references/plugins-and-federation.md) for platform interfaces, registration, FFI, and federated architecture.
- Read [publication readiness](references/publication-readiness.md) for dry-run inspection, pub.dev checklist, and release verification.

## Boundaries

- `flutter-platform-integration` owns app-side native code and low-level channel/FFI mechanics.
- `flutter-dependency-upgrades` owns consumer-side package upgrades in an application.
- `flutter-build-release` owns application stores and binary builds, not pub package publication.

## Verification

Format, analyze, run tests, and exercise the example fixture across all claimed platforms.
When publication readiness is in scope:
- Run `dart pub publish --dry-run` and inspect all output, warnings, and included files. A passing dry run proves neither compatibility nor authorization.
- Never publish, tag, or create releases without explicit user authorization. A conditional go-ahead ("publish if the dry run passes") does not cover changes you made after it: show the final diff and dry-run result, then ask before publishing.
- When tool or repository access is missing, provide an executable review plan with clear pass/fail criteria covering metadata, license, changelog, and dry-run output rather than fabricating results.

## Sources

- [Developing packages and plugins](https://docs.flutter.dev/packages-and-plugins/developing-packages)
- [Publishing packages](https://dart.dev/tools/pub/publishing)
- [Package layout conventions](https://dart.dev/tools/pub/package-layout)
