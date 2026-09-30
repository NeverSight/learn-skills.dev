---
name: flutter-unit-test
description: Write Flutter tests with Mocktail and Given-When-Then. Use when the user wants tests written or coverage gaps closed in the UChat Messenger project.
---

# Flutter Unit Test

UChat Messenger mandates **100% coverage** — line, branch, and function. Mocktail only, never Mockito.

## Rules

- `test/` mirrors `lib/` exactly — `core/{domain,data,presentation,infrastructure}/…` and `features/<feature>/{domain,data,presentation}/…`. So `lib/core/domain/usecases/get_user.dart` → `test/core/domain/usecases/get_user_test.dart`.
- Name tests `Given <state>, When <action>, Then <outcome>`.
- Every test body is `// Given` / `// When` / `// Then`, in the same order as the name. Combine to `// When & Then` when asserting a throw.
- One behaviour per test. Split "handles loading and error" into two.
- Mock the layer directly below, never deeper.
- Thai text is a first-class case: any model or widget carrying user text gets a `'สวัสดี ครับ'` test.
- Skip repository *interface* tests — asserting `isA<UserRepository>()` tests the compiler, not the code.

## Template

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late MockUserRepository mockRepository;
  late GetUserUseCase useCase;

  setUp(() {
    mockRepository = MockUserRepository();
    useCase = GetUserUseCase(mockRepository);
  });

  group('GetUserUseCase', () {
    test('Given the repository holds the user, '
        'When the use case is called, '
        'Then it returns that user', () async {
      // Given
      const userId = '123';
      const expectedUser = User(id: userId, name: 'John');
      when(() => mockRepository.getUser(userId)).thenReturn(expectedUser);

      // When
      final result = await useCase(userId);

      // Then
      expect(result, equals(expectedUser));
      verify(() => mockRepository.getUser(userId)).called(1);
    });

    test('Given the repository has no such user, '
        'When the use case is called, '
        'Then it throws UserNotFoundException', () async {
      // Given
      when(() => mockRepository.getUser('invalid'))
          .thenThrow(UserNotFoundException());

      // When & Then
      expect(() => useCase('invalid'), throwsA(isA<UserNotFoundException>()));
    });
  });
}
```

## Mocktail

Mocktail needs no codegen — declare `class MockX extends Mock implements X {}` and go. Every stub and verify wraps the call in a closure; a bare `when(mock.foo())` is the one mistake that silently fails.

```dart
when(() => mock.getUser('123')).thenReturn(user);              // sync
when(() => mock.fetch('123')).thenAnswer((_) async => user);   // async
when(() => mock.getUser('bad')).thenThrow(NetworkException()); // throw
when(() => mock.save(any())).thenAnswer((_) async => true);    // any arg
when(() => mock.post(any(), body: any(named: 'body')))         // named arg
    .thenAnswer((_) async => response);

verify(() => mock.getUser('123')).called(1);
verifyNever(() => mock.deleteUser('123'));
final captured = verify(() => mock.save(captureAny())).captured;
```

Register fallbacks for custom types used with `any()`:

```dart
setUpAll(() => registerFallbackValue(const User(id: '', name: '')));
```

## Per-layer recipes

Load only what the file under test needs:

- **entity, use case, repository impl, data source, model** → [references/layers.md](references/layers.md)
- **GetX controller, Rx state, worker, widget, navigation** → [references/getx.md](references/getx.md)
- **Isar database** → [references/isar.md](references/isar.md)
- **integration test (full flow on device)** → [references/integration.md](references/integration.md)

## Commands

```bash
fvm flutter test                                    # all
fvm flutter test test/core/domain/entities/user_test.dart
fvm flutter test --name "GetUserUseCase"            # substring match, group name
fvm flutter test --coverage                         # writes coverage/lcov.info
lcov --summary coverage/lcov.info                   # find gaps (brew install lcov)
genhtml coverage/lcov.info -o coverage/html         # browsable report
```

## Done when

- `fvm flutter test` green.
- `lcov --summary` reports 100% on lines, branches, and functions — no file excluded.
- Every public method, error path, and async path of the changed code has a test named `Given …, When …, Then …`.
- Thai text covered wherever user-facing strings flow.
