---
name: flutter-device-testing
description: Operate and verify Flutter apps on a concrete emulator, simulator, browser, desktop, or physical device. Use for target lifecycle, platform-state checks, runtime evidence, and live integration flows; pair with flutter-navigation for route correctness, and do not select it for widget or golden-only work.
---

# Flutter Device Testing

Use the smallest target matrix that proves the changed behavior, then state what was and was not exercised. Identify the runtime target separately from the data source used by the flow.

## Discover before acting

Inspect the project's SDK, supported platforms, flavors, entrypoints, and existing test tooling. Run `flutter devices` and, when a virtual target must be started, `flutter emulators`. Resolve one target by stable identifier, record whether it is reused or task-created, and wait until it is ready. Do not erase, reset, recreate, uninstall from, or clear data on a user's target without explicit need and authorization.

Prefer Flutter CLI and available Dart and Flutter MCP capabilities for Flutter-owned state. Use `adb` or `simctl` only for platform control they actually provide. Flutter finders cannot operate native system UI such as permission dialogs, notification trays, or platform views; use a native-capable harness already adopted by the project when that interaction is required. Do not introduce Patrol, Maestro, Appium, or another framework merely because it is familiar.

## Workflow

1. Confirm dependencies and generated code are ready without changing the project's package or architecture choices.
2. Verify target readiness and the flavor-specific application identity before changing runtime state.
3. Launch with the correct flavor, entrypoint, defines, and build mode; never place credentials in command arguments or retained artifacts.
4. Exercise the exact user flow and relevant lifecycle or platform states. Distinguish state injection from observing the real prompt, provider, or OS delivery path.
5. Capture focused assertions, screenshots, and filtered logs that correspond to the tested build. Run the project's integration or native-UI harness when durable automation is required.
6. Restore task-created target overrides and remove only task-owned artifacts, including after failures.

## Reliability

Do not assume a successful build, launch command, or OS trigger proves correct app behavior. Prefer semantic finders, accessibility identifiers, or integration APIs over hardcoded coordinates, and prefer bounded readiness conditions over arbitrary sleeps. A warm-start claim requires an explicit precondition proving the intended process and UI state before the trigger. When using the lifecycle runner, confirm that every hook inherits its bounded timeout and that `after` cleanup is attempted from its `finally` path after pass, failure, timeout, or command error.

Report target kind and a safe label, OS/runtime, build mode, flavor, entrypoint or relevant defines, exact flow, data source, assertions, artifacts, and skipped boundaries. Do not publish a raw physical-device identifier by default. Emulator or simulator behavior is functional evidence, not physical-hardware performance, GPU, camera, sensor, OEM, or production push evidence. Route benchmark attribution to `flutter-performance` and verify stronger hardware claims in profile or release-like mode on representative physical devices.

## References

- Read [device discovery and emulators](references/device-discovery-and-emulators.md) for shared target selection, ownership, readiness, safety, and evidence rules.
- Read [Android emulator operations](references/android-emulator-operations.md) when starting or controlling an Android virtual or physical target with Flutter and `adb`.
- Read [iOS Simulator operations](references/ios-simulator-operations.md) when controlling Simulator with Flutter and `simctl`, including permissions, location, screenshots, or simulated push.
- Read [semantic UI inspection](references/semantic-ui-inspection.md) when an agent must read or drive a running app through the platform accessibility tree (`idb`, `uiautomator`), when that tree is empty for a Flutter screen, or when stable `Semantics` identifiers are needed instead of coordinates or repeated screenshots.
- Read [integration test workflows](references/integration-test-workflows.md) when writing or running `package:integration_test` suites, deep links, or smoke tests on a live target.
- Read [lifecycle entry matrix](references/lifecycle-entry-matrix.md) when deep links or notification taps must be replayed across cold/warm start, authentication, duplicate delivery, slow data, or account changes. Resolve placeholders and require the included runner's dry run to exit successfully with the expected plan before adding `--execute`.

## Sources

- [Flutter CLI](https://docs.flutter.dev/reference/flutter-cli)
- [Integration testing](https://docs.flutter.dev/cookbook/testing/integration/introduction)
- [Dart and Flutter MCP server](https://docs.flutter.dev/ai/mcp-server)
