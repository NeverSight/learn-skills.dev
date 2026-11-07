---
name: flutter-testing
description: Design, write, or review Flutter unit, widget, golden, and integration tests. Use for test strategy, regressions, fakes, async UI behavior, and end-to-end flows; use device testing for operational emulator or hardware control.
---

# Flutter Testing

Test observable behavior at the cheapest layer that provides confidence.

## Choose the layer

- Unit tests: pure logic, state transitions, repositories, parsing, and failure policy.
- Widget tests: rendering, semantics, interaction, focus, navigation wiring, and state-to-UI behavior.
- Golden tests: stable visual contracts where platform/font control makes comparison meaningful.
- Integration tests: critical flows, plugin integration, performance, and behavior requiring a real target.

Do not replace behavior assertions with implementation details such as private method calls or exact widget-tree shape.

## Reliability

- Inject clocks, randomness, storage, and transports when determinism matters.
- Prefer small fakes over large mock graphs; verify outputs and side effects rather than incidental calls.
- Control async progress with the test framework; avoid arbitrary sleeps.
- Pump until a known state or bounded completion, not an unbounded `pumpAndSettle` when animations or timers persist.
- Give tests independent data and clean up global bindings, files, databases, and subscriptions.
- Update a golden only after reviewing the rendered difference.

## Disposable test probes

Classify each new test before creating it. Keep regression, acceptance, and specification tests as normal project files. A passing test is not a reason to delete it.

For a one-off diagnostic probe that should not be committed:

- Prefer an isolated temporary project or directory outside the repository when the runner permits it.
- If the probe must live under `test/` or `integration_test/`, choose one explicit unique path, record whether it existed or was tracked before creation, refuse to overwrite it, and mark the file as generated and disposable.
- Register host-side cleanup as soon as the path is created so it runs after success or failure. Preserve the test exit status and useful output before cleanup.
- Delete only artifacts created by the current run. Never recursively delete a test directory, use a broad glob, or delete pre-existing or tracked tests as routine cleanup.
- Confirm the recorded paths no longer exist and compare scoped `git status` with the pre-run state before reporting completion or preparing a commit. If execution was interrupted, inspect again rather than assuming cleanup ran.

Use test-framework teardown such as `addTearDown` for runtime files, databases, bindings, and subscriptions created inside a test. It does not replace host-side removal of an ephemeral Dart source file. If a probe exposes a reproducible defect, prefer converting it into a durable regression test unless the user explicitly wants only transient evidence.

Load [test layers and doubles](references/test-layers-and-doubles.md) when choosing boundaries, fakes, plugin seams, or native-UI coverage. Load [determinism, goldens, integration, and cleanup](references/determinism-goldens-and-integration.md) for async flakiness, visual contracts, device flows, or disposable test artifacts.

## Verification

Use the Dart and Flutter MCP test capability when available or the repository's established test command otherwise. Run the narrow test during iteration, then the relevant suite. Report the execution surface and data source independently—for example, a widget test with a fixture or an iOS simulator calling staging. Report skipped platforms, flaky behavior, or environment dependencies instead of treating them as success.

## Sources

- [Flutter testing](https://docs.flutter.dev/testing)
- [Integration testing](https://docs.flutter.dev/cookbook/testing/integration/introduction)
- [Dart and Flutter MCP server](https://docs.flutter.dev/ai/mcp-server)
