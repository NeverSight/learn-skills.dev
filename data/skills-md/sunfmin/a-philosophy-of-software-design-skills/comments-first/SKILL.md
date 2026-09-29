---
name: comments-first
description: "Write interface comments before implementation and use them as a design probe, audit existing code comments and doc comments, or choose precise names for variables, methods, and types (Ousterhout's \"A Philosophy of Software Design\"). Use when the user asks to write or improve comments or docstrings, says \"comments first\", suspects comments just repeat the code, or struggles to pick a good name for a variable, function, or type. Not for README, changelog, or user-facing docs."
---

# Comments First

Comments hold what was in the designer's head but can't live in code. Without an interface comment there is no abstraction: callers have to read the body.

## Mode A — new code (comments first)

1. Class or module interface comment: what abstraction it provides, what one instance represents, and its limits.
2. Signatures plus interface comments for the main public methods. Leave the bodies empty.
3. Iterate on those comments until they are short and complete. **If a comment can't be both, the design is wrong.** Fix the design, not the prose.
4. Comment the key fields, then write the bodies. Every new method gets its comment before its body.

## Mode B — audit existing code

Check in this order:

- **Interface comment** gives the caller-visible behavior, each argument and return value (precisely), side effects, errors, and preconditions. A caller should never need to read the body.
- **No implementation in the interface comment.** Internals belong inside the body.
- **Doesn't repeat code.** Test: could someone write this comment from the adjacent line alone? Use different words from the name.
- **Precision for fields and parameters**: units, inclusive or exclusive bounds, what null means, who frees or closes it, invariants. Describe what it *is* (nouns), not how code toggles it.
- **Implementation comments** explain *what* a block does and *why*, not *how*. Put one before each major phase or complex loop.
- **Cross-module rules** go in one place that people will find: the enum everyone edits, or a `designNotes` section referenced with `// See "X" in designNotes`.
- **Code, not commit log.** If a future reader needs the "why", put it in the code.
- **Maintenance.** Keep each comment next to the code it describes, document each fact once, and check the diff for stale comments before committing.

## Names

- **Create an image.** Seen alone, does the name let the reader guess what it is? Aim for 1–3 words.
- **Precise over generic.** Prefer `numActiveIndexlets` to `count`, `cursorVisible` to `blinkStatus`. Booleans are predicates.
- **Consistent.** One name per concept and one concept per name. If two kinds of the same thing exist, distinguish them (`fileBlock` vs `diskBlock`), ideally with distinct types.
- Name length grows with the distance between declaration and use. `i` is fine in a 3-line loop.
- **Hard to pick a name** means the thing probably has no clean definition. Split it.

## Output

In Mode A, the skeleton: comments and signatures, no bodies. In Mode B, `path:line — problem → rewritten comment or name`, plus a list of any design smells the comments exposed.
