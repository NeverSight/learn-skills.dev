---
name: flutter-testing
description: Use when writing tests for Flutter code - follows priority-based testing (Repository → State → Widget) after implementation
---

# Flutter Testing Guide

## Overview

Write tests following priority order after implementation. Focus on business logic first, UI last.

**Announce at start:** "I'm using the flutter-testing skill to write tests."

## Test Priority Order

```
Priority 1: Repository & DataSource Unit Tests
  ├── Business logic correctness
  ├── API integration
  └── Data transformation

Priority 2: State Management Unit Tests
  ├── BLoC/Cubit event handling
  ├── Provider state transitions
  └── Error state handling

Priority 3: Widget Tests (Optional)
  ├── User interactions
  ├── Widget rendering
  └── Navigation

Optional: Golden Tests
  └── Visual regression for design system

Optional: Integration Tests
  └── Full app flow testing
```

## Priority 1: Repository & DataSource Tests

### Repository Test Template

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';

@GenerateMocks([UserRemoteDataSource, UserLocalDataSource])
import 'user_repository_impl_test.mocks.dart';

void main() {
  late UserRepositoryImpl repository;
  late MockUserRemoteDataSource mockRemoteDataSource;
  late MockUserLocalDataSource mockLocalDataSource;

  setUp(() {
    mockRemoteDataSource = MockUserRemoteDataSource();
    mockLocalDataSource = MockUserLocalDataSource();
    repository = UserRepositoryImpl(
      remoteDataSource: mockRemoteDataSource,
      localDataSource: mockLocalDataSource,
    );
  });

  group('getUser', () {
    const tUserId = '123';
    final tUserModel = UserModel(id: '123', name: 'Test', email: 'test@test.com');
    final tUserEntity = User(id: '123', name: 'Test', email: 'test@test.com');

    test('should return User when remote data source succeeds', () async {
      // Arrange
      when(mockRemoteDataSource.getUser(any))
          .thenAnswer((_) async => tUserModel);

      // Act
      final result = await repository.getUser(tUserId);

      // Assert
      expect(result, equals(tUserEntity));
      verify(mockRemoteDataSource.getUser(tUserId));
    });

    test('should throw Exception when remote data source fails', () async {
      // Arrange
      when(mockRemoteDataSource.getUser(any))
          .thenThrow(Exception('Server error'));

      // Act & Assert
      expect(
        () => repository.getUser(tUserId),
        throwsException,
      );
    });
  });
}
```

### DataSource Test Template

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mockito/mockito.dart';

@GenerateMocks([http.Client])
import 'user_remote_datasource_test.mocks.dart';

void main() {
  late UserRemoteDataSourceImpl dataSource;
  late MockClient mockHttpClient;

  setUp(() {
    mockHttpClient = MockClient();
    dataSource = UserRemoteDataSourceImpl(client: mockHttpClient);
  });

  group('getUser', () {
    const tUserId = '123';
    final tUserJson = '{"id": "123", "name": "Test", "email": "test@test.com"}';

    test('should return UserModel when response is 200', () async {
      // Arrange
      when(mockHttpClient.get(any, headers: anyNamed('headers')))
          .thenAnswer((_) async => http.Response(tUserJson, 200));

      // Act
      final result = await dataSource.getUser(tUserId);

      // Assert
      expect(result, isA<UserModel>());
      expect(result.id, equals('123'));
    });

    test('should throw ServerException when response is not 200', () async {
      // Arrange
      when(mockHttpClient.get(any, headers: anyNamed('headers')))
          .thenAnswer((_) async => http.Response('Error', 500));

      // Act & Assert
      expect(
        () => dataSource.getUser(tUserId),
        throwsA(isA<ServerException>()),
      );
    });
  });
}
```

## Priority 2: State Management Tests

### BLoC Test Template

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';

@GenerateMocks([GetUserUseCase])
import 'user_bloc_test.mocks.dart';

