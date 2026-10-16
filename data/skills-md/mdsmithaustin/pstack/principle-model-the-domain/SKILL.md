---
name: principle-model-the-domain
description: "Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files."
---

# Model the Domain

Encode the real domain in a data structure instead of scattering it across conditionals. A structure that matches the domain makes invalid states unrepresentable and deletes branches. Choosing it at write time is cheap. Recovering it later reads as a refactor and gets deferred.

Reach for:

- A state machine instead of scattered booleans, phases, or lifecycle checks.
- A typed model instead of loose parameters or repeated shape assumptions.
- A map, registry, lookup table, or discriminated union instead of branching spread across files.
- A reducer or command/event model instead of ad hoc state mutations.
- A module organized around one body of domain knowledge instead of a sequence such as load, validate, transform, and save. Execution order is not ownership.
- A small module boundary that gathers repeated behavior, ownership, or invariants.
- A queue, cache, index, graph, tree, or normalized collection where the access pattern calls for it.
- Any other structure that fits. When none fits, work out what the code must never allow and how the data gets read, then find the structure that encodes exactly that.

**Use the domain's words.** Name types, functions, and modules with the words the domain uses. Before you name anything, read the nearest glossary if one exists, such as a `CONTEXT.md` or a glossary in the project's docs, and use its terms. Never use a word the glossary marks as one to avoid. Name an operation by the effect it has in the domain, not by the mechanism that performs it.

Do not force an abstraction. Prefer boring code if the current shape is already clear, local, and unlikely to grow. Be skeptical of an abstraction that adds indirection without removing branches, duplicated rules, invalid states, or lifecycle risk.

The sign that you skipped this is a new feature that grows an existing if/else chain by one more branch, or a second boolean that must stay in sync with the first. Temporal decomposition is another sign. Phase-named modules repeat the same domain rules across steps.

**In review.** When you review someone else's change, also check these three.

- **One name per concept.** Flag a new name for a concept the code already names. The fix direction is to keep the code's word.
- **Separate contexts.** One word can name different concepts in two parts of the codebase. Flag a change that combines them into one type whose fields are optional per meaning. The fix direction is a separate type in each part that shares only what means the same thing in both, such as an id. Convergence applies to one concept, not to one word.
- **Shared code answers to every caller.** List the callers of each shared function, type, or constant the change touches. Flag a change made for one request that alters behavior for a caller serving a different business function. The fix direction is to fork the shared piece and change only the requester's path. Look-alike code that different business functions change is two decisions, so do not ask to merge it.
