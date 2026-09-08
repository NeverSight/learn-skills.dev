---
name: code
description: Code design practices.
---

# Code

- Prefer clear ownership, explicit boundaries, and minimal coordination.
- Resolve competing principles in favor of correctness and understandability.

## Relevant skills

- Working on UI? Refer to [$ui](../ui/SKILL.md).
- Working on React? Refer to [$react](../react/SKILL.md).
- Working on layout? Refer to [$layout](../layout/SKILL.md).
- For folder structure, refer to [$folder-structure](../folder-structure/SKILL.md).

## Design

- Keep related logic and knowledge together.
- Keep dependencies explicit.
- Hide substantial complexity behind small interfaces, even across multiple files. (Deep Modules)
- Encapsulate decisions so callers do not need to understand or repeat them.
- Separate responsibilities; keep each boundary's internals together.
- Prefer existing capabilities over parallel implementations.
- Enforce boundaries with abstractions, even with one implementation.
- Keep similar code separate when its rules or reasons to change differ.
- Remove pass-through abstractions that neither protect boundaries nor hide complexity.
- Retain abstractions that prevent complexity from spreading into callers.
- Minimize the knowledge and coordination required from callers.
- Optimize for understandable code and localized changes.

## Extensibility

- Prefer composition.
- Accept replaceable dependencies.
- Remove unnecessary coupling that blocks extension.
- Add variants through contracts; avoid concrete-type branches in consumers.
- Revise contracts when their responsibilities change.
- Keep integration details out of core rules.
- Centralize wiring when multiple implementations need selection.
- Require interfaces, factories, and layers to enforce contracts, own policies, or isolate integrations.

## Implementation

- Represent each fact once; derive values instead of duplicating state.
- Make invalid states difficult to represent.
- Validate at boundaries; rely on enforced contracts internally.
- Handle failures explicitly; do not disguise them as successful results.
- Add dependencies only when their benefit justifies their cost.
- Explain non-obvious constraints and decisions in comments.
- Avoid compatibility paths unless compatibility is required.
