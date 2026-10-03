---
name: code-duplication-detection
description: Detects duplicated and near-duplicate code across the codebase and suggests consolidation. Use when reviewing for copy-paste code, repeated logic, or DRY violations.
license: CC0-1.0
metadata:
  category: code-quality
allowed-tools: Read Grep Glob Write
disable-model-invocation: true
argument-hint: "[path or scope]"
---

**Target:** $ARGUMENTS

If no target path is given above, review the entire codebase.

---

Examine all the code in our application.

Identify and analyze code duplication in our project. Look for similar looking functions.

Check for:

1. EXACT DUPLICATES
   - Copy-pasted code blocks
   - Identical functions in different files

2. NEAR DUPLICATES
   - Similar logic with different variable names
   - Slightly modified algorithms

3. STRUCTURAL DUPLICATES
   - Similar patterns repeated
   - Boilerplate code

4. DATA DUPLICATION
   - Repeated constants
   - Configuration duplication
   - Schema duplication

For each duplication found:
- Calculate duplication percentage
- Suggest extraction method (function, class, module)
- Provide DRY (Don't Repeat Yourself) solution
- Estimate refactoring effort

In the audit report, recommend a utilities module structure for common functions, including suggested file layout and function groupings.

## Provide:

A structured finding report

A scale of 1/10 on how important each finding is

Remediation: precise code-level fix or config change (snippets welcome) if possible

## Constraints & style:

Be concrete and cite exact code locations and identifiers.

Prefer minimal, drop-in fix snippets over prose.

Do not invent files or functions that aren’t present; if context is missing, mark as Unable to verify and say what code would prove it.

Write this into a markdown file and place it in the audits/ folder.
