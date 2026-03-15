---
name: c-verify-skill
description: Run C/C++ static analysis using clang-tidy and cppcheck to scan code, check quality, verify C code, detect bugs, review staged or modified files before commit.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# C/C++ Static Analysis Tool (AI-Optimized)

## Usage

```bash
# Check staged files (most common)
$SKILL_DIR/scripts/run_c_checks.sh --git-staged --project-root /path/to/project

# Check modified files
$SKILL_DIR/scripts/run_c_checks.sh --git-modified --project-root /path/to/project

# Check specific file
$SKILL_DIR/scripts/run_c_checks.sh -f code/main.c --project-root /path/to/project

# Check directory
$SKILL_DIR/scripts/run_c_checks.sh -d code/APP --project-root /path/to/project
```

**Required**: `--project-root` parameter must be provided.

## Output Format

Default output is JSON with 5 sections:

```json
{
  "summary": {
    "files_checked": 5,
    "errors": 1,
    "warnings": 8,
    "info": 1,
    "total": 10,
    "priority": "medium"  // high/medium/low
  },
  "issues_by_check": {
    "bugprone-macro-parentheses": {"count": 7},
    "clang-diagnostic-macro-redefined": {"count": 1}
  },
  "issues": [
    {"file": "code/main.c", "line": 48, "severity": "error", "message": "...", "check": "..."}
  ],
  "global_issues": [
    {"severity": "info", "message": "...", "check": "toomanyconfigs"}
  ],
  "top_files": [
    {"file": "code/xTarget.h", "issue_count": 4}
  ]
}
```

## AI Processing Guide

1. **Check priority**: `high` → must fix errors, `medium` → suggest fixes, `low` → optional
2. **Group by check**: Use `issues_by_check` to identify common issues and provide unified fix
3. **Focus on top_files**: Prioritize files with most issues
4. **Separate global_issues**: Usually tool config warnings, show last or ignore
5. **Provide fixes**: Based on `check` field, give specific code examples

**Response Template**:
```
Analysis complete! Priority: {priority} ({errors}E/{warnings}W)

Main issues:
- {check-name} ({count}x) - {explanation}

Top files: {file} ({count} issues)

Fix suggestions:
1. {file}:{line} - {specific fix with code}
```

## Options

- `--severity error`: Show only errors
- `--ignore <pattern>`: Ignore specific checks
- `--format text|markdown`: Alternative formats (not recommended for AI)

## Exit Codes

- 0: No errors (warnings OK)
- 1: Errors found (must fix)
- 2: Tool error or invalid args
