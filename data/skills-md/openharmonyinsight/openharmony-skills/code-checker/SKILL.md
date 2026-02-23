---
name: code-checker
description: Scan C/C++ codebases for code quality issues including extra large files/functions and circular dependencies. Use when the user asks to check file sizes, find oversized functions, detect circular dependencies, analyze code complexity, find code smells, or identify maintainability issues in C/C++ code. Supports scanning individual files or entire directories with configurable thresholds.
---

# C/C++ Code Checker

Analyzes C/C++ code for maintainability issues: extra large files/functions and circular dependencies between modules.

## Workflow

1. **Identify scan target** - If the user doesn't specify a file or directory, ask: "Which directory or file should I scan?"
2. **Determine check type** - Ask or infer which checks to run:
   - File/Function size analysis
   - Circular dependency detection
   - Both (default for full analysis)
3. **Run the scan** - Execute the appropriate script(s)
4. **Present findings** - Show the report and summarize key issues
5. **Offer help** - Ask if the user wants refactoring assistance

## Size Analysis

Scan for extra large files and functions:

```bash
scripts/scan_cpp_size.py <path> [options]
```

**Options:**
- `-o, --output <file>` - Write report to file
- `-f, --file-threshold <n>` - Large file threshold (default: 2000 effective lines)
- `-F, --function-threshold <n>` - Large function threshold (default: 50 effective lines)

**Example:**
```bash
scripts/scan_cpp_size.py ./src --file-threshold 1500 --function-threshold 40 -o size_report.md
```

## Circular Dependency Detection

Detect circular dependencies between directory modules:

```bash
scripts/circular_header_check.py <path> [options]
```

**Options:**
- `-o, --output <file>` - Write report to file
- `-v, --verbose` - Verbose output
- `--no-gn` - Skip GN build file parsing

**Example:**
```bash
scripts/circular_header_check.py ./src -o circular_report.md
```

The circular dependency checker:
- Parses GN build files (`BUILD.gn`, `*.gni`) for include paths
- Groups files by directory modules (handles `src/` and `include/` as one component)
- Detects when module A includes files from module B, which includes A

## After Finding Issues

When issues are found:

1. **Prioritize by impact** - Start with the largest issues first
2. **Understand context** - Read the code to understand responsibility
3. **Ask the user** - "Would you like help refactoring this?"

## Refactoring Guidance

| Issue Type | Reference |
|------------|-----------|
| Large functions | [references/refactoring.md](references/refactoring.md) |
| Circular dependencies | See [references/circular-deps.md](references/circular-deps.md) |

## What Counts as "Large"?

| Category | Default Threshold | Rationale |
|----------|-------------------|-----------|
| Files | 2000 effective lines | Hard to navigate, understand |
| Functions | 50 effective lines | Beyond cognitive fit, hard to test |

*Effective lines* exclude blank lines, comments, and preprocessor directives.

## File Extensions Scanned

`.c`, `.cpp`, `.cc`, `.cxx`, `.c++`, `.h`, `.hpp`, `.hh`, `.hxx`, `.h++`, `.inl`, `.inc`
