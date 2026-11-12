---
name: flutter-testing
description: Writes and runs Flutter tests (unit, cubit or bloc, repository, widget, integration) following the project's existing test setup. Use ONLY when the developer explicitly asks for tests, test setup or a test run; never add tests to other tasks.
license: Apache-2.0
---

# Flutter testing (on demand only)

Do not use this skill unless the developer asked for tests in this request. Other skills never add tests on their own; if a task would benefit from tests, say so in one line and stop.

## Steps

1. **Read the project's test setup.** Look at `test/` and `integration_test/` (layout, naming, helpers), `dev_dependencies` in `pubspec.yaml` (`flutter_test`, `bloc_test`, `mocktail`, `mockito`, `patrol`, `integration_test`), the project profile and any testing rules in `AGENTS.md`. Copy what exists: the same mock library, the same folder mirror of `lib/`, the same helper functions. Where a project rule and this skill disagree, the project rule wins.
2. **If there is no test setup,** propose the smallest one and ask before adding a package: `flutter_test` (in the SDK) and `mocktail`; plus `bloc_test` when the project uses Cubit or Bloc. Do not add a coverage tool, golden-test tool or UI driver unless asked.
3. **Agree on scope in one line** (which classes, which layer, which cases) when the request is broad. Default order of value: state classes (cubit, bloc or notifier) including the error path; repositories with the data source mocked; then one widget test per page that shows loading, data and error. Integration tests only when asked, and say they are slower and need a device or emulator.
4. **Write the tests** from `references/patterns.md`: test behaviour (what state sequence results from an action), not implementation details; one reason to fail per test; mock only the edges (repository, data source, clock). Do not test generated files (`*.g.dart`, `*.freezed.dart`, `*.gr.dart`) or plain data classes.
5. **Run them,** with the `fvm` prefix when `.fvmrc` exists: `flutter test test/path_test.dart` for the files you wrote, then the whole `flutter test` if time allows. Report the result as it is. If the run cannot happen (no SDK in the environment, missing generated files or secrets), say what was not run.
6. **When a test fails,** find out whether the test or the app code is wrong. Never weaken or delete a test to make it pass. If the app code has a bug, report it with the file and line and ask before changing app code that is outside the request.
7. **Finish** with: files added, what each covers, what is deliberately not covered, the command to run them, and the result.

## Rules

- Never put real keys, tokens or personal data in tests or fixtures.
- Do not make tests depend on the network, the clock, random values or the order other tests run in.
- A new test package changes `pubspec.yaml`: that is a package addition, so ask first.
- Android and iOS differences matter only for integration tests and plugins: plugin calls in unit tests need mocks of the platform channel or the plugin's interface; see Flutter's "Plugins in Flutter tests" page.
