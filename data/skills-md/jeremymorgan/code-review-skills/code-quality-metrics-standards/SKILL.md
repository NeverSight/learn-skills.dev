---
name: code-quality-metrics-standards
description: Analyzes code complexity and adherence to quality standards, flagging overly complex functions and metric outliers. Use when auditing maintainability, cyclomatic complexity, or coding-standard compliance.
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

Analyze code complexity across the codebase:

Look for complex functions/methods.

Also look at functions/methods and calculate/evaluate:

1. CYCLOMATIC COMPLEXITY
   - Functions with complexity > 10
   - Nested if/else depth
   - Switch statement complexity
   - Recommend refactoring for high complexity

2. COGNITIVE COMPLEXITY
   - How hard is the code to understand?
   - Nested loops and conditions
   - Recursive calls
   - Mixed levels of abstraction

3. LINES OF CODE METRICS
   - Functions over 50 lines
   - Files over 300 lines
   - Classes over 500 lines
   - Identify candidates for splitting

4. COUPLING METRICS
   - Afferent coupling (dependencies on this module)
   - Efferent coupling (dependencies of this module)
   - Instability index
   - Identify tightly coupled modules

5. COHESION ANALYSIS
   - Are related functions grouped?
   - Single responsibility adherence
   - Module focus clarity

Provide specific refactoring recommendations for complex areas.

## Provide:

A structured finding report

A scale of 1/10 on how important each finding is

Remediation: precise code-level fix or config change (snippets welcome) if possible

## Constraints & style:

Be concrete and cite exact code locations and identifiers.

Prefer minimal, drop-in fix snippets over prose.

Do not invent files or functions that aren’t present; if context is missing, mark as Unable to verify and say what code would prove it.

Write this into a markdown file and place it in the audits/ folder.
