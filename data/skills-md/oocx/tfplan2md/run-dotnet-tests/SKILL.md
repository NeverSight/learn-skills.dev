---
name: run-dotnet-tests
description: Run .NET tests correctly using the test-with-timeout.sh wrapper to handle .NET 10 dual test runner modes and prevent test hangs.
---

# Run .NET Tests

## Purpose
Provide standardized instructions for running .NET 10 tests correctly. Ensures agents use the `scripts/test-with-timeout.sh` wrapper instead of direct `dotnet test` calls, which fail due to .NET 10's dual test runner architecture.

## When to Use This Skill
- Before committing code changes that affect C# code
- When verifying bug fixes or new features
- When running targeted tests during development
- When the full test suite must pass before marking work complete

## Hard Rules

### Must
- **ALWAYS** use `scripts/test-with-timeout.sh` wrapper - never call `dotnet test` directly
- Run tests from the repository root (the wrapper handles directory changes automatically)
- Use `--solution src/tfplan2md.slnx` for full test suite runs
- Use `--project` with relative paths from `src/` directory (e.g., `--project tests/Oocx.TfPlan2Md.TUnit/`)
- Wait for test completion and check exit code (0 = pass, non-zero = fail)
- For snapshot test changes, use the `update-test-snapshots` skill instead of manual edits

### Must Not
- **NEVER** run `dotnet test` directly from command line - it will fail with `MSB1001: Unknown switch` errors from repo root
- Never manually edit snapshot files in `src/tests/Oocx.TfPlan2Md.TUnit/TestData/Snapshots/` - use the `update-test-snapshots` skill
- Never ignore test failures or skip tests to make CI pass
- Never modify test expectations to match broken output - fix the code, not the tests

## .NET 10 Dual Test Runner Issue

.NET 10 introduced two distinct test runners with incompatible CLI flags:

| Working Directory | Runner Mode | `--solution` | `--project` | `--treenode-filter` | Result |
|-------------------|-------------|:---:|:---:|:---:|---|
| Repo root (`/`) | VSTest | ❌ | ❌ | ❌ | `MSBuild error MSB1001: Unknown switch` |
| `src/` (where `global.json` lives) | Microsoft.Testing.Platform | ✅ | ✅ | ✅ | Works correctly |

The `scripts/test-with-timeout.sh` wrapper automatically:
1. Changes to the `src/` directory (where `global.json` with `"runner": "Microsoft.Testing.Platform"` exists)
2. Normalizes any `src/`-prefixed paths in arguments
3. Enforces a timeout to prevent hung test runs (default 120 seconds)

**Why direct `dotnet test` fails**: Running from repo root activates VSTest mode (no `global.json`), which doesn't support `--solution`, `--project`, or `--treenode-filter` flags. The wrapper ensures tests run from `src/` directory to activate Microsoft.Testing.Platform mode.

## Common Test Commands

### Run Full Test Suite
```bash
scripts/test-with-timeout.sh -- dotnet test --solution src/tfplan2md.slnx
```

### Run Tests with Build
```bash
scripts/test-with-timeout.sh -- dotnet test --solution src/tfplan2md.slnx --configuration Release --verbosity normal
```

### Run Tests Without Build (faster when already built)
```bash
scripts/test-with-timeout.sh -- dotnet test --solution src/tfplan2md.slnx --no-build
```

### Override Timeout (for slow tests)
```bash
scripts/test-with-timeout.sh --timeout-seconds 300 -- dotnet test --solution src/tfplan2md.slnx
```

### Run Specific Project Tests
```bash
scripts/test-with-timeout.sh -- dotnet test --project tests/Oocx.TfPlan2Md.TUnit/
```

## TUnit Test Filtering

**Important**: This project uses TUnit (not xUnit). TUnit uses `--treenode-filter` instead of `--filter`. All TUnit-specific flags must come after `--` in the wrapper command.

### Filter by Class Name (hierarchical pattern)
```bash
scripts/test-with-timeout.sh -- dotnet test --project tests/Oocx.TfPlan2Md.TUnit/ --treenode-filter /*/*/MarkdownRendererTests/*
```

