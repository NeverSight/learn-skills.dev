---
name: blast-radius
description: Find non-local breakage from a change and prove the decisive safety invariant with executable evidence. Use for blast radius, what could this break, or a suspicious small diff.
---

# Blast radius

Find what a change can break beyond its diff. Listing callers is reconnaissance, not the result. The result is the one fact the change is safe because of, proven as directly as practical.

## Contract

- **Fixed point:** review the requested base through current working state unless the caller supplies another point.
- **Fence:** inspect non-local contracts and run verification; do not edit product code.
- **Question:** what hidden consumer, lifecycle, wire shape, shared state, or external contract can turn this change into a defect?

## Proof ladder

Move each safety fact down this ladder as cheaply as possible: source line -> walked counterexample -> executable script or test -> real running entrypoint. A claim below executable proof is **unproven**, not safe by confidence.

## Pass

1. Read the complete change, changed symbols, call sites, producers, consumers, schemas, and public surfaces. State what behavior differs, including implicit timing and lifecycle changes.
2. Name the decisive safety invariant. Prefer one fact that clears several speculative risks, such as "the operation only removes expired entries and is otherwise inert."
3. Look where symbol search stops: serialized data, database columns, feature flags, another language, library source at the pinned version, teardown order, retries, concurrency, and callers reached through configuration.
4. Build the smallest credible failure path. Separate confirmed risks from checked-and-cleared paths. Cite exact evidence; a search that finds nothing is evidence only when the searched scope is complete.
5. Prove the invariant through the real code. Add a disposable script or focused public-contract test when that is the cheapest executable check. Do not keep a test that only repeats source text.
6. If the running user path is available, exercise it through `/dogfood`. Record where each fact stopped on the proof ladder.

## Output

- **Change:** observable semantic difference.
- **Safety invariant:** exact fact, proof rung, command, and observation; otherwise `unproven`.
- **Risks:** failure path, likelihood, impact, evidence, and cheapest check.
- **Cleared:** paths checked and the evidence that clears them.
- **Before merge:** smallest command or reproduction that fails if the invariant is false.

Keep risks evidence-backed and bounded. Do not inflate a list of possibilities after the decisive invariant has been proven.
