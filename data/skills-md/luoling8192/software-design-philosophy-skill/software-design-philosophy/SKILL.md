---
name: software-design-philosophy
description: >
  Software design philosophy guide based on John Ousterhout's "A Philosophy of Software Design."
  Use this skill during: code reviews, architecture discussions, API design, module decomposition decisions,
  refactoring guidance, complexity analysis, naming and commenting improvements, error handling strategy design.
  Trigger when the user mentions "code is too complex", "how to split modules", "interface design",
  "reduce coupling", "deep/shallow modules", "information leakage", "error handling", "code readability",
  "design philosophy", "pull complexity down", "define errors out of existence", or similar topics.
  Also trigger for any code review where design quality feedback is requested.
---

# A Philosophy of Software Design — Distilled Guide

> Source: John Ousterhout, *A Philosophy of Software Design*
> Central thesis: **The core challenge of software design is managing complexity.**

---

## I. Complexity: Know the Enemy

### Definition

Complexity is anything related to the structure of a software system that makes it **hard to understand and modify**. Complexity is not the same as system size — a small system can be complex, and a large well-designed system can be manageable.

### Three Symptoms of Complexity

1. **Change Amplification**: A seemingly simple change requires code modifications in many different places.
2. **Cognitive Load**: Developers must absorb a large amount of information to complete a task safely. Note: fewer lines of code ≠ simpler — sometimes more code is actually simpler because it reduces cognitive load.
3. **Unknown Unknowns**: It's unclear which code must be modified or what information is needed to complete a task. This is the most dangerous symptom.

### Two Root Causes

1. **Dependencies**: A piece of code cannot be understood or modified in isolation; it relates to other code that must also be considered.
2. **Obscurity**: Important information is not obvious — vague names, missing docs, implicit conventions, hidden constraints.

### Key Insight

- **Complexity is incremental**: It's not caused by a single catastrophic error; it accumulates through thousands of small decisions.
- Therefore you must adopt a **zero-tolerance** mindset — every bit of "minor" complexity matters.

---

## II. Strategic vs. Tactical Programming

### Tactical Programming (Anti-pattern)
- Goal: get features working as quickly as possible.
- Mindset: "Just make it work", "We'll refactor later."
- Result: complexity accumulates fast, tech debt spirals out of control.

### Strategic Programming (Recommended)
- Goal: produce great design; working code is a byproduct.
- Mindset: **invest roughly 10–20% of development time in design improvements.**
- Practices:
  - Look for opportunities to improve design with every change.
  - Working code is not enough — design quality matters equally.
  - The increments of software development should be **abstractions**, not features.

---

## III. Deep Modules: The Most Important Design Concept

### Core Metaphor

Think of a module as a rectangle:
- **Width** = complexity of its interface
- **Height/Depth** = amount of functionality hidden inside

**Deep module**: simple interface, rich implementation. (Good design)
**Shallow module**: complex interface, does very little. (Bad design 🚩)

### Classic Examples

- **Deep**: Unix file I/O — just 5 syscalls (open, read, write, lseek, close) expose a powerful file system.
- **Shallow**: Java I/O — reading a file requires composing FileInputStream, BufferedInputStream, ObjectInputStream, etc.

### Practical Principles

- Design interfaces so the **most common usage is as simple as possible**.
- A simple interface matters more than a simple implementation.
- Rare use cases can accept more complex calling patterns, but the common path should never pay for them.

---

## IV. Information Hiding and Information Leakage

### Information Hiding
- Each module should encapsulate **design decisions** (knowledge), exposing only a simplified interface.
- Hidden information includes: data structures, algorithms, low-level mechanisms, policy decisions.
- Information hiding minimizes inter-module dependencies.

### Information Leakage 🚩 Red Flag
- When the same design decision is reflected in multiple modules, information has leaked.
- **Temporal decomposition** is a common source: splitting modules by execution order (rather than by information hiding) causes steps to share excessive knowledge.

### Fixing Leakage
- Merge shared knowledge into a single module.
- If merging isn't possible, unify the shared information behind a single deep module.

---

## V. General-Purpose vs. Special-Purpose Modules

### Core Principle: General-purpose modules are usually deeper.

- A general interface is simpler than a specialized one because it covers more use cases with fewer methods.
- When designing a new module, ask: **What is the most general-purpose interface that can satisfy my current needs?**

### Judgment Criteria

- The interface should be general enough to support multiple use cases without modification.
- But the implementation can do only what's currently needed (don't over-build).
- General-purpose and special-purpose code should be **cleanly separated**.

---

## VI. Different Layers, Different Abstractions

### Principle
- A software system has multiple layers; each layer should provide a **different abstraction** from its adjacent layers.
- If two layers have similar abstractions, the layering is wrong.

### Pass-Through Method 🚩 Red Flag
- A method that does almost nothing except forward its arguments to another method with a similar signature.
- This signals that the layers don't offer different abstractions — the responsibility split is flawed.

### Pass-Through Variable 🚩 Red Flag
- A variable threaded from top to bottom through layers that don't use it.
- Solutions: context objects, dependency injection, or rethinking module boundaries.

---

## VII. Pull Complexity Downward

### Core Principle
- When complexity is unavoidable, the **module should absorb it internally** rather than pushing it to callers.
- Most modules have more users than developers — it's better for developers to suffer than for every user to suffer.

### Anti-patterns
- Turning hard decisions into configuration parameters and pushing them to sysadmins.
- Throwing exceptions for uncertain conditions and letting callers handle them.
- These save effort in the short term but amplify complexity system-wide.

---

## VIII. Define Errors Out of Existence

