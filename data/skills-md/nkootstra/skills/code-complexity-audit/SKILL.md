---
name: code-complexity-audit
description: >-
  Scan and analyze a software repository or project for design quality using
  principles from A Philosophy of Software Design by John Ousterhout. Use when
  user asks to review, audit, scan, or evaluate code quality, design quality,
  architecture, or technical debt. Also trigger for: code review, design review,
  complexity analysis, code health check, module depth analysis, information
  hiding review, how good is my code, review my project, find design problems,
  what is wrong with my codebase, rate my code, or anything about evaluating
  software design quality at a structural level. This is not a linter or style
  checker. It evaluates deep design qualities like module depth, abstraction
  quality, information hiding, and complexity patterns.
---

# Code Complexity Audit

Deep software design analysis based on "A Philosophy of Software Design" by John Ousterhout. Produces a **Design Health Report** evaluating structural and conceptual design quality — not linting or style.

## Process

1. Read this file
2. Read `references/analysis-framework.md` for detailed checklists and scoring rubrics
3. Scan the project structure and key files
4. Produce the Design Health Report

### Step 1: Reconnaissance

- List project structure (2-3 levels deep)
- Identify language(s), framework(s), paradigm (OOP, functional, etc.)
- Count approximate files, modules/classes, lines of code
- Identify entry point(s) and core modules
- Check dependency files (package.json, requirements.txt, go.mod, Cargo.toml, etc.)

### Step 2: Sampling Strategy

- **Always read**: Entry points, core domain modules, most-imported files
- **Sample**: 3-5 files from each major directory/package
- **Prioritize**: Largest, most-changed (git history), most-imported files
- **Include**: Public API surfaces, interfaces, error handling, tests

Aim for **15-30 representative files** depending on project size.

### Step 3: Deep Analysis

Read `references/analysis-framework.md` for the full framework. Evaluate across 15 dimensions:

**Core Design Structure** (highest weight):
1. **Module Depth** — Deep (simple interface, rich functionality) vs shallow?
2. **Information Hiding** — Knowledge encapsulated or leaking?
3. **Abstraction Quality** — Right level? True or false abstractions?
4. **Complexity Indicators** — Change amplification, cognitive load, unknown unknowns

**Structural & Process** (medium weight):
5. **Error Handling** — Defined out of existence, masked, or proliferating?
6. **Naming & Obviousness** — Clear mental images? Obvious code?
7. **Comments & Documentation** — Describe non-obvious things?
8. **Consistency** — Conventions followed uniformly?
9. **Layering** — Different layer = different abstraction? Or pass-through?
10. **Strategic vs. Tactical** — Design investment or quick fixes?

**Deep Structural Patterns**:
11. **Design Investment & Evolution** — Improving over time? "Design it Twice" evidence?
12. **Software Trends Anti-Patterns** — Getter/setter overuse, deep inheritance, forced patterns?
13. **Performance-Design Relationship** — Simplicity creating speed or complexity creating overhead?
14. **Comments as Design Tool** — Completing abstractions or afterthoughts?
15. **Codebase Navigability** — Zero-context newcomer can navigate from file tree alone?

### Step 4: Produce the Report

```markdown
# Code Complexity Audit: [Project Name]

## Executive Summary
[2-3 sentence assessment w/ letter grade A-F]

## Scores
[Table: each dimension scored 1-10 w/ brief justification]

## Top Findings

### Critical Design Issues
[Most severe — actively creating complexity]

### Improvement Opportunities
[Moderate — could be cleaner]

### Design Strengths
[What the project does well — always include]

## Detailed Analysis
[Per-dimension subsections w/ file/line references and code examples]

## Red Flags Detected
[Reference the canonical red flags list below]

## Recommendations
[Prioritized, actionable — what to fix first and how]

## Appendix: Files Reviewed
[All files examined]
```

## Ousterhout's Design Principles

Evaluate the project against each:

1. **Complexity is incremental** — small stuff accumulates
2. **Working code isn't enough** — design quality matters equally
3. **Continual small investments** — 10-20% of time on design improvement
4. **Modules should be deep** — simple interfaces, rich functionality
5. **Common case should be simple** — good defaults, minimal config
6. **Simple interface > simple implementation** — callers' ease matters more
7. **General-purpose modules are deeper** — avoid over-specialization
8. **Separate general-purpose and special-purpose** — push specialization up/down
9. **Different layers = different abstractions** — no pass-through layers
10. **Pull complexity downwards** — developers suffer, not users
11. **Define errors out of existence** — simplify error semantics
12. **Design it twice** — consider alternatives before committing
13. **Comments describe non-obvious things** — different level of detail than code
14. **Design for reading, not writing**
15. **Increments = abstractions, not features**
16. **Separate what matters from what doesn't**
17. **Not making design better → making it worse** — continuous evolution

## Red Flags

| Red Flag | Signal |
|---|---|
| **Shallow Module** | Interface nearly as complex as implementation |
| **Information Leakage** | Same design decision in multiple modules |
| **Temporal Decomposition** | Structured by execution order, not information hiding |
| **Overexposure** | Common-case users must learn rare features |
| **Pass-Through Method** | Forwards to another method w/ same signature |
| **Repetition** | Same nontrivial pattern in multiple places |
| **Special-General Mixture** | Special-purpose code in general-purpose mechanisms |
| **Conjoined Methods** | Can't understand one without reading another |
| **Comment Repeats Code** | Restates what code says |
| **Implementation in Interface Docs** | Interface docs describe implementation |
| **Vague Name** | Too generic to convey meaning |
| **Hard to Pick Name** | Naming difficulty → unclear design |
| **Hard to Describe** | Needs long comment → bad abstraction |
| **Nonobvious Code** | Behavior unclear from quick reading |

## Tone & Approach

- **Constructive** — help, not tear down
- Always include **strengths**
- **Specific** — reference files, classes, methods, line numbers
- **Actionable** recommendations w/ before/after examples
- **Context-aware** — weekend prototype ≠ production system
- Use the project's own code in examples

## Adapting to Project Size

- **Small** (<20 files): Read everything. Concise report.
- **Medium** (20-200 files): Sample. Focus on core modules.
- **Large** (200+ files): Heavy sampling. Focus on architecture and public APIs. Consider one subsystem deeply vs. everything shallowly.
