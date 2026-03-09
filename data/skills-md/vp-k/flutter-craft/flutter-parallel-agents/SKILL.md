---
name: flutter-parallel-agents
description: Use when facing 2+ independent Flutter tasks that can be worked on without shared state or sequential dependencies
---

# Dispatching Parallel Flutter Agents

## Overview

When you have multiple unrelated tasks (different features, different test files, different bugs), working on them sequentially wastes time. Each investigation is independent and can happen in parallel.

**Core principle:** Dispatch one agent per independent problem domain. Let them work concurrently.

**Announce at start:** "I'm using the flutter-parallel-agents skill to handle these tasks."

## When to Use

```
Multiple tasks/failures?
├─ NO  → Single agent handles it
└─ YES → Are they independent?
         ├─ NO (related) → Single agent investigates all
         └─ YES → Can they work in parallel?
                  ├─ NO (shared state/files) → Sequential agents
                  └─ YES → Parallel dispatch (this skill)
```

**Use when:**
- Multiple test files failing with different root causes
- Multiple features to implement in different areas
- Each problem can be understood without context from others
- No shared state between investigations
- Different Clean Architecture layers to work on

**Don't use when:**
- Failures are related (fix one might fix others)
- Tasks modify same files
- Tasks have dependencies on each other
- Need to understand full system state first

## Flutter-Specific Parallel Scenarios

### Independent Layer Tasks

```
lib/features/auth/
├── domain/      ← Agent 1: Implement entities & interfaces
├── data/        ← Agent 2: Implement models & datasources
└── presentation/ ← Wait for Agents 1 & 2 (has dependencies)
```

**Can parallelize:** Domain + Data layers (different files)
**Cannot parallelize:** Presentation depends on Domain

### Independent Feature Tasks

```
lib/features/
├── auth/        ← Agent 1: Auth feature
├── profile/     ← Agent 2: Profile feature
└── settings/    ← Agent 3: Settings feature
```

**Can parallelize:** All three (different feature folders)

### Independent Test Fixes

```
test/features/
├── auth/data/repositories/auth_repo_test.dart      ← Agent 1
├── profile/presentation/bloc/profile_bloc_test.dart ← Agent 2
└── settings/data/datasources/settings_ds_test.dart  ← Agent 3
```

**Can parallelize:** Different test files, different features

## The Pattern

### 1. Identify Independent Domains

Group tasks by what's affected:
- Feature A: User authentication
- Feature B: Profile management
- Feature C: Settings storage

Each domain is independent - fixing auth doesn't affect settings.

### 2. Create Focused Agent Tasks

Each agent gets:
- **Specific scope:** One feature or test area
- **Clear goal:** What to implement/fix
- **Constraints:** Don't change other features
- **Expected output:** Summary of what was done

### 3. Dispatch in Parallel

```
Task("Implement auth domain layer - entities and repository interface")
Task("Implement profile domain layer - entities and repository interface")
Task("Implement settings domain layer - entities and repository interface")
// All three run concurrently
```

### 4. Review and Integrate

When agents return:
- Read each summary
- Verify fixes don't conflict
- Run `flutter analyze`
- Run `flutter test`
- Integrate all changes

## Agent Prompt Structure

```markdown
Implement the [Layer] layer for [Feature] feature.

## Scope
lib/features/[feature]/[layer]/

## Files to Create
- entities/[entity].dart
- repositories/[repository].dart (interface)

## Requirements
[Paste specific requirements from plan]

## Constraints
- ONLY modify files in lib/features/[feature]/[layer]/
- Do NOT touch other features
- Follow Clean Architecture principles
- Run flutter analyze before committing

## Expected Output
- Summary of what you created
- flutter analyze result
- Commit message used
```

## Example: Parallel Feature Implementation

**Scenario:** Need to implement domain layers for 3 features

**Decision:** Each domain layer is independent

**Dispatch:**
```
Agent 1 → Implement auth/domain/ (User entity, AuthRepository interface)
Agent 2 → Implement profile/domain/ (Profile entity, ProfileRepository interface)
Agent 3 → Implement settings/domain/ (Settings entity, SettingsRepository interface)
```

**Results:**
- Agent 1: Created User entity, AuthRepository ✅
- Agent 2: Created Profile entity, ProfileRepository ✅
- Agent 3: Created Settings entity, SettingsRepository ✅

**Integration:**
```bash
flutter analyze  # All clean
flutter test     # All pass
git log --oneline -3  # See all three commits
```

## Common Mistakes

**❌ Too broad:** "Implement all features" - agent gets lost
**✅ Specific:** "Implement auth/domain layer" - focused scope

**❌ Dependent tasks in parallel:** Data layer before Domain
**✅ Correct order:** Domain first, then Data in parallel

**❌ Same files:** Two agents editing pubspec.yaml
**✅ No conflicts:** Each agent has isolated file scope

## When NOT to Use

- **Sequential dependencies:** Data layer needs Domain layer first
- **Shared files:** Multiple agents need same file
- **Cross-feature dependencies:** Feature B imports from Feature A
- **Need global context:** Understanding requires seeing entire app

## Verification

After agents return:
1. **Review each summary** - Understand what changed
2. **Check for conflicts** - Did agents edit same files?
3. **Run flutter analyze** - Verify all code is clean
4. **Run flutter test** - Verify tests pass
5. **Check imports** - No circular dependencies

```bash
flutter analyze
flutter test
git diff --stat  # See all changes
```

## Benefits

1. **Parallelization** - Multiple implementations simultaneously
2. **Focus** - Each agent has narrow scope
3. **Independence** - Agents don't interfere
4. **Speed** - N problems solved in time of 1
