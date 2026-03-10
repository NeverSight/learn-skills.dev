---
name: seam-ripper
description: Ruthlessly analyze architectural seams—the interfaces, boundaries, and contracts between system components—to expose coupling problems, abstraction leaks, and design failures. Use when asked to review architecture, analyze coupling, find interface problems, improve module boundaries, audit dependencies, or redesign system structure. Produces uncompromising redesign proposals that prioritize correctness over backwards compatibility.
---

# Seam Ripper

Systematically dissect a codebase's internal architecture to expose where it's wrong and propose what's right.

## Principles

**No sacred cows.** Existing patterns are evidence of past decisions, not correct ones.

**Seams reveal truth.** How components connect exposes what the system actually is, not what documentation claims.

**Backwards compatibility is not a constraint.** The goal is correct architecture. Migration is a separate problem.

**Complexity is guilt until proven innocent.** Every abstraction, indirection, and interface must justify its existence.

## Execution

### Phase 1: Map the Terrain

Build a complete picture of the system's internal structure before judging it.

1. **Identify all modules/packages/namespaces** - List every bounded unit of code
2. **Trace import/dependency graphs** - What depends on what, and why
3. **Catalog public interfaces** - Every exported function, class, type, constant
4. **Find the data contracts** - Shared types, DTOs, schemas that cross boundaries
5. **Locate the integration points** - Where modules actually talk to each other

Output a dependency map showing:
- Module → Module edges with dependency reason
- Circular dependencies (immediate red flags)
- Fan-in/fan-out counts per module

### Phase 2: Interrogate Each Seam

For every boundary identified, answer these questions:

**Interface Clarity**
- Can you understand what this module does from its public interface alone?
- Are there "util" or "helper" exports? (smell: no clear responsibility)
- Does the interface expose implementation details?

**Dependency Direction**
- Does this dependency make conceptual sense?
- Is a "lower-level" module depending on a "higher-level" one?
- Would inverting this dependency simplify both sides?

**Coupling Assessment**
- How many other modules break if this interface changes?
- Is the coupling through data, behavior, or both?
- Could this be an event/message instead of a direct call?

**Abstraction Integrity**
- Does this interface leak implementation details?
- Are callers doing work that belongs inside the module?
- Are there multiple ways to accomplish the same thing?

**Contract Stability**
- How often has this interface changed historically?
- Are there versioned interfaces or deprecation warnings? (smell: unstable contract)
- Do tests mock this interface? (evidence of coupling pain)

### Phase 3: Identify Patterns of Failure

Look for these systemic problems:

| Pattern | Symptoms | What's Actually Wrong |
|---------|----------|----------------------|
| **God Module** | Everything imports it, huge public API | Missing domain boundaries |
| **Shotgun Surgery** | One change requires edits across many modules | Responsibility scattered |
| **Feature Envy** | Module A constantly reaches into Module B's data | Wrong ownership of data/behavior |
| **Inappropriate Intimacy** | Two modules share private details | Should be one module or have explicit contract |
| **Middle Man** | Module just delegates to another | Unnecessary indirection |
| **Parallel Hierarchies** | Adding X requires adding Y in another module | Missing abstraction |
| **Speculative Generality** | Interfaces for flexibility never used | Premature abstraction |
| **Dead Abstraction** | Interface with one implementation forever | Abstraction without purpose |

### Phase 4: Propose the Redesign

For each significant problem, provide:

**1. The Indictment**
State clearly what is wrong and why it matters. Be specific:
- "Module X has 47 public exports and is imported by 23 other modules"
- "The User type is defined in `core` but has fields only used by `billing`"

**2. The Correct Architecture**
Describe what it should look like:
- Clear module boundaries with stated responsibilities
- Dependency direction that follows conceptual hierarchy
- Interfaces that expose intent, not implementation

**3. The Transformation**
Concrete steps to get from wrong to right:
- What moves where
- What gets split or merged
- What interfaces change
- What new abstractions emerge

**4. The Evidence**
Explain why this is better:
- Reduced coupling (quantify: N imports → M imports)
- Clearer responsibilities
- Easier to test, extend, or replace

## Output Format

```markdown
# Seam Analysis: [System/Area Name]

## Dependency Map
[Visual or textual representation of module dependencies]

## Critical Findings

### Finding 1: [Problem Name]
**Location:** [modules/files involved]
**Severity:** Critical | High | Medium
**Pattern:** [which failure pattern]

**Evidence:**
[Specific code/structure references]

**Indictment:**
[Clear statement of what's wrong]

**Redesign:**
[Proposed correct architecture]

**Transformation:**
1. [Step]
2. [Step]
...

### Finding 2: ...

## Recommended Architecture

[Overall vision for how the system should be structured]

## Transformation Sequence

[Ordered list of changes, grouped by logical phases]
```

## Red Lines

Refuse to:
- Propose "incremental improvements" that preserve broken architecture
- Accept "but it works" as justification for poor design
- Recommend adapters/facades that hide problems instead of fixing them
- Preserve interfaces just because they're widely used

Always:
- Name the actual problem, not a symptom
- Propose the correct design, not a compromise
- Quantify coupling and complexity where possible
- Explain the conceptual model that makes the redesign correct
