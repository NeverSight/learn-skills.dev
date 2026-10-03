---
name: code-clarity-and-docs
description: "Audits and improves code clarity and documentation using APOSD's obviousness rules: naming quality, comment accuracy, AI-facing doc completeness, and the comments-first workflow for new code. Not for generating project-wide convention docs (use code-standards) or structural simplification of the code itself (use aposd-simplifying-complexity)."
user-invocable: false
---

# Code Clarity and Documentation

## The Obviousness Rule

**If a code reviewer says your code is not obvious, it is not obvious** -- regardless of how clear it seems to you.

**For new code:** Write comments BEFORE implementation. If the comment is hard to write, fix the design, not the comment.

---

## Comments-First Workflow

For new classes/methods, write comments BEFORE implementation:

```
1. Write class interface comment (what abstraction it provides)
2. Write interface comments for public methods (signatures + comments, empty bodies)
3. Iterate on comments until structure feels right
4. Write instance variable declarations with comments
5. Fill in method bodies, adding implementation comments as needed
6. New methods discovered during implementation: comment before body
7. New variables: comment at same time as declaration
```

**Applies to:** writing from scratch, copy-paste-modify, extending functions (>5 lines), interface-changing refactors, prototype-to-production, test methods, non-trivial lambdas.

**Exempt:** one-liner utilities with precise names, trivial getters/setters, character-level bug fixes, temp debug code (mark `// TEMP:`).

---

## Comment Types and When to Use Them

| Type | Where | Purpose |
|------|-------|---------|
| **Interface** | Declarations | Define abstraction, usage info -- required for every public entity |
| **Implementation** | Inside methods | Help understand what code does -- optional for simple methods |
| **Cross-Module** | Dependencies | Describe cross-boundary relationships |

### Interface vs Implementation Comments

| Interface Comment | Implementation Comment |
|-------------------|------------------------|
| Describes externally visible behavior | Describes internal workings |
| Defines the abstraction | Helps understand how code works |
| What user needs to use it | What maintainer needs to modify it |
| **Never include implementation details** | Can reference interface concepts |

---

## The "Different Words" Test

**If your comment restates the code, it adds zero value.** Comments must use different words than the entity they describe.

| Bad | Good |
|-----|------|
| `# Gets user` for `getUser()` | `# Fetches user from cache, falling back to DB` |
| `# Process data` | `# Processes data in chunks to stay under memory limit` |
| `i++ // increment i` | Don't comment this at all |

### Comment Anti-Patterns

| Anti-Pattern | Example | Problem |
|--------------|---------|---------|
| Repeat the code | `i++ // increment i` | Zero value |
| State the obvious | `// loop through users` | Noise |
| Stale comment | Comment says X, code does Y | Dangerous |
| TODO forever | `// TODO: fix this` (no owner, no date) | Clutter |
| Commented-out code | Dead code as comment | Confusion |

### Patterns That Add Value

| Pattern | Example |
|---------|---------|
| Explain rationale | `// Use insertion sort: n < 10 always` |
| Warn about non-obvious | `// Must call before X, else crash` |
| Summarize algorithm | `// Binary search on sorted timestamps` |
| Document edge case | `// Empty list returns -1, not null` |
| Reference external | `// Per RFC 7231 section 6.5.4` |

---

## Variable Comment Checklist

For each variable, answer in the comment:

- [ ] What are the units? (seconds? milliseconds? bytes?)
- [ ] Are boundaries inclusive or exclusive?
- [ ] What does null mean, if permitted?
- [ ] Who owns the resource (responsible for freeing/closing)?
- [ ] What invariants always hold?

**Goal:** Comment should be complete enough that readers never need to examine all usage sites.

---

## Naming Principles

### Two Required Properties

| Property | Requirement | Test |
|----------|-------------|------|
| **Precision** | Name clearly conveys what entity refers to | "Can someone seeing this name in isolation guess what it refers to?" |
| **Consistency** | (1) Always use this name for this purpose (2) Never use it for other purposes (3) All instances have same behavior | Check all usages |

### Naming Procedure

```
1. Name Evaluation Test:
   "If someone sees this name without declaration or context,
   how closely can they guess what it refers to?"

2. Precision Check:
   - Could this name refer to multiple things? -> Too vague
   - Does this name imply narrower usage than actual? -> Too specific
   - Target: name matches actual scope exactly

3. Consistency Check:
   - Is this name used everywhere for this purpose?
   - Is this name used ONLY for this purpose?
   - Do all variables with this name behave identically?
```

### Common Naming Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Vague status words | `blinkStatus` | `cursorVisible` |
| Too generic | `getCount()` | `numActiveIndexlets` |
| Too specific | `delete(Range selection)` | `delete(Range range)` if it works on any range |
| Similar names, different things | `socket` vs `sock` | Distinct, descriptive names |
| Type in name | `strName` | Just `name` |
| Class repeated in variable | `File.fileBlock` | `File.block` |

---

## Red Flags (Code Clarity)

| Red Flag | What It Signals |
|----------|-----------------|
| Comment repeats code | Rewrite with different words |
| Hard to describe | Design problem -- fix the design |
| Hard to pick name | Design smell -- entity lacks clean design |
| Vague name (`status`, `flag`, `data`) | Conveys little information |
| Interface describes implementation | Shallow abstraction |
| Implementation contaminates interface | Violates separation of concerns |

---

## README Accuracy Checklist

- [ ] Does README describe current behavior?
- [ ] Are setup instructions still valid?
- [ ] Do examples still work?
- [ ] Are dependencies current with package manifests?
- [ ] Is the feature list accurate?

---

## Changelog Update Checklist

- [ ] Breaking changes documented with migration instructions?
- [ ] New features listed with usage examples?
- [ ] Bug fixes noted with issue references?
- [ ] Version number bumped if needed?

---

## AI Documentation Audit

Check any AI config files that exist in the project (`CLAUDE.md`, `AGENTS.md`, editor rule files such as `.cursorrules`, `.windsurfrules`, `.clinerules`, `.roomodes`, and similar):

- [ ] AI docs reflect current architecture?
- [ ] Agent/skill descriptions accurate?
- [ ] File structure documentation up to date?
- [ ] All AI config files consistent with each other?
- [ ] Version numbers synchronized across docs and manifests?

---

## Severity Guide

| Finding | Severity |
|---------|----------|
| README contradicts actual behavior | CRITICAL |
| API doc says wrong return type | CRITICAL |
| Stale comment causes bug risk | CRITICAL |
| CLAUDE.md describes deleted/renamed files | CRITICAL |
| New public API undocumented | IMPORTANT |
| Breaking change not in changelog | IMPORTANT |
| CLAUDE.md missing new features/agents | IMPORTANT |
| AI doc version mismatch | IMPORTANT |
| Stale TODO from distant past | SUGGESTION |
| Could add clarifying comment | SUGGESTION |
| Minor README improvement | SUGGESTION |

---

Detailed checklists for code review: `Read(${CLAUDE_SKILL_DIR}/checklists.md)`

---

## Chain

| After | Next |
|-------|------|
| Code written or changed | Audit using this skill + `${CLAUDE_SKILL_DIR}/checklists.md` |
| Docs verified | Done (pre-commit gate) |
