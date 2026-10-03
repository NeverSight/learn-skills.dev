---
name: solid-principles
description: Audits code for adherence to the five SOLID principles and reports violations with concrete fixes. Use when reviewing class design, dependency structure, or object-oriented quality.
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

Evaluate this application and its adherence to SOLID principles:


Check each principle:

1. SINGLE RESPONSIBILITY (SRP)
   - Does each module have one reason to change?
   - Identify modules violating SRP
   - Example: UserController handling emails, payments, and auth

2. OPEN/CLOSED PRINCIPLE
   - Can we extend without modifying?
   - Are there hardcoded switch statements that should be polymorphic?
   - Check for if/else chains that could be strategy pattern

3. LISKOV SUBSTITUTION
   - Do derived classes properly extend base classes?
   - Any violations of expected behavior?

4. INTERFACE SEGREGATION
   - Are interfaces too large?
   - Do clients depend on methods they don't use?

5. DEPENDENCY INVERSION
   - Are we depending on abstractions or concretions?
   - Is there proper dependency injection?
   - Check for 'new' keyword usage vs injection

Rate SOLID compliance (1-10) with specific violations and fixes.

## Provide:

A structured finding report

A scale of 1/10 on how important each finding is

Remediation: precise code-level fix or config change (snippets welcome) if possible

## Constraints & style:

Be concrete and cite exact code locations and identifiers.

Prefer minimal, drop-in fix snippets over prose.

Do not invent files or functions that aren’t present; if context is missing, mark as Unable to verify and say what code would prove it.

Write this into a markdown file and place it in the audits/ folder.
