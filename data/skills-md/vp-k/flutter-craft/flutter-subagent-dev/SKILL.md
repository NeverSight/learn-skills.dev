---
name: flutter-subagent-dev
description: Use when executing Flutter implementation plans with independent tasks in the current session
---

# Flutter Subagent-Driven Development

Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review.

**Core principle:** Fresh subagent per task + two-stage review = high quality Flutter code, fast iteration

**Announce at start:** "I'm using the flutter-subagent-dev skill to execute this plan."

## When to Use

```
Have implementation plan?
├─ NO  → Use flutter-brainstorming first
└─ YES → Tasks mostly independent?
         ├─ NO  → Tightly coupled → Use flutter-executing instead
         └─ YES → Stay in this session?
                  ├─ YES → Use flutter-subagent-dev (this skill)
                  └─ NO  → Use flutter-executing (parallel session)
```

**vs. Flutter Executing (batch mode):**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Two-stage review after each task
- Faster iteration

## The Process

```
1. Read plan, extract all tasks, create TodoWrite
   ↓
2. For each task:
   ├─ Dispatch implementer subagent
   ├─ Implementer asks questions? → Answer, then proceed
   ├─ Implementer implements, runs flutter analyze, commits
   ├─ Dispatch spec reviewer subagent
   ├─ Spec compliant?
   │   ├─ NO  → Implementer fixes, re-review
   │   └─ YES → Continue
   ├─ Dispatch code quality reviewer subagent
   ├─ Quality approved?
   │   ├─ NO  → Implementer fixes, re-review
   │   └─ YES → Mark task complete
   └─ Next task
   ↓
3. After all tasks:
   ├─ Dispatch final code reviewer
   └─ Use flutter-finishing skill
```

## Subagent Prompt Templates

### Implementer Subagent

```markdown
You are implementing Task N: [task name]

## Task Description
[Full task text from plan - copy exactly]

## Context
- Project: Flutter app using [BLoC/Provider/Riverpod]
- Architecture: Clean Architecture
- This task is part of: [feature name]
- Previous tasks completed: [list]
- Dependencies: [what this task depends on]

## Layer
[Domain / Data / Presentation / Test]

## Before You Begin
If you have questions about:
- Clean Architecture placement
- State management approach
- Widget composition
- Test strategy

Ask before implementing.

## Your Job
1. Implement exactly as specified in task
2. Run `flutter analyze` - must show no issues
3. Commit with conventional commit message
4. Self-review: Check against task requirements
5. Report what you implemented

## Verification
After implementation:
$ flutter analyze lib/features/<feature>/
Expected: No issues found!
```

### Spec Reviewer Subagent

```markdown
You are reviewing whether an implementation matches its specification.

## What Was Requested
[Full task requirements from plan]

## What Implementer Claims They Built
[From implementer's report]

## CRITICAL: Do Not Trust the Report
Verify everything independently by reading actual code.

**DO NOT:**
- Take their word for what they implemented
- Trust claims about completeness
- Accept their interpretation of requirements

**DO:**
- Read the actual code they wrote
- Compare actual implementation to requirements line by line
- Check for missing pieces
- Look for extra features not in spec

## Your Job
Read the implementation code and verify:

**Missing requirements:**
- Did they implement everything requested?
- Are there requirements they skipped?

**Extra/unneeded work:**
- Did they build things not requested?
- Did they add "nice to haves" not in spec?

**Flutter-Specific Checks:**
- Is the layer correct (Domain/Data/Presentation)?
- Does Clean Architecture structure match?
- Are dependencies pointing correct direction?

**Report:**
- ✅ Spec compliant (everything matches after code inspection)
- ❌ Issues found: [list specifically what's missing or extra, with file:line references]
```

### Code Quality Reviewer Subagent

```markdown
You are reviewing Flutter code quality after spec compliance is confirmed.

## What Was Implemented
[Description]

## Git Range to Review
Base: {BASE_SHA}
Head: {HEAD_SHA}

## Flutter Code Quality Checklist

**Clean Architecture:**
- [ ] Proper layer separation (Domain/Data/Presentation)
- [ ] Dependencies point inward
- [ ] No framework imports in Domain layer

**State Management:**
- [ ] Appropriate pattern for complexity
- [ ] Proper state transitions
- [ ] Error state handling

**Widget Quality:**
- [ ] StatelessWidget preferred when possible
- [ ] Proper const usage
- [ ] No deeply nested trees

**Dart Style:**
- [ ] flutter analyze clean
- [ ] Effective Dart followed
- [ ] Proper null safety

**Tests:**
- [ ] Priority 1 tests (Repository/DataSource) present
- [ ] Priority 2 tests (State) present if applicable
- [ ] Tests actually test logic (not just mocks)

## Output Format

### Strengths
[What's well done?]

### Issues

#### Critical (Must Fix)
[Bugs, security issues, broken functionality]

#### Important (Should Fix)
[Architecture problems, missing features, test gaps]

#### Minor (Nice to Have)
[Style, optimization]

### Assessment
**Ready to proceed?** [Yes/No/With fixes]
```

## Example Workflow

```
You: I'm using Flutter Subagent-Driven Development to execute this plan.

[Read plan: docs/plans/auth-plan.md]
[Extract all 5 tasks with context]
[Create TodoWrite with all tasks]

Task 1: User Entity (Domain Layer)

[Dispatch implementer subagent with full task text]

Implementer: "Implementing User entity in domain layer..."
  - Created lib/features/auth/domain/entities/user.dart
  - flutter analyze: No issues found!
  - Committed: "feat(auth): add User entity"

[Dispatch spec reviewer]
Spec reviewer: ✅ Spec compliant - User entity matches requirements

[Dispatch code quality reviewer]
Code reviewer:
  Strengths: Clean entity, proper const constructor
  Issues: None
  Assessment: Approved

[Mark Task 1 complete]

Task 2: AuthRepository Interface (Domain Layer)

[Dispatch implementer subagent]

Implementer: "Question: Should login return Either<Failure, User> or just User?"

You: "Use Either<Failure, User> pattern with dartz package"

Implementer: "Got it. Implementing..."
  - Created auth_repository.dart with Either return types
  - flutter analyze: No issues found!
  - Committed

[Dispatch spec reviewer]
Spec reviewer: ❌ Issues:
  - Missing: logout() method specified in plan
  - Extra: Added refreshToken() not in spec

[Implementer fixes]
Implementer: Added logout(), removed refreshToken()

[Spec reviewer reviews again]
Spec reviewer: ✅ Spec compliant

[Dispatch code quality reviewer]
Code reviewer: ✅ Approved

[Mark Task 2 complete]

... (continue for remaining tasks)

[After all tasks]
[Dispatch final code reviewer for entire feature]
[Use flutter-finishing skill]
```

## Red Flags

**Never:**
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed issues
- Start code quality review before spec compliance ✅
- Let implementer skip `flutter analyze`
- Ignore subagent questions

**If subagent asks questions:**
- Answer clearly about Clean Architecture placement
- Clarify state management approach
- Provide context about existing patterns

**If reviewer finds issues:**
- Implementer fixes them
- Reviewer reviews again
- Repeat until approved

## REQUIRED SUB-SKILL

After all tasks complete:
→ **flutter-craft:flutter-finishing** (present completion options)
