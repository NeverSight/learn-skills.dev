---
name: flutter-review-receive
description: Use when receiving code review feedback - requires technical evaluation and verification, not performative agreement or blind implementation
---

# Flutter Code Review Reception

## Overview

Code review requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

**Announce at start:** "I'm using the flutter-review-receive skill to process this feedback."

## The Response Pattern

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against Flutter/Dart codebase reality
4. EVALUATE: Technically sound for THIS Flutter project?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, run flutter analyze after each
```

## Forbidden Responses

**NEVER:**
- "You're absolutely right!"
- "Great point!" / "Excellent feedback!"
- "Let me implement that now" (before verification)

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working (actions > words)

## Flutter-Specific Verification

### Before Implementing Any Feedback

```bash
# Check current state
flutter analyze
flutter test

# Check what feedback affects
git diff --stat
```

### Clean Architecture Feedback

```
IF reviewer suggests architecture change:
  1. Check: Does current structure follow Clean Architecture?
  2. Check: Are dependencies pointing correct direction?
  3. Check: Will change break existing imports?

Example:
Reviewer: "Move UserModel to domain layer"
✅ VERIFY: "Models with fromJson/toJson belong in data layer, not domain.
           Entities in domain should be pure Dart. Is there a specific reason
           to move this?"
```

### State Management Feedback

```
IF reviewer suggests state management change:
  1. Check: What pattern is currently used? (BLoC/Provider/Riverpod)
  2. Check: Is suggestion compatible with project patterns?
  3. Check: Will change break existing state flow?

Example:
Reviewer: "Use Provider instead of BLoC here"
✅ VERIFY: "Project uses BLoC consistently. Mixing patterns would add complexity.
           Is there a specific reason Provider is better for this case?"
```

### Widget Feedback

```
IF reviewer suggests widget change:
  1. Check: Does widget need to be StatefulWidget?
  2. Check: Will change affect rebuild performance?
  3. Check: Does change follow composition patterns?

Example:
Reviewer: "Convert to StatefulWidget for animation"
✅ VERIFY: "Checking if AnimationController is needed... Yes, animation requires
           TickerProvider. Converting to StatefulWidget with SingleTickerProviderStateMixin."
```

## Implementation Order

For multi-item feedback, implement in this order:

1. **Clarify anything unclear FIRST**
2. **Then implement:**
   - Critical issues (bugs, security)
   - Important issues (architecture, missing tests)
   - Minor issues (style, naming)

3. **After each fix:**
   ```bash
   flutter analyze
   flutter test
   ```

4. **Commit atomically:**
   ```bash
   git add <specific files>
   git commit -m "fix: <specific issue from review>"
   ```

## When To Push Back

Push back when:

### Clean Architecture Violations
```
Reviewer: "Just put the API call in the widget"
❌ WRONG: Implement anyway
✅ RIGHT: "This would violate Clean Architecture - API calls belong in
          DataSource/Repository, not Presentation. Current structure is correct."
```

### YAGNI Violations
```
Reviewer: "Add caching, offline support, and sync"
✅ RIGHT: "Current requirements don't include offline support. Adding caching
          now would be YAGNI. Should we keep scope focused?"
```

### Platform-Specific Concerns
```
Reviewer: "Use this iOS-only package"
✅ RIGHT: "This package is iOS-only but we support Android too.
          Should we find a cross-platform alternative?"
```

### Test Coverage
```
Reviewer: "Add integration tests for everything"
✅ RIGHT: "Following project test priority: Repository/DataSource first,
          then State management, then Widget tests. Integration tests
          are optional. Current coverage follows this pattern."
```

## Acknowledging Correct Feedback

When feedback IS correct:

```
✅ "Fixed. Updated AuthBloc to handle timeout errors."
✅ "Good catch - missing null check in UserModel.fromJson. Fixed."
✅ [Just fix it and show in the code]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
```

**Why no thanks:** Actions speak. Just fix it. The code itself shows you heard the feedback.

## Common Flutter Review Issues

| Feedback | Verification |
|----------|-------------|
| "Add tests" | Check test priority - Repository first, then State, then Widget |
| "Use const" | Check if all parameters are compile-time constants |
| "Split widget" | Check if widget is > 100 lines or has multiple responsibilities |
| "Change state management" | Check project consistency - don't mix patterns |
| "Move to domain layer" | Check if it has framework dependencies (it shouldn't) |
| "Add error handling" | Check if BLoC/Provider has error state |

## Gracefully Correcting Your Pushback

If you pushed back and were wrong:

```
✅ "Checked flutter test output - you're right, the test fails on Android.
   Implementing the fix now."

✅ "Verified in DevTools - the rebuild is happening. Converting to const
   as suggested."

❌ Long apology
❌ Defending why you pushed back
```

## The Bottom Line

**External feedback = suggestions to evaluate, not orders to follow.**

For Flutter specifically:
- Verify against Clean Architecture principles
- Check flutter analyze output
- Run flutter test before and after
- Maintain project patterns consistency

No performative agreement. Technical rigor always.
