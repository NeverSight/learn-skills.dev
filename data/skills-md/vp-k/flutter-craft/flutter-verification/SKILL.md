---
name: flutter-verification
description: Use when about to claim work is complete, fixed, or passing - requires running Flutter verification commands and confirming output before making any success claims; evidence before assertions always
---

# Flutter Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## Flutter Verification Commands

### 1. Static Analysis (Always Required)

```bash
flutter analyze
```

**Expected output:**
```
Analyzing <project>...
No issues found!
```

**If issues found:**
```
Analyzing <project>...
   info • ... • lib/path/file.dart:42:10 • ...
   warning • ... • lib/path/file.dart:50:5 • ...

3 issues found. (1 warning, 2 hints)
```

### 2. Unit Tests (Priority 1 & 2)

```bash
# All tests
flutter test

# Specific feature tests
flutter test test/features/<feature>/

# Specific test file
flutter test test/features/<feature>/data/repositories/user_repository_test.dart
```

**Expected output:**
```
00:05 +12: All tests passed!
```

**If tests fail:**
```
00:03 +10 -2: Some tests failed.
```

### 3. Build Verification

```bash
# Android debug build
flutter build apk --debug

# iOS debug build (macOS only)
flutter build ios --debug --no-codesign

# Web build
flutter build web
```

**Expected output:**
```
✓ Built build/app/outputs/flutter-apk/app-debug.apk (XX.XMB)
```

### 4. Format Check (Optional)

```bash
dart format --set-exit-if-changed lib/
```

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Flutter Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| "Code is clean" | `flutter analyze`: No issues | "I wrote correct code" |
| "Tests pass" | `flutter test`: All passed | "Should pass", "Looks correct" |
| "Build succeeds" | `flutter build`: Built successfully | "Analyze passed" |
| "Feature complete" | All verification + requirements check | "Tests pass" |
| "Bug fixed" | Test original symptom + verify | "Code changed" |
| "Widget works" | Widget test or manual verification | "Code looks right" |

## Red Flags - STOP

If you catch yourself thinking or saying:

- "should work now"
- "probably passes"
- "looks correct"
- "I'm confident"
- "just this once"
- "analyze passed, so build will work"
- "the code is right"
- **ANY wording implying success without running verification**

**STOP. Run the verification command.**

## Verification Checklist

Before claiming completion:

```markdown
### Verification Results

**Static Analysis:**
```bash
$ flutter analyze
Analyzing flutter_app...
No issues found!
```
✅ Passed

**Unit Tests:**
```bash
$ flutter test test/features/<feature>/
00:05 +12: All tests passed!
```
✅ 12/12 passed

**Build:**
```bash
$ flutter build apk --debug
✓ Built build/app/outputs/flutter-apk/app-debug.apk
```
✅ Built successfully

**Ready to claim completion.**
```

## Key Patterns

**Static Analysis:**
```
✅ [Run flutter analyze] [See: No issues found!] "Analysis passes"
❌ "Code looks clean" / "I wrote it correctly"
```

**Tests:**
```
✅ [Run flutter test] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Tests look correct"
```

**Build:**
```
✅ [Run flutter build] [See: Built successfully] "Build passes"
❌ "Analyze passed" (analyze doesn't check build)
```

**Feature completion:**
```
✅ Re-read plan → Verify each requirement → Run all verifications → Report
❌ "Tests pass, feature complete"
```

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN flutter analyze/test |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Analyze passed" | Analyze ≠ build ≠ test |
| "Code looks right" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "It's simple code" | Simple code can still fail |

## Why This Matters

- **Trust:** If you claim "tests pass" without running them, trust is broken
- **Time:** False completion → redirect → rework wastes everyone's time
- **Quality:** Unverified code may crash in production
- **Integrity:** Honesty is a core value

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction ("Done!", "Fixed!", "Works!")
- Committing code
- Creating PRs
- Moving to next task
- Reporting to user

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

```bash
# Always run these before claiming completion:
flutter analyze
flutter test
flutter build apk --debug  # or appropriate build target
```

This is non-negotiable.
