---
name: bloc
description: >
  Best practices for Bloc state management in Flutter/Dart, covering Cubit versus Bloc, event and
  state naming, sealed classes with Equatable, the Page/View split with BlocProvider, BlocBuilder,
  BlocListener, and BlocSelector. Use when writing, modifying, or reviewing code that uses
  package:bloc, package:flutter_bloc, or package:bloc_test. Also use for any test of a class that
  extends Bloc or Cubit, including "write the unit tests for this bloc", "test my cubit", "add
  tests for LoginBloc", mocking a repository a bloc depends on, and asserting the states an event
  emits. Bloc and Cubit tests must use blocTest() from package:bloc_test with package:mocktail, so
  prefer this over the testing skill whenever the class under test is a Bloc or Cubit. Also use
  when a request pushes against these rules, such as injecting one bloc into another to read its
  state, calling a repository from a widget or build method, or keeping a Cubit for a feature that
  needs an event transformer such as debounce.
allowed-tools: Read Glob Grep
---

# Bloc

State management library for Dart and Flutter using the BLoC (Business Logic Component) pattern to separate business logic from the presentation layer.

---

## Core Standards

Apply these standards to ALL Bloc/Cubit work:

- **Use `blocTest()` from `package:bloc_test`** for all Bloc and Cubit tests — never raw `test()` with manual stream assertions
- **Use `package:mocktail` for mocking** — never `package:mockito`
- **`build:` constructs the bloc under test** — return a new instance from the callback, never one built in `setUp` and shared, so every `blocTest` starts from a clean bloc and its lifecycle stays with `blocTest`
- **No bloc-to-bloc direct dependencies** — blocs communicate through the UI or shared repositories
- **Page/View separation** — Page provides the Bloc/Cubit via `BlocProvider`, View consumes via `BlocBuilder`/`BlocListener`
- **Sealed classes for events and multi-state types** — enables exhaustive pattern matching with Dart 3 `switch`
- **Equatable for all states and events** — extend `Equatable` and override `props` for value equality
- **Business logic in Bloc/Cubit only** — never in widgets, pages, or views
- **Single responsibility** — one Bloc/Cubit per feature concern
- **Emit only after async checks** — use `emit` only inside the handler callback

---

## Cubit vs Bloc

| Aspect       | Cubit                         | Bloc                                    |
| ------------ | ----------------------------- | --------------------------------------- |
| API          | Functions → `emit(state)`     | Events → `on<Event>` → `emit(state)`    |
| Complexity   | Low                           | Higher                                  |
| Traceability | Less (no event log)           | Full (events + transitions)             |
| When to use  | Simple state, UI-driven logic | Complex flows, event-driven, transforms |
| Testing      | Call methods, assert states   | Add events, assert states               |

### Cubit Example

```dart
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);

  void increment() => emit(state + 1);
  void decrement() => emit(state - 1);
}
```

### Bloc Example

```dart
sealed class CounterEvent extends Equatable {
  const CounterEvent();

  @override
  List<Object> get props => [];
}

final class CounterIncrementPressed extends CounterEvent {}
final class CounterDecrementPressed extends CounterEvent {}

class CounterBloc extends Bloc<CounterEvent, int> {
  CounterBloc() : super(0) {
    on<CounterIncrementPressed>((event, emit) => emit(state + 1));
    on<CounterDecrementPressed>((event, emit) => emit(state - 1));
  }
}
```

---

## Naming Conventions

### Events

**Pattern:** `BlocSubject` + `Noun` + `VerbPastTense`

| Event class name                | Meaning                         |
| ------------------------------- | ------------------------------- |
| `TodoListSubscriptionRequested` | Subscribing to todo list stream |
| `TodoListTodoDeleted`           | Deleting a specific todo        |
| `TodoListUndoDeletionRequested` | Undoing the last deletion       |
| `LoginFormSubmitted`            | Submitting the login form       |
| `ProfilePageRefreshed`          | Refreshing the profile page     |

```dart
sealed class TodoListEvent extends Equatable {
  const TodoListEvent();

  @override
  List<Object> get props => [];
}

final class TodoListSubscriptionRequested extends TodoListEvent {}

final class TodoListTodoDeleted extends TodoListEvent {
  const TodoListTodoDeleted({required this.todo});

  final Todo todo;

  @override
  List<Object> get props => [todo];
}
```

### States

#### Subclass Approach (multiple state types)

Use when each state carries different data.

| State class name  | Meaning                 |
| ----------------- | ----------------------- |
| `LoginInitial`    | No action taken yet     |
| `LoginInProgress` | Login request in flight |
| `LoginSuccess`    | Login succeeded         |
| `LoginFailure`    | Login failed            |

```dart
sealed class LoginState extends Equatable {
  const LoginState();

  @override
  List<Object> get props => [];
}

final class LoginInitial extends LoginState {}
final class LoginInProgress extends LoginState {}
final class LoginSuccess extends LoginState {
  const LoginSuccess({required this.user});

  final User user;

  @override
  List<Object> get props => [user];
}
final class LoginFailure extends LoginState {
  const LoginFailure({required this.error});

  final String error;

  @override
  List<Object> get props => [error];
}
```

#### Single Class Approach (one state, multiple fields)

Use when all states share the same data shape: one class holding a `status` enum plus the
data fields, with a `copyWith` for transitions. See
[references/patterns.md](references/patterns.md) for the full shape.

---

## Architecture

| Layer              | Contains                     | Depends on       |
| ------------------ | ---------------------------- | ---------------- |
| **Presentation**   | Pages, Views, Widgets        | Business Logic   |
| **Business Logic** | Blocs, Cubits                | Data             |
| **Data**           | Repositories, Data Providers | External sources |

### Data Layer

Repositories abstract data sources and provide a clean API for Blocs/Cubits. Mirror the feature folder structure under `test/` for all test files.

See [references/architecture.md](references/architecture.md) for the repository example, feature folder structure, and test directory layout.

---

## Flutter Widgets

Use `BlocProvider` to supply a Bloc or Cubit to a subtree, then `BlocBuilder`,
`BlocListener`, `BlocConsumer`, or `BlocSelector` to consume it. Reach for `BlocSelector`
when a rebuild should depend on one field rather than the whole state, and `BlocListener`
for side effects such as navigation or a snackbar.

The rule that matters: **`context.read` in callbacks** (`onPressed`, `onTap`),
**`context.watch` or `BlocBuilder` in `build`**. Never call `context.watch` outside a
`build` method.

## Additional Resources

- [references/architecture.md](references/architecture.md) — repository example, feature folder structure, test directory layout
- [references/widgets.md](references/widgets.md) — widget and context extension tables, Page/View pattern, `BlocListener` example
- [references/testing.md](references/testing.md) — `blocTest()` parameters, Cubit/Bloc test examples, mocking dependencies, widget integration tests
- [references/patterns.md](references/patterns.md) — single-class state, adding features with Bloc/Cubit, async operations, event transformers
