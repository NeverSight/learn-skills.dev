---
name: ds-blueprint
description: "Design the types, function signatures and module layout first, agree on that shape, then implement against it. Use when work is non-trivial and coding straight away would lock in the wrong structure, or for /ds-blueprint, 'design this first', 'architect this'."
---

# ds-blueprint

Fix the shape of the code before writing the bodies, so the model fills in a plan instead of inventing one as it goes.

## Steps

1. Ground yourself. Read every module the new code will touch. If you cannot explain how they fit together, run /ds-explain first. Skip this only for code with no surrounding system.
2. Write at least two structurally different sketches. Each sketch is real files with types, signatures, module boundaries and stub bodies that raise "not implemented", plus short pseudocode. Use /ds-best-of-n to produce them in parallel when the design matters.
3. Compare the sketches. Prefer the one with the smaller public surface that hides more inside. Prefer the one where a change that looks right from a single file is also right for the whole repo. Note what you rejected and why.
4. Run the type checker or compiler on the chosen sketch. Paste the output. Stubs must compile.
5. Show the user the chosen sketch and wait for agreement before you fill in bodies. In an unattended run, record the choice with /ds-ledger instead.
6. Implement one stub at a time. After each, run the type checker and the relevant tests. If the sketch turns out wrong, stop and revise the sketch, not just the body.
7. Delete leftover stubs, dead sketches and unused types. Grep for "not implemented" to prove none remain.

## Stop when

- Every stub is implemented, the type checker passes and the tests pass, with output shown.
- Or the sketch needed three revisions during implementation. Stop and redesign with the user.

## Rules

- Signatures change only through step 6's revise path, never silently.
- Keep each sketch file small enough to read in one pass.
- Evidence is compiler and test output, not "it should work".
