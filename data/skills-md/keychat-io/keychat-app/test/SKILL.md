---
name: test
description: Run tests for Keychat packages
argument-hint: "[test-file|package]"
disable-model-invocation: true
allowed-tools: Bash(melos *), Bash(flutter test *)
---

Run tests for the Keychat project.

## Arguments
- `$ARGUMENTS` - Optional: specific test file path or package name

## Test Commands

### Run all tests
```bash
melos run test:all
```

### Run Flutter tests only
```bash
melos run test:flutter
```

### Run Dart tests only
```bash
melos run test:dart
```

### Run a specific test file
```bash
cd packages/app
flutter test $ARGUMENTS
```

## Workflow

1. If no arguments provided, run `melos run test:all`
2. If a file path is provided (ends with `.dart`), run that specific test
3. Report test results clearly, including any failures
