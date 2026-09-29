---
name: simple-code
description: "Define simple code for architecture, implementation, and review: clear responsibilities, direct data flow, justified abstraction, and explicit effects."
---

# Simple code

Build complex software from simple parts. Code is simple when a reader can understand its purpose, data flow, and effects without holding unrelated context in mind. Optimize for code that remains easy to change through repeated refactoring, not for the fewest lines.

## Clear parts

- Give each function one clear purpose, each type one clear concept, and each module one clear responsibility.
- Prefer direct data flow and obvious control flow. Follow the principle of least surprise in names, behaviour, and structure.
- Prefer straightforward code over clever machinery, generic frameworks, extra layers, and unnecessary indirection.
- Add an abstraction for a concrete current need. Several real cases can reveal a shared concept; predicted reuse alone does not establish one.
- Do not add interfaces, dependency injection layers, wrappers, or other abstractions only for hypothetical substitution or easier testing. Require a current responsibility that removes more reasoning than the abstraction adds.
- Do not pursue DRY as a goal by itself. Duplication is reasonable when divergence cannot silently become wrong. The compiler or tests can make a missed corresponding change visible, while separate concepts may rightly change independently.
- Parse weak or external input into meaningful domain types at system boundaries. Let internal code rely on established invariants instead of repeating validation.

## Visible effects

- Prefer pure, total functions for decisions when practical. A total function defines a result for every valid input and does not rely on a panic, abort, or hidden precondition.
- Normally return expected failures as values instead of throwing exceptions or panicking. Keep dependencies explicit.
- Make I/O, persistence, networking, time, randomness, shared mutation, and other effects visible in signatures, structure, or names. Do not hide an external action behind a helper that appears to calculate a value.
- Keep effectful regions small and give mutation narrow ownership. Separate deciding what should happen from performing an effect when the split makes the code easier to understand.
- Use effect information that the language exposes, such as `async`, and make remaining effects clear through structure and naming.

Apply these principles with judgment. A separation or abstraction should remove more reasoning than it adds.
