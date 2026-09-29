---
name: split-or-join
description: "Decide whether two pieces of code (functions, methods, classes, modules, services) belong together or apart, using Ousterhout's rules from \"A Philosophy of Software Design\" (ch. 5, 7, 9) — shared information, interface simplicity, general vs special purpose, conjoined methods, pass-through layers. Use when the user asks whether to extract, split, or merge a function or class, says a method is too long, there are too many small classes, asks where some code should live, or has wrappers, decorators, or parameters passed through many layers. Not for a full design review (complexity-review) or designing a new interface (design-it-twice)."
---

# Split or Join

Aim for the structure with the best information hiding, the fewest dependencies, and the deepest interfaces. Splitting has costs of its own: more interfaces, glue code, distance between related code, and duplication. **Length alone is never a reason to split.**

## Join when

- **They share information.** Both know the same format, protocol, or rule. Reading and parsing an HTTP request are one example.
- **Joining simplifies the interface.** The intermediate hand-off disappears, or a feature becomes automatic. Example: buffering built into file input instead of a separate class.
- **It removes duplication.** Factor out repeated code, or restructure so the snippet runs in only one place.
- **They're conjoined.** You can't understand one without reading the other. That is a split gone wrong.
- **They were split by time order** (read, then modify, then write) but share knowledge. That is temporal decomposition. Group by knowledge, not sequence.
- **They're used together in both directions.** A one-way relationship doesn't count: a block cache uses a hash table, but a hash table stands alone.

## Split when

- **General and special-purpose code are mixed.** The mechanism keeps the general part, and the use-specific code moves up to the caller or down into plug-ins. Example: History handles generic undo, while each text or selection action implements its own undo.
- **The pieces are truly independent.** Readers can focus on one at a time without flipping back and forth.

## Splitting a method

Split a method only in one of these two forms:

1. **Extract a subtask.** The child can be read without the parent and vice versa. Ideally the child is general enough to reuse. If you find yourself flipping between them, undo the split.
2. **Split into two public methods.** Only if the original did unrelated things and most callers need just one of the new methods. If callers must call both and pass state between them, don't split.

A deep 100-line method with a simple signature that reads well block by block is fine.

## Layer smells

- **Pass-through method.** Fix it in one of three ways: let callers use the lower layer directly, redistribute responsibilities, or merge the classes. Dispatchers and multiple implementations of one interface are fine.
- **Decorator or wrapper.** Before adding one, consider putting the feature into the base class (if most users want it), into the use case, into an existing decorator, or into a standalone class.
- **Pass-through variable.** Store it in an object that both ends already share, or in a context object that major objects hold a reference to. Avoid globals.
- **Interface mirrors the representation.** Line-based storage doesn't require a line-based API. The difference between the two is where the depth comes from.

## Output

```
Verdict: join | split (subtask | two methods | general/special) | keep
Rule: <which signal above, with the concrete evidence>
Shape: new signatures or module boundaries, briefly
```
