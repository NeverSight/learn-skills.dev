---
name: testing
description: >
  Best practices for Dart unit tests, Flutter widget tests, and golden file tests, covering group
  and test naming, setUp lifecycle and isolation, mocking with package:mocktail, and the shared
  pumpApp helper. Use when writing, modifying, or reviewing tests, goldens included, that use
  package:test, package:flutter_test, package:mocktail, or package:bloc_test. Use it also when no
  package is named: "add a golden test for my AppButton widget", "write a goldens test", goldens,
  matchesGoldenFile, tagging or updating goldens, writing a unit test or widget test, or adding a
  test helper or mock. A one-line golden or widget test request is in scope, including under "Dart
  code only"; a widget in a UI package is ui-package's. Use it too when the request asks for what
  these standards forbid: package:mockito, a raw string test tag instead of TestTag, an inline
  pumpWidget(MaterialApp(...)), asserting padding, color or font size in a widget test, or state
  shared between tests. Those requests are in scope, not out of it.
allowed-tools: Read Glob Grep mcp__very-good-cli__test
argument-hint: [file-or-directory]
---

# Dart & Flutter Testing

VGV testing conventions for Dart and Flutter. The framework APIs are assumed; what follows
is the house style layered on top of them.

## Core Standards

Apply these standards to ALL test work:

- **Descriptive test names** — verbose, readable names that describe the behavior; never `'works'` or `'renders'`
- **Hierarchical group/test structure that reads as natural sentences** — top-level `group` for the class, nested `group` for the method, `test` for the behavior (e.g., `UserRepository` → `getUser` → `returns User when API succeeds`)
- **String interpolation for type references** — use `'returns $User'` not `'returns User'` so renames propagate automatically
- **Private mocks per file** — declare `class _MockX extends Mock implements X {}` with underscore prefix to prevent cross-file coupling
- **Contained test setup within groups** — all `setUp`/`tearDown` calls live inside a `group`, never at the top level of `main()`
- **Initialize mutable objects in `setUp()` with `late`** — declare `late MyDep dep;` then assign in `setUp` so each test gets a fresh instance
- **No shared mutable state between tests** — never use static members, global variables, or top-level final instances that persist across tests
- **Use `package:mocktail`** — never `package:mockito`
- **Constant test tags** — use an `abstract class TestTag` with `static const` fields; never pass raw string literals as tags
- **Test behavior, not properties** — widget tests focus on functional outcomes; static visual properties validated via golden tests
- **Use `pumpApp` test helper** — wrap widgets via shared helper in `test/helpers/pump_app.dart`; never inline `pumpWidget(MaterialApp(...))`
- **Tag all golden tests** — annotate with `TestTag.golden` so goldens can run/update independently
- **Pass `directory` to the `test` MCP tool when the project is not at the workspace root** — monorepos with the Flutter project in a subdirectory (e.g. `mobile/`) require `directory: 'mobile'`; omit it only when `pubspec.yaml` is at the workspace root
- **Pass `timeout_seconds` to the `test` MCP tool** — Flutter tests can hang indefinitely when `pumpAndSettle()` is called without a timeout; set a cap (e.g. `timeout_seconds: 120`) so the run is killed instead of stalling
- **Cross-harness fallback for the `test` MCP tool** — on Claude Code use `mcp__very-good-cli__test`; on a host without this plugin's Bash hooks and without that MCP server connected, run `very_good test` (or `flutter test` / `dart test`) directly with the same coverage and timeout options — never block on a missing MCP server

## File Organization

| Convention           | Rule                                                                                           |
| -------------------- | ---------------------------------------------------------------------------------------------- |
| **File suffix**      | Every test file ends with `_test.dart`                                                         |
| **Directory**        | All tests live under `test/`                                                                   |
| **Mirror structure** | `test/` mirrors `lib/` exactly — `lib/src/models/user.dart` → `test/src/models/user_test.dart` |
| **Helpers**          | Shared test utilities go in `test/helpers/` (e.g., `pump_app.dart`, `fakes.dart`)              |

## Group and Test Hierarchy

Structure groups so that concatenated descriptions read as natural sentences. Use the
`PascalCase` type itself — not a string — in the top-level group.

```dart
class _MockApiClient extends Mock implements ApiClient {}

void main() {
  group(UserRepository, () {
    late ApiClient apiClient;
    late UserRepository subject;

    setUp(() {
      apiClient = _MockApiClient();
      subject = UserRepository(apiClient: apiClient);
    });

    group('getUser', () {
      test('returns $User when API call succeeds', () async {
        when(() => apiClient.fetchUser(any()))
            .thenAnswer((_) async => User(id: '1', name: 'Dash'));

        final result = await subject.getUser('1');

        expect(result, equals(User(id: '1', name: 'Dash')));
        verify(() => apiClient.fetchUser('1')).called(1);
      });

      test('throws $UserNotFoundException when API returns 404', () {
        when(() => apiClient.fetchUser(any()))
            .thenThrow(ApiException(statusCode: 404));

        expect(
          () => subject.getUser('1'),
          throwsA(isA<UserNotFoundException>()),
        );
      });
    });
  });
}
```

### Naming Conventions

