---
name: aposd-reviewing-module-design
description: "Assesses existing module and interface design for complexity symptoms: information leakage, shallow interfaces, pass-through layers, and unknown unknowns. Produces a structured assessment — not transformations (use aposd-simplifying-complexity to edit) and not new-design generation (use aposd-designing-deep-modules)."
user-invocable: false
---

# Skill: aposd-reviewing-module-design

## Review Is Systematic, Not Intuitive

**Run the checklist.** The checklist exists because intuition misses structural problems.

**Unknown unknowns are highest severity.** If it's unclear what code/info is needed for changes, flag immediately.

---

## Evaluation Checklist

Use this systematic checklist when reviewing code:

### 1. Complexity Symptoms (Ch2)

| Symptom | Question | If Yes |
|---------|----------|--------|
| **Change Amplification** | Does a simple change require modifications in many places? | Flag dependency problem |
| **Cognitive Load** | Must developer know too much to work here? | Flag obscurity or leaky abstraction |
| **Unknown Unknowns** | Is it unclear what code/info is needed for changes? | **Highest severity** - flag immediately |

### 2. Module Depth (Ch4)

| Check | Deep (Good) | Shallow (Bad) |
|-------|-------------|---------------|
| Interface vs implementation | Interface much simpler | Interface rivals implementation |
| Method count | Few, powerful methods | Many, limited methods |
| Hidden information | High | Low |
| Common case | Simple to use | Complex to use |

**Red flag:** If understanding the interface isn't much simpler than understanding the implementation, the module is shallow.

### 3. Information Hiding (Ch5)

| Red Flag | Detection | Severity |
|----------|-----------|----------|
| **Information Leakage** | Same knowledge in multiple modules | High |
| **Temporal Decomposition** | Structure mirrors execution order rather than knowledge | Medium |
| **Back-Door Leakage** | Shared knowledge not visible in interfaces but both depend on it | High |
| **Overexposure** | Common use forces learning rare features | Medium |
| **Silent Failure** | Module swallows errors, returns defaults, or hides failure states from callers | High |

### 4. Layer Abstraction (Ch7)

| Red Flag | Detection | Severity |
|----------|-----------|----------|
| **Pass-Through Method** | Method only passes arguments to another with same API | High |
| **Adjacent Similar Abstractions** | Following operation through layers, abstractions don't change | High |
| **Shallow Decorator** | Large boilerplate, small functionality gain | Medium |

**Test:** Follow a single operation through layers. Does the abstraction change with each method call? If not, there's a layer problem.

### 5. Together/Apart (Ch9)

| Red Flag | Detection | Severity |
|----------|-----------|----------|
| **Conjoined Methods** | Can't understand one method without another's implementation | High |
| **Special-General Mixture** | General mechanism contains use-case specific code | High |
| **Code Repetition** | Same code appears in multiple places | Medium |
| **Shallow Split** | Method split resulted in interface ≈ implementation | Medium |

---

## Together/Apart Decision Procedure

When evaluating whether code should be combined or separated:

```
1. Do pieces share information?
   YES → Should probably be together

2. Would combining simplify the interface?
   YES → Should probably be together

3. Is there repeated code?
   YES → Extract shared method (if long snippet, simple signature)

4. Does module mix general-purpose with special-purpose?
   YES → Should be separated
```

**Key principle:** Depth > Length. Never sacrifice depth for length.

---

## Depth vs Length Rule

| Situation | Correct Action |
|-----------|---------------|
| Long method with clean abstraction | Keep together |
| Short method requiring another's impl to understand | Combine them |
| Method split creating conjoined pair | Undo the split |
| Long method with extractable subtask | Extract subtask only |

**Test for valid split:** Can the pieces be understood independently AND reused separately?

---

## Evaluation Output Format

When reporting findings, use:

```
## Design Review: [Component Name]

### Critical Issues (Must Address)
- [Red flag]: [Specific location] - [Why it's a problem]

### Moderate Issues (Should Address)
- [Red flag]: [Specific location] - [Why it's a problem]

### Observations (Consider)
- [Pattern noticed] - [Potential concern]

### Positive Patterns
- [What's working well]
```

---

## Before Flagging a Problem

Before reporting any red flag, validate:

1. **Steel-man check:** What's the best argument this design choice is intentional?
2. **Intentional shallowness:** Is this an adapter, facade, or decorator where thinness is the point?
3. **Testing seam:** Is this "leakage" actually a legitimate dependency injection point?
4. **Abstraction quality:** Can callers use this interface correctly without knowing implementation details?

---

## Cross-Module Analysis

Ask before concluding:

- **Are there related modules that should be reviewed together?** Classitis often hides across file boundaries.
- **Would combining these modules simplify the overall interface?** If yes, flag as potential shallow split.
- **Must callers use these modules in sequence?** If yes, possible temporal decomposition.

### Pattern Consistency Check

| Question | If Yes |
|----------|--------|
| Is there an existing pattern for this type of problem? | Compare approaches |
| Does this introduce a second way to do the same thing? | Flag unless justified |
| Would a maintainer be surprised by the difference? | Requires explicit documentation |

**Balance:** Evaluate patterns on merit, but don't create gratuitous inconsistency. The goal is maintainability, not conformance.

---

## When Principles Conflict

| Conflict | Resolution |
|----------|------------|
| Depth vs Cohesion | Prefer cohesion. A focused shallow module beats a bloated deep one. |
| Information Hiding vs Testability | Testing seams (injectable dependencies) are acceptable "leakage" |
| Simple Interface vs Configurability | Real systems need configuration; penalize only unnecessary complexity |

---

Detailed per-dimension checklists: `Read(${CLAUDE_SKILL_DIR}/checklists.md)`

---

## Chain

| After | Next |
|-------|------|
| Issues found, transformation needed | `Skill(code-foundations:aposd-simplifying-complexity)` (transformation vs assessment) |
| Issues found, plan needed | Flag for /code-foundations:plan |
| No issues | Done |
