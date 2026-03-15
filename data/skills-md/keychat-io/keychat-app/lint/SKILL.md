---
name: lint
description: Run linting, formatting, and static analysis on the codebase
argument-hint: "[fix]"
disable-model-invocation: true
allowed-tools: Bash(melos *), Bash(dart format *), Bash(dart analyze *)
---

Run code quality checks on the Keychat project.

## Arguments
- `$ARGUMENTS` - Optional: "fix" to auto-fix formatting issues

## Commands

### Run all checks (analyze + format check)
```bash
melos run lint:all
```

### Run analyzer only
```bash
melos run analyze
```

### Check formatting
```bash
dart format --set-exit-if-changed .
```

### Fix formatting
```bash
dart format .
```

## Workflow

1. If `$ARGUMENTS` is "fix":
   - Run `dart format .` to fix formatting
   - Then run `melos run analyze` to check for remaining issues

2. Otherwise:
   - Run `melos run lint:all` to check everything
   - Report any issues found

## Analysis configuration
The project uses `very_good_analysis` rules defined in `analysis_options.yaml`.
