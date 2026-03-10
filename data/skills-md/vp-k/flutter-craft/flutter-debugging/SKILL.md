---
name: flutter-debugging
description: Use when encountering any bug, test failure, or unexpected behavior in Flutter - requires systematic investigation before proposing fixes
---

# Systematic Flutter Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Announce at start:** "I'm using the flutter-debugging skill to investigate this issue."

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY Flutter technical issue:
- Widget build errors
- State management bugs
- Test failures
- UI rendering issues
- Navigation problems
- API/network errors
- Build failures
- Platform-specific issues

**Use this ESPECIALLY when:**
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- Under time pressure

## Flutter Debugging Tools

### 1. Console Logging

```dart
// Basic logging (truncates long output)
print('Debug: $value');

// No truncation (preferred)
debugPrint('Debug: $value');

// Conditional debug logging
import 'package:flutter/foundation.dart';
if (kDebugMode) {
  debugPrint('Only in debug mode: $value');
}

// Developer log with tags
import 'dart:developer';
log('API response', name: 'NetworkService', error: e);
```

### 2. Flutter DevTools

```bash
# Open DevTools
flutter run --start-paused
# Then press 'd' or use DevTools button in IDE
```

**DevTools Panels:**
- **Widget Inspector:** Widget tree, properties, layout
- **Performance:** Timeline, frame rendering
- **Memory:** Heap usage, leaks
- **Network:** HTTP requests/responses
- **Logging:** All logs in one place

### 3. Debug Widgets

```dart
// Show widget boundaries
debugPaintSizeEnabled = true;

// Show baseline alignments
debugPaintBaselinesEnabled = true;

// Show repaint regions
debugRepaintRainbowEnabled = true;
```

### 4. Breakpoints

```dart
// Programmatic breakpoint
import 'dart:developer';
debugger();

// Or use IDE breakpoints
```

## The Four Phases

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

#### 1. Read Error Messages Carefully

```
════════════════════════════════════════════════════════════
EXCEPTION CAUGHT BY WIDGETS LIBRARY
════════════════════════════════════════════════════════════
The following assertion was thrown building MyWidget:
'package:flutter/src/widgets/container.dart': Failed assertion: line 287
'child != null || decoration != null || constraints != null'
════════════════════════════════════════════════════════════
```

**Don't skip past errors!** They often contain the exact solution.

#### 2. Reproduce Consistently

```bash
# Hot reload to reproduce
r  # in terminal

# Hot restart (clears state)
R  # in terminal

# Full restart
flutter run
```

- Can you trigger it reliably?
- What are the exact steps?
- Does Hot Reload vs Hot Restart matter?

#### 3. Check Recent Changes

```bash
# What changed recently?
git diff

# Recent commits
git log --oneline -10

# Diff with specific commit
git diff HEAD~3
```

#### 4. Add Diagnostic Logging

```dart
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    debugPrint('=== MyWidget.build() ===');
    debugPrint('context.mounted: ${context.mounted}');

    final state = context.watch<MyState>();
    debugPrint('state: $state');

    return Container(...);
  }
}
```

### Phase 2: Pattern Analysis

#### 1. Find Working Examples

```bash
# Search for similar working code
grep -r "similar_pattern" lib/
```

- What works that's similar to what's broken?
- Compare widget structure, state management

#### 2. Compare Against References

```dart
// Reference: Working widget
class WorkingWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<WorkingBloc, WorkingState>(
      builder: (context, state) => ...,
    );
  }
}

// Broken: My widget
class BrokenWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // What's different?
    return BlocBuilder<MyBloc, MyState>(
      builder: (context, state) => ...,
    );
  }
}
```

#### 3. Identify Differences

List every difference, however small:
- Widget type
- State provider location
- BuildContext usage
- Lifecycle methods

### Phase 3: Hypothesis and Testing

#### 1. Form Single Hypothesis

State clearly:
> "I think the issue is [X] because [Y]"

Example:
> "I think the build error is because the BLoC is not provided above this widget in the widget tree"

#### 2. Test Minimally

Make the SMALLEST possible change:

```dart
// Before (broken)
Widget build(BuildContext context) {
  final bloc = context.read<MyBloc>();
  return ...;
}

// After (testing hypothesis)
Widget build(BuildContext context) {
  debugPrint('Looking for MyBloc...');
  try {
    final bloc = context.read<MyBloc>();
    debugPrint('Found: $bloc');
  } catch (e) {
    debugPrint('Error: $e');
  }
  return ...;
}
```

#### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### Phase 4: Implementation

#### 1. Create Test Case (Optional based on priority)

For Repository/DataSource issues (Priority 1):
```dart
test('should return user when API succeeds', () async {
  // Arrange
  when(mockApi.getUser(any)).thenAnswer((_) async => userModel);

  // Act
  final result = await repository.getUser('123');

  // Assert
  expect(result, equals(userEntity));
});
```

#### 2. Implement Single Fix

ONE change at a time:

```dart
// Fix the root cause identified in Phase 3
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => getIt<MyBloc>(),
      child: BlocBuilder<MyBloc, MyState>(...),
    );
  }
}
```

#### 3. Verify Fix

```bash
# Run analysis
flutter analyze

# Run tests
flutter test

# Manual verification
flutter run
# Test the specific scenario
```

#### 4. If Fix Doesn't Work

- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze
- **If ≥ 3: STOP and question the architecture**

## Common Flutter Issues & Root Causes

| Symptom | Common Root Cause |
|---------|------------------|
| "No ancestor found" | Provider/BLoC not in widget tree above |
| "setState after dispose" | Async operation completing after widget disposed |
| "RenderBox not laid out" | Unbounded constraints (Column in Column, etc.) |
| "Null check operator" | Variable not initialized or API returned null |
| "Build during build" | setState called during build phase |
| "Ticker not disposed" | Missing `with TickerProviderStateMixin` or dispose |

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now"
- "Just wrap it in a try-catch"
- "Add a null check here"
- "Just add a Container around it"
- "Maybe just hot restart"
- "It's probably a state issue, let me reset"

**ALL of these mean: STOP. Return to Phase 1.**

## REQUIRED SUB-SKILL

After fixing the bug, you MUST invoke:
→ **flutter-craft:flutter-verification**

Verify the fix with `flutter analyze`, `flutter test`, and manual testing.

## Quick Reference

| Phase | Flutter Activities | Success Criteria |
|-------|-------------------|------------------|
| **1. Root Cause** | Read error, reproduce, add debugPrint | Understand WHAT and WHY |
| **2. Pattern** | Find working widgets, compare | Identify differences |
| **3. Hypothesis** | Form theory, minimal test | Confirmed or new hypothesis |
| **4. Implementation** | Create test (priority-based), fix, verify | Bug resolved, analysis clean |

## Real-World Impact

- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common