| Pattern                  | Example                                                  |
| ------------------------ | -------------------------------------------------------- |
| **Returns a value**      | `'returns $User when API call succeeds'`                 |
| **Throws an exception**  | `'throws $UserNotFoundException when user is not found'` |
| **Calls a dependency**   | `'calls apiClient.deleteUser with correct id'`           |
| **Emits states**         | `'emits [loading, success] when data is fetched'`        |
| **Conditional behavior** | `'returns cached value when cache is not expired'`       |
| **Edge case**            | `'returns empty list when repository has no items'`      |

## Test Isolation

Each test must pass when run **individually**, in **any order**, and in **parallel**. Use
`--test-randomize-ordering-seed random` to expose hidden dependencies.

| Anti-Pattern                            | Problem                                               | Correct Approach                            |
| --------------------------------------- | ----------------------------------------------------- | ------------------------------------------- |
| `setUp` at the top level of `main()`    | Breaks when test runner merges files for optimization | Move `setUp` inside a `group`               |
| `final dep = _MockDep();` (top-level)   | Same instance shared across all tests; state leaks    | Use `late` + `setUp` inside a group         |
| `class MockDep extends Mock` (public)   | Other test files can import and depend on it          | Use `class _MockDep extends Mock` (private) |
| Static/global mutable variables         | State persists across tests                           | Reset in `setUp` or avoid entirely          |
| Tests that must run in a specific order | Fragile, fails with random ordering                   | Make each test fully self-contained         |

## Testing Private Logic

Never test private methods directly. Exercise private logic through the public method that
uses it:

```dart
// If _normalizeEmail is private, test it through the public createUser method:
test('normalizes email to lowercase before saving', () async {
  when(() => repository.save(any())).thenAnswer((_) async {});

  await subject.createUser(email: 'Dash@Example.COM');

  final captured = verify(() => repository.save(captureAny())).captured;
  expect(captured.first.email, equals('dash@example.com'));
});
```

## Widget Testing

| Rule                                       | Details                                                                                                       |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| **Use `testWidgets`**                      | Every widget test uses `testWidgets` instead of `test`                                                        |
| **Prefer `find.byType`**                   | Default finder; use `find.text` for user-visible content, `find.byKey` only when type/text is ambiguous       |
| **Group by behavior category**             | Use `renders`, `navigates`, `calls [MethodName]`, `updates` as nested group names                             |
| **Focus on behavior**                      | Assert what the widget _does_ (shows text, calls callback, navigates); use golden tests for visual appearance |
| **Mock Blocs and Cubits**                  | Use `MockBloc`/`MockCubit` from `package:bloc_test`; never provide real Blocs in widget tests                 |
| **Prefer `pump()` over `pumpAndSettle()`** | `pumpAndSettle` hangs on infinite animations such as `CircularProgressIndicator`                              |

### pumpApp Helper

Every widget test wraps the widget under test through one shared helper, so no test
inlines its own `MaterialApp`:

```dart
// test/helpers/pump_app.dart
extension PumpApp on WidgetTester {
  Future<void> pumpApp(Widget widget) {
    return pumpWidget(
      MaterialApp(
        home: widget,
      ),
    );
  }
}
```

Export it from `test/helpers/helpers.dart` so every test imports it with one line:

```dart
import '../helpers/helpers.dart';

void main() {
  group(MyWidget, () {
    testWidgets('renders greeting text', (tester) async {
      await tester.pumpApp(const MyWidget());

      expect(find.text('Hello'), findsOneWidget);
    });
  });
}
```

### Widget Testing Anti-Patterns

| Anti-Pattern                           | Problem                                                                 | Correct Approach                               |
| -------------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------- |
| Inline `MaterialApp` in each test      | Duplicated boilerplate; inconsistent setup                              | Use `pumpApp` helper                           |
| `find.byKey` as default finder         | Couples tests to implementation keys                                    | Prefer `find.byType` or `find.text`            |
| Testing padding, colors, or font sizes | Fragile; breaks on every design tweak; asserts appearance, not behavior | Use a golden test for visual validation        |
| Missing `pump()` after interaction     | Widget tree does not rebuild; assertion sees stale state                | Always `pump()` after `tap`, `enterText`, etc. |
| Real Blocs in widget tests             | Tests become integration tests; slow, brittle, hard to isolate          | Use `MockBloc`/`MockCubit` from `bloc_test`    |

Padding, background color, and font size are the recurring temptation. Asserting them in a
widget test couples the test to the design system and breaks on every restyle — move them to
a golden test tagged `TestTag.golden`.

## Additional Resources

- [references/mocktail.md](references/mocktail.md) — mocks and fakes, stubbing, argument matchers, verification, fallback values
- [references/test-patterns.md](references/test-patterns.md) — `setUp`/`tearDown` lifecycle and patterns for async, streams, exceptions, `Equatable`, and callbacks
- [references/widget-tests.md](references/widget-tests.md) — full Bloc-backed widget test, themes/localization in `pumpApp`, pumping methods, finders, and interactions
- [references/golden-tests.md](references/golden-tests.md) — golden file testing (setup, writing goldens, tagging, running/updating, anti-patterns)
- [references/matchers.md](references/matchers.md) — matchers quick reference
- [references/configuration.md](references/configuration.md) — `dart_test.yaml` configuration (tags, platform overrides) and running tests via the MCP `test` tool
- [references/coverage.md](references/coverage.md) — coverage patterns and package/imports reference
- [references/animation-testing.md](references/animation-testing.md) — testing implicit/explicit animations, AnimatedSwitcher, page transitions, and injected controllers
