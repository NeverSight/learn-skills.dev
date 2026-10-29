---
name: codebase-design
description: Shared vocabulary for designing deep modules. Use when designing or improving a module interface, finding deepening opportunities, deciding a seam, improving testability or AI navigability, or supporting an architecture review.
---

# Codebase Design

Design **deep modules**: substantial behavior behind a small interface, placed at a
clean seam and tested through that interface. The aim is leverage for callers,
locality for maintainers, and testability for everyone.

## Vocabulary

Use these terms exactly. Do not substitute component, service, API, boundary, or unit
when one of these terms applies.

- **Module**: anything with an interface and implementation, regardless of scale.
- **Interface**: everything a caller must know to use a module correctly: types,
  invariants, ordering, errors, configuration, and performance characteristics.
- **Implementation**: the code inside a module. Use **adapter** when discussing a
  concrete thing that fills a seam.
- **Depth**: leverage at the interface. A deep module hides substantial behavior behind
  a small interface; a shallow module exposes an interface nearly as complex as its
  implementation.
- **Seam**: where behavior can change without editing that location; the location of a
  module interface.
- **Adapter**: a concrete implementation of an interface at a seam.
- **Leverage**: capability callers gain per unit of interface they learn.
- **Locality**: the concentration of change, bugs, knowledge, and verification in one
  place rather than across callers.

## Principles

- Depth is a property of the interface, not implementation size.
- Apply the deletion test: if deleting a module makes complexity reappear across its
  callers, it earns its keep.
- The interface is the test surface. Tests and callers cross the same seam.
- One adapter is a hypothetical seam; two adapters make it real.

When deepening a cluster with dependencies, read `DEEPENING.md` for dependency
categories, seam discipline, and replace-not-layer testing. When the user wants to
compare alternative interfaces, read `DESIGN-IT-TWICE.md` for the parallel design
process.
