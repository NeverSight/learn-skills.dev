---
name: flutter-dependency-upgrades
description: Plan, execute, or review Flutter and Dart SDK upgrades, dependency resolution, lockfile changes, package breaking changes, and compatible native toolchain migrations. Use when versions or compatibility are the task; route ordinary Dart refactoring to dart-language, security audits to flutter-security, and release artifacts to flutter-build-release.
---

# Flutter Dependency Upgrades

Upgrade the smallest coherent version set with reproducible evidence. Do not run a collection-wide major upgrade, delete the lockfile, or add an override before understanding the project's constraints and the requested outcome.

## Preflight

Read every relevant `pubspec.yaml`, the effective lockfile or Pub workspace resolution, Flutter/Dart SDK constraints, version-manager files, CI toolchain pins, enabled platforms, native build versions, code generators, generated-file policy, and pending worktree changes. Determine whether the repository is an application or published package because their lockfile and compatibility obligations differ.

Capture a clean baseline with the repository's established dependency retrieval, generation, analysis, tests, and representative target builds. If the baseline is already failing, separate that failure from the upgrade.

## Upgrade deliberately

1. Define the target: one package, a related package cohort, a security fix, a Flutter/Dart SDK, or a native toolchain requirement.
2. Inspect current, upgradable, resolvable, and latest versions plus official changelogs, migration guides, SDK bounds, platform support, and known incompatibilities. Use Dart and Flutter MCP package and analysis capabilities when available to cross-check resolved versions and API changes; otherwise rely on `dart pub outdated`/`flutter pub outdated` and changelog review.
3. Change one coherent layer at a time and preserve the repository's version manager, package sources, and architecture.
4. Regenerate only through project-owned commands, inspect API and generated diffs, and review every unexpected lockfile change.
5. Re-run the baseline checks and supported target builds before expanding the next upgrade cohort.

Use automated fixes only after reviewing their scope. Never treat a successful dependency resolution as proof that source, generated code, native builds, or runtime behavior remain compatible.

## Load details conditionally

- Read [SDK and package upgrades](references/sdk-and-package-upgrades.md) for Flutter/Dart version changes, major package updates, code generation, or staged rollout.
- Read [resolution conflicts and overrides](references/resolution-conflicts-and-overrides.md) for solver errors, transitive constraints, Pub workspaces, lockfiles, git/path sources, or temporary overrides.
- Read [platform toolchain migrations](references/platform-toolchain-migrations.md) when Android Gradle, AGP, Kotlin, JDK, Xcode, CocoaPods, Swift, deployment targets, desktop, or web tooling changes.

## Boundaries and completion

`dart-language` owns contained source-level modernization, `flutter-security` owns advisory risk and suppression decisions, `flutter-ci-cd` owns pipeline orchestration, and `flutter-build-release` owns signing and release artifacts. This skill owns the compatible version graph and migration evidence.

Do not publish, release, rotate credentials, or change signing material without explicit authorization. Report the final SDK/package/toolchain versions, intentional lockfile changes, migrations applied, checks run, supported targets not exercised, and any temporary override or compatibility debt that remains.

## Sources

- [Dart package dependencies](https://dart.dev/tools/pub/dependencies)
- [Dart pub outdated](https://dart.dev/tools/pub/cmd/pub-outdated)
- [Flutter upgrade guidance](https://docs.flutter.dev/install/upgrade)
- [Flutter breaking changes](https://docs.flutter.dev/release/breaking-changes)
- [Dart and Flutter MCP server](https://docs.flutter.dev/ai/mcp-server)