### Filter by Test Method Name
```bash
scripts/test-with-timeout.sh -- dotnet test --project tests/Oocx.TfPlan2Md.TUnit/ --treenode-filter /*/*/*/Render_ValidPlan_ContainsSummarySection
```

### Filter Pattern Explanation
TUnit uses hierarchical path patterns:
- `/*/*/*/TestMethodName` - Match specific test method
- `/*/*/ClassName/*` - Match all tests in a class
- `/*/Namespace.ClassName/*` - Match by namespace and class

## Workflow Integration

### When to Run Tests

1. **During Development** (after each meaningful change):
   ```bash
   # Run targeted tests for the area you modified
   scripts/test-with-timeout.sh -- dotnet test --project tests/Oocx.TfPlan2Md.TUnit/ --treenode-filter /*/*/YourTestClass/*
   ```

2. **Before Committing** (C# code changes only):
   ```bash
   # Run full test suite to ensure no regressions
   scripts/test-with-timeout.sh -- dotnet test --solution src/tfplan2md.slnx --no-build
   ```

3. **Skip Tests When** (documentation/agent instructions only):
   - Changes are limited to `.github/agents/`, `.github/skills/`, `.github/copilot-instructions.md`, or `docs/`
   - No C# code was modified
   - The test suite doesn't validate these file types

### Handling Test Failures

1. **Read the failure output** - TUnit provides detailed error messages
2. **Identify the failing test** - Look for the test method name and class
3. **Run the specific failing test** - Use `--treenode-filter` to isolate it
4. **Debug and fix** - Fix the code (never modify test expectations unless the test itself is wrong)
5. **Re-run tests** - Verify the fix works
6. **Run full suite** - Ensure no regressions before committing

### Snapshot Test Changes

If tests fail because snapshot files need updating (intentional output changes):

1. **Use the `update-test-snapshots` skill** - Never manually edit snapshot files
2. **Verify the new output is correct** - Review the diff carefully
3. **Include `SNAPSHOT_UPDATE_OK` in commit message** - Document the intentional change
4. **Re-run tests** - Confirm all tests pass with new snapshots

## Exit Codes

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | All tests passed | Proceed with commit |
| 1-123 | Test failures | Fix failing tests before committing |
| 124 | Timeout | Increase timeout with `--timeout-seconds` or investigate hung tests |
| 125 | Wrapper error | Check command syntax |

## Golden Example

Complete workflow for implementing a feature:

```bash
# 1. Build the project
dotnet build

# 2. Run targeted tests during development
scripts/test-with-timeout.sh -- dotnet test --project tests/Oocx.TfPlan2Md.TUnit/ --treenode-filter /*/*/MyFeatureTests/*

# 3. Make changes, run tests again
scripts/test-with-timeout.sh -- dotnet test --project tests/Oocx.TfPlan2Md.TUnit/ --treenode-filter /*/*/MyFeatureTests/*

# 4. Before committing, run full suite
scripts/test-with-timeout.sh -- dotnet test --solution src/tfplan2md.slnx --no-build

# 5. If all pass, commit changes
git add .
git commit -m "feat: implement my feature"
```

## Troubleshooting

### Error: `MSBuild error MSB1001: Unknown switch`
**Cause**: Running `dotnet test` directly from repo root (VSTest mode doesn't support `--solution`/`--project` flags)
**Solution**: Use `scripts/test-with-timeout.sh` wrapper

### Error: Timeout after 120 seconds
**Cause**: Tests taking longer than default timeout
**Solution**: Increase timeout with `--timeout-seconds 300` (or higher)

### Error: Test not found with `--treenode-filter`
**Cause**: Incorrect filter pattern or test doesn't exist
**Solution**: 
- List all tests first: `scripts/test-with-timeout.sh -- dotnet test --list-tests`
- Verify filter pattern matches TUnit hierarchical structure

### Snapshot test failures after output changes
**Cause**: Intentional output format changes
**Solution**: Use `update-test-snapshots` skill to regenerate snapshots correctly
