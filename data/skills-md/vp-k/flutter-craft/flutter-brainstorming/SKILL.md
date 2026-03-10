---
name: flutter-brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation using Clean Architecture principles."
---

# Brainstorming Flutter Features Into Designs

## Overview

Help turn ideas into fully formed Flutter designs and specs through natural collaborative dialogue.

Start by understanding the current project context (pubspec.yaml, lib/ structure, existing features), then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

**Announce at start:** "I'm using the flutter-brainstorming skill to design this feature."

## The Process

### Phase 1: Understanding the Idea

**Check project context first:**
```bash
# Check pubspec.yaml for dependencies
cat pubspec.yaml

# Check existing lib/ structure
ls -la lib/

# Check existing features
ls -la lib/features/ 2>/dev/null || echo "No features folder yet"
```

**Ask questions one at a time:**
- Prefer multiple choice questions when possible
- Only one question per message
- Focus on understanding: purpose, constraints, success criteria

**Key questions to explore:**
1. What user problem does this feature solve?
2. What data does this feature need?
3. What UI interactions are required?
4. What state needs to be managed?
5. Are there external dependencies (APIs, databases)?

### Phase 2: Exploring Approaches

**Propose 2-3 different approaches with trade-offs:**

Example for state management:
```
Approach A: Riverpod + Freezed (Recommended for new projects)
- Pros: Compile-time safety, immutable states, no boilerplate with codegen
- Cons: Learning curve, requires build_runner
- Best for: Most Flutter projects

Approach B: BLoC Pattern
- Pros: Separation of concerns, testable, scalable
- Cons: More boilerplate
- Best for: Complex state, multiple streams, large teams

Approach C: Provider + ChangeNotifier
- Pros: Simple, familiar
- Cons: Less structured, harder to test
- Best for: Simple local state, small projects
```

**Riverpod + Freezed Pattern Example:**

```dart
// State with freezed
@freezed
class AuthState with _$AuthState {
  const factory AuthState.initial() = _Initial;
  const factory AuthState.loading() = _Loading;
  const factory AuthState.authenticated(User user) = _Authenticated;
  const factory AuthState.error(String message) = _Error;
}

// Notifier with riverpod_generator
@riverpod
class Auth extends _$Auth {
  @override
  AuthState build() => const AuthState.initial();

  Future<void> login(String email, String password) async {
    state = const AuthState.loading();
    try {
      final user = await ref.read(authRepositoryProvider).login(email, password);
      state = AuthState.authenticated(user);
    } catch (e) {
      state = AuthState.error(e.toString());
    }
  }
}
```

**Lead with your recommendation and explain why.**

### Phase 3: Presenting the Design

**Present the design in sections of 200-300 words:**

1. **Feature Overview**
   - Purpose and scope
   - User stories

2. **Clean Architecture Structure**
   ```
   lib/features/<feature_name>/
   ├── domain/
   │   ├── entities/          # Business objects
   │   ├── repositories/      # Repository interfaces
   │   └── usecases/          # Business logic
   ├── data/
   │   ├── models/            # DTOs (fromJson, toJson)
   │   ├── datasources/       # Remote & Local data sources
   │   └── repositories/      # Repository implementations
   └── presentation/
       ├── bloc/ or provider/ # State management
       ├── widgets/           # Reusable UI components
       └── screens/           # Full screen widgets
   ```

3. **Data Flow**
   - API contracts (if applicable)
   - Local storage schema (if applicable)
   - State transitions

4. **UI/UX Design**
   - Widget hierarchy
   - Navigation flow
   - Error states

5. **Testing Strategy** (priority-based)
   - 1순위: Repository, DataSource unit tests
   - 2순위: State management (BLoC/Provider) unit tests
   - 3순위: Widget tests (optional)

**Ask after each section:** "Does this look right so far?"

## After the Design

### Documentation

Write the validated design to:
```
docs/plans/YYYY-MM-DD-<feature>-design.md
```

**Design document template:**
```markdown
# <Feature Name> Design

## Overview
[1-2 sentences describing the feature]

## User Stories
- As a user, I want to...

## Clean Architecture

### Domain Layer
- Entities: [list]
- UseCases: [list]
- Repository interfaces: [list]

### Data Layer
- Models: [list]
- DataSources: [list]
- Repository implementations: [list]

### Presentation Layer
- State Management: [BLoC/Provider/Riverpod]
- Screens: [list]
- Widgets: [list]

## Data Flow
[Diagram or description]

## API Contract
[If applicable]

## Testing Plan
- Unit tests: [list]
- Widget tests: [list]
- Integration tests: [if needed]

## Dependencies
[New packages needed in pubspec.yaml]
```

Commit the design document to git:
```bash
git add docs/plans/
git commit -m "docs: add <feature> design document"
```

### Implementation (if continuing)

Ask: **"Ready to create an implementation plan?"**

If yes:
- Use `flutter-craft:flutter-planning` to create detailed implementation plan
- Use `flutter-craft:flutter-worktrees` if isolated workspace is needed

## REQUIRED SUB-SKILL

After completing brainstorming and documenting the design, you MUST invoke:
→ **Skill tool: flutter-craft:flutter-planning**

This is NOT optional. The workflow is incomplete without a detailed implementation plan.

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended
- **Clean Architecture always** - Domain → Data → Presentation layer order
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Test priority** - Repository/DataSource → State → Widget

## Red Flags

**Never skip brainstorming because:**
- "It's just a simple widget" → Widgets need architecture context
- "I already know what to build" → User might have different expectations
- "Time is short" → Poor design costs more time later
- "It's obvious" → Assumptions cause bugs
