---
name: flutter-runtime-debugging
description: Reproduce, inspect, diagnose, and fix Flutter failures in a running app using logs, debugger attachment, DevTools, framework diagnostics, and minimal experiments. Use for runtime exceptions, incorrect live state, hangs, lifecycle failures, or failures that require execution evidence; route benchmarked jank to flutter-performance and planned device-flow verification to flutter-device-testing.
---

# Flutter Runtime Debugging

Turn a reported symptom into a repeatable failure, identify the first incorrect state or failing boundary, apply the smallest supported fix, and repeat the same flow as evidence.

## Establish the runtime

Read SDK constraints, flavors, entrypoints, defines, target platforms, recent changes, and existing logs or crash artifacts. Discover available devices and running applications before launching another copy. Preserve the user's chosen target and environment when they are material to the failure.

Do not infer a root cause from the last stack frame, a screenshot, or a downstream assertion alone. Record the exact trigger, expected result, actual result, build mode, platform, and whether the failure survives restart.

Use Dart and Flutter MCP capabilities for widget-tree inspection, structured logs, and runtime diagnostics when the environment exposes them; otherwise rely on DevTools and CLI output for the same evidence.

## Load references conditionally

- Read [reproduction and attachment](references/reproduction-and-attachment.md) when selecting a target, attaching to an existing process, handling startup or lifecycle failures, or reducing a flaky symptom.
- Read [DevTools diagnosis](references/devtools-diagnosis.md) when using the inspector, debugger, logging, network, memory, CPU, or frame views to test a concrete hypothesis.

## Diagnose narrowly

Use framework error details, causal stacks, structured logs, breakpoints, watches, and controlled state changes. Follow data and ownership across widget, state, isolate, transport, plugin, and native boundaries only as far as the evidence leads.

Before choosing a fix, require the first incorrect transition at every implicated boundary. For permission or lifecycle failures, explicitly trace the native callback, plugin or channel result and error mapping, application state owner, and resumed or disposed consumer. Do not stop at naming possible causes or pre-commit to a defensive null check.

Change one relevant variable at a time. Temporary instrumentation must be bounded, redact sensitive data, and be removed or converted into appropriate durable diagnostics before completion.

Hot reload preserves state and is not proof that startup, registration, initialization, generated code, or native configuration is correct. For plugin or native registration changes, perform a full rebuild and clean-process launch on every affected supported target before the first Dart call. Inspect startup and registration logs for errors, and verify that unsupported targets fail through the package's documented behavior rather than an accidental missing-plugin path. Reinstall when stale native artifacts or installation state could survive the rebuild.

## Boundaries

- `flutter-device-testing` owns executing a specified acceptance flow on a concrete device when diagnosis is not the task.
- `flutter-performance` owns profile-mode traces and before/after performance claims; use runtime debugging only to isolate a functional failure or candidate cause.
- `flutter-testing` owns durable automated test strategy; add a regression test after the runtime cause is understood.
- `flutter-observability` owns production telemetry design and backend ingestion, though its evidence can seed a local reproduction.
- `flutter-platform-integration` owns fixes inside channels, FFI, plugins, platform views, or native lifecycle code once that boundary is implicated.

## Verification

Repeat the original failing flow under equivalent conditions, then exercise the nearest error and lifecycle paths. Add the smallest durable regression test at the layer that owns the defect. State the target, build mode, commands or tools used, evidence observed, and anything not reproduced or verified.

## Sources

- [Flutter DevTools](https://docs.flutter.dev/tools/devtools)
- [Debug Flutter apps](https://docs.flutter.dev/testing/debugging)
- [Handling errors in Flutter](https://docs.flutter.dev/testing/errors)
- [Debugging add-to-app](https://docs.flutter.dev/add-to-app/debugging)
- [Dart and Flutter MCP server](https://docs.flutter.dev/ai/mcp-server)
