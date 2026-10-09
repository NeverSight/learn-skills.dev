---
name: flutter-planning
description: Use when you have a design or requirements for a multi-step Flutter feature, before touching code
---

# Writing Flutter Implementation Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase. Document everything they need: which files to create/modify for each task, complete code, testing approach, how to verify it works. Give them the whole plan as bite-sized tasks following Clean Architecture layer order.

**Announce at start:** "I'm using the flutter-planning skill to create the implementation plan."

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>-plan.md`

## Feature-Driven Development Order

**CRITICAL: Follow Clean Architecture layer order:**

```
1. Domain Layer (First)
   ├── Entities
   ├── Repository interfaces
   └── UseCases (optional)

2. Data Layer (Second)
   ├── Models (DTOs with fromJson/toJson)
   ├── DataSources (Remote/Local)
   └── Repository implementations

3. Presentation Layer (Third)
   ├── State Management (BLoC/Provider/Riverpod)
   ├── Widgets
   └── Screens

4. Tests (After implementation)
   ├── Priority 1: Repository, DataSource unit tests
   ├── Priority 2: State management unit tests
   ├── Priority 3: Widget tests (optional)
   └── Priority 4: Golden tests (optional, visual regression)

5. Integration & Wiring
   └── DI setup (get_it, injectable, etc.)
```

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use flutter-craft:flutter-executing to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** Clean Architecture with [BLoC/Provider/Riverpod]

**Dependencies:** [New packages needed]

---
```

## Task Structure

```markdown
### Task N: [Component Name]

**Layer:** Domain / Data / Presentation / Test

**Files:**
- Create: `lib/features/<feature>/domain/entities/user.dart`
- Modify: `lib/features/<feature>/data/repositories/user_repository_impl.dart`
- Test: `test/features/<feature>/data/repositories/user_repository_test.dart`

**Implementation:**

```dart
// Complete code here - no placeholders like "add validation"
class User {
  final String id;
  final String name;
  final String email;

  const User({
    required this.id,
    required this.name,
    required this.email,
  });
}
```

**Verification:**

```bash
flutter analyze lib/features/<feature>/
# Expected: No issues found!
```

**Commit:**

```bash
git add lib/features/<feature>/domain/entities/user.dart
git commit -m "feat(<feature>): add User entity"
```
```

## Task Granularity

**Each task is one logical unit (2-10 minutes):**

| Task Type | Example |
|-----------|---------|
| Entity | Create User entity with properties |
| Repository Interface | Define UserRepository abstract class |
| Model | Create UserModel with fromJson/toJson |
| DataSource | Implement RemoteUserDataSource |
| Repository Impl | Implement UserRepositoryImpl |
| State | Create UserBloc with states and events |
| Widget | Create UserListItem widget |
| Screen | Create UserListScreen |
| Test | Write UserRepository unit tests |

## Example Plan Structure

```markdown
# Authentication Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use flutter-craft:flutter-executing

**Goal:** Implement user login/logout with token-based auth

**Architecture:** Clean Architecture with BLoC

**Dependencies:**
```bash
flutter pub add dio
flutter pub add flutter_bloc
flutter pub add get_it
```

---

## Domain Layer

### Task 1: User Entity
**Layer:** Domain
**Files:**
- Create: `lib/features/auth/domain/entities/user.dart`
...

### Task 2: AuthRepository Interface
**Layer:** Domain
**Files:**
- Create: `lib/features/auth/domain/repositories/auth_repository.dart`
...

## Data Layer

### Task 3: UserModel
**Layer:** Data
**Files:**
- Create: `lib/features/auth/data/models/user_model.dart`
...

### Task 4: AuthRemoteDataSource
**Layer:** Data
**Files:**
- Create: `lib/features/auth/data/datasources/auth_remote_datasource.dart`
...

### Task 5: AuthRepositoryImpl
**Layer:** Data
**Files:**
- Create: `lib/features/auth/data/repositories/auth_repository_impl.dart`
...

## Presentation Layer

### Task 6: AuthBloc
**Layer:** Presentation
**Files:**
- Create: `lib/features/auth/presentation/bloc/auth_bloc.dart`
- Create: `lib/features/auth/presentation/bloc/auth_event.dart`
- Create: `lib/features/auth/presentation/bloc/auth_state.dart`
...

### Task 7: LoginScreen
**Layer:** Presentation
**Files:**
- Create: `lib/features/auth/presentation/screens/login_screen.dart`
...

## Testing

### Task 8: AuthRepository Unit Tests
**Layer:** Test (Priority 1)
**Files:**
- Create: `test/features/auth/data/repositories/auth_repository_impl_test.dart`
...

### Task 9: AuthBloc Unit Tests
**Layer:** Test (Priority 2)
**Files:**
- Create: `test/features/auth/presentation/bloc/auth_bloc_test.dart`
...

## Integration

### Task 10: DI Setup
**Layer:** Integration
**Files:**
- Modify: `lib/core/di/injection.dart`
...
```

## Remember

- **Exact file paths always** - Full path from lib/ or test/
- **Complete code in plan** - No "add validation here"
- **Verification commands** - flutter analyze, flutter test
- **Layer order** - Domain → Data → Presentation → Test
- **One commit per task** - Keep commits atomic
- **Conventional commits** - feat(), fix(), test(), refactor()

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (this session)** - Dispatch fresh subagent per task, review between tasks, fast iteration

**2. Batch Execution (this session)** - Execute 3 tasks at a time with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use flutter-craft:flutter-subagent-dev
- Fresh subagent per task + 2-stage code review

**If Batch Execution chosen:**
- **REQUIRED SUB-SKILL:** Use flutter-craft:flutter-executing
- Execute 3 tasks, verify, checkpoint, continue

## REQUIRED SUB-SKILL

After completing the plan, you MUST offer execution options and invoke one of:
→ **flutter-craft:flutter-executing** (batch execution)
→ **flutter-craft:flutter-subagent-dev** (subagent per task)

This is NOT optional. Plans without execution are incomplete.
