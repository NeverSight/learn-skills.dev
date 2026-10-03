---
name: initial-software-design-analysis
description: Produces a first-pass architecture and design review covering structure, maintainability, and scalability. Use when onboarding to or assessing the design of a codebase.
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

Initial Software Design Analysis:

Analyze the project architecture and identify:

Evaluate:
1. Is there clear separation of concerns?
2. Which architectural pattern is used (MVC, Layered, Microservices)?
3. Are there any God objects or modules doing too much?
4. Is the dependency flow clean (no circular dependencies)?
5. Rate the modularity (1-10) with justification

Create an architecture diagram showing:
- Layer dependencies
- Data flow
- External service integrations
- Potential bottlenecks

Identify anti-patterns:
- Spaghetti code
- Copy-paste programming  
- God classes/modules
- Tight coupling
- Missing abstractions

## Provide:

A structured finding report

A scale of 1/10 on how important each finding is

Remediation: precise code-level fix or config change (snippets welcome) if possible

## Constraints & style:

Be concrete and cite exact code locations and identifiers.

Prefer minimal, drop-in fix snippets over prose.

Do not invent files or functions that aren’t present; if context is missing, mark as Unable to verify and say what code would prove it.

Write this into a markdown file and place it in the audits/ folder.