### Core Insight
- Exception handling is one of the biggest sources of complexity.
- Reducing the number of exceptions that must be handled is one of the best techniques for reducing complexity.

### Strategies

1. **Redefine semantics so the error condition cannot arise.**
   - Example: `unset(key)` succeeds even if the key doesn't exist — it simply guarantees "after the call, the key does not exist."
   - Example: `substring(start, end)` auto-clips out-of-bounds parameters instead of throwing.

2. **Exception Masking**: Detect and handle exceptions at a low level so they never reach callers.

3. **Exception Aggregation**: Handle multiple exception types in one centralized place instead of scattering handlers at every call site.

### Important Distinction
- This is not about ignoring errors — it's about **designing better semantics so error conditions simply aren't errors**.
- Errors that truly require reporting (e.g., lost network packets) must still be handled properly.

---

## IX. Design It Twice

- For any important design decision, conceive **at least two different approaches** before choosing.
- Even if the first idea seems great, force yourself to think of an alternative.
- Comparison dimensions: interface simplicity, generality, performance, implementation difficulty.
- This habit significantly improves design quality.

---

## X. The Philosophy of Comments

### Why Write Comments
1. Comments capture **design decisions and intent** that code cannot express.
2. Comments are part of the abstraction — good interface docs mean users don't have to read the implementation.
3. Writing comments **early** exposes design problems before you invest in code.
4. Good comments dramatically reduce cognitive load.

### What Comments Should Describe
- **Non-obvious information**: the *why*, constraints, boundary conditions, side effects — things you can't see in the code.
- Comments should NOT repeat what the code already says. 🚩 Red Flag: Comment Repeats Code

### Comment Layers
- **Interface comments**: describe *what* and *why* — no implementation details.
- **Implementation comments**: explain *how* and *why this approach* — why the code is written this way.
- **Cross-module comments**: document design decisions and dependencies that span module boundaries.

### Comments-First Approach
- Write interface comments *before* writing the implementation — use comments as a design tool.
- If you can't write a clear comment, the design itself probably has a problem.

---

## XI. The Art of Naming

### Standards for Good Names
- **Precise**: conveys meaning to the reader without ambiguity.
- **Consistent**: the same name always means the same thing across the codebase.
- **Informative**: a good name is lightweight documentation by itself.

### Naming Red Flags 🚩
- **Vague names**: too generic (e.g., `data`, `result`, `tmp`, `info`) — carry no useful information.
- **Hard to name**: if you struggle to find a precise, intuitive name for an entity, the design itself may be flawed.

---

## XII. Consistency

- Handle **the same thing the same way** throughout the entire system.
- Consistency covers: naming, coding style, interface patterns, design patterns, invariants.
- Consistency dramatically reduces cognitive load — once a developer learns one pattern, it applies everywhere.
- Don't break consistency for "better" unless the improvement is significant enough and the old way can be fully replaced.

---

## XIII. Code Should Be Obvious

### Goal
- A reader should be able to quickly understand the behavior and intent of code without significant mental effort.
- Obviousness is the ultimate test of good design.

### Techniques for Obvious Code
- Good naming and consistency.
- Judicious use of whitespace and formatting to reveal structure.
- Comments that explain the non-obvious.
- Avoid implicit control flow in event-driven code (unless necessary).

### Non-Obvious Code 🚩 Red Flag
- If a reader cannot easily understand the behavior or meaning of a piece of code, it is not obvious enough.

---

## XIV. Red Flags Quick Reference

Use these signals during code reviews and self-reviews:

| Signal | Meaning |
|--------|---------|
| **Shallow Module** | Interface is nearly as complex as its implementation |
| **Information Leakage** | Same design decision reflected in multiple modules |
| **Temporal Decomposition** | Modules split by execution order, not information hiding |
| **Overexposure** | Common API forces callers to know about rarely-used features |
| **Pass-Through Method** | Method just forwards args to another method with similar signature |
| **Repetition** | Non-trivial code duplicated across locations |
| **Special-General Mixture** | General-purpose and special-purpose code not cleanly separated |
| **Conjoined Methods** | Understanding one method requires understanding another |
| **Comment Repeats Code** | Comment is just an English translation of the code |
| **Impl Contaminates Interface** | Interface docs expose implementation details users don't need |
| **Vague Name** | Name too generic to convey useful information |
| **Hard to Pick Name** | Can't find a precise, intuitive name — design may be flawed |
| **Hard to Describe** | Documentation must be long to be complete — module may be too complex |
| **Non-Obvious Code** | Behavior or meaning of code is not easily understood |

---

## XV. Design Principles Summary

1. Complexity is incremental — sweat the small stuff.
2. Working code isn't enough.
3. Make continual small investments to improve system design.
4. Modules should be deep.
5. Interfaces should make the most common usage as simple as possible.
6. A simple interface matters more than a simple implementation.
7. General-purpose modules are deeper.
8. Separate general-purpose and special-purpose code.
9. Different layers should have different abstractions.
10. Pull complexity downward.
11. Define errors (and special cases) out of existence.
12. Design it twice.
13. Comments should describe things not obvious from the code.
14. Software should be designed for ease of reading, not ease of writing.
15. The increments of software development should be abstractions, not features.

---

## Usage Guide

Reference this guide in the following scenarios:

- **Code review**: Use the Red Flags quick reference to spot design problems.
- **API/Interface design**: Aim for deep modules; ensure interfaces are simple for common usage.
- **Module decomposition**: Split based on information hiding, not execution order or line count.
- **Error handling**: Prefer "define errors out of existence" to reduce exception propagation.
- **Refactoring**: Spend 10–20% of each change improving surrounding design.
- **Naming and comments**: Names should be precise; comments should describe what the code doesn't show.
