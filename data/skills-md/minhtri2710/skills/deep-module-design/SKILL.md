---
name: deep-module-design
description: Design or deepen a module's interface and seam placement using the deep-module vocabulary. Use when the user wants to design a module interface, decide where a seam goes, find deepening opportunities in a named area, or compare alternative interfaces. Do not use for a whole-project archetype audit.
---

# Deep Module Design

A deep module puts a lot of behavior behind a small interface at a clean seam,
testable through that interface. Depth gives callers leverage and maintainers
locality. Use the terms below exactly in every proposal.

## Vocabulary

- **Module**: anything with an interface and an implementation — function, class,
  package, or a slice spanning tiers.
- **Interface**: everything a caller must know to use the module correctly: types,
  invariants, ordering constraints, error modes, required configuration, and
  performance characteristics.
- **Depth**: behavior a caller or test can exercise per unit of interface learned.
  Shallow means the interface is nearly as complex as the implementation.
- **Seam**: the place where behavior can change without editing that place; where
  the interface lives. Choosing it is its own decision.
- **Adapter**: a concrete thing that fills an interface at a seam; a role, not a
  size.
- **Leverage**: capability callers gain per unit of interface.
- **Locality**: change, bugs, and verification concentrated in one place.

## Principles

- Depth belongs to the interface. A deep module may be built from small internal
  parts with internal seams its own tests use; those stay out of the interface.
- Deletion test: imagine deleting the module. If complexity vanishes, it was a
  pass-through; if it reappears across callers, it earns its keep.
- The interface is the test surface. Needing to test past it means the module is
  the wrong shape.
- One adapter is a hypothetical seam; two adapters make it real. Add a port only
  when at least two adapters exist now, typically production and test.
- Testable interfaces accept dependencies instead of constructing them, return
  results instead of mutating arguments, and keep the surface small.

## Deepening a cluster

Classify each dependency; the category decides how the deepened module is tested:

1. In-process (pure computation, in-memory state): merge and test through the new
   interface directly.
2. Local-substitutable (a local stand-in exists, such as PGLite or an in-memory
   filesystem): test with the stand-in running; the seam stays internal.
3. Remote but owned (your own services over a network): define a port at the seam,
   with a transport adapter for production and an in-memory adapter for tests.
4. True external (third-party services): inject the dependency as a port and give
   tests a mock adapter.

Replace, don't layer: once tests exist at the deepened interface, delete the old
tests of the shallow modules in the same change.

When scanning a named area for candidates, weight files that recur in recent
`git log`, apply the deletion test to each suspect, read `CONTEXT.md` and ADRs
first, and surface a candidate that contradicts an ADR only when the friction
justifies reopening it. For each candidate report the files, the friction, the
proposed change, the leverage and locality gained, how tests change, and a
strength of `strong`, `worth exploring`, or `speculative`. Propose interfaces only
after the user picks a candidate.

## Design it twice

To compare interfaces for a chosen candidate, first write the constraints, the
dependency categories, and a rough sketch that grounds them. Then brief 3 or more
parallel subagents with the file paths, coupling details, dependency categories,
and this vocabulary, each under a different constraint:

- minimize the interface to 1-3 entry points;
- maximize flexibility across use cases;
- make the most common caller trivial;
- design around ports and adapters for cross-seam dependencies, when relevant.

Each returns the interface with invariants and error modes, a caller example, what
hides behind the seam, the dependency strategy, and where leverage is thin. Compare
the designs by depth, locality, and seam placement, then give one recommendation,
proposing a hybrid when parts combine well.
