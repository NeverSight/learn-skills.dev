---
name: flutter-review-request
description: Use when completing tasks, implementing major features, or before merging to verify Flutter code meets requirements
---

# Requesting Flutter Code Review

Dispatch flutter-craft:flutter-code-reviewer subagent to catch issues before they cascade.

**Core principle:** Review early, review often.

**Announce at start:** "I'm using the flutter-review-request skill to request code review."

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main
- After implementing new Clean Architecture layer

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug
- After adding new state management

## How to Request

### 1. Get git SHAs

```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

### 2. Dispatch flutter-code-reviewer subagent

Use Task tool with flutter-craft:flutter-code-reviewer type:

```
Task tool:
  subagent_type: "flutter-craft:flutter-code-reviewer"
  prompt: |
    ## What Was Implemented
    {WHAT_WAS_IMPLEMENTED}

    ## Requirements/Plan
    {PLAN_OR_REQUIREMENTS}

    ## Git Range to Review
    Base: {BASE_SHA}
    Head: {HEAD_SHA}

    ## Files Changed
    {FILES_CHANGED}

    Please review for:
    - Clean Architecture compliance
    - State management patterns
    - Flutter best practices
    - Test coverage (priority-based)
```

### 3. Act on Feedback

| Issue Severity | Action |
|---------------|--------|
| **Critical** | Fix immediately before proceeding |
| **Important** | Fix before proceeding to next task |
| **Minor** | Note for later, can proceed |

## Flutter-Specific Review Checklist

The reviewer will check:

### Clean Architecture
- [ ] Domain/Data/Presentation separation
- [ ] Dependencies point inward (Domain has no external deps)
- [ ] Entities are pure Dart classes (no framework deps)
- [ ] Repository interfaces in domain, implementations in data

### State Management
- [ ] Appropriate pattern for complexity (BLoC/Provider/Riverpod)
- [ ] No business logic in widgets
- [ ] Proper state transitions
- [ ] Error state handling

### Widget Composition
- [ ] StatelessWidget preferred over StatefulWidget
- [ ] Widgets are focused (single responsibility)
- [ ] No deeply nested widget trees
- [ ] Proper use of const constructors

### Dart Style
- [ ] Effective Dart guidelines followed
- [ ] Proper null safety usage
- [ ] No lint warnings (`flutter analyze` clean)

### Testing
- [ ] Repository tests present (Priority 1)
- [ ] State management tests present (Priority 2)
- [ ] Widget tests if complex UI (Priority 3)

## Example

```
[Just completed Task 3: Add AuthBloc]

You: Let me request code review before proceeding.

BASE_SHA=$(git rev-parse HEAD~3)
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch flutter-craft:flutter-code-reviewer subagent]
  WHAT_WAS_IMPLEMENTED: Authentication feature with login/logout
  PLAN_OR_REQUIREMENTS: Task 1-3 from docs/plans/auth-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  FILES_CHANGED:
    - lib/features/auth/domain/entities/user.dart
    - lib/features/auth/domain/repositories/auth_repository.dart
    - lib/features/auth/data/repositories/auth_repository_impl.dart
    - lib/features/auth/presentation/bloc/auth_bloc.dart

[Subagent returns]:
  ### Strengths
  - Clean layer separation
  - Proper BLoC state handling
  - Good error states

  ### Issues
  #### Important
  - Missing AuthBloc unit tests (auth_bloc_test.dart)
  - No error boundary in LoginScreen

  #### Minor
  - Consider using freezed for state classes

  ### Assessment
  **Ready to merge: With fixes**
  Fix the Important issues before proceeding.

You: [Add AuthBloc tests, add error boundary]
[Continue to Task 4]
```

## Integration with Workflows

### Subagent-Driven Development
- Review after EACH task
- Catch issues before they compound
- Fix before moving to next task

### Executing Plans
- Review after each batch (3 tasks)
- Get feedback, apply, continue

### Ad-Hoc Development
- Review before merge
- Review when stuck

## Red Flags

**Never:**
- Skip review because "it's simple Flutter code"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Skip testing feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show flutter test output that proves it works
- Request clarification on Flutter-specific concerns

## REQUIRED SUB-SKILL

After receiving review feedback, you MUST invoke:
→ **flutter-craft:flutter-review-receive**

Process the feedback systematically before continuing.
