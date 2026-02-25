---
name: harmonyos-review
description: >-
  HarmonyOS code review skill for auditing ArkTS projects against official
  Huawei development guidelines and security best practices. Use when
  reviewing HarmonyOS applications for: (1) Security compliance (hardcoded
  credentials, encryption, input validation), (2) ArkTS language standards
  (hilog usage, type safety, magic numbers), (3) Component lifecycle
  management (resource cleanup, event subscription handling), (4) State
  management (V1/V2 decorator consistency), (5) Database operations
  (ResultSet handling, transaction management, encryption), (6) Permission
  management (official permission patterns), (7) Performance issues (async
  forEach, resource leaks), (8) API version compatibility, (9) Kit usage
  best practices. Generates comprehensive markdown reports with prioritized
  fix recommendations.
---

# HarmonyOS Code Review

Audit HarmonyOS ArkTS projects against official Huawei guidelines. Generate prioritized fix reports.

## Review Process

### 1. Quick Scan

Run in parallel to identify critical issues:

```bash
# Hardcoded credentials
grep -r "password\|secret\|key\|token" --include="*.json5" --include="*.ets"

# console instead of hilog
grep -r "console\." --include="*.ets" | grep -v "hilog"

# async forEach anti-pattern
grep -r "forEach.*await" --include="*.ets"

# API version check
grep -r "compileSdkVersion\|targetSdkVersion" --include="*.json5"

# Deprecated API usage
grep -r "@Deprecated\|deprecated" --include="*.ets"
```

### 2. Deep Analysis

Apply checklist from [references/checklist.md](references/checklist.md) per category.

### 3. Generate Report

Use [references/report-template.md](references/report-template.md) as base structure. Include:
- Executive summary (issue counts by priority)
- Detailed findings with `file:line` references
- Prioritized fix recommendations
- Overall grade (A-F)

## References

- **Review checklist**: [references/checklist.md](references/checklist.md) - All review criteria by category
- **Official docs**: [references/official-docs.md](references/official-docs.md) - Huawei guidelines, Kit usage, API patterns
- **Report template**: [references/report-template.md](references/report-template.md) - Output format

## Issue Priority

- **Critical**: Blocks release, fix immediately
- **High**: Fix soon, affects quality
- **Medium**: Technical debt, consider fixing
- **Low**: Optional optimization

## Exit Criteria

- All checklist categories reviewed
- Report generated at `docs/YYYY-MM-DD-review.md`
- Critical/high issues have fix suggestions with `file:line` references