void main() {
  late UserBloc bloc;
  late MockGetUserUseCase mockGetUser;

  setUp(() {
    mockGetUser = MockGetUserUseCase();
    bloc = UserBloc(getUser: mockGetUser);
  });

  tearDown(() {
    bloc.close();
  });

  test('initial state should be UserInitial', () {
    expect(bloc.state, equals(UserInitial()));
  });

  blocTest<UserBloc, UserState>(
    'should emit [Loading, Loaded] when GetUser succeeds',
    build: () {
      when(mockGetUser(any))
          .thenAnswer((_) async => const User(id: '1', name: 'Test'));
      return bloc;
    },
    act: (bloc) => bloc.add(const GetUserEvent('1')),
    expect: () => [
      UserLoading(),
      const UserLoaded(User(id: '1', name: 'Test')),
    ],
  );

  blocTest<UserBloc, UserState>(
    'should emit [Loading, Error] when GetUser fails',
    build: () {
      when(mockGetUser(any)).thenThrow(Exception('error'));
      return bloc;
    },
    act: (bloc) => bloc.add(const GetUserEvent('1')),
    expect: () => [
      UserLoading(),
      const UserError('error'),
    ],
  );
}
```

### Provider/Riverpod Test Template

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mockito/mockito.dart';

void main() {
  late ProviderContainer container;
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
    container = ProviderContainer(
      overrides: [
        userRepositoryProvider.overrideWithValue(mockRepository),
      ],
    );
  });

  tearDown(() {
    container.dispose();
  });

  test('should return user when fetchUser succeeds', () async {
    // Arrange
    when(mockRepository.getUser(any))
        .thenAnswer((_) async => const User(id: '1', name: 'Test'));

    // Act
    final result = await container.read(userProvider('1').future);

    // Assert
    expect(result.name, equals('Test'));
  });
}
```

## Priority 3: Widget Tests (Optional)

### Widget Test Template

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mockito/mockito.dart';

void main() {
  late MockUserBloc mockBloc;

  setUp(() {
    mockBloc = MockUserBloc();
  });

  Widget createWidgetUnderTest() {
    return MaterialApp(
      home: BlocProvider<UserBloc>.value(
        value: mockBloc,
        child: const UserScreen(),
      ),
    );
  }

  testWidgets('should display loading indicator when state is Loading',
      (tester) async {
    // Arrange
    when(mockBloc.state).thenReturn(UserLoading());

    // Act
    await tester.pumpWidget(createWidgetUnderTest());

    // Assert
    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });

  testWidgets('should display user name when state is Loaded',
      (tester) async {
    // Arrange
    when(mockBloc.state).thenReturn(
      const UserLoaded(User(id: '1', name: 'John Doe')),
    );

    // Act
    await tester.pumpWidget(createWidgetUnderTest());

    // Assert
    expect(find.text('John Doe'), findsOneWidget);
  });

  testWidgets('should call GetUserEvent when button is tapped',
      (tester) async {
    // Arrange
    when(mockBloc.state).thenReturn(UserInitial());

    // Act
    await tester.pumpWidget(createWidgetUnderTest());
    await tester.tap(find.byType(ElevatedButton));

    // Assert
    verify(mockBloc.add(any)).called(1);
  });
}
```

## Test File Structure

```
test/
├── features/
│   └── auth/
│       ├── data/
│       │   ├── datasources/
│       │   │   └── auth_remote_datasource_test.dart
│       │   └── repositories/
│       │       └── auth_repository_impl_test.dart
│       └── presentation/
│           ├── bloc/
│           │   └── auth_bloc_test.dart
│           └── widgets/
│               └── login_button_test.dart
└── helpers/
    ├── test_helpers.dart
    └── pump_app.dart
```

## Running Tests

```bash
# All tests
flutter test

# Specific feature
flutter test test/features/auth/

# Specific file
flutter test test/features/auth/data/repositories/auth_repository_impl_test.dart

# With coverage
flutter test --coverage

# Generate coverage report
genhtml coverage/lcov.info -o coverage/html
```

## Test Dependencies

```bash
# Mocking (choose one)
flutter pub add dev:mockito        # Requires codegen
flutter pub add dev:mocktail       # No codegen required (recommended)

# Code generation
flutter pub add dev:build_runner

# State management testing
flutter pub add dev:bloc_test      # If using BLoC
flutter pub add dev:riverpod_test  # If using Riverpod (optional)

# Freezed (if using immutable states)
flutter pub add freezed_annotation
flutter pub add dev:freezed
```

## Generate Mocks

```bash
# Generate mock files
flutter pub run build_runner build --delete-conflicting-outputs
```

## Key Principles

1. **Priority Order:** Repository → State → Widget
2. **Mock Dependencies:** Don't test real APIs or databases
3. **Arrange-Act-Assert:** Clear test structure
4. **One Assertion Focus:** Each test tests one thing
5. **Descriptive Names:** Test names describe behavior

## When to Skip Tests

- **Skip Widget Tests when:**
  - Simple stateless widgets
  - No user interaction logic
  - Pure presentation (no business logic)

- **Never Skip:**
  - Repository tests (business logic)
  - State management tests (state transitions)
  - Error handling tests

## REQUIRED SUB-SKILL

After writing tests, you MUST invoke:
→ **flutter-craft:flutter-verification**

Run `flutter test` and verify all tests pass.
