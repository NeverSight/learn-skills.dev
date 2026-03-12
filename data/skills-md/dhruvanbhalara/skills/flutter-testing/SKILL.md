---
name: flutter-testing
description: Quality Assurance & Advanced Testing
metadata:
    platforms: "flutter"
    languages: "dart"
    category: "testing"
---

# Testing Strategy

-   **Test Pyramid**: More unit and widget tests, fewer integration tests. Unit tests are fastest and cheapest.
-   **Mirror Test Rule**: 100% logic and widget coverage. No code without a test.
-   **Mirror Organization**: Test files MUST strictly mirror the `lib/` directory structure and end with `_test.dart`.
-   **Coverage Targets**: Target 100% logic coverage for `domain` and `bloc` layers.
-   **Test Independence**: Each test MUST be independent. No shared mutable state between tests.

# Unit Testing

-   Follow the Arrange-Act-Assert (Given-When-Then) convention for clear and maintainable tests
-   Use mocks for dependencies except for lightweight third-party services
-   Test business logic in isolation from the UI
-   For tests, ensure to create 5 to 8 tests for logical operations with real scenarios
-   **Mocking Protocol**: Use `mocktail` for all dependency mocking. STRICTLY prohibit using real implementation dependencies in unit tests.
-   **Pure Logic**: Business logic inside BLoCs or UseCases should be extracted to static pure functions for 100% unit test coverage.

# Widget Testing

-   Write widget tests for all major UI components
-   Test user interactions and state changes
-   **Widget Keys**: Use `Key('feature_action_id')` format on interactive widgets for test access
-   **Test Localization**: Use `AppLocalizations` (`context.l10n`) in widget tests — no hardcoded strings

# Integration Testing

-   Use `IntegrationTestWidgetsFlutterBinding.ensureInitialized()` at the start of integration tests
-   Interact with widgets via `Key` (e.g., `find.byKey(const ValueKey('increment'))`)
-   Use `pumpAndSettle()` to wait for animations and async operations to complete
-   Run with: `flutter test integration_test/`

# Test Naming & Structure

-   **Test Naming**: Use string interpolation for test group names: `group('$ClassName',` not `group('ClassName',`. This ensures consistency and enables better tooling support.
-   **Test Grouping**: Use `group()` to organize tests by feature, class, or state for clearer reporting.
-   **Descriptive Names**: Test names should clearly describe what is being tested and why.

# Common Test Errors

-   `A RenderFlex overflowed...` — Wrap widget in `Expanded` or constrain dimensions in test
-   `Vertical viewport was given unbounded height` — Wrap `ListView` in `SizedBox` with fixed height in test
-   `setState called during build` — Defer state changes to post-frame callback

# Running Tests

-   `flutter test` — Run all unit and widget tests
-   `flutter test test/path/to/file_test.dart` — Run specific test file
-   `flutter test integration_test/` — Run integration tests
-   `flutter test --coverage` — Run with coverage report
